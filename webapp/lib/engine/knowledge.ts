/**
 * Comprehensive photography & cinematography knowledge base.
 *
 * This is the "expert brain" of the prompt engine — encodes professional
 * knowledge about lenses, camera angles, lighting, and outcome scenarios
 * so the system can recommend the right combination for any creative goal.
 */

import type {
  LensProfile,
  AngleProfile,
  OutcomeProfile,
  LensType,
  CameraAngle,
  OutcomeScenario,
} from "./types";

// ─── Lens profiles ────────────────────────────────────────────────────────────

export const LENS_PROFILES: Record<LensType, LensProfile> = {
  "14mm_ultra_wide": {
    key: "14mm_ultra_wide",
    label: "14mm Ultra Wide",
    focalLength: "14mm",
    fov: "114°",
    character:
      "Extreme perspective distortion, dramatic environmental context, immersive scale",
    bestFor: ["establishing shots", "architectural drama", "POV immersion", "pattern interrupt hooks"],
    promptToken: "14mm ultra-wide angle lens, extreme perspective, dramatic distortion",
    apertureRange: "f/2.8 – f/8",
  },
  "24mm_wide": {
    key: "24mm_wide",
    label: "24mm Wide",
    focalLength: "24mm",
    fov: "84°",
    character:
      "Environmental storytelling, subject in context, slight wide feel without heavy distortion",
    bestFor: ["street photography", "lifestyle", "environmental portraits", "techwear wide shots"],
    promptToken: "24mm wide angle lens, environmental context, subtle wide perspective",
    apertureRange: "f/1.4 – f/8",
  },
  "35mm_standard_wide": {
    key: "35mm_standard_wide",
    label: "35mm Standard Wide",
    focalLength: "35mm",
    fov: "63°",
    character:
      "Human eye perspective, natural street feel, documentary authenticity",
    bestFor: ["street", "UGC", "documentary", "talking head wide"],
    promptToken: "35mm prime lens, natural perspective, street documentary feel",
    apertureRange: "f/1.4 – f/5.6",
  },
  "50mm_normal": {
    key: "50mm_normal",
    label: "50mm Normal",
    focalLength: "50mm",
    fov: "47°",
    character:
      "Closest to natural human vision, clean and unbiased, cinematic standard",
    bestFor: ["cinematic", "portrait with environment", "neutral story framing"],
    promptToken: "50mm prime lens, natural field of view, cinematic standard lens",
    apertureRange: "f/1.2 – f/8",
  },
  "85mm_portrait": {
    key: "85mm_portrait",
    label: "85mm Portrait",
    focalLength: "85mm",
    fov: "29°",
    character:
      "Flattering facial compression, subject isolation, buttery background separation",
    bestFor: ["portraits", "talking head close-up", "character hero shots", "techwear closeup"],
    promptToken: "85mm f/1.4 portrait prime lens, flattering compression, subject isolation",
    apertureRange: "f/1.2 – f/2.8",
  },
  "135mm_short_telephoto": {
    key: "135mm_short_telephoto",
    label: "135mm Short Telephoto",
    focalLength: "135mm",
    fov: "18°",
    character:
      "Strong background compression, intimate close-up feel from distance, editorial depth",
    bestFor: ["editorial portraits", "fashion", "candid street", "emotional isolation"],
    promptToken: "135mm f/1.8 telephoto, strong background compression, editorial depth",
    apertureRange: "f/1.8 – f/4",
  },
  "200mm_telephoto": {
    key: "200mm_telephoto",
    label: "200mm Telephoto",
    focalLength: "200mm",
    fov: "12°",
    character:
      "Maximum background compression, subject pulled from environment, paparazzi distance feel",
    bestFor: ["wildlife", "sports", "candid urban", "voyeuristic cinematic style"],
    promptToken: "200mm f/2.0 telephoto, maximum compression, subject isolation from distance",
    apertureRange: "f/2.0 – f/4",
  },
};

// ─── Camera angle profiles ────────────────────────────────────────────────────

export const ANGLE_PROFILES: Record<CameraAngle, AngleProfile> = {
  eye_level: {
    key: "eye_level",
    label: "Eye Level",
    description: "Camera at subject's eye height — neutral, equal, conversational",
    emotionalEffect: "Relatable, trustworthy, peer-to-peer connection",
    promptToken: "eye-level camera angle, neutral perspective, direct engagement",
    bestFor: ["UGC", "talking head", "testimonials", "social proof"],
  },
  low_angle: {
    key: "low_angle",
    label: "Low Angle",
    description: "Camera below subject looking up — subject appears powerful",
    emotionalEffect: "Authority, dominance, strength, hero status",
    promptToken: "low angle shot looking up at subject, powerful perspective, hero framing",
    bestFor: ["character 28", "bold claim hooks", "brand authority", "cinematic hero"],
  },
  high_angle: {
    key: "high_angle",
    label: "High Angle",
    description: "Camera above subject looking down — vulnerability or overview",
    emotionalEffect: "Vulnerability, intimacy, or surveillance/overview",
    promptToken: "high angle looking down at subject, elevated perspective",
    bestFor: ["product reveals", "overhead lifestyle", "intimate emotional shots"],
  },
  dutch_angle: {
    key: "dutch_angle",
    label: "Dutch Angle",
    description: "Camera tilted on horizontal axis — disorientation, tension",
    emotionalEffect: "Unease, energy, disorientation, urban grit",
    promptToken: "dutch angle tilted camera, disorienting tension, dynamic composition",
    bestFor: ["pattern interrupt hooks", "urban techwear", "edgy editorial"],
  },
  birds_eye: {
    key: "birds_eye",
    label: "Bird's Eye",
    description: "Straight down from directly above — graphic, abstract",
    emotionalEffect: "Omniscient, graphic design feel, scale reveal",
    promptToken: "bird's eye view directly overhead, top-down perspective, graphic composition",
    bestFor: ["product flat lay", "establishing lifestyle", "abstract content"],
  },
  worms_eye: {
    key: "worms_eye",
    label: "Worm's Eye",
    description: "Ground-level looking up — extreme power, architectural drama",
    emotionalEffect: "Extreme power, urban scale, cinematic drama",
    promptToken: "worm's eye view from ground level looking up, extreme low perspective, urban drama",
    bestFor: ["architecture", "urban techwear", "extreme power statements", "cinematic hooks"],
  },
  over_shoulder: {
    key: "over_shoulder",
    label: "Over the Shoulder",
    description: "Camera behind subject's shoulder looking at scene/person",
    emotionalEffect: "Immersive, POV involvement, narrative conversation",
    promptToken: "over-the-shoulder shot, subject's shoulder visible in foreground, scene revealed behind",
    bestFor: ["POV hooks", "conversation scenes", "product interaction", "storytelling"],
  },
  pov: {
    key: "pov",
    label: "POV / First Person",
    description: "Camera represents subject's eyes — total immersion",
    emotionalEffect: "Full immersion, you-are-there, direct experience",
    promptToken: "first-person POV perspective, camera represents subject's eyes, immersive",
    bestFor: ["POV hooks", "experience content", "unboxing", "lifestyle immersion"],
  },
  hip_level: {
    key: "hip_level",
    label: "Hip Level",
    description: "Camera at hip/waist height — street, candid, journalistic",
    emotionalEffect: "Candid authenticity, documentary, casual street energy",
    promptToken: "hip-level camera angle, waist-height perspective, candid documentary",
    bestFor: ["street photography", "UGC lifestyle", "candid character shots"],
  },
  ground_level: {
    key: "ground_level",
    label: "Ground Level",
    description: "Camera at ground — dramatic upward perspective on subject",
    emotionalEffect: "Epic scale, cinematic presence, environmental drama",
    promptToken: "ground-level camera, shot along the ground surface looking up at subject",
    bestFor: ["techwear wide", "establishing power shots", "urban drama", "boots/shoes detail"],
  },
};

// ─── Outcome scenario profiles ────────────────────────────────────────────────

export const OUTCOME_PROFILES: Record<OutcomeScenario, OutcomeProfile> = {
  ugc_testimonial: {
    key: "ugc_testimonial",
    label: "UGC Testimonial",
    description: "Authentic, relatable person sharing real results directly to camera",
    recommendedShot: "talking_head",
    recommendedHook: "social_proof_hook",
    recommendedLens: "35mm_standard_wide",
    recommendedAngle: "eye_level",
    lightingStyle: "ring light at home, window natural light",
    motionStyle: "slow subtle push-in, handheld micro-drift",
    extraTokens: [
      "authentic candid feel", "natural skin texture", "real person energy",
      "direct eye contact", "genuine emotion", "UGC creator aesthetic",
    ],
  },
  fashion_editorial: {
    key: "fashion_editorial",
    label: "Fashion Editorial",
    description: "High-end cinematic fashion imagery with strong visual identity",
    recommendedShot: "techwear_street",
    recommendedHook: "urban_reveal",
    recommendedLens: "85mm_portrait",
    recommendedAngle: "low_angle",
    lightingStyle: "blue hour ambient, motivated practical street lighting",
    motionStyle: "slow deliberate push-in, cinematic authority framing",
    extraTokens: [
      "editorial fashion photography", "strong visual identity", "cinematic color grade",
      "high-end magazine quality", "atmospheric mood", "designer garment detail",
    ],
  },
  product_reveal: {
    key: "product_reveal",
    label: "Product Reveal",
    description: "Dramatic product showcase with desire-building visual language",
    recommendedShot: "unboxing",
    recommendedHook: "transformation_hook",
    recommendedLens: "85mm_portrait",
    recommendedAngle: "high_angle",
    lightingStyle: "three-point studio lighting, practical desk lamp",
    motionStyle: "slow reveal push-in, product focus pull, orbit",
    extraTokens: [
      "product detail sharp", "desire-inducing reveal", "clean background",
      "aspirational product presentation", "luxury feel", "material texture visible",
    ],
  },
  hook_scroll_stop: {
    key: "hook_scroll_stop",
    label: "Hook — Scroll Stop",
    description: "Maximum attention capture in the first 1-2 seconds",
    recommendedShot: "techwear_closeup",
    recommendedHook: "silent_stare",
    recommendedLens: "85mm_portrait",
    recommendedAngle: "eye_level",
    lightingStyle: "dramatic motivated lighting, strong contrast",
    motionStyle: "ultra-slow creeping push-in, almost imperceptible",
    extraTokens: [
      "scroll-stopping visual", "cannot look away", "magnetic intensity",
      "immediate attention lock", "strong subject presence",
    ],
  },
  social_proof: {
    key: "social_proof",
    label: "Social Proof",
    description: "Builds credibility through authentic result-sharing energy",
    recommendedShot: "talking_head",
    recommendedHook: "social_proof_hook",
    recommendedLens: "35mm_standard_wide",
    recommendedAngle: "eye_level",
    lightingStyle: "warm approachable home lighting, natural window light",
    motionStyle: "warm approachable push-in",
    extraTokens: [
      "genuine excited expression", "authentic result-sharing", "believable person",
      "real human imperfections", "trustworthy energy", "can't-believe-it expression",
    ],
  },
  emotional_story: {
    key: "emotional_story",
    label: "Emotional Story",
    description: "Narrative arc that creates emotional connection with viewer",
    recommendedShot: "lifestyle",
    recommendedHook: "question_hook",
    recommendedLens: "50mm_normal",
    recommendedAngle: "eye_level",
    lightingStyle: "natural warm ambient light, golden hour, overcast soft",
    motionStyle: "gentle tracking follow, intimate drift",
    extraTokens: [
      "emotional narrative depth", "human vulnerability", "authentic feeling",
      "story-driven composition", "emotional facial expression", "connection with viewer",
    ],
  },
  brand_identity: {
    key: "brand_identity",
    label: "Brand Identity",
    description: "Strong visual identity lock — consistent character, aesthetic, world",
    recommendedShot: "techwear_wide",
    recommendedHook: "urban_reveal",
    recommendedLens: "24mm_wide",
    recommendedAngle: "low_angle",
    lightingStyle: "cinematic signature lighting, strong color identity",
    motionStyle: "slow crane up reveal, brand-lock framing",
    extraTokens: [
      "strong visual brand identity", "consistent world-building",
      "signature aesthetic", "recognizable character presence",
      "cinematic quality", "aspirational brand mood",
    ],
  },
  lifestyle_content: {
    key: "lifestyle_content",
    label: "Lifestyle Content",
    description: "Aspirational day-in-life content that builds desire for the lifestyle",
    recommendedShot: "lifestyle",
    recommendedLens: "35mm_standard_wide",
    recommendedAngle: "hip_level",
    lightingStyle: "outdoor daylight, golden hour, natural ambient",
    motionStyle: "gentle tracking follow, environmental pan",
    extraTokens: [
      "aspirational lifestyle aesthetic", "authentic environmental storytelling",
      "genuine human moment", "real world texture", "desirable life quality",
    ],
  },
};

// ─── Aperture visual effects guide ───────────────────────────────────────────

export const APERTURE_GUIDE = {
  "f/1.2": {
    label: "f/1.2 — Maximum Cinematic",
    effect: "Razor-thin focus, extreme background melt, ultra-cinematic",
    bestFor: "Hero portraits, cinematic drama, character isolation",
    token: "f/1.2 wide open, razor thin focus plane, extreme cinematic bokeh",
  },
  "f/1.4": {
    label: "f/1.4 — Dreamy Separation",
    effect: "Very shallow DOF, beautiful bokeh, subject pops from background",
    bestFor: "Portraits, character shots, fashion, talking head hero",
    token: "f/1.4 wide open, dreamy background separation, buttery bokeh",
  },
  "f/1.8": {
    label: "f/1.8 — Balanced Bokeh",
    effect: "Shallow DOF with slightly more sharpness, practical cinematic",
    bestFor: "Most portrait and UGC scenarios, versatile hero shot",
    token: "f/1.8 shallow depth of field, creamy bokeh background",
  },
  "f/2.8": {
    label: "f/2.8 — Gentle Blur",
    effect: "Subject sharp, background gently blurred, environment still visible",
    bestFor: "Street, lifestyle, environmental portraits with context",
    token: "f/2.8, gentle background blur, subject in context",
  },
  "f/5.6": {
    label: "f/5.6 — Balanced Focus",
    effect: "Both subject and near-background sharp, full environmental context",
    bestFor: "Product, architecture, lifestyle with full scene",
    token: "f/5.6 balanced focus, sharp subject and environment",
  },
  "f/8": {
    label: "f/8 — Deep Landscape",
    effect: "Everything sharp foreground to background, landscape mode",
    bestFor: "Landscape, architectural, wide establishing shots",
    token: "f/8 landscape focus, everything sharp, deep depth of field",
  },
} as const;

// ─── Lighting knowledge ───────────────────────────────────────────────────────

export const LIGHTING_KNOWLEDGE = {
  "blue_hour_street": {
    label: "Blue Hour Street",
    description: "Post-sunset ambient, cool blue sky, warm street lamp contrast",
    mood: "Cinematic, melancholy, urban, moody",
    token: "blue hour ambient street light, cool blue sky, warm sodium vapor lamp contrast, wet reflections",
    bestFor: ["techwear", "urban cinematic", "fashion editorial", "character_28"],
  },
  "golden_hour": {
    label: "Golden Hour",
    description: "Warm orange-pink sunlight just before sunset",
    mood: "Warm, aspirational, romantic, lifestyle",
    token: "golden hour warm light, orange-pink rim light, soft directional sunlight",
    bestFor: ["lifestyle", "portrait", "fashion", "transformation hook"],
  },
  "ring_light_ugc": {
    label: "Ring Light UGC",
    description: "Classic creator ring light — catchlights in eyes, flat even face",
    mood: "UGC authentic, creator content, direct",
    token: "ring light at home, circular catchlights in eyes, even face illumination",
    bestFor: ["talking head", "UGC testimonial", "social proof"],
  },
  "window_natural": {
    label: "Window Natural",
    description: "Soft directional natural window light — beautiful and authentic",
    mood: "Authentic, warm, real, relatable",
    token: "natural window light, soft directional daylight, warm interior shadows",
    bestFor: ["UGC", "lifestyle", "emotional story", "everyday character"],
  },
  "neon_cyberpunk": {
    label: "Neon Cyberpunk",
    description: "Multi-colored neon light spill in urban environment",
    mood: "Dramatic, edgy, futuristic, editorial",
    token: "neon backlight, cyberpunk color spill, teal and magenta environmental light, atmospheric steam",
    bestFor: ["pattern interrupt", "techwear neon", "brand identity", "editorial"],
  },
  "rembrandt": {
    label: "Rembrandt Lighting",
    description: "Classic portrait lighting — 45° key light, triangle of light on cheek",
    mood: "Classic, artistic, authoritative, professional",
    token: "Rembrandt lighting, 45 degree key light, triangle highlight on cheek, deep shadow",
    bestFor: ["portrait", "expert character", "authority", "cinematic portrait"],
  },
  "chiaroscuro": {
    label: "Cinematic Chiaroscuro",
    description: "Extreme contrast between light and dark — cinematic drama",
    mood: "Dramatic, mysterious, cinematic, powerful",
    token: "cinematic chiaroscuro, extreme light-dark contrast, motivated single source light",
    bestFor: ["cinematic", "techwear closeup", "bold claim hook", "dramatic portrait"],
  },
} as const;
