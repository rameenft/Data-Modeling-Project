# Experience Storage and Retrieval: Making Lived History Searchable

## The Core Data Problem

The platform's central innovation is matching people by lived experience. This requires a data architecture that can:
1. Capture richly structured experience narratives from heterogeneous voice and text input
2. Store them in a form that supports fast semantic similarity search
3. Retrieve relevant experiences when a new user needs a match
4. Update experience records as situations evolve

## Experience Schema Design

A raw experience narrative ("I was diagnosed with stage 2 breast cancer at age 34, went through chemo for 8 months, and am now 2 years in remission") must be structured for matching. Two complementary representations are maintained:

**Structured record** (for filtering):
```json
{
  "experience_id": "exp_7291",
  "user_id": "u_4812",
  "category": "health",
  "subcategory": "cancer",
  "specificity": "breast cancer, stage 2",
  "time_since_onset_months": 30,
  "duration_months": 8,
  "current_status": "in remission",
  "emotional_texture": ["fear", "isolation", "relief"],
  "outcome": "positive",
  "open_to_mentoring": true,
  "created_at": "2024-09-15"
}
```

**Embedding vector** (for semantic search):
- The full narrative text is embedded using a sentence transformer or LLM embedding API
- Stored in a vector database (pgvector, Pinecone, Weaviate, or FAISS)
- Dimension: 1536 (OpenAI ada-002) or 3072 (text-embedding-3-large)

## LLM-Based Experience Extraction

Turning a voice narrative into a structured record requires extraction:

```
System prompt: Extract the following fields from this experience narrative.
Return JSON only.
Fields: category, subcategory, specificity, approximate_time_since_onset,
        duration, current_status, emotional_texture (list of emotions),
        outcome (positive/negative/ongoing/mixed).

Narrative: "I was diagnosed with stage 2 breast cancer at age 34..."
```

Claude can perform this extraction with high accuracy for most experience types. Edge cases:
- Ambiguous timelines: "a few years ago" → requires follow-up question
- Multiple simultaneous experiences: cancer + job loss → multi-experience record
- Experiences still in progress: outcome = "ongoing"

## Vector Database Architecture

```
Experience Narrative (text)
    → Embedding model → 1536-dim vector
    → Stored in pgvector table alongside structured fields

New User Query (text)
    → Embedding model → 1536-dim query vector
    → Approximate nearest neighbor search (HNSW index)
    → Top-100 candidate matches
    → Post-filter: category match, availability, capacity
    → Re-rank: LLM scores top-20 on match quality
    → Return top-5 with explanations
```

**HNSW (Hierarchical Navigable Small World)** index provides sub-millisecond approximate nearest neighbor search at millions of records. pgvector supports HNSW natively from PostgreSQL 16.

## Handling Experience Evolution

Experiences change. A person 3 months into unemployment is different from the same person 18 months later. The platform handles evolution through:

**Versioned records**: each update creates a new record version. The embedding is recomputed on the updated narrative. Historical versions are retained for trend analysis.

**Temporal weighting in matching**: more recent experience updates receive higher weight in similarity scores.

**Status transitions**: "active" (currently experiencing) vs. "graduated" (resolved) vs. "mentor-ready" (ready to support others). The platform makes these transitions explicit.

## Privacy-Preserving Retrieval

Experience data is sensitive. The retrieval architecture must:
- Never return raw narrative text to other users — only structured summaries
- Anonymize user IDs in candidate lists until mutual match acceptance
- Allow users to mark specific experiences as "not matchable" (stored but excluded from retrieval)
- Support right-to-deletion: experience records and their embeddings purged within 24 hours on request

## Feedback Loop for Retrieval Quality

Every completed mentor-mentee match generates a feedback signal:
- Both parties rate the relevance of the match (1-5)
- These ratings are used to fine-tune the re-ranking model
- Poor matches feed back into experience extraction quality review (was the narrative misclassified?)

Over time, the retrieval system improves through accumulated match feedback.

## Connection to This Project

The platform stores experience narratives in a PostgreSQL database with pgvector extension. LLM-based extraction populates structured fields; embedding-based indexing enables semantic search. The Q&A interface in the knowledge base queries this architecture to demonstrate how a new user's question ("I'm looking for someone who went through divorce after 20 years of marriage") triggers a retrieval, re-ranking, and explanation pipeline.
