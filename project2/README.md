# Project 2: LLM Personal Knowledge Base
## Topic: AI-Powered Social Platform for Shared Human Experiences

INDENG 231 — Data Modeling

---

## What This Is

A Karpathy-style personal knowledge base built with Claude. Raw source documents on the topic of AI-powered peer support platforms are compiled by an LLM into structured, interlinked wiki articles. A Q&A interface answers questions by retrieving relevant wiki articles and generating cited answers using the Claude API.

---

## Setup

```bash
pip install anthropic
```

Create a `.env` file with your Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-...
```

---

## Usage

### List compiled wiki articles
```bash
python qa.py --list
```

### Ask a question (single-shot)
```bash
python qa.py --question "How does the platform detect when a user is in crisis?"
python qa.py --question "What is the latency budget for voice interaction?"
python qa.py --question "How are mentor-mentee matches explained to users?"
```

### Interactive Q&A mode
```bash
python qa.py
```
Type questions and press Enter. Type `list` to see articles, `quit` to exit.

### Recompile the wiki (requires API key)
```bash
python compile_wiki.py           # skip existing articles
python compile_wiki.py --force   # recompile everything
python compile_wiki.py --topic AffectiveComputing  # recompile one article
```

---

## Project Structure

```
project2/
├── raw/                          # 10 source documents (the "personal notes")
│   ├── 01_shared_experience_platforms.md
│   ├── 02_mentor_mentee_matching.md
│   ├── 03_affective_computing.md
│   ├── 04_speech_to_text_pipelines.md
│   ├── 05_text_to_speech_synthesis.md
│   ├── 06_dialogue_systems.md
│   ├── 07_empathetic_ai_design.md
│   ├── 08_experience_storage_retrieval.md
│   ├── 09_platform_integration_architecture.md
│   └── 10_llm_knowledge_base_design.md
│
├── wiki/                         # Compiled wiki articles (LLM output)
│   ├── ExperienceMatching.md
│   ├── AffectiveComputing.md
│   ├── VoiceInterface.md
│   ├── DialogueSystem.md
│   ├── EmpathyDesign.md
│   ├── MentorMenteeSystem.md
│   ├── ExperienceStorageRetrieval.md
│   ├── PlatformArchitecture.md
│   ├── SafetyAndEscalation.md
│   ├── KnowledgeBaseDesign.md
│   └── _index.json               # Link graph and metadata
│
├── compile_wiki.py               # LLM-powered wiki compiler
├── qa.py                         # Q&A interface
├── build_index.py                # Rebuild _index.json (no API needed)
└── README.md
```

---

## Design

**Compilation** (`compile_wiki.py`): uses Claude Opus 4.7 with adaptive thinking to synthesize wiki articles from all raw sources. Each article uses `[[WikiLink]]` format to reference related topics, creating a navigable knowledge graph.

**Q&A** (`qa.py`): uses Claude Haiku 4.5 (fast, cost-effective) with keyword-based retrieval. Retrieves the top-4 most relevant wiki articles and injects them as context for answer generation.

**Pre-compilation**: the `wiki/` directory is pre-compiled and committed. Users can run Q&A without an API key unavailability interrupting the demo — only live Q&A requires the key.
