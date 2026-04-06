"""
Psychic Disco — AI Art, Influencer & Video Prompt Engineering Engine.

Supports 9 platforms: OpenArt, Higgsfield, MidJourney, Runway, Pika,
Leonardo AI, Kling, DALL-E 3, Adobe Firefly.

Core modules:
  builder        — Assembles structured PromptConfig into positive/negative pairs
  platforms      — Platform-specific formatters for all 9 platforms
  ai_interpreter — Claude-powered natural language brief → expert prompts
  modifiers      — Curated token libraries for all shot types
  learning       — Technique library and AI-powered explanations
  automation     — Google Sheets and Nano Banana integration
"""
from .builder import PromptConfig, BuiltPrompt, build
from .platforms import (
    FormattedPrompt,
    format_openart, format_higgsfield, format_midjourney,
    format_runway, format_pika, format_leonardo,
    format_kling, format_dalle3, format_firefly,
    format_all, ALL_PLATFORMS, VIDEO_PLATFORMS, IMAGE_PLATFORMS,
)

__all__ = [
    # Builder
    "PromptConfig",
    "BuiltPrompt",
    "build",
    # Platforms
    "FormattedPrompt",
    "format_openart",
    "format_higgsfield",
    "format_midjourney",
    "format_runway",
    "format_pika",
    "format_leonardo",
    "format_kling",
    "format_dalle3",
    "format_firefly",
    "format_all",
    "ALL_PLATFORMS",
    "VIDEO_PLATFORMS",
    "IMAGE_PLATFORMS",
]
