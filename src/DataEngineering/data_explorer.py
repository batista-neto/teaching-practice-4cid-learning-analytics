from IPython.display import display
import pandas as pd


class DataExplorer:
    """
    Classe para realizar uma análise inicial de um dataset.
    """

    def analyze(self, dataset: pd.DataFrame | None) -> None:
        if dataset is None:
            print("Nenhum dataset fornecido para análise.")
            return

        print("Primeiras linhas do dataset:")
        display(dataset.head())

        print("\nResumo estatístico do dataset:")
        display(dataset.describe())

        print("\nInformações sobre os tipos de dados:")
        dataset.info()
