#!/bin/bash

# Start the FastAPI backend on port 8000
uvicorn agentic_api.main:app --host 0.0.0.0 --port 8000 &

# Start the Streamlit frontend on port 8501
streamlit run frontend/app.py --server.port 8501 --server.enableCORS false
