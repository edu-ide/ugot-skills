

# Measuring infographic density

Use measurement to locate suspicious regions, then decide from the render. Texture, ornament, and dark backgrounds can make screenshot pixel-density heuristics unreliable, so prefer DOM or SVG geometry when available.

## Minimal manifest

Create a JSON file with the delivery viewport and the boxes that matter:

```json
{
  "viewport": {"width": 760, "height": 1078},
  "elements": [
    {
      "id": "summary",
      "role": "container",
      "rect": {"x": 44, "y": 820, "width": 672, "height": 180},
      "padding": {"top": 20, "right": 24, "bottom": 20, "left": 24}
    },
    {
      "id": "summary-copy",
      "role": "content",
      "parent": "summary",
      "rect": {"x": 105, "y": 846, "width": 550, "height": 52}
    },
    {
      "id": "summary-frame",
      "role": "asset",
      "rect": {"x": 44, "y": 820, "width": 672, "height": 180},
      "intrinsic": {"width": 1050, "height": 312},
      "fit": "stretch"
    }
  ]
}
```

Roles:

- `container`: a card, section, quote panel, or page region that owns content;
- `content`: meaningful text, values, charts, or explanatory imagery;
- `heading`, `data`, and `card`: also treated as semantic content;
- `asset`: a raster asset with `intrinsic` dimensions;
- `decorative`: ornament excluded from semantic occupancy.

Add `parent` to every semantic child whose interior fill should be checked. Padding is optional and defaults to zero.

For framed raster panels, set `padding` to the **usable content inset**, including transparent pixels and border-safe space. Do not count a section heading outside the panel as summary copy. Text fill is:

```text
union height of rendered text line boxes / usable framed interior height
```

Record the empty area's layout owner and its parent sizing when diagnosing CSS. Useful optional manifest fields are `computed.display`, `computed.flex`, `computed.alignContent`, `computed.position`, `computed.height`, `computed.minHeight`, and `computed.gridTemplateRows`. Inherited flex-item sizing is often the cause even when the child changes itself to `display: grid`.

## Browser collection

Use `getBoundingClientRect()` at the exact delivery viewport. Record `naturalWidth` and `naturalHeight` for `<img>` elements. For CSS background assets, read the source file dimensions separately; computed CSS does not expose intrinsic background dimensions.

Do not resize the browser after collecting boxes. Animation must be disabled or allowed to settle before capture. Fonts must be loaded (`await document.fonts.ready`) before measuring.

A screenshot crop is not page-overflow evidence. Collect geometry from the full delivery page and verify against a full-page capture or the PDF rendered back at the same aspect ratio.

## Run the audit

```bash
python3 scripts/audit_layout_manifest.py manifest.json --output audit.json

# Compare against the same page before the edit.
python3 scripts/audit_layout_manifest.py after.json --baseline before.json --output audit.json
```

The audit reports:

- `aspect_deviation`: difference between displayed and intrinsic aspect ratio;
- `container_vertical_fill`: semantic child extent divided by usable container height;
- `container_area_fill`: semantic child area divided by usable container area;
- `largest_semantic_gap`: the largest vertical gap between semantic bands;
- `container_semantic_gap`: the largest gap between semantic children owned by one section;
- `largest_page_void`: the largest semantic void including top and bottom page edges;
- `overflow`: children extending beyond the padded parent interior.

Defaults flag aspect deviation above 5%, container vertical fill below 45%, page gaps above 8%, and same-section semantic gaps above 6% of viewport height. `--baseline` also reports semantic-coverage change and the largest void's before/after size and location; it flags a likely whitespace relocation when the visible gap moves without a material coverage gain. These are review triggers. Use `--strict` only when the project has adopted those defaults as release gates.

## Interpreting the two common failures

### Large quote frame, two short lines at the top

The frame is not evidence that the content needs height. First reduce the panel height. If the quote is the primary conclusion, enlarge and vertically center the text while retaining readable line length. Do not enlarge a lower illustration to consume the difference.

When the frame itself contains corners, quotation marks, or side rays, preserve those edge regions and shrink only the repeatable center with 9-slice rendering. Keeping the original whole-image ratio can still be the wrong composition when the copy is much shorter than the asset was designed for.

### Small cards at the top, large empty middle, summary pinned at the bottom

Look for a fixed section height, `space-between`, or an absolutely positioned summary. Let the section shrink to content, grow the cards and their typography, then bring the summary upward. If the source contains distinct supporting points, a second semantic row is preferable to a decorative filler asset.

Do not stop after setting `flex: none` or removing a fixed height. That can move the same blank band below the section while leaving total semantic coverage unchanged. Compare the before/after `largest_page_void`, its location, and semantic coverage at identical viewport dimensions.
