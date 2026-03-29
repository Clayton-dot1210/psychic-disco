#!/usr/bin/env python3
"""
Art Prompting Engine CLI
========================
Generate photorealism-optimised prompts for OpenArt and Higgsfield AI.

Usage examples
--------------
# Basic portrait for both platforms
python prompt_engine.py "a young woman in a coffee shop" --shot portrait

# Landscape shot, OpenArt only, randomise some modifiers
python prompt_engine.py "mountain range at sunrise" --shot landscape --platform openart --randomize

# Cinematic street scene with custom lighting override and motion
python prompt_engine.py "busy Tokyo street at night" --shot street --platform higgsfield \\
    --lighting "neon backlight" --motion "handheld tracking shot, shallow depth"

# Product shot with seed for reproducibility
python prompt_engine.py "luxury watch on marble surface" --shot product --seed 42

# List all available shot types
python prompt_engine.py --list-shots
"""
import argparse
import json
import sys
from textwrap import indent

from engine import PromptConfig, build, format_openart, format_higgsfield
from engine.modifiers import SHOT_PRESETS


SHOT_DESCRIPTIONS = {
    "portrait":     "Close-up or environmental human/animal portraits",
    "landscape":    "Wide scenic outdoor environments",
    "street":       "Candid street photography, urban life",
    "product":      "Commercial product photography",
    "architecture": "Buildings, interiors, urban structures",
    "wildlife":     "Animals in natural habitats, nature",
    "cinematic":    "Movie-style dramatic scenes with cinematic look",
}


def _print_formatted(fp, show_copy_paste: bool = True) -> None:
    """Pretty-print a FormattedPrompt to stdout."""
    bar = "─" * 70
    print(f"\n{'═' * 70}")
    print(f"  Platform : {fp.platform.upper()}")
    print(f"{'═' * 70}")
    print("\n[POSITIVE PROMPT]")
    print(indent(fp.positive, "  "))
    print("\n[NEGATIVE PROMPT]")
    print(indent(fp.negative, "  "))
    print(f"\n[RECOMMENDED SETTINGS]")
    for k, v in fp.parameters.items():
        print(f"  {k:<25} {v}")
    if show_copy_paste:
        print(f"\n{bar}")
        print("  COPY-PASTE READY:")
        print(bar)
        print(fp.copy_paste)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate photorealism prompts for OpenArt and Higgsfield AI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "subject",
        nargs="?",
        help="Subject description, e.g. 'a woman reading in a Parisian café'",
    )
    parser.add_argument(
        "--shot", "-s",
        default="portrait",
        choices=list(SHOT_PRESETS.keys()),
        metavar="SHOT_TYPE",
        help=f"Shot type preset. Choices: {', '.join(SHOT_PRESETS.keys())}  (default: portrait)",
    )
    parser.add_argument(
        "--platform", "-p",
        default="both",
        choices=["openart", "higgsfield", "both"],
        help="Target platform (default: both)",
    )
    parser.add_argument(
        "--lighting", "-l",
        default=None,
        help="Override lighting (e.g. 'golden hour lighting')",
    )
    parser.add_argument(
        "--camera",
        default=None,
        help="Override camera body (e.g. 'shot on Leica M11')",
    )
    parser.add_argument(
        "--lens",
        default=None,
        help="Override lens (e.g. '85mm f/1.4 prime lens')",
    )
    parser.add_argument(
        "--aperture",
        default=None,
        help="Override aperture (e.g. 'f/1.4 wide open')",
    )
    parser.add_argument(
        "--atmosphere",
        default=None,
        help="Add atmosphere token (e.g. 'morning mist')",
    )
    parser.add_argument(
        "--composition",
        default=None,
        help="Add composition token (e.g. 'rule of thirds')",
    )
    parser.add_argument(
        "--style",
        default=None,
        help="Free-text style rider appended to the prompt",
    )
    parser.add_argument(
        "--motion",
        default=None,
        help="[Higgsfield only] Camera motion override (e.g. 'slow dolly push-in')",
    )
    parser.add_argument(
        "--randomize", "-r",
        action="store_true",
        help="Randomise modifiers not locked by other flags",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Integer seed for reproducible randomisation",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output results as JSON instead of human-readable text",
    )
    parser.add_argument(
        "--list-shots",
        action="store_true",
        help="List all available shot type presets and exit",
    )

    args = parser.parse_args()

    # ── --list-shots ──────────────────────────────────────────────────────────
    if args.list_shots:
        print("\nAvailable shot types:\n")
        for name, desc in SHOT_DESCRIPTIONS.items():
            preset = SHOT_PRESETS[name]
            print(f"  {name:<15} {desc}")
            print(f"               Camera  : {preset['camera']}")
            print(f"               Lens    : {preset['lens']}")
            print(f"               Lighting: {preset['lighting']}")
            print()
        sys.exit(0)

    # ── Validate subject ──────────────────────────────────────────────────────
    if not args.subject:
        parser.error("A subject description is required. Use --list-shots to see presets.")

    # ── Build core prompt ─────────────────────────────────────────────────────
    config = PromptConfig(
        subject=args.subject,
        shot_type=args.shot,
        lighting=args.lighting,
        camera=args.camera,
        lens=args.lens,
        aperture=args.aperture,
        atmosphere=args.atmosphere,
        composition=args.composition,
        extra_style=args.style,
        randomize=args.randomize,
        seed=args.seed,
    )

    built = build(config)

    # ── Format per platform ───────────────────────────────────────────────────
    results = {}

    if args.platform in ("openart", "both"):
        results["openart"] = format_openart(built)

    if args.platform in ("higgsfield", "both"):
        results["higgsfield"] = format_higgsfield(built, motion=args.motion)

    # ── Output ────────────────────────────────────────────────────────────────
    if args.output_json:
        out = {}
        for name, fp in results.items():
            out[name] = {
                "positive":   fp.positive,
                "negative":   fp.negative,
                "parameters": fp.parameters,
            }
        print(json.dumps(out, indent=2))
    else:
        print(f"\nSubject  : {args.subject}")
        print(f"Shot type: {args.shot}")
        for fp in results.values():
            _print_formatted(fp)
        print()


if __name__ == "__main__":
    main()
