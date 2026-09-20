# Progress
Saved actual pre-turn manifest baseline in /tmp/research-lifecycle-delivery/baseline/auto-research (includes previous Writing Plan).
Implemented stage runtime with explicit verified model bindings, serial Git checkpoint journal, parent/child completion rules and archive validation.
Implemented matrix expansion, design coverage checks, budget gates, traceable JSON/CSV statistics and audit qualification.
Updated lifecycle/agent/installer contracts and nine templates, preserving existing project/runtime files on reinstall.
Regression currently 48 passed including all prior Writing Plan and vibe tests; all Git writes exercised only in temporary repositories.
Verification packaging: mixed-root pytest collection inspected a disconnected /tmp/fuse mount. Run baseline tests with cwd=baseline instead; no source changes needed. Failure output retained in verification-environment-failure.json.

Final verification: pre-turn baseline 22 Writing Plan tests passed; modified workspace 48 combined tests passed; reopened package 46 manifest tests passed. Public vibe init/discovery and installed Writing Plan validation passed.
Refined all 11 major research phases with machine-readable `phase_details` and a human stage index covering goals, inputs, activities, outputs, gates, roles, checkpoints, exits, and return paths. Generated 22-file delta against actual pre-turn baseline (not HEAD). Applied patch on a copy, then executed rollback.py; all original bytes matched and previous Writing Plan remained.
Delivery: /tmp/research-lifecycle-delivery/{modified.tar.gz,lifecycle.patch,verification-record.json,rollback.py,original.tar.gz,changes.json,SHA256SUMS}.
No real model/cloud/experiment/submission calls; only explicit host-verifiable bindings, current skill orchestration contracts and local fixtures.

Added declarative figure generation and venue requirement support: `writing/figure-types.yaml`, `writing/venue-profiles.yaml`, `references/venue-requirements.md`, schema validation, resolver materialization, node-level figure artifact/provenance checks, and venue-aware rendering. Official source URLs are recorded in the profile snapshots and must be refreshed before submission. Regression now passes 50 tests; installed scaffold validation and resolved venue/figure smoke test passed. Refreshed delivery delta: 31 files; reopened package regression 48 passed; rollback and checksums passed.

Figure design extension: 17 per-type implementation contracts; 4 palettes with categorical/sequential/diverging variants; inherited figure_style and per-figure visual resolution; explicit plot backend accepted for data charts. Baseline 48 tests, modified 51 tests. Patch applied and 8-file rollback verified on isolated copy. Delivery: /tmp/figure-design-delivery. External renderers still execute final figures; visual quality requires final-size inspection.

Integrity review follow-up: empty/malformed figures, missing inputs and extension mismatches now fail; PDF/EPS envelope-only checks explicitly warn. Added figure_smoke.py synthetic gallery: 17 types x 4 palettes, 204 SVG/PDF/PNG files structurally verified. Visually inspected four contact sheets and enlarged earth heatmap/monochrome distribution; corrected categorical gradient misuse, missing colorbars/return arrows, grayscale median color, adaptive cell-label contrast. Full regression 73 passed; baseline 51 manifest tests vs modified 71; patch/rollback 5 files verified in copies. Attention overlay contrast and actual geographic/AI/real-data backend validation remain pending, recorded in /tmp/figure-integrity-delivery/GALLERY_REVIEW.md.

## 2026-09-20 — GPT visual / editable figure dual delivery
- Five schematic types routed to gpt-image visual drafts and GPT-authored SVG -> native PPTX; no silent legacy renderer fallback.
- Generated five-slide editable demo at /tmp/figure-style-v2/research-figures-editable.pptx; source SVG and export reports retained beside it.
- Local data-gallery renderer now handles twelve data-figure types; external five routes explicitly pending host backend binding.
- Updated typography to Liberation Sans, smaller headings and size hierarchy; visually reviewed all five vector pages and data contact sheet.
- Working-copy regression: 73 tests passed. Native PPTX structural inspection found zero picture objects, native shapes/text on all five slides. PowerPoint GUI interoperability not tested.
- Baseline, diff, verification and rollback artifacts: /tmp/figure-style-v2/. Model API client is not implemented; host must bind the generation tools.

## Table style review catalog
- 12 PDF/PNG/SVG pages; 12 native Word tables reopened and matched to fixture JSON.
- Synthetic fixture values only, not experimental results; multi-seed SD cross-checked with statistics.stdev.
- Reviewed all 12 preview pages; corrected text-column alignment. Source and checks archived under table-style-review/.
- Delivery: /tmp/research-table-gallery/table-style-catalog.zip. Word GUI pagination not verified; no manifest/CLI or accepted figure changes.

## LaTeX correction
Primary output switched from Word to native LaTeX. Four generic compile harnesses passed twice with no Overfull warnings; real two-page longtable verified. Actual ACM/IEEE class testing remains pending (classes absent). Source and literal compile logs archived in table-style-review/latex/.

- All-table LaTeX delivery: 20 independent source tables, standalone wrappers, PDFs and PNGs. Forty individual pdflatex passes succeeded; zero Overfull warnings. Expanded generic single/two-column and longtable harnesses also passed. No actual venue class certification. Archive: /tmp/research-tables-latex/research-tables-latex-all.zip.

- Added multi-benchmark LaTeX: 4 datasets × 9 methods × 3 metrics (108 fixture values), wide/split-metric/dataset-block layouts. Six documents compiled twice, zero Overfull warnings; ties and lower-is-better ECE verified; longtable is two pages.
