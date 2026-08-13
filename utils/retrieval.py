"""
RAG Retrieval Utilities
------------------------
This module implements a simple, local RAG (Retrieval-Augmented Generation)
pipeline over our Markdown knowledge base.

Pipeline:
  Markdown files  -->  DocumentLoader  -->  TextSplitter (chunks)
                    -->  Embeddings (vectors)  -->  FAISS vector store
                    -->  similarity_search (retriever)  -->  top-k chunks

Why FAISS (local vector store) instead of a hosted vector DB (Pinecone, etc)?
- The knowledge base is small (6 files) and fully local — no need for a
  managed cloud database.
- FAISS runs entirely on this machine, in-memory, with zero external
  dependencies or network calls, which keeps the project simple and free
  to run for a beginner project / take-home challenge.
- FAISS is fast enough for small-to-medium document sets like this one.

Why embeddings + similarity search instead of keyword search?
- Users phrase IT issues in many different ways ("VPN broke after password
  change" vs "can't connect to network after resetting login"). Embeddings
  capture MEANING, not just exact words, so semantically similar questions
  still retrieve the right document even without matching keywords exactly.
"""

import os
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Path to the knowledge_base folder (relative to project root, not this file)
KB_PATH = Path(__file__).resolve().parent.parent / "knowledge_base"
INDEX_PATH = Path(__file__).resolve().parent.parent / "faiss_index"

# Module-level cache so we don't rebuild the vector store on every call
_vectorstore = None


def _build_vectorstore():
    """
    Loads all markdown files, splits them into chunks, embeds them,
    and builds a FAISS vector store from scratch.
    """
    loader = DirectoryLoader(
        str(KB_PATH),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    if not documents:
        raise FileNotFoundError(
            f"No markdown files found in {KB_PATH}. "
            "Make sure the knowledge_base folder contains .md files."
        )

    # Split each document into smaller overlapping chunks.
    # chunk_size=800 keeps chunks focused on one sub-topic (e.g. just the
    # "Troubleshooting Steps" section) rather than mixing unrelated sections.
    # chunk_overlap=100 avoids losing context at chunk boundaries.
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


def get_vectorstore():
    """
    Returns a cached FAISS vector store, building/loading it once.
    On the very first run this builds the index; on later runs it is
    reused from memory (or reloaded from disk if saved).
    """
    global _vectorstore
    if _vectorstore is None:
        if INDEX_PATH.exists():
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            _vectorstore = FAISS.load_local(
                str(INDEX_PATH),
                embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            _vectorstore = _build_vectorstore()
            _vectorstore.save_local(str(INDEX_PATH))
    return _vectorstore


def retrieve_relevant_knowledge(query: str, k: int = 3):
    """
    Runs a similarity search against the vector store and returns:
      - a list of unique source document filenames (e.g. "vpn_troubleshooting.md")
      - a list of the actual retrieved text chunks

    IMPORTANT: We only send these top-k chunks to the LLM later, never the
    entire knowledge base. This keeps the LLM's context focused and grounded.
    """
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=k)

    sources = []
    contents = []
    for doc in results:
        source_name = os.path.basename(doc.metadata.get("source", "unknown.md"))
        sources.append(source_name)
        contents.append(doc.page_content)

    # Deduplicate sources while preserving order
    unique_sources = list(dict.fromkeys(sources))
    return unique_sources, contents
