# SafetyAndEscalation

## Overview

SafetyAndEscalation covers the systems designed to protect users in distress, prevent platform misuse, and ensure ethical operation of a platform serving vulnerable populations. Because the platform connects people navigating difficult life experiences, safety is a first-order design concern — not an afterthought.

## Key Concepts

- **Crisis detection**: real-time classification of conversation text for patterns associated with suicidal ideation, self-harm, acute psychological crisis, or imminent danger. Runs as a parallel stream alongside [[AffectiveComputing]] affect classification.
- **Escalation pathway**: the sequence of automated and human responses triggered by a crisis detection event, ranging from surfacing resources to routing to human moderators within 60 seconds.
- **False positive tolerance**: in this domain, over-triggering safety responses is strongly preferable to missing a genuine crisis. Thresholds are tuned conservatively.
- **Secondary trauma prevention**: mentors who regularly engage with distressing narratives are themselves at risk of secondary traumatic stress. The platform monitors mentor conversation patterns for burnout and overload signals.
- **Ethical audit**: a scheduled review process covering demographic bias, affect classification accuracy, safety system performance, and data handling compliance.

## Crisis Detection Architecture

```
User utterance (text + audio)
  → crisis-classifier (parallel to affect-service)
  → distress_score [0, 1]
  → if distress_score > threshold_soft (0.6):
      → surface safety resources in-conversation
      → log to audit trail
  → if distress_score > threshold_hard (0.85):
      → pause AI conversation
      → alert human moderator queue (< 60s response target)
      → display crisis hotlines immediately
      → flag conversation for post-session review
```

The crisis classifier uses a two-model approach:
1. **Fast lexical classifier**: keyword and phrase matching (immediate, < 5ms)
2. **Neural classifier**: fine-tuned RoBERTa on crisis datasets (100–200ms, higher accuracy)

Both classifiers run in parallel; the neural classifier can override a false negative from the lexical classifier.

## Escalation Levels

| Level | Trigger | Response |
|-------|---------|----------|
| 0 — Normal | distress < 0.4 | Standard conversation |
| 1 — Elevated | distress 0.4–0.6 | Subtle tone shift; increased validation focus |
| 2 — Soft Alert | distress 0.6–0.85 | Surface resources; log; notify on-call |
| 3 — Hard Alert | distress > 0.85 | Pause AI; human moderator joins; hotlines displayed |
| 4 — Emergency | imminent danger signal | Same as Level 3 + emergency services notification pathway |

## Human Moderator System

At Level 3+, a trained human moderator joins the conversation:
- Moderator sees full conversation context (with user consent pre-granted at onboarding)
- AI mediator steps back; moderator takes primary conversation role
- Post-session: moderator completes a structured incident report
- Conversation is flagged for review by the clinical advisory board if warranted

## Mentor Safety

Mentors are not trained counselors and can be overwhelmed by mentee crises. The platform:
- Sends crisis alerts to the mentor when their mentee triggers a Level 2+ event
- Provides immediate guidance: "Your mentee may be in distress. The platform's care team has been alerted. You don't need to handle this alone."
- Offers post-incident debrief resources for affected mentors
- Monitors mentor affect trajectories for secondary trauma signals

## Ethical Audit Schedule

| Cadence | Review |
|---------|--------|
| Daily | Automated crisis log review; unresolved escalations |
| Weekly | Human review of sampled crisis conversations |
| Monthly | Affect classifier accuracy audit (200-sample human review) |
| Quarterly | Matching bias audit (demographic parity analysis) |
| Annually | Third-party security and data handling audit |

## Privacy and Consent in Safety Contexts

Safety monitoring requires access to conversation content that users might consider private. Consent is obtained at onboarding:
- Users are informed that conversations are monitored for safety signals
- Aggregated (not individual) affect data may be used for platform improvement
- Emergency situations may involve sharing information with emergency services (disclosed explicitly)
- All safety-related conversation logs are retained for 90 days (versus 30 for standard transcripts), then deleted

## Design Implications

- **No perfect safety**: the platform reduces risk but cannot eliminate it. Clear communication to users and mentors about platform limitations is essential.
- **Moderator training and support**: human moderators face secondary trauma. Rotating schedules, mandatory breaks, peer supervision, and access to professional support are required.
- **Bias in crisis detection**: crisis classifiers trained on majority-population data may underperform for users expressing distress in culturally specific ways. Monthly audits specifically sample across demographic groups.
- **Audit trail immutability**: all safety events are written to an append-only audit log. Moderators and platform operators cannot delete or modify safety records.

## See Also

- [[AffectiveComputing]]
- [[DialogueSystem]]
- [[EmpathyDesign]]
- [[MentorMenteeSystem]]
- [[PlatformArchitecture]]
