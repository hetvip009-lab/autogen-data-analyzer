from google import genai
from dotenv import load_dotenv
import os
import streamlit as st
from core.data_loader import load_csv, get_data_info, clean_data
from agents.planner_agent import get_planner_prompt
from agents.coder_agent import get_coder_prompt
from agents.executor_agent import save_and_run_code
from agents.analyst_agent import get_analyst_prompt
from utils.logger import get_logger

# Load API key
load_dotenv()

logger = get_logger("app")

def get_api_key():
    """Get API key from Streamlit secrets or environment"""
    try:
        # First try Streamlit secrets (for deployed app)
        return st.secrets["GEMINI_API_KEY"]
    except:
        try:
            # Then try environment variable (for local)
            return os.getenv("GEMINI_API_KEY")
        except:
            return None

def ask_gemini(prompt, api_key):
    """Send prompt to Gemini and get response"""
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise Exception(f"Gemini API error: {str(e)}")

def run_pipeline(csv_path, user_query, api_key=None, status_callback=None):
    """Run the complete agent pipeline"""

    # Get API key automatically if not provided
    if api_key is None:
        api_key = get_api_key()

    if api_key is None:
        raise Exception("No API key found!")

    def update_status(message):
        if status_callback:
            status_callback(message)
        print(message)

    update_status("Step 1 of 7: Loading CSV file...")
    df = load_csv(csv_path)
    if df is None:
        raise Exception("Error loading CSV file!")

    update_status("Step 2 of 7: Cleaning data...")
    df = clean_data(df)
    df.to_csv("uploaded_file.csv", index=False)

    update_status("Step 3 of 7: Analyzing data structure...")
    data_info = get_data_info(df)

    update_status("Step 4 of 7: Planner Agent creating analysis plan...")
    planner_prompt = get_planner_prompt(user_query, data_info)
    plan = ask_gemini(planner_prompt, api_key)
    if plan is None:
        raise Exception("Planner Agent failed!")

    update_status("Step 5 of 7: Coder Agent writing Python code...")
    coder_prompt = get_coder_prompt(user_query, data_info, plan)
    code = ask_gemini(coder_prompt, api_key)
    if code is None:
        raise Exception("Coder Agent failed!")

    # Clean code
    code = code.replace("```python", "").replace("```", "").strip()

    update_status("Step 6 of 7: Executor Agent running the code...")
    result = save_and_run_code(code)
    if not result["success"]:
        raise Exception(f"Code execution failed: {result['error']}")

    update_status("Step 7 of 7: Analyst Agent preparing insights...")
    analyst_prompt = get_analyst_prompt(user_query, result["output"], data_info)
    analysis = ask_gemini(analyst_prompt, api_key)
    if analysis is None:
        raise Exception("Analyst Agent failed!")

    logger.info("Pipeline completed successfully!")
    return analysis, data_info

# Test run
if __name__ == "__main__":
    csv_path = "titanic.csv"
    user_query = "Show me the survival rate by gender"
    run_pipeline(csv_path, user_query)