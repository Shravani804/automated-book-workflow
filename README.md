
# Automated-Book-Workflow

The Automated Book Workflow System is an AI-powered tool designed to enhance the quality of textual content by blending automated intelligence with human insight. It begins by extracting content from a specified URL, typically from public domain sources like WikiSource. The extracted chapter is first rewritten using an advanced AI model to correct grammar, improve sentence structure, and enrich vocabulary. Next, an AI reviewer evaluates and refines the content further for clarity and flow. Finally, the system empowers the user to manually review and edit the content before finalizing it. Once completed, the final version can be downloaded or further refined through the same pipeline. This solution is ideal for writers, editors, and digital publishers who aim to efficiently polish textual material while retaining full creative control.


## Features

- URL-Based Scraping: Automatically fetches chapter content from a given online source.
- AI Writing Assistant: Rewrites content with improved grammar, vocabulary, and style.
- Reprocessing Loop: Easily re-edit or regenerate content through repeated iterations.
- Manual Editing Panel: Allows users to manually revise the AI-reviewed content for finalization.


## Installation

Clone the project

```bash
  git clone https://github.com/Shravani804/automated-book-workflow.git
```

Go to the project directory

```bash
  cd automated-book-workflow
```

Create a Virtual Environment

```bash
  python -m venv venv
```

Activate Environment

```bash
  venv\Scripts\activate
```

Install Python Dependencies
```bash
  pip install -r requirements.txt
```

Install Playwright Browsers
```bash
  playwright install
```

Set Up Environment Variables
```bash
  GEMINI_API_KEY=your_api_key_here
```


## Run Locally

Start the Backend Server (FastAPI)

```bash
  uvicorn agentic_api.main:app --reload
```
- Access the API at: http://127.0.0.1:8000
- Access API Docs at: http://127.0.0.1:8000/docs


Launch the Frontend Interface (Streamlit)

```bash
  streamlit run human_interface/editor.py
```
- Open your browser at: http://localhost:8501

