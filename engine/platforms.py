"""
Platform-specific prompt formatters.

OpenArt    – Stable Diffusion image generation. Positive/negative pair + settings.
Higgsfield – Cinematic video generation. Motion cues baked into prompt.
Runway     – Gen-3 video generation. Subject/style separation + motion direction.
Kling      – Realistic video generation. Prompt + motion mode + aspect ratio.
Pika       – Short-form video generation. Prompt + motion score + parameters.
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


# ─────────────────────────────────────────────────────────────────────────────
# Runway ML Gen-3 formatter
# ─────────────────────────────────────────────────────────────────────────────

RUNWAY_MOTION_PRESETS: dict[str, str] = {
    "portrait":        "camera slowly pushes in, subject holds still, subtle facial animation",
    "landscape":       "camera slowly pans right with parallax depth, environmental motion",
    "street":          "handheld camera slight drift, pedestrian movement in background",
    "product":         "camera slowly orbits product, gentle 360 rotation reveal",
    "architecture":    "camera tilts up to reveal full structure, slow crane",
    "wildlife":        "camera tracks subject movement, telephoto compression",
    "cinematic":       "slow dolly push-in, cinematic depth reveal",
    "talking_head":    "camera very subtly pushes in toward face, micro handheld drift",
    "techwear_street": "ultra-slow push-in toward subject, wet street reflection shimmer",
    "techwear_closeup":"imperceptible creep in, rain droplets on skin micro-movement",
    "techwear_wide":   "slow crane up from cobblestones to eye level, full reveal",
    "techwear_neon":   "slow drift into neon light, steam particle movement",
}

RUNWAY_ASPECT: dict[str, str] = {
    "portrait":     "768:1344",
    "landscape":    "1344:768",
    "street":       "768:1344",
    "product":      "1024:1024",
    "cinematic":    "1344:576",
    "talking_head": "768:1344",
    "techwear_street":  "768:1344",
    "techwear_closeup": "768:1344",
    "techwear_wide":    "768:1344",
    "techwear_neon":    "768:1344",
}


def format_runway(
    prompt: BuiltPrompt,
    motion: Optional[str] = None,
    duration_seconds: int = 5,
) -> FormattedPrompt:
    """
    Format a BuiltPrompt for Runway Gen-3 Alpha.

    Runway responds best to subject + action descriptions with motion direction
    stated upfront. Negative prompts go in a separate field.
    """
    shot_type = prompt.config.shot_type
    camera_motion = motion or RUNWAY_MOTION_PRESETS.get(shot_type, "slow subtle push-in")
    aspect = RUNWAY_ASPECT.get(shot_type, "768:1344")

    # Runway wants motion described as a fluid sentence, not token chains
    motion_direction = (
        f"{camera_motion}. "
        f"Photorealistic, cinematic quality, no camera shake unless handheld specified."
    )
    positive = f"{motion_direction} {prompt.positive}"

    parameters = {
        "aspect_ratio":       aspect,
        "duration_seconds":   duration_seconds,
        "camera_motion":      camera_motion,
        "style_preset":       "photorealistic",
        "seed":               prompt.config.seed or "random",
    }

    copy_paste = (
        f"[PROMPT]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n"
        + "\n".join(f"  {k}: {v}" for k, v in parameters.items())
    )

    return FormattedPrompt(
        platform="runway",
        positive=positive,
        negative=prompt.negative,
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Kling AI formatter
# ─────────────────────────────────────────────────────────────────────────────

KLING_MOTION_MODES: dict[str, str] = {
    "portrait":        "standard",
    "landscape":       "standard",
    "street":          "standard",
    "cinematic":       "pro",
    "talking_head":    "standard",
    "techwear_street": "pro",
    "techwear_closeup":"pro",
    "techwear_wide":   "pro",
    "techwear_neon":   "pro",
}

KLING_CAMERA_CONTROLS: dict[str, dict] = {
    "portrait":        {"type": "push_in",   "speed": 3},
    "landscape":       {"type": "pan_right",  "speed": 2},
    "street":          {"type": "handheld",   "speed": 4},
    "cinematic":       {"type": "dolly_zoom", "speed": 2},
    "talking_head":    {"type": "push_in",    "speed": 2},
    "techwear_street": {"type": "push_in",    "speed": 1},
    "techwear_closeup":{"type": "push_in",    "speed": 1},
    "techwear_wide":   {"type": "crane_up",   "speed": 2},
    "techwear_neon":   {"type": "push_in",    "speed": 2},
}


def format_kling(
    prompt: BuiltPrompt,
    motion: Optional[str] = None,
    duration_seconds: int = 5,
) -> FormattedPrompt:
    """
    Format a BuiltPrompt for Kling AI video generation.

    Kling has explicit camera control modes and a motion mode (standard/pro).
    Pro mode supports longer, more complex shots.
    """
    shot_type = prompt.config.shot_type
    motion_mode = KLING_MOTION_MODES.get(shot_type, "standard")
    camera_ctrl = KLING_CAMERA_CONTROLS.get(shot_type, {"type": "push_in", "speed": 2})

    positive = (
        f"Hyper-realistic cinematic video. {prompt.positive}, "
        f"photorealistic, film quality, no artifacts"
    )

    parameters = {
        "mode":               motion_mode,
        "duration":           f"{duration_seconds}s",
        "camera_type":        camera_ctrl["type"],
        "camera_speed":       camera_ctrl["speed"],
        "aspect_ratio":       "9:16" if shot_type in ("portrait", "talking_head", "techwear_street", "techwear_closeup", "techwear_wide", "techwear_neon") else "16:9",
        "cfg_scale":          0.5,
    }

    copy_paste = (
        f"[PROMPT]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n"
        + "\n".join(f"  {k}: {v}" for k, v in parameters.items())
    )

    return FormattedPrompt(
        platform="kling",
        positive=positive,
        negative=prompt.negative,
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Pika Labs formatter
# ─────────────────────────────────────────────────────────────────────────────

PIKA_CAMERA_MOVES: dict[str, str] = {
    "portrait":        "zoom in",
    "landscape":       "pan right",
    "street":          "move right",
    "cinematic":       "zoom in",
    "talking_head":    "zoom in",
    "techwear_street": "zoom in",
    "techwear_closeup":"zoom in",
    "techwear_wide":   "tilt up",
    "techwear_neon":   "zoom in",
}


def format_pika(
    prompt: BuiltPrompt,
    motion: Optional[str] = None,
    motion_strength: int = 1,
) -> FormattedPrompt:
    """
    Format a BuiltPrompt for Pika Labs video generation.

    Pika uses a simple prompt + camera motion command + motion strength (1-4).
    Low motion strength (1-2) is most realistic.
    """
    shot_type = prompt.config.shot_type
    camera_move = motion or PIKA_CAMERA_MOVES.get(shot_type, "zoom in")

    positive = (
        f"{prompt.positive}, photorealistic, high quality, cinematic"
    )

    parameters = {
        "camera_motion":   camera_move,
        "motion_strength": motion_strength,
        "aspect_ratio":    "9:16" if shot_type in ("portrait", "street", "talking_head", "techwear_street", "techwear_closeup", "techwear_wide", "techwear_neon") else "16:9",
        "fps":             24,
        "quality":         "1080p",
    }

    copy_paste = (
        f"[PROMPT]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n"
        + "\n".join(f"  {k}: {v}" for k, v in parameters.items())
    )

    return FormattedPrompt(
        platform="pika",
        positive=positive,
        negative=prompt.negative,
        parameters=parameters,
        copy_paste=copy_paste,
    )
