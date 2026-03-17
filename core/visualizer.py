import matplotlib.pyplot as plt
import pandas as pd
import os
from utils.logger import get_logger

logger = get_logger("visualizer")

# Create charts folder if not exists
if not os.path.exists("charts"):
    os.makedirs("charts")

def bar_chart(df, x_col, y_col, title="Bar Chart"):
    """Generate bar chart"""
    try:
        plt.figure(figsize=(10, 6))
        plt.bar(df[x_col], df[y_col], color="steelblue")
        plt.title(title)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = f"charts/bar_chart.png"
        plt.savefig(path)
        plt.close()
        logger.info("Bar chart created successfully!")
        return path
    except Exception as e:
        logger.error(f"Error creating bar chart: {e}")
        return None

def pie_chart(df, col, title="Pie Chart"):
    """Generate pie chart"""
    try:
        plt.figure(figsize=(8, 8))
        counts = df[col].value_counts()
        plt.pie(counts, labels=counts.index, autopct="%1.1f%%")
        plt.title(title)
        plt.tight_layout()
        path = f"charts/pie_chart.png"
        plt.savefig(path)
        plt.close()
        logger.info("Pie chart created successfully!")
        return path
    except Exception as e:
        logger.error(f"Error creating pie chart: {e}")
        return None

def line_chart(df, x_col, y_col, title="Line Chart"):
    """Generate line chart"""
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(df[x_col], df[y_col], marker="o", color="steelblue")
        plt.title(title)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.xticks(rotation=45)
        plt.tight_layout()
        path = f"charts/line_chart.png"
        plt.savefig(path)
        plt.close()
        logger.info("Line chart created successfully!")
        return path
    except Exception as e:
        logger.error(f"Error creating line chart: {e}")
        return None