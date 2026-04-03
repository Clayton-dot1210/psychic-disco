"""
Visual Hook Templates for AI video content.

Hooks are the first 1-3 seconds that stop the scroll and compel viewers to
keep watching. Each template defines the visual language, motion cue, and
prompt structure optimized for maximum attention capture.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class HookTemplate:
    """A visual hook pattern for the opening beat of a video."""

    name: str
    hook_type: str
    visual_setup: str           # What the viewer sees in frame
    camera_action: str          # How the camera moves
    subject_action: str         # What the character/subject does
    emotion_tone: str           # Emotional quality of the frame
    prompt_prefix: str          # Token string injected into positive prompt
    motion_cue: str             # Camera motion for video platforms
    duration_hint: str          # Recommended duration
    description: str            # Human-readable description


# ─────────────────────────────────────────────────────────────────────────────
# Hook templates
# ─────────────────────────────────────────────────────────────────────────────

HOOK_TEMPLATES: dict[str, HookTemplate] = {

    "pattern_interrupt": HookTemplate(
        name="Pattern Interrupt",
        hook_type="pattern_interrupt",
        visual_setup="unexpected jarring visual that breaks the scroll",
        camera_action="sudden snap zoom, aggressive push-in",
        subject_action="unexpected action or expression that surprises the viewer",
        emotion_tone="shocking, surprising, disruptive",
        prompt_prefix=(
            "scroll-stopping unexpected visual, immediate attention-grab, "
            "jarring pattern interrupt, viewer frozen mid-scroll, "
        ),
        motion_cue="sudden snap zoom in, aggressive push-in",
        duration_hint="1-2 seconds",
        description="Breaks viewer's scrolling pattern with a jarring unexpected visual",
    ),

    "bold_claim": HookTemplate(
        name="Bold Claim",
        hook_type="bold_claim",
        visual_setup="character looking directly into lens with absolute certainty",
        camera_action="slow confident push-in",
        subject_action="direct intense eye contact, slight forward lean toward camera",
        emotion_tone="confident, authoritative, unshakeable",
        prompt_prefix=(
            "intense direct eye contact into lens, commanding authority presence, "
            "absolute self-certainty, zero doubt expression, "
        ),
        motion_cue="slow deliberate push-in, authority framing",
        duration_hint="1-3 seconds",
        description="Character delivers a bold statement directly to camera with zero hesitation",
    ),

    "curiosity_hook": HookTemplate(
        name="Curiosity Hook",
        hook_type="curiosity",
        visual_setup="something partially revealed — viewer must know what happens next",
        camera_action="slow reveal pan or anticipation tilt",
        subject_action="knowing look, slight smirk, something off-frame grabbing their attention",
        emotion_tone="mysterious, intriguing, tantalizing",
        prompt_prefix=(
            "tantalizing partial reveal, curiosity-gap visual, "
            "viewer must know more, mysterious knowing expression, "
        ),
        motion_cue="slow reveal pan, anticipation tilt toward mystery",
        duration_hint="2-3 seconds",
        description="Creates a curiosity gap that psychologically compels continued watching",
    ),

    "pov_hook": HookTemplate(
        name="POV Hook",
        hook_type="pov",
        visual_setup="first-person perspective — the viewer is inside the scene",
        camera_action="slight handheld drift, immersive movement",
        subject_action="character reacts directly to the viewer/camera",
        emotion_tone="immersive, direct, engaging, intimate",
        prompt_prefix=(
            "immersive first-person POV, viewer placed inside the scene, "
            "direct address to camera, you-are-there perspective, "
        ),
        motion_cue="handheld immersive drift, subtle POV shake",
        duration_hint="2-3 seconds",
        description="Places the viewer directly inside the scene as a participant",
    ),

    "transformation_hook": HookTemplate(
        name="Transformation Hook",
        hook_type="transformation",
        visual_setup="show the impressive result/after state first — desire before explanation",
        camera_action="dramatic reveal push-in or crane up",
        subject_action="confident display of transformation result, proud reveal",
        emotion_tone="impressed, desiring, aspiring",
        prompt_prefix=(
            "dramatic reveal of impressive result, aspirational outcome displayed, "
            "desire-inducing transformation, show the prize first, "
        ),
        motion_cue="dramatic crane up reveal, cinematic push-in",
        duration_hint="2-3 seconds",
        description="Leads with the result to create desire and curiosity about the how",
    ),

    "social_proof_hook": HookTemplate(
        name="Social Proof Hook",
        hook_type="social_proof",
        visual_setup="authentic evidence of real results, testimonial energy",
        camera_action="warm approachable push-in",
        subject_action="genuine excited smile, sharing news they can't contain",
        emotion_tone="excited, validated, authentic",
        prompt_prefix=(
            "genuine excitement sharing real results, authentic testimonial energy, "
            "real person real outcome expression, can't-believe-it happened face, "
        ),
        motion_cue="warm approachable push-in, friend-sharing intimacy",
        duration_hint="1-2 seconds",
        description="Establishes credibility through authentic social proof energy",
    ),

    "question_hook": HookTemplate(
        name="Question Hook",
        hook_type="question",
        visual_setup="character posing a question the target audience deeply identifies with",
        camera_action="gentle drift toward camera, intimate pull-in",
        subject_action="questioning expression, engaged curious look, slight head tilt",
        emotion_tone="curious, relatable, conspiratorial",
        prompt_prefix=(
            "engaging questioning expression, relatable curiosity energy, "
            "viewer recognition face — they feel seen, slight knowing head tilt, "
        ),
        motion_cue="gentle drift toward lens, intimate questioning pull-in",
        duration_hint="1-2 seconds",
        description="Opens with a question the audience deeply identifies with",
    ),

    # ── Character 28 specific hooks ───────────────────────────────────────────

    "silent_stare": HookTemplate(
        name="Silent Stare (Character 28)",
        hook_type="pattern_interrupt",
        visual_setup=(
            "character stands perfectly still in rain-soaked street, "
            "staring directly into lens with cold intensity"
        ),
        camera_action="ultra-slow push-in from wide to close, creeping in",
        subject_action="absolute stillness, cold unblinking stare into lens",
        emotion_tone="cold, intense, unnerving, magnetic",
        prompt_prefix=(
            "absolute stillness in rain, cold unblinking stare into lens, "
            "magnetic intensity, you cannot look away, silent protagonist energy, "
            "rain falling around motionless figure, "
        ),
        motion_cue="ultra-slow creeping push-in, almost imperceptible drift",
        duration_hint="2-4 seconds",
        description="Character 28 signature: silent unblinking stare in rain — can't look away",
    ),

    "urban_reveal": HookTemplate(
        name="Urban Reveal (Character 28)",
        hook_type="transformation",
        visual_setup=(
            "slow crane up from wet cobblestones to reveal character "
            "standing centered in empty rain-lit street"
        ),
        camera_action="slow crane up from ground level, full body reveal",
        subject_action="standing centered, hands relaxed, facing camera with composed intensity",
        emotion_tone="cinematic, powerful, presence-establishing",
        prompt_prefix=(
            "cinematic full-body reveal, slow crane up from wet cobblestones, "
            "lone figure centered in rain-soaked street, establishing shot power, "
            "blue hour moody atmosphere, "
        ),
        motion_cue="slow crane up from ground to eye level, full reveal",
        duration_hint="3-5 seconds",
        description="Character 28 signature: cinematic crane-up reveal on wet empty street",
    ),

    "neon_emergence": HookTemplate(
        name="Neon Emergence (Character 28)",
        hook_type="pattern_interrupt",
        visual_setup=(
            "character's face emerges from darkness into neon-lit alley, "
            "steam and color spill framing the reveal"
        ),
        camera_action="slow push-in from dark to neon-lit face",
        subject_action="face emerges from shadow, eyes catching neon light",
        emotion_tone="dramatic, mysterious, cinematic",
        prompt_prefix=(
            "face emerging from urban darkness into neon light, "
            "atmospheric steam swirling, cyberpunk color spill, "
            "dramatic emergence from shadow, cinematic reveal, "
        ),
        motion_cue="slow push-in from darkness, neon light reveal",
        duration_hint="2-4 seconds",
        description="Character 28 variant: dramatic neon emergence from urban shadow",
    ),
}


def get_hook(hook_type: str) -> Optional[HookTemplate]:
    """Look up a hook template by key. Returns None if not found."""
    return HOOK_TEMPLATES.get(hook_type)


def list_hooks() -> dict[str, HookTemplate]:
    """Return all available hook templates."""
    return HOOK_TEMPLATES
