# PlatformArchitecture

## Overview

PlatformArchitecture describes the end-to-end system design: microservices, data flow, latency budget, state management, scaling strategy, and the continuous improvement feedback loop. The architecture integrates six subsystems — voice, AI mediator, experience storage, matching, affective computing, and safety — into a cohesive user experience.

## Key Concepts

- **Microservices**: each major subsystem is an independently deployable service. This enables targeted scaling (e.g., scale voice-service for audio processing without scaling the matching engine).
- **WebSocket for audio**: persistent bidirectional connection between client and voice-service. Required for streaming STT and low-latency TTS delivery (see [[VoiceInterface]]).
- **Redis for session state**: in-memory store for fast read/write of conversation state (current goal, affect history, retrieved candidates). 2-hour TTL per session.
- **Streaming LLM pipeline**: LLM response generation, TTS synthesis, and audio delivery all overlap in time. First audio chunk reaches the user before the LLM has finished generating the full response.
- **Feedback loop**: every user interaction (match acceptance, conversation rating, session completion) feeds a nightly improvement pipeline that updates matching models, affect classifiers, and response policies.

## Service Architecture

```
Client (mobile/web)
  ↕ WebSocket (audio stream)
  ↕ REST API (text, match requests, profiles)

API Gateway
  → Auth (JWT validation)
  → Rate limiting
  → Request routing

Core Services:
  voice-service      → STT (Whisper/Deepgram) + TTS (OpenAI TTS)
  dialogue-service   → LLM conversation (Claude Opus 4.7)
  affect-service     → Emotion classification, distress detection
  experience-service → Narrative extraction, embedding, pgvector queries
  match-service      → Candidate retrieval, re-ranking, explanation generation
  safety-service     → Crisis detection, escalation routing, audit logging

Data Layer:
  PostgreSQL + pgvector  → User profiles, experience records, embeddings
  Redis                  → Session state, real-time affect scores
  S3                     → Encrypted transcript archives (30-day retention)
```

## Request Flow: Voice Conversation Turn

1. User speaks → WebSocket audio stream to voice-service
2. VAD detects end-of-utterance → STT produces transcript
3. Parallel: affect-service classifies audio features + text sentiment
4. dialogue-service retrieves session state from Redis
5. If `conversation_goal = mentor_search`: match-service retrieves candidates from pgvector
6. dialogue-service calls Claude API with full context (state + retrieved context + conversation history)
7. LLM response streams → TTS synthesis begins on first chunk
8. Audio streams back to client → user hears response
9. Session state updated in Redis; affect score appended to trajectory

## Latency Budget

| Stage | Target |
|-------|--------|
| VAD end-of-speech | 200ms |
| STT transcription | 300ms |
| LLM first token | 500ms |
| TTS first audio chunk | 300ms |
| Audio delivery | 100ms |
| **Total** | **~1.4 seconds** |

## Scaling Considerations

- **LLM calls are the bottleneck**: use Claude Haiku for [[AffectiveComputing]] classification (cheap, fast) and Claude Opus 4.7 for dialogue generation (quality).
- **Vector search is read-heavy**: pgvector with HNSW handles ~1000 QPS on modest hardware at 300K experience records.
- **Audio is bandwidth-intensive**: 10K concurrent WebSocket connections require careful connection pooling and horizontal scaling of voice-service.
- **Stateless services**: all services are stateless (state in Redis/PostgreSQL). Horizontal scaling is straightforward.

## Continuous Improvement Loop

```
User interactions
  → match ratings + conversation ratings + session completions
  → Nightly pipeline:
      - Poor matches → experience extraction quality review
      - Good matches → positive training examples for re-ranker
      - Affect trajectory analysis → update response policies
      - Crisis escalations → threshold calibration review
  → Updated models deployed weekly
```

## Ethical Review Integration

- **Quarterly matching audit**: external review for demographic bias in match assignments
- **Monthly affect accuracy audit**: human review of 200 sampled affect classifications
- **Daily safety log review**: automated + weekly human review of crisis escalations
- **Annual third-party security audit**: penetration testing, data handling review

## Design Implications

- **Privacy-first data flows**: raw audio never persists beyond transcription; experience narratives flow only to explicitly matched users (post-acceptance, as summaries only).
- **Graceful degradation**: if affect-service is down, dialogue-service continues with neutral affect assumption. If match-service is slow, cached candidates from the previous turn are used.
- **Multi-region deployment**: for a globally distributed user base, voice-service and dialogue-service should be deployed in the user's nearest region for latency.

## See Also

- [[VoiceInterface]]
- [[DialogueSystem]]
- [[ExperienceStorageRetrieval]]
- [[ExperienceMatching]]
- [[SafetyAndEscalation]]
