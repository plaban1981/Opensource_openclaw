"""
Generate architecture diagram for MyOpenClaw agent.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ── Canvas ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(20, 15))
W, H = 20, 15
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_facecolor("#0d1117")
fig.patch.set_facecolor("#0d1117")
ax.axis("off")

# ── Palette ───────────────────────────────────────────────────────────────────
C = {
    "entry":    "#2ea043",   # green
    "crew":     "#1f6feb",   # blue
    "agent":    "#8957e5",   # purple
    "task":     "#d29922",   # amber
    "tool":     "#0e9aef",   # cyan
    "llm":      "#da3633",   # red
    "external": "#484f58",   # grey
    "line":     "#8b949e",
    "white":    "#e6edf3",
    "dim":      "#8b949e",
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def box(x, y, w, h, title, subtitle=None, color="#1f6feb", fs=9.5):
    pad = 0.12
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={pad}",
        facecolor=color + "cc",
        edgecolor=color,
        linewidth=2,
        zorder=3,
    )
    ax.add_patch(rect)
    cy = y + h / 2
    if subtitle:
        ax.text(x + w / 2, cy + h * 0.14, title,
                ha="center", va="center", color=C["white"],
                fontsize=fs, fontweight="bold", zorder=4)
        ax.text(x + w / 2, cy - h * 0.2, subtitle,
                ha="center", va="center", color=C["dim"],
                fontsize=fs - 1.5, style="italic", zorder=4)
    else:
        ax.text(x + w / 2, cy, title,
                ha="center", va="center", color=C["white"],
                fontsize=fs, fontweight="bold", zorder=4)


def arrow(x1, y1, x2, y2, color="#8b949e", style="->", lw=1.5, ls="solid"):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle=style, color=color,
                        lw=lw, linestyle=ls),
        zorder=2,
    )


def section_label(x, y, text):
    ax.text(x, y, text, color=C["dim"], fontsize=8,
            fontstyle="italic", ha="left", va="center", zorder=5)


# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(W / 2, 14.55, "MyOpenClaw — Agent Architecture",
        ha="center", va="center", color=C["white"],
        fontsize=17, fontweight="bold", zorder=5)
ax.text(W / 2, 14.15, "CrewAI  ·  Ollama (minimax-m2.5)  ·  Local LLM  ·  Python",
        ha="center", va="center", color=C["dim"], fontsize=10, zorder=5)

# horizontal rule
ax.plot([0.5, 19.5], [13.9, 13.9], color=C["line"], lw=0.8, zorder=2)

# ── Layer 1 — Entry Point ─────────────────────────────────────────────────────
section_label(0.3, 13.4, "ENTRY")
box(7.0, 12.9, 6.0, 0.85, "main()", 'task = "Create a REST API with Flask"',
    color=C["entry"], fs=10)
arrow(10, 12.9, 10, 12.45)

# ── Layer 2 — Crew Factory ────────────────────────────────────────────────────
section_label(0.3, 12.1, "FACTORY")
box(5.0, 11.6, 10.0, 0.75,
    "Crew Factory",
    "create_simple_crew()   |   create_crew()",
    color=C["crew"], fs=10)

# branch arrows
arrow(7.5, 11.6, 4.25, 10.95, color=C["crew"])
arrow(12.5, 11.6, 15.75, 10.95, color=C["crew"])

# ── Layer 3 — Crew Modes ──────────────────────────────────────────────────────
section_label(0.3, 10.7, "CREWS")
box(0.5, 10.3, 7.0, 0.75,
    "Simple Crew",
    "Process.sequential  ·  2 agents",
    color=C["crew"], fs=9.5)
box(12.5, 10.3, 7.0, 0.75,
    "Full Crew",
    "Process.hierarchical  ·  memory=True  ·  4 agents",
    color=C["crew"], fs=9.5)

# converge arrows to agents
arrow(4.0, 10.3, 4.5, 9.6, color=C["crew"])
arrow(4.0, 10.3, 8.5, 9.6, color=C["crew"])
arrow(16.0, 10.3, 2.5, 9.6, color=C["crew"], ls="dashed")
arrow(16.0, 10.3, 5.5, 9.6, color=C["crew"], ls="dashed")
arrow(16.0, 10.3, 12.5, 9.6, color=C["crew"], ls="dashed")
arrow(16.0, 10.3, 16.5, 9.6, color=C["crew"], ls="dashed")

# ── Layer 4 — Agents ─────────────────────────────────────────────────────────
section_label(0.3, 9.15, "AGENTS")
AGENT_DATA = [
    (0.5,  "Researcher\nAgent",  "Senior Research\nAnalyst"),
    (5.0,  "Coder\nAgent",       "Senior Software\nEngineer"),
    (9.5,  "Reviewer\nAgent",    "Code Reviewer"),
    (14.0, "Executor\nAgent",    "DevOps Engineer"),
]
AGENT_W = 4.2
AGENT_H = 0.95
AGENT_CXS = []
for ax_pos, title, sub in AGENT_DATA:
    box(ax_pos, 8.4, AGENT_W, AGENT_H, title, sub, color=C["agent"], fs=9)
    cx = ax_pos + AGENT_W / 2
    AGENT_CXS.append(cx)
    arrow(cx, 8.4, cx, 7.7, color=C["agent"])

# LLM dashed lines (agents ↔ LLM)
for cx in AGENT_CXS:
    arrow(cx, 8.4, 10, 7.25, color=C["llm"], ls="dashed", lw=1.2)

# ── Layer 5 — LLM ─────────────────────────────────────────────────────────────
section_label(0.3, 7.45, "LLM")
box(5.5, 6.9, 9.0, 0.75,
    "Ollama  ·  minimax-m2.5:cloud",
    "http://localhost:11434  ·  temperature=0.7  ·  fully local",
    color=C["llm"], fs=9.5)

# ── Layer 6 — Tasks ───────────────────────────────────────────────────────────
section_label(0.3, 6.4, "TASKS")
TASK_DATA = [
    (0.5,  "Research\nTask",   "→ Researcher"),
    (5.0,  "Coding\nTask",     "→ Coder"),
    (9.5,  "Review\nTask",     "→ Reviewer"),
    (14.0, "Execution\nTask",  "→ Executor"),
]
TASK_H = 0.85
for i, (ax_pos, title, sub) in enumerate(TASK_DATA):
    box(ax_pos, 5.55, AGENT_W, TASK_H, title, sub, color=C["task"], fs=9)
    cx = AGENT_CXS[i]
    arrow(cx, 5.55, cx, 5.0, color=C["task"])

# agent → task arrows (vertical, already from agent base)
# tasks → tools
for i, (ax_pos, _, _) in enumerate(TASK_DATA):
    cx = ax_pos + AGENT_W / 2
    arrow(cx, 5.55, cx, 5.0, color=C["task"])

# ── Layer 7 — Tools ───────────────────────────────────────────────────────────
section_label(0.3, 4.55, "TOOLS")

TOOLS = [
    (0.3,  "DuckDuckGo\nSearch"),
    (4.1,  "Web Content\nFetcher"),
    (7.9,  "Code\nExecutor"),
    (11.7, "File\nWriter"),
    (15.5, "File\nReader"),
]
TOOL_W = 3.5
TOOL_H = 0.85
TOOL_CXS = []
for ax_pos, title in TOOLS:
    box(ax_pos, 3.65, TOOL_W, TOOL_H, title, color=C["tool"], fs=9)
    TOOL_CXS.append(ax_pos + TOOL_W / 2)

# Task → Tool connections (show which agent/task uses which tools)
# Researcher → DDG, WebFetcher
arrow(AGENT_CXS[0], 5.55, TOOL_CXS[0], 4.5, color=C["dim"], ls="dashed", lw=1)
arrow(AGENT_CXS[0], 5.55, TOOL_CXS[1], 4.5, color=C["dim"], ls="dashed", lw=1)
# Coder → Code Executor, File Writer, File Reader
arrow(AGENT_CXS[1], 5.55, TOOL_CXS[2], 4.5, color=C["dim"], ls="dashed", lw=1)
arrow(AGENT_CXS[1], 5.55, TOOL_CXS[3], 4.5, color=C["dim"], ls="dashed", lw=1)
arrow(AGENT_CXS[1], 5.55, TOOL_CXS[4], 4.5, color=C["dim"], ls="dashed", lw=1)
# Reviewer → File Reader, DDG
arrow(AGENT_CXS[2], 5.55, TOOL_CXS[0], 4.5, color=C["dim"], ls="dashed", lw=1)
arrow(AGENT_CXS[2], 5.55, TOOL_CXS[4], 4.5, color=C["dim"], ls="dashed", lw=1)
# Executor → Code Executor, DDG
arrow(AGENT_CXS[3], 5.55, TOOL_CXS[2], 4.5, color=C["dim"], ls="dashed", lw=1)
arrow(AGENT_CXS[3], 5.55, TOOL_CXS[0], 4.5, color=C["dim"], ls="dashed", lw=1)

# ── Layer 8 — External World ──────────────────────────────────────────────────
section_label(0.3, 2.8, "EXTERNAL")

EXT_DATA = [
    (0.5,  "Internet / Web",      "Search results · Page content"),
    (7.0,  "File System",         "Read · Write · Persist"),
    (13.5, "Subprocess Runtime",  "Python · JavaScript · Bash"),
]
for ax_pos, title, sub in EXT_DATA:
    box(ax_pos, 2.0, 6.0, 0.85, title, sub, color=C["external"], fs=9)

# Tool → External
arrow(TOOL_CXS[0], 3.65, 2.5,  2.85, color=C["line"])   # DDG   → Internet
arrow(TOOL_CXS[1], 3.65, 3.5,  2.85, color=C["line"])   # Web   → Internet
arrow(TOOL_CXS[3], 3.65, 9.0,  2.85, color=C["line"])   # FW    → FileSystem
arrow(TOOL_CXS[4], 3.65, 11.0, 2.85, color=C["line"])   # FR    → FileSystem
arrow(TOOL_CXS[2], 3.65, 16.5, 2.85, color=C["line"])   # Code  → Subprocess

# ── Legend ────────────────────────────────────────────────────────────────────
ax.plot([0.5, 19.5], [1.55, 1.55], color=C["line"], lw=0.6, zorder=2)
legend_items = [
    (C["entry"],    "Entry Point"),
    (C["crew"],     "Crew Layer"),
    (C["agent"],    "Agents"),
    (C["task"],     "Tasks"),
    (C["tool"],     "Tools"),
    (C["llm"],      "LLM (local)"),
    (C["external"], "External World"),
]
lx = 0.8
for color, label in legend_items:
    rect = FancyBboxPatch((lx, 0.9), 0.45, 0.35,
                          boxstyle="round,pad=0.04",
                          facecolor=color, edgecolor=color, linewidth=1.5, zorder=3)
    ax.add_patch(rect)
    ax.text(lx + 0.6, 1.075, label, color=C["white"], fontsize=8.5,
            va="center", zorder=4)
    lx += 2.65

ax.text(W / 2, 0.35, "Dashed lines = tool access per agent   ·   Solid lines = data / control flow",
        ha="center", color=C["dim"], fontsize=8.5, zorder=5)

# ── Save ──────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0.4)
out = "openclaw_architecture.png"
plt.savefig(out, dpi=180, bbox_inches="tight",
            facecolor="#0d1117", edgecolor="none")
print(f"Saved: {out}")
