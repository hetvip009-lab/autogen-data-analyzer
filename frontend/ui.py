import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import run_pipeline, run_image_pipeline, get_api_key

st.set_page_config(
    page_title="AutoGen Data Analyzer GPT",
    layout="wide"
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = []
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

st.title("AutoGen Data Analyzer GPT")
st.markdown("An AI-powered data analysis system using multi-agent architecture")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Configuration")

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

    # Query History
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
        st.session_state.user_query = ""
        st.rerun()

    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("1. Upload a data file or image")
    st.markdown("2. Click example query or type your own")
    st.markdown("3. Click Analyze button")
    st.markdown("4. View results and charts")
    st.markdown("5. Download chart or report")

    st.markdown("---")
    st.markdown("### Supported Files")
    st.markdown("**Data Files:**")
    st.markdown("CSV, Excel, JSON, TSV, TXT, PDF")
    st.markdown("**Image Files:**")
    st.markdown("PNG, JPG, JPEG")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Analysis", "Image Analysis", "Data Explorer", "About"
])

# Tab 1 - Data Analysis
with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Upload Data File")

        uploaded_file = st.file_uploader(
            "Upload CSV, Excel, JSON, TSV, TXT or PDF",
            type=["csv", "xlsx", "xls", "json",
                  "tsv", "txt", "pdf"]
        )

        if uploaded_file is not None:
            try:
                # Save file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Load based on file type
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(temp_path)
                elif uploaded_file.name.endswith(
                        (".xlsx", ".xls")):
                    df = pd.read_excel(temp_path)
                elif uploaded_file.name.endswith(".json"):
                    df = pd.read_json(temp_path)
                elif uploaded_file.name.endswith(".tsv"):
                    df = pd.read_csv(temp_path, sep="\t")
                elif uploaded_file.name.endswith(".txt"):
                    try:
                        df = pd.read_csv(temp_path, sep="\t")
                    except:
                        df = pd.read_csv(temp_path)
                elif uploaded_file.name.endswith(".pdf"):
                    from core.data_loader import load_csv
                    df = load_csv(temp_path)

                if df is not None:
                    df.to_csv("uploaded_file.csv", index=False)
                    st.success(
                        f"File uploaded: {uploaded_file.name}")

                    st.markdown("### Data Preview")
                    st.dataframe(df.head(5))
                    st.markdown(
                        f"Total rows: **{df.shape[0]}** | "
                        f"Total columns: **{df.shape[1]}**"
                    )

                    st.download_button(
                        label="Download as CSV",
                        data=df.to_csv(index=False),
                        file_name="uploaded_data.csv",
                        mime="text/csv"
                    )

                # Clean temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

    with col2:
        st.subheader("Ask a Question")

        st.markdown("### Example Queries")
        st.markdown("Click any button to fill the question box:")

        example_queries = [
            "Show me the survival rate by gender",
            "What is the average age of passengers?",
            "Show me the distribution of passenger classes",
            "Which age group had the highest survival rate?",
            "Show me missing values in the dataset",
            "Give me complete statistical summary"
        ]

        for i, query in enumerate(example_queries):
            if st.button(
                    query, use_container_width=True,
                    key=f"q{i}"):
                st.session_state.user_query = query

        user_query = st.text_area(
            "Type your question about the data",
            value=st.session_state.get("user_query", ""),
            placeholder="Example: Show me the survival rate by gender",
            height=100
        )

        if user_query:
            st.session_state.user_query = user_query

        analyze_btn = st.button(
            "Analyze",
            type="primary",
            use_container_width=True
        )

        if analyze_btn:
            if not api_key:
                st.error("No API key available!")
            elif not os.path.exists("uploaded_file.csv"):
                st.error("Please upload a file first!")
            elif not user_query:
                st.error("Please type a question!")
            else:
                with st.spinner(
                        "Analyzing your data. Please wait..."):
                    try:
                        analysis, data_info = run_pipeline(
                            "uploaded_file.csv",
                            user_query,
                            api_key
                        )

                        if analysis:
                            st.session_state.chat_history.append({
                                "query": user_query,
                                "time": datetime.now().strftime(
                                    "%H:%M:%S"),
                                "analysis": analysis
                            })
                            st.session_state.analysis_results.append({
                                "query": user_query,
                                "analysis": analysis
                            })
                            st.session_state.user_query = ""
                            st.success("Analysis completed!")

                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    # Results section
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

# Tab 2 - Image Analysis
with tab2:
    st.subheader("Image Analysis")
    st.markdown(
        "Upload a screenshot of data, chart or table "
        "and ask questions about it!"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Upload Image")
        uploaded_image = st.file_uploader(
            "Upload PNG, JPG or JPEG",
            type=["png", "jpg", "jpeg"],
            key="image_uploader"
        )

        if uploaded_image is not None:
            st.image(uploaded_image,
                     caption="Uploaded Image",
                     use_column_width=True)

            # Save image
            img_path = f"uploaded_image.{uploaded_image.name.split('.')[-1]}"
            with open(img_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            st.success("Image uploaded successfully!")

    with col2:
        st.markdown("### Ask About the Image")

        image_query = st.text_area(
            "Type your question about the image",
            placeholder="Example: What does this chart show? "
                        "What are the key insights?",
            height=150,
            key="image_query"
        )

        st.markdown("### Example Image Queries")
        image_example_queries = [
            "What data is shown in this image?",
            "What are the key insights from this chart?",
            "Extract all data from this table",
            "What trends can you see in this graph?"
        ]

        for i, query in enumerate(image_example_queries):
            if st.button(
                    query, use_container_width=True,
                    key=f"iq{i}"):
                image_query = query

        analyze_image_btn = st.button(
            "Analyze Image",
            type="primary",
            use_container_width=True,
            key="analyze_image"
        )

        if analyze_image_btn:
            if not api_key:
                st.error("No API key available!")
            elif uploaded_image is None:
                st.error("Please upload an image first!")
            elif not image_query:
                st.error("Please type a question!")
            else:
                with st.spinner(
                        "Analyzing image. Please wait..."):
                    try:
                        analysis = run_image_pipeline(
                            img_path,
                            image_query,
                            api_key
                        )

                        st.markdown("---")
                        st.subheader("Image Analysis Results")
                        st.markdown(analysis)

                        st.download_button(
                            label="Download Image Analysis",
                            data=analysis,
                            file_name="image_analysis.txt",
                            mime="text/plain"
                        )

                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# Tab 3 - Data Explorer
with tab3:
    st.subheader("Data Explorer")

    if os.path.exists("uploaded_file.csv"):
        df = pd.read_csv("uploaded_file.csv")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", df.shape[0])
        with col2:
            st.metric("Total Columns", df.shape[1])
        with col3:
            st.metric("Missing Values",
                      df.isnull().sum().sum())
        with col4:
            st.metric("Duplicate Rows",
                      df.duplicated().sum())

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
        st.info(
            "Please upload a file in the Analysis tab first!")

# Tab 4 - About
with tab4:
    st.subheader("About This Project")
    st.markdown("""
    ### AutoGen Data Analyzer GPT

    AutoGen Data Analyzer GPT is an AI-powered automated data
    analysis system that allows users to upload any data file
    or image and ask questions in plain English — without
    writing a single line of code.

    ### Supported File Types

    **Data Files:**
    - CSV files (.csv)
    - Excel files (.xlsx, .xls)
    - JSON files (.json)
    - TSV files (.tsv)
    - Text files (.txt)
    - PDF files (.pdf)

    **Image Files:**
    - PNG images (.png)
    - JPG/JPEG images (.jpg, .jpeg)

    ### How It Works

    The system uses a team of 4 specialized AI agents:

    | Agent | Role |
    |---|---|
    | Planner Agent | Understands query and creates plan |
    | Coder Agent | Generates Python code automatically |
    | Executor Agent | Runs the code safely |
    | Analyst Agent | Explains results in simple language |

    ### Technologies Used
    - Python 3.13
    - Microsoft AutoGen Framework
    - Google Gemini AI (Vision + Text)
    - Streamlit
    - Pandas
    - Matplotlib
    - Docker
    - Git/GitHub

    ### Key Features
    - Upload CSV, Excel, JSON, TSV, TXT, PDF files
    - Upload images and screenshots for analysis
    - Ask questions in plain English
    - Automatic code generation
    - Auto generated charts and dashboards
    - Download analysis reports
    - Query history tracking
    """)

# Footer
st.markdown("---")
st.markdown(
    "AutoGen Data Analyzer GPT | "
    "Powered by Google Gemini AI and Microsoft AutoGen | "
    "Built with Streamlit"
)