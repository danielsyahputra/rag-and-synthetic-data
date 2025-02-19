# AI Services Collection

Collection of AI-powered tools and services for content generation and data analysis.

## Services

### AI Book Generator
Generate complete eBooks with AI including titles, content, and cover designs.

```bash
pip install python-docx docx2pdf python-docxtpl openai

python generator.py \
    --topic "your-topic" \
    --target-audience "target" \
    --num-chapters 6 \
    --output-docx "output.docx" \
    --output-pdf "output.pdf"
```

### Synthetic Data Generator
Generate synthetic e-commerce data for testing and development.

```bash
pip install pandas faker

python generate_data.py --num-rows 1000 --output dataset.csv --seed 42
```

### RAG Local
Question-answering system for PDF documents using RAG technology.

```bash
pip install -r requirements.txt

streamlit run app.py
```

## Project Structure
```
.
├── services/
│   ├── augmentoolkit/     # AI Book Generator
│   ├── rag/               # RAG Local System
│   ├── synthetic_csv/     # Data Generator
│   └── synthetic_pdf/     # PDF Generator
└── tmp/                   # Temporary files
```