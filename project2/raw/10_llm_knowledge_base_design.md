# LLM-Powered Personal Knowledge Base: Design and Implementation

## The Karpathy Knowledge Base Paradigm

Andrej Karpathy's personal knowledge base concept treats an LLM not as a Q&A oracle but as a curator and connector — the system reads raw sources, synthesizes them into structured wiki articles, creates links between related concepts, and then answers questions by reasoning over the compiled wiki rather than the raw sources.

This produces a knowledge base that is:
- **Coherent**: a single synthesizing voice across heterogeneous sources
- **Interlinked**: concepts reference each other in a navigable graph
- **Queryable**: a Q&A interface reasons over the compiled wiki with citations
- **Evolvable**: new raw sources can be added and incrementally compiled

## Architecture

```
raw/         ← Raw source documents (markdown, text, notes)
    ↓
compile_wiki.py ← LLM reads all raw sources, synthesizes wiki articles
    ↓
wiki/        ← Compiled, interlinked markdown articles
    ↓
qa.py        ← Q&A interface: retrieves relevant wiki sections, answers questions
```

## The Compilation Step

The compiler performs three subtasks:
1. **Concept extraction**: identify key concepts, topics, and entities across all raw sources
2. **Article synthesis**: for each identified concept, write a coherent wiki article synthesizing all relevant raw content
3. **Link injection**: add `[[WikiLinks]]` between related concepts, creating a knowledge graph

The LLM receives the full set of raw documents in context and generates wiki articles one at a time. With Claude's 1M token context window, all raw sources can fit in a single compilation pass.

**Prompt pattern for synthesis**:
```
You are a wiki author synthesizing a personal knowledge base on AI-powered social platforms.
You have read the following raw source documents: [list of filenames]

Write a comprehensive wiki article on the topic: "{topic}"
- Use clear headers (##, ###)
- Reference related concepts using [[WikiLink]] format for interlinking
- Synthesize across sources — don't just copy; add structure and connections
- Include a "## See Also" section listing 3-5 related wiki articles
- Keep the article self-contained: a reader unfamiliar with other articles should understand this one
```

## The Q&A Step

The Q&A interface:
1. Accepts a natural language question from the user
2. Identifies which wiki articles are most relevant (via keyword search or embedding similarity)
3. Injects the relevant article text into the LLM context
4. Generates an answer that cites specific wiki articles

**Prompt pattern for Q&A**:
```
You are answering questions using the following wiki knowledge base articles:
[injected wiki content]

Answer the following question concisely and accurately, citing the wiki articles you draw from:
Question: "{question}"
```

## Wiki Link Graph

The `[[WikiLink]]` format creates a navigable knowledge graph:
- Links are parsed and rendered as clickable references in the Q&A interface
- The link graph reveals conceptual proximity: topics that link to each other often are closely related
- Orphan detection: articles with no incoming links may indicate isolated topics that need connecting

## Incremental Compilation

When new raw sources are added:
1. Identify which existing wiki articles are affected (LLM-assisted topic classification)
2. Re-compile only those articles (not the full wiki)
3. Update the link graph
4. Re-index for Q&A retrieval

This avoids the cost of recompiling the entire wiki for each new source.

## Implementation Details for This Project

**Raw sources**: 10 markdown documents covering shared experience platforms, mentor-mentee matching, affective computing, STT, TTS, dialogue systems, empathetic AI design, experience storage, platform architecture, and this document.

**Wiki articles generated**: one per major concept identified by the LLM across all raw sources. Expected articles include: ExperienceMatching, AffectiveComputing, VoiceInterface, DialogueSystem, EmpathyDesign, MentorCapacityManagement, PrivacyArchitecture, SafetyEscalation, EmbeddingPipeline, MatchQualityMetrics.

**Q&A interface**: command-line; accepts any question; returns answer with cited wiki articles.

**LLM**: Claude Opus 4.7 with adaptive thinking for compilation (complex synthesis); Claude Haiku 4.5 for Q&A (faster, cheaper for retrieval-augmented Q&A).

## What This Demonstrates

The knowledge base shows that:
1. LLMs can synthesize heterogeneous raw documents into coherent, interlinked knowledge
2. The compiled wiki is more useful than the raw sources for Q&A — it adds structure that the raw sources lack
3. Retrieval-augmented Q&A over the wiki is accurate and citation-grounded
4. The pipeline is modular: swap the topic area, regenerate the wiki, and the Q&A interface works identically

This pattern generalizes to any domain where a practitioner has a body of notes, papers, and articles they want to make queryable.
