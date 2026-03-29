"""
Realism modifier libraries for OpenArt and Higgsfield prompt engineering.
Each category provides curated tokens that push generation toward photorealism.
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
]

LENSES = [
    "85mm f/1.4 prime lens",
    "50mm f/1.2 prime lens",
    "35mm f/1.4 prime lens",
    "135mm f/1.8 telephoto",
    "24-70mm f/2.8 zoom",
    "100mm f/2.8 macro",
    "200mm f/2.0 telephoto",
]

APERTURE = [
    "f/1.4 wide open",
    "f/1.8 shallow depth of field",
    "f/2.8",
    "f/5.6 deep focus",
    "f/8 landscape focus",
]

SHUTTER_SPEED = [
    "1/2000s",
    "1/500s",
    "1/250s",
    "1/60s",
    "30s long exposure",
]

ISO = [
    "ISO 100",
    "ISO 400",
    "ISO 800",
    "ISO 3200 high ISO grain",
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
]

# ── Film & Sensor Characteristics ─────────────────────────────────────────────
FILM_LOOKS = [
    "Kodak Portra 400 film",
    "Kodak Ektar 100 film",
    "Fujifilm Pro 400H film",
    "Ilford HP5 black and white film",
    "Cinestill 800T film",
    "Kodak Vision3 500T cinema film",
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
]

# ── Negative Prompts ──────────────────────────────────────────────────────────
NEGATIVE_REALISM = (
    "painting, illustration, drawing, cartoon, anime, sketch, render, CGI, "
    "3D render, digital art, concept art, low quality, blurry, out of focus, "
    "grainy, noisy, overexposed, underexposed, bad anatomy, distorted, "
    "watermark, text, logo, signature, extra limbs, disfigured, ugly, "
    "amateur, plastic skin, airbrushed, unrealistic colors, flat lighting, "
    "oversaturated, HDR overdone"
)

# ── Shot Type Presets ─────────────────────────────────────────────────────────
SHOT_PRESETS = {
    "portrait": {
        "camera": "shot on Sony A7R V",
        "lens": "85mm f/1.4 prime lens",
        "aperture": "f/1.8 shallow depth of field",
        "lighting": "Rembrandt lighting",
        "dof": "creamy bokeh background",
        "quality": ["ultra-detailed", "pore-level detail", "professional photography"],
        "post": ["RAW photo", "professionally retouched", "skin texture preserved"],
    },
    "landscape": {
        "camera": "shot on Hasselblad X2D 100C",
        "lens": "24-70mm f/2.8 zoom",
        "aperture": "f/8 landscape focus",
        "lighting": "golden hour lighting",
        "dof": "deep focus",
        "quality": ["ultra-detailed", "8K UHD", "award-winning photography"],
        "post": ["RAW photo", "HDR details", "color graded"],
    },
    "street": {
        "camera": "shot on Leica M11",
        "lens": "35mm f/1.4 prime lens",
        "aperture": "f/2.8",
        "lighting": "overcast soft diffused light",
        "dof": "subject separation",
        "quality": ["photojournalistic", "ultra-detailed", "professional photography"],
        "post": ["RAW photo", "Kodak Portra 400 film"],
    },
    "product": {
        "camera": "shot on Canon EOS R5",
        "lens": "100mm f/2.8 macro",
        "aperture": "f/5.6 deep focus",
        "lighting": "three-point studio lighting",
        "dof": "tack sharp focus",
        "quality": ["ultra-detailed", "magazine cover quality", "8K UHD"],
        "post": ["RAW photo", "color graded", "professionally retouched"],
    },
    "architecture": {
        "camera": "shot on Phase One IQ4 150MP",
        "lens": "24-70mm f/2.8 zoom",
        "aperture": "f/8 landscape focus",
        "lighting": "blue hour lighting",
        "dof": "sharp subject with soft background",
        "quality": ["ultra-detailed", "100 megapixel resolution", "award-winning photography"],
        "post": ["RAW photo", "HDR details", "dodge and burn"],
    },
    "wildlife": {
        "camera": "shot on Nikon Z9",
        "lens": "200mm f/2.0 telephoto",
        "aperture": "f/2.8",
        "lighting": "golden hour lighting",
        "dof": "shallow depth of field",
        "quality": ["ultra-detailed", "National Geographic quality", "professional photography"],
        "post": ["RAW photo", "color graded"],
    },
    "cinematic": {
        "camera": "shot on Canon EOS R5",
        "lens": "50mm f/1.2 prime lens",
        "aperture": "f/1.8 shallow depth of field",
        "lighting": "cinematic chiaroscuro",
        "dof": "razor thin focus plane",
        "quality": ["ultra-detailed", "photorealistic", "8K UHD"],
        "post": ["Kodak Vision3 500T cinema film", "color graded", "anamorphic lens flare"],
    },
}
