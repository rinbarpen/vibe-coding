# CCF-A-Style Method Figures

CCF-A names a venue tier rather than one visual template. Match the target
paper's column width and visual language while applying these stable defaults.

## Visual defaults

- White background; flat fills; one neutral and 2–4 restrained accents.
- Arial/Helvetica or the paper's sans-serif family; 8–10 pt at final print size.
- 1–1.5 pt borders, 1.5–2 pt primary arrows, consistent arrowheads.
- Short noun phrases inside modules; mathematical details stay in equations or
  captions unless essential to the visual argument.
- Align modules to a grid; use equal gaps and a single primary reading direction.
- Use grouping boxes only for real architectural boundaries.

Avoid gradients, glow, drop shadows, pseudo-3D, stock illustration, decorative
icons, oversized rounded cards, random color changes, prose inside boxes, and
unexplained arrows. These cues make a method diagram look generated or slide-like.

## Content hierarchy

1. Inputs and representations.
2. Core method modules and the novel contribution.
3. Outputs, losses, or evaluation paths.
4. Optional training-only paths, shown with a distinct dashed convention.

Every line needs a defined semantic: data flow, supervision, parameter sharing,
or feedback. Put the meaning in the legend or edge label and use it consistently.

## Iteration protocol

- Store semantics in `figure-spec.json`; render SVG deterministically.
- Change one concern per revision and keep `figure-v1.svg`, `figure-v2.svg`, etc.
- Compare semantic text/edges before visual polish.
- Validate at single-column and double-column target widths.
- Export PDF from SVG for submission; rasterize TIFF only when the venue asks.
