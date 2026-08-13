# Agentic AI IT Support Resolution System — Ollama Version

This is the merged version of the original **Agentic-AI-IT-support** project with the Ollama changes applied.

It keeps the original multi-stage LangGraph workflow:

```text
START
  ↓
TRIAGE
  ↓
KNOWLEDGE RETRIEVAL
  ↓
RESOLUTION
  ↓
REVIEW
  ↓
ESCALATION CHECK
  ├── no  → FINAL RESPONSE → END
  └── yes → HUMAN ESCALATION → END
```

## Main change

Paid OpenAI dependencies are removed.

- Chat model: `llama3.2:3b` via Ollama
- Embeddings: `nomic-embed-text` via Ollama
- Vector store: FAISS locally
- Orchestration: LangGraph
- App framework: Streamlit

## Project structure

```text
Agentic-AI-IT-support-Ollama-Merged/
├── agents/
│   ├── __init__.py
│   ├── triage_agent.py
│   ├── knowledge_agent.py
│   ├── resolution_agent.py
│   ├── reviewer_agent.py
│   └── escalation_agent.py
├── graph/
│   ├── __init__.py
│   ├── state.py
│   └── workflow.py
├── knowledge_base/
│   ├── vpn_troubleshooting.md
│   ├── password_reset.md
│   ├── microsoft_teams.md
│   ├── laptop_performance.md
│   ├── access_management.md
│   └── phishing_security.md
├── utils/
│   ├── __init__.py
│   ├── llm.py
│   ├── retrieval.py
│   └── logger.py
├── tests/
│   └── test_workflow.py
├── docs/
│   └── architecture.md
├── app.py
├── cli.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Run in GitHub Codespaces

### Terminal 1 — install and start Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

Keep Terminal 1 running.

### Terminal 2 — download models

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama list
```

### Create Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Optional environment file

```bash
cp .env.example .env
```

No API key is needed.

### Test Ollama chat model

```bash
python -c "from langchain_ollama import ChatOllama; print(ChatOllama(model='llama3.2:3b').invoke('Say hello in one sentence').content)"
```

### Test embeddings

```bash
python -c "from langchain_ollama import OllamaEmbeddings; e=OllamaEmbeddings(model='nomic-embed-text'); print(len(e.embed_query('VPN password issue')))"
```

### Run CLI first

```bash
python cli.py "My VPN stopped working after I changed my password."
```

### Run Streamlit

```bash
streamlit run app.py
```

Open forwarded port **8501** in Codespaces.

## If you previously used OpenAI embeddings

Delete the previous FAISS index before the first Ollama run:

```bash
rm -rf faiss_index
```

The app will rebuild it automatically using `nomic-embed-text`.
