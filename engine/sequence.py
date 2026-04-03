"""
Multi-shot video sequence builder.

Builds complete video sequences structured as Hook → Body → CTA.
Sequences are designed for UGC short-form platforms (TikTok, Reels, Shorts)
and can be built around a specific character and hook template.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .builder import PromptConfig, BuiltPrompt, build


@dataclass
class Shot:
    """A single shot within a video sequence."""

    shot_number: int
    label: str              # e.g. "HOOK", "BODY_1", "CTA"
    prompt: BuiltPrompt
    duration_hint: str      # e.g. "2-3 seconds"
    motion_cue: str         # camera motion descriptor for video platforms
    aspect_ratio: str       # e.g. "9:16"
    notes: str              # director notes / intention for this beat


@dataclass
class VideoSequence:
    """A complete multi-shot video sequence ready for generation."""

    title: str
    sequence_type: str
    total_duration: str
    platform_target: str
    shots: list[Shot]
    character_name: Optional[str] = None


@dataclass
class SequenceConfig:
    """All parameters for building a video sequence."""

    concept: str                                # Core content/topic
    character_key: Optional[str] = None         # Key into characters.CHARACTERS
    hook_key: Optional[str] = None              # Key into hooks.HOOK_TEMPLATES
    sequence_type: str = "ugc_standard"         # See SEQUENCE_STRUCTURES below
    platform_target: str = "tiktok"             # tiktok, reels, youtube_shorts
    product_name: Optional[str] = None          # For product-focused sequences
    seed: Optional[int] = None


# ── Sequence structure blueprints ─────────────────────────────────────────────

SEQUENCE_STRUCTURES: dict[str, list[dict]] = {

    "ugc_standard": [
        {
            "label": "HOOK",
            "shot": "talking_head",
            "duration": "1-2 seconds",
            "role": "Grab attention — stop the scroll",
        },
        {
            "label": "BODY_1",
            "shot": "lifestyle",
            "duration": "3-5 seconds",
            "role": "Establish context and build credibility",
        },
        {
            "label": "BODY_2",
            "shot": "talking_head",
            "duration": "3-5 seconds",
            "role": "Deliver the core message or value",
        },
        {
            "label": "CTA",
            "shot": "talking_head",
            "duration": "2-3 seconds",
            "role": "Clear call to action — link, follow, comment",
        },
    ],

    "product_demo": [
        {
            "label": "HOOK",
            "shot": "reaction",
            "duration": "1-2 seconds",
            "role": "Reaction hook — show the wow moment",
        },
        {
            "label": "INTRO",
            "shot": "talking_head",
            "duration": "2-3 seconds",
            "role": "Introduce the product and bold claim",
        },
        {
            "label": "DEMO",
            "shot": "unboxing",
            "duration": "4-6 seconds",
            "role": "Show the product in action",
        },
        {
            "label": "PROOF",
            "shot": "talking_head",
            "duration": "2-3 seconds",
            "role": "Social proof / real results",
        },
        {
            "label": "CTA",
            "shot": "talking_head",
            "duration": "1-2 seconds",
            "role": "Link in bio / buy now",
        },
    ],

    "story_arc": [
        {
            "label": "SETUP",
            "shot": "lifestyle",
            "duration": "2-3 seconds",
            "role": "Show the before / the problem",
        },
        {
            "label": "CONFLICT",
            "shot": "reaction",
            "duration": "2-3 seconds",
            "role": "The struggle / relatable pain point",
        },
        {
            "label": "TURNING_POINT",
            "shot": "transformation",
            "duration": "3-4 seconds",
            "role": "The discovery / solution moment",
        },
        {
            "label": "RESOLUTION",
            "shot": "talking_head",
            "duration": "3-4 seconds",
            "role": "The result / transformation achieved",
        },
        {
            "label": "CTA",
            "shot": "talking_head",
            "duration": "1-2 seconds",
            "role": "How the viewer gets the same result",
        },
    ],

    # ── Character 28 techwear sequences ───────────────────────────────────────

    "techwear_promo": [
        {
            "label": "HOOK",
            "shot": "techwear_street",
            "duration": "2-3 seconds",
            "role": "Crane-up reveal on wet street — silent and commanding",
        },
        {
            "label": "DETAIL_1",
            "shot": "techwear_closeup",
            "duration": "3-4 seconds",
            "role": "Extreme close-up — face, texture, rain on jacket",
        },
        {
            "label": "WIDE",
            "shot": "techwear_wide",
            "duration": "4-5 seconds",
            "role": "Full body centered — environment scale and presence",
        },
        {
            "label": "ATMOSPHERE",
            "shot": "techwear_neon",
            "duration": "4-5 seconds",
            "role": "Neon atmosphere variant — mood and world-building",
        },
        {
            "label": "CLOSE_OUT",
            "shot": "techwear_closeup",
            "duration": "2-3 seconds",
            "role": "Final close-up stare — brand lock-in moment",
        },
    ],

    "techwear_hook_only": [
        {
            "label": "HOOK",
            "shot": "techwear_street",
            "duration": "1-2 seconds",
            "role": "Instant stop-the-scroll opening frame",
        },
        {
            "label": "REVEAL",
            "shot": "techwear_closeup",
            "duration": "2-3 seconds",
            "role": "Face reveal — identity lock-in",
        },
    ],
}

# Default motion cues by UGC shot type
_DEFAULT_MOTION: dict[str, str] = {
    "talking_head":    "slow subtle push-in, handheld micro-drift",
    "lifestyle":       "gentle tracking follow, environmental pan",
    "reaction":        "handheld responsive reframe",
    "unboxing":        "slow reveal push-in, product focus pull",
    "transformation":  "dramatic crane up, reveal push-in",
    "pov":             "immersive handheld drift, POV slight motion",
    "techwear_street": "slow deliberate push-in",
    "techwear_closeup":"ultra-slow push-in, almost imperceptible",
    "techwear_wide":   "slow crane up, full body reveal",
    "techwear_neon":   "slow atmospheric push-in, steam drift",
}

_DEFAULT_ASPECT: dict[str, str] = {
    "tiktok":          "9:16",
    "reels":           "9:16",
    "youtube_shorts":  "9:16",
    "youtube":         "16:9",
    "cinematic":       "2.39:1",
}


def build_sequence(config: SequenceConfig) -> VideoSequence:
    """
    Build a complete multi-shot video sequence.

    Each shot is assembled as a full BuiltPrompt with character context,
    hook language, and UGC aesthetic tokens injected as appropriate.
    """
    from .characters import get_character
    from .hooks import get_hook
    from .ugc_modifiers import UGC_SHOT_PRESETS, NEGATIVE_UGC, NEGATIVE_TECHWEAR
    from .modifiers import SHOT_PRESETS, NEGATIVE_REALISM

    character = get_character(config.character_key) if config.character_key else None
    hook_tmpl = get_hook(config.hook_key) if config.hook_key else None
    structure = SEQUENCE_STRUCTURES.get(config.sequence_type, SEQUENCE_STRUCTURES["ugc_standard"])
    aspect = _DEFAULT_ASPECT.get(config.platform_target, "9:16")

    # Techwear sequences use the techwear negative
    is_techwear = config.sequence_type in ("techwear_promo", "techwear_hook_only")
    default_negative = NEGATIVE_TECHWEAR if is_techwear else NEGATIVE_UGC

    shots: list[Shot] = []

    for i, beat in enumerate(structure):
        shot_type = beat["shot"]

        # ── Build subject string ──────────────────────────────────────────────
        subject_parts: list[str] = []

        if character:
            subject_parts.append(character.to_subject_prefix())

        subject_parts.append(config.concept)

        if config.product_name and beat["label"] in ("DEMO", "INTRO", "PROOF"):
            subject_parts.append(f"featuring {config.product_name}")

        subject = ", ".join(p for p in subject_parts if p)

        # Inject hook prefix on the HOOK beat
        if beat["label"] == "HOOK" and hook_tmpl:
            subject = hook_tmpl.prompt_prefix + subject

        # ── Resolve preset tokens ─────────────────────────────────────────────
        if shot_type in UGC_SHOT_PRESETS:
            ugc_preset = UGC_SHOT_PRESETS[shot_type]
            negative = default_negative
            extra_tokens = ", ".join(
                ugc_preset.get("quality", []) + ugc_preset.get("post", [])
            )
            camera_tokens = (
                f"{ugc_preset['camera']}, {ugc_preset['lens']}, "
                f"{ugc_preset['aperture']}, {ugc_preset['lighting']}, "
                f"{ugc_preset['dof']}"
            )
            motion = (
                hook_tmpl.motion_cue
                if beat["label"] == "HOOK" and hook_tmpl
                else ugc_preset.get("motion_cue", _DEFAULT_MOTION.get(shot_type, "slow push-in"))
            )
            beat_aspect = ugc_preset.get("aspect", aspect)
        else:
            # Fall back to standard shot presets for non-UGC shots
            ugc_preset = None
            negative = NEGATIVE_REALISM
            extra_tokens = ""
            camera_tokens = ""
            motion = _DEFAULT_MOTION.get(shot_type, "slow push-in")
            beat_aspect = aspect

        # ── Assemble via builder ──────────────────────────────────────────────
        std_shot = shot_type if shot_type in SHOT_PRESETS else "portrait"
        prompt_config = PromptConfig(
            subject=subject,
            shot_type=std_shot,
            seed=(config.seed + i) if config.seed is not None else None,
        )
        built = build(prompt_config)

        # Extend positive with UGC/techwear tokens
        positive_parts = [built.positive]
        if camera_tokens:
            positive_parts.append(camera_tokens)
        if extra_tokens:
            positive_parts.append(extra_tokens)

        built = BuiltPrompt(
            positive=", ".join(p for p in positive_parts if p),
            negative=negative,
            config=built.config,
        )

        shots.append(Shot(
            shot_number=i + 1,
            label=beat["label"],
            prompt=built,
            duration_hint=beat["duration"],
            motion_cue=motion,
            aspect_ratio=beat_aspect,
            notes=beat["role"],
        ))

    # Estimate total duration
    min_s = sum(int(b["duration"].split("-")[0]) for b in structure)
    max_s = sum(int(b["duration"].split("-")[1].split()[0]) for b in structure)

    return VideoSequence(
        title=f"{config.sequence_type.replace('_', ' ').title()} — {config.concept[:50]}",
        sequence_type=config.sequence_type,
        total_duration=f"{min_s}-{max_s} seconds",
        platform_target=config.platform_target,
        shots=shots,
        character_name=character.name if character else None,
    )
