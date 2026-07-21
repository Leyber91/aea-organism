/* seals.js — THE SEAL PRESS: the 29 element seals + the three map-glyph states, generated.
   Governance: A11_SIGNATURE.md §3.3 (the shape grammar is BINDING — hexagon=principles ·
   pentagon=axes · triangle=verbs · square=mechanics · diamond=ops · circle=seeds; six shapes,
   twenty-nine elements, zero icons) · 02_VISUAL_LAW.md §1 (two inks: structure
   rgba(120,155,175,x) at EXACTLY .70/.45/.28/.14/.08; amber #ffb000 hot / #d4a24c warm),
   §4.1 (the concentric field is the sacred motif), §4.3 (no representational pictogram may
   ever enter — every engraving here is built from lines, arcs, rings and the six shapes),
   §5 (corner brackets, never closed boxes) · E1_CODE_ARCHITECTURE.md §2.2 (init(GAME)/
   dispose(); no cross-module globals beyond the GAME contract — window.SEALS is the module
   namespace, the world.html/ENGINE/BENCH idiom, and it adds no other), §4.4 (ONE truth per
   fact: names and proof strings are READ from window.AEA, never copied into this file).
   Reference sheets: design/concepts/B1_axis_principle_seals.png (pentagon + hexagon frames,
   the caption block with its proof line) · B2_seed_seals.png (circle frames) ·
   B3_verb_mechanic_op_seals.png (triangle / square / diamond) · A4_map_glyphs_seals.png
   (the three states: hidden dotted / sensed dashed / known solid+amber).

   Determinism law: an element's engraving is a pure function of its family and its index —
   the same element presses the same seal forever (FNV-1a over the element id seeds an LCG;
   no Math.random anywhere in this file). A seal that changed between two viewings would be
   a lie about what the element IS.

   Amber law (audited per seal, and the audit is ON the proof sheet — samples/seals_sample.html
   counts it live): amber appears on KNOWN-state glyphs, and on at most ONE accent per seal.
   ONE accent means one contiguous mark — a lit route and the node it terminates in count as
   one (B1's AX-P path and its cap; B2's SD-04 elbow), which is the only case that emits two
   amber references. hidden and sensed seals are entirely cold — 0 amber, measured.
   opts.live promotes the accent from warm #d4a24c (earned, idle) to hot #ffb000 (working now).

   Honesty law: the caption prints the element's REAL proof string from window.AEA. A seal
   whose element is not yet known prints the placeholder dashes (DASH) — never a value.
   This module owns no listeners, no timers, no fetches and no GPU resources; dispose()
   therefore releases the index and the GAME ref, and that is the whole of it. */
window.SEALS = (function () {
  "use strict";

  var GAME = null;
  var IDX = null;                      /* id -> record, built in init from window.AEA */

  /* ---- the two inks (02 §1 — five structure opacities and no others) ---- */
  var S = {
    a70: "rgba(120,155,175,.70)",
    a45: "rgba(120,155,175,.45)",
    a28: "rgba(120,155,175,.28)",
    a14: "rgba(120,155,175,.14)",
    a08: "rgba(120,155,175,.08)"
  };
  var HOT = "#ffb000", WARM = "#d4a24c";
  var DASH = "—.——";    /* the honest placeholder for a value with no live source */
  var FONT = "'IBM Plex Mono',Consolas,monospace";

  /* ---- family -> frame shape (A11 §3.3, binding) ---- */
  var SHAPE_OF = {
    seeds: "circle", axes: "pentagon", principles: "hexagon",
    verbs: "triangle", mechanics: "square", ops: "diamond"
  };
  var SHAPES = ["circle", "pentagon", "hexagon", "triangle", "square", "diamond"];
  /* sides + start angle (degrees). The A4 sheet's orientations: pentagon and triangle point
     up, hexagon points left/right, square sits axis-aligned, diamond stands on its point. */
  var GEOM = {
    pentagon: { n: 5, a0: -90 }, hexagon: { n: 6, a0: 0 },
    triangle: { n: 3, a0: -90 }, square: { n: 4, a0: -45 }, diamond: { n: 4, a0: -90 }
  };
  var STATES = ["hidden", "sensed", "known"];

  /* ---- deterministic seed: FNV-1a (shift form — ES5 has no Math.imul) ---- */
  function hash(str) {
    var h = 2166136261, i;
    for (i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0;
    }
    return h >>> 0;
  }
  /* LCG — products stay under 2^53, so the arithmetic is exact and portable */
  function rng(seed) {
    var s = seed >>> 0;
    return function () { s = (s * 1664525 + 1013904223) % 4294967296; return s / 4294967296; };
  }

  /* ---- svg primitives ---- */
  function esc(t) {
    return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function n2(v) { return Math.round(v * 100) / 100; }
  function attrs(o) {
    var k, out = "";
    for (k in o) if (o.hasOwnProperty(k) && o[k] !== null && o[k] !== undefined && o[k] !== "") {
      out += " " + k + '="' + o[k] + '"';
    }
    return out;
  }
  function line(x1, y1, x2, y2, ink, w, dash) {
    return "<line" + attrs({ x1: n2(x1), y1: n2(y1), x2: n2(x2), y2: n2(y2),
      stroke: ink, "stroke-width": w || 1, "stroke-dasharray": dash || "" }) + "/>";
  }
  function circ(cx, cy, r, ink, w, dash, fill) {
    return "<circle" + attrs({ cx: n2(cx), cy: n2(cy), r: n2(r), fill: fill || "none",
      stroke: ink || "", "stroke-width": ink ? (w || 1) : "", "stroke-dasharray": dash || "" }) + "/>";
  }
  function path(d, ink, w, dash, cap) {
    return "<path" + attrs({ d: d, fill: "none", stroke: ink, "stroke-width": w || 1,
      "stroke-dasharray": dash || "", "stroke-linecap": cap || "butt",
      "stroke-linejoin": "miter" }) + "/>";
  }
  function text(x, y, str, ink, size, ls, anchor) {
    return "<text" + attrs({ x: n2(x), y: n2(y), fill: ink, "font-family": FONT,
      "font-size": size, "letter-spacing": ls === undefined ? ".1em" : ls,
      "text-anchor": anchor || "middle" }) + ">" + esc(str) + "</text>";
  }

  /* ---- shape geometry ---- */
  function verts(shape, r, cx, cy) {
    var g = GEOM[shape], out = [], i, a;
    if (!g) return null;                                   /* circle has no vertices */
    for (i = 0; i < g.n; i++) {
      a = (g.a0 + i * 360 / g.n) * Math.PI / 180;
      out.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]);
    }
    return out;
  }
  /* every family draws as a PATH so one dash vocabulary serves all six (A4 sheet law) */
  function shapePath(shape, r, cx, cy) {
    var v, i, d;
    if (shape === "circle") {
      return "M " + n2(cx - r) + " " + n2(cy) +
             " A " + n2(r) + " " + n2(r) + " 0 1 0 " + n2(cx + r) + " " + n2(cy) +
             " A " + n2(r) + " " + n2(r) + " 0 1 0 " + n2(cx - r) + " " + n2(cy) + " Z";
    }
    v = verts(shape, r, cx, cy);
    d = "M " + n2(v[0][0]) + " " + n2(v[0][1]);
    for (i = 1; i < v.length; i++) d += " L " + n2(v[i][0]) + " " + n2(v[i][1]);
    return d + " Z";
  }
  function perimeter(shape, r) {
    var g = GEOM[shape];
    if (shape === "circle") return 2 * Math.PI * r;
    return g.n * 2 * r * Math.sin(Math.PI / g.n);
  }
  function arcPath(cx, cy, r, d0, d1) {
    var a0 = d0 * Math.PI / 180, a1 = d1 * Math.PI / 180;
    var big = Math.abs(d1 - d0) > 180 ? 1 : 0, sweep = d1 > d0 ? 1 : 0;
    return "M " + n2(cx + r * Math.cos(a0)) + " " + n2(cy + r * Math.sin(a0)) +
           " A " + n2(r) + " " + n2(r) + " 0 " + big + " " + sweep + " " +
           n2(cx + r * Math.cos(a1)) + " " + n2(cy + r * Math.sin(a1));
  }
  /* a micro family glyph — the only icon vocabulary that exists (A11 §3.3) */
  function mark(shape, x, y, r, ink, w, fill) {
    if (shape === "circle") return circ(x, y, r, ink, w, "", fill);
    return "<path" + attrs({ d: shapePath(shape, r, x, y), fill: fill || "none",
      stroke: ink, "stroke-width": w || 1 }) + "/>";
  }
  /* the sacred concentric field, faint, under every engraving (02 §4.1) */
  function ringField(cx, cy, r) {
    return circ(cx, cy, r * 0.92, S.a08, 1) +
           circ(cx, cy, r * 0.78, S.a14, 1, "1 5") +
           circ(cx, cy, r * 0.60, S.a08, 1) +
           circ(cx, cy, r * 0.30, S.a08, 1) +
           line(cx - r * 0.95, cy, cx - r * 0.66, cy, S.a14, 1) +
           line(cx + r * 0.66, cy, cx + r * 0.95, cy, S.a14, 1);
  }
  /* corner brackets — frames are four ticks, never a closed box (02 §5) */
  function brackets(x, y, w, h, len, ink) {
    var L = len || 12, k = ink || S.a28, o = "";
    o += path("M " + n2(x) + " " + n2(y + L) + " L " + n2(x) + " " + n2(y) + " L " + n2(x + L) + " " + n2(y), k, 1);
    o += path("M " + n2(x + w - L) + " " + n2(y) + " L " + n2(x + w) + " " + n2(y) + " L " + n2(x + w) + " " + n2(y + L), k, 1);
    o += path("M " + n2(x + w) + " " + n2(y + h - L) + " L " + n2(x + w) + " " + n2(y + h) + " L " + n2(x + w - L) + " " + n2(y + h), k, 1);
    o += path("M " + n2(x + L) + " " + n2(y + h) + " L " + n2(x) + " " + n2(y + h) + " L " + n2(x) + " " + n2(y + h - L), k, 1);
    return o;
  }
  /* the frame is also a mask: field and engraving are clipped to the rim so a seal never
     bleeds past its own shape (the triangle and diamond have far less inner area than
     their circumradius suggests — B3 keeps every mark inside the press) */
  function clipDefs(id, shape, r, cx, cy) {
    return '<defs><clipPath id="' + id + '"><path d="' + shapePath(shape, r, cx, cy) + '"/></clipPath></defs>';
  }
  function clipped(id, body) { return '<g clip-path="url(#' + id + ')">' + body + "</g>"; }

  function svg(w, h, body, cls) {
    return '<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h +
      '" viewBox="0 0 ' + w + " " + h + '"' + (cls ? ' class="' + cls + '"' : "") +
      ' shape-rendering="geometricPrecision">' + body + "</svg>";
  }

  /* ================= THE FRAME =================
     B1/B2/B3 construction, read at crop level: an outer rim, a heavier band inside it
     (the bevel that makes the seal read as pressed metal), a light inner rim, a vertex
     tick at every corner, and the concentric field beneath. Frames never close a box —
     the shape IS the frame, and the card around it uses brackets. */
  function frameBody(shape, r, cx, cy, opts) {
    var o = opts || {}, out = "", v, i, tick = Math.max(2, r * 0.045);
    out += path(shapePath(shape, r, cx, cy), S.a28, 1);                 /* outer rim  */
    out += path(shapePath(shape, r * 0.945, cx, cy), S.a45, 1.4);       /* the band   */
    out += path(shapePath(shape, r * 0.90, cx, cy), S.a14, 1);          /* band inner */
    out += path(shapePath(shape, r * 0.80, cx, cy), S.a28, 1);          /* inner rim  */
    if (shape === "circle") {
      /* a circle has no vertices: its ticks are eight radial notches on the band */
      for (i = 0; i < 8; i++) {
        var a = (i * 45) * Math.PI / 180;
        out += line(cx + Math.cos(a) * r * 0.90, cy + Math.sin(a) * r * 0.90,
                    cx + Math.cos(a) * r * 0.945, cy + Math.sin(a) * r * 0.945, S.a45, 1);
      }
    } else {
      v = verts(shape, r * 0.945, cx, cy);
      for (i = 0; i < v.length; i++) out += mark("square", v[i][0], v[i][1], tick, S.a45, 1);
    }
    if (o.accent) {                                   /* the ONE accent, when the caller owns it */
      out += path(shapePath(shape, r * 0.945, cx, cy), o.accent, 1.4);
    }
    return out;
  }

  /* ================= THE SIX ENGRAVINGS =================
     Every one is generated from the element's family and index. Vocabulary is closed:
     lines, arcs, concentric rings, and the six glyph shapes. No pictograms, ever.
     Each returns a string containing EXACTLY ONE mark in `ink` (the accent colour). */

  /* seeds — THE ORGAN. Ten organs must not press ten identical faces (B2 gives each seed its
     own mechanism), so the index selects one of three mechanisms and then varies inside it. */
  function engSeed(cx, cy, r, rnd, i, ink) {
    var out = "", k, a, x, y, sh, mech = i % 3;

    if (mech === 0) {                                     /* the rosette: a core and its limbs */
      var n = 5 + (i % 3), rr = r * 0.62, live = Math.floor(rnd() * n);
      out += circ(cx, cy, rr, S.a14, 1);
      out += path(arcPath(cx, cy, rr, -120 + i * 17, -20 + i * 17), S.a28, 1);
      for (k = 0; k < n; k++) {
        a = (-90 + k * 360 / n) * Math.PI / 180;
        x = cx + Math.cos(a) * rr; y = cy + Math.sin(a) * rr;
        sh = SHAPES[(i + k) % 6];
        out += line(cx + Math.cos(a) * r * 0.17, cy + Math.sin(a) * r * 0.17,
                    x - Math.cos(a) * r * 0.11, y - Math.sin(a) * r * 0.11,
                    k === live ? ink : S.a28, k === live ? 1.4 : 1, k === live ? "" : "3 3");
        out += mark(sh, x, y, r * 0.10, k === live ? ink : S.a45, 1);
        out += circ(x, y, r * 0.032, S.a28, 1);
      }
    } else if (mech === 1) {                              /* the ring stack: three shells, one swept */
      var shells = [0.76, 0.54, 0.32], liveS = Math.floor(rnd() * 3), m;
      for (k = 0; k < 3; k++) {
        var rs = r * shells[k], cnt = 3 + k;
        out += circ(cx, cy, rs, k === liveS ? S.a28 : S.a14, 1, k === 2 ? "" : "3 5");
        for (m = 0; m < cnt; m++) {
          a = (-90 + m * 360 / cnt + k * 24 + i * 9) * Math.PI / 180;
          out += mark(SHAPES[(i + k + m) % 6], cx + Math.cos(a) * rs, cy + Math.sin(a) * rs,
                      r * 0.075, S.a45, 1);
        }
      }
      /* the one accent: the shell actually swept, and the node it ends on */
      var a1 = -90 + i * 23, rl = r * shells[liveS];
      out += path(arcPath(cx, cy, rl, a1, a1 + 90 + (i % 3) * 30), ink, 1.5);
      var ae = (a1 + 90 + (i % 3) * 30) * Math.PI / 180;
      out += mark("circle", cx + Math.cos(ae) * rl, cy + Math.sin(ae) * rl, r * 0.06, ink, 1.4);
    } else {                                              /* the column: stations on a spine */
      var rows = 4, sx = cx - r * 0.10, liveR = Math.floor(rnd() * rows);
      out += circ(cx, cy, r * 0.74, S.a08, 1, "2 6");
      out += line(sx, cy - r * 0.58, sx, cy + r * 0.58, S.a28, 1);
      for (k = 0; k < rows; k++) {
        y = cy - r * 0.44 + k * (r * 0.88 / (rows - 1));
        out += line(sx, y, sx + r * 0.46, y, k === liveR ? ink : S.a28, k === liveR ? 1.4 : 1,
                    k === liveR ? "" : "3 4");
        out += mark(SHAPES[(i + k) % 6], sx + r * 0.52, y, r * 0.075, k === liveR ? ink : S.a45, 1);
        out += line(sx - r * 0.30, y, sx - r * 0.06, y, S.a14, 1);
        out += circ(sx - r * 0.36, y, r * 0.035, S.a28, 1);
      }
    }
    out += circ(cx, cy, r * 0.15, S.a70, 1.2);            /* the core: ring in ring, always */
    out += circ(cx, cy, r * 0.08, S.a45, 1);
    return out;
  }

  /* axes — THE BRANCH: a base node, a trunk to the apex, branch pairs to satellites.
     The accent is the through-path: one continuous polyline, base to apex (B1, AX-P). */
  function engAxis(cx, cy, r, rnd, i, ink) {
    var out = "", base = cy + r * 0.76, top = cy - r * 0.86, k;
    var tiers = 2 + (i % 3);                     /* 2-4 branch tiers — the index varies the tree */
    var side = rnd() < 0.5 ? -1 : 1;
    out += circ(cx, cy, r * 0.72, S.a08, 1);
    out += path(arcPath(cx, cy, r * 0.72, 158, 22), S.a14, 1, "2 5");
    out += path(arcPath(cx, cy, r * 0.44, 200, 340), S.a08, 1);
    for (k = 0; k < tiers; k++) {
      var yy = base - (k + 1) * (base - top) / (tiers + 1.15);
      var sp = r * (0.66 - k * (0.30 / tiers));  /* the pentagon narrows upward — so do the limbs */
      var sh = SHAPES[(i + k) % 6];
      var kd, m;
      for (m = -1; m <= 1; m += 2) {
        kd = "M " + n2(cx) + " " + n2(yy + r * 0.16) + " C " + n2(cx) + " " + n2(yy + r * 0.02) +
             " " + n2(cx + m * sp * 0.55) + " " + n2(yy) + " " + n2(cx + m * sp) + " " + n2(yy - r * 0.09);
        out += path(kd, S.a28, 1);
        out += mark(sh, cx + m * sp, yy - r * 0.13, r * 0.085, S.a45, 1);
        out += circ(cx + m * sp, yy - r * 0.13, r * 0.03, S.a28, 1);
        out += line(cx + m * sp, yy - r * 0.22, cx + m * sp, yy - r * 0.30, S.a14, 1);
      }
    }
    /* the accent: base -> one jog -> apex cap. One continuous path, one mark. */
    var jx = cx + side * r * (0.20 + (i % 3) * 0.08), my = cy - r * 0.04;
    out += path("M " + n2(cx) + " " + n2(base - r * 0.18) +
                " L " + n2(cx) + " " + n2(my + r * 0.26) +
                " L " + n2(jx) + " " + n2(my + r * 0.26) +
                " L " + n2(jx) + " " + n2(my - r * 0.16) +
                " L " + n2(cx) + " " + n2(my - r * 0.16) +
                " L " + n2(cx) + " " + n2(top + r * 0.14), ink, 1.6);
    out += mark("pentagon", cx, top, r * 0.10, S.a70, 1);
    out += circ(cx, base, r * 0.16, S.a70, 1.2);
    out += circ(cx, base, r * 0.085, S.a45, 1);
    return out;
  }

  /* principles — THE MESH: nodes on two rings, chords between them, one live node (B1 PR-E) */
  function engPrinciple(cx, cy, r, rnd, i, ink) {
    var out = "", outer = 8, inner = 3, ro = r * 0.60, ri = r * 0.26, pts = [], k, a;
    for (k = 0; k < outer; k++) {
      a = (-90 + k * 360 / outer + (i % 3) * 7) * Math.PI / 180;
      pts.push([cx + Math.cos(a) * ro, cy + Math.sin(a) * ro]);
    }
    for (k = 0; k < inner; k++) {
      a = (-90 + k * 360 / inner + i * 11) * Math.PI / 180;
      pts.push([cx + Math.cos(a) * ri, cy + Math.sin(a) * ri]);
    }
    out += circ(cx, cy, ro, S.a14, 1, "2 6");
    out += circ(cx, cy, ri, S.a08, 1);
    var step = 2 + (i % 3);
    for (k = 0; k < outer; k++) {
      var b = pts[(k + step) % outer];
      out += line(pts[k][0], pts[k][1], b[0], b[1], S.a14, 1);
      var c = pts[outer + (k % inner)];
      out += line(pts[k][0], pts[k][1], c[0], c[1], S.a08, 1);
    }
    for (k = 0; k < pts.length; k++) {
      out += mark("circle", pts[k][0], pts[k][1], k < outer ? r * 0.055 : r * 0.045, S.a45, 1);
    }
    var live = Math.floor(rnd() * outer);
    out += line(pts[live][0], pts[live][1], pts[(live + step) % outer][0], pts[(live + step) % outer][1], S.a28, 1);
    out += mark("hexagon", pts[live][0], pts[live][1], r * 0.10, ink, 1.4);   /* the one accent */
    out += circ(cx, cy, r * 0.09, S.a70, 1.2);
    return out;
  }

  /* verbs — THE RELAY: corner nodes, a dashed route between them, one arrival (B3 VB-02) */
  function engVerb(cx, cy, r, rnd, i, ink) {
    var out = "", v = verts("triangle", r * 0.60, cx, cy + r * 0.14), k;
    var arrive = Math.floor(rnd() * 3);
    out += path(arcPath(cx, cy + r * 0.14, r * 0.62, 200 + i * 9, 340 + i * 9), S.a08, 1);
    out += circ(cx, cy + r * 0.14, r * 0.34, S.a08, 1);
    for (k = 0; k < 3; k++) {
      var a = v[k], b = v[(k + 1) % 3];
      out += line(a[0], a[1], b[0], b[1], S.a28, 1, k === arrive ? "" : "5 4");
      out += line((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, cx, cy + r * 0.14, S.a08, 1);
      out += mark(SHAPES[(i + k) % 6], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, r * 0.075, S.a45, 1);
    }
    for (k = 0; k < 3; k++) {
      out += mark("circle", v[k][0], v[k][1], r * 0.105, k === arrive ? S.a70 : S.a45, 1);
      out += circ(v[k][0], v[k][1], r * 0.045, S.a28, 1);
    }
    /* the one accent: the arrival ring */
    out += circ(v[arrive][0], v[arrive][1], r * 0.155, ink, 1.5);
    return out;
  }

  /* mechanics — THE LATTICE: a bracketed field, dashed lanes with end nodes, one live lane
     (B3 MC-04 — rows of stations with a single amber column) */
  function engMechanic(cx, cy, r, rnd, i, ink) {
    var out = "", w = r * 0.62, rows = 4 + (i % 2), k;
    var live = Math.floor(rnd() * rows);
    /* arms stay short: four ticks, never a rectangle (02 §5) */
    out += brackets(cx - w, cy - w, w * 2, w * 2, w * 0.20, S.a14);
    out += circ(cx, cy, w * 0.86, S.a08, 1);
    out += circ(cx, cy, w * 0.50, S.a08, 1);
    for (k = 0; k < rows; k++) {
      var y = cy - w * 0.66 + k * (w * 1.32 / (rows - 1));
      out += line(cx - w * 0.78, y, cx + w * 0.78, y, S.a14, 1, "4 4");
      out += mark("circle", cx - w * 0.78, y, r * 0.065, k === live ? S.a70 : S.a45, 1);
      out += mark(SHAPES[(i + k) % 6], cx + w * 0.78, y, r * 0.065, S.a45, 1);
      if (k === live) out += line(cx - w * 0.78, y, cx + w * 0.30, y, S.a70, 1.2);
    }
    /* the ruler: dense terminal texture, evidence not ornament (02 §4.4) */
    for (k = 0; k < 13; k++) {
      var rx = cx - w * 0.62 + k * (w * 1.24 / 12);
      out += line(rx, cy + w * 0.90, rx, cy + w * (k % 4 === 0 ? 0.76 : 0.83), S.a28, 1);
    }
    out += line(cx - w * 0.62, cy + w * 0.90, cx + w * 0.62, cy + w * 0.90, S.a14, 1);
    /* the one accent: the spine column that feeds the lattice */
    out += path("M " + n2(cx + w * 0.30) + " " + n2(cy + w * 0.72) +
                " L " + n2(cx + w * 0.30) + " " + n2(cy - w * 0.72), ink, 1.5);
    out += mark("square", cx + w * 0.30, cy - w * 0.86, r * 0.07, S.a70, 1);
    return out;
  }

  /* ops — THE DIAL: a ticked ring, a pointer, one measured arc (B3 OP-02) */
  function engOp(cx, cy, r, rnd, i, ink) {
    var out = "", rr = r * 0.52, k, a;
    var span = 40 + Math.floor(rnd() * 5) * 30, start = -90 + (i % 4) * 45;
    out += circ(cx, cy, rr, S.a28, 1);
    out += circ(cx, cy, rr * 0.78, S.a08, 1);
    for (k = 0; k < 24; k++) {
      a = k * 15 * Math.PI / 180;
      var long = (k % 6 === 0) ? 0.12 : 0.06;
      out += line(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr,
                  cx + Math.cos(a) * rr * (1 - long), cy + Math.sin(a) * rr * (1 - long),
                  (k % 6 === 0) ? S.a45 : S.a14, 1);
    }
    for (k = 0; k < 4; k++) {
      a = (-90 + k * 90) * Math.PI / 180;
      out += mark(SHAPES[(i + k) % 6], cx + Math.cos(a) * r * 0.74, cy + Math.sin(a) * r * 0.74, r * 0.06, S.a28, 1);
    }
    var pa = (start + span) * Math.PI / 180;
    out += line(cx, cy, cx + Math.cos(pa) * rr * 0.74, cy + Math.sin(pa) * rr * 0.74, S.a70, 1.2);
    out += line(cx, cy, cx + Math.cos((start - 90) * Math.PI / 180) * rr * 0.46,
                cy + Math.sin((start - 90) * Math.PI / 180) * rr * 0.46, S.a45, 1);
    /* the one accent: the arc actually swept */
    out += path(arcPath(cx, cy, rr * 0.90, start, start + span), ink, 1.6);
    out += circ(cx, cy, r * 0.075, S.a70, 1.2);
    out += circ(cx, cy, r * 0.03, S.a45, 1);
    return out;
  }

  var ENGRAVE = {
    seeds: engSeed, axes: engAxis, principles: engPrinciple,
    verbs: engVerb, mechanics: engMechanic, ops: engOp
  };

  /* ================= THE INDEX (read from window.AEA — never copied here) ================= */

  /* atlas codes as the sheets press them: AX-P · SD-01 · VB-01 · MC-01 · OP-01 · PR-E */
  function codeOf(family, id, n) {
    var tail = id.split(".")[1] || "";
    if (family === "axes") return "AX-" + tail.toUpperCase().charAt(0);
    if (family === "principles") return "PR-" + tail.toUpperCase().charAt(0);
    if (family === "seeds") return "SD-" + (n < 10 ? "0" : "") + n;
    if (family === "verbs") return "VB-" + (n < 10 ? "0" : "") + n;
    if (family === "mechanics") return "MC-" + (n < 10 ? "0" : "") + n;
    return "OP-" + (n < 10 ? "0" : "") + n;
  }

  function buildIndex() {
    var A = window.AEA, map = {}, count = {}, i, e, fam, rec, seedOf = {};
    if (!A || !A.elements) throw new Error("window.AEA missing — load /aea_elements.js first");
    for (i = 0; i < A.elements.length; i++) {
      e = A.elements[i];
      fam = e.ring;                                       /* axes|seeds|verbs|ops|principles */
      count[fam] = (count[fam] || 0) + 1;
      rec = { id: e.id, name: e.name, line: e.line, proof: e.proof, family: fam,
              shape: SHAPE_OF[fam], n: count[fam], code: codeOf(fam, e.id, count[fam]) };
      map[e.id] = rec;
      seedOf[e.id] = rec;
    }
    /* mechanics are their own nodes on ring 3 and mirror a seed — their proof IS the
       seed's proof (aea_elements.js §mechanics). Read, never restated. */
    for (i = 0; i < (A.mechanics || []).length; i++) {
      var m = A.mechanics[i], src = seedOf[m.seed] || {};
      count.mechanics = (count.mechanics || 0) + 1;
      map[m.id] = { id: m.id, name: m.name, line: src.line || "", proof: src.proof || "",
                    family: "mechanics", shape: "square", n: count.mechanics,
                    code: codeOf("mechanics", m.id, count.mechanics), mirrors: m.seed };
    }
    return map;
  }
  function resolve(el) {
    var idx = IDX || (IDX = buildIndex());
    if (!el) return null;
    if (typeof el === "string") return idx[el] || null;
    if (el.id && idx[el.id]) return idx[el.id];
    return el.name ? el : null;                            /* caller-supplied record */
  }

  /* wrap a real string into <=maxLines lines of <=cols chars. Truncation is marked, never
     silent — a clipped proof that looked complete would be a small lie. */
  function wrap(str, cols, maxLines) {
    var words = String(str).split(/\s+/), lines = [], cur = "", i;
    for (i = 0; i < words.length; i++) {
      var w = words[i];
      if (!cur.length) { cur = w; }
      else if ((cur + " " + w).length <= cols) { cur += " " + w; }
      else { lines.push(cur); cur = w; if (lines.length === maxLines) break; }
    }
    if (cur.length && lines.length < maxLines) lines.push(cur);
    if (lines.length === maxLines && i < words.length - 1) {
      var last = lines[maxLines - 1];
      lines[maxLines - 1] = (last.length > cols - 3 ? last.slice(0, cols - 3) : last) + "...";
    }
    return lines;
  }

  /* ================= PUBLIC ================= */

  /* SEALS.frame(shape, size) -> the family frame, standalone.
     opts: {accent:"hot"|"warm"|false} — the frame's optional single accent ring. */
  function frame(shape, size, opts) {
    var o = opts || {}, sz = size || 160, r = sz * 0.44, c = sz / 2;
    if (SHAPE_OF[shape]) shape = SHAPE_OF[shape];        /* a family name is accepted too */
    if (shape !== "circle" && !GEOM[shape]) throw new Error("SEALS.frame: unknown shape " + shape);
    var acc = o.accent === "hot" ? HOT : (o.accent === "warm" ? WARM : null);
    var cid = "sealclip-frame-" + shape;
    return svg(sz, sz, clipDefs(cid, shape, r * 0.98, c, c) +
      clipped(cid, ringField(c, c, r * 0.86)) +
      frameBody(shape, r, c, c, { accent: acc }), "seal-frame");
  }

  /* SEALS.state(shape, state) -> the map glyph in hidden|sensed|known (sheet A4).
     hidden = dotted, no signal · sensed = broken arcs, weak return · known = solid
     concentric + amber, locked and indexed. Amber exists ONLY in the known state. */
  function stateGlyph(shape, state, size, opts) {
    var o = opts || {}, sz = size || 34, c = sz / 2, r = sz * 0.40, out = "";
    if (SHAPE_OF[shape]) shape = SHAPE_OF[shape];
    if (shape !== "circle" && !GEOM[shape]) throw new Error("SEALS.state: unknown shape " + shape);
    if (STATES.indexOf(state) < 0) throw new Error("SEALS.state: unknown state " + state);
    var per = perimeter(shape, r), seg;
    if (state === "hidden") {
      seg = per / 34;
      out += path(shapePath(shape, r, c, c), S.a28, 1, n2(seg * 0.22) + " " + n2(seg * 0.78), "round");
    } else if (state === "sensed") {
      seg = per / 10;
      out += path(shapePath(shape, r, c, c), S.a45, 1.2, n2(seg * 0.58) + " " + n2(seg * 0.42));
      out += circ(c, c, Math.max(1, r * 0.07), S.a28, 1);
    } else {
      var hot = o.live ? HOT : WARM;
      out += path(shapePath(shape, r, c, c), hot, 1.2);              /* the earned rim */
      out += path(shapePath(shape, r * 0.74, c, c), S.a70, 1);
      out += path(shapePath(shape, r * 0.46, c, c), hot, 1);
      var i, a;                                                      /* index ticks on the rim */
      for (i = 0; i < 8; i++) {
        a = i * 45 * Math.PI / 180;
        out += line(c + Math.cos(a) * r * 0.80, c + Math.sin(a) * r * 0.80,
                    c + Math.cos(a) * r * 0.90, c + Math.sin(a) * r * 0.90, S.a45, 1);
      }
      out += circ(c, c, Math.max(1.2, r * 0.11), hot, 1);
    }
    return svg(sz, sz, out, "seal-glyph seal-" + state);
  }

  /* SEALS.seal(element) -> the full seal: frame + generated engraving + caption + proof line.
     element = an AEA id ("seed.1", "mech.ceiling", "axis.P") or an element record.
     opts: {size, state:"hidden"|"sensed"|"known" (default known), live:false, readout}
       - state hidden  -> no engraving, no name, NO SIGNAL. Nothing is claimed.
       - state sensed  -> name shown, proof block is dashes: sensed is not earned.
       - readout: a string is printed verbatim; null prints DASH; omitted prints no row. */
  function seal(element, opts) {
    var o = opts || {}, rec = resolve(element);
    if (!rec) throw new Error("SEALS.seal: no such element " + element);
    var st = o.state || "known";
    if (STATES.indexOf(st) < 0) throw new Error("SEALS.seal: unknown state " + st);

    var hasRead = o.readout !== undefined;                      /* the row buys its own height */
    var sz = o.size || 260, W = sz, H = Math.round(sz * 1.34) + (hasRead ? 14 : 0);
    var cx = W / 2, cy = sz * 0.42, r = sz * 0.33;
    var ink = st === "known" ? (o.live ? HOT : WARM) : S.a70;   /* the ONE accent, cold unless known */
    var rnd = rng(hash(rec.id));
    var out = "";

    var cid = "sealclip-" + rec.id.replace(/[^a-zA-Z0-9]/g, "-");
    var inner = ringField(cx, cy, r * 0.86);
    if (st === "hidden") {
      /* an unknown element engraves nothing — the frame is the only honest mark */
      inner += path(shapePath(rec.shape, r * 0.62, cx, cy), S.a14, 1, "1 5", "round");
    } else {
      inner += ENGRAVE[rec.family](cx, cy, r * 0.78, rnd, rec.n, ink);
    }
    out += brackets(6, 6, W - 12, H - 12, 14, S.a28);
    out += clipDefs(cid, rec.shape, r * 0.98, cx, cy) + clipped(cid, inner);
    out += frameBody(rec.shape, r, cx, cy, null);

    /* ---- caption block (B1: index/code, NAME, proof line) ---- */
    var yb = sz * 0.84;
    var nm = st === "hidden" ? "—" : rec.name;
    var fs = nm.length > 26 ? 8 : (nm.length > 18 ? 9 : 11);
    out += text(cx, yb, (rec.n < 10 ? "0" : "") + rec.n + "  " + rec.code, S.a45, 9, ".16em");
    out += text(cx, yb + 18, nm, S.a70, fs, ".12em");

    /* B1's caption pressed the file on its own line ("proof swarm.py") and the evidence
       under it — the proof string's own "·" is that break, so it is honored before wrapping */
    var proofLines, cut = rec.proof ? rec.proof.indexOf("·") : -1;
    if (st === "known" && cut > 0) {
      proofLines = ["proof " + rec.proof.slice(0, cut).replace(/\s+$/, ""),
                    wrap(rec.proof.slice(cut + 1).replace(/^\s+/, ""), 34, 1)[0] || ""];
    } else if (st === "known") proofLines = wrap("proof " + rec.proof, 34, 2);
    else if (st === "sensed") proofLines = [DASH, ""];
    else proofLines = ["NO SIGNAL", ""];
    out += text(cx, yb + 34, proofLines[0] || "", S.a45, 8.5, ".06em");
    out += text(cx, yb + 45, proofLines[1] || "", S.a28, 8.5, ".06em");

    out += line(W * 0.24, yb + 56, W * 0.76, yb + 56, S.a14, 1);
    if (hasRead) {
      /* honesty law: a slot with no live source prints dashes, never a plausible number */
      out += text(cx, yb + 68, o.readout === null ? DASH + "s" : String(o.readout), S.a45, 8.5, ".1em");
    }
    out += text(cx, yb + (hasRead ? 82 : 68), rec.family.toUpperCase() + "  ·  " + st.toUpperCase(), S.a28, 8, ".18em");
    /* the family glyph, micro, at the foot — the same six-word language everywhere */
    out += mark(rec.shape, cx, H - 20, 6, S.a45, 1);
    return svg(W, H, out, "seal seal-" + rec.family + " seal-" + st);
  }

  /* SEALS.dom(...) — the same seals as live SVG nodes, for callers that need DOM */
  function dom(svgStr) {
    var host = document.createElement("div");
    host.innerHTML = svgStr;
    return host.firstChild;
  }

  function list(family) {
    var idx = IDX || (IDX = buildIndex()), k, out = [];
    for (k in idx) if (idx.hasOwnProperty(k) && (!family || idx[k].family === family)) out.push(idx[k]);
    out.sort(function (a, b) {
      var fa = SHAPES.indexOf(a.shape), fb = SHAPES.indexOf(b.shape);
      return fa === fb ? a.n - b.n : fa - fb;
    });
    return out;
  }

  function init(game) {
    try {
      GAME = game || null;
      IDX = buildIndex();
      /* aliasing, never relocation (E1 §2.2): other surfaces reach the press through GAME */
      if (GAME && GAME.state) GAME.state.seals = api;
    } catch (err) {
      var e = document.getElementById("err");            /* init failure reaches #err (E1 §5) */
      if (e) { e.textContent = "ERR SEALS INIT " + (err && err.message); e.style.display = "block"; }
      throw err;
    }
  }

  function dispose() {
    /* no listeners, no timers, no fetches, no GPU resources are ever taken here —
       the index and the GAME ref are the whole of this module's ownership (E1 §3.1) */
    if (GAME && GAME.state && GAME.state.seals === api) GAME.state.seals = null;
    IDX = null; GAME = null;
  }

  var api = {
    init: init, dispose: dispose,
    frame: frame, state: stateGlyph, seal: seal, dom: dom,
    list: list, of: resolve,
    SHAPES: SHAPES, STATES: STATES, SHAPE_OF: SHAPE_OF, DASH: DASH
  };
  return api;
})();
