from google import genai
from dotenv import load_dotenv
import os
from core.data_loader import load_csv, get_data_info, clean_data
from agents.planner_agent import get_planner_prompt
from agents.coder_agent import get_coder_prompt
from agents.executor_agent import save_and_run_code
from agents.analyst_agent import get_analyst_prompt
from utils.logger import get_logger

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
client = genai.Client(api_key=api_key)

logger = get_logger("app")

def ask_gemini(prompt):
    """Send prompt to Gemini and get response"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return None

def run_pipeline(csv_path, user_query):
    """Run the complete agent pipeline"""
    
    print("\n" + "="*50)
    print("AutoGen Data Analyzer GPT")
    print("="*50)
    
    # Step 1 - Load CSV
    print("\nStep 1: Loading CSV file...")
    df = load_csv(csv_path)
    if df is None:
        print("Error loading CSV file!")
        return
    
    # Step 2 - Clean Data
    print("Step 2: Cleaning data...")
    df = clean_data(df)
    df.to_csv("uploaded_file.csv", index=False)
    
    # Step 3 - Get Data Info
    print("Step 3: Analyzing data structure...")
    data_info = get_data_info(df)
    print(f"Data loaded: {data_info['rows']} rows, {data_info['columns']} columns")
    print(f"Columns: {data_info['column_names']}")
    
    # Step 4 - Planner Agent
    print("\nStep 4: Planner Agent creating analysis plan...")
    planner_prompt = get_planner_prompt(user_query, data_info)
    plan = ask_gemini(planner_prompt)
    if plan is None:
        print("Planner Agent failed!")
        return
    print(f"Plan created!\n{plan}")
    
    # Step 5 - Coder Agent
    print("\nStep 5: Coder Agent writing Python code...")
    coder_prompt = get_coder_prompt(user_query, data_info, plan)
    code = ask_gemini(coder_prompt)
    if code is None:
        print("Coder Agent failed!")
        return
    
    # Clean code (remove markdown if any)
    code = code.replace("```python", "").replace("```", "").strip()
    print("Code generated successfully!")
    
    # Step 6 - Executor Agent
    print("\nStep 6: Executor Agent running the code...")
    result = save_and_run_code(code)
    if not result["success"]:
        print(f"Execution failed: {result['error']}")
        return
    print("Code executed successfully!")
    print(f"Output:\n{result['output']}")
    
    # Step 7 - Analyst Agent
    print("\nStep 7: Analyst Agent preparing insights...")
    analyst_prompt = get_analyst_prompt(user_query, result["output"], data_info)
    analysis = ask_gemini(analyst_prompt)
    if analysis is None:
        print("Analyst Agent failed!")
        return
    
    print("\n" + "="*50)
    print("FINAL ANALYSIS")
    print("="*50)
    print(analysis)
    
    # Check if chart was generated
    if os.path.exists("charts/result.png"):
        print("\nChart saved to: charts/result.png")
    
    print("\nPipeline completed successfully!")
    return analysis

# Test run
if __name__ == "__main__":
    csv_path = "titanic.csv"
    user_query = "Show me the survival rate by gender"
    run_pipeline(csv_path, user_query)