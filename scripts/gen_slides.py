"""Generate presentation slides as PNG images for the SAFES demo video."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

OUT_DIR = Path(__file__).parent.parent / "docs" / "slides"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080


def get_font(size, bold=False):
    """Try to load a good font, fall back to default."""
    names = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    if bold:
        for n in ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/calibrib.ttf"]:
            try:
                return ImageFont.truetype(n, size)
            except Exception:
                pass
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            pass
    return ImageFont.load_default()


def draw_gradient(draw, x, y, w, h, color1, color2, direction="horizontal"):
    """Draw a gradient rectangle."""
    for i in range(w if direction == "horizontal" else h):
        ratio = i / (w if direction == "horizontal" else h)
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        if direction == "horizontal":
            draw.line([(x + i, y), (x + i, y + h)], fill=(r, g, b))
        else:
            draw.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))


def draw_rounded_rect(draw, xy, radius, fill):
    """Draw a rounded rectangle."""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)


def text_center(draw, text, y, font, fill):
    """Draw centered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, font=font, fill=fill)


# =============================================================================
# SLIDE 1: PROBLEM STATEMENT
# =============================================================================
def slide_problems():
    img = Image.new("RGB", (W, H), (15, 23, 42))  # Dark navy
    draw = ImageDraw.Draw(img)

    # Gradient header bar
    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    # Title
    title_font = get_font(52, bold=True)
    subtitle_font = get_font(24)
    text_center(draw, "PROBLEMS WITH CURRENT AI TOOLS", 50, title_font, (255, 255, 255))
    text_center(draw, "Why students need a better solution for exam preparation", 115, subtitle_font, (148, 163, 184))

    # 6 problem cards (2 rows x 3 cols)
    problems = [
        ("Hallucination", "AI generates false information\nconfidently and without warning", (239, 68, 68), "01"),
        ("No Citations", "No way to verify or\ncross-reference with textbook", (249, 115, 22), "02"),
        ("Syllabus Misalignment", "Answers may be correct but\noutside your exam scope", (234, 179, 8), "03"),
        ("Generic Responses", "Not optimized for\nexam-style answers", (16, 185, 129), "04"),
        ("No Cognitive Levels", "Same response for definitions\nand critical analysis", (14, 165, 233), "05"),
        ("No Transparency", "No confidence score telling\nhow reliable the answer is", (124, 58, 237), "06"),
    ]

    card_w, card_h = 540, 310
    gap_x, gap_y = 40, 35
    start_x = (W - 3 * card_w - 2 * gap_x) // 2
    start_y = 180

    num_font = get_font(80, bold=True)
    card_title_font = get_font(28, bold=True)
    card_body_font = get_font(20)

    for idx, (title, body, accent, num) in enumerate(problems):
        col = idx % 3
        row = idx // 3
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        # Card background
        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 16, (30, 41, 59))

        # Accent top border
        draw.rectangle([x + 16, y, x + card_w - 16, y + 4], fill=accent)

        # Number
        draw.text((x + 30, y + 25), num, font=num_font, fill=(*accent, 60))

        # Title
        draw.text((x + 30, y + 120), title, font=card_title_font, fill=(255, 255, 255))

        # Body
        body_y = y + 165
        for line in body.split("\n"):
            draw.text((x + 30, body_y), line, font=card_body_font, fill=(148, 163, 184))
            body_y += 28

        # Icon circle
        draw_rounded_rect(draw, (x + card_w - 70, y + 25, x + card_w - 25, y + 70), 22, accent)

        # X mark in circle
        cx, cy = x + card_w - 47, y + 47
        cross_font = get_font(24, bold=True)
        draw.text((cx - 7, cy - 14), "X", font=cross_font, fill=(255, 255, 255))

    # Bottom bar
    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))

    # Bottom text
    bottom_font = get_font(22, bold=True)
    text_center(draw, "No existing system combines solutions to ALL these problems.", H - 60, bottom_font, (167, 139, 250))

    img.save(OUT_DIR / "slide_01_problems.png", quality=95)
    print("Created: slide_01_problems.png")


# =============================================================================
# SLIDE 2: SAFES SOLUTION
# =============================================================================
def slide_solution():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Gradient header
    draw_gradient(draw, 0, 0, W, 200, (79, 70, 229), (219, 39, 119), "horizontal")

    # Overlay text on gradient
    badge_font = get_font(16, bold=True)
    title_font = get_font(64, bold=True)
    subtitle_font = get_font(22)

    draw.text((100, 40), "SOURCE-AWARE FRAMEWORK FOR EXAM SUPPORT", font=badge_font, fill=(255, 255, 255, 200))
    draw.text((100, 75), "SAFES", font=title_font, fill=(255, 255, 255))
    text_y = 155
    draw.text((100, text_y), "Exam-focused AI study assistant grounded in your own materials", font=subtitle_font, fill=(255, 255, 255, 220))

    # Feature cards
    features = [
        ("Citation-Grounded", "Every answer includes doc name,\npage number, and section reference", (79, 70, 229)),
        ("Hallucination Control", "Multi-method verification with\nconfidence scoring (0-100%)", (124, 58, 237)),
        ("Bloom's Taxonomy", "Adapts response style to 6\ncognitive levels automatically", (219, 39, 119)),
        ("Multi-Provider LLM", "OpenAI, Anthropic, Gemini,\nOllama - works with any LLM", (16, 185, 129)),
        ("Study Tools", "Study guides, practice tests,\ntopic comparison, key concepts", (14, 165, 233)),
        ("5 UI Themes", "Light, Dark, Midnight,\nSunset, Ocean", (249, 115, 22)),
    ]

    card_w, card_h = 540, 230
    gap_x, gap_y = 40, 30
    start_x = (W - 3 * card_w - 2 * gap_x) // 2
    start_y = 240

    card_title_font = get_font(26, bold=True)
    card_body_font = get_font(19)

    for idx, (title, body, accent) in enumerate(features):
        col = idx % 3
        row = idx // 3
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 14, (30, 41, 59))

        # Left accent bar
        draw.rectangle([x, y + 14, x + 5, y + card_h - 14], fill=accent)

        # Check icon
        draw_rounded_rect(draw, (x + 25, y + 25, x + 60, y + 60), 8, accent)
        check_font = get_font(22, bold=True)
        draw.text((x + 33, y + 30), "V", font=check_font, fill=(255, 255, 255))  # checkmark

        # Title
        draw.text((x + 75, y + 30), title, font=card_title_font, fill=(255, 255, 255))

        # Body
        body_y = y + 85
        for line in body.split("\n"):
            draw.text((x + 30, body_y), line, font=card_body_font, fill=(148, 163, 184))
            body_y += 26

    # Footer
    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))

    footer_font = get_font(20, bold=True)
    text_center(draw, "SAFES  |  FastAPI + Streamlit + RAG  |  91 Automated Tests  |  6,000+ Lines of Python", H - 55, footer_font, (100, 116, 139))

    img.save(OUT_DIR / "slide_02_solution.png", quality=95)
    print("Created: slide_02_solution.png")


# =============================================================================
# SLIDE 3: ARCHITECTURE
# =============================================================================
def slide_architecture():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    title_font = get_font(44, bold=True)
    text_center(draw, "System Architecture", 35, title_font, (255, 255, 255))

    # 4 layer boxes
    layers = [
        ("PRESENTATION LAYER", "Streamlit Frontend  |  5 Themes  |  Interactive Tabs", (219, 39, 119), 130),
        ("API LAYER", "FastAPI  |  REST Endpoints  |  Rate Limiter  |  CORS  |  Pydantic Validation", (167, 139, 250), 280),
        ("BUSINESS LOGIC LAYER", "RAG Engine  |  Hallucination Detector  |  Bloom's Taxonomy  |  Citation Manager", (79, 70, 229), 430),
        ("SERVICE LAYER", "LLM Service (4 providers)  |  Embedding Service  |  Retrieval (Hybrid + Rerank)  |  Document Processors", (14, 165, 233), 580),
    ]

    layer_w = 1600
    layer_h = 110
    layer_x = (W - layer_w) // 2

    layer_title_font = get_font(22, bold=True)
    layer_body_font = get_font(18)
    arrow_font = get_font(28, bold=True)

    for title, body, color, y in layers:
        draw_rounded_rect(draw, (layer_x, y, layer_x + layer_w, y + layer_h), 12, (30, 41, 59))
        draw.rectangle([layer_x, y, layer_x + 8, y + layer_h], fill=color)
        draw.text((layer_x + 30, y + 18), title, font=layer_title_font, fill=color)
        draw.text((layer_x + 30, y + 55), body, font=layer_body_font, fill=(148, 163, 184))

    # Arrows between layers
    for y in [240, 390, 540]:
        cx = W // 2
        draw.text((cx - 8, y + 15), "|", font=arrow_font, fill=(100, 116, 139))
        draw.text((cx - 8, y + 25), "V", font=arrow_font, fill=(100, 116, 139))

    # Data layer at bottom
    data_y = 730
    draw_rounded_rect(draw, (layer_x, data_y, layer_x + layer_w, data_y + layer_h + 30), 12, (30, 41, 59))
    draw.rectangle([layer_x, data_y, layer_x + 8, data_y + layer_h + 30], fill=(16, 185, 129))
    draw.text((layer_x + 30, data_y + 18), "DATA LAYER", font=layer_title_font, fill=(16, 185, 129))

    # Data layer boxes
    data_items = [
        ("ChromaDB / FAISS", "Persistent Vector Store", layer_x + 30),
        ("Document Storage", "PDF, DOCX, TXT, MD", layer_x + 450),
        ("BM25 Index", "Keyword Search", layer_x + 870),
        ("Query History", "JSON Persistence", layer_x + 1200),
    ]

    data_font = get_font(17, bold=True)
    data_sub_font = get_font(14)

    for title, sub, x in data_items:
        draw_rounded_rect(draw, (x, data_y + 55, x + 300, data_y + 120), 8, (22, 33, 49))
        draw.text((x + 15, data_y + 63), title, font=data_font, fill=(255, 255, 255))
        draw.text((x + 15, data_y + 90), sub, font=data_sub_font, fill=(100, 116, 139))

    # Arrow to data
    cx = W // 2
    draw.text((cx - 8, 695), "|", font=arrow_font, fill=(100, 116, 139))
    draw.text((cx - 8, 705), "V", font=arrow_font, fill=(100, 116, 139))

    # Bottom stats
    stats_font = get_font(18, bold=True)
    stats = "80 Python Files  |  91 Tests  |  14 API Endpoints  |  6 Core Services  |  5 Themes"
    text_center(draw, stats, H - 55, stats_font, (100, 116, 139))

    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))

    img.save(OUT_DIR / "slide_03_architecture.png", quality=95)
    print("Created: slide_03_architecture.png")


# =============================================================================
# SLIDE 4: TECH STACK
# =============================================================================
def slide_tech_stack():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    title_font = get_font(44, bold=True)
    text_center(draw, "Technology Stack", 35, title_font, (255, 255, 255))

    stack = [
        ("Frontend", "Streamlit", "Interactive web UI with 5 themes", (255, 75, 75)),
        ("Backend", "FastAPI", "Async REST API with auto-docs", (0, 150, 136)),
        ("Language", "Python 3.11+", "Core runtime", (55, 118, 171)),
        ("Vector DB", "ChromaDB + FAISS", "Persistent embedding storage", (79, 70, 229)),
        ("Embeddings", "Sentence-Transformers", "384-dim semantic vectors", (124, 58, 237)),
        ("LLM", "OpenAI / Claude / Gemini / Ollama", "Multi-provider generation", (16, 185, 129)),
        ("PDF", "pdfplumber + pypdf", "Text & table extraction", (249, 115, 22)),
        ("DOCX", "python-docx", "Word document parsing", (234, 179, 8)),
        ("NLP", "spaCy + NLTK", "Tokenization, NER, lemmatization", (14, 165, 233)),
        ("Tokenizer", "tiktoken", "Token-aware text chunking", (167, 139, 250)),
        ("Validation", "Pydantic v2", "Request/response schemas", (239, 68, 68)),
        ("Testing", "pytest (91 tests)", "Unit + integration suites", (219, 39, 119)),
    ]

    card_w, card_h = 420, 120
    gap_x, gap_y = 30, 22
    cols = 4
    start_x = (W - cols * card_w - (cols - 1) * gap_x) // 2
    start_y = 110

    cat_font = get_font(14, bold=True)
    name_font = get_font(22, bold=True)
    desc_font = get_font(16)

    for idx, (category, name, desc, color) in enumerate(stack):
        col = idx % cols
        row = idx // cols
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 12, (30, 41, 59))

        # Color dot
        draw.ellipse([x + 20, y + 22, x + 34, y + 36], fill=color)

        # Category
        draw.text((x + 45, y + 20), category.upper(), font=cat_font, fill=color)

        # Name
        draw.text((x + 20, y + 50), name, font=name_font, fill=(255, 255, 255))

        # Description
        draw.text((x + 20, y + 82), desc, font=desc_font, fill=(148, 163, 184))

    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))
    img.save(OUT_DIR / "slide_04_tech_stack.png", quality=95)
    print("Created: slide_04_tech_stack.png")


# =============================================================================
# SLIDE 5: DEVELOPMENT PHASES
# =============================================================================
def slide_dev_phases():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    title_font = get_font(44, bold=True)
    text_center(draw, "Development Journey  -  6 Phases", 35, title_font, (255, 255, 255))

    phases = [
        ("Phase 1", "Vector Store\nPersistence", "Real ChromaDB + FAISS\nData survives restarts\n14 new tests", (79, 70, 229)),
        ("Phase 2", "Hybrid Search\n+ Reranking", "BM25 + semantic fusion\nNLP service (spaCy)\n15 new tests", (124, 58, 237)),
        ("Phase 3", "Hallucination\nVerification", "LLM claim-by-claim check\nConfig-driven thresholds\n7 new tests", (219, 39, 119)),
        ("Phase 4", "Rate Limiting", "Per-IP sliding window\nASGI middleware\n3 new tests", (249, 115, 22)),
        ("Phase 5", "Query History", "JSON persistence\nStats API + analytics\n8 new tests", (14, 165, 233)),
        ("Phase 6", "Multi-Provider\nLLM + Topics", "4 LLM providers\nTopic comparison\n4 new tests", (16, 185, 129)),
    ]

    card_w, card_h = 260, 480
    gap = 30
    start_x = (W - 6 * card_w - 5 * gap) // 2
    start_y = 120

    phase_font = get_font(16, bold=True)
    phase_title_font = get_font(22, bold=True)
    phase_body_font = get_font(15)

    for idx, (phase, title, body, color) in enumerate(phases):
        x = start_x + idx * (card_w + gap)
        y = start_y

        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 14, (30, 41, 59))

        # Phase number badge
        draw_rounded_rect(draw, (x + 15, y + 15, x + card_w - 15, y + 55), 8, color)
        bbox = draw.textbbox((0, 0), phase, font=phase_font)
        tw = bbox[2] - bbox[0]
        draw.text((x + (card_w - tw) // 2, y + 23), phase, font=phase_font, fill=(255, 255, 255))

        # Title
        title_y = y + 80
        for line in title.split("\n"):
            draw.text((x + 20, title_y), line, font=phase_title_font, fill=(255, 255, 255))
            title_y += 30

        # Separator
        draw.rectangle([x + 20, title_y + 10, x + card_w - 20, title_y + 11], fill=(51, 65, 85))

        # Body
        body_y = title_y + 25
        for line in body.split("\n"):
            draw.text((x + 20, body_y), line, font=phase_body_font, fill=(148, 163, 184))
            body_y += 24

        # Arrow to next phase
        if idx < 5:
            ax = x + card_w + 5
            ay = y + card_h // 2
            draw.text((ax, ay - 12), ">", font=get_font(24, bold=True), fill=(100, 116, 139))

    # Bottom bar
    bottom_font = get_font(20, bold=True)
    text_center(draw, "Total: 91 Tests  |  18 New Files  |  16 Modified Files  |  All Pushed to GitHub", H - 55, bottom_font, (100, 116, 139))

    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))
    img.save(OUT_DIR / "slide_05_dev_phases.png", quality=95)
    print("Created: slide_05_dev_phases.png")


# =============================================================================
# RUN ALL
# =============================================================================
if __name__ == "__main__":
    slide_problems()
    slide_solution()
    slide_architecture()
    slide_tech_stack()
    slide_dev_phases()
    print(f"\nAll slides saved to: {OUT_DIR}")
