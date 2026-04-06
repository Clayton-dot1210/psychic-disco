"""
Platform-specific prompt formatters.

Supported platforms:
  - openart      — Stable Diffusion (OpenArt UI)
  - higgsfield   — Cinematic video/image AI
  - midjourney   — MidJourney v6 /imagine format
  - runway       — Runway Gen-3 Alpha / Gen-3 Turbo
  - pika         — Pika 2.0 video generation
  - leonardo     — Leonardo AI Phoenix / Diffusion XL
  - kling        — Kling 2.0 video generation
  - dalle3       — DALL-E 3 natural language format
  - firefly      — Adobe Firefly generative fill / text-to-image
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
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _settings_block(parameters: dict) -> str:
    return "\n".join(f"  {k}: {v}" for k, v in parameters.items())


# ─────────────────────────────────────────────────────────────────────────────
# OpenArt formatter
# ─────────────────────────────────────────────────────────────────────────────

OPENART_MODEL_HINTS = {
    "portrait":      {"model": "Realistic Vision V6.0 B1", "cfg": 7,  "steps": 30, "sampler": "DPM++ 2M Karras"},
    "landscape":     {"model": "Juggernaut XL v9",          "cfg": 6,  "steps": 35, "sampler": "DPM++ 2M Karras"},
    "street":        {"model": "Realistic Vision V6.0 B1", "cfg": 7,  "steps": 30, "sampler": "Euler a"},
    "product":       {"model": "SDXL 1.0 base",            "cfg": 7,  "steps": 40, "sampler": "DPM++ 2S a Karras"},
    "architecture":  {"model": "Juggernaut XL v9",          "cfg": 6,  "steps": 40, "sampler": "DPM++ 2M Karras"},
    "wildlife":      {"model": "Realistic Vision V6.0 B1", "cfg": 7,  "steps": 35, "sampler": "DPM++ 2M Karras"},
    "cinematic":     {"model": "CinematicKX",              "cfg": 8,  "steps": 35, "sampler": "DPM++ 2M Karras"},
    "lifestyle":     {"model": "Realistic Vision V6.0 B1", "cfg": 7,  "steps": 30, "sampler": "DPM++ 2M Karras"},
    "fashion":       {"model": "Juggernaut XL v9",          "cfg": 7,  "steps": 35, "sampler": "DPM++ 2M Karras"},
    "beauty":        {"model": "Realistic Vision V6.0 B1", "cfg": 7,  "steps": 35, "sampler": "DPM++ 2S a Karras"},
    "food":          {"model": "SDXL 1.0 base",            "cfg": 6,  "steps": 35, "sampler": "DPM++ 2M Karras"},
    "travel":        {"model": "Juggernaut XL v9",          "cfg": 6,  "steps": 35, "sampler": "DPM++ 2M Karras"},
    "fitness":       {"model": "Realistic Vision V6.0 B1", "cfg": 7,  "steps": 30, "sampler": "Euler a"},
    "social_story":  {"model": "Realistic Vision V6.0 B1", "cfg": 7,  "steps": 30, "sampler": "DPM++ 2M Karras"},
    "editorial":     {"model": "Juggernaut XL v9",          "cfg": 7,  "steps": 40, "sampler": "DPM++ 2M Karras"},
}

OPENART_RESOLUTION = {
    "portrait":      (832, 1216),
    "landscape":     (1216, 832),
    "street":        (832, 1216),
    "product":       (1024, 1024),
    "architecture":  (1216, 832),
    "wildlife":      (1216, 832),
    "cinematic":     (1280, 720),
    "lifestyle":     (864, 1080),
    "fashion":       (864, 1080),
    "beauty":        (1024, 1024),
    "food":          (1024, 1024),
    "travel":        (1216, 832),
    "fitness":       (864, 1080),
    "social_story":  (720, 1280),
    "editorial":     (864, 1080),
}


def format_openart(prompt: BuiltPrompt) -> FormattedPrompt:
    shot_type = prompt.config.shot_type
    hint = OPENART_MODEL_HINTS.get(shot_type, OPENART_MODEL_HINTS["portrait"])
    resolution = OPENART_RESOLUTION.get(shot_type, (1024, 1024))

    anchor = "masterpiece, best quality, ultra-realistic, (photorealistic:1.4)"
    positive = f"{anchor}, {prompt.positive}"

    parameters = {
        "recommended_model": hint["model"],
        "cfg_scale":         hint["cfg"],
        "sampling_steps":    hint["steps"],
        "sampler":           hint["sampler"],
        "width":             resolution[0],
        "height":            resolution[1],
        "hires_fix":         True,
        "hires_denoising":   0.45,
        "hires_upscale":     2.0,
        "clip_skip":         2,
    }

    copy_paste = (
        f"[POSITIVE]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n{_settings_block(parameters)}"
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

HIGGSFIELD_CAMERA_MOVES = {
    "portrait":     "slow push-in, subtle camera drift",
    "landscape":    "slow pan right, parallax depth",
    "street":       "handheld slight shake, tracking shot",
    "product":      "gentle orbit, slow 360 rotation",
    "architecture": "slow crane up, tilt reveal",
    "wildlife":     "tracking shot, telephoto drift",
    "cinematic":    "dolly zoom, slow push-in",
    "lifestyle":    "handheld candid drift, natural movement",
    "fashion":      "slow elegant pan, model walk tracking",
    "beauty":       "slow push-in to face, subtle breathing motion",
    "food":         "slow overhead crane, steam particle movement",
    "travel":       "slow sweeping pan, environmental reveal",
    "fitness":      "dynamic tracking shot, slow motion impact",
    "social_story": "handheld intimate, slight stabilized drift",
    "editorial":    "slow dolly reveal, editorial pace",
}

HIGGSFIELD_DURATION_HINTS = {
    "portrait":     "4-6 seconds",
    "landscape":    "6-8 seconds",
    "street":       "4-6 seconds",
    "product":      "6-8 seconds",
    "architecture": "6-10 seconds",
    "wildlife":     "4-6 seconds",
    "cinematic":    "6-8 seconds",
    "lifestyle":    "5-8 seconds",
    "fashion":      "6-8 seconds",
    "beauty":       "4-6 seconds",
    "food":         "5-7 seconds",
    "travel":       "6-10 seconds",
    "fitness":      "4-6 seconds",
    "social_story": "5-8 seconds",
    "editorial":    "6-8 seconds",
}

HIGGSFIELD_ASPECT = {
    "portrait":     "9:16",
    "landscape":    "16:9",
    "street":       "9:16",
    "product":      "1:1",
    "architecture": "16:9",
    "wildlife":     "16:9",
    "cinematic":    "2.39:1",
    "lifestyle":    "4:5",
    "fashion":      "4:5",
    "beauty":       "1:1",
    "food":         "1:1",
    "travel":       "16:9",
    "fitness":      "4:5",
    "social_story": "9:16",
    "editorial":    "4:5",
}


def format_higgsfield(prompt: BuiltPrompt, motion: Optional[str] = None) -> FormattedPrompt:
    shot_type = prompt.config.shot_type
    camera_move = motion or HIGGSFIELD_CAMERA_MOVES.get(shot_type, "slow push-in")
    duration    = HIGGSFIELD_DURATION_HINTS.get(shot_type, "5 seconds")
    aspect      = HIGGSFIELD_ASPECT.get(shot_type, "16:9")

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
        "motion_amount": "subtle",
    }

    copy_paste = (
        f"[PROMPT]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n{_settings_block(parameters)}"
    )

    return FormattedPrompt(
        platform="higgsfield",
        positive=positive,
        negative=prompt.negative,
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# MidJourney formatter (v6)
# ─────────────────────────────────────────────────────────────────────────────

MJ_ASPECT_RATIOS = {
    "portrait":     "3:4",
    "landscape":    "16:9",
    "street":       "3:4",
    "product":      "1:1",
    "architecture": "16:9",
    "wildlife":     "16:9",
    "cinematic":    "21:9",
    "lifestyle":    "4:5",
    "fashion":      "3:4",
    "beauty":       "1:1",
    "food":         "1:1",
    "travel":       "16:9",
    "fitness":      "4:5",
    "social_story": "9:16",
    "editorial":    "3:4",
}

MJ_STYLE_PARAMS = {
    "portrait":     "--style raw --stylize 750",
    "landscape":    "--style raw --stylize 500",
    "street":       "--style raw --stylize 600",
    "product":      "--style raw --stylize 400",
    "architecture": "--style raw --stylize 500",
    "wildlife":     "--style raw --stylize 700",
    "cinematic":    "--style cinematic --stylize 850",
    "lifestyle":    "--style raw --stylize 600",
    "fashion":      "--style raw --stylize 800",
    "beauty":       "--style raw --stylize 700",
    "food":         "--style raw --stylize 400",
    "travel":       "--style raw --stylize 650",
    "fitness":      "--style raw --stylize 600",
    "social_story": "--style raw --stylize 550",
    "editorial":    "--style raw --stylize 900",
}


def format_midjourney(prompt: BuiltPrompt) -> FormattedPrompt:
    """Format for MidJourney v6 /imagine command."""
    shot_type = prompt.config.shot_type
    ar = MJ_ASPECT_RATIOS.get(shot_type, "4:5")
    style_params = MJ_STYLE_PARAMS.get(shot_type, "--style raw --stylize 600")

    # MidJourney uses natural comma-separated prompts; no negative block in /imagine
    # Negative goes in --no parameter
    no_terms = "cartoon, anime, illustration, painting, sketch, 3D render, CGI, watermark, text"

    mj_prompt = (
        f"{prompt.positive}, "
        f"hyperrealistic photography, ultra-detailed, professional"
    )

    parameters = {
        "version":      "6.1",
        "aspect_ratio": ar,
        "style":        style_params.split("--style ")[-1].split(" ")[0],
        "stylize":      style_params.split("--stylize ")[-1],
        "quality":      "2",
        "no":           no_terms,
    }

    copy_paste = (
        f"/imagine {mj_prompt} "
        f"--ar {ar} {style_params} --q 2 --v 6.1 --no {no_terms}"
    )

    return FormattedPrompt(
        platform="midjourney",
        positive=mj_prompt,
        negative=no_terms,
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Runway Gen-3 Alpha formatter
# ─────────────────────────────────────────────────────────────────────────────

RUNWAY_CAMERA_MOVES = {
    "portrait":     "slow push in toward subject",
    "landscape":    "cinematic pan across the scene",
    "street":       "handheld follow shot",
    "product":      "slow orbital rotation around product",
    "architecture": "rising crane shot revealing full structure",
    "wildlife":     "telephoto tracking with subject",
    "cinematic":    "dramatic dolly zoom",
    "lifestyle":    "gentle handheld drift capturing natural moment",
    "fashion":      "tracking the model's movement, elegant pace",
    "beauty":       "slow push toward face, soft focus pull",
    "food":         "overhead descend revealing full spread",
    "travel":       "wide sweeping pan over landscape",
    "fitness":      "dynamic tracking shot capturing explosive movement",
    "social_story": "vertical intimate handheld",
    "editorial":    "slow dramatic reveal, editorial pacing",
}

RUNWAY_ASPECT = {
    "portrait":     "720:1280",
    "landscape":    "1280:720",
    "street":       "720:1280",
    "product":      "1024:1024",
    "architecture": "1280:720",
    "wildlife":     "1280:720",
    "cinematic":    "1280:540",
    "lifestyle":    "864:1080",
    "fashion":      "864:1080",
    "beauty":       "1024:1024",
    "food":         "1024:1024",
    "travel":       "1280:720",
    "fitness":      "864:1080",
    "social_story": "720:1280",
    "editorial":    "864:1080",
}


def format_runway(prompt: BuiltPrompt, motion: Optional[str] = None) -> FormattedPrompt:
    """Format for Runway Gen-3 Alpha."""
    shot_type = prompt.config.shot_type
    camera_move = motion or RUNWAY_CAMERA_MOVES.get(shot_type, "slow cinematic drift")
    resolution = RUNWAY_ASPECT.get(shot_type, "1280:720")

    # Runway works best with action-first prompts
    positive = (
        f"{camera_move}. {prompt.positive}. "
        f"Photorealistic, cinematic quality, smooth motion, no camera shake."
    )

    parameters = {
        "resolution":    resolution,
        "duration":      "10s",
        "camera_motion": camera_move,
        "seed":          "random",
        "upscale":       True,
    }

    copy_paste = (
        f"[TEXT PROMPT]\n{positive}\n\n"
        f"[SETTINGS]\n{_settings_block(parameters)}"
    )

    return FormattedPrompt(
        platform="runway",
        positive=positive,
        negative="",
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Pika 2.0 formatter
# ─────────────────────────────────────────────────────────────────────────────

PIKA_CAMERA_MOVES = {
    "portrait":     "dolly in",
    "landscape":    "pan right",
    "street":       "tracking shot",
    "product":      "orbit",
    "architecture": "crane up",
    "wildlife":     "follow",
    "cinematic":    "dolly zoom",
    "lifestyle":    "drift",
    "fashion":      "track",
    "beauty":       "push in",
    "food":         "descend",
    "travel":       "sweep",
    "fitness":      "dynamic tracking",
    "social_story": "drift",
    "editorial":    "slow reveal",
}


def format_pika(prompt: BuiltPrompt, motion: Optional[str] = None) -> FormattedPrompt:
    """Format for Pika 2.0 video generation."""
    shot_type = prompt.config.shot_type
    camera_move = motion or PIKA_CAMERA_MOVES.get(shot_type, "drift")
    aspect = HIGGSFIELD_ASPECT.get(shot_type, "16:9")

    positive = (
        f"{prompt.positive}, "
        f"cinematic quality, photorealistic, smooth motion"
    )

    parameters = {
        "aspect_ratio":       aspect,
        "camera_motion":      camera_move,
        "motion_strength":    3,          # 1-10, 3 = realistic subtle
        "fps":                24,
        "duration":           "5s",
        "negative_prompt":    prompt.negative[:200],
    }

    copy_paste = (
        f"[PROMPT]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n{_settings_block(parameters)}"
    )

    return FormattedPrompt(
        platform="pika",
        positive=positive,
        negative=prompt.negative,
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Leonardo AI formatter (Phoenix / Diffusion XL)
# ─────────────────────────────────────────────────────────────────────────────

LEONARDO_MODEL_HINTS = {
    "portrait":     {"model": "Leonardo Phoenix", "preset_style": "PHOTOGRAPHY"},
    "landscape":    {"model": "Leonardo Diffusion XL", "preset_style": "PHOTOGRAPHY"},
    "street":       {"model": "Leonardo Phoenix", "preset_style": "PHOTOGRAPHY"},
    "product":      {"model": "Leonardo Phoenix", "preset_style": "PRODUCT_PHOTOGRAPHY"},
    "architecture": {"model": "Leonardo Diffusion XL", "preset_style": "PHOTOGRAPHY"},
    "wildlife":     {"model": "Leonardo Diffusion XL", "preset_style": "PHOTOGRAPHY"},
    "cinematic":    {"model": "Leonardo Phoenix", "preset_style": "CINEMATIC"},
    "lifestyle":    {"model": "Leonardo Phoenix", "preset_style": "PHOTOGRAPHY"},
    "fashion":      {"model": "Leonardo Phoenix", "preset_style": "FASHION"},
    "beauty":       {"model": "Leonardo Phoenix", "preset_style": "PHOTOGRAPHY"},
    "food":         {"model": "Leonardo Phoenix", "preset_style": "PRODUCT_PHOTOGRAPHY"},
    "travel":       {"model": "Leonardo Diffusion XL", "preset_style": "PHOTOGRAPHY"},
    "fitness":      {"model": "Leonardo Phoenix", "preset_style": "PHOTOGRAPHY"},
    "social_story": {"model": "Leonardo Phoenix", "preset_style": "PHOTOGRAPHY"},
    "editorial":    {"model": "Leonardo Phoenix", "preset_style": "FASHION"},
}

LEONARDO_RESOLUTION = {
    "portrait":     (832, 1216),
    "landscape":    (1216, 832),
    "street":       (832, 1216),
    "product":      (1024, 1024),
    "architecture": (1216, 832),
    "wildlife":     (1216, 832),
    "cinematic":    (1280, 720),
    "lifestyle":    (864, 1080),
    "fashion":      (864, 1080),
    "beauty":       (1024, 1024),
    "food":         (1024, 1024),
    "travel":       (1216, 832),
    "fitness":      (864, 1080),
    "social_story": (720, 1280),
    "editorial":    (864, 1080),
}


def format_leonardo(prompt: BuiltPrompt) -> FormattedPrompt:
    """Format for Leonardo AI Phoenix / Diffusion XL."""
    shot_type = prompt.config.shot_type
    hint = LEONARDO_MODEL_HINTS.get(shot_type, LEONARDO_MODEL_HINTS["portrait"])
    resolution = LEONARDO_RESOLUTION.get(shot_type, (1024, 1024))

    anchor = "ultra-realistic photography, professional quality"
    positive = f"{anchor}, {prompt.positive}"

    parameters = {
        "model":          hint["model"],
        "preset_style":   hint["preset_style"],
        "width":          resolution[0],
        "height":         resolution[1],
        "num_inference_steps": 30,
        "guidance_scale": 7,
        "photoReal":      True,
        "photoReal_strength": 0.55,
        "alchemy":        True,
    }

    copy_paste = (
        f"[POSITIVE]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n{_settings_block(parameters)}"
    )

    return FormattedPrompt(
        platform="leonardo",
        positive=positive,
        negative=prompt.negative,
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Kling 2.0 formatter
# ─────────────────────────────────────────────────────────────────────────────

KLING_CAMERA_MOVES = {
    "portrait":     "slow push-in",
    "landscape":    "cinematic pan",
    "street":       "handheld follow",
    "product":      "slow orbit",
    "architecture": "rising crane",
    "wildlife":     "telephoto tracking",
    "cinematic":    "dramatic dolly zoom",
    "lifestyle":    "gentle handheld drift",
    "fashion":      "elegant model tracking",
    "beauty":       "slow face push-in",
    "food":         "overhead descend",
    "travel":       "sweeping landscape pan",
    "fitness":      "dynamic action tracking",
    "social_story": "vertical drift",
    "editorial":    "slow dramatic reveal",
}


def format_kling(prompt: BuiltPrompt, motion: Optional[str] = None) -> FormattedPrompt:
    """Format for Kling 2.0 video generation."""
    shot_type = prompt.config.shot_type
    camera_move = motion or KLING_CAMERA_MOVES.get(shot_type, "slow cinematic drift")
    aspect = HIGGSFIELD_ASPECT.get(shot_type, "16:9")

    positive = (
        f"{prompt.positive}, "
        f"cinematic quality, photorealistic, {camera_move}, smooth motion, 4K"
    )

    parameters = {
        "aspect_ratio":   aspect,
        "duration":       "5s",
        "mode":           "pro",            # standard / pro
        "camera_control": camera_move,
        "cfg_scale":      0.5,
        "negative_prompt": prompt.negative[:200],
    }

    copy_paste = (
        f"[PROMPT]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n{_settings_block(parameters)}"
    )

    return FormattedPrompt(
        platform="kling",
        positive=positive,
        negative=prompt.negative,
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# DALL-E 3 formatter (natural language)
# ─────────────────────────────────────────────────────────────────────────────

DALLE_SIZE = {
    "portrait":     "1024x1792",
    "landscape":    "1792x1024",
    "street":       "1024x1792",
    "product":      "1024x1024",
    "architecture": "1792x1024",
    "wildlife":     "1792x1024",
    "cinematic":    "1792x1024",
    "lifestyle":    "1024x1792",
    "fashion":      "1024x1792",
    "beauty":       "1024x1024",
    "food":         "1024x1024",
    "travel":       "1792x1024",
    "fitness":      "1024x1792",
    "social_story": "1024x1792",
    "editorial":    "1024x1792",
}


def format_dalle3(prompt: BuiltPrompt) -> FormattedPrompt:
    """
    Format for DALL-E 3. DALL-E 3 works best with detailed natural language
    rather than comma-separated token chains, so we rewrite the prompt.
    """
    shot_type = prompt.config.shot_type
    size = DALLE_SIZE.get(shot_type, "1024x1024")

    # Convert comma-separated tokens into flowing natural language description
    positive = (
        f"A photorealistic, ultra-detailed professional photograph of "
        f"{prompt.config.subject}. "
        f"{prompt.positive.replace(prompt.config.subject + ', ', '')}. "
        f"The image should look exactly like a real photograph with no AI artifacts, "
        f"ultra-sharp details, and professional lighting. "
        f"Do not add any artistic interpretation — pure photorealism."
    )

    parameters = {
        "model":   "dall-e-3",
        "size":    size,
        "quality": "hd",
        "style":   "natural",       # 'natural' = more photorealistic
        "n":       1,
    }

    copy_paste = (
        f"[PROMPT]\n{positive}\n\n"
        f"[SETTINGS]\n{_settings_block(parameters)}"
    )

    return FormattedPrompt(
        platform="dalle3",
        positive=positive,
        negative="",              # DALL-E 3 has no negative prompt field
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Adobe Firefly formatter
# ─────────────────────────────────────────────────────────────────────────────

FIREFLY_STYLES = {
    "portrait":     "Photo",
    "landscape":    "Photo",
    "street":       "Photo",
    "product":      "Photo",
    "architecture": "Photo",
    "wildlife":     "Photo",
    "cinematic":    "Cinematic",
    "lifestyle":    "Photo",
    "fashion":      "Fashion Photography",
    "beauty":       "Beauty Photography",
    "food":         "Food Photography",
    "travel":       "Travel Photography",
    "fitness":      "Action Photography",
    "social_story": "Photo",
    "editorial":    "Fashion Photography",
}

FIREFLY_CONTENT_CLASS = {
    "portrait":     "Photography",
    "landscape":    "Photography",
    "street":       "Photography",
    "product":      "Photography",
    "architecture": "Photography",
    "wildlife":     "Photography",
    "cinematic":    "Art",
    "lifestyle":    "Photography",
    "fashion":      "Photography",
    "beauty":       "Photography",
    "food":         "Photography",
    "travel":       "Photography",
    "fitness":      "Photography",
    "social_story": "Photography",
    "editorial":    "Photography",
}


def format_firefly(prompt: BuiltPrompt) -> FormattedPrompt:
    """Format for Adobe Firefly text-to-image."""
    shot_type = prompt.config.shot_type
    style = FIREFLY_STYLES.get(shot_type, "Photo")
    content_class = FIREFLY_CONTENT_CLASS.get(shot_type, "Photography")
    resolution = OPENART_RESOLUTION.get(shot_type, (1024, 1024))

    positive = f"{prompt.positive}, ultra-realistic, professional photography"

    parameters = {
        "style_preset":    style,
        "content_class":   content_class,
        "width":           resolution[0],
        "height":          resolution[1],
        "strength":        60,            # style influence 0-100
        "negative_prompt": prompt.negative[:300],
    }

    copy_paste = (
        f"[PROMPT]\n{positive}\n\n"
        f"[NEGATIVE]\n{prompt.negative}\n\n"
        f"[SETTINGS]\n{_settings_block(parameters)}"
    )

    return FormattedPrompt(
        platform="firefly",
        positive=positive,
        negative=prompt.negative,
        parameters=parameters,
        copy_paste=copy_paste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Platform registry
# ─────────────────────────────────────────────────────────────────────────────

ALL_PLATFORMS = [
    "openart", "higgsfield", "midjourney", "runway",
    "pika", "leonardo", "kling", "dalle3", "firefly",
]

VIDEO_PLATFORMS = ["higgsfield", "runway", "pika", "kling"]
IMAGE_PLATFORMS = ["openart", "midjourney", "leonardo", "dalle3", "firefly"]


def format_all(prompt: BuiltPrompt, motion: Optional[str] = None) -> dict[str, FormattedPrompt]:
    """Format a BuiltPrompt for every supported platform."""
    return {
        "openart":    format_openart(prompt),
        "higgsfield": format_higgsfield(prompt, motion),
        "midjourney": format_midjourney(prompt),
        "runway":     format_runway(prompt, motion),
        "pika":       format_pika(prompt, motion),
        "leonardo":   format_leonardo(prompt),
        "kling":      format_kling(prompt, motion),
        "dalle3":     format_dalle3(prompt),
        "firefly":    format_firefly(prompt),
    }

