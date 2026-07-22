/* panels.js — THE INSTRUMENT PANELS: IP-01..IP-08 as real, reusable UI components.
   Governance: E4_UX_P0.md (this is the bench's shipping UI vocabulary, not a demo) ·
   design/bundle_02/02_VISUAL_LAW.md (two inks; structure rgba(120,155,175,x) at the five
   sanctioned stops; amber ONLY where something is alive, working or earned; corner brackets
   never closed boxes; the six glyphs are the only icons; flat and matte) ·
   04_UI_BIBLE.md §0 (type law — three DOM sizes; truth law) · A11_SIGNATURE.md §3.1 (any
   circle sharing a centre CITES the AEA field: every concentric set below is built on the
   map's own r70/r150/r250/r360/r470 ratios — RING_R — so no ring here is decorative) ·
   §3.3 (six glyphs, zero icons) · E1_CODE_ARCHITECTURE.md §2.2 (init(GAME)/dispose(); no
   cross-module globals beyond the GAME contract), §3.1.3/.4 (dispose nulls refs AND removes
   the DOM — a node without an owner is a detached-DOM leak), §5 (comment law: constraints only).
   Reference sheet: design/concepts/C4_instrument_panels_v2.png (primary — bracket frames,
   callout leaders, plate windows, the amber discipline) · A6_instrument_panels.png (variant).

   THE HONESTY LAW, as a contract: every factory is make(data) with data OPTIONAL. Any value
   with no live source renders as DASHES in structure ink (never amber, never display weight).
   A panel may never print an invented number that looks measured. Absence is a state with its
   own rendering, distinguishable from a real reading of zero (see LADDER, ip07).

   AMBER RULINGS taken here, each argued (the sheet is the target; the law is the judge):
   - IP-01  cycles + checksum are MEASURED, earned numbers -> warm. The execution mark runs
            hot only while data.firing is true. The reticle is never amber.
   - IP-02  a row is warm only when data says that entry is live. Default: the whole strip cold.
   - IP-03  the sector index needle is the live pointer -> hot when a real sector exists, and
            absent entirely when there is none (no needle is honest; a parked needle is a lie).
            The ZONE caption stays structure: a 10px label is a label (type law), not a state.
   - IP-04  valid-until is the earned fact -> warm. The hash and the emblem are cold.
   - IP-05  the loss timestamp is the one measured fact of a failure -> warm, never hot:
            nothing is working. Code and hexagon are cold (failure is amber WITHDRAWN, E4 §9).
   - IP-06  the FAIL row only, exactly as the sheet prints it. HOLD is suspended, not working,
            so under the two-tier law it stays structure ink.
   - IP-07  lit ladder segments are real signal -> warm; hot only while data.live is true.
   - IP-08  no amber at all. A route card is a plan, not a run; nothing on it is firing.

   Stack: vanilla ES5-safe, no frameworks, no build step, divs + SVG only (no canvas, no images). */
window.PANELS = (function () {
  "use strict";

  var GAME = null;
  var SVGNS = "http://www.w3.org/2000/svg";

  /* live panel registry — dispose() must be able to reach every node it ever produced
     (E1 §3.1.4: a node whose owner forgot it is a detached-DOM leak) */
  var LIVE = [];

  /* ---- the honesty law's vocabulary: dash shapes per field type ---- */
  var DASH = {
    id: "———————",
    n6: "——————",
    n4: "————",
    n2: "——",
    word: "————",
    hash: "————-————",
    date: "——.——.——",
    clock: "——:——:——",
    secs: "—.——s",
    pct: "——%",
    glyph: "—"
  };

  /* the AEA map's own radii (04 §3 / A11 §3.1) — every concentric set is a citation of these
     ratios, which is what makes a ring in this game legal at all */
  var RING_R = [70, 150, 250, 360, 470];
  function ratio(i) { return RING_R[i] / RING_R[RING_R.length - 1]; }

  /* ---- tiny DOM/SVG helpers (house voice: verb-first, terse, no generic utils names) ---- */
  function add(parent, tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    parent.appendChild(n);
    return n;
  }
  function svg(tag, attrs) {
    var n = document.createElementNS(SVGNS, tag);
    for (var k in attrs) { if (attrs.hasOwnProperty(k)) n.setAttribute(k, attrs[k]); }
    return n;
  }
  function svgRoot(w, h, cls) {
    var s = svg("svg", { width: w, height: h, viewBox: "0 0 " + w + " " + h });
    if (cls) s.setAttribute("class", cls);
    s.setAttribute("shape-rendering", "geometricPrecision");
    return s;
  }

  /* pad(): slot engravings. A strip's 001..008 and a register's 01..08 are the PANEL'S OWN
     hardware numbering, not a measurement — they print always, and never as dashes. Only the
     entry sitting in the slot is data. */
  function pad(n, w) { var s = String(n); while (s.length < w) s = "0" + s; return s; }

  /* put(): the single honesty gate. Every printed value in this module passes through here.
     A "value" made only of punctuation — "—", "——:——", "-" — is a caller's own placeholder,
     NOT a measurement, and must not be allowed to wear the live ink. Caught here so no
     factory has to remember it. */
  var HAS_CHAR = /[0-9A-Za-z]/;
  function put(node, v, dash) {
    var has = !(v === undefined || v === null || v === "") && HAS_CHAR.test(String(v));
    node.textContent = has ? String(v) : (dash || DASH.word);
    if (has) node.classList.remove("ip-void"); else node.classList.add("ip-void");
    return has;
  }

  /* ---- the six glyphs. There is no seventh, ever (A11 §3.3). ---- */
  var GLYPH = {
    circle: function () { return svg("circle", { cx: 5, cy: 5, r: 4, "class": "gs" }); },
    square: function () { return svg("rect", { x: 1.2, y: 1.2, width: 7.6, height: 7.6, "class": "gs" }); },
    triangle: function () { return svg("polygon", { points: "5,1 9.2,8.7 0.8,8.7", "class": "gs" }); },
    diamond: function () { return svg("polygon", { points: "5,0.8 9.2,5 5,9.2 0.8,5", "class": "gs" }); },
    pentagon: function () { return svg("polygon", { points: "5,0.7 9.3,3.9 7.65,9.2 2.35,9.2 0.7,3.9", "class": "gs" }); },
    hexagon: function () { return svg("polygon", { points: "5,0.6 9.3,3.2 9.3,6.8 5,9.4 0.7,6.8 0.7,3.2", "class": "gs" }); }
  };
  function glyph(name, size, cls) {
    var s = svgRoot(size, size, "ip-g" + (cls ? " " + cls : ""));
    s.setAttribute("viewBox", "0 0 10 10");
    if (GLYPH[name]) s.appendChild(GLYPH[name]());
    return s;
  }

  /* ---- the chamfered plate shell: corner-cut outline + inner frame + edge notches ---- */
  function chamPath(x, y, w, h, c) {
    return "M" + (x + c) + "," + y + " H" + (x + w - c) + " L" + (x + w) + "," + (y + c) +
      " V" + (y + h - c) + " L" + (x + w - c) + "," + (y + h) + " H" + (x + c) +
      " L" + x + "," + (y + h - c) + " V" + (y + c) + " Z";
  }
  function shell(w, h, opts) {
    opts = opts || {};
    var s = svgRoot(w, h, "ip-shell");
    s.appendChild(svg("path", { d: chamPath(0.5, 0.5, w - 1, h - 1, 10), "class": "sk" }));
    s.appendChild(svg("path", { d: chamPath(4.5, 4.5, w - 9, h - 9, 7), "class": "sk-in" }));
    /* edge notches — the plate's mount slots; two per side, top and bottom slots on the caps */
    var ys = [52, h - 78];
    for (var i = 0; i < ys.length; i++) {
      s.appendChild(svg("rect", { x: 1.5, y: ys[i], width: 3, height: 26, "class": "sk-notch" }));
      s.appendChild(svg("rect", { x: w - 4.5, y: ys[i], width: 3, height: 26, "class": "sk-notch" }));
    }
    s.appendChild(svg("rect", { x: w / 2 - 22, y: 1.5, width: 44, height: 3, "class": "sk-notch" }));
    s.appendChild(svg("rect", { x: w / 2 - 22, y: h - 4.5, width: 44, height: 3, "class": "sk-notch" }));
    if (opts.bolts) {
      var bx = [14, w - 14], by = [15, h - 15];
      for (var a = 0; a < 2; a++) {
        for (var b = 0; b < 2; b++) {
          s.appendChild(svg("circle", { cx: bx[a], cy: by[b], r: 4, "class": "sk-bolt" }));
          s.appendChild(svg("circle", { cx: bx[a], cy: by[b], r: 1.4, "class": "sk-bolt" }));
        }
      }
    }
    if (opts.port) {
      s.appendChild(svg("circle", { cx: w / 2, cy: h - 1, r: 5, "class": "sk-notch" }));
      s.appendChild(svg("circle", { cx: w / 2, cy: h - 1, r: 2, "class": "sk-notch" }));
    }
    return s;
  }

  /* ---- concentric reticle / seal emblem: rings on the AEA ratios + a crosshair ---- */
  function reticle(size, opts) {
    opts = opts || {};
    var c = size / 2, R = size / 2 - 1;
    var s = svgRoot(size, size, "ip-rings");
    s.appendChild(svg("circle", { cx: c, cy: c, r: R * ratio(4), "class": "r1" }));
    s.appendChild(svg("circle", { cx: c, cy: c, r: R * ratio(3), "class": "r2" }));
    s.appendChild(svg("circle", { cx: c, cy: c, r: R * ratio(2), "class": "r1" }));
    s.appendChild(svg("circle", { cx: c, cy: c, r: R * ratio(1), "class": "r2" }));
    s.appendChild(svg("circle", { cx: c, cy: c, r: R * ratio(0), "class": "r1" }));
    var ext = opts.ext === undefined ? 8 : opts.ext;
    s.appendChild(svg("line", { x1: c - R - ext, y1: c, x2: c + R + ext, y2: c, "class": "cross dash" }));
    s.appendChild(svg("line", { x1: c, y1: c - R - ext, x2: c, y2: c + R + ext, "class": "cross dash" }));
    /* two short arc ticks — the reticle's read marks, short arcs ON the widest ring
       (sweep flag 1: the minor arc; flag 0 takes the long way round and swallows the ring) */
    s.appendChild(svg("path", {
      d: "M" + (c - R * 0.79) + "," + (c + R * 0.62) + " A" + R + "," + R + " 0 0 1 " + (c - R * 0.99) + "," + (c + R * 0.1),
      "class": "tick"
    }));
    s.appendChild(svg("path", {
      d: "M" + (c + R * 0.79) + "," + (c - R * 0.62) + " A" + R + "," + R + " 0 0 1 " + (c + R * 0.99) + "," + (c - R * 0.1),
      "class": "tick"
    }));
    return s;
  }

  /* ---- the cell: corner brackets, four callouts with leaders, and the plate body ---- */
  /* cell 320x310 · plate body x94..226 y34..262 · dial centre (160,148) r92 */
  var LEAD = {
    plate: [
      "M92,16 H108 L124,34", "M228,16 H212 L196,34",
      "M102,258 L88,270", "M218,258 L232,270"
    ],
    dial: [
      "M92,16 H108 L126,68", "M228,16 H212 L194,68",
      "M126,228 L88,270", "M194,228 L232,270"
    ],
    dots: { plate: [[102, 258], [218, 258]], dial: [[126, 228], [194, 228]] }
  };

  function cell(code, name, calls, opts) {
    opts = opts || {};
    var root = document.createElement("div");
    root.className = "ip";
    root.setAttribute("data-ip", code);
    var c = add(root, "div", "ip-cell");

    var corners = ["tl", "tr", "bl", "br"];
    for (var i = 0; i < 4; i++) add(c, "i", "ip-ck " + corners[i]);

    /* leaders first so labels and the plate paint over their tails */
    var leads = svgRoot(320, 310, "ip-leads");
    var kind = opts.leads || "plate";
    for (var l = 0; l < 4; l++) leads.appendChild(svg("path", { d: LEAD[kind][l] }));
    var dots = LEAD.dots[kind];
    for (var dI = 0; dI < dots.length; dI++) {
      leads.appendChild(svg("circle", { cx: dots[dI][0], cy: dots[dI][1], r: 2.2 }));
    }
    c.appendChild(leads);

    for (var k = 0; k < 4; k++) {
      var box = add(c, "div", "ip-call " + corners[k]);
      var lines = String(calls[k] || "").split("\n");
      for (var m = 0; m < lines.length; m++) add(box, "div", null, lines[m]);
    }

    var inn = null, body = null;
    if (kind === "plate") {
      body = add(c, "div", "ip-body");
      body.appendChild(shell(132, 228, opts.shell));
      inn = add(body, "div", "ip-in");
    }

    var cap = add(root, "div", "ip-cap");
    var idx = add(cap, "span", "ip-idx", "");
    add(cap, "span", "ip-code", code);
    add(cap, "span", "ip-slash", "/");
    add(cap, "span", "ip-name", name);

    root.code = code;
    root.panelName = name;
    root.setIndex = function (n) { idx.textContent = (n === undefined || n === null) ? "" : (n + ". "); };
    return { root: root, cellEl: c, body: body, inn: inn };
  }

  function win(parent, cls) { return add(parent, "div", "ip-win" + (cls ? " " + cls : "")); }

  /* register(): the ONLY way a panel leaves this module — nothing escapes the registry */
  function register(root, paint, data) {
    root.update = function (d) { paint(d || {}); return root; };
    LIVE.push(root);
    paint(data || {});
    return root;
  }

  /* ================= IP-01 RUN PLATE ================= */
  /* data: { id, cycles, cksm, firing } */
  function ip01(data) {
    var c = cell("IP-01", "RUN PLATE",
      ["RUN ID\nPLATE", "EXECUTION\nMARK", "CYCLE COUNT\nWINDOW", "CHECKSUM\nSEAL"]);

    var w1 = win(c.inn, "rel");
    add(w1, "div", "ip-lb", "RUN-ID");
    var idV = add(w1, "div", "ip-v");
    var mark = glyph("diamond", 13, "dim");
    mark.classList.add("ip-mark"); mark.classList.add("top");
    w1.appendChild(mark);

    var face = add(c.inn, "div", "ip-face");
    face.appendChild(reticle(78));

    var w2 = win(c.inn);
    add(w2, "div", "ip-lb", "CYCLES");
    var cyV = add(w2, "div", "ip-v num");

    var w3 = win(c.inn, "rel");
    add(w3, "div", "ip-lb", "CKSM");
    var ckV = add(w3, "div", "ip-v num");
    var seal = glyph("circle", 13, "dim");
    seal.classList.add("ip-mark");
    w3.appendChild(seal);

    function paint(d) {
      put(idV, d.id, DASH.id);
      put(cyV, d.cycles, DASH.n6);
      put(ckV, d.cksm, DASH.n4);
      /* the execution mark is the plate's one live tell — hot only while a run is actually out */
      mark.setAttribute("class", "ip-g ip-mark top " + (d.firing ? "hot" : "dim"));
    }
    return register(c.root, paint, data);
  }

  /* ================= IP-02 RECORD BOOK STRIP ================= */
  /* data: { channel, rows:[{ n, glyph, live }] } — 8 numbered rows, always */
  function ip02(data) {
    var c = cell("IP-02", "RECORD BOOK STRIP",
      ["ENTRY\nINDICATOR", "LOG\nCHANNEL", "SEQUENCE\nWINDOW", "INTEGRITY\nNOTCH"]);

    var hd = win(c.inn, "mid");
    add(hd, "div", "ip-lb", "REC-STRIP");
    var chV = add(hd, "div", "ip-lb");

    var rows = add(c.inn, "div", "ip2-rows");
    var gut = add(rows, "div", "ip2-gut");
    var list = add(rows, "div", "ip2-list");

    var R = [];
    for (var i = 0; i < 8; i++) {
      var pip = glyph("circle", 7, "dim");
      gut.appendChild(pip);
      var row = add(list, "div", "ip2-row");
      var n = add(row, "span", "n");
      var slot = add(row, "span", "gslot");
      R.push({ row: row, pip: pip, n: n, slot: slot });
    }

    function paint(d) {
      put(chV, d.channel ? "CH." + d.channel : null, "CH.——");
      var src = d.rows || [];
      for (var i = 0; i < 8; i++) {
        var r = R[i], e = src[i] || {};
        var live = !!e.live;
        /* the slot number is engraved on the strip; the ENTRY GLYPH is the datum */
        r.n.textContent = (e.n === undefined || e.n === null) ? pad(i + 1, 3) : String(e.n);
        r.slot.innerHTML = "";
        if (e.glyph && GLYPH[e.glyph]) {
          r.slot.appendChild(glyph(e.glyph, 11, live ? "warm" : ""));
        } else {
          add(r.slot, "span", "dash", DASH.glyph);
        }
        r.row.className = "ip2-row" + (live ? " live" : "");
        r.pip.setAttribute("class", "ip-g " + (live ? "warm" : "dim"));
      }
    }
    return register(c.root, paint, data);
  }

  /* ================= IP-03 ZONE DIAL ================= */
  /* data: { zone, sector, sectors } — concentric ring dial, sector index, the zone word */
  function ip03(data) {
    var c = cell("IP-03", "ZONE DIAL",
      ["ZONE\nRING", "SECTOR\nINDEX", "ALIGNMENT\nMARK", "READOUT\nWINDOW"], { leads: "dial" });

    var dial = add(c.cellEl, "div", "ip-dial");
    var SZ = 200, C = 100, R = 92;
    var s = svgRoot(SZ, SZ, "ip-rings");

    /* THE SHEET'S DIAL, read off C4 cell 3 (replica-lab correction 2026-07-21): the subject is
       ONE heavy annulus — rim at ratio(4), inner wall at ratio(3), a band ring on the mid
       radius between them — over an empty readout disc rimmed at ratio(2). Every radius here
       is still a map radius, which is what keeps the rings legal (A11 §3.1); what changed is
       that the two innermost citations were DROPPED from this dial. On the sheet the readout
       disc is empty, so a ring under the zone number is an invention, and an invented ring in
       a two-ink drawing is the same class of error as an invented number. */
    /* the annulus wall sits BETWEEN two map radii (the midpoint of ratio(2) and ratio(3)) —
       the sheet's band is wider than ratio(3) alone gives, and a midpoint of two cited radii
       is still a citation. ratio(3) stays as the band's second wall, which is what makes the
       sheet's double-band read. */
    var WALL = (ratio(2) + ratio(3)) / 2;
    var MID = (WALL + ratio(4)) / 2;
    s.appendChild(svg("circle", { cx: C, cy: C, r: R * ratio(4), "class": "r1" }));
    s.appendChild(svg("circle", { cx: C, cy: C, r: R * MID, "class": "r1" }));
    s.appendChild(svg("circle", { cx: C, cy: C, r: R * ratio(3), "class": "r2" }));
    s.appendChild(svg("circle", { cx: C, cy: C, r: R * WALL, "class": "r1" }));
    s.appendChild(svg("circle", { cx: C, cy: C, r: R * ratio(2), "class": "r2" }));

    /* the faint dashed cross the sheet rules through the whole face */
    s.appendChild(svg("line", { x1: C - R, y1: C, x2: C + R, y2: C, "class": "cross dash" }));
    s.appendChild(svg("line", { x1: C, y1: C - R, x2: C, y2: C + R, "class": "cross dash" }));

    /* eight spokes, crossing the ANNULUS only — they divide the band into sectors, they do
       not reach the readout (the sheet's segments stop at the annulus wall) */
    var inner = R * WALL, outer = R;
    var i, a, x1, y1, x2, y2;
    for (i = 0; i < 8; i++) {
      a = (i / 8) * Math.PI * 2 - Math.PI / 2;
      x1 = C + Math.cos(a) * inner; y1 = C + Math.sin(a) * inner;
      x2 = C + Math.cos(a) * outer; y2 = C + Math.sin(a) * outer;
      s.appendChild(svg("line", { x1: x1, y1: y1, x2: x2, y2: y2, "class": "spoke" }));
    }
    /* band blocks: the dial's read marks, one per sector, straddling the band ring with their
       long axis RADIAL — the sheet's rectangles. One set only; a second interleaved set read
       as a tick fringe the sheet does not have. */
    function block(r, deg, w, h) {
      var b = svg("rect", { x: C - w / 2, y: r - h / 2, width: w, height: h, "class": "blk" });
      b.setAttribute("transform", "rotate(" + deg + " " + C + " " + C + ")");
      return b;
    }
    for (i = 0; i < 8; i++) s.appendChild(block(C - R * MID, i * 45 + 22.5, 8, 15));

    /* the index sits INSIDE the annulus and stops at the rim. A needle overshooting the rim
       reads as a pointer at something outside the dial, which is a different claim. */
    var idx = svg("line", { x1: C, y1: C - R * 0.98, x2: C, y2: C - R * 0.74, "class": "idx" });
    var idxCap = svg("rect", { x: C - 4, y: C - R * 0.735, width: 8, height: 5, "class": "idx-cap" });
    s.appendChild(idx); s.appendChild(idxCap);
    dial.appendChild(s);

    var read = add(dial, "div", "ip3-read");
    add(read, "div", "ip-lb", "ZONE");
    var zV = add(read, "div", "ip-v num big");
    var align = add(dial, "div", "ip3-align");
    align.appendChild(glyph("triangle", 15));

    function paint(d) {
      var hasZone = put(zV, d.zone, DASH.n2);
      /* the readout takes a sector NUMBER or a zone WORD (grid.ZONES: private/sensitive/
         public) — a word drops to body-display size so it never overruns the inner disc */
      var short = hasZone && String(d.zone).length <= 3;
      zV.className = "ip-v num" + (short ? " big" : "") + (hasZone ? "" : " ip-void");
      var n = d.sectors || 12;
      var has = !(d.sector === undefined || d.sector === null) && n > 0;
      /* no measured sector => NO needle. A parked needle would read as a bearing. */
      idx.style.display = has ? "" : "none";
      idxCap.style.display = has ? "" : "none";
      if (has) {
        var deg = (Number(d.sector) / n) * 360;
        idx.setAttribute("transform", "rotate(" + deg + " " + C + " " + C + ")");
        idxCap.setAttribute("transform", "rotate(" + deg + " " + C + " " + C + ")");
      }
    }
    return register(c.root, paint, data);
  }

  /* ================= IP-04 TRUST SEAL ================= */
  /* data: { valid_until, hash } */
  function ip04(data) {
    var c = cell("IP-04", "TRUST SEAL",
      ["TRUST\nEMBLEM", "AUTH SEAL\nLENS", "VALIDITY\nFIELD", "SEAL\nHASH"], { shell: { bolts: true } });

    var face = add(c.inn, "div", "ip-face");
    face.appendChild(reticle(84, { ext: 14 }));

    var t = win(c.inn, "mid");
    add(t, "div", "ip-lb", "TRUST SEAL");

    var w2 = win(c.inn, "mid");
    add(w2, "div", "ip-lb", "VALID UNTIL");
    var vV = add(w2, "div", "ip-v num");

    var w3 = win(c.inn, "mid");
    add(w3, "div", "ip-lb", "HASH");
    var hV = add(w3, "div", "ip-v");

    function paint(d) {
      put(vV, d.valid_until, DASH.date);
      put(hV, d.hash, DASH.hash);
    }
    return register(c.root, paint, data);
  }

  /* ================= IP-05 CARRIER-LOST CARD ================= */
  /* data: { code, time } — the honest failure card (A10 CARRIER LOST) */
  function ip05(data) {
    var c = cell("IP-05", "CARRIER-LOST CARD",
      ["LOSS CODE\nFIELD", "TIME STAMP\nWINDOW", "RECOVERY\nFLAG", "ORIGIN\nMARK"]);

    var face = add(c.inn, "div", "ip5-face");
    var t = add(face, "div", "ip-title");
    add(t, "div", null, "CARRIER");
    add(t, "div", null, "LOST");

    /* the double hexagon: the loss sigil, drawn in the six-glyph grammar, always cold */
    var hx = svgRoot(56, 50, "ip-g dim");
    hx.setAttribute("viewBox", "0 0 56 50");
    hx.appendChild(svg("polygon", { points: "28,2 52,14 52,36 28,48 4,36 4,14", "class": "gs" }));
    hx.appendChild(svg("polygon", { points: "28,7 47.5,16.8 47.5,33.2 28,43 8.5,33.2 8.5,16.8", "class": "gs" }));
    face.appendChild(hx);

    var w1 = win(c.inn);
    add(w1, "div", "ip-lb", "CODE");
    var cV = add(w1, "div", "ip-v");

    var w2 = win(c.inn, "rel");
    add(w2, "div", "ip-lb", "TIME");
    var tV = add(w2, "div", "ip-v num");
    var org = glyph("diamond", 13, "dim");
    org.classList.add("ip-mark");
    w2.appendChild(org);

    function paint(d) {
      put(cV, d.code, DASH.n4);
      put(tV, d.time, DASH.clock);
    }
    return register(c.root, paint, data);
  }

  /* ================= IP-06 VERDICT REGISTER ================= */
  /* data: { rows:[{ n, glyph, verdict }] } — verdict in PASS | FAIL | HOLD | null */
  function ip06(data) {
    var c = cell("IP-06", "VERDICT REGISTER",
      ["VERDICT\nCHANNEL", "OUTCOME\nFIELD", "LOCK\nSTATE", "AUDIT\nNOTCH"]);

    var hd = win(c.inn, "mid");
    add(hd, "div", "ip-lb", "VERDICT REG");

    var rows = add(c.inn, "div", "ip6-rows");
    var R = [];
    for (var i = 0; i < 8; i++) {
      var row = add(rows, "div", "ip6-row");
      var n = add(row, "span", "n");
      var g = add(row, "span", "g");
      var o = add(row, "span", "o");
      R.push({ row: row, n: n, g: g, o: o });
    }

    function paint(d) {
      var src = d.rows || [];
      for (var i = 0; i < 8; i++) {
        var r = R[i], e = src[i] || {};
        var v = e.verdict ? String(e.verdict).toUpperCase() : null;
        /* the channel number is engraved; the VERDICT is the datum */
        r.n.textContent = (e.n === undefined || e.n === null) ? pad(i + 1, 2) : String(e.n);
        put(r.o, v, DASH.word);
        r.g.innerHTML = "";
        var tone = v === "FAIL" ? "hot" : "";
        if (e.glyph && GLYPH[e.glyph]) r.g.appendChild(glyph(e.glyph, 11, tone));
        else add(r.g, "span", "dash ip-void", DASH.glyph);
        r.row.className = "ip6-row" +
          (v === "FAIL" ? " fail" : v === "HOLD" ? " hold" : v ? "" : " void");
      }
    }
    return register(c.root, paint, data);
  }

  /* ================= IP-07 LINK METER ================= */
  /* data: { channel, db, quality, live } — dB ladder +20..-60, quality readout */
  var DB_TOP = 20, DB_FLOOR = -60, SEGS = 16;
  function ip07(data) {
    var c = cell("IP-07", "LINK METER",
      ["LINK\nCHANNEL", "SIGNAL\nMETER", "QUALITY\nREADOUT", "SYNC\nMARK"], { shell: { port: true } });

    var hd = win(c.inn, "mid");
    var chV = add(hd, "div", "ip-lb");

    var face = add(c.inn, "div", "ip7-face");
    var scale = add(face, "div", "ip7-scale");
    var marks = ["dB", "+20", "+10", "0", "-10", "-20", "-30", "-40", "-50", "-60"];
    for (var m = 0; m < marks.length; m++) add(scale, "span", null, marks[m]);

    var ladder = add(face, "div", "ip7-ladder");
    var segs = [];
    for (var i = 0; i < SEGS; i++) segs.push(add(ladder, "div", "ip7-seg"));

    var q = win(c.inn, "mid");
    add(q, "div", "ip-lb", "QUALITY");
    var qV = add(q, "div", "ip-v num");

    function paint(d) {
      put(chV, d.channel ? "LINK-" + d.channel : null, "LINK-——");
      var hasDb = !(d.db === undefined || d.db === null);
      /* absence must not look like a measured floor: the unlit rail recedes to the faintest
         stop, so "no reading" and "a real -60 dB" are never the same picture */
      ladder.className = "ip7-ladder" + (hasDb ? "" : " ip-void");
      var lit = 0;
      if (hasDb) {
        var f = (Number(d.db) - DB_FLOOR) / (DB_TOP - DB_FLOOR);
        f = f < 0 ? 0 : f > 1 ? 1 : f;
        lit = Math.round(f * SEGS);
      }
      /* the ladder fills from the FLOOR UP, exactly as C4 prints it: the scale runs +20 at the
         top to -60 at the bottom, so a rising signal lights the bottom segments first and the
         TOP of the amber column is the reading. seg[0] IS the floor segment — panels.css lays
         the rail out column-reverse, so index order and scale order already agree. (Checked
         against the sheet 2026-07-21: an "inverted meter" reading of this loop was wrong.) */
      for (var i = 0; i < SEGS; i++) {
        var on = hasDb && i < lit;
        var edge = on && d.live && i === lit - 1;
        segs[i].className = "ip7-seg" + (on ? " lit" : "") + (edge ? " hot" : "");
      }
      var had = put(qV, d.quality === undefined || d.quality === null ? null : d.quality + "%", DASH.pct);
      qV.className = "ip-v num" + (had && d.live ? " hot" : "") + (had ? "" : " ip-void");
    }
    return register(c.root, paint, data);
  }

  /* ================= IP-08 ROUTE CARD ================= */
  /* data: { nodes:[{glyph,x,y}] (x,y in 0..1 of the map field), path:[[i,j],..],
            hops, cost, eta } — a plan, never a run: no amber on this panel by law */
  function ip08(data) {
    var c = cell("IP-08", "ROUTE CARD",
      ["ORIGIN\nNODE", "DESTINATION\nNODE", "COST\nFIELD", "ETA\nWINDOW"]);

    var hd = win(c.inn, "mid");
    add(hd, "div", "ip-lb", "ROUTE CARD");

    var map = add(c.inn, "div", "ip8-map");
    var MW = 118, MH = 108;
    var s = svgRoot(MW, MH);
    map.appendChild(s);

    var data8 = add(c.inn, "div", "ip8-data");
    function line(k) {
      var row = add(data8, "div", "ip8-line");
      add(row, "span", "ip-lb", k);
      return add(row, "span", "ip-v");
    }
    var hV = line("HOPS"), cV = line("COST"), eV = line("ETA");

    function paint(d) {
      while (s.firstChild) s.removeChild(s.firstChild);
      var nodes = d.nodes || [];
      var pad = 14;
      function px(n) { return pad + n.x * (MW - pad * 2); }
      function py(n) { return pad + n.y * (MH - pad * 2); }
      var links = d.path || [];
      for (var l = 0; l < links.length; l++) {
        var a = nodes[links[l][0]], b = nodes[links[l][1]];
        if (!a || !b) continue;
        var ax = px(a), ay = py(a), bx = px(b), by = py(b);
        /* one bend per hop — the dashed route reads as a plan, not a live trace
           (the live trace is amber and moves; A11 §3.2 — the two must never be confused) */
        var mx = (ax + bx) / 2 + (ay < by ? 8 : -8), my = (ay + by) / 2;
        s.appendChild(svg("path", { d: "M" + ax + "," + ay + " Q" + mx + "," + my + " " + bx + "," + by, "class": "hop" }));
      }
      for (var n = 0; n < nodes.length; n++) {
        var nd = nodes[n], x = px(nd), y = py(nd);
        var g = svg("g", { transform: "translate(" + (x - 5) + "," + (y - 5) + ") scale(1.1)" });
        var shape = GLYPH[nd.glyph] ? GLYPH[nd.glyph]() : GLYPH.circle();
        shape.setAttribute("class", "nd");
        g.appendChild(shape);
        if (nd.terminal) {
          var ring = svg("circle", { cx: 5, cy: 5, r: 7.5, "class": "nd" });
          g.appendChild(ring);
        }
        s.appendChild(g);
      }
      put(hV, d.hops, DASH.n2);
      put(cV, d.cost, DASH.n2);
      put(eV, d.eta, DASH.clock);
    }
    return register(c.root, paint, data);
  }

  /* ================= the catalogue ================= */
  var CATALOG = [
    { code: "IP-01", name: "RUN PLATE", make: ip01 },
    { code: "IP-02", name: "RECORD BOOK STRIP", make: ip02 },
    { code: "IP-03", name: "ZONE DIAL", make: ip03 },
    { code: "IP-04", name: "TRUST SEAL", make: ip04 },
    { code: "IP-05", name: "CARRIER-LOST CARD", make: ip05 },
    { code: "IP-06", name: "VERDICT REGISTER", make: ip06 },
    { code: "IP-07", name: "LINK METER", make: ip07 },
    { code: "IP-08", name: "ROUTE CARD", make: ip08 }
  ];

  /* ================= init / dispose (E1 §2.2, §3.1) ================= */

  /* init(): the module's one real precondition is panels.css. Without it every panel renders
     as unstyled divs — the two inks, the five stops and the dash discipline all silently
     vanish, which is exactly the class of failure the honesty law exists to forbid. So the
     stylesheet contract is CHECKED here and a miss is painted to #err (E1 §5), never assumed. */
  function init(game) {
    GAME = game;
    try {
      var probe = document.createElement("div");
      probe.className = "ip";
      probe.style.position = "absolute"; probe.style.left = "-9999px";
      document.body.appendChild(probe);
      var ink = window.getComputedStyle(probe).getPropertyValue("--ip-hot").trim();
      document.body.removeChild(probe);
      if (ink !== "#ffb000") throw new Error("panels.css not loaded — two-ink law unenforceable");
    } catch (err) {
      var e = document.getElementById("err");
      if (e) { e.textContent = "ERR PANELS INIT " + (err && err.message); e.style.display = "block"; }
      throw err;
    }
  }

  /* release(): a caller that destroys ONE panel says so here, or the registry itself becomes
     the leak (E1 §3.1.3 — null the refs so the heap side can collect) */
  function release(el) {
    var i = LIVE.indexOf(el);
    if (i >= 0) LIVE.splice(i, 1);
    if (el && el.parentNode) el.parentNode.removeChild(el);
    if (el) { el.update = null; el.setIndex = null; }
  }

  function dispose() {
    /* panels take no listeners, no timers and no fetches by design — they render what the
       caller measured and nothing else. The one real resource is the DOM they produced. */
    while (LIVE.length) release(LIVE[LIVE.length - 1]);
    GAME = null;
  }

  return {
    init: init, dispose: dispose, release: release,
    CATALOG: CATALOG, GLYPHS: ["circle", "pentagon", "hexagon", "triangle", "square", "diamond"],
    ip01: ip01, ip02: ip02, ip03: ip03, ip04: ip04,
    ip05: ip05, ip06: ip06, ip07: ip07, ip08: ip08
  };
})();
