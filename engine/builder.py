"""
Core prompt builder — assembles subject descriptions with realism modifiers
into a structured prompt string ready for OpenArt or Higgsfield.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

from .modifiers import (
    APERTURE,
    ATMOSPHERE,
    CAMERA_BODIES,
    COMPOSITION,
    DOF_BOKEH,
    FILM_LOOKS,
    ISO,
    LENSES,
    LIGHTING_CINEMATIC,
    LIGHTING_NATURAL,
    LIGHTING_STUDIO,
    NEGATIVE_REALISM,
    POST_PROCESSING,
    QUALITY_BOOST,
    SENSOR_QUALITY,
    SHOT_PRESETS,
)


@dataclass
class PromptConfig:
    """All parameters that drive prompt generation."""

    subject: str
    shot_type: str = "portrait"            # key into SHOT_PRESETS
    lighting: Optional[str] = None         # override lighting
    camera: Optional[str] = None           # override camera
    lens: Optional[str] = None             # override lens
    aperture: Optional[str] = None         # override aperture
    atmosphere: Optional[str] = None       # optional atmosphere token
    composition: Optional[str] = None      # optional composition token
    extra_style: Optional[str] = None      # any free-text style riders
    randomize: bool = False                # randomise non-preset fields
    seed: Optional[int] = None             # for reproducible randomisation


@dataclass
class BuiltPrompt:
    """The assembled prompt pair returned to callers."""

    positive: str
    negative: str
    config: PromptConfig
    platform_hints: dict = field(default_factory=dict)


# ─────────────────────────────────────────────────────────────────────────────

def _pick(pool: list[str], override: Optional[str], rng: random.Random) -> str:
    if override:
        return override
    return rng.choice(pool)


def build(config: PromptConfig) -> BuiltPrompt:
    """
    Assemble a positive + negative prompt pair optimised for photorealism.

    Parameters
    ----------
    config : PromptConfig

    Returns
    -------
    BuiltPrompt
    """
    rng = random.Random(config.seed)

    preset = SHOT_PRESETS.get(config.shot_type, SHOT_PRESETS["portrait"])

    # ── Resolve each modifier ─────────────────────────────────────────────────
    camera = config.camera or preset["camera"]
    lens   = config.lens   or preset["lens"]
    aperture = config.aperture or preset["aperture"]
    lighting = config.lighting or preset["lighting"]
    dof    = preset["dof"]

    if config.randomize:
        camera   = _pick(CAMERA_BODIES,  config.camera,   rng)
        lens     = _pick(LENSES,         config.lens,     rng)
        aperture = _pick(APERTURE,       config.aperture, rng)
        all_lighting = LIGHTING_NATURAL + LIGHTING_STUDIO + LIGHTING_CINEMATIC
        lighting = _pick(all_lighting,   config.lighting, rng)
        dof      = rng.choice(DOF_BOKEH)

    quality_tokens = preset["quality"]
    post_tokens    = preset["post"]

    atmosphere  = config.atmosphere  or (rng.choice(ATMOSPHERE)  if config.randomize else None)
    composition = config.composition or (rng.choice(COMPOSITION) if config.randomize else None)

    # ── Assemble positive prompt ──────────────────────────────────────────────
    parts: list[str] = [config.subject]

    parts.append(camera)
    parts.append(lens)
    parts.append(aperture)
    parts.append(lighting)
    parts.append(dof)

    if composition:
        parts.append(composition)
    if atmosphere:
        parts.append(atmosphere)
    if config.extra_style:
        parts.append(config.extra_style)

    parts.extend(quality_tokens)
    parts.extend(post_tokens)

    positive = ", ".join(parts)
    negative = NEGATIVE_REALISM

    return BuiltPrompt(
        positive=positive,
        negative=negative,
        config=config,
    )
