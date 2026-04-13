"""Generate slides for Scene 10 (Testing), Scene 11 (Deployment & Closing)."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).parent.parent / "docs" / "slides"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080


def get_font(size, bold=False):
    names_bold = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/calibrib.ttf"]
    names_reg = ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"]
    for n in (names_bold if bold else names_reg):
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


# =============================================================================
# SLIDE 6: TESTING & QUALITY (Scene 10)
# =============================================================================
def slide_testing():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    text_center(draw, "Testing & Code Quality", 40, get_font(44, bold=True), (255, 255, 255))
    text_center(draw, '"Quality was non-negotiable"', 100, get_font(22), (167, 139, 250))

    # Big stat cards row
    stats = [
        ("91", "Total Tests", "Automated test suite", (79, 70, 229)),
        ("73", "Unit Tests", "Individual components", (124, 58, 237)),
        ("18", "Integration Tests", "Full API flows", (219, 39, 119)),
        ("100%", "Pass Rate", "All tests green", (16, 185, 129)),
    ]
    card_w = 380
    gap = 40
    start_x = (W - len(stats) * card_w - (len(stats)-1) * gap) // 2
    card_y = 165

    for idx, (val, label, sub, color) in enumerate(stats):
        x = start_x + idx * (card_w + gap)
        draw_rounded_rect(draw, (x, card_y, x + card_w, card_y + 160), 16, (30, 41, 59))
        draw.rectangle([x + 16, card_y, x + card_w - 16, card_y + 5], fill=color)
        draw.text((x + 30, card_y + 25), val, font=get_font(56, bold=True), fill=color)
        draw.text((x + 30, card_y + 95), label, font=get_font(22, bold=True), fill=(255, 255, 255))
        draw.text((x + 30, card_y + 125), sub, font=get_font(15), fill=(148, 163, 184))

    # What we test - grid
    wy = 370
    text_center(draw, "What We Test", wy, get_font(26, bold=True), (255, 255, 255))

    test_areas = [
        ("Text Chunker", "Token boundaries, overlap,\nmin chunk merging", "test_text_chunker.py"),
        ("Embedding Service", "Dimension consistency,\nbatch processing, cosine sim", "test_embedding_service.py"),
        ("ChromaDB Store", "Add, search, delete, persist,\nreload from disk", "test_chroma_store.py"),
        ("FAISS Store", "Add, search, rebuild-on-delete,\npersistence", "test_faiss_store.py"),
        ("BM25 Search", "Indexing, keyword scoring,\ndocument filtering", "test_bm25_search.py"),
        ("Reranker", "Score combination, top-k\ntruncation, order change", "test_reranker.py"),
        ("Hallucination Detector", "Heuristic vs LLM, config\nthresholds, JSON fallback", "test_hallucination_*.py"),
        ("Citation Manager", "Registration, formatting,\nmarker validation", "test_citation_manager.py"),
        ("Bloom's Taxonomy", "Level detection, practice\nquestion generation", "test_blooms_taxonomy.py"),
        ("Document Service", "Process, list, delete,\nkeyword search", "test_document_service.py"),
        ("Full API Flow", "Upload > Query > Citations\n> Delete (end-to-end)", "test_api.py + test_e2e.py"),
        ("Rate Limiter", "Under limit, over limit,\nRetry-After header", "test_rate_limiter.py"),
    ]

    tw = 400
    th = 130
    tgap_x = 30
    tgap_y = 18
    cols = 4
    tx_start = (W - cols * tw - (cols-1) * tgap_x) // 2
    ty_start = wy + 45

    tf = get_font(16, bold=True)
    bf = get_font(13)
    cf = get_font(11)

    for idx, (title, desc, filename) in enumerate(test_areas):
        col = idx % cols
        row = idx // cols
        x = tx_start + col * (tw + tgap_x)
        y = ty_start + row * (th + tgap_y)

        draw_rounded_rect(draw, (x, y, x + tw, y + th), 10, (30, 41, 59))
        draw.text((x + 15, y + 12), title, font=tf, fill=(255, 255, 255))

        lines = desc.split("\n")
        for li, line in enumerate(lines):
            draw.text((x + 15, y + 38 + li * 18), line, font=bf, fill=(148, 163, 184))

        # Filename badge
        draw_rounded_rect(draw, (x + 15, y + th - 30, x + tw - 15, y + th - 8), 5, (22, 33, 49))
        draw.text((x + 25, y + th - 27), filename, font=cf, fill=(100, 116, 139))

    # Tools bar at bottom
    tools_y = H - 100
    draw_rounded_rect(draw, (80, tools_y, W - 80, tools_y + 55), 12, (30, 41, 59))

    tools = [
        ("pytest", (79, 70, 229)),
        ("pytest-asyncio", (124, 58, 237)),
        ("pytest-cov", (167, 139, 250)),
        ("httpx", (14, 165, 233)),
        ("Black", (249, 115, 22)),
        ("isort", (234, 179, 8)),
        ("flake8", (239, 68, 68)),
        ("mypy", (219, 39, 119)),
        ("pre-commit", (16, 185, 129)),
        ("Pydantic v2", (124, 58, 237)),
    ]
    tool_x = 110
    for name, color in tools:
        bbox = draw.textbbox((0, 0), name, font=get_font(15, bold=True))
        bw = bbox[2] - bbox[0] + 24
        draw_rounded_rect(draw, (tool_x, tools_y + 12, tool_x + bw, tools_y + 42), 8, color)
        draw.text((tool_x + 12, tools_y + 17), name, font=get_font(15, bold=True), fill=(255, 255, 255))
        tool_x += bw + 14

    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))
    img.save(OUT_DIR / "slide_06_testing.png", quality=95)
    print("Created: slide_06_testing.png")


# =============================================================================
# SLIDE 7: DEPLOYMENT (Scene 11 - first half)
# =============================================================================
def slide_deployment():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    text_center(draw, "Deployment Architecture", 40, get_font(44, bold=True), (255, 255, 255))
    text_center(draw, "Docker + DigitalOcean Cloud  |  Accessible from Anywhere", 100, get_font(20), (148, 163, 184))

    # Docker architecture diagram
    diag_y = 165

    # DigitalOcean droplet box
    draw_rounded_rect(draw, (120, diag_y, W - 120, diag_y + 520), 20, (22, 33, 49))
    draw.text((160, diag_y + 18), "DigitalOcean Droplet  |  Ubuntu 24.04  |  2GB RAM  |  Bangalore", font=get_font(18, bold=True), fill=(14, 165, 233))

    # Docker box inside
    docker_y = diag_y + 55
    draw_rounded_rect(draw, (160, docker_y, W - 160, docker_y + 440), 16, (30, 41, 59))
    draw.text((200, docker_y + 15), "Docker Compose", font=get_font(18, bold=True), fill=(16, 185, 129))

    # API container
    api_x, api_y = 210, docker_y + 55
    api_w, api_h = 720, 360
    draw_rounded_rect(draw, (api_x, api_y, api_x + api_w, api_y + api_h), 14, (22, 33, 49))
    draw_rounded_rect(draw, (api_x, api_y, api_x + api_w, api_y + 50), 14, (79, 70, 229))
    draw.rectangle([api_x, api_y + 35, api_x + api_w, api_y + 50], fill=(79, 70, 229))
    text_center_x = api_x + api_w // 2
    bbox = draw.textbbox((0, 0), "safes-api  (Port 8000)", font=get_font(20, bold=True))
    draw.text((text_center_x - (bbox[2]-bbox[0])//2, api_y + 13), "safes-api  (Port 8000)", font=get_font(20, bold=True), fill=(255, 255, 255))

    api_items = [
        "FastAPI Application Server",
        "uvicorn ASGI (async)",
        "RAG Engine + LLM Service",
        "Hallucination Detector",
        "Embedding + Retrieval Service",
        "Document Processors",
        "Rate Limiter Middleware",
        "Health Check Endpoint",
    ]
    ay = api_y + 70
    for item in api_items:
        draw.text((api_x + 30, ay), "-  " + item, font=get_font(16), fill=(203, 213, 225))
        ay += 30

    # Volumes
    vol_y = api_y + api_h - 80
    draw_rounded_rect(draw, (api_x + 20, vol_y, api_x + 230, vol_y + 30), 6, (16, 185, 129))
    draw.text((api_x + 32, vol_y + 5), "safes_data volume", font=get_font(13, bold=True), fill=(255, 255, 255))
    draw_rounded_rect(draw, (api_x + 250, vol_y, api_x + 450, vol_y + 30), 6, (14, 165, 233))
    draw.text((api_x + 262, vol_y + 5), "safes_logs volume", font=get_font(13, bold=True), fill=(255, 255, 255))

    # Arrow between containers
    arrow_x = api_x + api_w + 20
    arrow_y = api_y + api_h // 2
    draw.text((arrow_x, arrow_y - 20), "depends_on", font=get_font(13), fill=(100, 116, 139))
    draw.text((arrow_x + 10, arrow_y + 2), "<---", font=get_font(20, bold=True), fill=(100, 116, 139))
    draw.text((arrow_x, arrow_y + 25), "health check", font=get_font(13), fill=(100, 116, 139))

    # Frontend container
    fe_x = arrow_x + 100
    fe_w = 520
    fe_h = api_h
    draw_rounded_rect(draw, (fe_x, api_y, fe_x + fe_w, api_y + fe_h), 14, (22, 33, 49))
    draw_rounded_rect(draw, (fe_x, api_y, fe_x + fe_w, api_y + 50), 14, (219, 39, 119))
    draw.rectangle([fe_x, api_y + 35, fe_x + fe_w, api_y + 50], fill=(219, 39, 119))
    bbox = draw.textbbox((0, 0), "safes-frontend  (Port 80)", font=get_font(20, bold=True))
    draw.text((fe_x + (fe_w-(bbox[2]-bbox[0]))//2, api_y + 13), "safes-frontend  (Port 80)", font=get_font(20, bold=True), fill=(255, 255, 255))

    fe_items = [
        "Streamlit Application",
        "5 Interactive Tabs",
        "5 Switchable Themes",
        "Document Upload UI",
        "Query + Analytics",
        "Headless mode",
        "API_URL = http://api:8000",
    ]
    fy = api_y + 70
    for item in fe_items:
        draw.text((fe_x + 30, fy), "-  " + item, font=get_font(16), fill=(203, 213, 225))
        fy += 30

    # Internet users
    user_y = diag_y + 540
    draw_rounded_rect(draw, (300, user_y + 20, W - 300, user_y + 90), 14, (30, 41, 59))

    users_text = "Students / Classmates / Anyone with the URL"
    bbox = draw.textbbox((0, 0), users_text, font=get_font(20, bold=True))
    draw.text(((W-(bbox[2]-bbox[0]))//2, user_y + 35), users_text, font=get_font(20, bold=True), fill=(167, 139, 250))

    draw.text((W//2 - 40, user_y - 5), "| | |", font=get_font(18), fill=(100, 116, 139))
    draw.text((W//2 - 20, user_y + 75), "V", font=get_font(18), fill=(100, 116, 139))

    # URL
    url_y = user_y + 95
    draw_rounded_rect(draw, (550, url_y, W - 550, url_y + 45), 10, (79, 70, 229))
    bbox = draw.textbbox((0, 0), "http://139.59.44.122", font=get_font(22, bold=True))
    draw.text(((W-(bbox[2]-bbox[0]))//2, url_y + 10), "http://139.59.44.122", font=get_font(22, bold=True), fill=(255, 255, 255))

    # Bottom stats
    stats_text = "Always On  |  $12/mo ($300 credit = 25 months)  |  Auto-restart  |  Hot-patchable"
    text_center(draw, stats_text, H - 55, get_font(18, bold=True), (100, 116, 139))

    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))
    img.save(OUT_DIR / "slide_07_deployment.png", quality=95)
    print("Created: slide_07_deployment.png")


# =============================================================================
# SLIDE 8: PROJECT SUMMARY (Scene 11 - second half)
# =============================================================================
def slide_summary():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, 0, 0, W, 6, (79, 70, 229), (219, 39, 119))

    text_center(draw, "What SAFES Delivers", 40, get_font(44, bold=True), (255, 255, 255))

    # Checkmark items - the summary points
    items = [
        ("Grounded Answers", "Every response generated ONLY from uploaded study materials", (79, 70, 229)),
        ("Verifiable Citations", "Document name, page number, section title with every claim", (124, 58, 237)),
        ("Hallucination Detection", "Heuristic + LLM-based verification with confidence scoring", (219, 39, 119)),
        ("Bloom's Taxonomy", "Adaptive responses across 6 cognitive levels (Remember to Create)", (167, 139, 250)),
        ("Study Tools", "Guides, practice tests, topic comparison, key concept extraction", (14, 165, 233)),
        ("Multi-Provider LLM", "Works with OpenAI, Anthropic, Gemini, Ollama, or any compatible API", (16, 185, 129)),
        ("Beautiful UI", "5 switchable themes, interactive analytics, query history tracking", (249, 115, 22)),
    ]

    item_h = 80
    gap = 12
    start_y = 120
    item_w = 1400
    ix = (W - item_w) // 2

    for idx, (title, desc, color) in enumerate(items):
        y = start_y + idx * (item_h + gap)
        draw_rounded_rect(draw, (ix, y, ix + item_w, y + item_h), 14, (30, 41, 59))

        # Checkmark circle
        draw_rounded_rect(draw, (ix + 20, y + 20, ix + 60, y + 60), 20, color)
        draw.text((ix + 31, y + 25), "V", font=get_font(22, bold=True), fill=(255, 255, 255))

        # Title + desc
        draw.text((ix + 80, y + 15), title, font=get_font(22, bold=True), fill=(255, 255, 255))
        draw.text((ix + 80, y + 47), desc, font=get_font(17), fill=(148, 163, 184))

        # Number badge on right
        draw_rounded_rect(draw, (ix + item_w - 65, y + 25, ix + item_w - 20, y + 55), 8, color)
        num = str(idx + 1)
        bbox = draw.textbbox((0, 0), num, font=get_font(18, bold=True))
        draw.text((ix + item_w - 52 + (20-(bbox[2]-bbox[0]))//2, y + 31), num, font=get_font(18, bold=True), fill=(255, 255, 255))

    # Bottom stats row
    stats_y = H - 130
    project_stats = [
        ("~9,000", "Total Lines", (79, 70, 229)),
        ("80", "Python Files", (124, 58, 237)),
        ("91", "Automated Tests", (219, 39, 119)),
        ("14", "API Endpoints", (14, 165, 233)),
        ("5", "UI Themes", (249, 115, 22)),
        ("4", "LLM Providers", (16, 185, 129)),
    ]
    sw = 250
    sgap = 28
    sx = (W - len(project_stats) * sw - (len(project_stats)-1) * sgap) // 2
    for idx, (val, label, color) in enumerate(project_stats):
        x = sx + idx * (sw + sgap)
        draw_rounded_rect(draw, (x, stats_y, x + sw, stats_y + 75), 10, (30, 41, 59))
        draw.text((x + 20, stats_y + 8), val, font=get_font(30, bold=True), fill=color)
        draw.text((x + 20, stats_y + 48), label, font=get_font(14, bold=True), fill=(148, 163, 184))

    draw_gradient(draw, 0, H - 6, W, 6, (79, 70, 229), (219, 39, 119))
    img.save(OUT_DIR / "slide_08_summary.png", quality=95)
    print("Created: slide_08_summary.png")


# =============================================================================
# SLIDE 9: CLOSING / THANK YOU (Final screen)
# =============================================================================
def slide_closing():
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Full gradient background
    draw_gradient(draw, 0, 0, W, H, (79, 70, 229), (219, 39, 119), "horizontal")

    # Darken slightly for readability
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 100))
    img.paste(Image.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), overlay).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img)

    # Big SAFES title
    text_center(draw, "SAFES", 200, get_font(120, bold=True), (255, 255, 255))

    # Subtitle
    text_center(draw, "Source-Aware Framework for Exam Support", 340, get_font(32), (255, 255, 255))

    # Tagline
    draw.rectangle([(W//2 - 400, 420), (W//2 + 400, 421)], fill=(255, 255, 255, 100))

    text_center(draw, '"Because the answer to your exam question', 450, get_font(26), (255, 255, 255))
    text_center(draw, 'should come from your textbook, not from the internet."', 488, get_font(26), (255, 255, 255))

    # Tech badges
    badges = ["FastAPI", "Streamlit", "RAG", "ChromaDB", "GLM-5", "Python"]
    bx = (W - len(badges) * 160 - (len(badges)-1) * 15) // 2
    by = 570
    for badge in badges:
        bw = 150
        draw_rounded_rect(draw, (bx, by, bx + bw, by + 38), 10, (255, 255, 255, 40))
        draw.rectangle([bx + 10, by, bx + bw - 10, by + 38], fill=(255, 255, 255, 30))
        bbox = draw.textbbox((0, 0), badge, font=get_font(16, bold=True))
        draw.text((bx + (bw-(bbox[2]-bbox[0]))//2, by + 9), badge, font=get_font(16, bold=True), fill=(255, 255, 255))
        bx += bw + 15

    # URL
    text_center(draw, "http://139.59.44.122", 660, get_font(28, bold=True), (255, 255, 255))

    # GitHub
    text_center(draw, "github.com/ShreyanshVaibhaw/SAFES-Source-Aware-Framework-for-Exam-Support-", 710, get_font(16), (255, 255, 255))

    # Contributors
    text_center(draw, "Built by", 790, get_font(18), (255, 255, 255))
    text_center(draw, "Shreyansh Vaibhaw  &  Harshit Kumar", 820, get_font(26, bold=True), (255, 255, 255))

    # Thank you
    text_center(draw, "Thank You", 910, get_font(50, bold=True), (255, 255, 255))

    img.save(OUT_DIR / "slide_09_closing.png", quality=95)
    print("Created: slide_09_closing.png")


if __name__ == "__main__":
    slide_testing()
    slide_deployment()
    slide_summary()
    slide_closing()
    print(f"\nAll 4 closing slides saved to: {OUT_DIR}")
