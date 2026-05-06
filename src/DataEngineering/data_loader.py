from pathlib import Path

import pandas as pd


class DataLoader:
    """
    Carrega dados tabulares a partir de CSV ou Excel.
    """

    def __init__(self, filepath: str, sheet_name: str | int = 0, **read_kwargs):
        self.filepath = Path(filepath)
        self.sheet_name = sheet_name
        self.read_kwargs = read_kwargs

    def load_data(self) -> pd.DataFrame:
        if not self.filepath.is_file():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.filepath}")

        suffix = self.filepath.suffix.lower()
        if suffix == ".csv":
            return pd.read_csv(self.filepath, **self.read_kwargs)
        if suffix in (".xlsx", ".xls"):
            engine = "openpyxl" if suffix == ".xlsx" else None
            kw = {**self.read_kwargs}
            if engine and "engine" not in kw:
                kw["engine"] = engine
            return pd.read_excel(
                self.filepath, sheet_name=self.sheet_name, **kw
            )
        raise ValueError(f"Formato não suportado: {suffix}")
