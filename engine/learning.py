"""
Learning & Education module for the Psychic Disco prompt system.

Provides curated technique libraries, tips, tutorials, and the ability
to generate AI-powered explanations using Claude.
"""
from __future__ import annotations

import os
from typing import Optional

import anthropic


# ─────────────────────────────────────────────────────────────────────────────
# Curated technique library
# ─────────────────────────────────────────────────────────────────────────────

TECHNIQUE_LIBRARY = {
    "lighting": {
        "title": "Lighting Masterclass",
        "techniques": [
            {
                "name": "Golden Hour Photography",
                "level": "beginner",
                "description": "The hour after sunrise and before sunset produces warm, soft, directional light. The low sun angle creates long shadows and wraps light around subjects naturally.",
                "prompt_tokens": "golden hour lighting, warm amber light, long shadows, rim light",
                "best_for": ["portrait", "landscape", "lifestyle", "travel"],
                "tips": [
                    "Shoot within 30 minutes of sunrise/sunset for the best light",
                    "Position subject with sun behind or 45° to the side for rim light",
                    "Use a reflector to fill shadows on the face",
                    "Set white balance to 'Cloudy' (5500-6000K) to enhance warmth",
                ],
            },
            {
                "name": "Rembrandt Lighting",
                "level": "intermediate",
                "description": "A classic portrait lighting setup where a small triangle of light appears on the shadow side of the face. Creates depth and drama.",
                "prompt_tokens": "Rembrandt lighting, triangle of light on cheek, dramatic shadows, moody portrait",
                "best_for": ["portrait", "editorial", "cinematic"],
                "tips": [
                    "Place the key light at 45° to subject, slightly above eye level",
                    "The triangle of light should appear on the shadowed cheek",
                    "Use a ratio of 3:1 or 4:1 for dramatic results",
                    "Works best with directional, focused light sources",
                ],
            },
            {
                "name": "Beauty Dish Lighting",
                "level": "intermediate",
                "description": "A concave metallic dish modifier that creates a distinctive hard-yet-flattering light with a dark center spot. The industry standard for beauty and fashion.",
                "prompt_tokens": "beauty dish with fill card, catchlights, soft hard light, beauty editorial",
                "best_for": ["beauty", "fashion", "portrait"],
                "tips": [
                    "Use a white beauty dish for softer light, silver for more punch",
                    "Add a fill card below the chin to eliminate unflattering shadows",
                    "Distance affects hardness: closer = softer (larger relative source)",
                    "Combine with a strip box for background separation",
                ],
            },
            {
                "name": "Cinematic Chiaroscuro",
                "level": "advanced",
                "description": "The dramatic interplay of deep shadows and bright highlights used in film noir and high-end cinema. Inspired by Caravaggio's paintings.",
                "prompt_tokens": "cinematic chiaroscuro, deep shadows, motivated lighting, film noir, single key light",
                "best_for": ["cinematic", "editorial", "portrait"],
                "tips": [
                    "Use a single hard light source and let shadows fall naturally",
                    "No fill light — embrace the darkness for drama",
                    "Motivated lighting means light appears to come from a natural source in scene",
                    "Add a subtle practical light (candle, lamp) in frame for authenticity",
                ],
            },
            {
                "name": "Clamshell Lighting",
                "level": "beginner",
                "description": "Two softboxes above and below the subject facing each other, creating even, flattering light with minimal shadows. The go-to for beauty and headshots.",
                "prompt_tokens": "clamshell lighting setup, even beauty light, soft catchlights, commercial headshot",
                "best_for": ["beauty", "portrait", "product"],
                "tips": [
                    "Top light is the key, bottom light is a fill (weaker by 1-2 stops)",
                    "The V-flat or beauty dish below acts as a giant reflector",
                    "Adjust the lower light distance to control shadow fill",
                    "Add a hair light from behind for separation from background",
                ],
            },
        ],
    },
    "lenses": {
        "title": "Lens Selection Guide",
        "techniques": [
            {
                "name": "85mm Portrait Lens",
                "level": "beginner",
                "description": "The industry standard portrait focal length. At f/1.4-1.8, it creates beautiful subject separation, natural perspective, and flattering compression without distortion.",
                "prompt_tokens": "85mm f/1.4 prime lens, natural portrait perspective, creamy bokeh, subject separation",
                "best_for": ["portrait", "fashion", "beauty", "editorial"],
                "tips": [
                    "Shoot at f/1.4-2.0 for maximum bokeh and subject pop",
                    "Keep at least 5-8 feet from subject for natural perspective",
                    "The 85mm avoids the nose-enlargement distortion of wider lenses",
                    "Best for upper body to environmental portraits",
                ],
            },
            {
                "name": "35mm Street Lens",
                "level": "beginner",
                "description": "The quintessential street photography focal length. Close to human field of view, allowing environmental context while maintaining intimacy.",
                "prompt_tokens": "35mm f/1.4 prime lens, environmental context, street photography, Leica perspective",
                "best_for": ["street", "lifestyle", "travel", "documentary"],
                "tips": [
                    "Get closer than feels comfortable — 35mm rewards proximity",
                    "Zone focus at f/5.6-f/8 for fast candid shooting",
                    "Slight wide-angle distortion adds dynamism to compositions",
                    "Great for environmental portraits that show the setting",
                ],
            },
            {
                "name": "100mm Macro",
                "level": "intermediate",
                "description": "A true macro lens capable of 1:1 reproduction for extreme close-up details. Also an exceptional portrait and product lens with gorgeous bokeh.",
                "prompt_tokens": "100mm f/2.8 macro, extreme close-up detail, 1:1 macro reproduction, micro texture",
                "best_for": ["beauty", "food", "product", "wildlife"],
                "tips": [
                    "Use at 1:1 for skin texture, fabric weave, flower pistils",
                    "At f/2.8 as a portrait lens it rivals dedicated portrait primes",
                    "Depth of field is razor thin at macro distances — use a tripod",
                    "For product photography, shoot at f/8-11 for maximum detail sharpness",
                ],
            },
            {
                "name": "200mm Telephoto",
                "level": "intermediate",
                "description": "Extreme background compression and subject isolation. At f/2.0-2.8 it produces out-of-focus backgrounds that are almost painterly.",
                "prompt_tokens": "200mm f/2.0 telephoto, extreme background compression, painterly bokeh, telephoto reach",
                "best_for": ["wildlife", "sports", "fashion", "portrait"],
                "tips": [
                    "Background compression makes distant objects appear closer to subject",
                    "At f/2.0 the bokeh is buttery smooth and almost surreal",
                    "Minimum shutter speed: 1/400s+ to avoid camera shake",
                    "Use for fashion to isolate model from a busy location background",
                ],
            },
            {
                "name": "Tilt-Shift for Food & Architecture",
                "level": "advanced",
                "description": "A specialized lens that controls the plane of focus and perspective independently. Eliminates keystoning in architecture and creates selective focus effects in food photography.",
                "prompt_tokens": "tilt-shift lens, miniature effect, selective focus plane, perspective correction",
                "best_for": ["food", "architecture", "product"],
                "tips": [
                    "Tilt moves the focus plane; shift corrects converging vertical lines",
                    "For food: tilt the focus plane along the table surface at an angle",
                    "For architecture: shift up to keep building lines perfectly vertical",
                    "The miniature tilt-shift effect works on cityscape aerials",
                ],
            },
        ],
    },
    "composition": {
        "title": "Composition Techniques",
        "techniques": [
            {
                "name": "Rule of Thirds",
                "level": "beginner",
                "description": "Divide the frame into a 3x3 grid. Place key subjects and horizons on the grid lines or intersection points for dynamic, naturally balanced images.",
                "prompt_tokens": "rule of thirds composition, off-center subject, dynamic balance",
                "best_for": ["all"],
                "tips": [
                    "Eyes belong on the top third line, not the center of frame",
                    "Horizons should follow the upper or lower third, not the middle",
                    "Leave 'look space' in the direction the subject is facing",
                    "Breaking the rule intentionally can create powerful centered compositions",
                ],
            },
            {
                "name": "Environmental Portraiture",
                "level": "intermediate",
                "description": "Including the subject's environment to tell a story about who they are. The setting becomes a character in the image.",
                "prompt_tokens": "environmental portrait, context-rich setting, storytelling composition, 35mm environmental",
                "best_for": ["lifestyle", "editorial", "travel", "street"],
                "tips": [
                    "Show enough environment to tell a story without cluttering the frame",
                    "The subject should be clearly the main element despite the environment",
                    "Leading lines in the environment should direct to the subject",
                    "Use the environment's natural frames (doorways, windows, arches)",
                ],
            },
            {
                "name": "Flat Lay & Overhead Composition",
                "level": "beginner",
                "description": "A bird's-eye view with the camera directly overhead. Essential for food, fashion, and lifestyle content. Props and negative space are critical.",
                "prompt_tokens": "flat lay overhead shot, bird's eye composition, styled props, negative space",
                "best_for": ["food", "product", "lifestyle", "fashion"],
                "tips": [
                    "Use a spirit level to ensure the camera is perfectly horizontal",
                    "Odd numbers of props feel more natural than even numbers",
                    "Negative space (empty areas) is as important as the subject",
                    "Create diagonal or triangular arrangements of props",
                ],
            },
        ],
    },
    "platforms": {
        "title": "Platform-Specific Mastery",
        "techniques": [
            {
                "name": "MidJourney v6 Mastery",
                "level": "intermediate",
                "description": "MidJourney v6 excels at photorealism with --style raw. The stylize parameter (--s) controls adherence to prompt vs. MJ's artistic interpretation.",
                "prompt_tokens": "photorealistic, ultra-detailed, --style raw --ar 3:4 --s 750 --v 6.1",
                "best_for": ["portrait", "fashion", "editorial", "lifestyle"],
                "tips": [
                    "--style raw keeps output closest to your prompt description",
                    "--s 100-400 = less MJ influence, more literal; --s 750-1000 = more stylized",
                    "Aspect ratios: --ar 3:4 (portrait), --ar 16:9 (landscape), --ar 9:16 (story)",
                    "Use --no to exclude elements: --no text, watermark, cartoon, anime",
                    "Photographer names work well: 'photographed by Annie Leibovitz'",
                ],
            },
            {
                "name": "Runway Gen-3 Prompting",
                "level": "intermediate",
                "description": "Runway Gen-3 Alpha responds best to action-first prompts with clear camera motion described at the beginning. Duration up to 10 seconds.",
                "prompt_tokens": "cinematic tracking shot, smooth camera motion, 4K photorealistic video",
                "best_for": ["portrait", "fashion", "lifestyle", "cinematic"],
                "tips": [
                    "Start the prompt with camera movement: 'Slow push-in toward...'",
                    "Describe what's changing in the scene for more dynamic results",
                    "Use 'no camera shake', 'smooth motion' to stabilize output",
                    "Gen-3 Turbo is faster but Gen-3 Alpha has better motion quality",
                    "Extend clips by feeding the last frame back as an image prompt",
                ],
            },
            {
                "name": "DALL-E 3 Natural Language",
                "level": "beginner",
                "description": "DALL-E 3 is unique: it works better with detailed natural language descriptions than comma-separated tokens. Describe the scene as you would to a human photographer.",
                "prompt_tokens": "Describe as natural sentences: 'A professional photograph of...'",
                "best_for": ["portrait", "lifestyle", "product", "food"],
                "tips": [
                    "Write in complete sentences, not comma-separated tokens",
                    "Include 'photorealistic, no artistic interpretation' to prevent stylization",
                    "Set style to 'natural' (not 'vivid') for photorealism",
                    "Be very explicit: DALL-E 3 will follow instructions more literally than MJ",
                    "Mention 'professional photographer', 'shot on camera' to anchor realism",
                ],
            },
            {
                "name": "Pika 2.0 Motion Control",
                "level": "intermediate",
                "description": "Pika excels at short-form social media video. Motion strength 1-3 for subtle realistic movement, 4-7 for dynamic motion.",
                "prompt_tokens": "photorealistic, smooth motion, cinematic quality",
                "best_for": ["lifestyle", "fashion", "beauty", "social_story"],
                "tips": [
                    "Motion strength 1-3: subtle, realistic — great for portraits and beauty",
                    "Motion strength 4-7: dynamic — best for action, travel, fitness",
                    "Start from an image for the most controlled results",
                    "9:16 aspect ratio is optimized for TikTok and Instagram Reels",
                    "Use scene and lip sync features for influencer content",
                ],
            },
        ],
    },
    "content_strategy": {
        "title": "Content Strategy & Automation",
        "techniques": [
            {
                "name": "Content Batching with Google Sheets",
                "level": "beginner",
                "description": "Use a Google Sheet as a content calendar and prompt database. Generate multiple prompts in batch, track what performed well, and automate your workflow.",
                "prompt_tokens": "N/A — workflow technique",
                "best_for": ["all"],
                "tips": [
                    "Create columns: Date, Brief, Shot Type, Platform, Prompt, Status, Performance",
                    "Use Psychic Disco's batch API to generate 50+ prompts at once",
                    "Track which prompt styles get the most engagement",
                    "Build a library of winning prompts for each content category",
                    "Schedule content 2 weeks in advance using the content calendar",
                ],
            },
            {
                "name": "Influencer Content Pillars",
                "level": "beginner",
                "description": "Successful influencer accounts are built on 3-5 content pillars. Each pillar has consistent visual aesthetics defined by specific prompt settings.",
                "prompt_tokens": "N/A — strategy technique",
                "best_for": ["all"],
                "tips": [
                    "Define 3-5 content pillars (e.g. beauty, travel, lifestyle, behind-the-scenes)",
                    "Each pillar should have a consistent color grade and lighting style",
                    "Create preset prompt templates for each pillar",
                    "Maintain visual cohesion: same camera/lens/color grade across a pillar",
                    "Post ratio: 2:1 value content to promotional content",
                ],
            },
            {
                "name": "Nano Banana Automation",
                "level": "intermediate",
                "description": "Nano Banana can trigger prompt generation via webhooks, integrate with your social scheduling tools, and automate the content production pipeline.",
                "prompt_tokens": "N/A — automation technique",
                "best_for": ["all"],
                "tips": [
                    "Set up a webhook to trigger batch generation when you add rows to Google Sheets",
                    "Use Nano Banana to automatically post generated images to scheduled platforms",
                    "Create automation: Brief → Generate → Review → Schedule → Post",
                    "Build a Zap: New Sheet Row → Psychic Disco API → Save result → Schedule",
                    "Use the batch endpoint for cost-effective bulk generation",
                ],
            },
        ],
    },
    "color_grading": {
        "title": "Color Grading & Film Aesthetics",
        "techniques": [
            {
                "name": "Kodak Portra 400 Look",
                "level": "beginner",
                "description": "The most beloved color negative film. Warm skin tones, slightly desaturated greens/blues, lifted shadows, and a subtle grain structure that feels organic.",
                "prompt_tokens": "Kodak Portra 400 film, warm skin tones, lifted shadows, organic grain, film photography",
                "best_for": ["portrait", "lifestyle", "fashion", "wedding"],
                "tips": [
                    "Lift the blacks/shadows to around 10-20% for that film-like quality",
                    "Pull cyan out of skin tones, push toward warm orange",
                    "Desaturate greens and blues by 15-20%",
                    "Add a very subtle warm color cast in the highlights",
                    "Keep saturation moderate — Portra is about refined color, not vivid",
                ],
            },
            {
                "name": "Cinestill 800T Night Look",
                "level": "intermediate",
                "description": "Cinestill 800T is a tungsten-balanced cinema film. Under artificial light it goes warm; under daylight it goes cool. The 'halation' effect creates red glows around bright lights.",
                "prompt_tokens": "Cinestill 800T film, tungsten color cast, neon halation, high ISO grain, night photography",
                "best_for": ["cinematic", "street", "editorial", "nightlife"],
                "tips": [
                    "The red halation glow around highlights is the signature look",
                    "Under tungsten light: warm, golden, creamy",
                    "Under daylight: cool, blue-tinted, moody",
                    "High ISO grain adds texture and authenticity",
                    "Push the exposure 1-2 stops in post for the proper Cinestill feel",
                ],
            },
            {
                "name": "Editorial Matte Color Grade",
                "level": "intermediate",
                "description": "The classic fashion editorial look: lifted blacks, slightly desaturated palette, strong contrast in the mids, and a sophisticated color cast. Think Vogue and i-D.",
                "prompt_tokens": "editorial matte color grade, lifted blacks, desaturated palette, fashion magazine aesthetic",
                "best_for": ["fashion", "editorial", "beauty", "portrait"],
                "tips": [
                    "Lift the black point to 15-20% to create the matte fade",
                    "Use an S-curve with strong contrast in the midtones",
                    "Apply a subtle teal or green cast to shadows",
                    "Keep highlights slightly warm and clean",
                    "Reduce overall saturation by 10-15% then selectively boost skin tones",
                ],
            },
        ],
    },
}

SHOT_TYPE_GUIDES = {
    shot: {
        "recommended_lenses": [],
        "ideal_lighting": [],
        "key_techniques": [],
    }
    for shot in [
        "portrait", "landscape", "street", "product", "architecture",
        "wildlife", "cinematic", "lifestyle", "fashion", "beauty",
        "food", "travel", "fitness", "social_story", "editorial",
    ]
}


# ─────────────────────────────────────────────────────────────────────────────
# AI-powered learning explanations
# ─────────────────────────────────────────────────────────────────────────────

async def explain_technique(
    technique_name: str,
    user_level: str = "beginner",
    api_key: Optional[str] = None,
) -> str:
    """
    Use Claude to generate a detailed, personalized explanation of a
    photography/AI prompting technique tailored to the user's level.

    Parameters
    ----------
    technique_name : str
        The technique to explain (e.g. 'Rembrandt lighting', 'MidJourney --style raw')
    user_level : str
        'beginner', 'intermediate', or 'advanced'
    api_key : str, optional
        Anthropic API key.

    Returns
    -------
    str — detailed explanation with practical tips and example prompts
    """
    client = anthropic.AsyncAnthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    system = (
        "You are a master photography educator and AI prompt engineering expert. "
        "You teach with clarity, enthusiasm, and practical examples. "
        "Always include: what the technique is, why it works, how to apply it in AI prompts, "
        "and 3 concrete example prompt snippets."
    )

    async with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=1500,
        thinking={"type": "adaptive"},
        system=system,
        messages=[{
            "role": "user",
            "content": (
                f"Explain '{technique_name}' for a {user_level} level creator. "
                f"Include: clear explanation, why it creates better results, "
                f"how to use it in AI image/video prompts, and 3 example prompt snippets. "
                f"Be encouraging and practical."
            )
        }],
    ) as stream:
        final = await stream.get_final_message()

    for block in final.content:
        if block.type == "text":
            return block.text

    return "Unable to generate explanation."


async def generate_learning_path(
    goal: str,
    current_level: str = "beginner",
    api_key: Optional[str] = None,
) -> dict:
    """
    Generate a personalized learning path based on the user's goal.

    Parameters
    ----------
    goal : str
        What the user wants to achieve (e.g. 'become a fashion content creator')
    current_level : str
        'beginner', 'intermediate', or 'advanced'
    api_key : str, optional

    Returns
    -------
    dict with learning path, milestones, and recommended techniques
    """
    client = anthropic.AsyncAnthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    system = (
        "You are an expert content creation coach specializing in AI-powered visual content. "
        "Create structured, actionable learning paths. "
        "Respond with valid JSON only, no markdown."
    )

    async with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=2000,
        thinking={"type": "adaptive"},
        system=system,
        messages=[{
            "role": "user",
            "content": (
                f"Create a learning path for: '{goal}'\n"
                f"Current level: {current_level}\n\n"
                f"Return JSON with:\n"
                f"- title: string\n"
                f"- overview: string\n"
                f"- milestones: array of {{week, focus, techniques, prompts_to_practice}}\n"
                f"- recommended_platforms: array of platform names\n"
                f"- first_prompt_to_try: string (an actual AI image prompt to start with)"
            )
        }],
    ) as stream:
        final = await stream.get_final_message()

    raw = ""
    for block in final.content:
        if block.type == "text":
            raw = block.text.strip()
            break

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    import json
    return json.loads(raw)


def get_all_techniques() -> list[dict]:
    """Return a flat list of all techniques for the learning library UI."""
    techniques = []
    for category_key, category in TECHNIQUE_LIBRARY.items():
        for technique in category["techniques"]:
            techniques.append({
                "category": category_key,
                "category_title": category["title"],
                **technique,
            })
    return techniques


def get_techniques_by_shot_type(shot_type: str) -> list[dict]:
    """Return techniques relevant to a given shot type."""
    all_techniques = get_all_techniques()
    return [
        t for t in all_techniques
        if shot_type in t.get("best_for", []) or "all" in t.get("best_for", [])
    ]
