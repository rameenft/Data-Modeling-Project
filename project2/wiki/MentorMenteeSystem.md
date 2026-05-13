# MentorMenteeSystem

## Overview

The MentorMenteeSystem manages the two-sided market of peer support relationships on the platform. It handles mentor onboarding, capacity management, match assignment, conversation facilitation, and the ongoing health of mentoring relationships. The fundamental premise is reciprocal value: mentors gain by articulating their recovery; mentees gain a lived roadmap.

## Key Concepts

- **Two-sided market**: both mentor and mentee must accept a match for it to activate. This is distinct from one-sided recommendation (e.g., suggesting products). The Gale-Shapley stable matching formulation underpins the assignment algorithm.
- **Mentor capacity**: maximum number of active mentees a mentor supports simultaneously. Default: 3. Enforced by [[ExperienceMatching]] to prevent mentor burnout.
- **Mentor readiness**: a status transition — users move from "active" (experiencing) to "graduated" (resolved) to "mentor-ready" (prepared to support others). The transition is user-initiated and confirmed by a brief readiness interview.
- **Match acceptance rate**: the primary short-term matching quality metric. Target: > 60% of suggested matches accepted by both parties.
- **Relationship health score**: a composite score derived from conversation frequency, session length, mentee affect trajectory (see [[AffectiveComputing]]), and self-reported satisfaction.

## Mentor Onboarding

Mentor onboarding produces the experience record that drives [[ExperienceMatching]]:
1. Guided narrative interview (voice or text): "Tell me about the experience you went through."
2. LLM extracts structured record (see [[ExperienceStorageRetrieval]])
3. Embedding computed and stored
4. Mentor sets availability preferences (hours/week, preferred communication style, topics willing to discuss)
5. Readiness assessment: 5-question structured interview assessing emotional distance from the experience

## Handling the Cold-Start Problem

New users have no experience narrative. Solutions:
- **Structured onboarding interview**: 8–10 guided questions generate a synthetic narrative immediately
- **Progressive disclosure**: users can start with a sparse record and add detail over time; matching quality improves incrementally
- **Collaborative filtering fallback**: if embedding similarity is unavailable, match on structured fields (category, subcategory) until behavioral data accumulates

## Mentor Burnout Prevention

Peer mentors are volunteers, not therapists. The system protects them:
- Hard capacity cap (default 3 active mentees)
- Automated check-ins: "You've been talking with [mentee] for 6 weeks — how are you feeling about the relationship?"
- Mentor-only community space: a private forum for mentors to share challenges and get peer support
- Structured off-ramps: "This relationship has reached a natural milestone. Would you like to close the formal mentorship and move to open contact?"
- Crisis detection on mentor conversations too (see [[SafetyAndEscalation]]): mentors can experience secondary trauma

## Evaluation Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Match acceptance rate | Both parties accept the suggested match | > 60% |
| First message within 48h | Conversation started promptly after match | > 70% |
| 4-week retention | Still talking at 4 weeks | > 40% |
| Mentee helpfulness score | Post-session 1–5 survey | > 4.0 |
| Mentor satisfaction | Monthly 1–5 survey | > 3.8 |
| Mentor burnout rate | Mentors who stop taking new mentees | < 10% per quarter |

## AI Mediator Role in First Connection

The [[DialogueSystem]] AI mediator facilitates the first conversation between a matched pair:
- Introduces both parties to each other (with consent-approved experience summaries)
- Sets conversation norms ("This is a peer support conversation — both of you are the expert on your own experience")
- Moderates early turns if conversation stalls
- Withdraws gradually as the pair develops their own rapport

## Design Implications

- **Reciprocity messaging**: framing both mentor and mentee as mutual contributors (not helper/helped) reduces stigma and increases mentor willingness to share vulnerably.
- **Match explanation transparency**: as described in [[ExperienceMatching]], the match explanation must be shown to both parties — it increases acceptance rates and sets the right expectations.
- **Long-term relationship tracking**: mentor-mentee relationships may evolve into friendships, peer collaborations, or informal ongoing support beyond the platform's facilitation. The system should gracefully support this transition rather than fighting it.

## See Also

- [[ExperienceMatching]]
- [[EmpathyDesign]]
- [[SafetyAndEscalation]]
- [[DialogueSystem]]
- [[ExperienceStorageRetrieval]]
