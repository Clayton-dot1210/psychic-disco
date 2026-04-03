"""
UGC (User Generated Content) and visual hook modifiers.

UGC aesthetic prioritizes authentic, raw, and relatable visuals over polished
commercial photography. These tokens push generation toward content that feels
real, human, and organically created — ideal for TikTok, Reels, and Shorts.
"""

# ── UGC Camera Aesthetic ──────────────────────────────────────────────────────

UGC_CAMERA_BODIES = [
    "shot on iPhone 15 Pro",
    "shot on Samsung Galaxy S24 Ultra",
    "shot on GoPro HERO12",
    "shot on DJI Osmo Pocket 3",
    "shot on Canon EOS M50 Mark II",
    "shot on Sony ZV-E10",
    "shot on Fujifilm X-T5",
]

UGC_LENSES = [
    "wide angle front camera",
    "24mm wide lens",
    "standard 28mm lens",
    "slightly wide 35mm",
    "selfie camera perspective",
]

# ── UGC Lighting ──────────────────────────────────────────────────────────────

UGC_LIGHTING = [
    "ring light at home",
    "window natural light selfie",
    "natural ambient room light",
    "soft overhead light",
    "outdoor daylight selfie",
    "warm tungsten room light",
    "practical desk lamp light",
    "sunlit window background",
]

# ── Techwear / Character_28 Specific Lighting ─────────────────────────────────

TECHWEAR_LIGHTING = [
    "blue hour ambient street light, wet reflections",
    "neon backlight rain atmosphere",
    "overcast diffused grey sky light",
    "motivated practical street lamp warm vs cool contrast",
    "wet cobblestone puddle light reflections",
    "cinematic dusk low-key urban lighting",
    "sodium vapor street lamp warm glow",
    "cyberpunk neon environmental light spill",
]

# ── UGC Authenticity Tokens ───────────────────────────────────────────────────

UGC_AUTHENTICITY = [
    "authentic candid feel",
    "real person look",
    "natural imperfections",
    "organic unposed",
    "genuine human moment",
    "lived-in authenticity",
    "relatable everyday aesthetic",
    "raw and real",
]

# ── UGC Composition Styles ────────────────────────────────────────────────────

UGC_COMPOSITION = [
    "direct to camera talking head",
    "tight centered selfie frame",
    "slightly off-center handheld",
    "close-up face fill frame",
    "vertical 9:16 TikTok frame",
    "POV hand-held perspective",
    "shoulder-level self-shot",
]

# ── Platform Context Tokens ───────────────────────────────────────────────────

UGC_PLATFORM_CONTEXT: dict[str, list[str]] = {
    "tiktok": [
        "TikTok-style vertical video",
        "bold expressive face",
        "short-form content energy",
        "high-retention visual hook",
    ],
    "reels": [
        "Instagram Reels aesthetic",
        "polished but casual",
        "aspirational everyday content",
        "bright and vibrant",
    ],
    "youtube_shorts": [
        "YouTube Shorts format",
        "direct engaging eye contact",
        "clear facial expression",
        "high-retention thumbnail energy",
    ],
}

# ── Negative Prompt: UGC (removes overly polished commercial look) ─────────────

NEGATIVE_UGC = (
    "overly retouched, airbrushed skin, plastic smooth skin, commercial photography look, "
    "studio flat lighting, stock photo feel, posed model, advertisement aesthetic, "
    "high-fashion editorial, over color-graded, low quality, blurry motion, noisy grain, "
    "bad anatomy, watermark, text overlay, distorted face, multiple people unless intended"
)

# ── Negative Prompt: Techwear / Dark Cinematic (preserves gritty mood) ────────

NEGATIVE_TECHWEAR = (
    "bright cheerful colors, warm sunny look, airbrushed perfect skin, "
    "commercial advertisement feel, stock photo pose, flat studio lighting, "
    "low quality, blurry, distorted anatomy, watermark, text, multiple faces, "
    "cartoon, illustration, anime, CGI render, overly saturated, HDR overdone"
)

# ── UGC Shot Type Presets ─────────────────────────────────────────────────────

UGC_SHOT_PRESETS: dict[str, dict] = {
    "talking_head": {
        "camera": "shot on iPhone 15 Pro",
        "lens": "wide angle front camera",
        "aperture": "f/1.8 shallow depth of field",
        "lighting": "ring light at home",
        "dof": "slight background blur",
        "quality": ["natural skin texture", "pore-level detail", "authentic candid feel"],
        "post": ["natural color grade", "real person look", "organic unposed"],
        "description": "Direct to camera talking head, UGC creator style",
        "motion_cue": "slow subtle push-in, handheld micro-drift",
        "duration": "3-5 seconds",
        "aspect": "9:16",
    },
    "pov": {
        "camera": "shot on iPhone 15 Pro",
        "lens": "wide angle 24mm lens",
        "aperture": "f/2.8",
        "lighting": "natural ambient room light",
        "dof": "deep POV focus",
        "quality": ["immersive first-person perspective", "authentic candid feel"],
        "post": ["handheld natural motion", "raw and real"],
        "description": "Point-of-view first-person perspective shot",
        "motion_cue": "immersive handheld drift, POV slight shake",
        "duration": "3-5 seconds",
        "aspect": "9:16",
    },
    "reaction": {
        "camera": "shot on Sony ZV-E10",
        "lens": "slightly wide 35mm",
        "aperture": "f/2.0",
        "lighting": "window natural light selfie",
        "dof": "sharp face with soft room background",
        "quality": ["genuine human emotion", "authentic expression", "relatable everyday aesthetic"],
        "post": ["lived-in authenticity", "organic unposed"],
        "description": "Authentic reaction/response shot",
        "motion_cue": "handheld responsive reframe, quick expression catch",
        "duration": "2-4 seconds",
        "aspect": "9:16",
    },
    "lifestyle": {
        "camera": "shot on Fujifilm X-T5",
        "lens": "standard 28mm lens",
        "aperture": "f/2.8",
        "lighting": "outdoor daylight selfie",
        "dof": "environmental context with sharp subject",
        "quality": ["lifestyle documentary feel", "genuine human moment", "relatable"],
        "post": ["natural color grade", "warm tones", "real world textures"],
        "description": "Day-in-life lifestyle content shot",
        "motion_cue": "gentle tracking follow, environmental pan",
        "duration": "4-6 seconds",
        "aspect": "9:16",
    },
    "unboxing": {
        "camera": "shot on iPhone 15 Pro",
        "lens": "wide angle front camera",
        "aperture": "f/2.0",
        "lighting": "practical desk lamp light",
        "dof": "product in foreground, creator in background",
        "quality": ["product detail visible", "authentic unboxing energy", "real person reaction"],
        "post": ["natural lighting color grade", "genuine excitement"],
        "description": "Product reveal and unboxing style",
        "motion_cue": "slow reveal push-in, product focus pull",
        "duration": "4-6 seconds",
        "aspect": "9:16",
    },
    "transformation": {
        "camera": "shot on Canon EOS M50 Mark II",
        "lens": "35mm f/1.4 prime lens",
        "aperture": "f/1.8 shallow depth of field",
        "lighting": "soft overhead light",
        "dof": "sharp subject pop",
        "quality": ["before after visual clarity", "aspirational result", "compelling transformation"],
        "post": ["clean color grade", "professional finish", "high contrast reveal"],
        "description": "Before/after or reveal transformation shot",
        "motion_cue": "dramatic crane up reveal, push-in",
        "duration": "3-5 seconds",
        "aspect": "9:16",
    },

    # ── Character 28 signature shot presets ───────────────────────────────────

    "techwear_street": {
        "camera": "shot on Sony A7R V",
        "lens": "35mm f/1.4 prime lens",
        "aperture": "f/1.8 shallow depth of field",
        "lighting": "blue hour ambient street light, wet cobblestone reflections",
        "dof": "sharp subject, creamy bokeh shop lights behind",
        "quality": [
            "pore-level skin detail", "rain moisture on jacket surface",
            "wet cobblestone texture", "photojournalistic realism",
        ],
        "post": [
            "cinematic blue-teal grade", "Kodak Vision3 500T cinema film",
            "motivated street lamp warm glow", "wet reflections color depth",
        ],
        "description": "Character 28 signature: wet street blue hour techwear",
        "motion_cue": "slow deliberate push-in, slight handheld steadiness",
        "duration": "4-6 seconds",
        "aspect": "9:16",
    },
    "techwear_closeup": {
        "camera": "shot on Sony A7R V",
        "lens": "85mm f/1.4 prime lens",
        "aperture": "f/1.4 wide open",
        "lighting": "cinematic dusk low-key street lighting",
        "dof": "razor thin focus on eyes, creamy street bokeh background",
        "quality": [
            "pore-level face detail", "intense eye focus", "rain on skin texture",
            "micro contrast skin rendering",
        ],
        "post": [
            "desaturated cool teal grade", "cinematic chiaroscuro",
            "subtle anamorphic lens quality", "ultra-realistic skin",
        ],
        "description": "Character 28 signature: extreme close-up intense face",
        "motion_cue": "ultra-slow push-in, almost imperceptible drift",
        "duration": "3-5 seconds",
        "aspect": "9:16",
    },
    "techwear_wide": {
        "camera": "shot on Sony A7R V",
        "lens": "24-70mm f/2.8 zoom",
        "aperture": "f/2.8",
        "lighting": "overcast blue-grey sky, ambient street lamp warm glow",
        "dof": "full environmental portrait, sharp subject in environment",
        "quality": [
            "full body environmental portrait", "wet street texture detail",
            "architectural depth", "urban scale context",
        ],
        "post": [
            "desaturated moody grade", "cool blue tones", "wet pavement reflections",
            "cinematic atmosphere",
        ],
        "description": "Character 28 signature: full body centered wet street",
        "motion_cue": "slow crane up, full reveal from ground to face",
        "duration": "5-7 seconds",
        "aspect": "9:16",
    },
    "techwear_neon": {
        "camera": "shot on Canon EOS R5",
        "lens": "50mm f/1.2 prime lens",
        "aperture": "f/1.2 wide open",
        "lighting": "neon sign backlight, cyberpunk color spill, steam atmosphere",
        "dof": "sharp face, neon bokeh background chaos",
        "quality": [
            "neon light skin glow", "atmospheric steam particles",
            "urban decay texture", "cyberpunk realism",
        ],
        "post": [
            "teal and orange split grade", "neon color bleed",
            "Cinestill 800T pushed grain", "cinematic anamorphic quality",
        ],
        "description": "Character 28 variant: neon cyberpunk alley atmosphere",
        "motion_cue": "slow atmospheric push-in, steam drift",
        "duration": "5-7 seconds",
        "aspect": "9:16",
    },
}
