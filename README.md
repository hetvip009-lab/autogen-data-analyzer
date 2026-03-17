# AutoGen Data Analyzer GPT

An AI-powered automated data analysis system built using Microsoft's AutoGen framework and Google Gemini API.

## Project Overview

AutoGen Data Analyzer GPT allows users to upload any CSV file and ask questions about their data in plain English — without writing any code. The system uses a team of specialized AI agents that work together to understand the query, generate Python code, execute it safely, and return visual charts and written insights automatically.

## Features

- Upload any CSV file for analysis
- Ask questions in plain English
- Automatic Python code generation
- Safe code execution
- Auto-generated charts and visualizations
- Download analysis reports
- Query history tracking
- User-friendly web interface

## Project Structure
```
autogen-data-analyzer/
│
├── agents/
│   ├── planner_agent.py     — Understands user query and creates plan
│   ├── coder_agent.py       — Generates Python code automatically
│   ├── executor_agent.py    — Runs code safely
│   └── analyst_agent.py     — Explains results in plain English
│
├── core/
│   ├── data_loader.py       — CSV loading and cleaning
│   └── visualizer.py        — Chart generation
│
├── frontend/
│   └── ui.py                — Streamlit web interface
│
├── utils/
│   └── logger.py            — Logging utility
│
├── app.py                   — Main pipeline
├── .env                     — API keys
├── requirements.txt         — Dependencies
└── README.md                — Project documentation
```

## Technologies Used

- Python 3.13
- Microsoft AutoGen Framework
- Google Gemini API
- Streamlit
- Pandas
- Matplotlib
- Docker
- Git/GitHub

## How to Run

1. Clone the repository
```
git clone https://github.com/hetvip009-lab/autogen-data-analyzer.git
```

2. Create virtual environment
```
python -m venv myenv
source myenv/Scripts/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Run the application
```
streamlit run frontend/ui.py
```

5. Open browser at http://localhost:8501

## How to Use

1. Enter your Gemini API key in the sidebar
2. Upload any CSV file
3. Type your question about the data
4. Click Analyze button
5. View results and charts

## Agent Architecture

| Agent | Role |
|---|---|
| Planner Agent | Understands user query and creates analysis plan |
| Coder Agent | Generates Python code based on the plan |
| Executor Agent | Runs the generated code safely |
| Analyst Agent | Explains results in simple language |

## Developer

- Name: Patel Hetvi Prafulbhai
- Enrollment: 25MSC04005
- University: GSFC University
- Department: Data Science