import pandas as pd
import os
import json
from utils.logger import get_logger

logger = get_logger("data_loader")

def load_csv(file_path):
    """Load any supported file and return dataframe"""
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        elif ext == ".json":
            df = pd.read_json(file_path)
        elif ext == ".tsv":
            df = pd.read_csv(file_path, sep="\t")
        elif ext == ".txt":
            # Try tab separated first then comma
            try:
                df = pd.read_csv(file_path, sep="\t")
            except:
                df = pd.read_csv(file_path, sep=",")
        elif ext == ".pdf":
            df = read_pdf(file_path)
        else:
            df = pd.read_csv(file_path)

        logger.info(f"File loaded successfully! Shape: {df.shape}")
        return df

    except Exception as e:
        logger.error(f"Error loading file: {e}")
        return None

def read_pdf(file_path):
    """Extract tables from PDF file"""
    try:
        import pdfplumber
        tables = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    df_page = pd.DataFrame(
                        table[1:],
                        columns=table[0]
                    )
                    tables.append(df_page)
        if tables:
            return pd.concat(tables, ignore_index=True)
        else:
            # If no tables found extract text
            text_data = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_data.append({"text": text})
            return pd.DataFrame(text_data)
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
        return None

def get_data_info(df):
    """Get basic info about the dataframe"""
    try:
        info = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": list(df.columns),
            "data_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "sample_data": df.head(3).to_string()
        }
        logger.info("Data info extracted successfully!")
        return info
    except Exception as e:
        logger.error(f"Error getting data info: {e}")
        return None

def clean_data(df):
    """Basic data cleaning"""
    try:
        df = df.drop_duplicates()
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("Unknown")
            else:
                df[col] = df[col].fillna(df[col].mean())
        logger.info("Data cleaned successfully!")
        return df
    except Exception as e:
        logger.error(f"Error cleaning data: {e}")
        return None