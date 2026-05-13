# ExperienceStorageRetrieval

## Overview

ExperienceStorageRetrieval is the data layer that stores, indexes, and retrieves user experience narratives. It combines a relational database (PostgreSQL) for structured queries with a vector database extension (pgvector) for semantic similarity search, enabling the [[ExperienceMatching]] engine to find relevant experience matches at scale.

## Key Concepts

- **Dual representation**: every experience is stored as both a structured record (for filtering) and an embedding vector (for semantic search). These are complementary: the structured record handles hard constraints (category, availability); the embedding handles semantic nuance.
- **pgvector**: a PostgreSQL extension that stores and queries dense vector embeddings using HNSW (Hierarchical Navigable Small World) index — sub-millisecond approximate nearest-neighbor search at millions of records.
- **LLM-based extraction**: Claude converts free-text narratives into structured JSON records. This is the primary technique for populating the structured schema from unstructured input.
- **Versioned records**: each experience update creates a new record version. Historical versions are retained for trend analysis and trajectory modeling (see [[AffectiveComputing]]).
- **Right-to-deletion**: experience records and their embeddings are purged within 24 hours on user request, in compliance with GDPR/CCPA.

## Experience Schema

**Structured record** (filterable fields):
```json
{
  "experience_id": "exp_7291",
  "user_id": "u_4812",
  "category": "health",
  "subcategory": "cancer",
  "specificity": "breast cancer, stage 2",
  "time_since_onset_months": 30,
  "duration_months": 8,
  "current_status": "in_remission",
  "emotional_texture": ["fear", "isolation", "relief"],
  "outcome": "positive",
  "open_to_mentoring": true,
  "version": 3,
  "created_at": "2024-09-15"
}
```

**Embedding vector**: 1536-dimensional dense vector (OpenAI text-embedding-3-large) representing the full narrative text. Stored in a pgvector column alongside the structured record.

## LLM Extraction Pipeline

Turning a voice or text narrative into a structured record:
```
User narrative (cleaned transcript from [[VoiceInterface]])
  → LLM extraction prompt: "Extract the following fields as JSON: category, subcategory..."
  → Structured record (JSON)
  → Embedding computation on full narrative
  → Insert into PostgreSQL + pgvector
```

Edge cases handled:
- **Ambiguous timelines** ("a few years ago") → store as null, flag for follow-up question
- **Multiple experiences** (cancer + job loss) → create multi-experience record with primary/secondary tagging
- **Ongoing experiences** → outcome = "ongoing"; time_since_onset counts from start; re-extraction on each session

## Retrieval Pipeline

```
New user query (embedding)
  → pgvector HNSW index: ANN search → top-100 candidates
  → SQL filter: category match, open_to_mentoring=true, capacity available
  → LLM re-ranking: score top-20 on semantic fit
  → Return top-5 with generated explanations
```

The HNSW index is rebuilt nightly to incorporate new embeddings. At 100K users with 3 experiences each, a single pgvector table with HNSW handles ~1000 QPS with < 5ms P99 latency.

## Privacy-Preserving Design

- Raw narrative text is never returned to other users; only LLM-generated summaries are shared (with user consent)
- Candidate lists use anonymized user IDs until mutual match acceptance
- Selective matchability: users can mark individual experiences as "not matchable" — stored for trajectory analysis but excluded from retrieval
- Audit log: every retrieval query is logged with timestamp, querying user, and top-5 candidates returned

## Incremental Updates

When a user updates their experience narrative:
1. New embedding is computed on the updated narrative
2. New structured record version is created
3. Old version is marked historical (retained for trajectory analysis)
4. HNSW index is updated incrementally (pgvector supports online insertions)

## Design Implications

- **Embedding drift**: if the embedding model is updated (e.g., switching from ada-002 to text-embedding-3-large), all existing embeddings must be recomputed. Plan for this migration in the data schema.
- **Schema evolution**: the structured record schema will grow as new experience categories are added. Use a JSONB column for extensibility rather than rigid column-per-field.
- **Feedback-driven quality**: every accepted/rejected match generates a signal. Use this to fine-tune the re-ranking model (see [[ExperienceMatching]]).

## See Also

- [[ExperienceMatching]]
- [[PlatformArchitecture]]
- [[MentorMenteeSystem]]
- [[SafetyAndEscalation]]
- [[KnowledgeBaseDesign]]
