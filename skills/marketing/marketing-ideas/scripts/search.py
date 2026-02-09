#!/usr/bin/env python3
"""Search and filter marketing ideas from the ideas CSV database.

Usage:
    python search.py "keyword"                          # keyword search
    python search.py --category "Content"               # by category
    python search.py --effort low --budget free          # filter by effort/budget
    python search.py --stage early                       # by stage
    python search.py --impact high                       # high impact only
    python search.py --timeline quick                    # quick wins
    python search.py --list-categories                   # show all categories
    python search.py --effort low --impact high          # combine filters
"""

import argparse
import csv
import os
import sys
from pathlib import Path

# Column widths for formatting
COL_ID = 4
COL_NAME = 32
COL_CATEGORY = 22
COL_EFFORT = 8
COL_IMPACT = 8
COL_BUDGET = 8
COL_STAGE = 12
COL_TIMELINE = 8


def get_csv_path() -> Path:
    """Resolve the path to ideas.csv relative to this script."""
    script_dir = Path(__file__).resolve().parent
    csv_path = script_dir.parent / "data" / "ideas.csv"
    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}", file=sys.stderr)
        sys.exit(1)
    return csv_path


def load_ideas(csv_path: Path) -> list[dict]:
    """Load all ideas from the CSV file."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def search_keyword(ideas: list[dict], keyword: str) -> list[dict]:
    """Search ideas by keyword across name, category, and description."""
    keyword_lower = keyword.lower()
    results = []
    for idea in ideas:
        searchable = " ".join([
            idea.get("name", ""),
            idea.get("category", ""),
            idea.get("description", ""),
        ]).lower()
        if keyword_lower in searchable:
            results.append(idea)
    return results


def filter_ideas(ideas: list[dict], **filters) -> list[dict]:
    """Filter ideas by exact match on specified fields."""
    results = ideas
    for field, value in filters.items():
        if value is None:
            continue
        value_lower = value.lower()
        if field == "category":
            # Category supports partial matching
            results = [
                idea for idea in results
                if value_lower in idea.get("category", "").lower()
            ]
        else:
            results = [
                idea for idea in results
                if idea.get(field, "").lower() == value_lower
            ]
    return results


def get_categories(ideas: list[dict]) -> list[str]:
    """Get sorted unique categories."""
    categories = set()
    for idea in ideas:
        cat = idea.get("category", "").strip()
        if cat:
            categories.add(cat)
    return sorted(categories)


def print_header():
    """Print the table header."""
    header = (
        f"{'ID':<{COL_ID}} "
        f"{'Name':<{COL_NAME}} "
        f"{'Category':<{COL_CATEGORY}} "
        f"{'Effort':<{COL_EFFORT}} "
        f"{'Impact':<{COL_IMPACT}} "
        f"{'Budget':<{COL_BUDGET}} "
        f"{'Stage':<{COL_STAGE}} "
        f"{'Timeline':<{COL_TIMELINE}}"
    )
    print(header)
    print("-" * len(header))


def print_idea(idea: dict):
    """Print a single idea row."""
    print(
        f"{idea.get('id', ''):<{COL_ID}} "
        f"{idea.get('name', ''):<{COL_NAME}} "
        f"{idea.get('category', ''):<{COL_CATEGORY}} "
        f"{idea.get('effort', ''):<{COL_EFFORT}} "
        f"{idea.get('impact', ''):<{COL_IMPACT}} "
        f"{idea.get('budget', ''):<{COL_BUDGET}} "
        f"{idea.get('stage', ''):<{COL_STAGE}} "
        f"{idea.get('timeline', ''):<{COL_TIMELINE}}"
    )


def print_detail(idea: dict):
    """Print a detailed view of a single idea."""
    print(f"  [{idea.get('id', '')}] {idea.get('name', '')}")
    print(f"       Category: {idea.get('category', '')}")
    print(f"       {idea.get('description', '')}")
    print(
        f"       Effort: {idea.get('effort', '')} | "
        f"Impact: {idea.get('impact', '')} | "
        f"Budget: {idea.get('budget', '')} | "
        f"Stage: {idea.get('stage', '')} | "
        f"Timeline: {idea.get('timeline', '')}"
    )
    print()


def print_results(ideas: list[dict], detail: bool = False):
    """Print search results."""
    if not ideas:
        print("No ideas found matching your criteria.")
        return

    print(f"\nFound {len(ideas)} idea(s):\n")

    if detail:
        for idea in ideas:
            print_detail(idea)
    else:
        print_header()
        for idea in ideas:
            print_idea(idea)
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Search and filter marketing ideas.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python search.py "SEO"                         # keyword search
  python search.py --category "Content"          # by category
  python search.py --effort low --budget free    # filter by effort/budget
  python search.py --stage early                 # by stage
  python search.py --impact high                 # high impact only
  python search.py --timeline quick              # quick wins
  python search.py --list-categories             # show all categories
  python search.py --detail "email"              # detailed view""",
    )

    parser.add_argument(
        "keyword", nargs="?", default=None,
        help="Keyword to search across name, category, and description",
    )
    parser.add_argument(
        "--category", "-c", default=None,
        help="Filter by category (partial match)",
    )
    parser.add_argument(
        "--effort", "-e", default=None, choices=["low", "medium", "high"],
        help="Filter by effort level",
    )
    parser.add_argument(
        "--impact", "-i", default=None, choices=["low", "medium", "high"],
        help="Filter by impact level",
    )
    parser.add_argument(
        "--budget", "-b", default=None, choices=["free", "low", "medium", "high"],
        help="Filter by budget requirement",
    )
    parser.add_argument(
        "--stage", "-s", default=None,
        choices=["pre-launch", "early", "growth", "scale", "any"],
        help="Filter by company stage",
    )
    parser.add_argument(
        "--timeline", "-t", default=None, choices=["quick", "medium", "long"],
        help="Filter by implementation timeline",
    )
    parser.add_argument(
        "--list-categories", action="store_true",
        help="List all available categories",
    )
    parser.add_argument(
        "--detail", "-d", action="store_true",
        help="Show detailed view with descriptions",
    )

    args = parser.parse_args()

    csv_path = get_csv_path()
    ideas = load_ideas(csv_path)

    # List categories mode
    if args.list_categories:
        categories = get_categories(ideas)
        print(f"\n{len(categories)} categories:\n")
        for cat in categories:
            count = sum(1 for i in ideas if i.get("category") == cat)
            print(f"  {cat:<25} ({count} ideas)")
        print()
        return

    # No arguments: show all
    if (
        args.keyword is None
        and args.category is None
        and args.effort is None
        and args.impact is None
        and args.budget is None
        and args.stage is None
        and args.timeline is None
    ):
        print_results(ideas, detail=args.detail)
        return

    # Start with all ideas
    results = ideas

    # Apply keyword search
    if args.keyword:
        results = search_keyword(results, args.keyword)

    # Apply filters
    results = filter_ideas(
        results,
        category=args.category,
        effort=args.effort,
        impact=args.impact,
        budget=args.budget,
        stage=args.stage,
        timeline=args.timeline,
    )

    print_results(results, detail=args.detail)


if __name__ == "__main__":
    main()
