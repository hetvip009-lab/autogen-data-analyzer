from utils.logger import get_logger

logger = get_logger("coder_agent")

def get_coder_prompt(user_query, data_info, plan):
    """Create Python code based on the plan"""
    
    prompt = f"""
    You are a Python Data Analysis Coder Agent.
    
    The user has uploaded a CSV file with the following information:
    - Rows: {data_info['rows']}
    - Columns: {data_info['columns']}
    - Column Names: {data_info['column_names']}
    - Data Types: {data_info['data_types']}
    - Sample Data: {data_info['sample_data']}
    
    User Query: {user_query}
    
    Analysis Plan: {plan}
    
    Your job is to write clean Python code that:
    1. Loads the CSV file: df = pd.read_csv('uploaded_file.csv')
    2. Analyzes the data based on the plan
    3. Creates a comprehensive dashboard with multiple charts
    4. Saves the final chart as 'charts/result.png'
    5. Prints a clear summary of results
    
    IMPORTANT - Always create a multi-chart dashboard like this:
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import numpy as np
    import os
    
    os.makedirs('charts', exist_ok=True)
    df = pd.read_csv('uploaded_file.csv')
    
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Data Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # Add these chart types based on the query:
    # - Bar chart for comparisons
    # - Pie chart for distributions
    # - Donut chart for proportions
    # - Line chart for trends
    # - Histogram for distributions
    # - KPI metrics boxes
    # - Summary statistics
    
    plt.tight_layout()
    plt.savefig('charts/result.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    Rules:
    - Always create minimum 4 charts in one dashboard
    - Always include KPI metrics boxes
    - Always include a summary statistics box
    - Always save to 'charts/result.png'
    - Always print key findings
    - Handle errors with try/except
    - Write simple and clean code
    
    Return ONLY the Python code, nothing else.
    """
    
    logger.info(f"Coder prompt created for query: {user_query}")
    return prompt