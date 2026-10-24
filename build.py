#!/usr/bin/env python3
"""
Regenerates be.css and be.js from tokens.json.

    python build.py

tokens.json is the single source of truth. Never edit be.css or be.js by hand:
they are overwritten on every build (the GitHub Action runs this on push).
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
T = json.loads((ROOT / "tokens.json").read_text())

HEADER = (
    "/* Britain Elects style — generated from tokens.json by build.py. "
    f"v{T['version']}. Do not edit by hand. */\n"
)


def clean(d):
    """Drop $comment keys."""
    if isinstance(d, dict):
        return {k: clean(v) for k, v in d.items() if not k.startswith("$")}
    return d


def css():
    light, dark = [], []
    allp = {**clean(T["parties"]), **clean(T["secondaryParties"])}
    for key, p in allp.items():
        light += [f"  --be-{key}: {p['fill']};", f"  --be-{key}-text: {p['text']};"]
        dark += [f"  --be-{key}: {p['fillDark']};", f"  --be-{key}-text: {p['textDark']};"]
    for key, s in clean(T["signal"]).items():
        light += [f"  --be-{key}: {s['fill']};", f"  --be-{key}-text: {s['text']};"]
        dark += [f"  --be-{key}: {s['fillDark']};", f"  --be-{key}-text: {s['textDark']};"]
    for mode, out in (("light", light), ("dark", dark)):
        for k, v in T["neutrals"][mode].items():
            name = "".join("-" + c.lower() if c.isupper() else c for c in k)
            out.append(f"  --be-{name}: {v};")
        for k, v in T["logo"][mode].items():
            out.append(f"  --be-logo-{k}: {v};")

    ty = T["type"]
    base = [
        f"  --be-font: {ty['family']};",
        f"  --be-font-mono: {ty['familyMono']};",
        f"  --be-font-figures: {ty['familyFigures']};",
        f"  --be-heading-tracking: {ty['headingTracking']};",
        f"  --be-weight-semibold: {ty['weights']['semibold']};",
        f"  --be-weight-regular: {ty['weights']['regular']};",
        f"  --be-weight-bold: {ty['weights']['bold']};",
        f"  --be-lh-tight: {ty['lineHeight']['tight']};",
        f"  --be-lh-body: {ty['lineHeight']['body']};",
    ] + [f"  --be-size-{k}: {v};" for k, v in ty["scale"].items()]
    ch = T["chart"]
    base += [
        f"  --be-line-width: {ch['lineWidth']}px;",
        f"  --be-halo-width: {ch['haloWidth']}px;",
        f"  --be-radius: {T['ui']['radius']}px;",
        f"  --be-radius-mark: {T['ui']['radiusMark']}px;",
    ]

    keys = list(allp) + list(clean(T["signal"]))
    utils = []
    for k in keys:
        utils.append(f".be-c-{k}{{color:var(--be-{k}-text)}}")
        utils.append(f".be-bg-{k}{{background-color:var(--be-{k})}}")

    L, D, B = "\n".join(light), "\n".join(dark), "\n".join(base)
    return (
        HEADER
        + f"@import url('{ty['fontImport']}');\n\n"
        + f":root {{\n{B}\n{L}\n}}\n\n"
        + "/* Dark: opt in with <html data-theme=\"dark\">, or data-theme=\"auto\" to follow the reader's system setting. */\n"
        + f":root[data-theme=\"dark\"] {{\n{D}\n}}\n"
        + f"@media (prefers-color-scheme: dark) {{\n  :root[data-theme=\"auto\"] {{\n{D}\n  }}\n}}\n\n"
        + "/* Opt-in base styles: add class=\"be\" to <body> (or any wrapper). */\n"
        + ".be{font-family:var(--be-font);font-size:var(--be-size-body);line-height:var(--be-lh-body);"
          "color:var(--be-ink);background:var(--be-bg);font-variant-numeric:tabular-nums lining-nums}\n"
        + ".be h1,.be h2,.be h3{font-weight:var(--be-weight-bold);line-height:var(--be-lh-tight);letter-spacing:var(--be-heading-tracking);margin:0 0 .5em}\n"
        + ".be h1{font-size:var(--be-size-h1)}.be h2{font-size:var(--be-size-h2)}\n"
        + ".be .be-display{font-size:var(--be-size-display);font-weight:var(--be-weight-bold);line-height:var(--be-lh-tight);letter-spacing:var(--be-heading-tracking)}\n"
        + ".be .be-figures,.be td.be-num{font-family:var(--be-font-figures);font-variant-numeric:tabular-nums}\n"
        + ".be small,.be .be-small{font-size:var(--be-size-small)}\n"
        + ".be .be-caption{font-size:var(--be-size-caption);color:var(--be-ink-muted)}\n"
        + ".be .be-muted{color:var(--be-ink-secondary)}\n\n"
        + "\n".join(utils) + "\n"
    )


JS_RUNTIME = r"""
(function (root) {
  var T = __TOKENS__;
  var ALL = Object.assign({}, T.parties, T.secondaryParties);
  var FORMS = { general: 0, analysis: 1, short: 2 };

  function norm(k) { return String(k == null ? '' : k).toLowerCase().replace(/[^a-z]/g, ''); }
  function key(k) {
    var n = norm(k);
    if (ALL[n]) return n;
    if (T.aliases[n]) return T.aliases[n];
    var base = norm(String(k).split('(')[0]);
    if (ALL[base]) return base;
    if (T.aliases[base]) return T.aliases[base];
    return null;
  }
  /** Series that aren't parties: 'Positive', 'Approve', 'Unsure', "Don't know"... */
  function sig(k) {
    var n = norm(k);
    return T.signal[n] || T.signal[T.signalAliases[n]] || null;
  }
  function isDark(opt) {
    if (opt && typeof opt.dark === 'boolean') return opt.dark;
    var el = typeof document !== 'undefined' && document.documentElement;
    var t = el && el.getAttribute('data-theme');
    if (t === 'dark') return true;
    if (t === 'auto' && root.matchMedia) return root.matchMedia('(prefers-color-scheme: dark)').matches;
    return false;
  }
  function pick(entry, kind, opt) {
    if (!entry) return null;
    var d = isDark(opt);
    return kind === 'text' ? (d ? entry.textDark : entry.text) : (d ? entry.fillDark : entry.fill);
  }

  var BE = {
    version: T.version,
    tokens: T,
    /** Canonical key for any spelling: 'Lib Dem', 'LD', 'ldem' -> 'ldem'. null if unknown. */
    key: key,
    party: function (k) { var c = key(k); return c ? Object.assign({ key: c }, ALL[c]) : null; },
    /** Line / map / bar colour. opt.dark forces a mode; default reads <html data-theme>. */
    fill: function (k, opt) { return pick(ALL[key(k)] || sig(k), 'fill', opt); },
    /** Colour for party-coloured text (passes 4.5:1 on the background). */
    text: function (k, opt) { return pick(ALL[key(k)] || sig(k), 'text', opt); },
    /** Party name in one of the three house forms: 'general' | 'analysis' | 'short'. */
    name: function (k, form) { var p = ALL[key(k)]; return p ? p.names[FORMS[form || 'general']] : k; },
    /** Map of the caller's own keys to fills: BE.colours(['con','lab']) -> {con:'#..', lab:'#..'} */
    colours: function (keys, opt) {
      var out = {};
      (keys || Object.keys(T.parties)).forEach(function (k) { var c = BE.fill(k, opt); if (c) out[k] = c; });
      return out;
    },
    signal: function (which, kind, opt) { return pick(sig(which), kind || 'fill', opt); },
    neutral: function (name, opt) { return T.neutrals[isDark(opt) ? 'dark' : 'light'][name]; },
    logo: function (opt) { return T.logo[isDark(opt) ? 'dark' : 'light']; },
    font: T.type.family,
    fontFigures: T.type.familyFigures,
    isDark: isDark,
    /**
     * The result line used at the top of map panels:
     * "■ GRN GAIN FROM ■ LAB" (or "■ GRN HOLD"), party names in their own text colours.
     * Unknown parties fall back to the label you pass in `names`.
     */
    resultLine: function (win, prev, names) {
      names = names || {};
      function part(k) {
        var label = BE.key(k) ? BE.name(k, 'short') : (names[k] || k);
        return '<i class="be-sq" style="background:' + (BE.fill(k) || '#A9ACA8') + '"></i>' +
          '<span class="be-party" style="color:' + (BE.text(k) || 'inherit') + '">' + label + '</span>';
      }
      var gain = prev && BE.key(prev) !== BE.key(win) && String(prev) !== String(win);
      return part(win) + (gain ? ' <span class="be-gf">gain from</span> ' + part(prev) : ' <span class="be-gf">hold</span>');
    },
    /**
     * Applies a result to a panel element: sets the top rule colours (--be-win / --be-prev),
     * marks gains so the rule splits, and fills any .result-bar-text inside it.
     * Pass prev = null when there is no previous result (the rule is then one colour, no text change).
     */
    setResult: function (el, win, prev, names) {
      if (!el) return;
      el.style.setProperty('--be-win', BE.fill(win) || '#A9ACA8');
      el.style.setProperty('--be-prev', BE.fill(prev || win) || '#A9ACA8');
      el.classList.add('be-has-result');
      el.classList.toggle('be-gain', !!prev && BE.key(prev) !== BE.key(win) && String(prev) !== String(win));
      var t = el.querySelector('.result-bar-text');
      if (t && prev !== null && prev !== undefined) t.innerHTML = BE.resultLine(win, prev, names);
    }
  };
  /* Vote-share bins: one set of ranges for every party and project (tokens.share). */
  function mix(hex, t) {
    var a = String(hex).replace('#', ''), b = T.share.blendWith.replace('#', '');
    var ch = function (h, i) { return parseInt(h.slice(i, i + 2), 16); };
    var out = [0, 2, 4].map(function (i) { return Math.round(ch(b, i) + (ch(a, i) - ch(b, i)) * t); });
    return 'rgb(' + out.join(',') + ')';
  }
  /** Bin edges in %: [10, 20, 30, 40, 50, 60] */
  BE.shareBreaks = T.share.breaks.slice();
  /** Which bin a share (in %) falls in: 0 = under the first break. */
  BE.shareBin = function (pct) {
    var i = 0;
    while (i < T.share.breaks.length && pct >= T.share.breaks[i]) i++;
    return i;
  };
  /** One colour per bin for a party (or a hex), lightest first. */
  BE.shareColours = function (k, opt) {
    var hex = (k && k.charAt && k.charAt(0) === '#') ? k : (BE.fill(k, opt) || '#A9ACA8');
    return T.share.tints.map(function (t) { return mix(hex, t); });
  };
  /** Colour for one share (in %). */
  BE.shareColour = function (k, pct, opt) { return BE.shareColours(k, opt)[BE.shareBin(pct || 0)]; };
  /** MapLibre stepped expression over a numeric share (in %): BE.shareStep('lab', ['get', 'lab_pct']) */
  BE.shareStep = function (k, valueExpr, opt) {
    var c = BE.shareColours(k, opt), e = ['step', valueExpr, c[0]];
    T.share.breaks.forEach(function (b, i) { e.push(b, c[i + 1]); });
    return e;
  };
  /** Legend labels, one per bin: ['<10%', '10–20%', ... '60%+'] */
  BE.shareLabels = function () {
    var b = T.share.breaks, out = ['<' + b[0] + '%'];
    for (var i = 1; i < b.length; i++) out.push(b[i - 1] + '–' + b[i] + '%');
    out.push(b[b.length - 1] + '%+');
    return out;
  };
  /** Fills a legend element with the binned key for a party: seven swatches, break values beneath. */
  BE.shareLegend = function (el, k, opt) {
    if (!el) return;
    var c = BE.shareColours(k, opt), b = T.share.breaks;
    el.classList.add('be-share-legend');
    el.innerHTML = c.map(function (col, i) {
      var tick = i ? '<b>' + b[i - 1] + (i === b.length ? '%' : '') + '</b>' : '';
      return '<span class="be-share-bin"><i style="background:' + col + '"></i>' + tick + '</span>';
    }).join('');
  };
  BE.color = BE.fill; BE.colors = BE.colours;

  if (typeof module !== 'undefined' && module.exports) module.exports = BE;
  else root.BE = BE;
})(typeof window !== 'undefined' ? window : this);
"""


def js():
    tok = json.dumps(clean(T), separators=(",", ":"))
    return HEADER + JS_RUNTIME.replace("__TOKENS__", tok).lstrip("\n")


if __name__ == "__main__":
    (ROOT / "be.css").write_text(css())
    (ROOT / "be.js").write_text(js())
    print("Built be.css and be.js from tokens.json v" + T["version"])
