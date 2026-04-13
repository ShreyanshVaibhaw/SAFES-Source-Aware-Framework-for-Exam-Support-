"""Generate 4 detailed slides for the Development Journey & Challenges section."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).parent.parent / "docs" / "slides"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080


def get_font(size, bold=False):
    names_bold = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    names_regular = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    for n in (names_bold if bold else names_regular):
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            pass
    return ImageFont.load_default()


def draw_gradient(draw, x, y, w, h, c1, c2, direction="horizontal"):
    for i in range(w if direction == "horizontal" else h):
        ratio = i / max(1, (w if direction == "horizontal" else h) - 1)
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        if direction == "horizontal":
            draw.line([(x + i, y), (x + i, y + h)], fill=(r, g, b))
        else:
            draw.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))


def draw_rounded_rect(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.pieslice([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=fill)
    draw.pieslice([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=fill)


def text_center(draw, text, y, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, font=font, fill=fill)


def draw_phase_badge(draw, x, y, phase_num, color):
    """Draw a small phase number badge."""
    draw_rounded_rect(draw, (x, y, x + 110, y + 36), 8, color)
    f = get_font(15, bold=True)
    draw.text((x + 12, y + 8), f"PHASE {phase_num}", font=f, fill=(255, 255, 255))


def draw_section(draw, x, y, w, title, items, title_color, icon_char=""):
    """Draw a section with title and bullet items."""
    tf = get_font(22, bold=True)
    bf = get_font(17)

    if icon_char:
        draw.text((x, y), icon_char, font=get_font(22), fill=title_color)
        draw.text((x + 30, y), title, font=tf, fill=title_color)
    else:
        draw.text((x, y), title, font=tf, fill=title_color)

    item_y = y + 38
    for item in items:
        draw.text((x + 15, item_y), "-", font=bf, fill=(100, 116, 139))
        # Wrap long lines
        words = item.split()
        line = ""
        for word in words:
            test = line + " " + word if line else word
            bbox = draw.textbbox((0, 0), test, font=bf)
            if bbox[2] - bbox[0] > w - 40:
                draw.text((x + 30, item_y), line, font=bf, fill=(203, 213, 225))
                item_y += 24
                line = word
            else:
                line = test
        if line:
            draw.text((x + 30, item_y), line, font=bf, fill=(203, 213, 225))
            item_y += 28
    return item_y


# =============================================================================
# CHALLENGE SLIDE 1: Vector Store Persistence + Hybrid Search
# =============================================================================
def challenge_slide_1():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    # Title
    text_center(draw, "Challenge 1: Making Data Persist & Search Smarter", 40, get_font(40, bold=True), (255, 255, 255))
    text_center(draw, "Phases 1 & 2  |  Vector Store Persistence + Hybrid Search + Reranking", 95, get_font(20), (148, 163, 184))

    # Left panel - THE PROBLEM
    panel_x, panel_y = 80, 155
    panel_w = 850
    draw_rounded_rect(draw, (panel_x, panel_y, panel_x + panel_w, panel_y + 400), 16, (30, 41, 59))

    draw_phase_badge(draw, panel_x + 20, panel_y + 20, "1", (239, 68, 68))
    draw.text((panel_x + 145, panel_y + 24), "THE PROBLEM", font=get_font(20, bold=True), fill=(239, 68, 68))

    draw_section(draw, panel_x + 30, panel_y + 75, panel_w, "Before", [
        "Vector stores were in-memory Python dictionaries",
        "Every server restart wiped ALL uploaded documents",
        "Users had to re-upload everything after each deployment",
        "ChromaDB and FAISS libraries were installed but never used",
        "Search was pure semantic - missed keyword-specific facts",
    ], (239, 68, 68), "X")

    # Left panel bottom - code snippet
    code_y = panel_y + 310
    draw_rounded_rect(draw, (panel_x + 25, code_y, panel_x + panel_w - 25, code_y + 70), 8, (15, 23, 42))
    code_font = get_font(14)
    draw.text((panel_x + 40, code_y + 8), "# OLD: Data lost on restart", font=code_font, fill=(100, 116, 139))
    draw.text((panel_x + 40, code_y + 28), "self._records: Dict[str, StoredChunk] = {}  # in-memory only!", font=code_font, fill=(239, 68, 68))
    draw.text((panel_x + 40, code_y + 48), "# No persistence, no disk writes, no reload", font=code_font, fill=(100, 116, 139))

    # Right panel - THE SOLUTION
    panel_x2 = 980
    draw_rounded_rect(draw, (panel_x2, panel_y, panel_x2 + panel_w, panel_y + 400), 16, (30, 41, 59))

    draw_phase_badge(draw, panel_x2 + 20, panel_y + 20, "1-2", (16, 185, 129))
    draw.text((panel_x2 + 145, panel_y + 24), "THE SOLUTION", font=get_font(20, bold=True), fill=(16, 185, 129))

    draw_section(draw, panel_x2 + 30, panel_y + 75, panel_w, "After", [
        "ChromaDB PersistentClient with cosine similarity index",
        "FAISS IndexFlatIP with JSON metadata + disk persistence",
        "Data survives restarts - upload once, query forever",
        "BM25 keyword search combined via Reciprocal Rank Fusion",
        "Reranker with keyword + entity overlap scoring",
    ], (16, 185, 129), "V")

    code_y2 = panel_y + 310
    draw_rounded_rect(draw, (panel_x2 + 25, code_y2, panel_x2 + panel_w - 25, code_y2 + 70), 8, (15, 23, 42))
    draw.text((panel_x2 + 40, code_y2 + 8), "# NEW: Real persistent storage", font=code_font, fill=(100, 116, 139))
    draw.text((panel_x2 + 40, code_y2 + 28), "self._client = chromadb.PersistentClient(path=persist_dir)", font=code_font, fill=(16, 185, 129))
    draw.text((panel_x2 + 40, code_y2 + 48), "# + BM25 hybrid search + reranker pipeline", font=code_font, fill=(100, 116, 139))

    # Bottom stats
    stats_y = 600
    stats = [
        ("29", "New Tests", (79, 70, 229)),
        ("6", "Files Modified", (124, 58, 237)),
        ("3", "New Services", (16, 185, 129)),
        ("RRF", "Fusion Algorithm", (14, 165, 233)),
    ]
    stat_w = 380
    stat_gap = 40
    stat_x = (W - len(stats) * stat_w - (len(stats) - 1) * stat_gap) // 2

    for idx, (val, label, color) in enumerate(stats):
        x = stat_x + idx * (stat_w + stat_gap)
        draw_rounded_rect(draw, (x, stats_y, x + stat_w, stats_y + 100), 12, (30, 41, 59))
        draw.text((x + 25, stats_y + 15), val, font=get_font(40, bold=True), fill=color)
        draw.text((x + 25, stats_y + 65), label, font=get_font(16, bold=True), fill=(148, 163, 184))

    # Pipeline diagram at bottom
    pipe_y = 740
    text_center(draw, "Search Pipeline Flow", pipe_y, get_font(22, bold=True), (167, 139, 250))

    steps = [
        ("Query", (79, 70, 229)),
        ("Embedding", (124, 58, 237)),
        ("Semantic\nSearch", (167, 139, 250)),
        ("BM25\nKeyword", (14, 165, 233)),
        ("RRF\nFusion", (219, 39, 119)),
        ("Reranker", (249, 115, 22)),
        ("Top-K\nResults", (16, 185, 129)),
    ]
    step_w, step_h = 200, 80
    step_gap = 30
    step_x = (W - len(steps) * step_w - (len(steps) - 1) * step_gap) // 2
    step_y = pipe_y + 40

    for idx, (label, color) in enumerate(steps):
        x = step_x + idx * (step_w + step_gap)
        draw_rounded_rect(draw, (x, step_y, x + step_w, step_y + step_h), 10, color)
        lines = label.split("\n")
        for li, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=get_font(16, bold=True))
            tw = bbox[2] - bbox[0]
            ly = step_y + (step_h - len(lines) * 22) // 2 + li * 22
            draw.text((x + (step_w - tw) // 2, ly), line, font=get_font(16, bold=True), fill=(255, 255, 255))

        if idx < len(steps) - 1:
            ax = x + step_w + 5
            ay = step_y + step_h // 2 - 8
            draw.text((ax, ay), ">", font=get_font(22, bold=True), fill=(100, 116, 139))

    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))
    img.save(OUT_DIR / "challenge_01_persistence_search.png", quality=95)
    print("Created: challenge_01_persistence_search.png")


# =============================================================================
# CHALLENGE SLIDE 2: Hallucination Detection
# =============================================================================
def challenge_slide_2():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    text_center(draw, "Challenge 2: Detecting AI Hallucinations", 40, get_font(40, bold=True), (255, 255, 255))
    text_center(draw, "Phase 3  |  From Heuristic to LLM-Based Claim Verification", 95, get_font(20), (148, 163, 184))

    # Two-column: Heuristic vs LLM
    col_w = 820
    gap = 60
    col1_x = (W - 2 * col_w - gap) // 2
    col2_x = col1_x + col_w + gap
    col_y = 155

    # Column 1: Heuristic Method
    draw_rounded_rect(draw, (col1_x, col_y, col1_x + col_w, col_y + 500), 16, (30, 41, 59))
    draw_rounded_rect(draw, (col1_x, col_y, col1_x + col_w, col_y + 55), 16, (249, 115, 22))
    draw.rectangle([col1_x, col_y + 40, col1_x + col_w, col_y + 55], fill=(249, 115, 22))
    text_center_x = col1_x + col_w // 2
    f = get_font(20, bold=True)
    bbox = draw.textbbox((0, 0), "METHOD 1: HEURISTIC (Fast Fallback)", font=f)
    draw.text((text_center_x - (bbox[2]-bbox[0])//2, col_y + 15), "METHOD 1: HEURISTIC (Fast Fallback)", font=f, fill=(255, 255, 255))

    steps_h = [
        ("Step 1: Extract Keywords", "Remove stopwords, tokenize answer + context", (249, 115, 22)),
        ("Step 2: Calculate Overlap", "overlap = |answer_terms & context_terms| / |answer_terms|", (249, 115, 22)),
        ("Step 3: Score Sentences", "Flag sentences with < 15% keyword overlap as unsupported", (249, 115, 22)),
        ("Step 4: Compute Confidence", "confidence = min(1.0, overlap * 1.5) + citation_bonus", (249, 115, 22)),
        ("Step 5: Grounding Decision", "Grounded if confidence >= threshold AND unsupported <= max_ratio", (249, 115, 22)),
    ]

    sy = col_y + 75
    tf = get_font(18, bold=True)
    bf = get_font(15)
    for title, desc, color in steps_h:
        draw.ellipse([col1_x + 30, sy + 4, col1_x + 44, sy + 18], fill=color)
        draw.text((col1_x + 55, sy), title, font=tf, fill=(255, 255, 255))
        draw.text((col1_x + 55, sy + 26), desc, font=bf, fill=(148, 163, 184))
        sy += 70

    # Pros/cons
    draw.rectangle([col1_x + 20, sy + 10, col1_x + col_w - 20, sy + 11], fill=(51, 65, 85))
    draw.text((col1_x + 30, sy + 22), "+ Fast (< 10ms)  |  + No API calls  |  + Always available", font=get_font(14, bold=True), fill=(16, 185, 129))
    draw.text((col1_x + 30, sy + 46), "- Cannot understand semantic nuance or logical errors", font=get_font(14, bold=True), fill=(239, 68, 68))

    # Column 2: LLM Method
    draw_rounded_rect(draw, (col2_x, col_y, col2_x + col_w, col_y + 500), 16, (30, 41, 59))
    draw_rounded_rect(draw, (col2_x, col_y, col2_x + col_w, col_y + 55), 16, (124, 58, 237))
    draw.rectangle([col2_x, col_y + 40, col2_x + col_w, col_y + 55], fill=(124, 58, 237))
    bbox = draw.textbbox((0, 0), "METHOD 2: LLM VERIFICATION (Deep Check)", font=f)
    draw.text((col2_x + col_w//2 - (bbox[2]-bbox[0])//2, col_y + 15), "METHOD 2: LLM VERIFICATION (Deep Check)", font=f, fill=(255, 255, 255))

    steps_l = [
        ("Step 1: Split Into Claims", "Use NLP sentence splitter to extract individual claims", (124, 58, 237)),
        ("Step 2: Build Prompt", "Construct verification prompt with claims + source context", (124, 58, 237)),
        ("Step 3: LLM Evaluation", "Send to LLM (temp=0) to rate each claim independently", (124, 58, 237)),
        ("Step 4: Parse JSON Result", "Each claim rated: supported / partially / unsupported", (124, 58, 237)),
        ("Step 5: Aggregate Score", "confidence = (supported + 0.5*partial) / total + citation_bonus", (124, 58, 237)),
    ]

    sy = col_y + 75
    for title, desc, color in steps_l:
        draw.ellipse([col2_x + 30, sy + 4, col2_x + 44, sy + 18], fill=color)
        draw.text((col2_x + 55, sy), title, font=tf, fill=(255, 255, 255))
        draw.text((col2_x + 55, sy + 26), desc, font=bf, fill=(148, 163, 184))
        sy += 70

    draw.rectangle([col2_x + 20, sy + 10, col2_x + col_w - 20, sy + 11], fill=(51, 65, 85))
    draw.text((col2_x + 30, sy + 22), "+ Understands meaning  |  + Catches logical errors  |  + Per-claim detail", font=get_font(14, bold=True), fill=(16, 185, 129))
    draw.text((col2_x + 30, sy + 46), "- Requires LLM API  |  - Slower (1-3s)  |  - Must handle JSON parse errors", font=get_font(14, bold=True), fill=(239, 68, 68))

    # Bottom: How we handle failure
    bot_y = 700
    draw_rounded_rect(draw, (col1_x, bot_y, col1_x + 2*col_w + gap, bot_y + 130), 14, (30, 41, 59))
    draw.text((col1_x + 30, bot_y + 15), "CHALLENGE: Making it bulletproof", font=get_font(24, bold=True), fill=(219, 39, 119))

    challenges = [
        "LLM returns invalid JSON  ->  Catch exception, fall back to heuristic automatically",
        "API timeout or rate limit  ->  Graceful degradation, heuristic result still returned",
        "Config-driven behavior     ->  on_hallucination: 'warn' | 'refuse' | 'flag' (from config.yaml)",
        "7 test scenarios covering  ->  Mock OpenAI, malformed JSON, API errors, no-LLM fallback",
    ]
    cy = bot_y + 52
    for c in challenges:
        draw.text((col1_x + 40, cy), c, font=get_font(16), fill=(203, 213, 225))
        cy += 24

    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))
    img.save(OUT_DIR / "challenge_02_hallucination.png", quality=95)
    print("Created: challenge_02_hallucination.png")


# =============================================================================
# CHALLENGE SLIDE 3: Multi-Provider LLM
# =============================================================================
def challenge_slide_3():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    text_center(draw, "Challenge 3: Supporting Any LLM Provider", 40, get_font(40, bold=True), (255, 255, 255))
    text_center(draw, "Phase 6  |  OpenAI, Anthropic Claude, Google Gemini, Ollama (Local)", 95, get_font(20), (148, 163, 184))

    # Provider cards
    providers = [
        ("OpenAI", "GPT-3.5 / GPT-4 / GPT-4o", "chat.completions.create()", "OPENAI_API_KEY", (16, 185, 129), "Also works for Groq, Together,\nLM Studio, OpenCode via\nOPENAI_BASE_URL override"),
        ("Anthropic", "Claude Sonnet / Opus / Haiku", "client.messages.create()", "ANTHROPIC_API_KEY", (167, 139, 250), "Different API format:\nsystem param is separate,\nresponse in content[0].text"),
        ("Google Gemini", "Gemini 2.0 Flash / Pro", "model.generate_content()", "GEMINI_API_KEY", (14, 165, 233), "No system/user separation:\nprompts concatenated into\nsingle generate call"),
        ("Ollama", "Llama, Mistral, Phi (local)", "OpenAI-compatible /v1", "No key needed", (249, 115, 22), "Uses OpenAI client with\nbase_url=localhost:11434/v1\nConnectivity check on init"),
    ]

    card_w = 410
    card_h = 370
    gap = 30
    start_x = (W - 4 * card_w - 3 * gap) // 2
    card_y = 150

    tf = get_font(24, bold=True)
    mf = get_font(16, bold=True)
    bf = get_font(14)
    cf = get_font(13)

    for idx, (name, models, api_call, key, color, notes) in enumerate(providers):
        x = start_x + idx * (card_w + gap)

        draw_rounded_rect(draw, (x, card_y, x + card_w, card_y + card_h), 14, (30, 41, 59))

        # Color header
        draw_rounded_rect(draw, (x, card_y, x + card_w, card_y + 60), 14, color)
        draw.rectangle([x, card_y + 45, x + card_w, card_y + 60], fill=color)
        bbox = draw.textbbox((0, 0), name, font=tf)
        draw.text((x + (card_w - (bbox[2]-bbox[0]))//2, card_y + 16), name, font=tf, fill=(255, 255, 255))

        # Models
        draw.text((x + 20, card_y + 80), "Models:", font=mf, fill=color)
        draw.text((x + 20, card_y + 103), models, font=bf, fill=(203, 213, 225))

        # API call
        draw.text((x + 20, card_y + 140), "API Call:", font=mf, fill=color)
        draw_rounded_rect(draw, (x + 15, card_y + 163, x + card_w - 15, card_y + 190), 6, (15, 23, 42))
        draw.text((x + 25, card_y + 168), api_call, font=cf, fill=(16, 185, 129))

        # Key
        draw.text((x + 20, card_y + 205), "Auth:", font=mf, fill=color)
        draw.text((x + 20, card_y + 228), key, font=bf, fill=(203, 213, 225))

        # Notes
        draw.rectangle([x + 15, card_y + 258, x + card_w - 15, card_y + 259], fill=(51, 65, 85))
        ny = card_y + 270
        for line in notes.split("\n"):
            draw.text((x + 20, ny), line, font=cf, fill=(148, 163, 184))
            ny += 19

    # Bottom: Auto-detection flow
    bot_y = 570
    draw_rounded_rect(draw, (start_x, bot_y, start_x + 4*card_w + 3*gap, bot_y + 220), 14, (30, 41, 59))
    draw.text((start_x + 30, bot_y + 15), "AUTO-DETECTION & FALLBACK CHAIN", font=get_font(22, bold=True), fill=(219, 39, 119))

    # Flow diagram
    flow_y = bot_y + 65
    flow_steps = [
        ("Check\nLLM_PROVIDER\nenv var", (79, 70, 229)),
        ("Try configured\nprovider\nfirst", (124, 58, 237)),
        ("Fallback:\nOpenAI >>\nAnthropic", (167, 139, 250)),
        ("Fallback:\nGemini >>\nOllama", (14, 165, 233)),
        ("No provider?\nFallback mode\n(context only)", (249, 115, 22)),
    ]
    fw = 300
    fgap = 35
    fx = start_x + 40
    for idx, (label, color) in enumerate(flow_steps):
        draw_rounded_rect(draw, (fx, flow_y, fx + fw, flow_y + 90), 10, color)
        lines = label.split("\n")
        for li, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=get_font(15, bold=True))
            tw = bbox[2] - bbox[0]
            draw.text((fx + (fw-tw)//2, flow_y + 10 + li*24), line, font=get_font(15, bold=True), fill=(255, 255, 255))
        if idx < len(flow_steps) - 1:
            draw.text((fx + fw + 8, flow_y + 30), ">>", font=get_font(20, bold=True), fill=(100, 116, 139))
        fx += fw + fgap

    # Key insight
    draw.text((start_x + 40, bot_y + 175), "KEY INSIGHT:", font=get_font(16, bold=True), fill=(16, 185, 129))
    draw.text((start_x + 170, bot_y + 175), "Unified generate_answer() interface - callers never know which provider is active. Swap providers with one env var.", font=get_font(16), fill=(203, 213, 225))

    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))
    img.save(OUT_DIR / "challenge_03_multi_llm.png", quality=95)
    print("Created: challenge_03_multi_llm.png")


# =============================================================================
# CHALLENGE SLIDE 4: Testing & Deployment
# =============================================================================
def challenge_slide_4():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    text_center(draw, "Challenge 4: Testing, Quality & Deployment", 40, get_font(40, bold=True), (255, 255, 255))
    text_center(draw, "91 Tests  |  Pre-commit Hooks  |  Docker  |  DigitalOcean Cloud", 95, get_font(20), (148, 163, 184))

    # Three columns
    col_w = 560
    col_gap = 30
    col_x = (W - 3 * col_w - 2 * col_gap) // 2
    col_y = 155

    # Column 1: Testing
    draw_rounded_rect(draw, (col_x, col_y, col_x + col_w, col_y + 550), 16, (30, 41, 59))
    draw_rounded_rect(draw, (col_x, col_y, col_x + col_w, col_y + 55), 16, (79, 70, 229))
    draw.rectangle([col_x, col_y + 40, col_x + col_w, col_y + 55], fill=(79, 70, 229))
    bbox = draw.textbbox((0, 0), "TESTING (91 Tests)", font=get_font(20, bold=True))
    draw.text((col_x + (col_w-(bbox[2]-bbox[0]))//2, col_y + 15), "TESTING (91 Tests)", font=get_font(20, bold=True), fill=(255, 255, 255))

    test_items = [
        ("Unit Tests: 73", "Every component tested in isolation", (79, 70, 229)),
        ("Integration Tests: 18", "Full API flow: upload > query > delete", (124, 58, 237)),
        ("Mocked External APIs", "OpenAI calls mocked for offline testing", (167, 139, 250)),
        ("Test Isolation", "tmp_path fixtures, no test affects another", (14, 165, 233)),
        ("Coverage Tracking", "pytest-cov with src/ source mapping", (16, 185, 129)),
    ]
    ty = col_y + 75
    for title, desc, color in test_items:
        draw.ellipse([col_x + 25, ty + 4, col_x + 39, ty + 18], fill=color)
        draw.text((col_x + 50, ty), title, font=get_font(17, bold=True), fill=(255, 255, 255))
        draw.text((col_x + 50, ty + 25), desc, font=get_font(14), fill=(148, 163, 184))
        ty += 60

    # Test pyramid
    py_y = ty + 20
    draw.text((col_x + 30, py_y), "Test Pyramid:", font=get_font(16, bold=True), fill=(167, 139, 250))
    levels = [("E2E (API)", 180, (219, 39, 119)), ("Integration (18)", 280, (124, 58, 237)), ("Unit (73)", 400, (79, 70, 229))]
    for label, w, color in levels:
        py_y += 35
        bx = col_x + (col_w - w) // 2
        draw_rounded_rect(draw, (bx, py_y, bx + w, py_y + 28), 6, color)
        bbox = draw.textbbox((0, 0), label, font=get_font(13, bold=True))
        draw.text((bx + (w-(bbox[2]-bbox[0]))//2, py_y + 6), label, font=get_font(13, bold=True), fill=(255, 255, 255))

    # Column 2: Code Quality
    col2_x = col_x + col_w + col_gap
    draw_rounded_rect(draw, (col2_x, col_y, col2_x + col_w, col_y + 550), 16, (30, 41, 59))
    draw_rounded_rect(draw, (col2_x, col_y, col2_x + col_w, col_y + 55), 16, (249, 115, 22))
    draw.rectangle([col2_x, col_y + 40, col2_x + col_w, col_y + 55], fill=(249, 115, 22))
    bbox = draw.textbbox((0, 0), "CODE QUALITY", font=get_font(20, bold=True))
    draw.text((col2_x + (col_w-(bbox[2]-bbox[0]))//2, col_y + 15), "CODE QUALITY", font=get_font(20, bold=True), fill=(255, 255, 255))

    quality_items = [
        ("Black", "Automatic code formatting\n100 char line length", (249, 115, 22)),
        ("isort", "Import ordering\nConsistent import groups", (234, 179, 8)),
        ("flake8", "Linting for style violations\nE203, W503 ignored", (239, 68, 68)),
        ("mypy", "Static type checking\nType hints throughout", (124, 58, 237)),
        ("pre-commit", "Hooks run on every commit\nBlack + isort + flake8", (16, 185, 129)),
        ("Pydantic v2", "Runtime data validation\nAll API models validated", (14, 165, 233)),
    ]
    qy = col_y + 75
    for title, desc, color in quality_items:
        draw_rounded_rect(draw, (col2_x + 20, qy, col2_x + col_w - 20, qy + 70), 8, (22, 33, 49))
        draw.text((col2_x + 35, qy + 8), title, font=get_font(17, bold=True), fill=color)
        lines = desc.split("\n")
        for li, line in enumerate(lines):
            draw.text((col2_x + 35, qy + 32 + li*18), line, font=get_font(13), fill=(148, 163, 184))
        qy += 80

    # Column 3: Deployment
    col3_x = col2_x + col_w + col_gap
    draw_rounded_rect(draw, (col3_x, col_y, col3_x + col_w, col_y + 550), 16, (30, 41, 59))
    draw_rounded_rect(draw, (col3_x, col_y, col3_x + col_w, col_y + 55), 16, (16, 185, 129))
    draw.rectangle([col3_x, col_y + 40, col3_x + col_w, col_y + 55], fill=(16, 185, 129))
    bbox = draw.textbbox((0, 0), "DEPLOYMENT", font=get_font(20, bold=True))
    draw.text((col3_x + (col_w-(bbox[2]-bbox[0]))//2, col_y + 15), "DEPLOYMENT", font=get_font(20, bold=True), fill=(255, 255, 255))

    deploy_items = [
        ("Docker", "Single image, two containers\nAPI (port 8000) + Frontend (port 80)", (16, 185, 129)),
        ("docker-compose", "Named volumes for persistence\nHealth checks, auto-restart", (14, 165, 233)),
        ("DigitalOcean", "2GB droplet ($12/mo)\nBangalore region, 24/7 uptime", (79, 70, 229)),
        ("One-Command Setup", "curl setup_server.sh | bash\nInstalls Docker, clones, deploys", (124, 58, 237)),
        ("Hot-Patching", "docker cp + restart for\ncode-only changes (no rebuild)", (249, 115, 22)),
        ("Rate Limiter", "60 req/min per IP\nSliding window middleware", (239, 68, 68)),
    ]
    dy = col_y + 75
    for title, desc, color in deploy_items:
        draw_rounded_rect(draw, (col3_x + 20, dy, col3_x + col_w - 20, dy + 70), 8, (22, 33, 49))
        draw.text((col3_x + 35, dy + 8), title, font=get_font(17, bold=True), fill=color)
        lines = desc.split("\n")
        for li, line in enumerate(lines):
            draw.text((col3_x + 35, dy + 32 + li*18), line, font=get_font(13), fill=(148, 163, 184))
        dy += 80

    # Bottom stats bar
    text_center(draw, "6,000+ Lines of Python  |  80 Files  |  14 API Endpoints  |  5 Themes  |  4 LLM Providers", H - 55, get_font(18, bold=True), (100, 116, 139))

    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))
    img.save(OUT_DIR / "challenge_04_testing_deploy.png", quality=95)
    print("Created: challenge_04_testing_deploy.png")


if __name__ == "__main__":
    challenge_slide_1()
    challenge_slide_2()
    challenge_slide_3()
    challenge_slide_4()
    print(f"\nAll 4 challenge slides saved to: {OUT_DIR}")
