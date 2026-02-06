# LaTeX Writing Guide for English Medical Papers

## 1. Document Class and Essential Packages

For most medical journals, the `article` class or journal-specific classes (like `naturemag`, `ieeeconf`) are used.

```latex
\documentclass[12pt, a4paper]{article}

% Essential Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry} % Margins
\usepackage{amsmath, amssymb} % Math
\usepackage{graphicx} % Figures
\usepackage{booktabs} % Professional tables (Three-line tables)
\usepackage{hyperref} % Hyperlinks
\usepackage[numbers, sort&compress]{natbib} % Vancouver-style citations
\usepackage{lineno} % Line numbers for review
\usepackage{setspace} % Double spacing

\geometry{margin=1in}
\doublespacing
\linenumbers
```

## 2. IMRaD Structure Template

```latex
\title{Your Full Research Title}
\author{Author A, Author B}
\date{}

\begin{document}
\maketitle

\begin{abstract}
Objective, Methods, Results, Conclusion.
\end{abstract}

\section{Introduction}
Background and purpose...

\section{Methods}
\subsection{Ethical Approval}
Approved by IRB No. XXX...
\subsection{Statistical Analysis}
Data were analyzed using SPSS...

\section{Results}
Major findings...

\section{Discussion}
Interpretation and limitations...

\bibliographystyle{vancouver}
\bibliography{references}

\end{document}
```

## 3. Professional Tables (Three-line Table)

Use the `booktabs` package for professional medical tables.

```latex
\begin{table}[htbp]
  \centering
  \caption{Baseline characteristics of the study population.}
  \begin{tabular}{lccc}
    \toprule
    Variable & Group A (n=50) & Group B (n=50) & P-value \\
    \midrule
    Age (years) & 65.4 $\pm$ 8.2 & 64.8 $\pm$ 7.9 & 0.708 \\
    Sex (M/F) & 28/22 & 26/24 & 0.685 \\
    \bottomrule
  \end{tabular}
\end{table}
```

## 4. Mathematical Notations

- P-values: Use `$P < .05$` or `$P = .023$`.
- Mean $\pm$ SD: `$65.4 \pm 8.2$`.
- Units: Use `\text{mg/dL}` or the `siunitx` package.
