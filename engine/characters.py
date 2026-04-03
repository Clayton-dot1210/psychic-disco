"""
AI Content Character profiles for UGC video promotion.

Characters provide visual consistency tokens injected into prompts,
ensuring your AI persona looks and feels coherent across all shots
in a sequence, hook, or single-frame generation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Character:
    """A reusable AI content character with defined visual attributes."""

    name: str
    archetype: str                       # creator, expert, everyday, influencer, entrepreneur
    age_range: str                       # e.g. "mid-20s", "early 30s"
    gender_expression: str               # e.g. "woman", "man", "person"
    style: str                           # high-level visual style description
    wardrobe_tokens: list[str]           # clothing/accessory descriptor tokens
    environment_tokens: list[str]        # typical background/setting tokens
    expression_tokens: list[str]         # default facial expressions / emotions
    skin_detail: str = "natural skin texture, pore-level detail, no airbrushing"
    hair_detail: str = ""
    extra_tokens: list[str] = field(default_factory=list)

    def to_subject_prefix(self) -> str:
        """
        Generate a comma-separated subject prefix for prompt injection.
        Keeps wardrobe tokens to the first two to avoid over-constraining generation.
        """
        parts: list[str] = [
            f"{self.age_range} {self.gender_expression}",
            self.style,
        ]
        parts.extend(self.wardrobe_tokens[:2])
        if self.hair_detail:
            parts.append(self.hair_detail)
        parts.append(self.skin_detail)
        parts.extend(self.extra_tokens)
        return ", ".join(p for p in parts if p)

    def primary_environment(self) -> str:
        """Return the first (most characteristic) environment token."""
        return self.environment_tokens[0] if self.environment_tokens else ""

    def primary_expression(self) -> str:
        """Return the first (default) expression token."""
        return self.expression_tokens[0] if self.expression_tokens else ""


# ─────────────────────────────────────────────────────────────────────────────
# Predefined character archetypes
# ─────────────────────────────────────────────────────────────────────────────

CHARACTERS: dict[str, Character] = {

    "creator": Character(
        name="The Creator",
        archetype="creator",
        age_range="mid-20s",
        gender_expression="woman",
        style="casual-chic content creator aesthetic",
        wardrobe_tokens=[
            "oversized neutral-tone hoodie",
            "minimal delicate jewelry",
            "clean white sneakers",
        ],
        environment_tokens=[
            "minimalist home studio with soft ring light",
            "bright natural-light apartment interior",
            "cozy organized desk setup",
        ],
        expression_tokens=[
            "genuine warm smile",
            "engaged expressive face",
            "direct confident eye contact with camera",
        ],
        hair_detail="effortless natural hair, lived-in texture",
    ),

    "expert": Character(
        name="The Expert",
        archetype="expert",
        age_range="early 30s",
        gender_expression="man",
        style="polished professional authority figure",
        wardrobe_tokens=[
            "well-fitted crisp white dress shirt",
            "subtle minimal watch",
        ],
        environment_tokens=[
            "clean modern home office with bookshelf background",
            "minimalist desk with laptop and clean surface",
            "pure white seamless background",
        ],
        expression_tokens=[
            "confident composed authority expression",
            "direct steady gaze into lens",
            "slight knowing half-smile",
        ],
        hair_detail="neat professionally groomed hair",
        extra_tokens=["trustworthy demeanor", "calm authority"],
    ),

    "everyday": Character(
        name="The Everyday Person",
        archetype="everyday",
        age_range="late 20s",
        gender_expression="person",
        style="relatable authentic real-life look",
        wardrobe_tokens=[
            "comfortable casual t-shirt",
            "well-worn jeans",
        ],
        environment_tokens=[
            "cozy lived-in living room",
            "casual kitchen background",
            "outdoor neighborhood sidewalk",
        ],
        expression_tokens=[
            "genuine candid unposed expression",
            "natural human emotion",
            "authentic relatable face",
        ],
        hair_detail="natural unstyled everyday hair",
        extra_tokens=["real human imperfections", "organic authenticity"],
    ),

    "influencer": Character(
        name="The Influencer",
        archetype="influencer",
        age_range="mid-20s",
        gender_expression="woman",
        style="high-fashion aspirational lifestyle influencer",
        wardrobe_tokens=[
            "on-trend curated outfit",
            "designer accessories",
            "polished put-together look",
        ],
        environment_tokens=[
            "luxury light-filled apartment with curated decor",
            "upscale coffee shop with marble surfaces",
            "rooftop terrace with city skyline",
        ],
        expression_tokens=[
            "radiant confident editorial smile",
            "aspirational poised charisma",
            "captivating magnetic presence",
        ],
        hair_detail="perfectly styled glossy hair",
        extra_tokens=["flawless natural makeup", "aspirational glow"],
    ),

    "entrepreneur": Character(
        name="The Entrepreneur",
        archetype="entrepreneur",
        age_range="early 30s",
        gender_expression="man",
        style="driven modern entrepreneur hustle aesthetic",
        wardrobe_tokens=[
            "fitted dark premium crewneck",
            "clean minimal luxury watch",
        ],
        environment_tokens=[
            "sleek modern coworking space",
            "minimalist private office",
            "laptop open at upscale coffee shop",
        ],
        expression_tokens=[
            "intense focused driven expression",
            "ambitious forward-leaning energy",
            "self-made confident authority",
        ],
        hair_detail="clean sharp fade or well-groomed hair",
        extra_tokens=["sharp focused intensity", "successful grounded energy"],
    ),

    # ── Custom character built from reference images ──────────────────────────

    "character_28": Character(
        name="Character 28",
        archetype="urban_explorer",
        age_range="28-year-old",
        gender_expression="man",
        style=(
            "dark techwear urban explorer, Arc'teryx gorpcore aesthetic, "
            "cinematic silent protagonist energy"
        ),
        wardrobe_tokens=[
            "Arc'teryx black technical shell jacket with hood",
            "Arc'teryx black/tan geometric patterned beanie pulled low",
            "black balaclava neck gaiter",
            "Arc'teryx black sling crossbody bag",
            "Arc'teryx black technical pants",
            "Salomon trail running shoes",
        ],
        environment_tokens=[
            "wet rain-slicked cobblestone British high street at blue hour dusk",
            "neon-lit dystopian urban alley with steam and graffiti",
            "overcast grey city streets with bokeh shop lights in background",
            "rain-wet steps of urban architecture at dusk",
        ],
        expression_tokens=[
            "cold intense stoic expression, thousand-yard stare",
            "calm unreadable intensity, silent protagonist energy",
            "slight jaw tension, composed under pressure",
        ],
        skin_detail=(
            "natural skin texture, visible pores, light freckle scatter, "
            "no airbrushing, realistic imperfections, rain moisture on skin"
        ),
        hair_detail="short dark hair hidden under Arc'teryx beanie",
        extra_tokens=[
            "lean athletic build",
            "sharp defined jaw",
            "hazel brown eyes",
            "wet rain droplets on jacket",
            "blue hour ambient street light",
            "moody cinematic urban atmosphere",
        ],
    ),

    "character_28_shades": Character(
        name="Character 28 (Sunglasses Variant)",
        archetype="urban_explorer",
        age_range="28-year-old",
        gender_expression="man",
        style=(
            "dark techwear urban explorer, Arc'teryx gorpcore aesthetic, "
            "Oakley wraparound mirrored lens variant"
        ),
        wardrobe_tokens=[
            "Arc'teryx black technical shell jacket",
            "Arc'teryx black/tan geometric patterned beanie",
            "Oakley wraparound sunglasses with red orange mirrored lenses",
            "black balaclava neck gaiter",
            "Arc'teryx black sling bag",
            "Arc'teryx black technical pants",
            "Salomon trail running shoes",
        ],
        environment_tokens=[
            "wet cobblestone high street with bokeh shop lights",
            "overcast British street at dusk",
            "rain-wet urban steps, grey sky",
        ],
        expression_tokens=[
            "stoic unreadable face behind mirrored lenses",
            "cold composed authority through tinted glasses",
            "silent observer energy, masked intensity",
        ],
        skin_detail=(
            "natural skin texture, realistic pores, no airbrushing, "
            "rain moisture on skin surface"
        ),
        hair_detail="short dark hair under Arc'teryx beanie",
        extra_tokens=[
            "lean athletic build",
            "sharp defined jaw",
            "red orange mirrored lens reflection of street",
            "wet rain on jacket surface",
            "moody blue hour street atmosphere",
        ],
    ),
}


def get_character(name: str) -> Optional[Character]:
    """Look up a character by archetype key. Returns None if not found."""
    return CHARACTERS.get(name)


def list_characters() -> dict[str, Character]:
    """Return all available character definitions."""
    return CHARACTERS
