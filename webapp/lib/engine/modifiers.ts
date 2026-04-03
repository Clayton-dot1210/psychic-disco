import type { ShotType } from "./types";

interface ShotPreset {
  camera: string;
  lens: string;
  aperture: string;
  lighting: string;
  dof: string;
  quality: string[];
  post: string[];
  description?: string;
  motionCue?: string;
  duration?: string;
  aspect?: string;
}

export const SHOT_PRESETS: Record<ShotType, ShotPreset> = {
  // ── Standard photography ───────────────────────────────────────────────────
  portrait: {
    camera: "shot on Sony A7R V",
    lens: "85mm f/1.4 prime lens",
    aperture: "f/1.8 shallow depth of field",
    lighting: "Rembrandt lighting",
    dof: "creamy bokeh background",
    quality: ["ultra-detailed", "pore-level detail", "professional photography"],
    post: ["RAW photo", "professionally retouched", "skin texture preserved"],
    motionCue: "slow push-in",
    aspect: "9:16",
  },
  landscape: {
    camera: "shot on Hasselblad X2D 100C",
    lens: "24-70mm f/2.8 zoom",
    aperture: "f/8 landscape focus",
    lighting: "golden hour lighting",
    dof: "deep focus",
    quality: ["ultra-detailed", "8K UHD", "award-winning photography"],
    post: ["RAW photo", "HDR details", "color graded"],
    motionCue: "slow pan right",
    aspect: "16:9",
  },
  street: {
    camera: "shot on Leica M11",
    lens: "35mm f/1.4 prime lens",
    aperture: "f/2.8",
    lighting: "overcast soft diffused light",
    dof: "subject separation",
    quality: ["photojournalistic", "ultra-detailed", "professional photography"],
    post: ["RAW photo", "Kodak Portra 400 film"],
    motionCue: "handheld tracking shot",
    aspect: "9:16",
  },
  product: {
    camera: "shot on Canon EOS R5",
    lens: "100mm f/2.8 macro",
    aperture: "f/5.6 deep focus",
    lighting: "three-point studio lighting",
    dof: "tack sharp focus",
    quality: ["ultra-detailed", "magazine cover quality", "8K UHD"],
    post: ["RAW photo", "color graded", "professionally retouched"],
    motionCue: "gentle orbit",
    aspect: "1:1",
  },
  architecture: {
    camera: "shot on Phase One IQ4 150MP",
    lens: "24-70mm f/2.8 zoom",
    aperture: "f/8 landscape focus",
    lighting: "blue hour lighting",
    dof: "sharp subject with soft background",
    quality: ["ultra-detailed", "100 megapixel resolution", "award-winning photography"],
    post: ["RAW photo", "HDR details", "dodge and burn"],
    motionCue: "slow crane up",
    aspect: "16:9",
  },
  wildlife: {
    camera: "shot on Nikon Z9",
    lens: "200mm f/2.0 telephoto",
    aperture: "f/2.8",
    lighting: "golden hour lighting",
    dof: "shallow depth of field",
    quality: ["ultra-detailed", "National Geographic quality", "professional photography"],
    post: ["RAW photo", "color graded"],
    motionCue: "tracking follow shot",
    aspect: "16:9",
  },
  cinematic: {
    camera: "shot on Canon EOS R5",
    lens: "50mm f/1.2 prime lens",
    aperture: "f/1.8 shallow depth of field",
    lighting: "cinematic chiaroscuro",
    dof: "razor thin focus plane",
    quality: ["ultra-detailed", "photorealistic", "8K UHD"],
    post: ["Kodak Vision3 500T cinema film", "color graded", "anamorphic lens flare"],
    motionCue: "dolly zoom",
    aspect: "21:9",
  },

  // ── UGC shots ──────────────────────────────────────────────────────────────
  talking_head: {
    camera: "shot on iPhone 15 Pro",
    lens: "wide angle front camera",
    aperture: "f/1.8 shallow depth of field",
    lighting: "ring light at home",
    dof: "slight background blur",
    quality: ["natural skin texture", "pore-level detail", "authentic candid feel"],
    post: ["natural color grade", "real person look", "organic unposed"],
    description: "Direct to camera talking head, UGC creator style",
    motionCue: "slow subtle push-in, handheld micro-drift",
    duration: "3-5s",
    aspect: "9:16",
  },
  pov: {
    camera: "shot on iPhone 15 Pro",
    lens: "wide angle 24mm lens",
    aperture: "f/2.8",
    lighting: "natural ambient room light",
    dof: "deep POV focus",
    quality: ["immersive first-person perspective", "authentic candid feel"],
    post: ["handheld natural motion", "raw and real"],
    motionCue: "immersive handheld drift",
    aspect: "9:16",
  },
  reaction: {
    camera: "shot on Sony ZV-E10",
    lens: "slightly wide 35mm",
    aperture: "f/2.0",
    lighting: "window natural light selfie",
    dof: "sharp face with soft room background",
    quality: ["genuine human emotion", "authentic expression", "relatable everyday aesthetic"],
    post: ["lived-in authenticity", "organic unposed"],
    motionCue: "handheld responsive reframe",
    aspect: "9:16",
  },
  lifestyle: {
    camera: "shot on Fujifilm X-T5",
    lens: "standard 28mm lens",
    aperture: "f/2.8",
    lighting: "outdoor daylight selfie",
    dof: "environmental context with sharp subject",
    quality: ["lifestyle documentary feel", "genuine human moment", "relatable"],
    post: ["natural color grade", "warm tones", "real world textures"],
    motionCue: "gentle tracking follow",
    aspect: "9:16",
  },
  unboxing: {
    camera: "shot on iPhone 15 Pro",
    lens: "wide angle front camera",
    aperture: "f/2.0",
    lighting: "practical desk lamp light",
    dof: "product in foreground, creator in background",
    quality: ["product detail visible", "authentic unboxing energy", "real person reaction"],
    post: ["natural lighting color grade", "genuine excitement"],
    motionCue: "slow reveal push-in",
    aspect: "9:16",
  },
  transformation: {
    camera: "shot on Canon EOS M50 Mark II",
    lens: "35mm f/1.4 prime lens",
    aperture: "f/1.8 shallow depth of field",
    lighting: "soft overhead light",
    dof: "sharp subject pop",
    quality: ["before after visual clarity", "aspirational result", "compelling transformation"],
    post: ["clean color grade", "professional finish", "high contrast reveal"],
    motionCue: "dramatic crane up reveal",
    aspect: "9:16",
  },

  // ── Character 28 / Techwear ────────────────────────────────────────────────
  techwear_street: {
    camera: "shot on Sony A7R V",
    lens: "35mm f/1.4 prime lens",
    aperture: "f/1.8 shallow depth of field",
    lighting: "blue hour ambient street light, wet cobblestone reflections",
    dof: "sharp subject, creamy bokeh shop lights behind",
    quality: [
      "pore-level skin detail",
      "rain moisture on jacket surface",
      "wet cobblestone texture",
      "photojournalistic realism",
    ],
    post: [
      "cinematic blue-teal grade",
      "Kodak Vision3 500T cinema film",
      "motivated street lamp warm glow",
      "wet reflections color depth",
    ],
    description: "Character 28 signature: wet street blue hour techwear",
    motionCue: "slow deliberate push-in, slight handheld steadiness",
    duration: "4-6s",
    aspect: "9:16",
  },
  techwear_closeup: {
    camera: "shot on Sony A7R V",
    lens: "85mm f/1.4 prime lens",
    aperture: "f/1.4 wide open",
    lighting: "cinematic dusk low-key street lighting",
    dof: "razor thin focus on eyes, creamy street bokeh background",
    quality: [
      "pore-level face detail",
      "intense eye focus",
      "rain on skin texture",
      "micro contrast skin rendering",
    ],
    post: [
      "desaturated cool teal grade",
      "cinematic chiaroscuro",
      "subtle anamorphic lens quality",
      "ultra-realistic skin",
    ],
    description: "Character 28 signature: extreme close-up intense face",
    motionCue: "ultra-slow push-in, almost imperceptible drift",
    duration: "3-5s",
    aspect: "9:16",
  },
  techwear_wide: {
    camera: "shot on Sony A7R V",
    lens: "24-70mm f/2.8 zoom",
    aperture: "f/2.8",
    lighting: "overcast blue-grey sky, ambient street lamp warm glow",
    dof: "full environmental portrait, sharp subject in environment",
    quality: [
      "full body environmental portrait",
      "wet street texture detail",
      "architectural depth",
      "urban scale context",
    ],
    post: [
      "desaturated moody grade",
      "cool blue tones",
      "wet pavement reflections",
      "cinematic atmosphere",
    ],
    description: "Character 28 signature: full body centered wet street",
    motionCue: "slow crane up, full reveal from ground to face",
    duration: "5-7s",
    aspect: "9:16",
  },
  techwear_neon: {
    camera: "shot on Canon EOS R5",
    lens: "50mm f/1.2 prime lens",
    aperture: "f/1.2 wide open",
    lighting: "neon sign backlight, cyberpunk color spill, steam atmosphere",
    dof: "sharp face, neon bokeh background chaos",
    quality: [
      "neon light skin glow",
      "atmospheric steam particles",
      "urban decay texture",
      "cyberpunk realism",
    ],
    post: [
      "teal and orange split grade",
      "neon color bleed",
      "Cinestill 800T pushed grain",
      "cinematic anamorphic quality",
    ],
    description: "Character 28 variant: neon cyberpunk alley atmosphere",
    motionCue: "slow atmospheric push-in, steam drift",
    duration: "5-7s",
    aspect: "9:16",
  },
};

// ─── Negative prompts ─────────────────────────────────────────────────────────

export const NEGATIVE_REALISM =
  "painting, illustration, drawing, cartoon, anime, sketch, render, CGI, " +
  "3D render, digital art, concept art, low quality, blurry, out of focus, " +
  "grainy, noisy, overexposed, underexposed, bad anatomy, distorted, " +
  "watermark, text, logo, signature, extra limbs, disfigured, ugly, " +
  "amateur, plastic skin, airbrushed, unrealistic colors, flat lighting, " +
  "oversaturated, HDR overdone";

export const NEGATIVE_UGC =
  "overly retouched, airbrushed skin, plastic smooth skin, commercial photography look, " +
  "studio flat lighting, stock photo feel, posed model, advertisement aesthetic, " +
  "high-fashion editorial, over color-graded, low quality, blurry motion, noisy grain, " +
  "bad anatomy, watermark, text overlay, distorted face";

export const NEGATIVE_TECHWEAR =
  "bright cheerful colors, warm sunny look, airbrushed perfect skin, " +
  "commercial advertisement feel, stock photo pose, flat studio lighting, " +
  "low quality, blurry, distorted anatomy, watermark, text, multiple faces, " +
  "cartoon, illustration, anime, CGI render, overly saturated, HDR overdone";
