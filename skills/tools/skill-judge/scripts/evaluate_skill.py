#!/usr/bin/env python3
"""
evaluate_skill.py -- Automated skill evaluation and scoring.

Scores skills across six quality dimensions (0-10 each, 60 total) and
assigns a letter grade.  Supports single-skill evaluation, batch mode,
JSON output, sorting, and minimum-score filtering.

Usage:
    python evaluate_skill.py .agents/skills/clean-code
    python evaluate_skill.py --all
    python evaluate_skill.py --all --json
    python evaluate_skill.py --all --sort score
    python evaluate_skill.py --all --min-score 40

No external dependencies — uses only stdlib (argparse, pathlib, re, json).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SKILLS_DIR = Path(".agents/skills")
MAX_SCORE_PER_DIM = 10
DIMENSIONS = [
    "Structure",
    "Completeness",
    "Actionability",
    "Depth",
    "Ecosystem",
    "Quality",
]
GRADE_THRESHOLDS = [
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
    (0,  "F"),
]
PLACEHOLDER_PATS = [
    re.compile(r"\bTODO\b", re.I),
    re.compile(r"\bFIXME\b", re.I),
    re.compile(r"<placeholder>", re.I),
    re.compile(r"\bTBD\b"),
    re.compile(r"\bXXX\b"),
]
EMPTY_SECTION_RE = re.compile(
    r"^(#{1,3}\s+.+)\n{2,}(?=#{1,3}\s|\Z)", re.MULTILINE
)

# ---------------------------------------------------------------------------
# Terminal colors (graceful no-color fallback)
# ---------------------------------------------------------------------------
def _has_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

_COLOR = _has_color()

def _c(code: str, t: str) -> str:
    return f"\033[{code}m{t}\033[0m" if _COLOR else t

def red(t: str) -> str:    return _c("31", t)
def green(t: str) -> str:  return _c("32", t)
def yellow(t: str) -> str: return _c("33", t)
def cyan(t: str) -> str:   return _c("36", t)
def bold(t: str) -> str:   return _c("1", t)
def dim(t: str) -> str:    return _c("2", t)

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------
@dataclass
class DimensionScore:
    name: str
    score: int
    max_score: int
    notes: list[str] = field(default_factory=list)

    def bar(self, width: int = 11) -> str:
        filled = round(self.score / self.max_score * width)
        return "\u2588" * filled + "\u2591" * (width - filled)

@dataclass
class SkillEvaluation:
    name: str
    path: str
    dimensions: list[DimensionScore] = field(default_factory=list)

    @property
    def total(self) -> int:
        return sum(d.score for d in self.dimensions)

    @property
    def max_total(self) -> int:
        return sum(d.max_score for d in self.dimensions)

    @property
    def pct(self) -> float:
        return (self.total / self.max_total * 100) if self.max_total else 0

    @property
    def grade(self) -> str:
        p = self.pct
        for threshold, letter in GRADE_THRESHOLDS:
            if p >= threshold:
                return letter
        return "F"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "total": self.total,
            "max": self.max_total,
            "pct": round(self.pct, 1),
            "grade": self.grade,
            "dimensions": [
                {"name": d.name, "score": d.score, "max": d.max_score,
                 "notes": d.notes}
                for d in self.dimensions
            ],
        }

# ---------------------------------------------------------------------------
# Frontmatter helpers (no PyYAML dependency)
# ---------------------------------------------------------------------------
def _parse_frontmatter(content: str) -> Optional[dict[str, str]]:
    """Extract YAML-like frontmatter as a simple key-value dict."""
    if not content.startswith("---"):
        return None
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return None
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        kv = line.split(":", 1)
        if len(kv) == 2:
            fm[kv[0].strip()] = kv[1].strip().strip('"').strip("'")
    return fm


def _body(content: str) -> str:
    """Return SKILL.md content after frontmatter."""
    m = re.match(r"^---\n.*?\n---\n?(.*)", content, re.DOTALL)
    return m.group(1) if m else content

# ---------------------------------------------------------------------------
# Scoring functions — each returns a DimensionScore
# ---------------------------------------------------------------------------
def score_structure(content: str, fm: Optional[dict]) -> DimensionScore:
    """Has YAML frontmatter, proper H1, sections with tables, code examples."""
    ds = DimensionScore(name="Structure", score=0, max_score=MAX_SCORE_PER_DIM)
    body = _body(content)

    # Frontmatter (3 pts)
    if fm is not None:
        ds.score += 2
        ds.notes.append("has frontmatter")
        if "name" in fm and "description" in fm:
            ds.score += 1
            ds.notes.append("frontmatter has name+description")
        else:
            ds.notes.append("frontmatter missing name or description")
    else:
        ds.notes.append("no YAML frontmatter")

    # H1 heading (1 pt)
    if re.search(r"^# .+", body, re.MULTILINE):
        ds.score += 1
        ds.notes.append("has H1 heading")
    else:
        ds.notes.append("no H1 heading")

    # H2 sections (2 pts)
    h2_count = len(re.findall(r"^## .+", body, re.MULTILINE))
    if h2_count >= 4:
        ds.score += 2
        ds.notes.append(f"{h2_count} H2 sections")
    elif h2_count >= 2:
        ds.score += 1
        ds.notes.append(f"only {h2_count} H2 sections")
    else:
        ds.notes.append(f"only {h2_count} H2 section(s)")

    # Tables (2 pts)
    table_count = len(re.findall(r"^\|.+\|.+\|$", body, re.MULTILINE))
    if table_count >= 6:
        ds.score += 2
        ds.notes.append(f"{table_count} table rows")
    elif table_count >= 2:
        ds.score += 1
        ds.notes.append(f"only {table_count} table rows")
    else:
        ds.notes.append("no tables")

    # Code examples (2 pts)
    code_blocks = len(re.findall(r"^```", body, re.MULTILINE))
    fenced = code_blocks // 2  # opening+closing pairs
    if fenced >= 3:
        ds.score += 2
        ds.notes.append(f"{fenced} code blocks")
    elif fenced >= 1:
        ds.score += 1
        ds.notes.append(f"only {fenced} code block(s)")
    else:
        ds.notes.append("no code blocks")

    return ds


def score_completeness(content: str, fm: Optional[dict]) -> DimensionScore:
    """Has name, description, core content, examples, references."""
    ds = DimensionScore(name="Completeness", score=0, max_score=MAX_SCORE_PER_DIM)
    body = _body(content)
    bl = body.lower()

    # Name (1 pt)
    if fm and fm.get("name"):
        ds.score += 1
        ds.notes.append("has name")
    else:
        ds.notes.append("missing name")

    # Description (2 pts)
    desc = (fm or {}).get("description", "")
    if len(desc) >= 80:
        ds.score += 2
        ds.notes.append("rich description")
    elif len(desc) >= 20:
        ds.score += 1
        ds.notes.append("short description")
    else:
        ds.notes.append("missing or very short description")

    # Core content section (2 pts)
    core_keywords = ["core", "principle", "overview", "fundamental", "philosophy",
                     "guideline", "standard", "rule"]
    found_core = sum(1 for kw in core_keywords if kw in bl)
    if found_core >= 3:
        ds.score += 2
        ds.notes.append("strong core content")
    elif found_core >= 1:
        ds.score += 1
        ds.notes.append("some core content")
    else:
        ds.notes.append("weak core content")

    # Examples / patterns (2 pts)
    example_markers = len(re.findall(
        r"(example|pattern|sample|template|snippet|demo)", bl))
    code_blocks = len(re.findall(r"^```", body, re.MULTILINE)) // 2
    ex_score = min(example_markers + code_blocks, 6)
    if ex_score >= 4:
        ds.score += 2
        ds.notes.append("good examples coverage")
    elif ex_score >= 1:
        ds.score += 1
        ds.notes.append("some examples")
    else:
        ds.notes.append("no examples")

    # Anti-patterns / warnings (1 pt)
    anti_kws = ["never", "don't", "avoid", "anti-pattern", "bad", "wrong",
                "mistake", "pitfall"]
    if sum(1 for kw in anti_kws if kw in bl) >= 2:
        ds.score += 1
        ds.notes.append("has anti-patterns / warnings")
    else:
        ds.notes.append("no anti-patterns section")

    # References / links (2 pts)
    links = re.findall(r"\[([^\]]*)\]\(([^)]+)\)", body)
    if len(links) >= 5:
        ds.score += 2
        ds.notes.append(f"{len(links)} links/references")
    elif len(links) >= 1:
        ds.score += 1
        ds.notes.append(f"only {len(links)} link(s)")
    else:
        ds.notes.append("no links or references")

    return ds


def score_actionability(content: str) -> DimensionScore:
    """Contains tables, code snippets, checklists, step-by-step instructions."""
    ds = DimensionScore(name="Actionability", score=0, max_score=MAX_SCORE_PER_DIM)
    body = _body(content)

    # Tables (3 pts)
    table_rows = len(re.findall(r"^\|.+\|.+\|$", body, re.MULTILINE))
    if table_rows >= 10:
        ds.score += 3
        ds.notes.append(f"{table_rows} table rows")
    elif table_rows >= 5:
        ds.score += 2
        ds.notes.append(f"{table_rows} table rows")
    elif table_rows >= 1:
        ds.score += 1
        ds.notes.append(f"only {table_rows} table row(s)")
    else:
        ds.notes.append("no tables")

    # Code blocks (3 pts)
    code_blocks = len(re.findall(r"^```", body, re.MULTILINE)) // 2
    if code_blocks >= 5:
        ds.score += 3
        ds.notes.append(f"{code_blocks} code blocks")
    elif code_blocks >= 2:
        ds.score += 2
        ds.notes.append(f"{code_blocks} code blocks")
    elif code_blocks >= 1:
        ds.score += 1
        ds.notes.append(f"only {code_blocks} code block")
    else:
        ds.notes.append("no code blocks")

    # Checklists (2 pts)
    checklists = len(re.findall(r"^\s*-\s*\[[ x]\]", body, re.MULTILINE))
    bullets = len(re.findall(r"^\s*[-*]\s+\S", body, re.MULTILINE))
    if checklists >= 3:
        ds.score += 2
        ds.notes.append(f"{checklists} checklist items")
    elif checklists >= 1 or bullets >= 8:
        ds.score += 1
        ds.notes.append(f"{checklists} checklist(s), {bullets} bullet(s)")
    else:
        ds.notes.append("no checklists")

    # Step-by-step / numbered lists / decision trees (2 pts)
    numbered = len(re.findall(r"^\s*\d+\.\s+", body, re.MULTILINE))
    decision_kws = sum(1 for kw in ["if ", "when ", "decision", "choose",
                                     "step ", "phase", "workflow"]
                       if kw in body.lower())
    if numbered >= 5 or decision_kws >= 4:
        ds.score += 2
        ds.notes.append(f"{numbered} numbered items, {decision_kws} decision keywords")
    elif numbered >= 2 or decision_kws >= 2:
        ds.score += 1
        ds.notes.append(f"{numbered} numbered items, {decision_kws} decision keywords")
    else:
        ds.notes.append("no step-by-step instructions")

    return ds


def score_depth(content: str) -> DimensionScore:
    """Line count, section count, detail level."""
    ds = DimensionScore(name="Depth", score=0, max_score=MAX_SCORE_PER_DIM)
    body = _body(content)
    lines = content.count("\n") + 1
    sections = len(re.findall(r"^#{1,3}\s+.+", body, re.MULTILINE))
    words = len(body.split())

    # Line count (4 pts): 50+ min, 150+ good, 250+ excellent
    if lines >= 250:
        ds.score += 4
        ds.notes.append(f"{lines} lines (excellent)")
    elif lines >= 150:
        ds.score += 3
        ds.notes.append(f"{lines} lines (good)")
    elif lines >= 80:
        ds.score += 2
        ds.notes.append(f"{lines} lines (adequate)")
    elif lines >= 50:
        ds.score += 1
        ds.notes.append(f"{lines} lines (minimal)")
    else:
        ds.notes.append(f"{lines} lines (too short)")

    # Section count (3 pts)
    if sections >= 8:
        ds.score += 3
        ds.notes.append(f"{sections} sections")
    elif sections >= 5:
        ds.score += 2
        ds.notes.append(f"{sections} sections")
    elif sections >= 2:
        ds.score += 1
        ds.notes.append(f"{sections} sections")
    else:
        ds.notes.append(f"only {sections} section(s)")

    # Word count / detail level (3 pts)
    if words >= 1500:
        ds.score += 3
        ds.notes.append(f"{words} words (deep)")
    elif words >= 800:
        ds.score += 2
        ds.notes.append(f"{words} words")
    elif words >= 300:
        ds.score += 1
        ds.notes.append(f"{words} words")
    else:
        ds.notes.append(f"only {words} words")

    return ds


def score_ecosystem(skill_path: Path) -> DimensionScore:
    """Has references/, templates/, scripts/ subdirectories with content."""
    ds = DimensionScore(name="Ecosystem", score=0, max_score=MAX_SCORE_PER_DIM)

    subdirs = {
        "references": 3,
        "templates": 2,
        "scripts": 2,
        "assets": 1,
    }
    total_weight = 0
    earned = 0

    for dirname, weight in subdirs.items():
        d = skill_path / dirname
        if d.is_dir():
            files = [f for f in d.iterdir() if f.is_file()]
            if files:
                earned += weight
                ds.notes.append(f"{dirname}/ ({len(files)} file(s))")
            else:
                ds.notes.append(f"{dirname}/ exists but empty")
        total_weight += weight

    # Additional files beyond SKILL.md (2 pts)
    extra_files = [f for f in skill_path.iterdir()
                   if f.is_file() and f.name != "SKILL.md"
                   and not f.name.startswith(".")]
    if extra_files:
        earned += min(len(extra_files), 2)
        ds.notes.append(f"{len(extra_files)} extra file(s) at root")

    if not any((skill_path / d).is_dir() for d in subdirs) and not extra_files:
        ds.notes.append("no ecosystem (SKILL.md only)")

    # Scale earned points to 0-10
    ds.score = min(round(earned / total_weight * MAX_SCORE_PER_DIM), MAX_SCORE_PER_DIM)
    return ds


def score_quality(content: str) -> DimensionScore:
    """No placeholder text, no TODO markers, no empty sections, consistent formatting."""
    ds = DimensionScore(name="Quality", score=MAX_SCORE_PER_DIM, max_score=MAX_SCORE_PER_DIM)
    body = _body(content)

    # Placeholder / TODO markers (-2 per type found, max -4)
    placeholder_penalty = 0
    for pat in PLACEHOLDER_PATS:
        hits = len(pat.findall(body))
        if hits:
            placeholder_penalty += 2
            ds.notes.append(f"found {hits}x {pat.pattern}")
    ds.score -= min(placeholder_penalty, 4)

    # Empty sections (-1 each, max -3)
    empty = EMPTY_SECTION_RE.findall(body)
    if empty:
        penalty = min(len(empty), 3)
        ds.score -= penalty
        ds.notes.append(f"{len(empty)} empty section(s)")

    # Inconsistent heading levels (-1)
    headings = re.findall(r"^(#{1,6})\s", body, re.MULTILINE)
    if headings:
        levels = [len(h) for h in headings]
        # Check for jumps > 1 level (e.g. H1 -> H3)
        for i in range(1, len(levels)):
            if levels[i] > levels[i - 1] + 1:
                ds.score -= 1
                ds.notes.append("heading level jump detected")
                break

    # Trailing whitespace (-1)
    trailing = sum(1 for line in content.splitlines() if line != line.rstrip())
    if trailing > 5:
        ds.score -= 1
        ds.notes.append(f"{trailing} lines with trailing whitespace")

    # Very long lines (-1)
    long_lines = sum(1 for line in body.splitlines() if len(line) > 200)
    if long_lines > 3:
        ds.score -= 1
        ds.notes.append(f"{long_lines} lines > 200 chars")

    ds.score = max(ds.score, 0)
    if ds.score == MAX_SCORE_PER_DIM:
        ds.notes.append("clean — no issues detected")

    return ds

# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def evaluate_skill(skill_path: Path) -> SkillEvaluation:
    """Run all dimension scorers against a single skill directory."""
    ev = SkillEvaluation(name=skill_path.name, path=str(skill_path))
    md = skill_path / "SKILL.md"
    if not md.exists():
        # Return zeroes for all dimensions
        for name in DIMENSIONS:
            ev.dimensions.append(
                DimensionScore(name=name, score=0, max_score=MAX_SCORE_PER_DIM,
                               notes=["SKILL.md not found"]))
        return ev

    try:
        content = md.read_text()
    except OSError as e:
        for name in DIMENSIONS:
            ev.dimensions.append(
                DimensionScore(name=name, score=0, max_score=MAX_SCORE_PER_DIM,
                               notes=[f"Cannot read SKILL.md: {e}"]))
        return ev

    fm = _parse_frontmatter(content)

    ev.dimensions.append(score_structure(content, fm))
    ev.dimensions.append(score_completeness(content, fm))
    ev.dimensions.append(score_actionability(content))
    ev.dimensions.append(score_depth(content))
    ev.dimensions.append(score_ecosystem(skill_path))
    ev.dimensions.append(score_quality(content))

    return ev

# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------
def discover_skills(root: Path, single: Optional[str] = None) -> list[Path]:
    """Find skill directories under .agents/skills/."""
    base = root / SKILLS_DIR
    if not base.is_dir():
        print(red(f"Skills directory not found: {base}"), file=sys.stderr)
        sys.exit(1)
    if single:
        # Accept either bare name or path
        target = Path(single)
        if not target.is_absolute():
            # Try as relative path first, then as bare name
            if not target.is_dir():
                target = base / target.name
            if not target.is_dir():
                target = base / single
        if not target.is_dir():
            print(red(f"Skill not found: {single}"), file=sys.stderr)
            sys.exit(1)
        return [target]
    return sorted(p for p in base.iterdir()
                  if p.is_dir() and (p / "SKILL.md").exists())


def resolve_repo_root() -> Path:
    """Walk up from cwd to find the repo root containing .agents/skills/."""
    c = Path.cwd()
    while c != c.parent:
        if (c / SKILLS_DIR).is_dir():
            return c
        c = c.parent
    return Path.cwd()

# ---------------------------------------------------------------------------
# Reporting — Markdown
# ---------------------------------------------------------------------------
def _grade_color(grade: str) -> str:
    return {"A": green, "B": green, "C": yellow, "D": yellow, "F": red}.get(
        grade, str)(grade)


def print_evaluation(ev: SkillEvaluation) -> None:
    """Pretty-print a single skill evaluation."""
    header = f"Skill Evaluation: {ev.name}"
    print(f"\n{bold(header)}")
    print(bold("=" * len(header)))

    max_label = max(len(d.name) for d in ev.dimensions)
    for d in ev.dimensions:
        label = d.name.ljust(max_label)
        bar = d.bar()
        score_str = f"{d.score}/{d.max_score}"
        if d.score >= 8:
            score_str = green(score_str)
        elif d.score >= 5:
            score_str = yellow(score_str)
        else:
            score_str = red(score_str)
        print(f"  {label}  {score_str}  {bar}")

    print()
    pct = round(ev.pct)
    grade = _grade_color(ev.grade)
    print(f"  {bold('Overall')}: {ev.total}/{ev.max_total} ({pct}%) — "
          f"Grade: {bold(grade)}")
    print()


def print_batch_summary(evaluations: list[SkillEvaluation]) -> None:
    """Print a summary table for batch evaluations."""
    print(f"\n{bold('=' * 72)}")
    print(bold("  Skill Evaluation Summary"))
    print(bold("=" * 72))

    max_name = max(len(e.name) for e in evaluations) if evaluations else 10
    header = f"  {'Skill'.ljust(max_name)}  {'Score':>7}  {'Pct':>5}  Grade"
    print(dim(header))
    print(dim("  " + "-" * (max_name + 24)))

    for ev in evaluations:
        score_str = f"{ev.total}/{ev.max_total}"
        pct_str = f"{round(ev.pct)}%"
        grade = _grade_color(ev.grade)
        print(f"  {ev.name.ljust(max_name)}  {score_str:>7}  {pct_str:>5}  {grade}")

    # Aggregate stats
    total_skills = len(evaluations)
    avg_score = sum(e.total for e in evaluations) / total_skills if total_skills else 0
    avg_pct = sum(e.pct for e in evaluations) / total_skills if total_skills else 0
    grade_dist = {}
    for e in evaluations:
        grade_dist[e.grade] = grade_dist.get(e.grade, 0) + 1

    print(dim("  " + "-" * (max_name + 24)))
    print(f"  {bold('Total')}: {total_skills} skills   "
          f"{bold('Avg')}: {avg_score:.1f}/{evaluations[0].max_total if evaluations else 60} "
          f"({avg_pct:.0f}%)   "
          f"Grades: {', '.join(f'{g}={n}' for g, n in sorted(grade_dist.items()))}")
    print(bold("=" * 72) + "\n")


def print_json_output(evaluations: list[SkillEvaluation]) -> None:
    """Output evaluations as JSON."""
    total = len(evaluations)
    output = {
        "summary": {
            "total": total,
            "avg_score": round(sum(e.total for e in evaluations) / total, 1) if total else 0,
            "avg_pct": round(sum(e.pct for e in evaluations) / total, 1) if total else 0,
            "grade_distribution": {},
        },
        "evaluations": [e.to_dict() for e in evaluations],
    }
    for e in evaluations:
        g = e.grade
        output["summary"]["grade_distribution"][g] = (
            output["summary"]["grade_distribution"].get(g, 0) + 1)
    print(json.dumps(output, indent=2))

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Evaluate skills against quality criteria and score them.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  %(prog)s .agents/skills/clean-code\n"
            "  %(prog)s --all\n"
            "  %(prog)s --all --json\n"
            "  %(prog)s --all --sort score\n"
            "  %(prog)s --all --min-score 40\n"
        ),
    )
    p.add_argument("skill_path", nargs="?", default=None,
                   help="Path to a skill directory (containing SKILL.md)")
    p.add_argument("--all", action="store_true",
                   help="Evaluate all skills in .agents/skills/")
    p.add_argument("--json", action="store_true", dest="json_output",
                   help="Output results as JSON")
    p.add_argument("--sort", choices=["score", "name", "grade"],
                   default="name",
                   help="Sort order for batch results (default: name)")
    p.add_argument("--min-score", type=int, default=None, metavar="N",
                   help="Only show skills with total score >= N")
    p.add_argument("--verbose", action="store_true",
                   help="Show per-dimension notes in markdown output")
    return p


def main() -> int:
    args = build_parser().parse_args()

    if not args.skill_path and not args.all:
        print(red("Provide a skill path or use --all"), file=sys.stderr)
        return 1

    root = resolve_repo_root()

    if args.all:
        skill_dirs = discover_skills(root)
    else:
        skill_dirs = discover_skills(root, single=args.skill_path)

    if not skill_dirs:
        print(red("No skills found."), file=sys.stderr)
        return 1

    evaluations = [evaluate_skill(sd) for sd in skill_dirs]

    # Filter by minimum score
    if args.min_score is not None:
        evaluations = [e for e in evaluations if e.total >= args.min_score]

    # Sort
    if args.sort == "score":
        evaluations.sort(key=lambda e: e.total, reverse=True)
    elif args.sort == "grade":
        grade_order = {"A": 0, "B": 1, "C": 2, "D": 3, "F": 4}
        evaluations.sort(key=lambda e: (grade_order.get(e.grade, 5), -e.total))
    else:
        evaluations.sort(key=lambda e: e.name)

    # Output
    if args.json_output:
        print_json_output(evaluations)
    elif len(evaluations) == 1:
        ev = evaluations[0]
        print_evaluation(ev)
        if args.verbose:
            for d in ev.dimensions:
                print(f"  {bold(d.name)}:")
                for note in d.notes:
                    print(f"    - {dim(note)}")
            print()
    else:
        for ev in evaluations:
            print_evaluation(ev)
        print_batch_summary(evaluations)

    return 0


if __name__ == "__main__":
    sys.exit(main())
