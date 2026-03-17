import pandas as pd
import os
from utils.logger import get_logger

logger = get_logger("data_loader")

def load_csv(file_path):
    """Load CSV file and return dataframe"""
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        
        df = pd.read_csv(file_path)
        logger.info(f"CSV loaded successfully! Shape: {df.shape}")
        return df

    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
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
        # Remove duplicate rows
        df = df.drop_duplicates()
        
        # Fill missing values
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