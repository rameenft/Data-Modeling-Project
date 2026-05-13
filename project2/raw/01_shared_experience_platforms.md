# Shared Experience Platforms: Design Principles and Architecture

## Overview

Shared experience platforms connect individuals based on common life events, challenges, or milestones. Unlike traditional social networks that connect users by demographics or interests, experience-based platforms treat lived history as the primary signal for meaningful connection. The foundational hypothesis is that empathy is most effectively transmitted between people who have navigated the same territory.

## Key Design Principles

**Experience as Identity**: Users define themselves not by profession or location but by their life events — illness, grief, career transitions, immigration, parenthood. These events carry emotional weight that makes connections deeper and conversations more productive.

**Contextual Relevance**: A 45-year-old cancer survivor and a newly diagnosed 28-year-old share a meaningful connection despite demographic differences. Experience-based matching surfaces this signal above noise.

**Reciprocal Value**: Unlike information-query systems, shared experience platforms produce bidirectional value. The mentor reinforces their own growth by articulating it; the mentee gains a roadmap. This dynamic is central to peer support networks like AA, grief counseling circles, and Reddit communities like r/survivorship.

## Existing Examples

- **Togetherall** (formerly Big White Wall): Anonymous mental health peer support, licensed to universities and employers.
- **7 Cups**: Volunteer listeners matched to people seeking emotional support, using structured conversation flows.
- **PatientsLikeMe**: Medical experience sharing platform where patients document treatment journeys and connect with others on similar paths.
- **Reddit AMAs and support subreddits**: Informal experience-based connection at massive scale.

## Data Architecture Challenges

The core technical challenge is representing "experience" in a machine-readable, matchable form. Three approaches dominate:

1. **Tag-based schemas**: Users select from a predefined taxonomy (e.g., "diagnosed with Type 2 diabetes, 2019"). Simple and queryable but loses nuance.
2. **Free-text narrative storage**: Users write their story; NLP extracts entities and sentiment. Richer but requires robust extraction pipelines.
3. **Structured interview capture**: Platform asks guided questions; answers are stored as structured records. Balances richness with queryability.

## Privacy and Trust Mechanisms

Experience-based platforms handle uniquely sensitive data. Effective mechanisms include:
- Opt-in anonymity toggles per experience type
- Federated identity: profile visible to matched users only
- Time-decay: old experiences can be archived or de-emphasized
- Consent-first data sharing for research use

## Matching Quality Metrics

Evaluating match quality is harder than for product recommendation. Relevant metrics include:
- **Conversation initiation rate**: did the matched pair actually connect?
- **Session length and return rate**: did they have a meaningful exchange?
- **Self-reported value** (post-conversation surveys): did the mentee feel helped?
- **Mentor burnout rate**: are helpers feeling overwhelmed?

## Connection to This Project

This platform builds on these principles by adding two new layers: (1) an AI-mediated conversational interface that removes friction from the first connection, and (2) affective computing that enables the platform to recognize when a conversation is going well versus when a user is in distress, triggering appropriate responses.
