"""Data import and quality checks for the new workbench."""
from pathlib import Path
import numpy as np
import pandas as pd
SUPPORTED = {".csv",".txt",".tsv",".xlsx",".xls"}
def load_table(path, **kwargs):
    """Load CSV/TSV/TXT/Excel without intentionally altering source values."""
    p=Path(path)
    if not p.exists(): raise FileNotFoundError(p)
    if p.suffix.lower() not in SUPPORTED: raise ValueError(f"Unsupported format: {p.suffix}")
    if p.suffix.lower() in {".xlsx",".xls"}: return pd.read_excel(p,**kwargs)
    sep=kwargs.pop("sep","\t" if p.suffix.lower()==".tsv" else ",")
    return pd.read_csv(p,sep=sep,**kwargs)
def quality_report(frame):
    numeric=frame.select_dtypes(include=[np.number])
    return {"rows":int(len(frame)),"columns":int(len(frame.columns)),"column_names":[str(c) for c in frame.columns],"missing_by_column":{str(k):int(v) for k,v in frame.isna().sum().items()},"duplicate_rows":int(frame.duplicated().sum()),"numeric_summary":numeric.describe().to_dict()}
