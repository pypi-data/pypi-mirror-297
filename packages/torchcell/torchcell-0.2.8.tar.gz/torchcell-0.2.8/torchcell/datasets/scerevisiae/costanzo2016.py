# torchcell/datasets/scerevisiae/costanzo2016
# [[torchcell.datasets.scerevisiae.costanzo2016]]
# https://github.com/Mjvolk3/torchcell/tree/main/torchcell/datasets/scerevisiae/costanzo2016
# Test file: tests/torchcell/datasets/scerevisiae/test_costanzo2016.py
import logging
import os
import os.path as osp
import pickle
import shutil
import zipfile
from collections.abc import Callable
import lmdb
import pandas as pd
from torch_geometric.data import download_url
from tqdm import tqdm
from torchcell.datamodels import (
    Environment,
    Genotype,
    FitnessExperiment,
    FitnessExperimentReference,
    FitnessPhenotype,
    Media,
    ReferenceGenome,
    SgaKanMxDeletionPerturbation,
    SgaNatMxDeletionPerturbation,
    SgaDampPerturbation,
    SgaSuppressorAllelePerturbation,
    SgaTsAllelePerturbation,
    Temperature,
    Experiment,
    ExperimentReference,
    GeneInteractionPhenotype,
    GeneInteractionExperimentReference,
    GeneInteractionExperiment,
    Publication,
)
from torchcell.data import ExperimentDataset, post_process
from concurrent.futures import ThreadPoolExecutor
from torchcell.datasets.dataset_registry import register_dataset

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# Fitness
@register_dataset
class SmfCostanzo2016Dataset(ExperimentDataset):
    url = (
        "https://thecellmap.org/costanzo2016/data_files/"
        "Raw%20genetic%20interaction%20datasets:%20Pair-wise%20interaction%20format.zip"
    )

    def __init__(
        self,
        root: str = "data/torchcell/smf_costanzo2016",
        io_workers: int = 0,
        transform: Callable | None = None,
        pre_transform: Callable | None = None,
        **kwargs,
    ):
        super().__init__(root, io_workers, transform, pre_transform, **kwargs)

    @property
    def experiment_class(self) -> Experiment:
        return FitnessExperiment

    @property
    def reference_class(self) -> ExperimentReference:
        return FitnessExperimentReference

    @property
    def raw_file_names(self) -> str:
        return "strain_ids_and_single_mutant_fitness.xlsx"

    def download(self):
        path = download_url(self.url, self.raw_dir)
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(self.raw_dir)
        os.remove(path)

        # Move the contents of the subdirectory to the parent raw directory
        sub_dir = os.path.join(
            self.raw_dir,
            "Data File S1. Raw genetic interaction datasets: Pair-wise interaction format",
        )
        for filename in os.listdir(sub_dir):
            shutil.move(os.path.join(sub_dir, filename), self.raw_dir)
        os.rmdir(sub_dir)
        # remove any excess files not needed
        for file_name in os.listdir(self.raw_dir):
            # if the file name ends in .txt remove it
            if file_name.endswith(".txt"):
                os.remove(osp.join(self.raw_dir, file_name))

    @post_process
    def process(self):
        xlsx_path = osp.join(self.raw_dir, "strain_ids_and_single_mutant_fitness.xlsx")
        df = pd.read_excel(xlsx_path)
        df = self.preprocess_raw(df)
        (phenotype_reference_std_26, phenotype_reference_std_30) = (
            self.compute_phenotype_reference_std(df)
        )

        # Save preprocssed df - mainly for quick stats
        os.makedirs(self.preprocess_dir, exist_ok=True)
        df.to_csv(osp.join(self.preprocess_dir, "data.csv"), index=False)

        log.info("Processing SMF Files...")

        # Initialize LMDB environment
        env = lmdb.open(
            osp.join(self.processed_dir, "lmdb"),
            map_size=int(1e12),  # Adjust map_size as needed
        )

        with env.begin(write=True) as txn:
            for index, row in tqdm(df.iterrows(), total=df.shape[0]):
                experiment, reference, publication = self.create_experiment(
                    self.name,
                    row,
                    phenotype_reference_std_26=phenotype_reference_std_26,
                    phenotype_reference_std_30=phenotype_reference_std_30,
                )

                # Serialize the Pydantic objects
                serialized_data = pickle.dumps(
                    {
                        "experiment": experiment.model_dump(),
                        "reference": reference.model_dump(),
                        "publication": publication.model_dump(),
                    }
                )
                txn.put(f"{index}".encode(), serialized_data)

        env.close()

    def preprocess_raw(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Strain_ID_suffix"] = df["Strain ID"].str.split("_", expand=True)[1]

        # Determine perturbation type based on Strain_ID_suffix
        df["perturbation_type"] = df["Strain_ID_suffix"].apply(
            lambda x: (
                "damp"
                if "damp" in x
                else (
                    "temperature_sensitive"
                    if "tsa" in x or "tsq" in x
                    else (
                        "KanMX_deletion"
                        if "dma" in x
                        else (
                            "NatMX_deletion"
                            if "sn" in x  # or "S" in x or "A_S" in x
                            else "suppression_allele" if "S" in x else "unknown"
                        )
                    )
                )
            )
        )

        # Create separate dataframes for the two temperatures
        df_26 = df[
            [
                "Strain ID",
                "Systematic gene name",
                "Allele/Gene name",
                "Single mutant fitness (26°)",
                "Single mutant fitness (26°) stddev",
                "perturbation_type",
            ]
        ].copy()
        df_26["Temperature"] = 26

        df_30 = df[
            [
                "Strain ID",
                "Systematic gene name",
                "Allele/Gene name",
                "Single mutant fitness (30°)",
                "Single mutant fitness (30°) stddev",
                "perturbation_type",
            ]
        ].copy()
        df_30["Temperature"] = 30

        # Rename the columns for fitness and stddev to be common for both dataframes
        df_26.rename(
            columns={
                "Single mutant fitness (26°)": "Single mutant fitness",
                "Single mutant fitness (26°) stddev": "Single mutant fitness stddev",
            },
            inplace=True,
        )

        df_30.rename(
            columns={
                "Single mutant fitness (30°)": "Single mutant fitness",
                "Single mutant fitness (30°) stddev": "Single mutant fitness stddev",
            },
            inplace=True,
        )

        # Concatenate the two dataframes
        combined_df = pd.concat([df_26, df_30], ignore_index=True)
        combined_df = combined_df.dropna()
        combined_df = combined_df.drop_duplicates()
        combined_df = combined_df.reset_index(drop=True)

        return combined_df

    @staticmethod
    def compute_phenotype_reference_std(df: pd.DataFrame):
        mean_stds = df.groupby("Temperature")["Single mutant fitness stddev"].mean()
        phenotype_reference_std_26 = mean_stds[26]
        phenotype_reference_std_30 = mean_stds[30]
        return phenotype_reference_std_26, phenotype_reference_std_30

    @staticmethod
    def create_experiment(
        dataset_name, row, phenotype_reference_std_26, phenotype_reference_std_30
    ):
        # Common attributes for both temperatures
        genome_reference = ReferenceGenome(
            species="Saccharomyces cerevisiae", strain="S288C"
        )

        # Deal with different types of perturbations
        if "temperature_sensitive" in row["perturbation_type"]:
            genotype = Genotype(
                perturbations=[
                    SgaTsAllelePerturbation(
                        systematic_gene_name=row["Systematic gene name"],
                        perturbed_gene_name=row["Allele/Gene name"],
                        strain_id=row["Strain ID"],
                    )
                ]
            )
        elif "damp" in row["perturbation_type"]:
            genotype = Genotype(
                perturbations=[
                    SgaDampPerturbation(
                        systematic_gene_name=row["Systematic gene name"],
                        perturbed_gene_name=row["Allele/Gene name"],
                        strain_id=row["Strain ID"],
                    )
                ]
            )
        elif "KanMX_deletion" in row["perturbation_type"]:
            genotype = Genotype(
                perturbations=[
                    SgaKanMxDeletionPerturbation(
                        systematic_gene_name=row["Systematic gene name"],
                        perturbed_gene_name=row["Allele/Gene name"],
                        strain_id=row["Strain ID"],
                    )
                ]
            )
        elif "NatMX_deletion" in row["perturbation_type"]:
            genotype = Genotype(
                perturbations=[
                    SgaNatMxDeletionPerturbation(
                        systematic_gene_name=row["Systematic gene name"],
                        perturbed_gene_name=row["Allele/Gene name"],
                        strain_id=row["Strain ID"],
                    )
                ]
            )
        elif "suppression_allele" in row["perturbation_type"]:
            genotype = Genotype(
                perturbations=[
                    SgaSuppressorAllelePerturbation(
                        systematic_gene_name=row["Systematic gene name"],
                        perturbed_gene_name=row["Allele/Gene name"],
                        strain_id=row["Strain ID"],
                    )
                ]
            )

        environment = Environment(
            media=Media(name="YEPD", state="solid"),
            temperature=Temperature(value=row["Temperature"]),
        )
        environment_reference = environment.model_copy()
        # Phenotype based on temperature
        smf_key = "Single mutant fitness"
        smf_std_key = "Single mutant fitness stddev"
        phenotype = FitnessPhenotype(fitness=row[smf_key], std=row[smf_std_key])

        if row["Temperature"] == 26:
            phenotype_reference_std = phenotype_reference_std_26
        elif row["Temperature"] == 30:
            phenotype_reference_std = phenotype_reference_std_30
        phenotype_reference = FitnessPhenotype(fitness=1.0, std=phenotype_reference_std)

        reference = FitnessExperimentReference(
            dataset_name=dataset_name,
            genome_reference=genome_reference,
            environment_reference=environment_reference,
            phenotype_reference=phenotype_reference,
        )

        experiment = FitnessExperiment(
            dataset_name=dataset_name,
            genotype=genotype,
            environment=environment,
            phenotype=phenotype,
        )

        publication = Publication(
            pubmed_id="27708008",
            pubmed_url="https://pubmed.ncbi.nlm.nih.gov/27708008/",
            doi="10.1126/science.aaf1420",
            doi_url="https://www.science.org/doi/10.1126/science.aaf1420",
        )

        return experiment, reference, publication


@register_dataset
class DmfCostanzo2016Dataset(ExperimentDataset):
    url = (
        "https://thecellmap.org/costanzo2016/data_files/"
        "Raw%20genetic%20interaction%20datasets:%20Pair-wise%20interaction%20format.zip"
    )

    def __init__(
        self,
        root: str = "data/torchcell/smf_costanzo2016",
        subset_n: int = None,
        batch_size: int = int(1e4),
        io_workers: int = 1,
        transform: Callable | None = None,
        pre_transform: Callable | None = None,
        **kwargs,
    ):
        self.io_workers = io_workers
        self.subset_n = subset_n
        self.batch_size = batch_size
        super().__init__(root, io_workers, transform, pre_transform, **kwargs)

    def download(self):
        path = download_url(self.url, self.raw_dir)
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(self.raw_dir)
        os.remove(path)

        # Move the contents of the subdirectory to the parent raw directory
        sub_dir = os.path.join(
            self.raw_dir,
            "Data File S1. Raw genetic interaction datasets: Pair-wise interaction format",
        )
        for filename in os.listdir(sub_dir):
            shutil.move(os.path.join(sub_dir, filename), self.raw_dir)
        os.rmdir(sub_dir)
        # remove any excess files not needed
        os.remove(osp.join(self.raw_dir, "strain_ids_and_single_mutant_fitness.xlsx"))

    @property
    def experiment_class(self) -> Experiment:
        return FitnessExperiment

    @property
    def reference_class(self) -> ExperimentReference:
        return FitnessExperimentReference

    @property
    def raw_file_names(self) -> list[str]:
        return ["SGA_DAmP.txt", "SGA_ExE.txt", "SGA_ExN_NxE.txt", "SGA_NxN.txt"]

    def preprocess_raw(self, df: pd.DataFrame, preprocess: dict | None = None):
        log.info("Preprocess on raw data...")

        # Function to extract gene name
        def extract_systematic_name(x):
            return x.apply(lambda y: y.split("_")[0])

        # Extract gene names
        df["Query Systematic Name"] = extract_systematic_name(df["Query Strain ID"])
        df["Array Systematic Name"] = extract_systematic_name(df["Array Strain ID"])
        Temperature = df["Arraytype/Temp"].str.extract("(\d+)").astype(int)
        df["Temperature"] = Temperature
        df["query_perturbation_type"] = df["Query Strain ID"].apply(
            lambda x: (
                "damp"
                if "damp" in x
                else (
                    "temperature_sensitive"
                    if "tsa" in x or "tsq" in x
                    else (
                        "KanMX_deletion"
                        if "dma" in x
                        else (
                            "NatMX_deletion"
                            if "sn" in x  # or "S" in x or "A_S" in x
                            else "suppression_allele" if "S" in x else "unknown"
                        )
                    )
                )
            )
        )
        df["array_perturbation_type"] = df["Array Strain ID"].apply(
            lambda x: (
                "damp"
                if "damp" in x
                else (
                    "temperature_sensitive"
                    if "tsa" in x or "tsq" in x
                    else (
                        "KanMX_deletion"
                        if "dma" in x
                        else (
                            "NatMX_deletion"
                            if "sn" in x  # or "S" in x or "A_S" in x
                            else "suppression_allele" if "S" in x else "unknown"
                        )
                    )
                )
            )
        )
        means = df.groupby("Temperature")[
            "Double mutant fitness standard deviation"
        ].mean()

        # Extracting means for specific temperatures
        self.phenotype_reference_std_26 = means.get(26, None)
        self.phenotype_reference_std_30 = means.get(30, None)

        return df

    @post_process
    def process(self):
        os.makedirs(self.preprocess_dir, exist_ok=True)

        # Initialize an empty DataFrame to hold all raw data
        df = pd.DataFrame()

        # Read and concatenate all raw files
        log.info("Reading and Concatenating Raw Files...")
        for file_name in tqdm(self.raw_file_names):
            file_path = os.path.join(self.raw_dir, file_name)
            # Reading data using Pandas; limit rows for demonstration
            df_temp = pd.read_csv(file_path, sep="\t")
            # Concatenating data frames
            df = pd.concat([df, df_temp], ignore_index=True)

        # Functions for data filtering... duplicates selection,
        df = self.preprocess_raw(df)

        # Subset
        if self.subset_n is not None:
            df = df.sample(n=self.subset_n, random_state=42).reset_index(drop=True)

        # Save preprocssed df - mainly for quick stats
        df.to_csv(osp.join(self.preprocess_dir, "data.csv"), index=False)

        log.info("Processing DMF Files...")

        # Initialize LMDB environment
        env = lmdb.open(
            osp.join(self.processed_dir, "lmdb"),
            map_size=int(1e12),  # Adjust map_size as needed
        )

        # Create a ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.io_workers) as executor:
            futures = []
            for batch_start in range(0, df.shape[0], self.batch_size):
                batch_end = min(batch_start + self.batch_size, df.shape[0])
                batch_df = df.iloc[batch_start:batch_end]
                future = executor.submit(self._process_batch, batch_df, env)
                futures.append(future)

            # Wait for all futures to complete
            for future in tqdm(futures, total=len(futures)):
                future.result()

        env.close()

    def _process_batch(self, batch_df, env):
        with env.begin(write=True) as txn:
            for index, row in batch_df.iterrows():
                experiment, reference, publication = self.create_experiment(
                    self.name,
                    row,
                    phenotype_reference_std_26=self.phenotype_reference_std_26,
                    phenotype_reference_std_30=self.phenotype_reference_std_30,
                )

                # Serialize the Pydantic objects
                serialized_data = pickle.dumps(
                    {
                        "experiment": experiment.model_dump(),
                        "reference": reference.model_dump(),
                        "publication": publication.model_dump(),
                    }
                )

                txn.put(f"{index}".encode(), serialized_data)

    @staticmethod
    def create_experiment(
        dataset_name, row, phenotype_reference_std_26, phenotype_reference_std_30
    ):
        # Common attributes for both temperatures
        genome_reference = ReferenceGenome(
            species="Saccharomyces cerevisiae", strain="S288C"
        )
        # genotype
        perturbations = []
        # Query
        if "temperature_sensitive" in row["query_perturbation_type"]:
            perturbations.append(
                SgaTsAllelePerturbation(
                    systematic_gene_name=row["Query Systematic Name"],
                    perturbed_gene_name=row["Query allele name"],
                    strain_id=row["Query Strain ID"],
                )
            )
        elif "damp" in row["query_perturbation_type"]:
            perturbations.append(
                SgaDampPerturbation(
                    systematic_gene_name=row["Query Systematic Name"],
                    perturbed_gene_name=row["Query allele name"],
                    strain_id=row["Query Strain ID"],
                )
            )
        elif "KanMX_deletion" in row["query_perturbation_type"]:
            perturbations.append(
                SgaKanMxDeletionPerturbation(
                    systematic_gene_name=row["Query Systematic Name"],
                    perturbed_gene_name=row["Query allele name"],
                    strain_id=row["Query Strain ID"],
                )
            )

        elif "NatMX_deletion" in row["query_perturbation_type"]:
            perturbations.append(
                SgaNatMxDeletionPerturbation(
                    systematic_gene_name=row["Query Systematic Name"],
                    perturbed_gene_name=row["Query allele name"],
                    strain_id=row["Query Strain ID"],
                )
            )
        elif "suppression_allele" in row["query_perturbation_type"]:
            perturbations.append(
                SgaSuppressorAllelePerturbation(
                    systematic_gene_name=row["Query Systematic Name"],
                    perturbed_gene_name=row["Query allele name"],
                    strain_id=row["Query Strain ID"],
                )
            )

        # Array
        if "temperature_sensitive" in row["array_perturbation_type"]:
            perturbations.append(
                SgaTsAllelePerturbation(
                    systematic_gene_name=row["Array Systematic Name"],
                    perturbed_gene_name=row["Array allele name"],
                    strain_id=row["Array Strain ID"],
                )
            )
        elif "damp" in row["array_perturbation_type"]:
            perturbations.append(
                SgaDampPerturbation(
                    systematic_gene_name=row["Array Systematic Name"],
                    perturbed_gene_name=row["Array allele name"],
                    strain_id=row["Array Strain ID"],
                )
            )
        elif "KanMX_deletion" in row["array_perturbation_type"]:
            perturbations.append(
                SgaKanMxDeletionPerturbation(
                    systematic_gene_name=row["Array Systematic Name"],
                    perturbed_gene_name=row["Array allele name"],
                    strain_id=row["Array Strain ID"],
                )
            )

        elif "NatMX_deletion" in row["array_perturbation_type"]:
            perturbations.append(
                SgaNatMxDeletionPerturbation(
                    systematic_gene_name=row["Array Systematic Name"],
                    perturbed_gene_name=row["Array allele name"],
                    strain_id=row["Array Strain ID"],
                )
            )

        elif "suppression_allele" in row["array_perturbation_type"]:
            perturbations.append(
                SgaSuppressorAllelePerturbation(
                    systematic_gene_name=row["Array Systematic Name"],
                    perturbed_gene_name=row["Array allele name"],
                    strain_id=row["Array Strain ID"],
                )
            )
        genotype = Genotype(perturbations=perturbations)
        # genotype
        environment = Environment(
            media=Media(name="YEPD", state="solid"),
            temperature=Temperature(value=row["Temperature"]),
        )
        environment_reference = environment.model_copy()
        # Phenotype based on temperature
        dmf_key = "Double mutant fitness"
        dmf_std_key = "Double mutant fitness standard deviation"
        phenotype = FitnessPhenotype(fitness=row[dmf_key], std=row[dmf_std_key])

        if row["Temperature"] == 26:
            phenotype_reference_std = phenotype_reference_std_26
        elif row["Temperature"] == 30:
            phenotype_reference_std = phenotype_reference_std_30
        phenotype_reference = FitnessPhenotype(fitness=1.0, std=phenotype_reference_std)

        reference = FitnessExperimentReference(
            dataset_name=dataset_name,
            genome_reference=genome_reference,
            environment_reference=environment_reference,
            phenotype_reference=phenotype_reference,
        )

        experiment = FitnessExperiment(
            dataset_name=dataset_name,
            genotype=genotype,
            environment=environment,
            phenotype=phenotype,
        )

        publication = Publication(
            pubmed_id="27708008",
            pubmed_url="https://pubmed.ncbi.nlm.nih.gov/27708008/",
            doi="10.1126/science.aaf1420",
            doi_url="https://www.science.org/doi/10.1126/science.aaf1420",
        )

        return experiment, reference, publication


# Interactions
@register_dataset
class DmiCostanzo2016Dataset(ExperimentDataset):
    url = (
        "https://thecellmap.org/costanzo2016/data_files/"
        "Raw%20genetic%20interaction%20datasets:%20Pair-wise%20interaction%20format.zip"
    )

    def __init__(
        self,
        root: str = "data/torchcell/dmi_costanzo2016",
        subset_n: int = None,
        batch_size: int = int(1e4),
        io_workers: int = 1,
        transform: Callable | None = None,
        pre_transform: Callable | None = None,
        **kwargs,
    ):
        self.io_workers = io_workers
        self.subset_n = subset_n
        self.batch_size = batch_size
        super().__init__(root, io_workers, transform, pre_transform, **kwargs)

    def download(self):
        path = download_url(self.url, self.raw_dir)
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(self.raw_dir)
        os.remove(path)

        # Move the contents of the subdirectory to the parent raw directory
        sub_dir = os.path.join(
            self.raw_dir,
            "Data File S1. Raw genetic interaction datasets: Pair-wise interaction format",
        )
        for filename in os.listdir(sub_dir):
            shutil.move(os.path.join(sub_dir, filename), self.raw_dir)
        os.rmdir(sub_dir)
        # remove any excess files not needed
        os.remove(osp.join(self.raw_dir, "strain_ids_and_single_mutant_fitness.xlsx"))

    @property
    def experiment_class(self) -> ExperimentReference:
        return GeneInteractionExperiment

    @property
    def reference_class(self) -> ExperimentReference:
        return GeneInteractionExperimentReference

    @property
    def raw_file_names(self) -> list[str]:
        return ["SGA_DAmP.txt", "SGA_ExE.txt", "SGA_ExN_NxE.txt", "SGA_NxN.txt"]

    def preprocess_raw(self, df: pd.DataFrame, preprocess: dict | None = None):
        log.info("Preprocess on raw data...")

        # Function to extract gene name
        def extract_systematic_name(x):
            return x.apply(lambda y: y.split("_")[0])

        # Extract gene names
        df["Query Systematic Name"] = extract_systematic_name(df["Query Strain ID"])
        df["Array Systematic Name"] = extract_systematic_name(df["Array Strain ID"])
        Temperature = df["Arraytype/Temp"].str.extract("(\d+)").astype(int)
        df["Temperature"] = Temperature
        df["query_perturbation_type"] = df["Query Strain ID"].apply(
            lambda x: (
                "damp"
                if "damp" in x
                else (
                    "temperature_sensitive"
                    if "tsa" in x or "tsq" in x
                    else (
                        "KanMX_deletion"
                        if "dma" in x
                        else (
                            "NatMX_deletion"
                            if "sn" in x
                            else "suppression_allele" if "S" in x else "unknown"
                        )
                    )
                )
            )
        )
        df["array_perturbation_type"] = df["Array Strain ID"].apply(
            lambda x: (
                "damp"
                if "damp" in x
                else (
                    "temperature_sensitive"
                    if "tsa" in x or "tsq" in x
                    else (
                        "KanMX_deletion"
                        if "dma" in x
                        else (
                            "NatMX_deletion"
                            if "sn" in x
                            else "suppression_allele" if "S" in x else "unknown"
                        )
                    )
                )
            )
        )

        return df

    @post_process
    def process(self):
        os.makedirs(self.preprocess_dir, exist_ok=True)

        # Initialize an empty DataFrame to hold all raw data
        df = pd.DataFrame()

        # Read and concatenate all raw files
        log.info("Reading and Concatenating Raw Files...")
        for file_name in tqdm(self.raw_file_names):
            file_path = os.path.join(self.raw_dir, file_name)
            # Reading data using Pandas; limit rows for demonstration
            df_temp = pd.read_csv(file_path, sep="\t")
            # Concatenating data frames
            df = pd.concat([df, df_temp], ignore_index=True)

        # Functions for data filtering... duplicates selection,
        df = self.preprocess_raw(df)

        # Subset
        if self.subset_n is not None:
            df = df.sample(n=self.subset_n, random_state=42).reset_index(drop=True)

        # Save preprocssed df - mainly for quick stats
        df.to_csv(osp.join(self.preprocess_dir, "data.csv"), index=False)

        log.info("Processing DMI Files...")

        # Initialize LMDB environment
        env = lmdb.open(
            osp.join(self.processed_dir, "lmdb"),
            map_size=int(1e12),  # Adjust map_size as needed
        )

        # Create a ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.io_workers) as executor:
            futures = []
            for batch_start in range(0, df.shape[0], self.batch_size):
                batch_end = min(batch_start + self.batch_size, df.shape[0])
                batch_df = df.iloc[batch_start:batch_end]
                future = executor.submit(self._process_batch, batch_df, env)
                futures.append(future)

            # Wait for all futures to complete
            for future in tqdm(futures, total=len(futures)):
                future.result()

        env.close()

    def _process_batch(self, batch_df, env):
        with env.begin(write=True) as txn:
            for index, row in batch_df.iterrows():
                experiment, reference, publication = self.create_experiment(
                    self.name, row
                )

                # Serialize the Pydantic objects
                serialized_data = pickle.dumps(
                    {
                        "experiment": experiment.model_dump(),
                        "reference": reference.model_dump(),
                        "publication": publication.model_dump(),
                    }
                )

                txn.put(f"{index}".encode(), serialized_data)

    @staticmethod
    def create_experiment(dataset_name, row):
        genome_reference = ReferenceGenome(
            species="Saccharomyces cerevisiae", strain="S288C"
        )

        perturbations = []
        # Query
        if "temperature_sensitive" in row["query_perturbation_type"]:
            perturbations.append(
                SgaTsAllelePerturbation(
                    systematic_gene_name=row["Query Systematic Name"],
                    perturbed_gene_name=row["Query allele name"],
                    strain_id=row["Query Strain ID"],
                )
            )
        elif "damp" in row["query_perturbation_type"]:
            perturbations.append(
                SgaDampPerturbation(
                    systematic_gene_name=row["Query Systematic Name"],
                    perturbed_gene_name=row["Query allele name"],
                    strain_id=row["Query Strain ID"],
                )
            )
        elif "KanMX_deletion" in row["query_perturbation_type"]:
            perturbations.append(
                SgaKanMxDeletionPerturbation(
                    systematic_gene_name=row["Query Systematic Name"],
                    perturbed_gene_name=row["Query allele name"],
                    strain_id=row["Query Strain ID"],
                )
            )
        elif "NatMX_deletion" in row["query_perturbation_type"]:
            perturbations.append(
                SgaNatMxDeletionPerturbation(
                    systematic_gene_name=row["Query Systematic Name"],
                    perturbed_gene_name=row["Query allele name"],
                    strain_id=row["Query Strain ID"],
                )
            )
        elif "suppression_allele" in row["query_perturbation_type"]:
            perturbations.append(
                SgaSuppressorAllelePerturbation(
                    systematic_gene_name=row["Query Systematic Name"],
                    perturbed_gene_name=row["Query allele name"],
                    strain_id=row["Query Strain ID"],
                )
            )

        # Array
        if "temperature_sensitive" in row["array_perturbation_type"]:
            perturbations.append(
                SgaTsAllelePerturbation(
                    systematic_gene_name=row["Array Systematic Name"],
                    perturbed_gene_name=row["Array allele name"],
                    strain_id=row["Array Strain ID"],
                )
            )
        elif "damp" in row["array_perturbation_type"]:
            perturbations.append(
                SgaDampPerturbation(
                    systematic_gene_name=row["Array Systematic Name"],
                    perturbed_gene_name=row["Array allele name"],
                    strain_id=row["Array Strain ID"],
                )
            )
        elif "KanMX_deletion" in row["array_perturbation_type"]:
            perturbations.append(
                SgaKanMxDeletionPerturbation(
                    systematic_gene_name=row["Array Systematic Name"],
                    perturbed_gene_name=row["Array allele name"],
                    strain_id=row["Array Strain ID"],
                )
            )
        elif "NatMX_deletion" in row["array_perturbation_type"]:
            perturbations.append(
                SgaNatMxDeletionPerturbation(
                    systematic_gene_name=row["Array Systematic Name"],
                    perturbed_gene_name=row["Array allele name"],
                    strain_id=row["Array Strain ID"],
                )
            )
        elif "suppression_allele" in row["array_perturbation_type"]:
            perturbations.append(
                SgaSuppressorAllelePerturbation(
                    systematic_gene_name=row["Array Systematic Name"],
                    perturbed_gene_name=row["Array allele name"],
                    strain_id=row["Array Strain ID"],
                )
            )
        genotype = Genotype(perturbations=perturbations)
        assert len(genotype) == 2, "Genotype must have 2 perturbations."

        environment = Environment(
            media=Media(name="YEPD", state="solid"),
            temperature=Temperature(value=row["Temperature"]),
        )
        environment_reference = environment.model_copy()

        phenotype = GeneInteractionPhenotype(
            gene_interaction=row["Genetic interaction score (ε)"], p_value=row["P-value"]
        )

        # By definition, the reference interaction would be 0.
        phenotype_reference = GeneInteractionPhenotype(gene_interaction=0.0, p_value=None)

        reference = GeneInteractionExperimentReference(
            dataset_name=dataset_name,
            genome_reference=genome_reference,
            environment_reference=environment_reference,
            phenotype_reference=phenotype_reference,
        )

        experiment = GeneInteractionExperiment(
            dataset_name=dataset_name,
            genotype=genotype,
            environment=environment,
            phenotype=phenotype,
        )

        publication = Publication(
            pubmed_id="27708008",
            pubmed_url="https://pubmed.ncbi.nlm.nih.gov/27708008/",
            doi="10.1126/science.aaf1420",
            doi_url="https://www.science.org/doi/10.1126/science.aaf1420",
        )

        return experiment, reference, publication


def main():
    from dotenv import load_dotenv

    load_dotenv()
    DATA_ROOT = os.getenv("DATA_ROOT")

    # Single mutant fitness
    dataset = SmfCostanzo2016Dataset(
        root=osp.join(DATA_ROOT, "data/torchcell/smf_costanzo2016"), io_workers=10
    )
    print(len(dataset))
    print(dataset[100])

    # Double mutant fitness
    dataset = DmfCostanzo2016Dataset(
        root=osp.join(DATA_ROOT, "data/torchcell/dmf_costanzo2016_1e5"),
        io_workers=10,
        batch_size=int(1e4),
        subset_n=int(1e5),
    )
    print(len(dataset))
    print(dataset[0])

    dataset = DmfCostanzo2016Dataset(
        root=osp.join(DATA_ROOT, "data/torchcell/dmf_costanzo2016_5e5"),
        io_workers=10,
        batch_size=int(1e4),
        subset_n=int(5e5),
    )
    print(len(dataset))
    print(dataset[0])

    dataset = DmfCostanzo2016Dataset(
        root=osp.join(DATA_ROOT, "data/torchcell/dmf_costanzo2016"),
        io_workers=10,
        batch_size=int(1e4),
    )
    print(len(dataset))
    print(dataset[0])

    # Interactions
    dataset = DmiCostanzo2016Dataset(
        root=osp.join(DATA_ROOT, "data/torchcell/dmi_costanzo2016_1e5"),
        io_workers=10,
        subset_n=int(1e5),
    )
    print(len(dataset))
    print(dataset[0])

    dataset = DmiCostanzo2016Dataset(
        root=osp.join(DATA_ROOT, "data/torchcell/dmi_costanzo2016_5e5"),
        io_workers=10,
        subset_n=int(5e5),
    )
    print(len(dataset))
    print(dataset[0])

    dataset = DmiCostanzo2016Dataset(
        root=osp.join(DATA_ROOT, "data/torchcell/dmi_costanzo2016"), io_workers=10
    )
    print(len(dataset))
    print(dataset[0])


if __name__ == "__main__":
    main()
