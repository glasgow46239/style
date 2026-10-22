# Britain Elects style

One source of truth for colours, type and chart rules across every Britain Elects project.

**Style guide:** https://glasgow46239.github.io/style/

## The one rule

Edit **`tokens.json`** for colours and type (and `be-map.css` for map panels). On push, a GitHub Action runs `build.py`, which regenerates:

| File | Used by |
|---|---|
| `be.css` | CSS custom properties (`--be-lab`, `--be-lab-text`, `--be-font`…) plus `be-c-*` / `be-bg-*` classes |
| `be.js`  | `window.BE` — `BE.setResult(panel, win, prev)`, `BE.fill('Lib Dem')`, `BE.text('ldem')`, `BE.name('grn','analysis')`, `BE.signal('negative')` |
| `be-map.css` | Hand-written. Shared map results/history panels (le2026, learchive, Britain Predicts) |
| `index.html` | The style guide page (reads `be.js`, so it always matches) |

Python projects (benma) fetch `tokens.json` directly — see `brand.py` in that repo.

## Linking a project

```html
<link rel="stylesheet" href="https://glasgow46239.github.io/style/be.css">
<script src="https://glasgow46239.github.io/style/be.js"></script>
```

Changes go live everywhere on the next page load. To freeze a project on a version, tag a release here (`v1.0.0`) and link
`https://cdn.jsdelivr.net/gh/glasgow46239/style@v1.0.0/be.js` instead.

## Dark backgrounds

Pages are light by default. `<html data-theme="dark">` switches to the dark-background values; `data-theme="auto"` follows the reader's system setting.

## Logo

`logo/mark.svg` (light backgrounds), `logo/mark-dark.svg` (dark/broadcast), `logo/mark-mono-black.svg`, `logo/mark-mono-white.svg`. Logo colours are fixed brand colours, deliberately separate from the party palette.
