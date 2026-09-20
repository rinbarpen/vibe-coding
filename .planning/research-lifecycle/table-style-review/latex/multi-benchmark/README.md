# Multi-dataset / multi-baseline / multi-metric tables

9 methods (8 placeholder baselines + Candidate), 4 datasets, 3 metrics = 108 values. All invented layout fixtures; default one run, no uncertainty claims. F1 in the wide header means Macro-F1.

- wide.tex + wide-body.tex: table* with two-level dataset/metric headers.
- metric-1.tex through metric-3.tex: one metric per table, four dataset columns.
- dataset-blocks.tex: one-column supplement longtable with repeat headers.
- packages.tex: dependencies and ranking macros; inherit actual venue fonts/captions.
- data.json: shared input values. Bold = best displayed value, underline = second distinct value; ties share rank. Lower ECE wins. These marks do not assert significance.
- *-preview.pdf/png: actual LaTeX output, not image-simulated tables.
- integration.pdf: generic two-column harness. Actual ACM/IEEE/venue classes are not tested.

Use from this directory, or adjust input paths after copying into the manuscript:
Preamble: \input{packages}
Body: \input{wide}

Rebuild with python3 build.py (NumPy, pdflatex, pdftoppm required).
Six documents compiled twice; no Overfull warnings. Wide-table width checked against textwidth without resizebox. Longtable has two pages. The three layouts reuse the same values.
