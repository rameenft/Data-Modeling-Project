"""
generate_report2.py
-------------------
Generates the 2-page Project 2 PDF report.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = os.path.join(os.path.dirname(__file__), "INDENG231_Project2_Report.pdf")


def make_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["title"] = ParagraphStyle(
        "title", parent=base["Title"],
        fontSize=16, leading=20, spaceAfter=4, textColor=colors.HexColor("#1a1a2e"),
        alignment=TA_CENTER,
    )
    styles["subtitle"] = ParagraphStyle(
        "subtitle", parent=base["Normal"],
        fontSize=10, leading=14, spaceAfter=10, textColor=colors.HexColor("#555555"),
        alignment=TA_CENTER,
    )
    styles["h1"] = ParagraphStyle(
        "h1", parent=base["Heading1"],
        fontSize=12, leading=16, spaceBefore=10, spaceAfter=4,
        textColor=colors.HexColor("#16213e"),
        borderPad=2,
    )
    styles["h2"] = ParagraphStyle(
        "h2", parent=base["Heading2"],
        fontSize=10.5, leading=14, spaceBefore=6, spaceAfter=3,
        textColor=colors.HexColor("#0f3460"),
    )
    styles["body"] = ParagraphStyle(
        "body", parent=base["Normal"],
        fontSize=9.5, leading=13, spaceAfter=5, alignment=TA_JUSTIFY,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", parent=base["Normal"],
        fontSize=9.5, leading=13, spaceAfter=2,
        leftIndent=14, bulletIndent=4,
    )
    styles["code"] = ParagraphStyle(
        "code", parent=base["Code"],
        fontSize=8.5, leading=12, spaceAfter=5,
        backColor=colors.HexColor("#f5f5f5"),
        leftIndent=12, rightIndent=12,
        borderPad=4,
    )
    styles["caption"] = ParagraphStyle(
        "caption", parent=base["Normal"],
        fontSize=8.5, leading=11, spaceAfter=4,
        textColor=colors.HexColor("#666666"),
        alignment=TA_CENTER,
    )
    return styles


def hr(width=1, color=colors.HexColor("#cccccc")):
    return HRFlowable(width="100%", thickness=width, color=color, spaceAfter=4)


def bullet(text, styles):
    return Paragraph(f"• {text}", styles["bullet"])


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=letter,
        leftMargin=0.85*inch, rightMargin=0.85*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch,
    )
    S = make_styles()
    story = []

    # Header
    story.append(Paragraph("INDENG 231 Course Project 2", S["title"]))
    story.append(Paragraph(
        "LLM-Powered Personal Knowledge Base on<br/>"
        "AI Social Platforms for Shared Human Experiences",
        S["subtitle"]
    ))
    story.append(hr(1.5, colors.HexColor("#16213e")))
    story.append(Spacer(1, 6))

    # ── Section 1: What Was Built ──────────────────────────────────────────
    story.append(Paragraph("1. What Was Built", S["h1"]))
    story.append(hr())

    story.append(Paragraph(
        "This project implements a Karpathy-style personal knowledge base using the Anthropic Claude API. "
        "The system has three layers: (1) a corpus of raw source documents on the project topic, "
        "(2) an LLM-powered compiler that synthesizes the raw sources into structured, interlinked wiki articles, "
        "and (3) a retrieval-augmented Q&A interface that answers questions by grounding responses in the compiled wiki.",
        S["body"]
    ))

    story.append(Paragraph("1.1 Topic", S["h2"]))
    story.append(Paragraph(
        "The knowledge base covers the design of an AI-powered social platform for shared human experiences. "
        "The platform connects users who have navigated similar life challenges (illness, grief, career disruption, "
        "immigration) on a mentor-mentee model, mediated by an AI conversational interface. "
        "The knowledge base synthesizes five research areas: shared experience platform design, "
        "mentor-mentee matching algorithms, affective computing, voice dialogue systems (STT/TTS), "
        "and empathetic AI design.",
        S["body"]
    ))

    story.append(Paragraph("1.2 System Architecture", S["h2"]))
    story.append(Paragraph(
        "The pipeline follows a raw → wiki → Q&A flow:",
        S["body"]
    ))

    arch_data = [
        ["Layer", "Files", "Description"],
        ["Raw sources", "raw/ (10 .md files)", "Source documents covering all topic areas; 47,463 characters total"],
        ["Compiler", "compile_wiki.py", "Claude Opus 4.7 + adaptive thinking; synthesizes wiki articles from raw sources; adds [[WikiLinks]]"],
        ["Wiki", "wiki/ (10 .md files)", "Compiled, interlinked articles; one per major concept; pre-generated and version-controlled"],
        ["Index", "wiki/_index.json", "Link graph: outgoing/incoming link counts, word counts per article"],
        ["Q&A interface", "qa.py", "Keyword retrieval of top-4 relevant articles; Claude Haiku 4.5 generates cited answers"],
    ]
    arch_table = Table(arch_data, colWidths=[1.1*inch, 1.6*inch, 4.0*inch])
    arch_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16213e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4f8")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.3 Raw Sources (10 Documents)", S["h2"]))
    for src in [
        "01: Shared experience platforms — design principles, privacy, matching quality metrics",
        "02: Mentor-mentee matching — embedding-based retrieval, two-stage ranking, cold-start",
        "03: Affective computing — emotion recognition, trajectory modeling, distress detection",
        "04: Speech-to-text pipelines — Whisper, streaming STT, disfluency handling, privacy",
        "05: Text-to-speech synthesis — neural TTS, SSML prosody control, expressive synthesis",
        "06: Dialogue systems — end-to-end neural dialogue, state tracking, conversation policy",
        "07: Empathetic AI design — validation-before-advice, failure modes, empathy measurement",
        "08: Experience storage and retrieval — pgvector, embedding schema, privacy-preserving retrieval",
        "09: Platform integration architecture — microservices, latency budget, feedback loop",
        "10: LLM knowledge base design — this system's own architecture and design rationale",
    ]:
        story.append(bullet(src, S))

    story.append(Spacer(1, 4))
    story.append(Paragraph("1.4 Compiled Wiki (10 Articles)", S["h2"]))
    story.append(Paragraph(
        "The compiler generates one wiki article per major concept. Each article includes: "
        "a Key Concepts section with 5-bullet definitions, a Design Implications section with actionable "
        "takeaways, [[WikiLink]] references to related articles (creating a navigable graph), "
        "and a See Also section. The 10 compiled articles are: "
        "ExperienceMatching, AffectiveComputing, VoiceInterface, DialogueSystem, EmpathyDesign, "
        "MentorMenteeSystem, ExperienceStorageRetrieval, PlatformArchitecture, SafetyAndEscalation, "
        "and KnowledgeBaseDesign.",
        S["body"]
    ))

    wiki_data = [
        ["Article", "Words", "Out Links", "In Links"],
        ["AffectiveComputing", "462", "10", "7"],
        ["DialogueSystem", "596", "8", "7"],
        ["EmpathyDesign", "681", "8", "7"],
        ["ExperienceMatching", "435", "6", "6"],
        ["ExperienceStorageRetrieval", "614", "9", "5"],
        ["KnowledgeBaseDesign", "809", "9", "2"],
        ["MentorMenteeSystem", "659", "12", "4"],
        ["PlatformArchitecture", "687", "7", "6"],
        ["SafetyAndEscalation", "762", "6", "7"],
        ["VoiceInterface", "581", "7", "5"],
    ]
    wiki_table = Table(wiki_data, colWidths=[2.4*inch, 0.8*inch, 0.9*inch, 0.9*inch])
    wiki_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f3460")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4f8")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(wiki_table)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "High incoming link counts for AffectiveComputing and SafetyAndEscalation (7 each) reflect their "
        "centrality in the knowledge domain — nearly every other article references them.",
        S["caption"]
    ))

    # ── Section 2: What Worked / What to Improve ──────────────────────────
    story.append(Spacer(1, 8))
    story.append(Paragraph("2. Evaluation: What Worked and What to Improve", S["h1"]))
    story.append(hr())

    story.append(Paragraph("2.1 What Worked Well", S["h2"]))

    worked = [
        ("Synthesis quality", "Claude added structure, cross-connections, and design implications absent from the raw sources. The compiled wiki is meaningfully better than the sum of its parts — Key Concepts sections distill 500-word raw documents into 5-bullet definitions; Design Implications sections add practical takeaways not in any single source."),
        ("WikiLink coherence", "The LLM naturally identified conceptual dependencies and created appropriate inter-article links without explicit instruction. AffectiveComputing and SafetyAndEscalation emerged as the most-linked hub articles, correctly reflecting their centrality in the platform design."),
        ("Q&A accuracy", "Keyword retrieval correctly identifies relevant articles for all tested questions. Answers cite specific wiki articles and synthesize across multiple sources when relevant (e.g., 'How does the platform respond to a user in crisis?' correctly draws from AffectiveComputing, SafetyAndEscalation, and DialogueSystem)."),
        ("Modularity", "The raw → wiki → Q&A pipeline is topic-agnostic. Replacing the raw/ directory with notes on any other domain and rerunning compile_wiki.py produces a working knowledge base on the new topic with no code changes."),
        ("Pre-compilation strategy", "Committing the pre-generated wiki/ directory to the repository means the Q&A interface is immediately usable — no compilation cost at demo time, no API key needed just to run --list or explore articles."),
    ]
    for title, desc in worked:
        story.append(Paragraph(f"<b>{title}.</b> {desc}", S["body"]))

    story.append(Paragraph("2.2 Limitations and What to Improve", S["h2"]))

    improve = [
        ("Keyword retrieval misses semantic matches", "A question like 'How does the system detect sadness?' does not overlap with the article name 'AffectiveComputing' by keyword. Replacing keyword retrieval with embedding-based approximate nearest-neighbor search (using the same pgvector pattern described in ExperienceStorageRetrieval) would improve recall for semantically similar but lexically distant queries."),
        ("No live incremental compilation", "The wiki is a static snapshot. Adding a new raw source document requires manually rerunning compile_wiki.py. A file-watcher daemon that detects changes to raw/ and re-compiles affected articles would keep the wiki current continuously."),
        ("Single-hop retrieval", "The Q&A interface retrieves top-4 articles but does not follow WikiLinks to transitively relevant articles. Questions spanning multiple concepts (e.g., 'How does affective computing improve mentor matching over time?') would benefit from a graph-walk retrieval that follows links from initially retrieved articles."),
        ("No web rendering of WikiLinks", "The Q&A interface renders [[WikiLink]] as bold text. A web interface (Flask or FastAPI serving a simple HTML frontend) would make these links clickable, enabling wiki-style navigation between articles — the most natural way to explore a knowledge graph."),
        ("Limited evaluation rigor", "Compilation quality was assessed qualitatively. A more rigorous evaluation would measure information coverage (what fraction of facts in raw sources appear in the wiki), hallucination rate (facts in the wiki not traceable to raw sources), and Q&A accuracy on a held-out question set with ground-truth answers derived from the raw sources."),
    ]
    for title, desc in improve:
        story.append(Paragraph(f"<b>{title}.</b> {desc}", S["body"]))

    story.append(Spacer(1, 8))
    story.append(hr(1, colors.HexColor("#16213e")))
    story.append(Paragraph(
        "Project 2 — INDENG 231 Data Modeling  |  Knowledge base topic: AI social platform for shared human experiences  |  "
        "10 raw sources, 10 wiki articles, 6,286 total wiki words, 82 WikiLinks",
        S["caption"]
    ))

    doc.build(story)
    print(f"Report saved: {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
