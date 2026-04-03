import { NextRequest, NextResponse } from "next/server";
import { build, buildFromOutcome, formatForPlatforms } from "@/lib/engine";
import type { PromptConfig, Platform } from "@/lib/engine/types";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const {
      subject,
      shotType = "portrait",
      characterKey,
      hookKey,
      cameraAngle,
      lensOverride,
      lightingOverride,
      atmosphereOverride,
      motionOverride,
      outcomeScenario,
      extraStyle,
      referenceImageUrl,
      platforms = ["kling_3", "kling_3_omni", "seedance_2", "higgsfield"],
      durationSeconds = 5,
      pikaMotionStrength = 1,
    } = body as PromptConfig & {
      platforms?: Platform[];
      durationSeconds?: 5 | 10;
      pikaMotionStrength?: 1 | 2 | 3 | 4;
    };

    if (!subject || typeof subject !== "string") {
      return NextResponse.json({ error: "subject is required" }, { status: 400 });
    }

    // Build the core prompt — use outcome-aware builder if scenario provided
    const builtPrompt = outcomeScenario
      ? buildFromOutcome(subject, outcomeScenario, characterKey, {
          hookKey,
          cameraAngle,
          lensOverride,
          lightingOverride,
          atmosphereOverride,
          extraStyle,
          referenceImageUrl,
        })
      : build({
          subject,
          shotType,
          characterKey,
          hookKey,
          cameraAngle,
          lensOverride,
          lightingOverride,
          atmosphereOverride,
          extraStyle,
          referenceImageUrl,
          outcomeScenario,
        });

    // Format for all requested platforms
    const outputs = formatForPlatforms(builtPrompt, platforms, {
      motionOverride,
      durationSeconds,
      referenceImageUrl,
      pikaMotionStrength,
    });

    return NextResponse.json({ outputs, prompt: builtPrompt });
  } catch (err) {
    console.error("[generate]", err);
    return NextResponse.json({ error: "Generation failed" }, { status: 500 });
  }
}
