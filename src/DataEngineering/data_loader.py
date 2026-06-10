import shutil
import tempfile
import zipfile
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
            return self._read_csv()
        if suffix in (".xlsx", ".xls"):
            if suffix == ".xlsx" and self._is_numbers_package():
                return self._load_numbers_package()
            engine = "openpyxl" if suffix == ".xlsx" else None
            kw = {**self.read_kwargs}
            if engine and "engine" not in kw:
                kw["engine"] = engine
            return pd.read_excel(
                self.filepath, sheet_name=self.sheet_name, **kw
            )
        raise ValueError(f"Formato não suportado: {suffix}")

    def _read_csv(self) -> pd.DataFrame:
        if "sep" in self.read_kwargs:
            return pd.read_csv(self.filepath, **self.read_kwargs)

        sample = self.filepath.read_text(encoding="utf-8")[:4096]
        sep = ";" if sample.count(";") > sample.count(",") else ","
        return pd.read_csv(self.filepath, sep=sep, **self.read_kwargs)

    def _is_numbers_package(self) -> bool:
        """Detecta pacote Apple Numbers salvo com extensão .xlsx."""
        try:
            with zipfile.ZipFile(self.filepath) as archive:
                return any(name.startswith("Index/") for name in archive.namelist())
        except zipfile.BadZipFile:
            return False

    def _load_numbers_package(self) -> pd.DataFrame:
        from numbers_parser import Document

        with tempfile.NamedTemporaryFile(suffix=".numbers", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            shutil.copy(self.filepath, tmp_path)
            doc = Document(tmp_path)
            sheet = doc.sheets[self.sheet_name if isinstance(self.sheet_name, int) else 0]
            table = sheet.tables[0]
            rows = [
                [table.cell(row, col).value for col in range(table.num_cols)]
                for row in range(table.num_rows)
            ]
            if not rows:
                return pd.DataFrame()
            return pd.DataFrame(rows[1:], columns=rows[0])
        finally:
            tmp_path.unlink(missing_ok=True)
