# Medical Paper Format Conversion Guide

This guide explains how to convert your LaTeX (English) or HTML (Chinese) manuscripts into PDF and DOCX formats using Pandoc and other tools.

## 1. Prerequisites

You need to have **Pandoc** installed on your system.
- Ubuntu/Debian: `sudo apt-get install pandoc`
- MacOS: `brew install pandoc`
- Windows: `choco install pandoc`

For LaTeX to PDF conversion, a TeX distribution (like TeX Live or MiKTeX) is required.

## 2. LaTeX Conversion (English Papers)

### LaTeX to PDF
Use `pdflatex` or `xelatex`:
```bash
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

### LaTeX to DOCX
Use Pandoc:
```bash
pandoc manuscript.tex -o manuscript.docx --citeproc --bibliography=references.bib
```

## 3. HTML Conversion (Chinese Papers)

### HTML to DOCX (Recommended)
Pandoc handles HTML to DOCX conversion very well, preserving table structures and headers.
```bash
pandoc manuscript.html -o manuscript.docx
```

### HTML to PDF
You can use Pandoc with a PDF engine (like `wkhtmltopdf` or `weasyprint`), or simply use your browser's "Print to PDF" feature.
```bash
# Using Pandoc with WeasyPrint
pandoc manuscript.html -o manuscript.pdf --pdf-engine=weasyprint
```

## 4. Advanced Pandoc Options

- **Reference Document**: Use a reference DOCX file to maintain specific styles (fonts, spacing).
    ```bash
    pandoc manuscript.html --reference-doc=template.docx -o manuscript.docx
    ```
- **Math Support**: For HTML to DOCX, Pandoc automatically converts MathJax/LaTeX formulas into Word equations.

## 5. Troubleshooting

- **Encoding**: Ensure your files are saved in **UTF-8** encoding to avoid character corruption in Chinese papers.
- **Images**: Ensure image paths in your LaTeX/HTML files are relative and correct.
- **Tables**: Complex nested tables in HTML might need manual adjustment in Word after conversion.
