"""
compile_wiki.py
---------------
Reads all raw source documents and uses Claude to synthesize a structured,
interlinked wiki knowledge base.

Usage:
    python compile_wiki.py [--topic TOPIC] [--force]

Options:
    --force   Recompile all articles even if wiki/ already exists
"""

import os
import re
import json
import argparse

# Support .env file for API key
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            if _line.startswith("ANTHROPIC_API_KEY="):
                os.environ.setdefault("ANTHROPIC_API_KEY", _line.strip().split("=", 1)[1])

import anthropic

RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
WIKI_DIR = os.path.join(os.path.dirname(__file__), "wiki")
INDEX_PATH = os.path.join(WIKI_DIR, "_index.json")

client = anthropic.Anthropic()

TOPIC_OVERVIEW = "AI-powered social platform for shared human experiences: mentor-mentee matching, affective computing, voice-driven dialogue, and empathetic AI design"

WIKI_TOPICS = [
    ("ExperienceMatching", "How the platform matches users based on shared lived experiences, including embedding-based retrieval and re-ranking"),
    ("AffectiveComputing", "Emotion recognition, affect classification, emotional trajectory modeling, and crisis detection in conversation"),
    ("VoiceInterface", "Speech-to-text and text-to-speech pipelines, streaming architecture, and latency design for voice-first interaction"),
    ("DialogueSystem", "Real-time dialogue architecture, conversation state tracking, and LLM-based multi-turn conversation management"),
    ("EmpathyDesign", "Design principles for empathetic AI: validation-before-advice, failure modes, prompt engineering for empathy, and measuring empathy quality"),
    ("MentorMenteeSystem", "Two-sided mentor-mentee matching, capacity management, onboarding, cold-start handling, and evaluation metrics"),
    ("ExperienceStorageRetrieval", "Data architecture for storing and retrieving experience narratives: schema design, vector databases, pgvector, and privacy-preserving retrieval"),
    ("PlatformArchitecture", "End-to-end system architecture: microservices, latency budget, state management, scaling, and continuous improvement loop"),
    ("SafetyAndEscalation", "Crisis detection, escalation pathways, ethical review processes, and content safety for vulnerable population platforms"),
    ("KnowledgeBaseDesign", "LLM-powered personal knowledge base design: compilation pipeline, wiki link graph, Q&A interface, and incremental updates"),
]


def load_raw_sources() -> dict[str, str]:
    sources = {}
    for fname in sorted(os.listdir(RAW_DIR)):
        if fname.endswith(".md"):
            path = os.path.join(RAW_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                sources[fname] = f.read()
    return sources


def compile_article(topic: str, description: str, raw_sources: dict[str, str]) -> str:
    all_other_topics = [t for t, _ in WIKI_TOPICS if t != topic]

    sources_text = "\n\n".join(
        f"=== {fname} ===\n{content}" for fname, content in raw_sources.items()
    )

    prompt = f"""You are writing a wiki knowledge base on the topic: {TOPIC_OVERVIEW}

You have the following raw source documents available:

{sources_text}

---

Write a comprehensive wiki article on the specific topic: **{topic}**
Topic description: {description}

Requirements:
1. Use markdown with clear headers (## for sections, ### for subsections)
2. Synthesize across ALL relevant raw sources — do not copy; add structure and connections
3. Use [[WikiLink]] format to reference related wiki articles from this list: {all_other_topics}
   Use WikiLinks naturally within the text, not just in "See Also"
4. Include a "## Key Concepts" section with 3-5 bullet-point definitions
5. Include a "## Design Implications" section with actionable design takeaways
6. Include a "## See Also" section listing 3-5 related wiki articles as [[WikiLinks]]
7. The article should be self-contained and useful to someone reading it first
8. Length: 500-800 words

Write the article now:"""

    print(f"   Compiling: {topic}...")

    full_response = ""
    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=2000,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            full_response += text
            print(text, end="", flush=True)

    print()  # newline after streaming
    return full_response


def extract_wikilinks(text: str) -> list[str]:
    return re.findall(r"\[\[([^\]]+)\]\]", text)


def build_index(articles: dict[str, str]) -> dict:
    index = {}
    for topic, content in articles.items():
        links = extract_wikilinks(content)
        word_count = len(content.split())
        index[topic] = {
            "filename": f"{topic}.md",
            "word_count": word_count,
            "outgoing_links": links,
        }
    # Add incoming links
    for topic in index:
        index[topic]["incoming_links"] = [
            t for t, meta in index.items()
            if topic in meta["outgoing_links"]
        ]
    return index


def main():
    parser = argparse.ArgumentParser(description="Compile wiki from raw sources")
    parser.add_argument("--force", action="store_true", help="Recompile all articles")
    parser.add_argument("--topic", help="Compile only this topic")
    args = parser.parse_args()

    os.makedirs(WIKI_DIR, exist_ok=True)

    print(f"Loading raw sources from {RAW_DIR}...")
    raw_sources = load_raw_sources()
    print(f"Loaded {len(raw_sources)} source documents ({sum(len(v) for v in raw_sources.values()):,} chars total)\n")

    topics_to_compile = WIKI_TOPICS
    if args.topic:
        topics_to_compile = [(t, d) for t, d in WIKI_TOPICS if t == args.topic]
        if not topics_to_compile:
            print(f"Topic '{args.topic}' not found. Available: {[t for t, _ in WIKI_TOPICS]}")
            return

    compiled = {}
    for topic, description in topics_to_compile:
        wiki_path = os.path.join(WIKI_DIR, f"{topic}.md")
        if os.path.exists(wiki_path) and not args.force:
            print(f"   Skipping (exists): {topic}  [use --force to recompile]")
            with open(wiki_path, "r", encoding="utf-8") as f:
                compiled[topic] = f.read()
            continue

        article = compile_article(topic, description, raw_sources)
        wiki_path = os.path.join(WIKI_DIR, f"{topic}.md")
        with open(wiki_path, "w", encoding="utf-8") as f:
            f.write(f"# {topic}\n\n")
            f.write(article)
        compiled[topic] = article

    # Write index
    index = build_index(compiled)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Wiki compiled: {len(compiled)} articles in {WIKI_DIR}/")
    print(f"Index written: {INDEX_PATH}")
    print("\nLink graph summary:")
    for topic, meta in index.items():
        print(f"  {topic}: {meta['word_count']} words, "
              f"{len(meta['outgoing_links'])} outgoing links, "
              f"{len(meta['incoming_links'])} incoming links")


if __name__ == "__main__":
    main()
