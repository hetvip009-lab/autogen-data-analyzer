from utils.logger import get_logger

logger = get_logger("planner_agent")

def get_planner_prompt(user_query, data_info):
    """Create a plan based on user query and data info"""
    
    prompt = f"""
    You are a Data Analysis Planner Agent.
    
    The user has uploaded a CSV file with the following information:
    - Rows: {data_info['rows']}
    - Columns: {data_info['columns']}
    - Column Names: {data_info['column_names']}
    - Data Types: {data_info['data_types']}
    
    User Query: {user_query}
    
    Your job is to:
    1. Understand the user query
    2. Create a clear step by step plan to answer it
    3. Specify which columns to use
    4. Specify what type of chart to use (bar/pie/line)
    
    Give a clear and simple plan in points.
    """
    
    logger.info(f"Planner prompt created for query: {user_query}")
    return prompt