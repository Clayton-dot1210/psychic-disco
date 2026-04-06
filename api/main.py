"""
Psychic Disco API — FastAPI backend for the AI prompt engineering system.

Endpoints:
  POST /api/generate          — NL brief → expert prompts via Claude AI
  POST /api/build             — Structured config → prompts (no AI)
  GET  /api/shot-types        — List available shot type presets
  GET  /api/platforms         — List supported platforms
  GET  /api/learn             — Full technique library
  GET  /api/learn/{category}  — Techniques by category
  GET  /api/learn/shot/{shot} — Techniques for a shot type
  POST /api/learn/explain     — AI-powered technique explanation
  POST /api/learn/path        — AI-generated learning path
  POST /api/automate/batch    — Batch generation from Google Sheets
  POST /api/automate/webhook  — Send results to any webhook
  GET  /api/health            — Health check
"""
from __future__ import annotations

import os
from typing import Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from engine.builder import PromptConfig, build
from engine.modifiers import SHOT_PRESETS, SOCIAL_FORMATS
from engine.platforms import (
    ALL_PLATFORMS, VIDEO_PLATFORMS, IMAGE_PLATFORMS,
    format_openart, format_higgsfield, format_midjourney,
    format_runway, format_pika, format_leonardo,
    format_kling, format_dalle3, format_firefly, format_all,
    FormattedPrompt,
)
from engine.ai_interpreter import interpret_async
from engine.learning import (
    TECHNIQUE_LIBRARY, get_all_techniques,
    get_techniques_by_shot_type, explain_technique,
    generate_learning_path,
)
from engine.automation import (
    NanoBananaWebhook, run_batch_from_sheet, send_to_webhook,
    CONTENT_CALENDAR_HEADERS,
)


# ─────────────────────────────────────────────────────────────────────────────
# App setup
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Psychic Disco — AI Prompt Engineering API",
    description=(
        "Expert AI art, influencer, and video prompting system. "
        "Drop a creative brief, get expert prompts for every major AI platform."
    ),
    version="2.0.0",
)

# CORS — allow Lovable's domain and localhost for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.lovableproject.com",
        "https://*.lovable.app",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "*",  # Relax for development; tighten in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────────────────────────
# Pydantic models
# ─────────────────────────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    brief: str = Field(..., description="Natural language creative brief from the user", min_length=3)
    target_platforms: Optional[list[str]] = Field(
        None,
        description="Platforms to optimize for. Defaults to all if not specified.",
        example=["midjourney", "runway", "pika"],
    )

class BuildRequest(BaseModel):
    subject: str = Field(..., description="Scene or subject description")
    shot_type: str = Field("portrait", description="Shot type preset key")
    platform: str = Field("all", description="Target platform or 'all'")
    lighting: Optional[str] = None
    camera: Optional[str] = None
    lens: Optional[str] = None
    aperture: Optional[str] = None
    atmosphere: Optional[str] = None
    composition: Optional[str] = None
    extra_style: Optional[str] = None
    motion: Optional[str] = Field(None, description="Camera motion override for video platforms")
    randomize: bool = False
    seed: Optional[int] = None

class ExplainRequest(BaseModel):
    technique: str = Field(..., description="Technique name to explain")
    level: str = Field("beginner", description="User level: beginner, intermediate, advanced")

class LearningPathRequest(BaseModel):
    goal: str = Field(..., description="What the user wants to achieve")
    current_level: str = Field("beginner", description="beginner, intermediate, or advanced")

class BatchSheetRequest(BaseModel):
    spreadsheet_id: str = Field(..., description="Google Sheets spreadsheet ID")
    sheet_range: str = Field("Sheet1!A1:N200", description="A1 notation range")
    credentials_path: Optional[str] = Field(None, description="Path to Google service account JSON")

class WebhookRequest(BaseModel):
    webhook_url: str = Field(..., description="Target webhook URL")
    brief: str = Field(..., description="Creative brief to generate and send")
    target_platforms: Optional[list[str]] = None
    metadata: Optional[dict] = None

class FormattedPromptOut(BaseModel):
    platform: str
    positive: str
    negative: str
    parameters: dict
    copy_paste: str

    @classmethod
    def from_domain(cls, fp: FormattedPrompt) -> "FormattedPromptOut":
        return cls(
            platform=fp.platform,
            positive=fp.positive,
            negative=fp.negative,
            parameters=fp.parameters,
            copy_paste=fp.copy_paste,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "version": "2.0.0",
        "platforms_supported": len(ALL_PLATFORMS),
        "shot_types_supported": len(SHOT_PRESETS),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Core generation endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/generate")
async def generate_from_brief(request: GenerateRequest):
    """
    The main endpoint. User drops a natural language brief and gets back
    expert-crafted prompts for every requested platform, powered by Claude AI.

    Example brief:
      "a moody fashion editorial in a Paris alleyway at dusk, woman in red coat"
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ANTHROPIC_API_KEY not configured on server."
        )

    try:
        result = await interpret_async(
            user_brief=request.brief,
            target_platforms=request.target_platforms,
            api_key=api_key,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

    built = result["built_prompt"]
    platforms_out = {
        platform: FormattedPromptOut.from_domain(fp).model_dump()
        for platform, fp in result["platforms"].items()
    }

    return {
        "brief": request.brief,
        "subject": result["raw_claude"].get("subject", ""),
        "shot_type": result["raw_claude"].get("shot_type", ""),
        "creative_notes": result["creative_notes"],
        "reasoning": result["reasoning"],
        "content_format": result["content_format"],
        "motion_description": result["motion_description"],
        "base_prompt": {
            "positive": built.positive,
            "negative": built.negative,
        },
        "config": {
            "shot_type": result["config"].shot_type,
            "lighting": result["config"].lighting,
            "camera": result["config"].camera,
            "lens": result["config"].lens,
            "aperture": result["config"].aperture,
            "atmosphere": result["config"].atmosphere,
            "composition": result["config"].composition,
            "extra_style": result["config"].extra_style,
        },
        "platforms": platforms_out,
    }


@app.post("/api/build")
async def build_structured(request: BuildRequest):
    """
    Build prompts from structured config (no AI interpretation).
    Use this when you already know the exact shot type and settings.
    """
    if request.shot_type not in SHOT_PRESETS:
        available = list(SHOT_PRESETS.keys())
        raise HTTPException(
            status_code=400,
            detail=f"Unknown shot_type '{request.shot_type}'. Available: {available}"
        )

    config = PromptConfig(
        subject=request.subject,
        shot_type=request.shot_type,
        lighting=request.lighting,
        camera=request.camera,
        lens=request.lens,
        aperture=request.aperture,
        atmosphere=request.atmosphere,
        composition=request.composition,
        extra_style=request.extra_style,
        randomize=request.randomize,
        seed=request.seed,
    )
    built = build(config)

    # Format for requested platforms
    if request.platform == "all":
        formatted = format_all(built, request.motion)
    else:
        format_map = {
            "openart":    lambda p: format_openart(p),
            "higgsfield": lambda p: format_higgsfield(p, request.motion),
            "midjourney": lambda p: format_midjourney(p),
            "runway":     lambda p: format_runway(p, request.motion),
            "pika":       lambda p: format_pika(p, request.motion),
            "leonardo":   lambda p: format_leonardo(p),
            "kling":      lambda p: format_kling(p, request.motion),
            "dalle3":     lambda p: format_dalle3(p),
            "firefly":    lambda p: format_firefly(p),
        }
        fmt_fn = format_map.get(request.platform)
        if not fmt_fn:
            raise HTTPException(status_code=400, detail=f"Unknown platform '{request.platform}'")
        formatted = {request.platform: fmt_fn(built)}

    return {
        "base_prompt": {
            "positive": built.positive,
            "negative": built.negative,
        },
        "platforms": {
            p: FormattedPromptOut.from_domain(fp).model_dump()
            for p, fp in formatted.items()
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# Discovery endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/shot-types")
async def list_shot_types():
    """List all available shot type presets with their default settings."""
    shot_types = []
    for key, preset in SHOT_PRESETS.items():
        shot_types.append({
            "key": key,
            "label": key.replace("_", " ").title(),
            "camera": preset["camera"],
            "lens": preset["lens"],
            "lighting": preset["lighting"],
            "aspect": preset.get("aspect", "4:5"),
            "style_notes": preset.get("style_notes", ""),
            "video_motion": preset.get("video_motion", ""),
        })
    return {"shot_types": shot_types, "total": len(shot_types)}


@app.get("/api/platforms")
async def list_platforms():
    """List all supported AI platforms with their type (image/video)."""
    platforms = []
    for p in ALL_PLATFORMS:
        platforms.append({
            "key": p,
            "label": {
                "openart": "OpenArt (Stable Diffusion)",
                "higgsfield": "Higgsfield AI (Video)",
                "midjourney": "MidJourney v6.1",
                "runway": "Runway Gen-3 Alpha",
                "pika": "Pika 2.0",
                "leonardo": "Leonardo AI (Phoenix)",
                "kling": "Kling 2.0",
                "dalle3": "DALL-E 3",
                "firefly": "Adobe Firefly",
            }.get(p, p.title()),
            "type": "video" if p in VIDEO_PLATFORMS else "image",
            "best_for": {
                "openart": "Stable Diffusion photorealism with full control",
                "higgsfield": "Cinematic video clips with camera motion",
                "midjourney": "High quality artistic and editorial images",
                "runway": "10-second cinematic video generation",
                "pika": "Short-form social media video content",
                "leonardo": "Photorealistic images with style presets",
                "kling": "High quality video with motion control",
                "dalle3": "Natural language image generation",
                "firefly": "Adobe ecosystem, generative fill, brand-safe",
            }.get(p, ""),
        })
    return {"platforms": platforms, "total": len(platforms)}


@app.get("/api/social-formats")
async def list_social_formats():
    """List all social media format specifications."""
    formats = [
        {
            "key": key,
            "label": key.replace("_", " ").title(),
            "aspect": spec["aspect"],
            "resolution": spec["resolution"],
        }
        for key, spec in SOCIAL_FORMATS.items()
    ]
    return {"formats": formats}


# ─────────────────────────────────────────────────────────────────────────────
# Learning endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/learn")
async def get_all_learning():
    """Return the full curated technique library."""
    return {
        "categories": {
            key: {
                "title": cat["title"],
                "technique_count": len(cat["techniques"]),
                "techniques": cat["techniques"],
            }
            for key, cat in TECHNIQUE_LIBRARY.items()
        },
        "total_techniques": len(get_all_techniques()),
    }


@app.get("/api/learn/techniques")
async def get_flat_techniques():
    """Return a flat list of all techniques, useful for search and filtering."""
    return {"techniques": get_all_techniques()}


@app.get("/api/learn/category/{category}")
async def get_category(category: str):
    """Return all techniques in a specific category."""
    if category not in TECHNIQUE_LIBRARY:
        available = list(TECHNIQUE_LIBRARY.keys())
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category}' not found. Available: {available}"
        )
    cat = TECHNIQUE_LIBRARY[category]
    return {
        "category": category,
        "title": cat["title"],
        "techniques": cat["techniques"],
    }


@app.get("/api/learn/shot/{shot_type}")
async def get_techniques_for_shot(shot_type: str):
    """Return all techniques relevant to a specific shot type."""
    techniques = get_techniques_by_shot_type(shot_type)
    return {
        "shot_type": shot_type,
        "techniques": techniques,
        "count": len(techniques),
    }


@app.post("/api/learn/explain")
async def explain_technique_endpoint(request: ExplainRequest):
    """
    Use Claude AI to generate a detailed, level-appropriate explanation
    of any photography or AI prompting technique.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured.")

    valid_levels = ["beginner", "intermediate", "advanced"]
    if request.level not in valid_levels:
        raise HTTPException(status_code=400, detail=f"Level must be one of {valid_levels}")

    try:
        explanation = await explain_technique(
            technique_name=request.technique,
            user_level=request.level,
            api_key=api_key,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")

    return {
        "technique": request.technique,
        "level": request.level,
        "explanation": explanation,
    }


@app.post("/api/learn/path")
async def learning_path_endpoint(request: LearningPathRequest):
    """
    Generate a personalized AI-powered learning path toward any content creation goal.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured.")

    try:
        path = await generate_learning_path(
            goal=request.goal,
            current_level=request.current_level,
            api_key=api_key,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning path generation failed: {str(e)}")

    return path


# ─────────────────────────────────────────────────────────────────────────────
# Automation endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/api/automate/batch-sheet")
async def batch_from_google_sheet(request: BatchSheetRequest, background_tasks: BackgroundTasks):
    """
    Read creative briefs from a Google Sheet, generate expert prompts for each,
    and write the results back to the sheet.

    The sheet must have the following columns:
    Date | Status | Brief | Shot Type | Target Platform | Social Format |
    Generated Prompt (Positive) | Generated Prompt (Negative) |
    MidJourney Command | Runway Prompt | Pika Prompt |
    Creative Notes | Performance Score | Notes

    Rows with Status = 'TODO' or empty will be processed.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured.")

    try:
        result = await run_batch_from_sheet(
            spreadsheet_id=request.spreadsheet_id,
            sheet_range=request.sheet_range,
            credentials_path=request.credentials_path,
            api_key=api_key,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")

    return result


@app.get("/api/automate/sheet-template")
async def get_sheet_template():
    """
    Return the column headers for setting up a content calendar Google Sheet.
    Copy these headers into row 1 of your sheet.
    """
    return {
        "headers": CONTENT_CALENDAR_HEADERS,
        "instructions": (
            "Create a Google Sheet with these headers in row 1. "
            "Fill in 'Brief' column with your creative ideas and set 'Status' to 'TODO'. "
            "Use the batch-sheet endpoint to auto-generate all prompts."
        ),
    }


@app.post("/api/automate/webhook")
async def generate_and_webhook(request: WebhookRequest):
    """
    Generate prompts from a brief and immediately send the result to any webhook URL.
    Compatible with Nano Banana, Zapier, Make (Integromat), n8n, and custom webhooks.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured.")

    try:
        result = await interpret_async(
            user_brief=request.brief,
            target_platforms=request.target_platforms,
            api_key=api_key,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

    built = result["built_prompt"]
    platforms_payload = {
        platform: {
            "positive": fp.positive,
            "negative": fp.negative,
            "copy_paste": fp.copy_paste,
            "parameters": fp.parameters,
        }
        for platform, fp in result["platforms"].items()
    }

    payload = {
        "brief": request.brief,
        "subject": result["raw_claude"].get("subject", ""),
        "shot_type": result["raw_claude"].get("shot_type", ""),
        "creative_notes": result["creative_notes"],
        "base_positive_prompt": built.positive,
        "base_negative_prompt": built.negative,
        "platforms": platforms_payload,
        "metadata": request.metadata or {},
    }

    try:
        webhook_result = await send_to_webhook(request.webhook_url, payload)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Prompts generated but webhook delivery failed: {str(e)}"
        )

    return {
        "generated": True,
        "webhook_delivered": True,
        "webhook_status": webhook_result.get("status"),
        "platforms_generated": list(result["platforms"].keys()),
    }


@app.post("/api/automate/nano-banana")
async def generate_and_nano_banana(request: WebhookRequest):
    """
    Generate prompts and send to a Nano Banana webhook with structured payload.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured.")

    try:
        result = await interpret_async(
            user_brief=request.brief,
            target_platforms=request.target_platforms,
            api_key=api_key,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

    nb = NanoBananaWebhook(webhook_url=request.webhook_url)
    try:
        nb_result = await nb.send_generated_prompts(
            interpretation_result=result,
            metadata=request.metadata,
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Prompts generated but Nano Banana delivery failed: {str(e)}"
        )

    return {
        "generated": True,
        "nano_banana_delivered": True,
        "status": nb_result.get("status"),
        "platforms_generated": list(result["platforms"].keys()),
        "creative_notes": result["creative_notes"],
    }
