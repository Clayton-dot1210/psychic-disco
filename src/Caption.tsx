import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

interface CaptionProps {
  text: string;
  /** Frame at which this caption starts appearing */
  startFrame: number;
  /** How many frames to display this caption */
  durationFrames: number;
}

/**
 * Animated caption that fades in from below, holds, then fades out upward.
 * Designed for 9:16 short-form content.
 */
export const Caption: React.FC<CaptionProps> = ({
  text,
  startFrame,
  durationFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeDuration = Math.round(fps * 0.25); // 0.25s fade
  const localFrame = frame - startFrame;

  if (localFrame < 0 || localFrame > durationFrames) return null;

  const opacity = interpolate(
    localFrame,
    [0, fadeDuration, durationFrames - fadeDuration, durationFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const translateY = interpolate(
    localFrame,
    [0, fadeDuration],
    [20, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 120,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          opacity,
          transform: `translateY(${translateY}px)`,
          background: "rgba(0,0,0,0.55)",
          backdropFilter: "blur(8px)",
          borderRadius: 16,
          padding: "18px 32px",
          maxWidth: "88%",
          textAlign: "center",
        }}
      >
        <span
          style={{
            color: "#ffffff",
            fontSize: 48,
            fontFamily: "'Inter', 'Helvetica Neue', sans-serif",
            fontWeight: 700,
            lineHeight: 1.3,
            letterSpacing: "-0.02em",
            textShadow: "0 2px 8px rgba(0,0,0,0.4)",
          }}
        >
          {text}
        </span>
      </div>
    </AbsoluteFill>
  );
};
