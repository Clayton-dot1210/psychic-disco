"""Art Prompting Engine — OpenArt, Higgsfield, Runway, Kling & Pika realism prompt builder."""
from .builder import PromptConfig, BuiltPrompt, build
from .platforms import (
    FormattedPrompt,
    format_openart,
    format_higgsfield,
    format_runway,
    format_kling,
    format_pika,
)
from .characters import Character, get_character, list_characters, CHARACTERS
from .hooks import HookTemplate, get_hook, list_hooks, HOOK_TEMPLATES
from .sequence import Shot, VideoSequence, SequenceConfig, build_sequence, SEQUENCE_STRUCTURES
from .ugc_modifiers import UGC_SHOT_PRESETS

__all__ = [
    # Core builder
    "PromptConfig",
    "BuiltPrompt",
    "build",
    # Platform formatters
    "FormattedPrompt",
    "format_openart",
    "format_higgsfield",
    "format_runway",
    "format_kling",
    "format_pika",
    # Characters
    "Character",
    "get_character",
    "list_characters",
    "CHARACTERS",
    # Hooks
    "HookTemplate",
    "get_hook",
    "list_hooks",
    "HOOK_TEMPLATES",
    # Sequences
    "Shot",
    "VideoSequence",
    "SequenceConfig",
    "build_sequence",
    "SEQUENCE_STRUCTURES",
    # UGC modifiers
    "UGC_SHOT_PRESETS",
]
