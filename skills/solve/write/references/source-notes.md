# Source notes

## Primary source

- Title: `ASD-STE100 Simplified Technical English`
- Issue: 9
- Publication date: `January 2025`
- Publisher: `Aerospace, Security and Defence Industries Association of Europe`
- Official site: <https://asd-ste100.org/>
- Source length: 434 PDF pages
- Part 1: 9 sections and 53 writing rules
- Part 2: 875 approved words and 1,274 non-approved entries with alternatives

Optional source files on the authoring Mac:

- PDF: `/Users/namanbajpai/Downloads/ASD-STE100_ISSUE9.pdf`
- Markdown OCR: `/Users/namanbajpai/ocr/output/ASD-STE100_ISSUE9/ASD-STE100_ISSUE9.md`
- Raw OCR JSON: `/Users/namanbajpai/ocr/output/ASD-STE100_ISSUE9/ASD-STE100_ISSUE9.json`
- Figure annotations:
  `/Users/namanbajpai/ocr/output/ASD-STE100_ISSUE9/image_annotations.json`

The skill does not require these files. A Linux installation uses the condensed
rules and references in the skill package.

The paths below are from the upstream `ste-writing` repository. simplify-writing
does not include the full-book dictionary build. In upstream, the full book is
available locally, relative to that repository:

- Markdown: `vale/private/ASD-STE100_ISSUE9.md`
- Original archive: `vale/private/ASD-STE100_ISSUE9.zip`
- Extracted dictionary and restrictions: `vale/private/dictionary.json`

These files are Git-ignored. The Markdown matches the archive member byte for
byte. [The Vale package](../vale/README.md) documents the extraction audit and
its unresolved count discrepancy. [The coverage map](../vale/coverage.md)
records all 53 rules, their source locations, and remaining contextual review.

The OCR result contains 434 unique page indexes, no empty OCR pages, 7 extracted
figures, and 4,508 Markdown table rows.

## Efficient verification

Use this section only when the optional Markdown source is present. Do not load
the full 698 KB file for a normal rewrite. Search first:

```bash
rg -n -i 'Rule 5\\.1|procedural writing|maximum of 20 words' \
  /Users/namanbajpai/ocr/output/ASD-STE100_ISSUE9/ASD-STE100_ISSUE9.md
```

Read a bounded region around the match:

```bash
sed -n '3826,3940p' \
  /Users/namanbajpai/ocr/output/ASD-STE100_ISSUE9/ASD-STE100_ISSUE9.md
```

Useful regions:

| Topic | Markdown lines |
|---|---:|
| Guide and scope | 1513-1803 |
| Section 1: words | 1840-2719 |
| Section 2: multi-word nouns | 2720-2915 |
| Section 3: verbs | 2916-3374 |
| Section 4: sentences | 3375-3825 |
| Section 5: procedures | 3826-4161 |
| Section 6: descriptions | 4162-4454 |
| Section 7: safety | 4455-4594 |
| Section 8: punctuation and count | 4595-5032 |
| Section 9: writing practices | 5033-5704 |
| Dictionary guide | 5738-6231 |

## Scope and rights

The public package contains condensed study notes, original guidance on using
the rules, and linter code. It excludes the full standard, source archive,
extracted dictionary, and generated full-dictionary scripts. Keep those source
materials in the Git-ignored `vale/private/` directory. The code's MIT license
does not grant rights to redistribute the standard.

Use the official document for regulated work. Do not present OCR or these notes as
an official edition.
