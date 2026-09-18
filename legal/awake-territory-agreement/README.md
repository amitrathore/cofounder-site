# Awake Territory Agreement

A general business territory operating agreement contributed by Amit Rathore and AwakeVC. Adapted from the supplied territory operating agreement for use beyond its original industry and geography.

## Current release

- Version: 1.0; date: 2026-09-17
- Canonical source: [awake-territory-agreement.md](./awake-territory-agreement.md)
- Orientation: general business; parties, jurisdiction, industry, territory, and economics are configurable
- Binding posture: intended to bind when completed and executed
- Independent legal review: not recorded
- Template license: [CC BY 4.0](./LICENSE.md)

## Files

- [Online reading page](./index.html), with the complete agreement as accessible HTML
- [PDF](./awake-territory-agreement.pdf), rendered from Word
- [Editable Word](./awake-territory-agreement.docx), with highlighted fields
- [Completion guide](./guide.md), including material changes from the source
- [Disclaimer](./DISCLAIMER.md), [changelog](./CHANGELOG.md), and [contribution instructions](./CONTRIBUTING.md)
- `build.py`, generating Word and HTML from canonical Markdown; `reader.css`, scoped reader styles

## Rebuild and verify

Run `python build.py` in an environment with `python-docx`. It supports the headings-and-paragraphs subset used by the canonical source and deliberately rejects unsupported block syntax.

Render the generated DOCX using the Documents skill's `render_docx.py`, with `--output_dir` pointing to a temporary directory and `--emit_pdf`. Inspect every page image, then copy the emitted PDF here as `awake-territory-agreement.pdf`. Reconcile extracted PDF text against the Markdown and Word, check every page link, and verify no source-specific identifiers remain. Do not publish a stale PDF after source changes.

## Scope

The grant is exclusive and performance-conditioned. Existing, inbound, automated, and centrally generated business falls within its economics when attributable to the Territory, except expressly reserved activities. Company supplies agreed resources and retains its intellectual property. The template includes no equity grant, automatic renewal, or termination for convenience.

The guide documents substantive drafting choices, including pass-through receipts, negative periods, conversion of exclusivity, and later collections on pre-termination business. Adapt those choices with counsel; this is not a universal substitute for franchise, agency, or distribution documentation.
