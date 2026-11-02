# Agentic AI System

An agentic, multimodal question-answering system built around the IFC annual report. This project extends the earlier IFC RAG chatbot by adding a planner-driven agent, more retrieval modes, and a richer data-processing pipeline for text, tables, and images.

## What this project does

The system ingests the IFC Annual Report 2024 PDF, extracts text/tables/images, chunks the content, embeds it with a local sentence-transformer model, stores it in a FAISS vector index, and answers user questions through retrieval-augmented generation (RAG).

In addition to the base chatbot flow, the repo includes:

- an agent router that chooses between RAG, web news, financial data, and a report-generation flow
- a Streamlit-based chatbot UI
- multimodal chunk preparation for text, tables, and image captions
- evaluation questions and simple benchmarking scripts

This is effectively an evolution of the earlier IFC RAG chatbot, expanded into an agentic AI workflow for broader corporate-document Q&A.

## Why it exists

The repo is designed for answering questions about IFC documents and related business context using evidence from the annual report instead of relying only on general-purpose model knowledge. It is useful for:

- interactive document Q&A
- report-based research and fact checking
- retrieval from financial documents and tables
- testing how well an AI system answers structured questions from a PDF corpus

## Tech stack

- Python
- Streamlit
- FAISS
- SentenceTransformers
- Google Gemini
- PyMuPDF / pypdf
- NumPy
- BeautifulSoup
- yfinance (used in the agent finance tool)

## Repository structure

```text
.
├── .streamlit/
│   └── config.toml              # Streamlit server config
├── data/
│   ├── images/                  # extracted PDF images
│   ├── processed/               # processed JSON chunk data
│   ├── tables/                  # extracted table outputs
│   └── ifc-annual-report-2024-financials.pdf
├── src/
│   ├── agent_system.py          # main agent planner + tools
│   ├── app.py                  # simple RAG chatbot interface
│   ├── app_agent.py            # agentic Streamlit chat interface
│   ├── preprocess.py           # chunking logic
│   ├── extract_text.py         # PDF text extraction
│   ├── extract_tables.py       # table extraction
│   ├── extract_images.py       # image extraction
│   ├── combine_multimodal.py   # merge text/table/image chunks
│   ├── search.py               # BM25 + FAISS search demo
│   ├── search_multimodal.py    # multimodal retrieval demo
│   ├── evaluate.py             # evaluation flow
│   ├── add_metadata.py        # metadata utility
│   ├── answer.py              # response helper
│   ├── filter_search.py       # search filtering
│   ├── rerank_search.py       # reranking utility
│   ├── image_captions.py      # image captioning helpers
│   ├── table_chunks.py        # table chunk processing
│   ├── multihop_demo.py       # multi-hop example
│   ├── news_agent.py          # news integration example
│   ├── cache_demo.py          # cache example
│   ├── colpali_demo.py        # ColPali-related demo
│   ├── save_demo_embedding.py # embedding demo utility
│   └── ...
├── vectorstores/
│   ├── faiss_index.index       # text vector index
│   └── multimodal.index        # multimodal vector index
├── .gitignore
├── evaluation_questions.txt    # sample evaluation prompts
├── requirements.txt            # Python dependencies
├── runtime.txt                 # runtime version target
├── tables_output.txt           # generated table export
├── Agentic AI Systemdemopdf.pdf # report/demo PDF
└── README.md                   # project documentation
```

## How the system works

1. PDF data is loaded from the IFC annual report.
2. Text, tables, and images are extracted into the `data/` folder.
3. Content is chunked and normalized.
4. Chunks are embedded using `SentenceTransformer("all-MiniLM-L6-v2")`.
5. Embeddings are stored in a FAISS index.
6. User queries are encoded and matched against the vector store.
7. Retrieved chunks are passed to Gemini for grounded answer generation.
8. The agent layer can route to specialized tools for:
   - RAG answers from the annual report
   - live news retrieval
   - financial data lookups
   - report generation

## Main entry points

### Streamlit app

```bash
streamlit run src/app.py
```

This opens the standard RAG-style chatbot interface for the IFC report.

### Agentic app

```bash
streamlit run src/app_agent.py
```

This is the agent-driven version, where the app picks a tool based on the prompt and displays the selected tool in the chat.

### Direct Python agent flow

```bash
python src/agent_system.py
```

This runs the interactive agent console and asks for a query in the terminal.

## Environment variables

The project expects a Gemini API key:

```bash
export GEMINI_API_KEY="your_key_here"
```

The code also assumes the `data/processed` and `vectorstores` folders are present and populated before executing the retrieval logic.

## Dependencies

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Relationship to IFC RAG chatbot

This repository is a direct extension of the earlier IFC RAG chatbot concept:

- the original version focused on standard report Q&A using a PDF and vector search
- this repository adds agent orchestration, tool-based routing, multimodal knowledge processing, and a more complete research workflow

In other words, the project keeps the core IFC-document RAG idea, but generalizes it into a more agentic, modular system.

## Typical use cases

- "What is IFC's mission?"
- "What were IFC's key financial results in FY24?"
- "Which sectors does IFC support?"
- "Summarize the report's strategic priorities."
- "Find information around IFC investments and growth areas."

## Notes

- Some scripts are pipeline utilities and are not intended to be launched directly as the main app.
- The system depends on local embedding models and vector indexes already created in the repo.
- For best results, keep the original PDF and processed data available in the expected folder structure.

## License

No explicit license file is included in this repository, so licensing should be checked before redistribution or public deployment.

## Future improvements

Potential next steps include:

- cleaner packaging and CLI entry points
- persistent config for model and index paths
- database-backed conversation history
- stronger multimodal retrieval and citation grounding
- deployment via Docker or a hosted web app

---

This README was created to explain the repository structure, how the system works, and how it extends the original IFC RAG chatbot into an agentic AI workflow.
