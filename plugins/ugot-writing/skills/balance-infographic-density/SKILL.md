---
name: balance-infographic-density
description: Rebalance static infographic, report, poster, and PDF-render layouts when oversized containers, tiny text, dead zones, stretched assets, or illustrations mismatched to the content weaken communication. Use for rendered HTML/CSS/SVG/React pages, not ordinary application spacing tweaks.
principle: pro-quality
---

# Balance Infographic Density

Make the information—not decorative art—occupy the page. Preserve the source text, numbers, reading order, and design tone while producing a dense, legible composition whose asset proportions remain intact.

## Required evidence

Start from an actual render at the delivery viewport. Do not approve a layout from CSS values or component structure alone. Keep a before render and compare it with the final render at the same dimensions.

Before editing, identify:

- the page's one-sentence takeaway and reading order;
- the intrinsic dimensions of every raster frame, plaque, card, and icon;
- semantic content boxes versus purely decorative layers;
- fixed heights, `min-height`, absolute positioning, `space-between`, oversized grid rows, and `background-size: 100% 100%`;
- the computed layout properties of the empty area's nearest owner **and its sizing as a flex/grid item**. Record the parent display mode plus the child's `flex`, `align-self`, `height`, `min-height`, grid row, and positioning instead of inspecting only the child's own `display`.
- whether the task is in **asset-backed fidelity mode**: enable it whenever the user asks to match a native/reference infographic, explicitly rejects CSS-only decoration, or supplies a reusable premium asset set. In this mode, inventory the asset source for every visible decorative surface before changing layout.

For a repeatable DOM audit, read [references/measurement.md](references/measurement.md). When box geometry is available, run `scripts/audit_layout_manifest.py` to expose low-fill containers, large vertical dead zones, overflow, and asset distortion.

## Semantic asset fit and on-demand generation

An available asset is not necessarily a suitable asset. Check meaning before applying the density correction ladder; a semantic mismatch requires replacement even when the layout already fits.

- For each explanatory image, identify the exact feature, relationship, or change it must communicate. Inspect the image itself, not only its filename, caption, or alt text. Record the intended meaning, asset path, and consuming pages in the existing asset mapping or manifest.
- Reuse only when the depicted action and relationship support that meaning at delivery size. Do not relabel one illustration to cover unrelated concepts, rewrite accurate content to fit available art, or use a vague symbol that needs a paragraph to explain its relevance. For example, people building a bridge can convey cooperation but do not by themselves convey a mismatch between outward activity and one's inner pace.
- When image-backed production is authorized and no existing asset fits, create the needed scene during the current workflow using the available image-generation tool and applicable imagegen instructions. Do not stop at a recommendation, wait for another request for each missing asset, or fill the slot with an unsuitable substitute. Generate only what the current content needs, within the authorized scope and resource limits.
- Match the approved reference's style and setting. Specify the subject, action, relationship, target aspect ratio, and text-safe area; request transparent exteriors for composited cutouts or frames. Use paired scenes when a before/after or contrasting relationship is the point. Do not invent a causal relationship, event, or outcome to make a more dramatic picture.
- Inspect each generated asset before integrating it. Reject unclear meaning, a wrong action, broken transparency, illegible small details, or a style mismatch. Save accepted assets in the project's existing asset library and register them in its mapping/gallery when present. Keep personalized text, chart values, and data arrows live rather than baked into the image.
- If generation is unavailable or repeatedly fails the required meaning, report the specific unfilled role and the delivery limitation. Do not silently reuse a misleading image or claim that the replacement was completed.

Review a multi-page contact sheet for repeated art carrying different meanings. Repetition is acceptable for the same concept; variation for its own sake and novelty quotas are not required. Replace mismatches in the explanatory block itself rather than adding decorative filler below it.

## Content-first correction ladder

Use the first applicable intervention and render again before escalating.

1. **Remove artificial space.** Replace unjustified fixed heights and surplus grid rows with content-driven sizing. Eliminate `space-between` or bottom anchoring that creates a hollow middle. Reduce gaps and padding while retaining a deliberate outer safe area. Re-measure after this step: a fix is invalid when the same void merely moves below the section or above the footer.
2. **Increase semantic content.** Enlarge the title, section label, body copy, values, and explanatory icons together. Adjust line length and line height so the copy remains readable; do not merely scale one font until it collides.
3. **Recompose the blocks.** Move the summary closer to its evidence, change row/column structure, let cards grow, or split a thin row into a stronger two-tier composition. The eye should move continuously from premise to evidence to interpretation.
4. **Use more of the authorized source material.** If the source already contains relevant evidence or interpretation, restore it rather than leaving an empty panel. Never invent claims, numbers, or personalized readings to fill space.
5. **Create or select a new semantic asset when needed for density.** Add a topic-specific diagram, icon cluster, or frame variant when it improves comprehension or balances an otherwise irreducible gap. This ordering applies to space correction, not to semantic mismatches, which require replacement immediately under the preceding section. A larger footer illustration, generic ornament, or duplicated icon is not a density fix.

## Asset proportion rules

- Treat `background-size: 100% 100%` as an inspection trigger, not an automatic failure. Approve or reject a raster by its measured displayed ratio: it may be safe when the target box matches the intrinsic ratio, but must not exceed the 5% deviation gate.
- Use an ordinary `<img>` with intrinsic ratio for standalone art and icons.
- Use `object-fit: contain` when the entire asset must remain visible; use `cover` only for crop-safe textures or scenery.
- Use CSS borders, SVG, or 9-slice `border-image` for containers whose center must expand while corners and endcaps remain fixed.
- For a short one- or two-line summary inside a tall fixed-ratio frame, prefer a compact 9-slice frame that removes excess center height. Measure transparent insets, quotation marks, side rays, and corner-safe regions before choosing slice values.
- Use a dedicated frame variant when 9-slice cannot preserve the source engraving or when the target shape differs materially from the source.
- Do not stretch a generated asset merely because its subject is centered; transparent padding is still part of its composition and must be inspected.

## Asset-backed fidelity mode

In asset-backed fidelity mode, CSS owns layout and live typography, not the illustrated finish. Every visible decorative surface must resolve to a real raster or vector asset:

- page frame and textured background;
- section plaque, page-number badge, evidence/basis strip, and summary/quote frame;
- each card, capsule, medallion, icon plate, and callout container;
- topic-specific icon or illustration when the reference uses one.

Do not count a page background as coverage for nested cards or plaques. Do not count a texture-only fill as a card frame. Reusing one generic stretched frame for visibly different shapes is also a failure: use a compatible 9-slice asset or a dedicated shape variant. A surface is asset-backed only when the element, one of its pseudo-elements, or a dedicated child image resolves to a loaded local asset assigned to that surface.

Keep semantic text, numbers, and labels as live HTML/SVG so they remain sharp and personalized. Charts, plotted data, connector lines, and simple data markers may remain SVG, canvas, or CSS because they encode values rather than decorative finish. Plain layout wrappers with no visible fill, border, shadow, or ornament are not surfaces and need no asset.

Before approval, run a DOM asset audit at the delivery viewport:

1. Mark every decorative surface with a stable audit selector or role.
2. Collect the element plus `::before` and `::after` computed `background-image`, `border-image-source`, `mask-image`, and dedicated child `<img>` sources.
3. Fail when a marked surface has no loaded local image, when a source is external, or when one page-level image is being claimed for an unbacked nested surface.
4. Check each raster's displayed ratio or 9-slice behavior, then render all consumers of a shared asset.

CSS gradients, solid fills, borders, shadows, `clip-path`, and text glyphs may supplement an asset but cannot be the sole decorative treatment of a marked surface in this mode.

## Visual acceptance gates

Judge the final page at delivery scale, not zoomed in.

- No semantic block is clipped, overlapped, or pushed outside its container.
- Distinguish an intentionally cropped diagnostic screenshot from the delivered page. Overflow fails only when DOM geometry or a full-page final render proves that content is outside the real page/container bounds.
- No raster frame, card, plaque, icon, or illustration has more than 5% aspect-ratio deviation unless cropping is intentional and documented.
- In asset-backed fidelity mode, the DOM asset audit reports zero unbacked decorative surfaces and zero broken or external asset sources.
- Every explanatory image supports its assigned meaning in the actual render. Loaded files, matching colors, and distinct alt text do not establish semantic fit; inspect reused scenes across their consumers and reject misleading substitutions.
- A text-only summary panel should usually use at least 45% of its usable interior height. Define this as the union height of the actual text line boxes divided by the frame's usable interior: exclude transparent raster insets, border-safe inset, heading outside the panel, and CSS padding from the denominator. If it misses the gate, shrink the panel or strengthen the content hierarchy.
- A vertical gap larger than roughly 8% of page height is a page-level review trigger. A dead zone between semantic siblings in the same section gets a stricter 6% trigger. Keep either only when it clearly separates narrative acts or reserves a purposeful visual focal area.
- Compare the largest void's size **and location** before and after. Do not approve a change that closes the middle only by moving equivalent blank space under the content, above the footer, or into another section.
- Body text remains comfortably readable at final PDF or image size. For an A5 consumer infographic, 10–13 pt is a useful working range; verify the actual embedded/rendered size.
- Decorative art does not grow while titles, explanations, values, and cards remain undersized.
- The final render makes the page's takeaway understandable within a few seconds, then rewards closer reading.

Thresholds are diagnostic triggers, not permission to optimize a score blindly. A visually intentional exception must be visible in the render and explained in the handoff.

## Verification loop

Render every affected page at its final viewport and also render the assembled PDF back to images. Inspect representative pages at full size plus a contact sheet for rhythm across the set. If one CSS rule or shared asset changed, audit every page that consumes it—not only the page where the defect was reported. For density corrections, collect both manifests and pass the earlier one with `--baseline`; an unchanged semantic coverage plus a relocated void is still a review finding.

Report:

- which dead zones or distortions were found;
- which correction-ladder step fixed each class of issue;
- which semantic mismatches were replaced, which new assets were generated and integrated, and any unresolved asset roles;
- before/after render paths and delivery dimensions;
- remaining intentional whitespace or exceptions;
- the final PDF/image path and any automated audit result.
