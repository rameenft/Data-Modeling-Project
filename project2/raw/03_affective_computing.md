# Affective Computing: Recognizing and Responding to Emotional States

## What Is Affective Computing?

Affective computing (Picard, 1997) is the study of systems that recognize, interpret, process, and simulate human affect — emotions, moods, and attitudes. In the context of social platforms, affective computing enables the system to detect when a conversation is going well, when a user is in distress, or when a mentor is becoming overwhelmed, and to respond accordingly.

The three core capabilities are:
1. **Affect recognition**: identify the user's emotional state from input signals
2. **Affect modeling**: maintain a dynamic model of emotional state over time
3. **Affect generation**: produce responses calibrated to the detected state

## Input Modalities for Affect Recognition

**Text**:
- Sentiment analysis: positive/negative/neutral polarity
- Emotion classification: joy, sadness, anger, fear, surprise, disgust (Ekman's basic emotions)
- Distress signals: crisis language detection (hopelessness, self-harm ideation)
- Hedging and uncertainty markers: "I don't know if this makes sense" indicates low confidence

**Voice/Audio**:
- Prosody: pitch, speech rate, pausing patterns
- Volume dynamics: whispered vs. loud speech
- Voice quality: trembling, breathiness (associated with anxiety)
- Acoustic features: MFCCs (Mel-frequency cepstral coefficients), zero-crossing rate

**Multimodal fusion**:
Most robust systems combine text and audio signals. Audio catches what text misses (e.g., sarcasm, masked distress). Text catches nuance that audio misses (e.g., careful word choices indicating shame).

## Text-Based Affect Recognition Pipeline

```
User input (text)
    → Preprocessing: tokenization, normalization
    → Feature extraction: TF-IDF, embeddings, linguistic features
    → Classification: fine-tuned BERT/RoBERTa for emotion labels
    → Output: probability distribution over emotion categories
          + distress severity score (0-1)
          + engagement quality score (0-1)
```

State-of-the-art models: **GoEmotions** (Google, 2020) — 27 emotion categories on Reddit data. **EmoRoBERTa** — fine-tuned for nuanced emotional text. **VADER** — rule-based, fast, good for social media.

## LLM-Based Affective Response Generation

Large language models can be prompted to generate affectively calibrated responses:

```
System prompt: You are an empathetic facilitator on a peer support platform.
The user appears to be in emotional distress (distress score: 0.82).
Respond with warmth, validate their feelings, and avoid giving advice.
Do not minimize their experience. Ask one open-ended question.
```

This approach lets the platform dynamically adjust tone without maintaining separate response models per emotion category.

## Crisis Detection and Escalation

Any platform dealing with vulnerable populations needs a crisis layer:
- Trained classifiers detect language patterns associated with suicidal ideation, self-harm, or acute crisis
- Crisis-flagged conversations are immediately escalated to human moderators
- Auto-generated safety resources are surfaced (crisis hotlines, professional referrals)
- The AI moderates its own behavior: no advice-giving, only validation and redirection

**False positive tolerance**: in this domain, it is better to over-flag than to miss a genuine crisis.

## Emotional Trajectory Modeling

A single affect score is insufficient. The platform maintains an **emotional trajectory** for each user across sessions:
- Are they trending toward more positive states over time? (good sign)
- Are they stuck in the same emotional register for multiple sessions? (intervention signal)
- Did a match produce a measurable lift in positive affect? (match quality signal)

This trajectory data feeds back into the matching algorithm: mentors who consistently produce positive trajectory shifts in mentees are surfaced more frequently.

## Ethical Dimensions

Affective computing raises serious ethical questions:
- **Consent**: users may not realize their emotional state is being classified
- **Accuracy disparities**: models trained on majority populations may underperform for minority groups, misclassifying culturally specific expression
- **Manipulation risk**: a system that knows your emotional state has disproportionate influence — this must be constrained to supportive, not persuasive, ends
- **Data sensitivity**: emotional state data is among the most sensitive personal information imaginable; storage and access must be tightly controlled

## Connection to This Project

The platform uses LLM-based affect classification on conversation text to: (1) calibrate the AI's response tone in real-time, (2) detect crisis signals and trigger escalation, and (3) compute match quality by tracking emotional trajectory improvements across sessions with a given mentor.
