---
name: research-figure-generation
description: Use when creating publication-oriented scientific illustrations, mechanisms, workflows, graphical abstracts, multi-panel comparisons, or cover art from research content and a target journal or print size.
---

# Research Figure Generation

Turn research content into a scientifically bounded figure prompt, a generated
candidate, and a submission-ready package. This skill complements `matplotlib`
for measured data and `scientific-schematics` for deterministic schematics.

## Figure types

| Type | Primary question |
|---|---|
| Technical route / workflow | How does the study proceed? |
| Experimental setup | What documented apparatus and links are used? |
| Mechanism | What causal path explains the phenomenon? |
| Multi-panel comparison | How do groups or conditions differ? |
| Graphical abstract | What is the central contribution? |
| Presentation overview | How does the complete project fit together? |
| Journal cover | How can the research insight become a strong visual metaphor? |

## Workflow

1. **Classify the figure**: technical route, experimental setup, mechanism,
   multi-panel comparison, graphical abstract, presentation overview, or cover.
2. **Extract the blueprint**: purpose, modules, reading direction, arrow
   semantics, allowed labels, real data versus qualitative illustration, and
   forbidden invented entities/results. Never add a step or number absent from
   the source.
3. **Choose a backend**: use `auto-figure` for structured generation and
   `auto-figure-edit` for targeted edits when those tools are available. When
   unavailable, use the available image-generation/editing tool. Preserve a
   mother image while editing so layout and palette remain stable.
4. **Render in stages**: split long or dense figures into submodules, generate
   a candidate, inspect text/arrows/scientific relationships, then issue local
   edits instead of regenerating a correct composition.
5. **Rebuild for delivery**: use SVG/PDF or manually re-typeset labels for
   structure-heavy figures. Export a TIFF for raster-only venues.
6. **Verify**: create a spec such as `{"width_in": 7, "height_in": 4,
   "min_ppi": 600}` and run:

   ```bash
   python scripts/validate_figure.py --spec figure-spec.json --image figure.tiff
   ```

   A passing file must meet both pixel dimensions and embedded PPI. Changing
   only metadata does not add detail; use `ceil(width_in × PPI)` pixels.

## Prompt contract

Return these sections: **Image goal**, **recommended composition**, **regions**,
**connections and arrow meanings**, **visible text**, **scientific boundaries**,
**render prompt**, **local edit commands**, and **delivery/verification record**.
Use short labels and list every permitted visible string. For real results,
consume supplied data; without data, prohibit numbers, axes, significance marks,
and invented curves.

## Style and compliance

Use a restrained academic palette, consistent typography, clear contrast, and
one reading direction. Check spelling, labels, arrow direction, panel numbering,
scale consistency, clipping, and journal disclosure requirements. AI output is
a candidate for scientific review, vector reconstruction, or re-typesetting—not
an unattended claim of experimental fact.

## References

- [Prompt templates and figure-type rules](references/prompt-templates.md)
- [Quality and delivery checklist](references/quality-checklist.md)
- [Happy Figure quick reference](https://github.com/datawhalechina/happy-figure/blob/main/docs/appendix/quick-reference.md)
