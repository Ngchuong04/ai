#!/usr/bin/env python3
"""Search marketing psychology mental models from models.csv.

Usage:
    python search.py "pricing"                # keyword search across all fields
    python search.py --category "Pricing"     # filter by category (partial match)
    python search.py --trigger "conversions"  # filter by trigger context
    python search.py --difficulty beginner    # filter by difficulty level
    python search.py --list-categories        # show all categories with counts
    python search.py --list-triggers          # show all trigger contexts
    python search.py --stats                  # summary statistics
"""

import argparse
import csv
import os
import sys
from collections import Counter

# Resolve CSV path relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "..", "data", "models.csv")


def load_models(path=CSV_PATH):
    """Load mental models from CSV file."""
    resolved = os.path.normpath(path)
    if not os.path.exists(resolved):
        print(f"Error: CSV not found at {resolved}", file=sys.stderr)
        sys.exit(1)
    with open(resolved, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def keyword_search(models, query):
    """Search across all fields for a keyword (case-insensitive)."""
    query_lower = query.lower()
    results = []
    for model in models:
        searchable = " ".join(model.values()).lower()
        if query_lower in searchable:
            results.append(model)
    return results


def filter_by_field(models, field, value):
    """Filter models where a field contains the value (case-insensitive)."""
    value_lower = value.lower()
    return [m for m in models if value_lower in m.get(field, "").lower()]


def format_model(model, verbose=True):
    """Format a single model for display."""
    lines = [
        f"  [{model['id']}] {model['name']}",
        f"      Category:    {model['category']}",
        f"      Difficulty:  {model['difficulty']}",
    ]
    if verbose:
        lines.append(f"      Description: {model['description']}")
        lines.append(f"      Application: {model['marketing_application']}")
        lines.append(f"      Trigger:     {model['trigger_context']}")
    return "\n".join(lines)


def print_results(results, query_desc, verbose=True):
    """Print formatted search results."""
    count = len(results)
    if count == 0:
        print(f"\nNo models found for: {query_desc}")
        return

    noun = "model" if count == 1 else "models"
    print(f"\n{count} {noun} found for: {query_desc}")
    print("=" * 60)

    # Group by category for readability
    by_category = {}
    for model in results:
        cat = model["category"]
        by_category.setdefault(cat, []).append(model)

    for category, models_in_cat in by_category.items():
        print(f"\n  --- {category} ---")
        for model in models_in_cat:
            print(format_model(model, verbose=verbose))
            print()


def list_categories(models):
    """Display all categories with model counts."""
    counts = Counter(m["category"] for m in models)
    print(f"\nCategories ({len(counts)} total):")
    print("=" * 40)
    for category, count in counts.items():
        noun = "model" if count == 1 else "models"
        print(f"  {category:30s} {count:3d} {noun}")
    print(f"  {'TOTAL':30s} {len(models):3d}")


def list_triggers(models):
    """Display all unique trigger contexts with counts."""
    counts = Counter(m["trigger_context"] for m in models)
    print(f"\nTrigger Contexts ({len(counts)} unique):")
    print("=" * 40)
    for trigger, count in counts.most_common():
        noun = "model" if count == 1 else "models"
        print(f"  {trigger:30s} {count:3d} {noun}")


def show_stats(models):
    """Display summary statistics."""
    total = len(models)
    categories = Counter(m["category"] for m in models)
    difficulties = Counter(m["difficulty"] for m in models)
    triggers = Counter(m["trigger_context"] for m in models)

    print(f"\nMarketing Psychology Mental Models — Summary")
    print("=" * 50)
    print(f"  Total models: {total}")

    print(f"\n  By category ({len(categories)}):")
    for cat, count in categories.items():
        print(f"    {cat:30s} {count:3d}")

    print(f"\n  By difficulty:")
    for level in ("beginner", "intermediate", "advanced"):
        print(f"    {level:30s} {difficulties.get(level, 0):3d}")

    print(f"\n  Top trigger contexts:")
    for trigger, count in triggers.most_common(8):
        print(f"    {trigger:30s} {count:3d}")


def build_parser():
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        description="Search marketing psychology mental models.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  python search.py "pricing"                keyword search
  python search.py --category "Pricing"     by category
  python search.py --trigger "conversions"  by trigger context
  python search.py --difficulty beginner    by difficulty
  python search.py --list-categories        show categories
  python search.py --list-triggers          show trigger contexts
  python search.py --stats                  summary statistics
""",
    )
    parser.add_argument(
        "query",
        nargs="?",
        default=None,
        help="Keyword to search across all fields",
    )
    parser.add_argument(
        "--category", "-c",
        help="Filter by category (partial match)",
    )
    parser.add_argument(
        "--trigger", "-t",
        help="Filter by trigger context (partial match)",
    )
    parser.add_argument(
        "--difficulty", "-d",
        choices=["beginner", "intermediate", "advanced"],
        help="Filter by difficulty level",
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List all categories with counts",
    )
    parser.add_argument(
        "--list-triggers",
        action="store_true",
        help="List all trigger contexts with counts",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show summary statistics",
    )
    parser.add_argument(
        "--brief", "-b",
        action="store_true",
        help="Brief output (hide description and application)",
    )
    parser.add_argument(
        "--csv-path",
        default=CSV_PATH,
        help=f"Path to models CSV (default: {CSV_PATH})",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    models = load_models(args.csv_path)

    # List/stats commands
    if args.list_categories:
        list_categories(models)
        return
    if args.list_triggers:
        list_triggers(models)
        return
    if args.stats:
        show_stats(models)
        return

    # No search criteria provided
    if not args.query and not args.category and not args.trigger and not args.difficulty:
        parser.print_help()
        return

    # Apply filters (combinable)
    results = models

    if args.query:
        results = keyword_search(results, args.query)
    if args.category:
        results = filter_by_field(results, "category", args.category)
    if args.trigger:
        results = filter_by_field(results, "trigger_context", args.trigger)
    if args.difficulty:
        results = filter_by_field(results, "difficulty", args.difficulty)

    # Build description of the query
    parts = []
    if args.query:
        parts.append(f'"{args.query}"')
    if args.category:
        parts.append(f'category="{args.category}"')
    if args.trigger:
        parts.append(f'trigger="{args.trigger}"')
    if args.difficulty:
        parts.append(f"difficulty={args.difficulty}")
    query_desc = " + ".join(parts)

    print_results(results, query_desc, verbose=not args.brief)


if __name__ == "__main__":
    main()
