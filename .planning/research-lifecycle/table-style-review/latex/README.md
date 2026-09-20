# Native LaTeX research tables

Primary artifacts are LaTeX source and compiled PDFs. No Word dependency.

## Use in a manuscript
Copy `tables/`, `bodies/`, and `table-packages.tex` into the manuscript project. Review the package list against the venue's allowed packages. If the class already loads a package, avoid conflicting options.

```tex
% Preamble, after the venue's official document class:
\input{table-packages}
% Manuscript body:
\input{tables/02-component-ablation}
```

`table` is used for narrow interaction/delta examples; wider examples use `table*`. The author may change this boundary after checking the actual column width. Caption fonts, numbering, and float placement are inherited from the host class. No global geometry, caption patch, fixed figure font size, or resizebox is imposed by the table snippets. `geometry` belongs only to the local compile harnesses. `longtable` is for a one-column supplement, not a two-column floating table.

## Verification
`catalog.tex`, `two-column.tex`, `supplement.tex`, `width-check.tex` each compiled twice with pdflatex, exit 0, no Overfull warnings. Width check uses 85 mm for compact examples and the test text width for wide examples. The appendix actually spans two pages with continued headings and 32 stable configuration IDs. See verification.json for literal commands and stdout.

The local environment lacks acmart.cls and IEEEtran.cls. Actual ACM/IEEE/individual venue template validation remains pending. CCF ranking is not a layout template. These are reusable table structures, not a universal top-journal compliance certificate.

## Styles and data
Grouped benchmarks, component removal, sequential addition, design-choice blocks, factor interactions, efficiency, robustness, multi-seed summary, compact delta and appendix longtable are provided. The old review-only heat variant is monochrome in this publication-oriented package. All data are inherited invented layout fixtures, not experiment outputs. Only the explicitly multi-seed example uses five seeds. Bold labels denote references, not significance. Positive deltas retain their plus signs. Numeric columns use siunitx S alignment. Missing entries use a dash and a status/footnote.

Official references:
- https://portalparts.acm.org/hippo/latex_templates/acmart.pdf
- https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/authoring-tools-and-templates/

## Rebuild
Run `python3 generate.py` using the bundled fixtures.json. For direct compilation no Python or fixture file is needed:
`pdflatex -interaction=nonstopmode -halt-on-error catalog.tex` (run twice).

## All-table edition
20 distinct table files now each have a standalone compilation wrapper, an independent PDF, a PNG preview and extracted PDF text. See INDEX.md. Run `python3 compile-individual.py` to rebuild these. All 20 compiled twice with no Overfull warnings; individual-verification.json retains commands, stdout and statuses. The supplement PDF spans two pages. Wrapper previews are not replacement venue templates.
