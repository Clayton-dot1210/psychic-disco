import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { z } from "zod";
import { Caption } from "./Caption";

// ── Schema (drives Remotion Studio's props panel) ──────────────────────────

export const ReelCompositionSchema = z.object({
  /** Path to the project folder containing visuals/ and optionally voiceover.mp3 */
  projectDir: z.string().default("projects/my-reel"),
  /** Explicit audio path — if empty, looks for <projectDir>/voiceover.mp3 */
  audioSrc: z.string().default(""),
  /** Frames per second (must match Root.tsx Composition setting) */
  fps: z.number().default(30),
  /** Total reel duration in seconds */
  durationInSeconds: z.number().default(30),
  /**
   * Caption lines in order.
   * Each string maps 1-to-1 with a shot.
   * Leave empty to skip captions.
   */
  captionLines: z.array(z.string()).default([]),
  /**
   * Shot manifest path (JSON produced by generate.js).
   * If omitted, the composition renders a placeholder.
   */
  manifestPath: z.string().optional(),
  /**
   * Explicit list of image paths. Takes precedence over manifestPath.
   * Useful when you want to specify order manually.
   */
  imagePaths: z.array(z.string()).optional(),
});

export type ReelCompositionProps = z.infer<typeof ReelCompositionSchema>;

// ── Ken Burns zoom helper ──────────────────────────────────────────────────

interface ShotProps {
  src: string;
  startFrame: number;
  durationFrames: number;
  /** Even-indexed shots zoom in, odd zoom out for variety */
  shotIndex: number;
}

const Shot: React.FC<ShotProps> = ({ src, durationFrames, shotIndex }) => {
  const frame = useCurrentFrame();

  const zoomIn = shotIndex % 2 === 0;
  const scale = interpolate(
    frame,
    [0, durationFrames],
    zoomIn ? [1, 1.08] : [1.08, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Subtle pan: even shots drift right, odd drift left
  const panX = interpolate(
    frame,
    [0, durationFrames],
    shotIndex % 2 === 0 ? [0, 12] : [12, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale}) translateX(${panX}px)`,
          transformOrigin: "center center",
        }}
      />
    </AbsoluteFill>
  );
};

// ── Cross-fade transition overlay ──────────────────────────────────────────

interface FadeOverlayProps {
  /** Duration of the cross-fade in frames */
  fadeDuration: number;
  /** Total frames for this sequence */
  sequenceDuration: number;
}

const FadeOverlay: React.FC<FadeOverlayProps> = ({
  fadeDuration,
  sequenceDuration,
}) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(
    frame,
    [
      0,
      fadeDuration,
      sequenceDuration - fadeDuration,
      sequenceDuration,
    ],
    [1, 0, 0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{ background: "#000000", opacity, pointerEvents: "none" }}
    />
  );
};

// ── Main composition ───────────────────────────────────────────────────────

export const ReelComposition: React.FC<ReelCompositionProps> = ({
  projectDir,
  audioSrc,
  fps,
  durationInSeconds,
  captionLines,
  imagePaths,
}) => {
  const { width, height } = useVideoConfig();
  const totalFrames = durationInSeconds * fps;

  // Resolve images — use explicit list or fall back to placeholders
  const images: string[] = imagePaths && imagePaths.length > 0
    ? imagePaths
    : [];

  const shotCount = images.length || 1;
  const framesPerShot = Math.floor(totalFrames / shotCount);
  const fadeDuration = Math.round(fps * 0.4); // 0.4 s cross-fade

  const resolvedAudio =
    audioSrc || (projectDir ? `${projectDir}/voiceover.mp3` : "");

  return (
    <AbsoluteFill style={{ background: "#000000" }}>
      {/* ── Audio layer ─────────────────────────────────────────────────── */}
      {resolvedAudio && (
        <Audio src={resolvedAudio} volume={1} />
      )}

      {/* ── Shot sequences ──────────────────────────────────────────────── */}
      {images.length > 0 ? (
        images.map((src, i) => {
          const startFrame = i * framesPerShot;
          const captionText = captionLines[i] ?? "";

          return (
            <Sequence
              key={src}
              from={startFrame}
              durationInFrames={framesPerShot}
            >
              <Shot
                src={src}
                startFrame={startFrame}
                durationFrames={framesPerShot}
                shotIndex={i}
              />
              <FadeOverlay
                fadeDuration={fadeDuration}
                sequenceDuration={framesPerShot}
              />
              {captionText && (
                <Caption
                  text={captionText}
                  startFrame={fadeDuration}
                  durationFrames={framesPerShot - fadeDuration * 2}
                />
              )}
            </Sequence>
          );
        })
      ) : (
        /* Placeholder when no images are loaded yet */
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
            flexDirection: "column",
            gap: 24,
          }}
        >
          <div
            style={{
              color: "#ffffff",
              fontSize: 52,
              fontFamily: "monospace",
              opacity: 0.7,
              textAlign: "center",
              padding: "0 60px",
            }}
          >
            No images loaded.
          </div>
          <div
            style={{
              color: "#aaaaaa",
              fontSize: 30,
              fontFamily: "monospace",
              textAlign: "center",
              padding: "0 60px",
            }}
          >
            Run <code style={{ color: "#7fffff" }}>node generate.js</code> to
            generate visuals, then pass{" "}
            <code style={{ color: "#7fffff" }}>--props</code> with imagePaths.
          </div>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
