import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import run_pipeline

# Page configuration
st.set_page_config(
    page_title="AutoGen Data Analyzer GPT",
    layout="wide"
)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = []

# Title
st.title("AutoGen Data Analyzer GPT")
st.markdown("An AI-powered data analysis system using multi-agent architecture")
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
    
    if api_key:
        st.success("API Key entered!")
    
    st.markdown("---")
    
    # Chat History in sidebar
    st.header("Query History")
    if len(st.session_state.chat_history) == 0:
        st.info("No queries yet!")
    else:
        for i, chat in enumerate(st.session_state.chat_history):
            st.markdown(f"**{i+1}.** {chat['query']}")
            st.markdown(f"*{chat['time']}*")
            st.markdown("---")
    
    # Clear history button
    if st.button("Clear History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.analysis_results = []
        st.rerun()
    
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
        df = pd.read_csv("uploaded_file.csv")
        st.markdown("### Data Preview")
        st.dataframe(df.head(5))
        st.markdown(f"Total rows: **{df.shape[0]}** | Total columns: **{df.shape[1]}**")
        
        # Download uploaded CSV
        st.download_button(
            label="Download Uploaded CSV",
            data=df.to_csv(index=False),
            file_name="uploaded_data.csv",
            mime="text/csv"
        )

with col2:
    st.subheader("Ask a Question")
    
    # Query input
    user_query = st.text_area(
        "Type your question about the data",
        placeholder="Example: Show me the survival rate by gender",
        height=100
    )
    
    # Example queries
    st.markdown("### Example Queries")
    example_queries = [
        "Show me the survival rate by gender",
        "What is the average age of passengers?",
        "Show me the distribution of passenger classes",
        "Which age group had the highest survival rate?"
    ]
    
    for query in example_queries:
        if st.button(query, use_container_width=True):
            user_query = query
    
    # Analyze button
    analyze_btn = st.button(
        "Analyze",
        type="primary",
        use_container_width=True
    )
    
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
            
            with st.spinner("Analyzing your data. Please wait..."):
                try:
                    analysis = run_pipeline("uploaded_file.csv", user_query)
                    
                    if analysis:
                        # Save to chat history
                        st.session_state.chat_history.append({
                            "query": user_query,
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "analysis": analysis
                        })
                        
                        # Save analysis result
                        st.session_state.analysis_results.append({
                            "query": user_query,
                            "analysis": analysis
                        })
                        
                        st.success("Analysis completed!")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Results section
if len(st.session_state.analysis_results) > 0:
    st.markdown("---")
    st.subheader("Analysis Results")
    
    # Show latest result
    latest = st.session_state.analysis_results[-1]
    st.markdown(f"**Query:** {latest['query']}")
    st.markdown(latest['analysis'])
    
    # Show chart if exists
    if os.path.exists("charts/result.png"):
        st.markdown("### Generated Chart")
        st.image("charts/result.png", use_column_width=True)
        
        # Download chart button
        with open("charts/result.png", "rb") as f:
            st.download_button(
                label="Download Chart",
                data=f,
                file_name="analysis_chart.png",
                mime="image/png"
            )
    
    # Download analysis as text
    st.download_button(
        label="Download Analysis Report",
        data=latest['analysis'],
        file_name="analysis_report.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown("AutoGen Data Analyzer GPT | Built with Streamlit and Google Gemini")