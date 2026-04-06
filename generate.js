#!/usr/bin/env node
/**
 * fal.ai Image Generator
 * ======================
 * Generates images via fal.ai using prompts from the Python art prompting engine
 * or directly from command-line arguments.
 *
 * Usage
 * -----
 * # Generate 5 images using the prompt engine
 * node generate.js \
 *   --subject "a woman on a tennis court at sunset" \
 *   --shot portrait \
 *   --model fal-ai/nano-banana-2 \
 *   --count 5 \
 *   --output projects/my-reel/visuals
 *
 * # Use a raw prompt directly (skips the Python engine)
 * node generate.js \
 *   --prompt "editorial photo of a woman on a tennis court, golden hour" \
 *   --model fal-ai/flux/dev \
 *   --count 3 \
 *   --output projects/my-reel/visuals
 *
 * # Image-to-video (uses a source image)
 * node generate.js \
 *   --image projects/my-reel/visuals/shot_01.jpg \
 *   --model fal-ai/stable-video \
 *   --output projects/my-reel/clips
 *
 * Environment
 * -----------
 * Set FAL_KEY in your environment before running:
 *   export FAL_KEY=your_fal_api_key
 */

import { fal } from "@fal-ai/client";
import { execSync } from "child_process";
import { existsSync, mkdirSync, writeFileSync } from "fs";
import { join, basename, extname } from "path";

// ── CLI argument parser ────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    if (key.startsWith("--")) {
      args[key.slice(2)] = argv[i + 1] ?? true;
      i++;
    }
  }
  return args;
}

// ── Prompt resolution ──────────────────────────────────────────────────────

/**
 * Get the positive prompt text.
 * If --prompt is given, use it directly.
 * Otherwise call the Python prompt_engine.py and parse its JSON output.
 */
function resolvePrompt(args) {
  if (args.prompt) {
    return { positive: args.prompt, negative: "" };
  }

  if (!args.subject) {
    console.error("Error: provide --prompt or --subject");
    process.exit(1);
  }

  const shot = args.shot || "portrait";
  const platform = args.platform || "openart";
  const seed = args.seed ? `--seed ${args.seed}` : "";
  const extra = args.style ? `--style "${args.style}"` : "";
  const lighting = args.lighting ? `--lighting "${args.lighting}"` : "";

  const cmd = [
    "python3 prompt_engine.py",
    `"${args.subject}"`,
    `--shot ${shot}`,
    `--platform ${platform}`,
    "--json",
    seed,
    extra,
    lighting,
  ]
    .filter(Boolean)
    .join(" ");

  let output;
  try {
    output = execSync(cmd, { encoding: "utf8" });
  } catch (err) {
    console.error("Failed to run prompt_engine.py:", err.message);
    process.exit(1);
  }

  const parsed = JSON.parse(output);
  const platformData = parsed[platform] || parsed[Object.keys(parsed)[0]];
  return {
    positive: platformData.positive,
    negative: platformData.negative,
  };
}

// ── Model helpers ──────────────────────────────────────────────────────────

const MODEL_ALIASES = {
  "nano-banana-2": "fal-ai/nano-banana-2",
  "flux":          "fal-ai/flux/dev",
  "flux-schnell":  "fal-ai/flux/schnell",
  "flux-pro":      "fal-ai/flux-pro",
  "sd":            "fal-ai/stable-diffusion-v3-medium",
  "svd":           "fal-ai/stable-video",
};

function resolveModel(model) {
  return MODEL_ALIASES[model] || model || "fal-ai/flux/dev";
}

// ── Output helpers ─────────────────────────────────────────────────────────

function ensureDir(dir) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
    console.log(`Created output directory: ${dir}`);
  }
}

function padIndex(i, total) {
  const width = String(total).length;
  return String(i + 1).padStart(width, "0");
}

// ── Core generation ────────────────────────────────────────────────────────

async function generateImages({ prompt, negative, model, count, output, size }) {
  const [width, height] = (size || "1080x1920").split("x").map(Number);

  console.log(`\nModel   : ${model}`);
  console.log(`Count   : ${count}`);
  console.log(`Size    : ${width}x${height}`);
  console.log(`Output  : ${output}`);
  console.log(`\nPrompt  : ${prompt.slice(0, 120)}...`);
  console.log("\nGenerating in parallel...\n");

  const tasks = Array.from({ length: count }, (_, i) =>
    fal.subscribe(model, {
      input: {
        prompt,
        negative_prompt: negative || "",
        image_size: { width, height },
        num_images: 1,
        enable_safety_checker: false,
      },
      logs: false,
    }).then((result) => ({ index: i, result }))
  );

  const results = await Promise.all(tasks);

  const saved = [];
  for (const { index, result } of results) {
    const images = result.data?.images ?? result.images ?? [];
    if (!images.length) {
      console.warn(`Shot ${index + 1}: no image returned`);
      continue;
    }

    const imgUrl = images[0].url;
    const ext = extname(imgUrl.split("?")[0]) || ".jpg";
    const filename = `shot_${padIndex(index, count)}${ext}`;
    const filepath = join(output, filename);

    // Download the image
    const resp = await fetch(imgUrl);
    if (!resp.ok) throw new Error(`Failed to download ${imgUrl}: ${resp.status}`);
    const buffer = Buffer.from(await resp.arrayBuffer());
    writeFileSync(filepath, buffer);

    console.log(`  ✓ shot_${padIndex(index, count)}${ext}`);
    saved.push(filepath);
  }

  return saved;
}

async function generateVideo({ imagePath, model, output }) {
  console.log(`\nImage-to-video`);
  console.log(`Model  : ${model}`);
  console.log(`Source : ${imagePath}`);
  console.log(`Output : ${output}\n`);

  const result = await fal.subscribe(model, {
    input: {
      image_url: imagePath,
      motion_bucket_id: 127,
      cond_aug: 0.02,
    },
    logs: false,
  });

  const videos = result.data?.video ? [result.data.video] : result.video ? [result.video] : [];
  if (!videos.length) throw new Error("No video returned from model");

  const videoUrl = videos[0].url;
  const filename = basename(imagePath, extname(imagePath)) + ".mp4";
  const filepath = join(output, filename);

  const resp = await fetch(videoUrl);
  if (!resp.ok) throw new Error(`Failed to download video: ${resp.status}`);
  const buffer = Buffer.from(await resp.arrayBuffer());
  writeFileSync(filepath, buffer);

  console.log(`  ✓ ${filename}`);
  return filepath;
}

// ── Entry point ────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv);

  if (!process.env.FAL_KEY) {
    console.error(
      "Error: FAL_KEY environment variable is not set.\n" +
      "Get your key at https://fal.ai/dashboard/keys and run:\n" +
      "  export FAL_KEY=your_key_here"
    );
    process.exit(1);
  }

  const output = args.output || "projects/my-reel/visuals";
  ensureDir(output);

  const model = resolveModel(args.model);

  // Image-to-video mode
  if (args.image) {
    await generateVideo({ imagePath: args.image, model, output });
    return;
  }

  // Text-to-image mode
  const { positive, negative } = resolvePrompt(args);
  const count = parseInt(args.count || "1", 10);

  const saved = await generateImages({
    prompt: positive,
    negative,
    model,
    count,
    output,
    size: args.size,
  });

  console.log(`\nDone. ${saved.length} image(s) saved to ${output}/`);

  // Write a manifest for Remotion to pick up
  const manifest = {
    subject: args.subject || args.prompt,
    shot: args.shot || "portrait",
    model,
    generated_at: new Date().toISOString(),
    images: saved,
  };
  writeFileSync(join(output, "manifest.json"), JSON.stringify(manifest, null, 2));
  console.log(`Manifest written to ${output}/manifest.json`);
}

main().catch((err) => {
  console.error("Generation failed:", err.message);
  process.exit(1);
});
