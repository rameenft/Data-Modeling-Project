# Speech-to-Text Pipelines for Conversational AI

## Why Voice Input Matters for Vulnerable Populations

Text input requires cognitive effort and typing skill. For users navigating grief, illness, or emotional distress, typing a coherent narrative may be a barrier. Voice is more natural, faster, and often more emotionally expressive. For the shared experience platform, voice input enables:
- Richer narrative capture (prosody, pacing, emotion)
- Lower friction onboarding for less tech-comfortable users
- Real-time conversation with an AI mediator

## Architecture of a Production STT Pipeline

```
Audio Input (microphone stream / uploaded file)
    → Voice Activity Detection (VAD): detect speech vs. silence
    → Audio preprocessing: noise reduction, normalization, resampling to 16kHz mono
    → Acoustic model: maps audio frames → phoneme probabilities
    → Language model: maps phoneme sequences → word sequences (beam search)
    → Post-processing: punctuation insertion, capitalization, disfluency removal
    → Output: transcript text + word-level timestamps + confidence scores
```

## Leading STT Systems

**OpenAI Whisper** (open source):
- Trained on 680K hours of multilingual audio
- Models: tiny (39M params) to large-v3 (1.5B params)
- Handles accented speech, noisy environments, code-switching
- No real-time streaming in base implementation; WhisperX adds alignment
- Best for: offline transcription of pre-recorded narratives

**Google Speech-to-Text API**:
- Real-time streaming with ~300ms latency
- Speaker diarization (identifies multiple speakers)
- Medical model variant for clinical terminology
- Best for: real-time conversation transcription

**AssemblyAI**:
- Offers sentiment analysis, topic detection, and auto-chapters alongside transcription
- Speaker labels in real-time
- Best for: platforms that want a single API for transcription + analysis

**Deepgram Nova-2**:
- 2-5x faster than real-time on most audio
- Strong on spontaneous speech and conversational register
- SDKs for Python, Node, Go

## Handling Disfluencies and Emotion Markers

Raw speech contains:
- Filler words: "um", "uh", "like", "you know"
- False starts: "I was — I mean — it felt like..."
- Repetitions: "and then and then he said..."
- Emotional breaks: crying, laughter, long silences

For most downstream tasks, disfluencies should be removed. But for affective computing, they are signal:
- High filler word rate → cognitive load, uncertainty
- False starts → emotionally difficult topic
- Long silences → grief, trauma processing

A dual-output pipeline preserves raw transcript (for affect analysis) and produces a cleaned transcript (for NLP downstream tasks).

## Real-Time Streaming Architecture

```
WebSocket (client → server)
    → Audio chunks arrive in ~100ms segments
    → Partial transcript returned after each chunk (interim results)
    → Final transcript returned at end of utterance (end of speech detected)
    → Parallel: audio sent to affective feature extractor
    → Responses generated against partial transcript for low latency
```

Key latency targets:
- VAD to first word: < 500ms
- End-of-utterance to final transcript: < 300ms
- Transcript to AI response generation start: < 200ms
- Total perceived latency (speak → hear response): < 2 seconds

## Multilingual and Accent Considerations

Users of a shared experience platform are globally distributed. STT systems must handle:
- Non-native English speakers with strong accents
- Code-switching (mixing languages mid-sentence)
- Regional dialects

Whisper large-v3 handles 99 languages with reasonable accuracy. For production, a language detection step before transcription improves model selection.

## Privacy in Audio Processing

Audio data is uniquely sensitive — voice is a biometric identifier. Best practices:
- Never store raw audio beyond the transcription session
- Transcripts stored without audio linkage
- On-device STT (Whisper tiny/base running locally) for highest privacy — no data leaves device
- Explicit user consent for any audio analysis beyond transcription

## Connection to This Project

The platform uses a streaming STT pipeline (Whisper or Deepgram) to convert user voice narratives into text, which is then processed by the experience extraction pipeline. Affective features (prosody, disfluency rate, pause patterns) are extracted in parallel from the audio stream before the raw audio is discarded.
