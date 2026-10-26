/* Britain Elects house base map for MapLibre (hand-written; load after be.js).
 *
 *   map style:   BE.basemap.style({ sources: { wards: {...} }, layers: [ ...your results layers ] })
 *   results:     paint: { 'fill-color': ..., 'fill-opacity': BE.basemap.fillOpacity() }   // 66%, 33% when pinned
 *   boundaries:  paint: BE.basemap.boundary()
 *   pinned line: paint: BE.basemap.pinnedLine()
 *   panel tools: BE.basemap.panelTools({ panel, drawerSlot, onZoom, onClose })      // magnifier + ×
 *   ward bounds: BE.basemap.bounds(feature)                                        // for fitBounds
 *
 * Decisions (Bobby, 23 Oct 2026): warm ground, warm built-up cover and brown roads drawn solid
 * beneath the results; grey water; no parks; no buildings; results at 66%; a clicked ward drops to
 * 33% so its streets and settlements show through; dark boundaries; IBM Plex Sans labels with
 * cities and towns larger and semibold; hamlets named from close in.
 */
(function (root) {
  var BE = root.BE || (root.BE = {});
  var FONTS = 'https://glasgow46239.github.io/style/fonts/{fontstack}/{range}.pbf';
  var PINNED = ['boolean', ['feature-state', 'pinned'], false];
  var cls = function (city, town, other, hamlet) {
    return ['match', ['get', 'class'], 'city', city, 'town', town, 'hamlet', hamlet, other];
  };
  var road = function (id, classes, colour, width) {
    return { id: id, type: 'line', source: 'basemap', 'source-layer': 'transportation',
      filter: ['in', ['get', 'class'], ['literal', classes]],
      paint: { 'line-color': colour, 'line-width': width } };
  };

  function below() {
    return [
      { id: 'bg', type: 'background', paint: { 'background-color': 'rgb(245, 242, 232)' } },
      { id: 'water', type: 'fill', source: 'basemap', 'source-layer': 'water', paint: { 'fill-color': '#DCE3E7' } },
      { id: 'landuse-residential', type: 'fill', source: 'basemap', 'source-layer': 'landuse',
        filter: ['in', ['get', 'class'], ['literal', ['residential', 'suburb', 'neighbourhood']]],
        paint: { 'fill-color': 'rgb(222, 211, 190)', 'fill-opacity': 0.45 } },
      road('road-path', ['path', 'track', 'service'], 'rgb(200,195,185)', ['interpolate', ['linear'], ['zoom'], 13, 0.4, 17, 1.2]),
      road('road-minor', ['minor', 'residential'], 'rgb(210,205,192)', ['interpolate', ['linear'], ['zoom'], 11, 0.4, 15, 2]),
      road('road-secondary', ['secondary', 'tertiary'], 'rgb(200,193,178)', ['interpolate', ['linear'], ['zoom'], 9, 0.5, 14, 3]),
      road('road-primary', ['primary'], 'rgb(188,178,160)', ['interpolate', ['linear'], ['zoom'], 8, 0.8, 14, 4]),
      road('road-motorway', ['motorway', 'trunk'], 'rgb(175,165,145)', ['interpolate', ['linear'], ['zoom'], 6, 1, 14, 5]),
      { id: 'railway', type: 'line', source: 'basemap', 'source-layer': 'transportation',
        filter: ['==', ['get', 'class'], 'rail'],
        paint: { 'line-color': 'hsl(34,12%,66%)', 'line-width': 1, 'line-opacity': 0.7 } },
    ];
  }

  function labels() {
    var label = function (id, classes, size, font, minzoom) {
      var l = {
        id: id, type: 'symbol', source: 'basemap', 'source-layer': 'place',
        filter: ['in', ['get', 'class'], ['literal', classes]],
        // name:latin: a Latin-script name for places whose local name isn't (the
        // house glyphs only carry Latin; other ranges are empty placeholders)
        layout: { 'text-field': ['coalesce', ['get', 'name:latin'], ['get', 'name']], 'text-font': font, 'text-size': size, 'text-anchor': 'center', 'text-max-width': 8 },
        paint: { 'text-color': 'hsl(0,0%,25%)', 'text-halo-color': 'hsla(0,0%,100%,0.85)', 'text-halo-width': 2 },
      };
      if (minzoom) l.minzoom = minzoom;
      return l;
    };
    return [
      // Hamlets: named from close in only, smallest
      label('place-labels-hamlet', ['hamlet'], ['interpolate', ['linear'], ['zoom'], 12, 10, 16, 13], ['IBM Plex Sans Regular'], 12),
      // Suburbs and villages, then towns and cities a step larger in semibold (later layers win label collisions)
      label('place-labels', ['suburb', 'village'], ['interpolate', ['linear'], ['zoom'], 6, 9, 9, 10, 13, 14, 16, 15], ['IBM Plex Sans Regular']),
      label('place-labels-major', ['city', 'town'],
        ['interpolate', ['linear'], ['zoom'], 6, cls(12, 10.5, 10.5, 10.5), 9, cls(14, 12.5, 12.5, 12.5), 13, cls(18, 16, 16, 16), 16, cls(20, 18, 18, 18)],
        ['IBM Plex Sans SemiBold']),
    ];
  }

  function bounds(feature) {
    var g = feature && feature.geometry;
    if (!g) return null;
    var polys = g.type === 'Polygon' ? [g.coordinates] : g.type === 'MultiPolygon' ? g.coordinates : [];
    var w = 180, s = 90, e = -180, n = -90;
    polys.forEach(function (p) { p[0].forEach(function (c) { w = Math.min(w, c[0]); e = Math.max(e, c[0]); s = Math.min(s, c[1]); n = Math.max(n, c[1]); }); });
    return polys.length ? [[w, s], [e, n]] : null;
  }

  var MAG = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
    + '<circle cx="6.75" cy="6.75" r="4.75"/><path d="M10.25 10.25 14.5 14.5" stroke-linecap="round"/></svg>';
  function button(kind, label, fn) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'bm-icon-btn'; b.title = label; b.setAttribute('aria-label', label);
    if (kind === 'zoom') b.innerHTML = MAG; else b.textContent = '×';
    b.addEventListener('click', function (ev) { ev.stopPropagation(); fn(); });
    return b;
  }

  BE.basemap = {
    glyphs: FONTS,
    below: below,
    labels: labels,
    sources: function () { return { basemap: { type: 'vector', url: 'https://tiles.openfreemap.org/planet' } }; },
    /** Full style: house base map beneath your layers, labels on top. */
    style: function (opt) {
      var src = this.sources();
      Object.keys(opt.sources || {}).forEach(function (k) { src[k] = opt.sources[k]; });
      return { version: 8, glyphs: FONTS, sources: src, layers: below().concat(opt.layers || [], labels()) };
    },
    /** Results opacity: `base` normally (66% by default), 33% on the pinned (clicked) feature. */
    fillOpacity: function (base) { return ['case', PINNED, 0.33, base == null ? 0.66 : base]; },
    boundary: function () {
      return {
        'line-color': '#1A1A1A',
        'line-opacity': ['interpolate', ['linear'], ['zoom'], 5, 0.25, 9, 0.45],
        'line-width': ['interpolate', ['linear'], ['zoom'], 5, 0.15, 9, 0.5, 12, 1, 15, 1.5],
      };
    },
    pinnedLine: function () {
      return { 'line-color': '#111111', 'line-width': 2, 'line-opacity': ['case', PINNED, 1, 0] };
    },
    bounds: bounds,
    /** Adds the magnifier and close buttons to the panel (and the mobile drawer, if given). */
    panelTools: function (o) {
      var t = document.createElement('div');
      t.className = 'bm-panel-tools';
      t.append(button('zoom', o.zoomLabel || 'Zoom to this area', o.onZoom), button('close', 'Close', o.onClose));
      o.panel.appendChild(t);
      if (o.drawerSlot) {
        var d = document.createElement('div');
        d.className = 'bm-drawer-tools';
        d.append(button('zoom', o.zoomLabel || 'Zoom to this area', o.onZoom), button('close', 'Close', o.onClose));
        o.drawerSlot.appendChild(d);
      }
      document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') o.onClose(); });
    },
  };
})(typeof window !== 'undefined' ? window : this);
