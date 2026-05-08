import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class FeatureSelector:
    """
    Classe para realizar a seleção de atributos.
    """

    def __init__(self, dataset: pd.DataFrame | None):
        self.dataset = dataset

    def analyze_correlation(self, threshold: float = 0.8) -> list[tuple[str, str, float]]:
        """
        Analisa a correlação entre os atributos e retorna pares de atributos com alta correlação.
        """
        if self.dataset is None:
            print("Nenhum dataset fornecido para análise de correlação.")
            return []

        numeric_df = self.dataset.select_dtypes(include=["number"])
        if numeric_df.shape[1] < 2:
            print(
                "Menos de duas colunas numéricas: não é possível calcular correlações entre atributos."
            )
            return []

        correlation_matrix = numeric_df.corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(
            correlation_matrix,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            linewidths=0.5,
        )
        plt.title("Matriz de Correlação", fontsize=16)
        plt.show()

        high_correlation_pairs: list[tuple[str, str, float]] = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                if abs(correlation_matrix.iloc[i, j]) > threshold:
                    col1 = correlation_matrix.columns[i]
                    col2 = correlation_matrix.columns[j]
                    correlation_value = float(correlation_matrix.iloc[i, j])
                    high_correlation_pairs.append((col1, col2, correlation_value))

        if high_correlation_pairs:
            print(f"Atributos com alta correlação (acima de {threshold}):")
            for col1, col2, corr in high_correlation_pairs:
                print(f"{col1} e {col2} - Correlação: {corr:.2f}")
        else:
            print("Nenhum par de atributos com correlação alta encontrado.")

        return high_correlation_pairs

    def drop_columns(self, columns_to_drop: list[str]) -> pd.DataFrame | None:
        """
        Remove as colunas especificadas do dataset original.
        """
        if self.dataset is None:
            print("Nenhum dataset fornecido; nada a remover.")
            return None

        print(f"Removendo as colunas: {columns_to_drop}")
        self.dataset = self.dataset.drop(labels=columns_to_drop, axis=1)
        return self.dataset
