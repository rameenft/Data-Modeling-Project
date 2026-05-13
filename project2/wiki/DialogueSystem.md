# DialogueSystem

## Overview

The DialogueSystem is the conversational backbone of the platform, managing multi-turn interactions between users and the AI mediator. It tracks conversation state, enforces supportive conversation policies, and integrates retrieval from the experience corpus to ground responses in real mentor profiles and platform knowledge.

## Key Concepts

- **End-to-end neural dialogue**: a single LLM (Claude Opus 4.7) processes the full conversation history and generates the next response. No explicit state machine — context is managed via structured system prompt injection.
- **Conversation state tracking**: explicit state (current goal, emotional state, outstanding questions, session metadata) is maintained in Redis and injected as structured context at each turn.
- **Retrieval-augmented generation (RAG)**: relevant mentor profiles and wiki articles are retrieved and injected into the LLM context, preventing hallucination and grounding recommendations in real data.
- **Dialogue policy**: conversation behavior rules (validation-first, one-question-at-a-time, advice only when requested) are enforced through system prompt instructions rather than a hardcoded state machine.
- **Graceful uncertainty**: the system explicitly signals when it lacks information rather than confabulating.

## Conversation State Object

```json
{
  "user_id": "u_4812",
  "conversation_goal": "mentor_search",
  "turn_count": 6,
  "affect_history": [
    {"turn": 1, "emotion": "anxious", "intensity": 0.8},
    {"turn": 6, "emotion": "hopeful", "intensity": 0.4}
  ],
  "extracted_experience": { "category": "health", "subcategory": "cancer" },
  "retrieved_candidates": ["u_291", "u_445"],
  "crisis_flag": false
}
```

This state is injected into the system prompt at every turn, giving the LLM coherent context without relying solely on conversation history.

## Conversation Policies

The [[EmpathyDesign]] principles are enforced through system prompt rules:

1. **Validation-first**: acknowledge the user's emotional experience before any information-giving. Never lead with resources or advice.
2. **One question per turn**: avoid overwhelming users. Ask one open-ended question at a time.
3. **Reflect before advise**: summarize what you've heard before offering perspective.
4. **No clinical advice**: never advise on medication, treatment plans, or legal matters. Redirect to professionals explicitly.
5. **AI identity transparency**: never claim to be human. Identify as AI when asked.

## Multi-Turn Context Management

With Claude's 1M token context window, the full conversation history usually fits in context without truncation. For very long sessions (> 2 hours of conversation):
- Older turns are compressed into a rolling summary
- Key facts (user's name, primary experience, outstanding topics) are extracted and maintained as structured memory in the system prompt

## Retrieval Integration

Before generating each response, the DialogueSystem queries the [[ExperienceStorageRetrieval]] layer:
- If `conversation_goal = mentor_search`: retrieve top candidate profiles
- If `conversation_goal = resource_seeking`: retrieve relevant platform articles
- Retrieved content is injected into context with a "Retrieved context:" prefix to prevent the LLM from treating it as part of the conversation

## Evaluation

| Metric | Target |
|--------|--------|
| Task completion rate | > 70% |
| Dialogue coherence (human judges) | > 4.0 / 5.0 |
| Empathy score (classifier) | > 0.75 |
| Turns to mentor match | < 10 |
| User satisfaction (post-session) | > 4.0 / 5.0 |

Note: automated metrics like BLEU/ROUGE are explicitly not used — they measure n-gram overlap, not empathy or task success.

## Design Implications

- **State persistence across disconnects**: the Redis state must survive brief connection drops (common in mobile use). TTL should be at least 2 hours.
- **Conversation goal detection**: the system must classify whether the user is venting (needs validation), seeking a mentor (needs matching), or in crisis (needs escalation) — and transition gracefully between goals.
- **Pacing control**: the system introduces deliberate pauses (via TTS `<break>` tags, see [[VoiceInterface]]) to allow emotional processing.

## See Also

- [[EmpathyDesign]]
- [[AffectiveComputing]]
- [[VoiceInterface]]
- [[ExperienceMatching]]
- [[SafetyAndEscalation]]
