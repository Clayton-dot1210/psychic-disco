"""
AI Interpreter — Claude-powered natural language to prompt config converter.

User drops a plain-language comment like:
  "moody editorial fashion shoot in Paris at golden hour, woman in black coat"

Claude (claude-opus-4-6 with adaptive thinking) interprets the intent and
returns a structured PromptConfig + expert prompt suggestions for every
target platform.
"""
from __future__ import annotations

import json
import os
from typing import Optional

import anthropic

from .builder import PromptConfig, build
from .modifiers import SHOT_PRESETS
from .platforms import (
    ALL_PLATFORMS,
    format_openart, format_higgsfield, format_midjourney,
    format_runway, format_pika, format_leonardo,
    format_kling, format_dalle3, format_firefly,
    format_all,
)


# ── System prompt that turns Claude into a specialist ────────────────────────

_SYSTEM_PROMPT = """You are the world's foremost expert in AI image and video prompt engineering.
You have deep mastery of:
- Photography: cameras, lenses, aperture, shutter speed, ISO, DOF, bokeh
- Lighting: natural light, studio setups, cinematic lighting, fashion lighting, beauty lighting
- Composition: rule of thirds, leading lines, framing, negative space, perspective
- Film aesthetics: Kodak Portra, Cinestill, Fujifilm film stocks
- Video motion: dolly shots, tracking shots, parallax, rack focus, crane moves
- Platform-specific optimization: MidJourney, Runway, Pika, Leonardo, Higgsfield, DALL-E 3, Adobe Firefly, OpenArt
- Content verticals: fashion, beauty, lifestyle, food, travel, fitness, editorial, social media, influencer

Your job is to interpret a user's creative brief and extract structured intent,
then recommend the optimal shot type, lighting, camera setup, and platform settings.

You MUST respond with a valid JSON object matching this exact schema:
{
  "subject": "refined subject description with creative detail",
  "shot_type": "one of: portrait|landscape|street|product|architecture|wildlife|cinematic|lifestyle|fashion|beauty|food|travel|fitness|social_story|editorial",
  "lighting": "specific lighting setup (e.g. 'golden hour rim light', 'butterfly studio lighting')",
  "camera": "specific camera body recommendation (e.g. 'shot on Hasselblad X2D 100C')",
  "lens": "specific lens recommendation (e.g. '85mm f/1.4 prime lens')",
  "aperture": "aperture recommendation (e.g. 'f/1.8 shallow depth of field')",
  "atmosphere": "optional atmosphere/environment detail (e.g. 'Parisian street bokeh')",
  "composition": "composition approach (e.g. 'rule of thirds, environmental portrait')",
  "extra_style": "any additional style tokens (e.g. 'high fashion editorial, luxury brand campaign')",
  "target_platforms": ["array of recommended platforms from: openart, higgsfield, midjourney, runway, pika, leonardo, kling, dalle3, firefly"],
  "creative_notes": "1-2 sentences of expert creative direction for the user",
  "motion_description": "for video platforms: camera motion description (e.g. 'slow dolly reveal, elegant tracking')",
  "content_format": "recommended social format (e.g. 'instagram_post', 'tiktok', 'youtube_thumbnail')",
  "reasoning": "brief explanation of your technical choices"
}

Be specific and expert. Never be generic. Every token you add should meaningfully improve output quality."""


# ─────────────────────────────────────────────────────────────────────────────

def interpret(
    user_brief: str,
    target_platforms: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> dict:
    """
    Send a user's natural language brief to Claude and get back a structured
    PromptConfig plus formatted prompts for all target platforms.

    Parameters
    ----------
    user_brief : str
        The user's plain-language creative brief.
    target_platforms : list[str], optional
        Which platforms to format output for. Defaults to all platforms.
    api_key : str, optional
        Anthropic API key. Falls back to ANTHROPIC_API_KEY env var.

    Returns
    -------
    dict with keys:
        config          — PromptConfig built from Claude's interpretation
        built_prompt    — BuiltPrompt (positive + negative strings)
        platforms       — dict[platform_name → FormattedPrompt]
        creative_notes  — Claude's expert creative direction
        reasoning       — Claude's technical reasoning
        raw_claude      — The raw JSON Claude returned
    """
    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    # Use streaming + adaptive thinking for highest quality interpretation
    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Creative brief: {user_brief}\n\n"
                    f"Preferred platforms: {', '.join(target_platforms) if target_platforms else 'all platforms'}\n\n"
                    "Respond with ONLY the JSON object, no markdown fences, no extra text."
                ),
            }
        ],
    ) as stream:
        final_message = stream.get_final_message()

    # Extract the text response (skip thinking blocks)
    raw_json = ""
    for block in final_message.content:
        if block.type == "text":
            raw_json = block.text.strip()
            break

    # Strip any accidental markdown fences
    if raw_json.startswith("```"):
        raw_json = raw_json.split("```")[1]
        if raw_json.startswith("json"):
            raw_json = raw_json[4:]

    parsed = json.loads(raw_json)

    # Build the PromptConfig from Claude's structured output
    config = PromptConfig(
        subject=parsed.get("subject", user_brief),
        shot_type=parsed.get("shot_type", "portrait"),
        lighting=parsed.get("lighting"),
        camera=parsed.get("camera"),
        lens=parsed.get("lens"),
        aperture=parsed.get("aperture"),
        atmosphere=parsed.get("atmosphere"),
        composition=parsed.get("composition"),
        extra_style=parsed.get("extra_style"),
    )

    built = build(config)

    # Format for requested platforms
    platforms_to_format = target_platforms or ALL_PLATFORMS
    formatted = {}
    format_map = {
        "openart":    format_openart,
        "higgsfield": lambda p: format_higgsfield(p, parsed.get("motion_description")),
        "midjourney": format_midjourney,
        "runway":     lambda p: format_runway(p, parsed.get("motion_description")),
        "pika":       lambda p: format_pika(p, parsed.get("motion_description")),
        "leonardo":   format_leonardo,
        "kling":      lambda p: format_kling(p, parsed.get("motion_description")),
        "dalle3":     format_dalle3,
        "firefly":    format_firefly,
    }
    for platform in platforms_to_format:
        fmt_fn = format_map.get(platform)
        if fmt_fn:
            formatted[platform] = fmt_fn(built)

    return {
        "config": config,
        "built_prompt": built,
        "platforms": formatted,
        "creative_notes": parsed.get("creative_notes", ""),
        "reasoning": parsed.get("reasoning", ""),
        "content_format": parsed.get("content_format", ""),
        "motion_description": parsed.get("motion_description", ""),
        "raw_claude": parsed,
    }


async def interpret_async(
    user_brief: str,
    target_platforms: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> dict:
    """
    Async version of interpret() for use in FastAPI async endpoints.
    Uses streaming with adaptive thinking for best quality.
    """
    client = anthropic.AsyncAnthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    async with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Creative brief: {user_brief}\n\n"
                    f"Preferred platforms: {', '.join(target_platforms) if target_platforms else 'all platforms'}\n\n"
                    "Respond with ONLY the JSON object, no markdown fences, no extra text."
                ),
            }
        ],
    ) as stream:
        final_message = await stream.get_final_message()

    raw_json = ""
    for block in final_message.content:
        if block.type == "text":
            raw_json = block.text.strip()
            break

    if raw_json.startswith("```"):
        raw_json = raw_json.split("```")[1]
        if raw_json.startswith("json"):
            raw_json = raw_json[4:]

    parsed = json.loads(raw_json)

    config = PromptConfig(
        subject=parsed.get("subject", user_brief),
        shot_type=parsed.get("shot_type", "portrait"),
        lighting=parsed.get("lighting"),
        camera=parsed.get("camera"),
        lens=parsed.get("lens"),
        aperture=parsed.get("aperture"),
        atmosphere=parsed.get("atmosphere"),
        composition=parsed.get("composition"),
        extra_style=parsed.get("extra_style"),
    )

    built = build(config)

    platforms_to_format = target_platforms or ALL_PLATFORMS
    formatted = {}
    format_map = {
        "openart":    format_openart,
        "higgsfield": lambda p: format_higgsfield(p, parsed.get("motion_description")),
        "midjourney": format_midjourney,
        "runway":     lambda p: format_runway(p, parsed.get("motion_description")),
        "pika":       lambda p: format_pika(p, parsed.get("motion_description")),
        "leonardo":   format_leonardo,
        "kling":      lambda p: format_kling(p, parsed.get("motion_description")),
        "dalle3":     format_dalle3,
        "firefly":    format_firefly,
    }
    for platform in platforms_to_format:
        fmt_fn = format_map.get(platform)
        if fmt_fn:
            formatted[platform] = fmt_fn(built)

    return {
        "config": config,
        "built_prompt": built,
        "platforms": formatted,
        "creative_notes": parsed.get("creative_notes", ""),
        "reasoning": parsed.get("reasoning", ""),
        "content_format": parsed.get("content_format", ""),
        "motion_description": parsed.get("motion_description", ""),
        "raw_claude": parsed,
    }
