/* Britain Elects style — generated from tokens.json by build.py. v1.2.0. Do not edit by hand. */
(function (root) {
  var T = {"version":"1.2.0","parties":{"con":{"names":["Conservative","the Conservatives","Con"],"fill":"#05718F","text":"#05718F","fillDark":"#1C7A98","textDark":"#368CAB"},"lab":{"names":["Labour","Labour","Lab"],"fill":"#CF4545","text":"#CF4545","fillDark":"#CF4545","textDark":"#DF5351"},"ldem":{"names":["Lib Dem","the Lib Dems","LDem"],"fill":"#FAA61A","text":"#9C6B25","fillDark":"#FAA61A","textDark":"#FAA61A"},"ref":{"names":["Reform","Reform","Ref"],"fill":"#15B6C2","text":"#298088","fillDark":"#15B6C2","textDark":"#15B6C2"},"grn":{"names":["Green","the Greens","Grn"],"fill":"#62B65A","text":"#4C8145","fillDark":"#62B65A","textDark":"#62B65A"},"snp":{"names":["SNP","the SNP","SNP"],"fill":"#F1EC3C","text":"#7C773A","fillDark":"#F1EC3C","textDark":"#F1EC3C"},"pc":{"names":["Plaid Cymru","Plaid Cymru","PC"],"fill":"#2F7865","text":"#2F7865","fillDark":"#357D6A","textDark":"#478F7B"},"rst":{"names":["Restore Britain","Restore","Restore"],"fill":"#485255","text":"#485255","fillDark":"#687376","textDark":"#7A8588"},"oth":{"names":["Others","the smaller parties","Oth"],"fill":"#A9ACA8","text":"#737573","fillDark":"#A9ACA8","textDark":"#A9ACA8"},"ind":{"names":["Independent","the independents","Ind"],"fill":"#7E817D","text":"#6B6E6A","fillDark":"#7E817D","textDark":"#9C9F9B"}},"secondaryParties":{"ukip":{"names":["UKIP","UKIP","UKIP"],"fill":"#6D3177","text":"#6D3177","fillDark":"#9A5AA5","textDark":"#B07ABA"},"alba":{"names":["Alba","Alba","Alba"],"fill":"#005EB8","text":"#005EB8","fillDark":"#3C82D0","textDark":"#5A96DA"},"dup":{"names":["DUP","the DUP","DUP"],"fill":"#B5442E","text":"#B5442E","fillDark":"#C8553E","textDark":"#DC6A52"},"sf":{"names":["Sinn F\u00e9in","Sinn F\u00e9in","SF"],"fill":"#326760","text":"#326760","fillDark":"#4A8178","textDark":"#5E948B"},"sdlp":{"names":["SDLP","the SDLP","SDLP"],"fill":"#2AA82C","text":"#227F24","fillDark":"#2AA82C","textDark":"#2AA82C"},"uup":{"names":["UUP","the UUP","UUP"],"fill":"#48A5EE","text":"#2A6FA8","fillDark":"#48A5EE","textDark":"#48A5EE"},"apni":{"names":["Alliance","Alliance","APNI"],"fill":"#F6CB2F","text":"#7F6A1C","fillDark":"#F6CB2F","textDark":"#F6CB2F"}},"aliases":{"conservative":"con","conservatives":"con","tory":"con","tories":"con","labour":"lab","ld":"ldem","libdem":"ldem","libdems":"ldem","liberaldemocrat":"ldem","liberaldemocrats":"ldem","reform":"ref","reformuk":"ref","brexit":"ref","brexitparty":"ref","green":"grn","greens":"grn","gre":"grn","plaid":"pc","plaidcymru":"pc","restore":"rst","restorebritain":"rst","independent":"ind","independents":"ind","other":"oth","others":"oth","sinnfein":"sf","alliance":"apni"},"signalAliases":{"pos":"positive","approve":"positive","approval":"positive","favourable":"positive","favorable":"positive","well":"positive","good":"positive","yes":"positive","satisfied":"positive","neg":"negative","disapprove":"negative","disapproval":"negative","unfavourable":"negative","unfavorable":"negative","badly":"negative","bad":"negative","no":"negative","dissatisfied":"negative","unsure":"neutral","dontknow":"neutral","dk":"neutral","neither":"neutral","undecided":"neutral"},"signal":{"positive":{"fill":"#2A6FB0","text":"#2A6FB0","fillDark":"#3274B5","textDark":"#4986C9"},"negative":{"fill":"#E07A1F","text":"#B35A0E","fillDark":"#E07A1F","textDark":"#E07A1F"},"neutral":{"fill":"#A9ACA8","text":"#737573","fillDark":"#7E817D","textDark":"#A9ACA8"}},"neutrals":{"light":{"bg":"#FFFFFF","surface":"#F5F5F5","border":"#DDDDDD","ink":"#1A1A1A","inkSecondary":"#555555","inkMuted":"#767676","grid":"#E5E5E5","baseline":"#1A1A1A","halo":"#FFFFFF"},"dark":{"bg":"#16181B","surface":"#1F2226","border":"#33373C","ink":"#F2F2F2","inkSecondary":"#B8BCC2","inkMuted":"#8D939A","grid":"#2C3035","baseline":"#E6E6E6","halo":"#16181B"}},"logo":{"light":{"top":"#05718F","left":"#D34C4C","right":"#777777","bottom":"#EBB82F","ink":"#181818"},"dark":{"top":"#2E95B8","left":"#E26060","right":"#A3A3A3","bottom":"#F0C03A","ink":"#F2F2F2"}},"type":{"fontImport":"https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,600;0,700;1,400&family=Roboto+Mono:wght@400;500;700&display=swap","family":"'IBM Plex Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif","familyFigures":"'Roboto Mono', ui-monospace, Menlo, Consolas, monospace","familyMono":"'Roboto Mono', ui-monospace, Menlo, Consolas, monospace","weights":{"regular":400,"semibold":600,"bold":700},"headingTracking":"-0.02em","scale":{"display":"2rem","h1":"1.5rem","h2":"1.125rem","body":"1rem","small":"0.8125rem","caption":"0.6875rem"},"lineHeight":{"tight":1.15,"body":1.5}},"ui":{"radius":5,"radiusMark":0},"chart":{"lineWidth":2.5,"haloWidth":3,"gridWidth":1,"baselineWidth":1.25,"radius":0}};
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
  BE.color = BE.fill; BE.colors = BE.colours;

  if (typeof module !== 'undefined' && module.exports) module.exports = BE;
  else root.BE = BE;
})(typeof window !== 'undefined' ? window : this);
