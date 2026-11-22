"""The progress map: one cell per exercise, a row per module, in the style of the exam map in Joel's episodes.
Passed cells are lit amber, the current one is outlined, the rest are still to come; the counter says how many
are passed. The last row, MCP server, is the worked example in examples/mcp-server/, not an exercise: its one
cell is lit when progress.json's "examples" marks "mcp-server" done. Reads progress.json and exercises/, writes lessons/progress.svg and lessons/progress.md (gitignored),
which VS Code opens in its Markdown preview.

    python3 .claude/skills/progress/progress_map.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODULES = [
    ("Syntax and data", 1, 7), ("Types", 8, 11), ("Packages and files", 12, 16), ("Testing", 17, 20),
    ("NumPy and vectors", 21, 24), ("Async and a model", 25, 29), ("The pipeline", 30, 39),
    ("The eval harness", 40, 46), ("FastAPI service", 47, 49), ("Capstone", 50, 50),
]
AMBER, NAVY, EDGE, INK, MUTED, BG = "#f59e0b", "#242e48", "#465478", "#eef2ff", "#94a3b8", "#14171f"
CELL, GAP, LEFT, TOP, ROW = 44, 8, 200, 120, 58


def main():
    progress = json.loads((ROOT / "progress.json").read_text()) if (ROOT / "progress.json").exists() else {}
    done = {k for k, v in progress.get("exercises", {}).items() if v.get("status") == "passed"}
    current = progress.get("current")
    slugs = {int(p.name[:2]): p.name for p in (ROOT / "exercises").iterdir() if p.is_dir() and p.name[:2].isdigit()}
    total = len(slugs)
    width = LEFT + 10 * (CELL + GAP) + 40
    height = TOP + (len(MODULES) + 1) * ROW + 70
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
           f'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">',
           f'<rect width="100%" height="100%" rx="14" fill="{BG}"/>',
           f'<text x="32" y="56" font-size="26" font-weight="700" fill="{INK}">Your path to a RAG pipeline</text>',
           f'<text x="{width - 32}" y="52" font-size="30" font-weight="700" fill="{AMBER}" text-anchor="end">'
           f'{len(done)} of {total} exercises</text>']
    current_name = ""
    for row, (name, first, last) in enumerate(MODULES):
        y = TOP + row * ROW
        nums = [n for n in range(first, last + 1) if n in slugs]
        passed = sum(slugs[n] in done for n in nums)
        here = any(slugs[n] == current for n in nums)
        if here:
            current_name = name
        out.append(f'<text x="{LEFT - 16}" y="{y + CELL / 2 + 6}" font-size="15" text-anchor="end" '
                   f'fill="{INK if here else MUTED}" font-weight="{600 if here else 400}">{name}</text>')
        for i, n in enumerate(nums):
            x = LEFT + i * (CELL + GAP)
            slug = slugs[n]
            if slug in done:
                fill, stroke, sw, label = AMBER, AMBER, 1.5, "#1a1205"
            elif slug == current:
                fill, stroke, sw, label = NAVY, AMBER, 3.5, INK
            else:
                fill, stroke, sw, label = NAVY, EDGE, 1.5, MUTED
            out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="8" fill="{fill}" stroke="{stroke}" '
                       f'stroke-width="{sw}"><title>{slug}</title></rect>')
            out.append(f'<text x="{x + CELL / 2}" y="{y + CELL / 2 + 5}" font-size="13" text-anchor="middle" '
                       f'fill="{label}">{n:02d}</text>')
        if passed == len(nums):
            out.append(f'<text x="{LEFT + len(nums) * (CELL + GAP) + 4}" y="{y + CELL / 2 + 6}" font-size="18" '
                       f'fill="{AMBER}">✓</text>')
    y = TOP + len(MODULES) * ROW
    mcp_done = progress.get("examples", {}).get("mcp-server") == "done"
    mcp_here = current == "mcp-server"
    out.append(f'<text x="{LEFT - 16}" y="{y + CELL / 2 + 6}" font-size="15" text-anchor="end" '
               f'fill="{INK if mcp_here else MUTED}" font-weight="{600 if mcp_here else 400}">MCP server</text>')
    fill, stroke, sw, label = ((AMBER, AMBER, 1.5, "#1a1205") if mcp_done else (NAVY, AMBER, 3.5, INK) if mcp_here
                               else (NAVY, EDGE, 1.5, MUTED))
    out.append(f'<rect x="{LEFT}" y="{y}" width="{CELL * 2 + GAP}" height="{CELL}" rx="8" fill="{fill}" stroke="{stroke}" '
               f'stroke-width="{sw}" stroke-dasharray="{"" if mcp_done or mcp_here else "5 4"}"><title>examples/mcp-server</title></rect>')
    out.append(f'<text x="{LEFT + CELL + GAP / 2}" y="{y + CELL / 2 + 5}" font-size="13" text-anchor="middle" fill="{label}">MCP</text>')
    out.append(f'<text x="{LEFT + 2 * (CELL + GAP) + 6}" y="{y + CELL / 2 + 5}" font-size="13" fill="{MUTED}">worked example, after the capstone</text>')
    if mcp_here:
        current_name = "MCP server"
    sub = f"Now: {current} · {current_name}" if current and current not in done else "Type /teach-me"
    out.append(f'<text x="{width - 32}" y="84" font-size="16" fill="{MUTED}" text-anchor="end">{sub}</text>')
    ly = height - 34
    for k, (fill, stroke, sw, text) in enumerate([(AMBER, AMBER, 1.5, "Passed"), (NAVY, AMBER, 3.5, "Current"),
                                                   (NAVY, EDGE, 1.5, "Still to come")]):
        x = LEFT + k * 170
        out.append(f'<rect x="{x}" y="{ly - 16}" width="26" height="22" rx="5" fill="{fill}" stroke="{stroke}" '
                   f'stroke-width="{sw}"/><text x="{x + 36}" y="{ly}" font-size="15" fill="{MUTED}">{text}</text>')
    out.append("</svg>")
    lessons = ROOT / "lessons"
    lessons.mkdir(exist_ok=True)
    (lessons / "progress.svg").write_text("\n".join(out))
    review = progress.get("review", [])
    lines = ["# Progress", "", "![Your progress map](progress.svg)", ""]
    if review:
        lines += [f"**To review:** {', '.join(review)}", ""]
    lines += ["Type `/teach-me` for the next exercise, taught from a worked example, and `/check` to have it graded."]
    (lessons / "progress.md").write_text("\n".join(lines) + "\n")
    print(f"{len(done)} of {total} passed; current {current}")


if __name__ == "__main__":
    main()
