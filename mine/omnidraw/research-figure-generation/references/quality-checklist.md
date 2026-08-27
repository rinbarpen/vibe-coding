# Quality and Delivery Checklist

## Scientific review

- Purpose and figure type match the requested claim.
- Every module, arrow, panel, label, and scale is grounded in the source.
- No fabricated data, mechanism, equipment, numerical value, or significance mark.
- Text spelling, symbols, units, panel order, and arrow semantics are correct.

## Visual review

- One clear reading direction; no overlaps, clipped labels, or orphan arrows.
- Consistent font, stroke width, palette, legend, margins, and panel scale.
- Local edits preserve the mother image's composition and visual identity.

## File review

- Prefer `figure.svg` and `figure.pdf` for structure-heavy output.
- For raster delivery, use TIFF and a JSON spec with final physical dimensions.
- Run `scripts/validate_figure.py`; require `status: pass`.
- Record the exact command, target dimensions/PPI, actual pixels, embedded PPI,
  and the final artifact paths.
