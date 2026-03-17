import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import run_pipeline
from google import genai
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="AutoGen Data Analyzer GPT",
    page_icon="",
    layout="wide"
)

# Title
st.title("AutoGen Data Analyzer GPT")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Enter Gemini API Key",
        type="password",
        placeholder="Paste your API key here"
    )
    
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("1. Enter your Gemini API key")
    st.markdown("2. Upload a CSV file")
    st.markdown("3. Type your question")
    st.markdown("4. Click Analyze button")
    st.markdown("5. View results and charts")

# Main area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Data")
    
    # CSV upload
    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )
    
    if uploaded_file is not None:
        # Save uploaded file
        with open("uploaded_file.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File uploaded: {uploaded_file.name}")
        
        # Show preview
        import pandas as pd
        df = pd.read_csv("uploaded_file.csv")
        st.markdown("### Data Preview")
        st.dataframe(df.head(5))
        st.markdown(f"Total rows: {df.shape[0]} | Total columns: {df.shape[1]}")

with col2:
    st.subheader("Ask a Question")
    
    # Query input
    user_query = st.text_area(
        "Type your question about the data",
        placeholder="Example: Show me the survival rate by gender",
        height=100
    )
    
    # Analyze button
    analyze_btn = st.button("Analyze", type="primary", use_container_width=True)
    
    if analyze_btn:
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar!")
        elif uploaded_file is None:
            st.error("Please upload a CSV file first!")
        elif not user_query:
            st.error("Please type a question!")
        else:
            # Set API key in environment
            os.environ["GEMINI_API_KEY"] = api_key
            
            with st.spinner("Analyzing your data..."):
                try:
                    analysis = run_pipeline("uploaded_file.csv", user_query)
                    
                    # Show analysis
                    st.markdown("---")
                    st.subheader("Analysis Results")
                    st.markdown(analysis)
                    
                    # Show chart if exists
                    if os.path.exists("charts/result.png"):
                        st.markdown("### Chart")
                        st.image("charts/result.png")
                        
                        # Download button for chart
                        with open("charts/result.png", "rb") as f:
                            st.download_button(
                                label="Download Chart",
                                data=f,
                                file_name="analysis_chart.png",
                                mime="image/png"
                            )
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("AutoGen Data Analyzer GPT | Built with Streamlit and Google Gemini")