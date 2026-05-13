# Platform Integration Architecture: Bringing It All Together

## System Overview

The shared experience platform integrates six technical subsystems into a coherent user experience:

1. **Voice interface** (STT + TTS)
2. **AI mediator** (LLM dialogue system with affective calibration)
3. **Experience storage and retrieval** (pgvector + LLM extraction)
4. **Mentor-mentee matching engine** (embedding similarity + re-ranking)
5. **Affective computing layer** (real-time emotion classification)
6. **Safety and escalation system** (crisis detection + human moderation)

## User Journey: First-Time User

```
1. User opens platform (web or mobile)
2. Voice onboarding begins:
   "Hi, I'm your guide here. Can you tell me a bit about what brought you here today?"
3. User speaks → STT transcribes → affective features extracted from audio
4. LLM extracts structured experience from narrative
5. Embedding computed → candidate mentors retrieved
6. LLM generates top-3 mentor match cards with explanations
7. User selects a match → connection request sent
8. Mutual acceptance → private conversation channel opened
9. AI mediator facilitates first conversation
10. Post-conversation: both parties rate the interaction
```

## Request Flow Architecture

```
Client (mobile/web)
    ↕ WebSocket (audio stream)
    ↕ REST API (text, match requests)
    
API Gateway
    → Auth service (JWT validation)
    → Rate limiting
    → Request routing

Core Services:
    voice-service: STT (Whisper/Deepgram) + TTS (OpenAI TTS)
    dialogue-service: LLM conversation management (Claude API)
    affect-service: emotion classifier, distress detector
    experience-service: extraction, embedding, pgvector queries
    match-service: candidate retrieval, re-ranking, explanation generation
    safety-service: crisis detection, escalation routing, audit logging

Data Layer:
    PostgreSQL + pgvector: user profiles, experience records, embeddings
    Redis: session state, real-time affect scores, conversation context
    S3: encrypted transcript archives (30-day retention, then delete)
```

## Latency Budget for Voice Interaction

End-to-end target: user stops speaking → AI response heard < 2.5 seconds

| Stage | Target Latency |
|-------|---------------|
| VAD end-of-speech detection | 200ms |
| STT transcription (streaming) | 300ms |
| Parallel affective feature extraction | 0ms (concurrent) |
| Context retrieval (Redis session) | 20ms |
| LLM response generation (streaming, first token) | 500ms |
| TTS synthesis (first audio chunk) | 300ms |
| Audio delivery to client | 100ms |
| **Total** | **~1.4 seconds** |

Streaming is essential: LLM generation and TTS synthesis overlap with audio delivery.

## State Management

Conversation state is stored in Redis (fast read/write, 2-hour TTL per session):

```json
{
  "session_id": "sess_9912",
  "user_id": "u_4812",
  "conversation_goal": "mentor_search",
  "turn_count": 6,
  "affect_history": [
    {"turn": 1, "emotion": "anxious", "intensity": 0.8},
    {"turn": 3, "emotion": "sad", "intensity": 0.6},
    {"turn": 6, "emotion": "hopeful", "intensity": 0.4}
  ],
  "extracted_experience": { ... },
  "retrieved_candidates": ["u_291", "u_445", "u_882"],
  "pending_match_request": null,
  "crisis_flag": false
}
```

The affective trajectory (stored in affect_history) is visible to the AI mediator, enabling it to note emotional shifts: "It sounds like you're feeling a bit more hopeful as we talk."

## Scaling Considerations

**LLM calls are the bottleneck**: each turn requires at least one LLM call (dialogue generation) and potentially two more (affect classification, experience re-extraction). At scale:
- Cache experience embeddings (don't recompute unless narrative changes)
- Batch affect classification across short time windows
- Use Claude Haiku for affect classification (cheap, fast), Claude Opus for dialogue generation (quality)

**Voice is bandwidth-intensive**: streaming audio requires persistent WebSocket connections. At 10K concurrent users, this requires careful connection pooling and horizontal scaling of the voice-service.

**Matching is read-heavy**: the matching engine performs pgvector queries for every new user onboarding. pgvector with HNSW index handles ~1000 QPS on modest hardware.

## Feedback and Continuous Improvement Loop

```
User experience → match rating + conversation rating
    → Stored in feedback_events table
    → Nightly pipeline:
        - Poor matches → reviewed by experience team
        - Good matches → positive examples for re-ranking fine-tuning
        - Affect trajectory analysis → update affective response policies
        - Crisis escalation review → improve detection thresholds
```

## Ethical Review Integration

The architecture includes:
- **Algorithm audit**: quarterly external review of matching system for demographic bias
- **Affect accuracy audit**: monthly human review of 200 sampled affect classifications
- **Safety log review**: daily automated + weekly human review of crisis escalations
- **Data retention compliance**: automated deletion pipelines, GDPR/CCPA controls

## Connection to This Project

The knowledge base wiki captures the architecture of each subsystem and how they integrate. The Q&A interface demonstrates the "match explanation generation" component: given a new user's experience description, it retrieves similar experiences from the wiki and generates a natural-language explanation of how the matching would work, using Claude API with retrieval augmentation.
