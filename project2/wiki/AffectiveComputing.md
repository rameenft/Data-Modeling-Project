# AffectiveComputing

## Overview

Affective computing enables the platform to recognize, track, and respond to users' emotional states in real time. It underpins the AI mediator's ability to calibrate tone, detect crisis signals, and measure match quality through emotional trajectory analysis.

## Key Concepts

- **Affect recognition**: classifying the user's emotional state from text, audio, or both. Output is a probability distribution over emotion categories (joy, sadness, anxiety, anger, etc.) plus a scalar distress severity score (0–1).
- **Emotional trajectory**: a per-user time series of affect scores across sessions. A trajectory trending toward more positive states indicates a healthy mentor relationship; stagnation or regression triggers intervention.
- **Distress threshold**: a configurable distress score above which the [[SafetyAndEscalation]] system activates — routing the conversation to human moderators and surfacing crisis resources.
- **Multimodal fusion**: combining text sentiment and audio prosody features yields more accurate affect classification than either modality alone. Particularly useful for detecting masked distress.
- **Affective response calibration**: using the detected emotion to select TTS prosody settings (see [[VoiceInterface]]) and adjust the AI mediator's language register.

## Text-Based Affect Recognition

For text input, the pipeline uses a fine-tuned transformer model (RoBERTa or similar, trained on GoEmotions) to produce per-turn emotion labels. Additional heuristics detect:
- High filler word density → cognitive load / uncertainty
- First-person distress language → depression signal
- Minimization language ("it's fine, I'm okay") → masked distress

## Audio-Based Affect Recognition

For voice input, acoustic features are extracted in parallel with STT transcription (see [[VoiceInterface]]):
- MFCCs (Mel-frequency cepstral coefficients)
- Pitch mean and variance (higher pitch variance → emotional arousal)
- Speech rate (slower speech → sadness or thoughtfulness)
- Long pauses (> 3 seconds) → grief, trauma processing

These features feed a lightweight classifier (MLP or SVM) producing a parallel affect score that is fused with the text-based score.

## Match Quality Through Trajectory Analysis

The emotional trajectory provides a match quality signal:
- Positive trajectory shift across sessions with a given mentor → high match quality; surface this mentor more frequently
- No change or negative trajectory → review the match; offer the mentee an alternative

This feedback loop continuously improves the [[ExperienceMatching]] re-ranking model without requiring explicit user ratings.

## Design Implications

- **Consent transparency**: users must be informed that their emotional state is being classified; opt-out must be available with graceful degradation.
- **Accuracy disparities**: classifier performance varies by demographic and cultural background. Regular audits (see [[SafetyAndEscalation]]) are mandatory.
- **Conservative distress thresholds**: in this domain, false positives (over-triggering safety) are far preferable to false negatives (missing a genuine crisis).
- **No persuasion use**: affective data is used only to calibrate supportive responses, never for persuasive or commercial ends.

## See Also

- [[VoiceInterface]]
- [[DialogueSystem]]
- [[EmpathyDesign]]
- [[SafetyAndEscalation]]
- [[PlatformArchitecture]]
