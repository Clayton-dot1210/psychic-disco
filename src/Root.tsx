import React from "react";
import { Composition } from "remotion";
import { ReelComposition, ReelCompositionSchema } from "./ReelComposition";

// Default props used in Remotion Studio preview.
// Override via --props when rendering from the CLI.
const DEFAULT_PROPS = {
  projectDir: "projects/my-reel",
  audioSrc: "",         // e.g. "projects/my-reel/voiceover.mp3"
  fps: 30,
  durationInSeconds: 30,
  captionLines: [] as string[],
};

export const Root: React.FC = () => {
  return (
    <Composition
      id="ReelComposition"
      component={ReelComposition}
      durationInFrames={DEFAULT_PROPS.durationInSeconds * DEFAULT_PROPS.fps}
      fps={DEFAULT_PROPS.fps}
      width={1080}
      height={1920}
      defaultProps={DEFAULT_PROPS}
      schema={ReelCompositionSchema}
    />
  );
};
