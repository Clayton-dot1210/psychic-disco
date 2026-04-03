#!/usr/bin/env python3
"""
UGC Video Promotion Engine
===========================
Generate highest-quality AI realistic video prompts for UGC content,
visual hooks, and AI content character promotion.

Supports: Higgsfield · Runway Gen-3 · Kling AI · Pika Labs · OpenArt

Usage examples
--------------
# Single techwear street shot for Character 28
python ugc_engine.py "standing in the rain" --character character_28 --shot techwear_street

# Build a full techwear promo sequence
python ugc_engine.py "Arc'teryx techwear urban explorer" \\
    --character character_28 --sequence techwear_promo --platform kling

# Hook only — silent stare, all video platforms
python ugc_engine.py "lone figure in rain" \\
    --character character_28 --hook silent_stare

# UGC standard sequence with hook for TikTok
python ugc_engine.py "why I switched to techwear" \\
    --character character_28 --sequence ugc_standard --hook bold_claim \\
    --platform-target tiktok

# List everything available
python ugc_engine.py --list-characters
python ugc_engine.py --list-hooks
python ugc_engine.py --list-sequences
python ugc_engine.py --list-shots

# JSON output for scripting
python ugc_engine.py "urban street scene" --character character_28 --json
"""
from __future__ import annotations

import argparse
import json
import sys
from textwrap import indent

from engine import (
    PromptConfig, build,
    format_higgsfield, format_runway, format_kling, format_pika, format_openart,
    FormattedPrompt,
    get_character, list_characters,
    get_hook, list_hooks,
    SequenceConfig, build_sequence, SEQUENCE_STRUCTURES,
)
from engine.ugc_modifiers import UGC_SHOT_PRESETS
from engine.modifiers import SHOT_PRESETS

ALL_SHOT_PRESETS = {**SHOT_PRESETS, **UGC_SHOT_PRESETS}

VIDEO_PLATFORMS = ["higgsfield", "runway", "kling", "pika", "openart", "all"]


# ─────────────────────────────────────────────────────────────────────────────
# Formatting helpers
# ─────────────────────────────────────────────────────────────────────────────

def _bar(char: str = "─", width: int = 72) -> str:
    return char * width


def _print_shot(fp: FormattedPrompt) -> None:
    """Pretty-print a single FormattedPrompt."""
    print(f"\n{'═' * 72}")
    print(f"  Platform : {fp.platform.upper()}")
    print(f"{'═' * 72}")
    print("\n[POSITIVE PROMPT]")
    print(indent(fp.positive, "  "))
    print("\n[NEGATIVE PROMPT]")
    print(indent(fp.negative, "  "))
    print("\n[SETTINGS]")
    for k, v in fp.parameters.items():
        print(f"  {k:<28} {v}")
    print(f"\n{_bar()}")
    print("  COPY-PASTE READY:")
    print(_bar())
    print(fp.copy_paste)


def _print_sequence(seq, show_copy_paste: bool = True) -> None:
    """Pretty-print a VideoSequence."""
    print(f"\n{'█' * 72}")
    print(f"  SEQUENCE  : {seq.title}")
    print(f"  Type      : {seq.sequence_type}")
    print(f"  Character : {seq.character_name or 'none'}")
    print(f"  Platform  : {seq.platform_target.upper()}")
    print(f"  Duration  : {seq.total_duration}")
    print(f"  Shots     : {len(seq.shots)}")
    print(f"{'█' * 72}")

    for shot in seq.shots:
        print(f"\n{'─' * 72}")
        print(f"  SHOT {shot.shot_number}  [{shot.label}]  ·  {shot.duration_hint}  ·  {shot.aspect_ratio}")
        print(f"  Notes   : {shot.notes}")
        print(f"  Motion  : {shot.motion_cue}")
        print(f"{'─' * 72}")
        print("\n  POSITIVE:")
        print(indent(shot.prompt.positive, "    "))
        print("\n  NEGATIVE:")
        print(indent(shot.prompt.negative, "    "))
        if show_copy_paste:
            print(f"\n  COPY-PASTE:")
            print(indent(shot.prompt.positive, "    "))
    print(f"\n{'█' * 72}\n")


def _sequence_to_dict(seq) -> dict:
    return {
        "title": seq.title,
        "sequence_type": seq.sequence_type,
        "character": seq.character_name,
        "platform": seq.platform_target,
        "total_duration": seq.total_duration,
        "shots": [
            {
                "shot_number": s.shot_number,
                "label": s.label,
                "duration_hint": s.duration_hint,
                "motion_cue": s.motion_cue,
                "aspect_ratio": s.aspect_ratio,
                "notes": s.notes,
                "positive": s.prompt.positive,
                "negative": s.prompt.negative,
            }
            for s in seq.shots
        ],
    }


def _format_for_platform(built, platform: str, motion: str | None) -> list[FormattedPrompt]:
    results: list[FormattedPrompt] = []
    if platform in ("higgsfield", "all"):
        results.append(format_higgsfield(built, motion=motion))
    if platform in ("runway", "all"):
        results.append(format_runway(built, motion=motion))
    if platform in ("kling", "all"):
        results.append(format_kling(built, motion=motion))
    if platform in ("pika", "all"):
        results.append(format_pika(built))
    if platform in ("openart", "all"):
        results.append(format_openart(built))
    return results


# ─────────────────────────────────────────────────────────────────────────────
# --list helpers
# ─────────────────────────────────────────────────────────────────────────────

def _list_characters() -> None:
    chars = list_characters()
    print(f"\n{'═' * 72}")
    print("  AVAILABLE CHARACTERS")
    print(f"{'═' * 72}\n")
    for key, c in chars.items():
        print(f"  {key:<22}  {c.name}")
        print(f"  {'':22}  Age: {c.age_range}  |  {c.style}")
        env = c.primary_environment()
        if env:
            print(f"  {'':22}  Default env: {env}")
        print()


def _list_hooks() -> None:
    hooks = list_hooks()
    print(f"\n{'═' * 72}")
    print("  AVAILABLE HOOK TEMPLATES")
    print(f"{'═' * 72}\n")
    for key, h in hooks.items():
        print(f"  {key:<22}  {h.name}")
        print(f"  {'':22}  {h.description}")
        print(f"  {'':22}  Duration: {h.duration_hint}  |  Tone: {h.emotion_tone}")
        print()


def _list_sequences() -> None:
    print(f"\n{'═' * 72}")
    print("  AVAILABLE SEQUENCE TYPES")
    print(f"{'═' * 72}\n")
    descriptions = {
        "ugc_standard":       "Hook → Body x2 → CTA  (4 shots, general UGC)",
        "product_demo":       "Hook → Intro → Demo → Proof → CTA  (5 shots, product)",
        "story_arc":          "Setup → Conflict → Turning Point → Resolution → CTA  (5 shots)",
        "techwear_promo":     "Hook → Detail → Wide → Atmosphere → Close-out  (5 shots, Character 28)",
        "techwear_hook_only": "Hook → Reveal  (2 shots, quick Character 28 hook)",
    }
    for key, desc in descriptions.items():
        beats = SEQUENCE_STRUCTURES[key]
        print(f"  {key:<22}  {desc}")
        print(f"  {'':22}  Shots: {', '.join(b['label'] for b in beats)}")
        print()


def _list_shots() -> None:
    print(f"\n{'═' * 72}")
    print("  AVAILABLE SHOT PRESETS")
    print(f"{'═' * 72}\n")
    print("  [Standard shots]")
    for key, preset in SHOT_PRESETS.items():
        print(f"  {key:<22}  {preset['camera']}  ·  {preset['lighting']}")
    print()
    print("  [UGC / Techwear shots]")
    for key, preset in UGC_SHOT_PRESETS.items():
        desc = preset.get("description", "")
        print(f"  {key:<22}  {desc}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Main CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="UGC Video Promotion Engine — AI realistic video prompt generator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "subject",
        nargs="?",
        help="Subject or concept, e.g. 'standing in rain' or 'why I switched to techwear'",
    )

    # ── Character & hook ──────────────────────────────────────────────────────
    parser.add_argument(
        "--character", "-c",
        default=None,
        metavar="CHARACTER_KEY",
        help="Character archetype key (e.g. character_28, creator, expert)",
    )
    parser.add_argument(
        "--hook",
        default=None,
        metavar="HOOK_KEY",
        help="Visual hook template (e.g. silent_stare, bold_claim, urban_reveal)",
    )

    # ── Shot type ─────────────────────────────────────────────────────────────
    parser.add_argument(
        "--shot", "-s",
        default="techwear_street",
        metavar="SHOT_TYPE",
        help=f"Shot type preset. Use --list-shots to see all options. (default: techwear_street)",
    )

    # ── Sequence mode ─────────────────────────────────────────────────────────
    parser.add_argument(
        "--sequence",
        default=None,
        metavar="SEQUENCE_TYPE",
        help="Build a full multi-shot sequence (e.g. techwear_promo, ugc_standard)",
    )
    parser.add_argument(
        "--platform-target",
        default="tiktok",
        choices=["tiktok", "reels", "youtube_shorts", "youtube", "cinematic"],
        help="Target social platform for sequences (default: tiktok)",
    )

    # ── Video platform output ─────────────────────────────────────────────────
    parser.add_argument(
        "--platform", "-p",
        default="all",
        choices=VIDEO_PLATFORMS,
        help="Output platform(s) for single-shot mode (default: all)",
    )

    # ── Manual overrides ──────────────────────────────────────────────────────
    parser.add_argument("--lighting",     default=None, help="Override lighting token")
    parser.add_argument("--camera",       default=None, help="Override camera body token")
    parser.add_argument("--lens",         default=None, help="Override lens token")
    parser.add_argument("--aperture",     default=None, help="Override aperture token")
    parser.add_argument("--atmosphere",   default=None, help="Add atmosphere token")
    parser.add_argument("--composition",  default=None, help="Add composition token")
    parser.add_argument("--style",        default=None, help="Free-text style rider")
    parser.add_argument(
        "--motion",
        default=None,
        help="Camera motion override for video platforms",
    )

    # ── Randomisation ─────────────────────────────────────────────────────────
    parser.add_argument(
        "--randomize", "-r",
        action="store_true",
        help="Randomise modifiers not locked by flags",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed for reproducible randomisation",
    )

    # ── Output format ─────────────────────────────────────────────────────────
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output as JSON instead of formatted text",
    )

    # ── List commands ─────────────────────────────────────────────────────────
    parser.add_argument("--list-characters", action="store_true", help="List all character profiles")
    parser.add_argument("--list-hooks",      action="store_true", help="List all hook templates")
    parser.add_argument("--list-sequences",  action="store_true", help="List all sequence types")
    parser.add_argument("--list-shots",      action="store_true", help="List all shot presets")

    args = parser.parse_args()

    # ── List commands (exit after) ────────────────────────────────────────────
    if args.list_characters:
        _list_characters()
        sys.exit(0)
    if args.list_hooks:
        _list_hooks()
        sys.exit(0)
    if args.list_sequences:
        _list_sequences()
        sys.exit(0)
    if args.list_shots:
        _list_shots()
        sys.exit(0)

    if not args.subject:
        parser.error("A subject/concept is required. Use --list-* flags to explore options.")

    # ── Validate character & hook ──────────────────────────────────────────────
    character = None
    if args.character:
        character = get_character(args.character)
        if character is None:
            parser.error(
                f"Unknown character '{args.character}'. "
                f"Use --list-characters to see available options."
            )

    hook_tmpl = None
    if args.hook:
        hook_tmpl = get_hook(args.hook)
        if hook_tmpl is None:
            parser.error(
                f"Unknown hook '{args.hook}'. "
                f"Use --list-hooks to see available options."
            )

    # ── Sequence mode ─────────────────────────────────────────────────────────
    if args.sequence:
        if args.sequence not in SEQUENCE_STRUCTURES:
            parser.error(
                f"Unknown sequence '{args.sequence}'. "
                f"Use --list-sequences to see available options."
            )
        seq_config = SequenceConfig(
            concept=args.subject,
            character_key=args.character,
            hook_key=args.hook,
            sequence_type=args.sequence,
            platform_target=args.platform_target,
            seed=args.seed,
        )
        seq = build_sequence(seq_config)

        if args.output_json:
            print(json.dumps(_sequence_to_dict(seq), indent=2))
        else:
            _print_sequence(seq)
        return

    # ── Single-shot mode ──────────────────────────────────────────────────────

    # Build subject: inject character prefix + optional hook prefix
    subject_parts: list[str] = []
    if character:
        subject_parts.append(character.to_subject_prefix())
    subject_parts.append(args.subject)
    subject = ", ".join(subject_parts)

    if hook_tmpl:
        subject = hook_tmpl.prompt_prefix + subject

    # Resolve shot type — UGC presets override to portrait for PromptConfig
    shot_type = args.shot
    from engine.modifiers import SHOT_PRESETS as STD_PRESETS
    std_shot = shot_type if shot_type in STD_PRESETS else "portrait"

    config = PromptConfig(
        subject=subject,
        shot_type=std_shot,
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

    # Inject UGC preset tokens if shot_type is a UGC preset
    if shot_type in UGC_SHOT_PRESETS:
        from engine.ugc_modifiers import UGC_SHOT_PRESETS as UGC_P, NEGATIVE_TECHWEAR, NEGATIVE_UGC
        from engine.builder import BuiltPrompt
        ugc = UGC_P[shot_type]
        extra = ", ".join(ugc.get("quality", []) + ugc.get("post", []))
        camera_tok = f"{ugc['camera']}, {ugc['lens']}, {ugc['aperture']}, {ugc['lighting']}, {ugc['dof']}"
        negative = NEGATIVE_TECHWEAR if "techwear" in shot_type else NEGATIVE_UGC
        built = BuiltPrompt(
            positive=f"{built.positive}, {camera_tok}, {extra}",
            negative=negative,
            config=built.config,
        )

    # Format per platform
    results = _format_for_platform(built, args.platform, args.motion)

    if args.output_json:
        out = {}
        for fp in results:
            out[fp.platform] = {
                "positive":   fp.positive,
                "negative":   fp.negative,
                "parameters": fp.parameters,
            }
        print(json.dumps(out, indent=2))
    else:
        char_label = f"{character.name} ({args.character})" if character else "none"
        hook_label = f"{hook_tmpl.name} ({args.hook})" if hook_tmpl else "none"
        print(f"\nSubject   : {args.subject}")
        print(f"Character : {char_label}")
        print(f"Hook      : {hook_label}")
        print(f"Shot      : {shot_type}")
        for fp in results:
            _print_shot(fp)
        print()


if __name__ == "__main__":
    main()
