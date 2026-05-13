# Real-Time Dialogue Systems: Architecture and Design for Social Platforms

## What Makes Dialogue Hard

A dialogue system must do more than generate good responses to isolated messages. It must:
- Maintain coherent context across many turns
- Track conversational goals and ensure they are being met
- Recover gracefully from misunderstandings
- Know when to ask clarifying questions vs. make progress
- Manage pacing — when to push forward, when to let silence breathe

In emotionally sensitive conversations, these challenges are amplified: misreading the user's intent or responding too quickly can damage trust.

## Classic Dialogue System Architectures

**Pipeline architecture**:
```
ASR → NLU → Dialogue Manager → NLG → TTS
```
- ASR: speech recognition
- NLU: intent classification + entity extraction
- DM: selects next action based on dialogue state
- NLG: generates text response
- TTS: synthesizes speech

Advantages: modular, each component can be improved independently.
Disadvantages: error propagation (ASR error → NLU error → wrong action), rigid state machine limits naturalness.

**End-to-end neural dialogue** (modern):
- Single large model processes conversation history and generates next response
- No explicit state machine — context managed implicitly in transformer attention
- Examples: ChatGPT, Claude, Gemini
- Advantages: flexible, handles novel situations gracefully
- Disadvantages: less controllable, may hallucinate or drift from task

## Retrieval-Augmented Dialogue

For a knowledge-grounded platform, the dialogue system integrates retrieval:

```
User utterance
    → Retrieval: find relevant mentor profiles, past conversations, resource articles
    → Augmented context: retrieved content + conversation history
    → LLM: generates response grounded in retrieved context
    → Response + citations
```

This prevents the model from fabricating mentor experiences and grounds recommendations in actual matched profiles.

## Conversation State Tracking

Even in end-to-end systems, explicit state tracking improves reliability:

**Beliefs tracked**:
- User's primary experience (extracted at onboarding, updated over time)
- Current emotional state (from affective classifier)
- Conversation goal: are we in (a) narrative exploration, (b) active mentor search, (c) crisis support?
- Outstanding questions: what has the user asked that hasn't been answered?

**State representation**:
```json
{
  "user_id": "u_8421",
  "primary_experience": "cancer diagnosis, stage 2 breast cancer, 2024",
  "current_emotion": {"dominant": "anxious", "intensity": 0.7},
  "conversation_goal": "mentor_search",
  "session_turn": 4,
  "pending_questions": ["treatment options", "hair loss timeline"]
}
```

## Multi-Turn Context Management

LLMs have finite context windows. For long conversations:
- **Rolling window**: keep last N turns in context
- **Summarization**: compress older turns into a running summary
- **Memory extraction**: extract key facts (user's name, situation details) and inject as structured context at each turn

Claude's 1M token context window reduces the need for aggressive truncation, but structured memory injection still improves coherence.

## Dialogue Policies for Supportive Conversations

The dialogue manager enforces conversation policies appropriate for peer support:

**Validation-first policy**: before any information-giving or action, validate the user's emotional experience. ("That sounds incredibly difficult" before "Here are some resources.")

**One-question-at-a-time**: avoid overwhelming users with multiple questions in a single turn.

**Reflection before advice**: summarize what you've heard before offering perspective.

**Pacing control**: if the user is sharing something heavy, don't immediately pivot to next steps. Allow silence equivalents ("Take your time — I'm here").

**Graceful uncertainty**: if the system doesn't know, say so. "I don't have enough information to suggest a mentor yet — can you tell me more about..."

## Evaluation Metrics for Dialogue Systems

| Metric | Method |
|--------|--------|
| Task completion rate | Did the user find a mentor / get the information they needed? |
| Conversation coherence | Human judges rate coherence 1-5 |
| Empathy score | Trained classifier or human rating |
| Dialogue efficiency | Turns to task completion |
| User-reported satisfaction | Post-session NPS or Likert scale |

Automated metrics (BLEU, ROUGE) are poor proxies for dialogue quality — they measure n-gram overlap, not empathy or task success.

## Connection to This Project

The platform implements an LLM-based end-to-end dialogue system with explicit state tracking injected as structured system prompt context at each turn. Conversation policy rules (validation-first, one-question-at-a-time) are enforced through system prompt instructions rather than a hardcoded state machine, allowing natural language flexibility while maintaining structural guarantees.
