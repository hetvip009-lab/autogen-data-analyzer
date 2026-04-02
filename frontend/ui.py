import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import run_pipeline, get_api_key

st.set_page_config(
    page_title="AutoGen Data Analyzer GPT",
    layout="wide"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = []

st.title("AutoGen Data Analyzer GPT")
st.markdown("An AI-powered data analysis system using multi-agent architecture")
st.markdown("---")

with st.sidebar:
    st.header("Configuration")

    # Check if API key exists in secrets
    api_key = get_api_key()

    if api_key:
        st.success("API Key configured!")
        st.info("Ready to analyze your data!")
    else:
        st.warning("No API key found!")
        manual_key = st.text_input(
            "Enter Gemini API Key manually",
            type="password",
            placeholder="Paste your API key here"
        )
        if manual_key:
            api_key = manual_key
            st.success("API Key entered!")

    st.markdown("---")

    st.header("Query History")
    if len(st.session_state.chat_history) == 0:
        st.info("No queries yet!")
    else:
        for i, chat in enumerate(st.session_state.chat_history):
            st.markdown(f"**{i+1}.** {chat['query']}")
            st.markdown(f"*{chat['time']}*")
            st.markdown("---")

    if st.button("Clear History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.analysis_results = []
        st.rerun()

    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("1. Upload a CSV file")
    st.markdown("2. Type your question")
    st.markdown("3. Click Analyze button")
    st.markdown("4. View results and charts")

tab1, tab2, tab3 = st.tabs(["Analysis", "Data Explorer", "About"])

with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Upload Data")

        uploaded_file = st.file_uploader(
            "Upload CSV File",
            type=["csv"]
        )

        if uploaded_file is not None:
            with open("uploaded_file.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File uploaded: {uploaded_file.name}")

            df = pd.read_csv("uploaded_file.csv")
            st.markdown("### Data Preview")
            st.dataframe(df.head(5))
            st.markdown(
                f"Total rows: **{df.shape[0]}** | "
                f"Total columns: **{df.shape[1]}**"
            )

            st.download_button(
                label="Download CSV",
                data=df.to_csv(index=False),
                file_name="uploaded_data.csv",
                mime="text/csv"
            )

    with col2:
        st.subheader("Ask a Question")

        user_query = st.text_area(
            "Type your question about the data",
            placeholder="Example: Show me the survival rate by gender",
            height=100
        )

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

        analyze_btn = st.button(
            "Analyze",
            type="primary",
            use_container_width=True
        )

        if analyze_btn:
            if not api_key:
                st.error("No API key available!")
            elif uploaded_file is None:
                st.error("Please upload a CSV file first!")
            elif not user_query:
                st.error("Please type a question!")
            else:
                with st.spinner("Analyzing your data. Please wait..."):
                    try:
                        analysis, data_info = run_pipeline(
                            "uploaded_file.csv",
                            user_query,
                            api_key
                        )

                        if analysis:
                            st.session_state.chat_history.append({
                                "query": user_query,
                                "time": datetime.now().strftime("%H:%M:%S"),
                                "analysis": analysis
                            })
                            st.session_state.analysis_results.append({
                                "query": user_query,
                                "analysis": analysis
                            })
                            st.success("Analysis completed!")

                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    if len(st.session_state.analysis_results) > 0:
        st.markdown("---")
        st.subheader("Analysis Results")

        latest = st.session_state.analysis_results[-1]
        st.markdown(f"**Query:** {latest['query']}")
        st.markdown(latest['analysis'])

        if os.path.exists("charts/result.png"):
            st.markdown("### Generated Chart")
            st.image("charts/result.png", width=700)

            with open("charts/result.png", "rb") as f:
                st.download_button(
                    label="Download Chart",
                    data=f,
                    file_name="analysis_chart.png",
                    mime="image/png"
                )

        st.download_button(
            label="Download Analysis Report",
            data=latest['analysis'],
            file_name="analysis_report.txt",
            mime="text/plain"
        )

with tab2:
    st.subheader("Data Explorer")

    if os.path.exists("uploaded_file.csv"):
        df = pd.read_csv("uploaded_file.csv")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", df.shape[0])
        with col2:
            st.metric("Total Columns", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())
        with col4:
            st.metric("Duplicate Rows", df.duplicated().sum())

        st.markdown("---")
        st.markdown("### Full Dataset")
        st.dataframe(df)

        st.markdown("### Column Information")
        col_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.values,
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })
        st.dataframe(col_info)

        st.markdown("### Basic Statistics")
        st.dataframe(df.describe())

    else:
        st.info("Please upload a CSV file in the Analysis tab first!")

with tab3:
    st.subheader("About This Project")
    st.markdown("""
    ### AutoGen Data Analyzer GPT

    AutoGen Data Analyzer GPT is an AI-powered data analysis system
    built using Microsoft's AutoGen framework and Google Gemini API.

    ### How It Works

    The system uses a team of 4 specialized AI agents:

    | Agent | Role |
    |---|---|
    | Planner Agent | Understands query and creates analysis plan |
    | Coder Agent | Generates Python code automatically |
    | Executor Agent | Runs the code safely |
    | Analyst Agent | Explains results in simple language |

    ### Technologies Used

    - Python 3.13
    - Microsoft AutoGen Framework
    - Google Gemini API
    - Streamlit
    - Pandas
    - Matplotlib
    - Docker
    - Git/GitHub
    """)

st.markdown("---")
st.markdown("AutoGen Data Analyzer GPT | Built with Streamlit and Google Gemini")