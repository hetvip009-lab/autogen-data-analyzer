from utils.logger import get_logger

logger = get_logger("analyst_agent")

def get_analyst_prompt(user_query, code_output, data_info):
    """Create a human readable analysis from code output"""
    
    prompt = f"""
    You are a Data Analysis Analyst Agent.
    
    The user asked: {user_query}
    
    The data had the following information:
    - Rows: {data_info['rows']}
    - Columns: {data_info['columns']}
    - Column Names: {data_info['column_names']}
    
    The Python code produced this output:
    {code_output}
    
    Your job is to:
    1. Read the code output carefully
    2. Write a clear and simple explanation of the results
    3. Highlight the most important findings
    4. Give 2-3 useful insights from the data
    5. Suggest 1-2 follow up questions the user can ask
    
    Rules:
    - Use simple and easy language
    - No technical jargon
    - Be specific with numbers and facts
    - Keep it short and clear
    """
    
    logger.info(f"Analyst prompt created for query: {user_query}")
    return prompt