# AI Book Generator

A Python-based tool that automatically generates eBooks using AI, complete with title generation, content creation, and cover design.

## Features

- Automatic title generation
- Chapter and section outline creation
- Content generation with references and statistics
- Cover photo generation
- Visualization generation for chapters
- PDF and DOCX output formats
- Preview mode support
- Support for both English and Indonesian content

## Requirements

```bash
pip install python-docx docx2pdf python-docxtpl openai
```

```
python generator.py \
    --topic "peran generative ai dalam industry" \
    --target-audience "c-level and manajer tingkat tinggi" \
    --num-chapters 6 \
    --num-subsections 5 \
    --output-docx "tmp/dokumen.docx" \
    --output-pdf "tmp/dokumen.pdf" \
    --cover-template "tmp/dokumen.docx"
```

```
project/
├── tmp/
│   └── temp.docx
└── wrapper.py      # openai wrapper
└── generator.py      # Main script
```
