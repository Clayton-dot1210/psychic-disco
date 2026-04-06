"""
Realism modifier libraries for AI image/video generation.
Covers photorealism, influencer/social media, editorial fashion, beauty,
lifestyle, food, travel, fitness, and cinematic shot types.
"""

# ── Camera & Optics ───────────────────────────────────────────────────────────
CAMERA_BODIES = [
    "shot on Sony A7R V",
    "shot on Canon EOS R5",
    "shot on Nikon Z9",
    "shot on Hasselblad X2D 100C",
    "shot on Phase One IQ4 150MP",
    "shot on Leica M11",
    "shot on Fujifilm GFX 100S",
    "shot on Sony A1",
    "shot on Canon EOS R3",
    "shot on Nikon Z8",
]

LENSES = [
    "85mm f/1.4 prime lens",
    "50mm f/1.2 prime lens",
    "35mm f/1.4 prime lens",
    "135mm f/1.8 telephoto",
    "24-70mm f/2.8 zoom",
    "100mm f/2.8 macro",
    "200mm f/2.0 telephoto",
    "24mm f/1.4 wide angle",
    "70-200mm f/2.8 telephoto zoom",
    "16-35mm f/2.8 ultra wide",
    "90mm f/2.8 tilt-shift",
    "58mm f/1.4 Otus",
]

APERTURE = [
    "f/1.2 maximum bokeh",
    "f/1.4 wide open",
    "f/1.8 shallow depth of field",
    "f/2.0",
    "f/2.8",
    "f/4.0",
    "f/5.6 deep focus",
    "f/8 landscape focus",
    "f/11 maximum sharpness",
]

SHUTTER_SPEED = [
    "1/4000s frozen motion",
    "1/2000s",
    "1/500s",
    "1/250s",
    "1/60s",
    "1/30s motion blur",
    "30s long exposure",
]

ISO = [
    "ISO 100 base",
    "ISO 400",
    "ISO 800",
    "ISO 1600",
    "ISO 3200 high ISO grain",
    "ISO 6400 cinematic grain",
]

# ── Lighting ──────────────────────────────────────────────────────────────────
LIGHTING_NATURAL = [
    "golden hour lighting",
    "blue hour lighting",
    "overcast soft diffused light",
    "harsh midday sunlight",
    "sunrise backlight",
    "sunset rim light",
    "dappled forest light",
    "window natural light",
    "soft north-facing window light",
    "dusk silhouette light",
    "cloud-diffused overhead light",
    "shade with fill reflector",
]

LIGHTING_STUDIO = [
    "Rembrandt lighting",
    "butterfly lighting",
    "split lighting",
    "loop lighting",
    "broad lighting",
    "short lighting",
    "three-point studio lighting",
    "single softbox key light",
    "large octabox diffused light",
    "ring light catchlights",
    "beauty dish with fill card",
    "parabolic silver reflector",
    "clamshell lighting setup",
    "high-key white background lighting",
]

LIGHTING_CINEMATIC = [
    "cinematic chiaroscuro",
    "neon backlight",
    "motivated practical lighting",
    "noir hard shadows",
    "high-key even lighting",
    "low-key dramatic lighting",
    "volumetric god rays",
    "anamorphic lens flare",
    "warm tungsten practical light",
    "cool HMI daylight fill",
    "colored gel accent light",
    "cyberpunk neon ambiance",
]

LIGHTING_FASHION = [
    "editorial strobe lighting",
    "fashion tent lighting",
    "high-contrast fashion lighting",
    "dramatic shadow fashion light",
    "glossy magazine lighting",
    "sharp fashion strobe",
    "moody editorial low key",
    "ethereal diffused fashion light",
]

LIGHTING_BEAUTY = [
    "beauty ring light",
    "on-axis soft box beauty light",
    "diffused beauty dish",
    "soft window beauty light",
    "glam catchlights",
    "skincare even lighting",
    "translucent skin light",
]

# ── Film & Sensor Characteristics ─────────────────────────────────────────────
FILM_LOOKS = [
    "Kodak Portra 400 film",
    "Kodak Ektar 100 film",
    "Fujifilm Pro 400H film",
    "Ilford HP5 black and white film",
    "Cinestill 800T film",
    "Kodak Vision3 500T cinema film",
    "Fujifilm Velvia 50 slide film",
    "Kodak Gold 200 film",
    "Lomography Color Negative 400",
    "Agfa Vista 200 film",
]

SENSOR_QUALITY = [
    "full-frame sensor",
    "medium format sensor",
    "100 megapixel resolution",
    "8K resolution",
    "extremely fine grain",
    "tack sharp focus",
    "micro contrast",
    "true-to-life color rendition",
    "dynamic range preserved highlights",
]

# ── Depth of Field & Bokeh ────────────────────────────────────────────────────
DOF_BOKEH = [
    "creamy bokeh background",
    "butter smooth bokeh",
    "swirly bokeh",
    "sharp subject with soft background",
    "bokeh balls in background",
    "subject separation",
    "shallow depth of field",
    "razor thin focus plane",
    "lush depth compression",
    "gossamer out of focus foreground",
]

# ── Post-Processing & Rendering ───────────────────────────────────────────────
POST_PROCESSING = [
    "RAW photo",
    "professionally retouched",
    "Lightroom edited",
    "color graded",
    "HDR details",
    "dodge and burn",
    "skin texture preserved",
    "pore-level detail",
    "photo realistic",
    "hyperrealistic",
    "photojournalistic",
    "frequency separation retouching",
    "luminosity masking",
]

# ── Composition ───────────────────────────────────────────────────────────────
COMPOSITION = [
    "rule of thirds",
    "centered composition",
    "leading lines",
    "framing within frame",
    "negative space",
    "symmetrical composition",
    "dutch angle",
    "bird's eye view",
    "worm's eye view",
    "close-up portrait",
    "environmental portrait",
    "wide establishing shot",
    "medium shot",
    "extreme close-up",
    "over-the-shoulder perspective",
    "dynamic diagonal composition",
    "flat lay overhead",
    "candid unposed moment",
]

# ── Atmosphere & Environment ──────────────────────────────────────────────────
ATMOSPHERE = [
    "atmospheric haze",
    "morning mist",
    "light fog",
    "dust particles in light",
    "smoke atmosphere",
    "rainy weather reflections",
    "wet pavement reflections",
    "crisp clear air",
    "petal confetti falling",
    "warm steam rising",
    "bokeh fairy lights background",
    "urban glow ambient",
]

# ── Quality Boosters ──────────────────────────────────────────────────────────
QUALITY_BOOST = [
    "ultra-detailed",
    "intricate details",
    "highly realistic",
    "photorealistic",
    "8K UHD",
    "award-winning photography",
    "National Geographic quality",
    "professional photography",
    "masterful composition",
    "magazine cover quality",
    "Vogue editorial quality",
    "Harper's Bazaar editorial",
    "luxury brand campaign",
]

# ── Influencer & Social Media Content ────────────────────────────────────────
SOCIAL_FORMATS = {
    "instagram_post":   {"aspect": "4:5",  "resolution": (1080, 1350)},
    "instagram_story":  {"aspect": "9:16", "resolution": (1080, 1920)},
    "instagram_reel":   {"aspect": "9:16", "resolution": (1080, 1920)},
    "tiktok":           {"aspect": "9:16", "resolution": (1080, 1920)},
    "youtube_thumbnail":{"aspect": "16:9", "resolution": (1280, 720)},
    "youtube_short":    {"aspect": "9:16", "resolution": (1080, 1920)},
    "pinterest":        {"aspect": "2:3",  "resolution": (1000, 1500)},
    "twitter_x":        {"aspect": "16:9", "resolution": (1280, 720)},
    "linkedin":         {"aspect": "1.91:1","resolution":(1200, 627)},
}

# ── Motion / Video Vocabulary ─────────────────────────────────────────────────
VIDEO_MOTION = [
    "slow push-in, subtle drift",
    "cinematic dolly zoom",
    "handheld tracking shot",
    "smooth pan reveal",
    "overhead crane descend",
    "slow orbit around subject",
    "whip pan transition",
    "timelapse sky movement",
    "slow motion 240fps",
    "subtle parallax drift",
    "rack focus pull",
    "steady stabilized glide",
]

# ── Negative Prompts ──────────────────────────────────────────────────────────
NEGATIVE_REALISM = (
    "painting, illustration, drawing, cartoon, anime, sketch, render, CGI, "
    "3D render, digital art, concept art, low quality, blurry, out of focus, "
    "grainy, noisy, overexposed, underexposed, bad anatomy, distorted, "
    "watermark, text, logo, signature, extra limbs, disfigured, ugly, "
    "amateur, plastic skin, airbrushed, unrealistic colors, flat lighting, "
    "oversaturated, HDR overdone, fake, artificial, unnatural"
)

NEGATIVE_FASHION = (
    "amateur, low quality, blurry, bad anatomy, extra limbs, disfigured, "
    "watermark, text, logo, cheap clothing, unflattering, distorted proportions, "
    "overexposed, flat lighting, unfashionable, outdated styling, poorly styled"
)

NEGATIVE_BEAUTY = (
    "blemishes unless artistic, heavy makeup artifacts, plastic skin, "
    "overretouched, waxy skin, unnatural skin tone, bad anatomy, extra limbs, "
    "watermark, text, logo, low quality, blurry, out of focus, overexposed"
)

NEGATIVE_FOOD = (
    "unappetizing, moldy, rotten, bad plating, messy, dirty plate, "
    "bad lighting, amateur, low quality, blurry, watermark, text, "
    "artificial colors, plastic looking, overexposed, underexposed"
)

NEGATIVE_VIDEO = (
    "jittery camera, unstable footage, motion blur artifacts, compression artifacts, "
    "interlacing, low resolution, pixelated, 30fps judder, amateur footage, "
    "watermark, text overlay, bad cut, abrupt motion"
)

# ── Shot Type Presets ─────────────────────────────────────────────────────────
SHOT_PRESETS = {
    # ── Original presets ──────────────────────────────────────────────────────
    "portrait": {
        "camera": "shot on Sony A7R V",
        "lens": "85mm f/1.4 prime lens",
        "aperture": "f/1.8 shallow depth of field",
        "lighting": "Rembrandt lighting",
        "dof": "creamy bokeh background",
        "quality": ["ultra-detailed", "pore-level detail", "professional photography"],
        "post": ["RAW photo", "professionally retouched", "skin texture preserved"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "slow push-in, subtle camera drift",
        "aspect": "4:5",
    },
    "landscape": {
        "camera": "shot on Hasselblad X2D 100C",
        "lens": "24-70mm f/2.8 zoom",
        "aperture": "f/8 landscape focus",
        "lighting": "golden hour lighting",
        "dof": "deep focus",
        "quality": ["ultra-detailed", "8K UHD", "award-winning photography"],
        "post": ["RAW photo", "HDR details", "color graded"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "slow pan right, parallax depth",
        "aspect": "16:9",
    },
    "street": {
        "camera": "shot on Leica M11",
        "lens": "35mm f/1.4 prime lens",
        "aperture": "f/2.8",
        "lighting": "overcast soft diffused light",
        "dof": "subject separation",
        "quality": ["photojournalistic", "ultra-detailed", "professional photography"],
        "post": ["RAW photo", "Kodak Portra 400 film"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "handheld slight shake, tracking shot",
        "aspect": "4:5",
    },
    "product": {
        "camera": "shot on Canon EOS R5",
        "lens": "100mm f/2.8 macro",
        "aperture": "f/5.6 deep focus",
        "lighting": "three-point studio lighting",
        "dof": "tack sharp focus",
        "quality": ["ultra-detailed", "magazine cover quality", "8K UHD"],
        "post": ["RAW photo", "color graded", "professionally retouched"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "gentle orbit, slow 360 rotation",
        "aspect": "1:1",
    },
    "architecture": {
        "camera": "shot on Phase One IQ4 150MP",
        "lens": "24-70mm f/2.8 zoom",
        "aperture": "f/8 landscape focus",
        "lighting": "blue hour lighting",
        "dof": "sharp subject with soft background",
        "quality": ["ultra-detailed", "100 megapixel resolution", "award-winning photography"],
        "post": ["RAW photo", "HDR details", "dodge and burn"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "slow crane up, tilt reveal",
        "aspect": "16:9",
    },
    "wildlife": {
        "camera": "shot on Nikon Z9",
        "lens": "200mm f/2.0 telephoto",
        "aperture": "f/2.8",
        "lighting": "golden hour lighting",
        "dof": "shallow depth of field",
        "quality": ["ultra-detailed", "National Geographic quality", "professional photography"],
        "post": ["RAW photo", "color graded"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "tracking shot, telephoto drift",
        "aspect": "16:9",
    },
    "cinematic": {
        "camera": "shot on Canon EOS R5",
        "lens": "50mm f/1.2 prime lens",
        "aperture": "f/1.8 shallow depth of field",
        "lighting": "cinematic chiaroscuro",
        "dof": "razor thin focus plane",
        "quality": ["ultra-detailed", "photorealistic", "8K UHD"],
        "post": ["Kodak Vision3 500T cinema film", "color graded", "anamorphic lens flare"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "dolly zoom, slow push-in",
        "aspect": "2.39:1",
    },

    # ── Influencer & Social Media presets ─────────────────────────────────────
    "lifestyle": {
        "camera": "shot on Sony A7R V",
        "lens": "35mm f/1.4 prime lens",
        "aperture": "f/2.0",
        "lighting": "golden hour lighting",
        "dof": "sharp subject with soft background",
        "quality": ["ultra-detailed", "magazine cover quality", "professional photography"],
        "post": ["RAW photo", "Kodak Portra 400 film", "color graded"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "handheld candid tracking, subtle drift",
        "aspect": "4:5",
        "style_notes": "authentic, candid, warm tones, lifestyle brand feel",
    },
    "fashion": {
        "camera": "shot on Hasselblad X2D 100C",
        "lens": "85mm f/1.4 prime lens",
        "aperture": "f/2.0",
        "lighting": "editorial strobe lighting",
        "dof": "sharp subject with soft background",
        "quality": ["ultra-detailed", "Vogue editorial quality", "Harper's Bazaar editorial"],
        "post": ["RAW photo", "professionally retouched", "high contrast color grade"],
        "negative": NEGATIVE_FASHION,
        "video_motion": "slow elegant pan, model walk tracking",
        "aspect": "4:5",
        "style_notes": "high fashion, editorial, luxury brand, couture",
    },
    "beauty": {
        "camera": "shot on Canon EOS R5",
        "lens": "100mm f/2.8 macro",
        "aperture": "f/4.0",
        "lighting": "beauty dish with fill card",
        "dof": "razor thin focus plane",
        "quality": ["ultra-detailed", "pore-level detail", "magazine cover quality"],
        "post": ["RAW photo", "frequency separation retouching", "skin texture preserved"],
        "negative": NEGATIVE_BEAUTY,
        "video_motion": "slow push-in to face, subtle breathing motion",
        "aspect": "1:1",
        "style_notes": "flawless skin, catchlights, beauty editorial",
    },
    "food": {
        "camera": "shot on Sony A7R V",
        "lens": "90mm f/2.8 tilt-shift",
        "aperture": "f/2.8",
        "lighting": "soft north-facing window light",
        "dof": "shallow depth of field",
        "quality": ["ultra-detailed", "magazine cover quality", "professional photography"],
        "post": ["RAW photo", "warm color grade", "professionally retouched"],
        "negative": NEGATIVE_FOOD,
        "video_motion": "slow overhead crane, gentle steam particle movement",
        "aspect": "1:1",
        "style_notes": "appetizing, fresh, warm tones, props, garnish detail",
    },
    "travel": {
        "camera": "shot on Sony A1",
        "lens": "24mm f/1.4 wide angle",
        "aperture": "f/5.6 deep focus",
        "lighting": "golden hour lighting",
        "dof": "deep focus",
        "quality": ["ultra-detailed", "National Geographic quality", "award-winning photography"],
        "post": ["RAW photo", "color graded", "atmospheric haze"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "slow sweeping pan, environmental reveal",
        "aspect": "16:9",
        "style_notes": "wanderlust, adventure, destination, sense of scale",
    },
    "fitness": {
        "camera": "shot on Canon EOS R3",
        "lens": "70-200mm f/2.8 telephoto zoom",
        "aperture": "f/2.8",
        "lighting": "dramatic side light, motivated sunlight",
        "dof": "subject separation",
        "quality": ["ultra-detailed", "professional photography", "dynamic motion"],
        "post": ["RAW photo", "high contrast color grade", "muscle definition enhanced"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "dynamic tracking, slow motion impact frames",
        "aspect": "4:5",
        "style_notes": "athletic, powerful, sweat texture, muscle definition, energy",
    },
    "social_story": {
        "camera": "shot on Sony A7R V",
        "lens": "35mm f/1.4 prime lens",
        "aperture": "f/2.0",
        "lighting": "soft natural window light",
        "dof": "sharp subject with soft background",
        "quality": ["ultra-detailed", "professional photography", "magazine cover quality"],
        "post": ["RAW photo", "color graded", "professionally retouched"],
        "negative": NEGATIVE_REALISM,
        "video_motion": "handheld intimate feel, slight drift",
        "aspect": "9:16",
        "style_notes": "vertical format, bold, punchy, swipe-stopping, social-first",
    },
    "editorial": {
        "camera": "shot on Hasselblad X2D 100C",
        "lens": "85mm f/1.4 prime lens",
        "aperture": "f/1.8 shallow depth of field",
        "lighting": "high-contrast fashion lighting",
        "dof": "creamy bokeh background",
        "quality": ["ultra-detailed", "Harper's Bazaar editorial", "luxury brand campaign"],
        "post": ["RAW photo", "color graded", "professionally retouched"],
        "negative": NEGATIVE_FASHION,
        "video_motion": "slow dolly reveal, editorial pace",
        "aspect": "4:5",
        "style_notes": "conceptual, story-driven, high art direction, mood",
    },
}
