"""
qa.py
-----
Q&A interface over the compiled wiki knowledge base.

Usage:
    python qa.py                          # interactive mode
    python qa.py --question "How does affective computing work?"
    python qa.py --list                   # list available wiki articles
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

WIKI_DIR = os.path.join(os.path.dirname(__file__), "wiki")
INDEX_PATH = os.path.join(WIKI_DIR, "_index.json")

client = anthropic.Anthropic()


def load_wiki() -> dict[str, str]:
    articles = {}
    if not os.path.isdir(WIKI_DIR):
        return articles
    for fname in os.listdir(WIKI_DIR):
        if fname.endswith(".md") and not fname.startswith("_"):
            path = os.path.join(WIKI_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                topic = fname[:-3]  # strip .md
                articles[topic] = f.read()
    return articles


def load_index() -> dict:
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def keyword_retrieve(question: str, articles: dict[str, str], top_k: int = 4) -> list[str]:
    """Simple keyword overlap retrieval — no embeddings needed for a small wiki."""
    q_words = set(re.findall(r"\b\w{4,}\b", question.lower()))
    scores = {}
    for topic, content in articles.items():
        content_words = set(re.findall(r"\b\w{4,}\b", content.lower()))
        topic_words = set(re.findall(r"\b\w{4,}\b", topic.lower()))
        overlap = len(q_words & (content_words | topic_words))
        scores[topic] = overlap
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [t for t, _ in ranked[:top_k] if scores[t] > 0]


def render_wikilinks(text: str, available_topics: set) -> str:
    """Render [[WikiLink]] as (see: WikiLink) with availability check."""
    def replace(match):
        topic = match.group(1)
        if topic in available_topics:
            return f"**{topic}**"
        return f"*{topic}*"
    return re.sub(r"\[\[([^\]]+)\]\]", replace, text)


def answer_question(question: str, articles: dict[str, str]) -> tuple[str, list[str]]:
    if not articles:
        return "No wiki articles found. Run compile_wiki.py first.", []

    relevant_topics = keyword_retrieve(question, articles, top_k=4)

    if not relevant_topics:
        relevant_topics = list(articles.keys())[:3]

    context_parts = []
    for topic in relevant_topics:
        content = articles[topic]
        context_parts.append(f"=== Wiki Article: {topic} ===\n{content}")

    context = "\n\n".join(context_parts)

    prompt = f"""You are answering questions using a compiled wiki knowledge base about:
"AI-powered social platform for shared human experiences — mentor-mentee matching,
affective computing, voice dialogue systems, and empathetic AI."

Relevant wiki articles:
{context}

---

Question: {question}

Instructions:
- Answer concisely and accurately using only the wiki content above
- Cite the wiki articles you draw from (e.g., "According to ExperienceMatching,...")
- If the answer spans multiple articles, synthesize them
- If the wiki doesn't cover the question, say so clearly
- Use bullet points for multi-part answers
- Keep the answer under 300 words"""

    print("\nGenerating answer", end="", flush=True)
    answer = ""
    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            answer += text
            print(".", end="", flush=True)

    print()  # newline
    answer = render_wikilinks(answer, set(articles.keys()))
    return answer, relevant_topics


def interactive_mode(articles: dict[str, str]):
    print("\n" + "="*60)
    print("  Knowledge Base Q&A — AI Social Platform Wiki")
    print("="*60)
    print(f"  {len(articles)} wiki articles loaded")
    print("  Type 'quit' to exit, 'list' to see all articles\n")

    while True:
        try:
            question = input("Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            break
        if question.lower() == "list":
            print("\nAvailable wiki articles:")
            for topic in sorted(articles.keys()):
                wc = len(articles[topic].split())
                print(f"  - {topic} ({wc} words)")
            print()
            continue

        answer, sources = answer_question(question, articles)
        print(f"\nAnswer:\n{answer}")
        print(f"\nSources used: {', '.join(sources)}\n")
        print("-" * 40)


def main():
    parser = argparse.ArgumentParser(description="Q&A over compiled wiki")
    parser.add_argument("--question", "-q", help="Ask a single question and exit")
    parser.add_argument("--list", "-l", action="store_true", help="List all wiki articles")
    args = parser.parse_args()

    articles = load_wiki()

    if not articles:
        print("No wiki articles found in wiki/. Run compile_wiki.py first.")
        return

    if args.list:
        index = load_index()
        print(f"\nWiki Knowledge Base — {len(articles)} articles\n")
        for topic in sorted(articles.keys()):
            meta = index.get(topic, {})
            wc = meta.get("word_count", len(articles[topic].split()))
            links = len(meta.get("outgoing_links", []))
            print(f"  {topic:35s} {wc:4d} words  {links:2d} links")
        return

    if args.question:
        answer, sources = answer_question(args.question, articles)
        print(f"\nQuestion: {args.question}")
        print(f"\nAnswer:\n{answer}")
        print(f"\nSources: {', '.join(sources)}")
    else:
        interactive_mode(articles)


if __name__ == "__main__":
    main()
