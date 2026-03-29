"""
Platform-specific prompt formatters.

OpenArt  – supports a positive/negative pair plus optional parameter tags.
           Best results come from structured, comma-separated token chains.

Higgsfield – video/image generation focused on cinematic realism.
             Needs motion intent, camera movement cues, and aspect ratio hints
             baked into the prompt string itself.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .builder import BuiltPrompt


# ─────────────────────────────────────────────────────────────────────────────
# Shared output dataclass
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class FormattedPrompt:
    platform: str
    positive: str
    negative: str
    parameters: dict          # platform-specific key/value hints
    copy_paste: str           # ready-to-paste single string for that platform


# ─────────────────────────────────────────────────────────────────────────────
# OpenArt formatter
# ─────────────────────────────────────────────────────────────────────────────

# Recommended OpenArt realism models and their known best CFG / step combos
OPENART_MODEL_HINTS = {
    "portrait":     {"model": "Realistic Vision V6.0 B1", "cfg": 7,  "steps": 30, "sampler": "DPM++ 2M Karras"},
    "landscape":    {"model": "Juggernaut XL v9",          "cfg": 6,  "steps": 35, "sampler": "DPM++ 2M Karras"},
    "street":       {"model": "Realistic Vision V6.0 B1", "cfg": 7,  "steps": 30, "sampler": "Euler a"},
    "product":      {"model": "SDXL 1.0 base",            "cfg": 7,  "steps": 40, "sampler": "DPM++ 2S a Karras"},
    "architecture": {"model": "Juggernaut XL v9",          "cfg": 6,  "steps": 40, "sampler": "DPM++ 2M Karras"},
    "wildlife":     {"model": "Realistic Vision V6.0 B1", "cfg": 7,  "steps": 35, "sampler": "DPM++ 2M Karras"},
    "cinematic":    {"model": "CinematicKX",              "cfg": 8,  "steps": 35, "sampler": "DPM++ 2M Karras"},
}

OPENART_RESOLUTION = {
    "portrait":     (832, 1216),
    "landscape":    (1216, 832),
    "street":       (832, 1216),
    "product":      (1024, 1024),
    "architecture": (1216, 832),
    "wildlife":     (1216, 832),
    "cinematic":    (1280, 720),
}


def format_openart(prompt: BuiltPrompt) -> FormattedPrompt:
    """
    Format a BuiltPrompt for OpenArt's Stable Diffusion interface.
    Prepends quality anchor tokens that OpenArt's pipeline responds well to.
    """
    shot_type = prompt.config.shot_type
    hint = OPENART_MODEL_HINTS.get(shot_type, OPENART_MODEL_HINTS["portrait"])
    resolution = OPENART_RESOLUTION.get(shot_type, (1024, 1024))

    # Prepend anchor tokens – these sit at the high-attention start of the prompt
    anchor = "masterpiece, best quality, ultra-realistic, (photorealistic:1.4)"
    positive = f"{anchor}, {prompt.positive}"

    parameters = {
        "recommended_model":   hint["model"],
        "cfg_scale":           hint["cfg"],
        "sampling_steps":      hint["steps"],
        "sampler":             hint["sampler"],
        "width":               resolution[0],
        "height":              resolution[1],
        "hires_fix":           True,
        "hires_denoising":     0.45,
        "hires_upscale":       2.0,
        "clip_skip":           2,
    }

    copy_paste = (
        f"[POSITIVE]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n"
        + "\n".join(f"  {k}: {v}" for k, v in parameters.items())
    )

    return FormattedPrompt(
        platform="openart",
        positive=positive,
        negative=prompt.negative,
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Higgsfield formatter
# ─────────────────────────────────────────────────────────────────────────────

# Camera motion vocabulary Higgsfield responds to
HIGGSFIELD_CAMERA_MOVES = {
    "portrait":     "slow push-in, subtle camera drift",
    "landscape":    "slow pan right, parallax depth",
    "street":       "handheld slight shake, tracking shot",
    "product":      "gentle orbit, slow 360 rotation",
    "architecture": "slow crane up, tilt reveal",
    "wildlife":     "tracking shot, telephoto drift",
    "cinematic":    "dolly zoom, slow push-in",
}

HIGGSFIELD_DURATION_HINTS = {
    "portrait":     "4-6 seconds",
    "landscape":    "6-8 seconds",
    "street":       "4-6 seconds",
    "product":      "6-8 seconds",
    "architecture": "6-10 seconds",
    "wildlife":     "4-6 seconds",
    "cinematic":    "6-8 seconds",
}

HIGGSFIELD_ASPECT = {
    "portrait":     "9:16",
    "landscape":    "16:9",
    "street":       "9:16",
    "product":      "1:1",
    "architecture": "16:9",
    "wildlife":     "16:9",
    "cinematic":    "2.39:1",
}


def format_higgsfield(prompt: BuiltPrompt, motion: Optional[str] = None) -> FormattedPrompt:
    """
    Format a BuiltPrompt for Higgsfield AI's cinematic video/image pipeline.

    Higgsfield interprets everything from a single text prompt, so camera
    motion and temporal cues are embedded directly into the string.
    Negative prompts are also passed as a separate field in its UI.

    Parameters
    ----------
    prompt : BuiltPrompt
    motion : str, optional
        Override the camera motion description.
    """
    shot_type = prompt.config.shot_type
    camera_move = motion or HIGGSFIELD_CAMERA_MOVES.get(shot_type, "slow push-in")
    duration    = HIGGSFIELD_DURATION_HINTS.get(shot_type, "5 seconds")
    aspect      = HIGGSFIELD_ASPECT.get(shot_type, "16:9")

    # Higgsfield benefits from motion and temporal language prepended
    motion_prefix = (
        f"Cinematic {duration} video clip. "
        f"Camera: {camera_move}. "
    )
    positive = f"{motion_prefix}{prompt.positive}, cinematic motion, smooth movement, no camera shake"

    parameters = {
        "aspect_ratio":  aspect,
        "duration_hint": duration,
        "camera_motion": camera_move,
        "style":         "photorealistic",
        "motion_amount": "subtle",        # low = more realistic
    }

    copy_paste = (
        f"[PROMPT]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n"
        + "\n".join(f"  {k}: {v}" for k, v in parameters.items())
    )

    return FormattedPrompt(
        platform="higgsfield",
        positive=positive,
        negative=prompt.negative,
        parameters=parameters,
        copy_paste=copy_paste,
    )
