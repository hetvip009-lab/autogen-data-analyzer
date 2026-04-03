from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import base64
import streamlit as st
from core.data_loader import load_csv, get_data_info, clean_data
from agents.planner_agent import get_planner_prompt
from agents.coder_agent import get_coder_prompt
from agents.executor_agent import save_and_run_code
from agents.analyst_agent import get_analyst_prompt
from utils.logger import get_logger

load_dotenv()
logger = get_logger("app")

def get_api_key():
    """Get API key from Streamlit secrets or environment"""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        try:
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

def analyze_image(image_path, user_query, api_key):
    """Analyze image using Gemini Vision"""
    try:
        client = genai.Client(api_key=api_key)

        # Read image as base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        # Get file extension
        ext = os.path.splitext(image_path)[1].lower()
        if ext in [".jpg", ".jpeg"]:
            mime_type = "image/jpeg"
        elif ext == ".png":
            mime_type = "image/png"
        else:
            mime_type = "image/jpeg"

        prompt = f"""
        You are a Data Analysis Expert.
        
        Please analyze this image carefully and answer the following question:
        {user_query}
        
        If the image contains a table or data:
        1. Extract all the data you can see
        2. Analyze it based on the question
        3. Provide clear insights and findings
        4. Give specific numbers and facts
        
        If the image contains a chart or graph:
        1. Describe what the chart shows
        2. Extract key values and trends
        3. Answer the user question based on the chart
        4. Give useful insights
        
        Please provide a comprehensive and clear analysis.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=base64.b64decode(image_data),
                    mime_type=mime_type
                ),
                prompt
            ]
        )
        return response.text

    except Exception as e:
        logger.error(f"Image analysis error: {e}")
        raise Exception(f"Image analysis error: {str(e)}")

def run_pipeline(csv_path, user_query, api_key=None, status_callback=None):
    """Run the complete agent pipeline"""
    if api_key is None:
        api_key = get_api_key()
    if api_key is None:
        raise Exception("No API key found!")

    def update_status(message):
        if status_callback:
            status_callback(message)
        print(message)

    update_status("Step 1 of 7: Loading file...")
    df = load_csv(csv_path)
    if df is None:
        raise Exception("Error loading file!")

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

    code = code.replace("```python", "").replace("```", "").strip()

    update_status("Step 6 of 7: Executor Agent running the code...")
    result = save_and_run_code(code)
    if not result["success"]:
        raise Exception(f"Code execution failed: {result['error']}")

    update_status("Step 7 of 7: Analyst Agent preparing insights...")
    analyst_prompt = get_analyst_prompt(
        user_query, result["output"], data_info)
    analysis = ask_gemini(analyst_prompt, api_key)
    if analysis is None:
        raise Exception("Analyst Agent failed!")

    logger.info("Pipeline completed successfully!")
    return analysis, data_info

def run_image_pipeline(image_path, user_query, api_key=None):
    """Run image analysis pipeline"""
    if api_key is None:
        api_key = get_api_key()
    if api_key is None:
        raise Exception("No API key found!")

    analysis = analyze_image(image_path, user_query, api_key)
    return analysis

if __name__ == "__main__":
    csv_path = "titanic.csv"
    user_query = "Show me the survival rate by gender"
    run_pipeline(csv_path, user_query)