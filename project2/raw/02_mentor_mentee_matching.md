# Mentor-Mentee Matching Systems: Algorithms and Experience-Based Approaches

## The Matching Problem

Mentor-mentee matching is a form of two-sided market assignment. Unlike one-sided recommendation (suggesting products to users), both parties must find value. The classic formulation is the **stable marriage problem** (Gale-Shapley, 1962): find an assignment such that no mentor-mentee pair would both prefer to be matched with each other over their current assignment.

In practice, experience-based platforms relax the stability requirement and optimize instead for **predicted engagement** and **perceived relevance**.

## Feature Engineering for Experience Matching

A matching system must extract features from user-submitted experiences. Key feature categories:

**Temporal features**: When did the experience occur? Recency matters — a person 2 years past a divorce is more useful to someone 6 months in than someone 15 years past.

**Severity and duration**: A 3-month job loss differs from a 2-year unemployment spiral. Capturing magnitude affects matching quality.

**Outcome trajectory**: Did the mentor's situation resolve positively, negatively, or remain ongoing? Users in similar outcome trajectories often have more to offer each other.

**Emotional texture**: Was the experience primarily isolating, chaotic, grief-filled, uncertain? Matching on emotional texture surfaces empathetic resonance.

## Embedding-Based Matching

Modern systems use large language models to embed experience narratives into dense vector representations. Two users are matched when their experience embeddings have high cosine similarity in a shared semantic space.

**Pipeline**:
1. User writes/records their experience narrative
2. Speech-to-text transcription (if voice input)
3. LLM embeds the narrative: `embedding = model.embed(narrative)`
4. Nearest-neighbor search in the experience embedding space (FAISS or pgvector)
5. Candidate pool returned for further filtering

**Advantages**: captures semantic nuance beyond keyword overlap; generalizes to novel phrasings.

**Disadvantages**: embeddings are opaque — a match seems good but it's hard to explain why. Users may distrust black-box recommendations.

## Hybrid Scoring Architecture

Best-in-class systems use a two-stage approach:

**Stage 1 — Retrieval**: Fast approximate nearest-neighbor search using embeddings to retrieve top-100 candidates from a pool of thousands.

**Stage 2 — Re-ranking**: A slower but more precise scoring model considers:
- Compatibility score (embedding similarity)
- Availability signal (mentor active in past 30 days?)
- Communication style match (formal vs. casual, verbose vs. terse)
- Mentor capacity (how many mentees are they currently supporting?)

## Cold-Start Problem

New users have no experience narrative yet. Solutions:
- **Guided onboarding**: structured interview that produces a synthetic narrative
- **Collaborative filtering fallback**: match on demographic proxies until behavioral data accumulates
- **Progressive disclosure**: allow users to add experiences incrementally; improve matches over time

## Mentor Capacity and Burnout Prevention

Peer mentors are not therapists. Systems must:
- Cap mentor load (e.g., maximum 3 active mentees)
- Monitor conversation length and frequency for burnout signals
- Build in structured off-ramps ("this conversation has been going for 8 weeks — how are you both doing?")
- Offer mentor-only support channels and community spaces

## Evaluation Framework

| Metric | Definition | Target |
|--------|-----------|--------|
| Match acceptance rate | % of suggested matches both parties accept | > 60% |
| First message sent within 48h | Immediacy of connection | > 70% |
| 4-week conversation retention | Still talking after a month | > 40% |
| Mentee-reported helpfulness (1-5) | Post-conversation survey | > 4.0 |
| Mentor satisfaction score | Monthly survey | > 3.8 |

## Connection to This Project

The platform automates Stage 1 retrieval using LLM-based experience embedding and uses Claude to re-rank candidates by generating a natural-language "fit explanation" — why this mentor and mentee are a good match. This explanation is shown to both parties, increasing acceptance rates by making the match feel intentional rather than algorithmic.
