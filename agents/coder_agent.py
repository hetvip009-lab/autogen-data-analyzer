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
    
    Your job is to:
    1. Write clean Python code using Pandas and Matplotlib
    2. Load the CSV file using: df = pd.read_csv('uploaded_file.csv')
    3. Analyze the data based on the plan
    4. Generate a chart and save it as 'charts/result.png'
    5. Print a clear summary of the results
    
    Rules:
    - Use only Pandas and Matplotlib
    - Always save chart to 'charts/result.png'
    - Always print results clearly
    - Handle errors with try/except
    - Write simple and clean code
    
    Return ONLY the Python code, nothing else.
    """
    
    logger.info(f"Coder prompt created for query: {user_query}")
    return prompt