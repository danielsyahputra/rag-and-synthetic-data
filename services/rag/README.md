# RAG Local

A local document question-answering application built with Streamlit that allows users to upload PDF documents and get answers to their questions using RAG (Retrieval-Augmented Generation) technology.

## Features

- PDF document upload and processing
- Interactive chat interface
- Document source reference for answers
- Quantum-themed loading messages
- Conversation history tracking
- Configurable conversation message limits
- Custom avatars for user and assistant

## Prerequisites

- Python 3.8+
- Required Python packages (install via `pip install -r requirements.txt`):
  - streamlit
  - python-dotenv
  - asyncio
  - (other dependencies based on src/ modules)

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── src/
│   ├── chain.py       # Question-answering chain implementation
│   ├── config.py      # Application configuration
│   ├── ingestor.py    # Document ingestion logic
│   ├── model.py       # LLM model creation
│   ├── retriever.py   # Document retrieval implementation
│   └── uploader.py    # File upload handling
├── images/
│   ├── assistant-avatar.png
│   └── user-avatar.png
└── .env               # Environment variables
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd rag-local
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your configuration:
```env
# Add your environment variables here
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Launch the application using `streamlit run app.py`
2. Upload one or more PDF documents using the file uploader
3. Wait for the documents to be processed
4. Start asking questions about your documents in the chat interface
5. View source references by expanding the "Source #X" sections below each answer

## Configuration

The application can be configured through the `Config` class in `src/config.py`:

- `CONVERSATION_MESSAGES_LIMIT`: Maximum number of messages in a conversation (set to 0 for unlimited)
- Custom paths for images and other resources
- Other configuration options as defined in the config module

## Language

The application interface is in Indonesian language. Key translations:

- "Unggah file PDF" - Upload PDF file
- "Ajukan pertanyaan Anda di sini" - Ask your question here
- "Silakan unggah dokumen PDF untuk melanjutkan!" - Please upload PDF documents to continue!
- "Menganalisis dokumen Anda..." - Analyzing your documents...