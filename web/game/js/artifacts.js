/* artifacts.js — WORLD ARTIFACTS + SPECIMEN RODS as procedural geometry.
   Governance: 02_VISUAL_LAW.md (two inks — void, structure ink at EXACTLY .70/.45/.28/.14/.08,
   amber only where something is alive/working/earned; §4 the concentric field + the six-glyph
   grammar are the only icons; §6 no chrome, no bevels, no third hue) ·
   E5_3D_TRANSLATION.md §1 PROCEDURAL FORMS + §3 TIER 1 (the atlas sheets are read as a SHAPE
   GRAMMAR, never modelled — box + cylinder + torus + lathe composed by parameter) ·
   E1_CODE_ARCHITECTURE.md §2.2 (init(GAME)/dispose(); window.ARTIFACTS is a module global in the
   load-order law, nothing else crosses), §3.1 (every geometry and material registered and
   released; SHARED marks non-owned resources), §5 (comment law: constraints only).
   Reference sheets (studied at full resolution, dimensions read off the rules):
     design/concepts/C3_world_artifacts_v3_dimensioned.png  <- PRIMARY: metres + provenance
     design/concepts/C1_world_artifacts_v2.png              <- interior anatomy
     design/concepts/A5_world_artifacts.png                 <- silhouette + surface language
     design/concepts/A2_specimen_rods.png                   <- the rod anatomy + decay states

   Two laws this file enforces in code, not in prose:
   1. AMBER CENSUS — every artifact carries AT MOST ONE amber element, and the severed rot link
      carries NONE (a dead link earned nothing). The outreach capsule's port is the only HOT
      amber in the whole set: the message awaiting the human hand.
   2. DECAY IS NOT A PALETTE — vessel(state) moves emissiveIntensity and surface integrity ONLY.
      The core amber is the same #ffb000 in `fresh` and in `dead`; in `dead` it is simply at 0.
      No state anywhere swaps a hue.

   Colour law (E2 Move 5, copied from engine.js by construction, not by memory): the palette is
   authored in display space and linearized ONCE, because the composer's LAST pass does the sRGB
   encode. A material built with a raw hex here would come out wrong under that tail. */
window.ARTIFACTS = (function () {
  "use strict";

  var GAME = null;

  /* ---- resource registry (E1 §3.1) — geometries and materials are the only resources this
     module takes: no listeners, no timers, no fetches, no textures. ---- */
  var R = { geoms: [], mats: [] };
  var GC = {};   /* SHARED geometry cache — owned by this module's dispose(), never by a holder */
  var MC = {};   /* SHARED material cache — same ownership */

  function geo(g) { R.geoms.push(g); return g; }
  function mat(m) { R.mats.push(m); return m; }
  function cgeo(key, build) { if (!GC[key]) GC[key] = geo(build()); return GC[key]; }
  function cmat(key, build) { if (!MC[key]) MC[key] = mat(build()); return MC[key]; }

  function lin(hex) { return new THREE.Color(hex).convertSRGBToLinear(); }
  var INK = {
    structure: lin(0x789baf),   /* rgba(120,155,175) — THE structure ink */
    shell:     lin(0x11161d),   /* artifact body: void-adjacent, reads by facet not by albedo */
    shellDeep: lin(0x0a0f15),
    crystal:   lin(0x18222c),
    dark:      lin(0x0b0803),   /* base under an emitter — an emitter is never a lit surface */
    warm:      lin(0xd4a24c),
    hot:       lin(0xffb000)
  };
  /* the five sanctioned structure-ink opacities and NO others (02 §1) */
  var ALPHAS = [0.70, 0.45, 0.28, 0.14, 0.08];
  /* emissive tiers carried from engine.js T-066 — verified post-gamma, never re-tuned here */
  var EMISSIVE = { idle: 0.35, fired: 1.0 };

  function legalAlpha(a) {
    var best = ALPHAS[0], d = 9;
    for (var i = 0; i < ALPHAS.length; i++) {
      var k = Math.abs(ALPHAS[i] - a);
      if (k < d) { d = k; best = ALPHAS[i]; }
    }
    return best;   /* a stray opacity is a stray ink: snapped, never passed through */
  }

  function hash01(n) { var s = Math.sin(n * 127.31) * 43758.5453; return s - Math.floor(s); }

  /* ---- the three material families ---------------------------------------------------- */

  function inkMat(alpha, wire) {
    var a = legalAlpha(alpha);
    return cmat("ink:" + a + ":" + (wire ? 1 : 0), function () {
      return new THREE.MeshBasicMaterial({
        color: INK.structure, transparent: true, opacity: a, wireframe: !!wire, fog: true
      });
    });
  }

  function bodyMat(kind) {
    /* matte, flat-shaded, never glossy (02 §3/§6: no chrome, no specular highlight).
       "matrix" is the crystal that must TRANSMIT — a resonance core sealed inside an opaque
       prism is a core nobody can see, which is the same as not building it. */
    var c = kind === "crystal" || kind === "matrix" ? INK.crystal : (kind === "deep" ? INK.shellDeep : INK.shell);
    var rough = kind === "crystal" || kind === "matrix" ? 0.42 : 0.72;
    return cmat("body:" + kind, function () {
      var o = { color: c, roughness: rough, metalness: 0.0, flatShading: true };
      if (kind === "matrix") { o.transparent = true; o.opacity = 0.45; o.depthWrite = false; }
      return new THREE.MeshStandardMaterial(o);
    });
  }

  function glassMat(alpha) {
    var a = legalAlpha(alpha);
    return cmat("glass:" + a, function () {
      return new THREE.MeshStandardMaterial({
        color: INK.structure, transparent: true, opacity: a, depthWrite: false,
        side: THREE.DoubleSide, roughness: 0.18, metalness: 0.0
      });
    });
  }

  function amberMat(tier, intensity) {
    var i = Math.round(intensity * 100) / 100;
    return cmat("amber:" + tier + ":" + i, function () {
      return new THREE.MeshStandardMaterial({
        color: INK.dark, emissive: tier === "hot" ? INK.hot : INK.warm,
        emissiveIntensity: i, roughness: 0.5, metalness: 0.0
      });
    });
  }

  /* ---- primitive helpers (Box · Cylinder · Torus · Icosahedron · Octahedron · Lathe · Extrude) */

  function put(group, geometry, material, x, y, z) {
    var m = new THREE.Mesh(geometry, material);
    m.position.set(x || 0, y || 0, z || 0);
    group.add(m);
    return m;
  }

  /* Cache-key law (lesson, 2026-07-21): the key carries EVERY parameter, not just the part
     name. A name-only key silently hands back the first variant built and every later size
     collapses onto it — the defect is invisible because the scene still renders. */
  function pkey(prefix, name, args) {
    return prefix + ":" + name + ":" + Array.prototype.slice.call(args, 1).join(",");
  }

  function cyl(key, rt, rb, h, seg) {
    return cgeo(pkey("cyl", key, arguments), function () { return new THREE.CylinderGeometry(rt, rb, h, seg); });
  }
  function box(key, w, h, d) {
    return cgeo(pkey("box", key, arguments), function () { return new THREE.BoxGeometry(w, h, d); });
  }
  function torus(key, r, tube, rseg, tseg, arc) {
    return cgeo(pkey("tor", key, arguments), function () {
      return new THREE.TorusGeometry(r, tube, rseg, tseg, arc === undefined ? Math.PI * 2 : arc);
    });
  }
  function octa(key, r) {
    return cgeo(pkey("oct", key, arguments), function () { return new THREE.OctahedronGeometry(r); });
  }
  function icosa(key, r, detail) {
    return cgeo(pkey("ico", key, arguments), function () { return new THREE.IcosahedronGeometry(r, detail); });
  }
  function dome(key, r, h, seg) {
    /* LatheGeometry quarter-profile — the only sanctioned way to a cap that is not a sphere */
    return cgeo(pkey("lat", key, arguments), function () {
      var pts = [], n = 6;
      for (var i = 0; i <= n; i++) {
        var a = (i / n) * (Math.PI / 2);
        pts.push(new THREE.Vector2(Math.cos(a) * r, Math.sin(a) * h));
      }
      return new THREE.LatheGeometry(pts, seg);
    });
  }

  /* the six-glyph grammar (02 §4.3) — the ONLY icon vocabulary in this world */
  var GLYPH_SIDES = { circle: 24, triangle: 3, square: 4, pentagon: 5, hexagon: 6, diamond: 4 };
  function glyph(kind, r, depth) {
    return cgeo("gly:" + kind + ":" + r + ":" + depth, function () {
      var n = GLYPH_SIDES[kind] || 6;
      var turn = kind === "diamond" ? 0 : (kind === "square" ? Math.PI / 4 : Math.PI / 2);
      var s = new THREE.Shape();
      for (var i = 0; i < n; i++) {
        var a = turn + (i / n) * Math.PI * 2;
        var x = Math.cos(a) * r, y = Math.sin(a) * r;
        if (i === 0) s.moveTo(x, y); else s.lineTo(x, y);
      }
      s.closePath();
      var g = new THREE.ExtrudeGeometry(s, { depth: depth, bevelEnabled: false, curveSegments: 6 });
      g.translate(0, 0, -depth / 2);
      g.rotateX(-Math.PI / 2);          /* extrusion runs +Z; every artifact stands on +Y */
      return g;
    });
  }

  /* the concentric field (02 §4.1, the sacred motif) — rings lying flat on a face, cold */
  function concentric(group, y, radii, alphas, tube) {
    for (var i = 0; i < radii.length; i++) {
      var t = tube || 0.0035;
      var m = put(group, torus("cc:" + radii[i] + ":" + t, radii[i], t, 6, 32),
        inkMat(alphas[i], false), 0, y + i * 0.0004, 0);
      m.rotation.x = -Math.PI / 2;
    }
  }

  /* deterministic fracture — surface integrity expressed as geometry, never as a colour */
  function fractured(key, build, amount, seed) {
    return cgeo("frc:" + key + ":" + amount.toFixed(3), function () {
      var g = build();
      var p = g.attributes.position;
      for (var i = 0; i < p.count; i++) {
        p.setXYZ(i,
          p.getX(i) + (hash01(i + seed) - 0.5) * amount,
          p.getY(i) + (hash01(i * 3 + seed + 7) - 0.5) * amount,
          p.getZ(i) + (hash01(i * 7 + seed + 13) - 0.5) * amount);
      }
      p.needsUpdate = true;
      g.computeVertexNormals();
      return g;
    });
  }

  /* ---- THE CATALOG — dimensions and provenance read off C3, not invented ------------------ */

  var SPEC = {
    ingot:    { code: "WA-09", name: "MEMORY INGOT",          height: 0.48, glyph: "circle",   provenance: "ARCHIVE STRATA-03" },
    capsule:  { code: "WA-10", name: "THOUGHT-BIRTH CAPSULE", height: 0.52, glyph: "pentagon", provenance: "BIRTH FORGE" },
    rotlink:  { code: "WA-11", name: "SEVERED ROT LINK",      height: 0.41, glyph: "hexagon",  provenance: "UNKNOWN ORIGIN" },
    ribbon:   { code: "WA-12", name: "TRACE RIBBON",          height: 0.46, glyph: "triangle", provenance: "TRACE LABORATORY" },
    wafer:    { code: "WA-13", name: "WATCH VERDICT CORE",    height: 0.39, glyph: "square",   provenance: "WATCHER GATE" },
    monolith: { code: "WA-14", name: "DATA MONOLITH",         height: 0.50, glyph: "diamond",  provenance: "LINEAGE ARCHIVE" },
    sphere:   { code: "WA-15", name: "TRUST SPHERE",          height: 0.43, glyph: "circle",   provenance: "TRUST CHAMBER" },
    outreach: { code: "WA-16", name: "OUTREACH CAPSULE",      height: 0.47, glyph: "pentagon", provenance: "BROADCAST MAST" }
  };
  var ALIAS = {
    "wa-09": "ingot", "wa09": "ingot", "memory-ingot": "ingot",
    "wa-10": "capsule", "wa10": "capsule", "thought-birth-capsule": "capsule", "birth-capsule": "capsule",
    "wa-11": "rotlink", "wa11": "rotlink", "severed-rot-link": "rotlink", "rot-link": "rotlink",
    "wa-12": "ribbon", "wa12": "ribbon", "trace-ribbon": "ribbon",
    "wa-13": "wafer", "wa13": "wafer", "verdict-wafer": "wafer", "verdict": "wafer",
    "wa-14": "monolith", "wa14": "monolith", "data-monolith": "monolith",
    "wa-15": "sphere", "wa15": "sphere", "trust-sphere": "sphere",
    "wa-16": "outreach", "wa16": "outreach", "outreach-capsule": "outreach"
  };

  /* ---- 1. WA-09 MEMORY INGOT — 0.48 m -----------------------------------------------------
     Crystalline matrix over a stability base; entangled traces run the length of the prism;
     ONE resonance core, warm (a stored memory exists — it is not working). */
  function buildIngot(g) {
    /* FACET LAW (fix 2026-07-21, from the first render): a tapered cylinder under a cone reads
       as a bullet, not as a crystal. The prism must have PARALLEL sides and terminate through
       bevels — the double-terminated silhouette on A5/C3. FACE turns the hexagon so a FLAT face
       (apothem 0.0676, not the 0.078 circumradius) presents to +Z for the resonance rings. */
    var FACE = Math.PI / 6;
    /* the plinth is BODY, not void (replica-lab 2026-07-21): in `deep` it sat at void luminance
       and its clasp ring read as a hoop floating under a bullet, which is not what C3 draws */
    put(g, cyl("ing.base", 0.086, 0.096, 0.040, 6), bodyMat("shell"), 0, 0.020, 0).rotation.y = FACE;
    put(g, torus("ing.clasp", 0.0845, 0.0035, 6, 24), inkMat(0.14), 0, 0.041, 0).rotation.x = -Math.PI / 2;

    /* PROPORTION, read off C3's dimension line (replica-lab 2026-07-21): the prism is a little
       over half the total height and each termination is a SHORT double bevel closing on a flat
       cap about half the body width. The first build spent 29% of the object on the upper taper,
       which is a bullet nose however parallel the sides below it are. */
    put(g, cyl("ing.bevelL", 0.078, 0.052, 0.050, 6), bodyMat("matrix"), 0, 0.065, 0).rotation.y = FACE;
    put(g, cyl("ing.prism", 0.078, 0.078, 0.285, 6), bodyMat("matrix"), 0, 0.2325, 0).rotation.y = FACE;
    put(g, cyl("ing.bevelU", 0.058, 0.078, 0.060, 6), bodyMat("matrix"), 0, 0.405, 0).rotation.y = FACE;
    put(g, cyl("ing.tip", 0.038, 0.058, 0.045, 6), bodyMat("matrix"), 0, 0.4575, 0).rotation.y = FACE;

    /* stability banding — two cold hairlines, the only rules on the prism. At .28/.14 they lit
       as bright hoops around the body; the sheet rules them faintly, so they sit at the two
       lowest stops and the silhouette carries the form instead. */
    [0.130, 0.300].forEach(function (y, i) {
      var b = put(g, torus("ing.band", 0.0790, 0.0030, 6, 32), inkMat(i ? 0.08 : 0.14), 0, y, 0);
      b.rotation.x = -Math.PI / 2;
    });

    /* entangled traces — five slivers frozen inside the matrix, deterministic, never centred */
    for (var i = 0; i < 5; i++) {
      var a = (i / 5) * Math.PI * 2 + 0.4;
      var rr = 0.026 + hash01(i + 3) * 0.028;
      /* the traces are INSIDE a matrix, not a cage around it: at .45 they lit as bright rods
         and became the silhouette. Shorter, and at the two recessive stops (replica-lab). */
      var t = put(g, box("ing.trace", 0.0030, 0.120 + hash01(i + 9) * 0.055, 0.0030),
        inkMat(i % 2 ? 0.14 : 0.28),
        Math.cos(a) * rr, 0.210 + (hash01(i + 21) - 0.5) * 0.05, Math.sin(a) * rr);
      t.rotation.z = (hash01(i + 31) - 0.5) * 0.22;
      t.rotation.x = (hash01(i + 41) - 0.5) * 0.18;
    }

    /* THE ONE AMBER: the resonance core, read THROUGH the matrix, ringed by the motif on the
       flat face (torus already stands in XY — no rotation, it faces the reader) */
    put(g, octa("ing.core", 0.021), amberMat("warm", EMISSIVE.idle), 0, 0.215, 0);
    [[0.028, 0.45], [0.042, 0.28], [0.056, 0.14]].forEach(function (r) {
      put(g, torus("ing.cc", r[0], 0.0030, 6, 28), inkMat(r[1]), 0, 0.215, 0.0690);
    });
    return g;
  }

  /* ---- 2. WA-10 THOUGHT-BIRTH CAPSULE — 0.52 m ---------------------------------------------
     Stasis chamber under a birth-seal cap. The seed nest holds a nascent behaviour: warm, idle,
     NOT hot — it "requires lattice to awaken" and has therefore earned nothing yet. */
  function buildCapsule(g) {
    put(g, cyl("cap.foot", 0.088, 0.094, 0.035, 12), bodyMat("deep"), 0, 0.0175, 0);
    put(g, torus("cap.life", 0.091, 0.008, 6, 28), inkMat(0.28), 0, 0.050, 0).rotation.x = -Math.PI / 2;

    /* chamber: glass shell over six cold staves (the shell alone reads as nothing) */
    put(g, cyl("cap.shell", 0.078, 0.078, 0.330, 12), glassMat(0.14), 0, 0.200, 0);
    for (var i = 0; i < 6; i++) {
      var a = (i / 6) * Math.PI * 2;
      var s = put(g, box("cap.stave", 0.012, 0.330, 0.008), bodyMat("shell"),
        Math.cos(a) * 0.076, 0.200, Math.sin(a) * 0.076);
      s.rotation.y = -a;
    }
    put(g, torus("cap.mid", 0.080, 0.005, 6, 28), inkMat(0.14), 0, 0.200, 0).rotation.x = -Math.PI / 2;

    /* the seed nest: five struts leaning in on ONE amber seed */
    for (var n = 0; n < 5; n++) {
      var na = (n / 5) * Math.PI * 2 + 0.3;
      var strut = put(g, box("cap.nest", 0.004, 0.060, 0.004), inkMat(0.45),
        Math.cos(na) * 0.030, 0.185, Math.sin(na) * 0.030);
      strut.rotation.z = Math.cos(na) * 0.5;
      strut.rotation.x = -Math.sin(na) * 0.5;
    }
    put(g, octa("cap.seed", 0.018), amberMat("warm", 0.55), 0, 0.212, 0);

    /* birth seal cap — lathe dome, then the seal stack */
    put(g, dome("cap.dome", 0.082, 0.060, 12), bodyMat("shell"), 0, 0.365, 0);
    put(g, cyl("cap.seal", 0.056, 0.072, 0.050, 12), bodyMat("shell"), 0, 0.450, 0);
    put(g, torus("cap.sealring", 0.058, 0.005, 6, 24), inkMat(0.45), 0, 0.470, 0).rotation.x = -Math.PI / 2;
    put(g, cyl("cap.stud", 0.030, 0.044, 0.045, 12), bodyMat("deep"), 0, 0.4975, 0);
    return g;
  }

  /* ---- 3. WA-11 SEVERED ROT LINK — 0.41 m --------------------------------------------------
     A broken torus standing in XY, gap open, joint faces exposed, corruption crystals grown on
     the outer surface. ZERO amber, by law: nothing here is alive, working, or earned. */
  function buildRotLink(g) {
    var Rr = 0.150, tube = 0.048, arc = Math.PI * 1.66;
    /* the arc sweeps from 0; its gap therefore straddles 2π. rot lifts the gap's midpoint to
       +Y so the break reads against the void instead of sitting on the bench. */
    var rot = Math.PI / 2 - (arc + Math.PI * 2) / 2;
    var ring = put(g, torus("rot.ring", Rr, tube, 6, 26, arc), bodyMat("shell"), 0, Rr + tube, 0);
    ring.rotation.z = rot;

    /* severed joint faces — flat, cut, unfinished */
    for (var e = 0; e < 2; e++) {
      var ea = rot + (e ? arc : 0);
      var f = put(g, box("rot.joint", 0.094, 0.094, 0.016), bodyMat("deep"),
        Math.cos(ea) * Rr, Rr + tube + Math.sin(ea) * Rr, 0);
      f.rotation.z = ea;
    }

    /* rot vector scars — cold rules laid across the tube, never a glow */
    for (var s = 0; s < 5; s++) {
      var sa = rot + 0.30 + s * ((arc - 0.60) / 4);
      var sc = put(g, box("rot.scar", 0.100, 0.0035, 0.0035), inkMat(s % 2 ? 0.28 : 0.45),
        Math.cos(sa) * Rr, Rr + tube + Math.sin(sa) * Rr, 0);
      sc.rotation.z = sa + Math.PI / 2;
    }

    /* corruption crystals on the outer surface + link fragments drifted out of the gap */
    for (var c = 0; c < 7; c++) {
      var ca = rot + hash01(c + 5) * arc;
      var cr = Rr + tube * (0.65 + hash01(c + 15) * 0.4);
      var xt = put(g, octa("rot.crystal" + (c % 3), 0.011 + (c % 3) * 0.005), bodyMat("crystal"),
        Math.cos(ca) * cr, Rr + tube + Math.sin(ca) * cr, (hash01(c + 25) - 0.5) * 0.045);
      xt.rotation.set(hash01(c + 35) * 3, hash01(c + 45) * 3, hash01(c + 55) * 3);
    }
    for (var fr = 0; fr < 3; fr++) {
      var fa = rot - (0.16 + fr * 0.14);
      var chip = put(g, box("rot.chip" + fr, 0.030 + fr * 0.008, 0.026, 0.034), bodyMat("shell"),
        Math.cos(fa) * (Rr + fr * 0.012), Rr + tube + Math.sin(fa) * (Rr - fr * 0.010), (hash01(fr + 2) - 0.5) * 0.03);
      chip.rotation.set(hash01(fr + 61) * 1.2, hash01(fr + 71) * 1.2, fa);
    }
    return g;
  }

  /* ---- 4. WA-12 TRACE RIBBON — 0.46 m ------------------------------------------------------
     A frozen trace: the helix is warm, never hot. It is a record of a run, not a run.
     (02 §4.2 reserves the moving amber packet for the live trace; this one does not move.) */
  function buildRibbon(g) {
    put(g, cyl("rib.plinth", 0.072, 0.080, 0.035, 8), bodyMat("deep"), 0, 0.0175, 0);
    put(g, cyl("rib.plug", 0.030, 0.030, 0.022, 8), bodyMat("shell"), 0, 0.046, 0);
    put(g, cyl("rib.shell", 0.068, 0.068, 0.340, 10), glassMat(0.14), 0, 0.205, 0);

    /* eight cold verticals give the glass an edge to read against the void */
    for (var i = 0; i < 8; i++) {
      var a = (i / 8) * Math.PI * 2;
      put(g, box("rib.mullion", 0.004, 0.340, 0.004), inkMat(0.28),
        Math.cos(a) * 0.0675, 0.205, Math.sin(a) * 0.0675);
    }

    /* THE ONE AMBER: the ribbon itself — 2.5 turns of banded segments, tangent-oriented */
    /* ORIENTATION LAW (fix 2026-07-21, from the first render): under rotation.y = t, a box's
       local +X maps to (cos t, 0, -sin t) — the RADIAL direction. Setting it to -ang therefore
       pointed every segment outward and the ribbon rendered as a sawtooth of fins. The tangent
       of the helix needs -(ang + PI/2). The pitch and the segment length are then derived from
       the helix, not guessed: a guessed pitch leaves visible gaps at the turns. */
    var segs = 64, turns = 2.5, y0 = 0.070, hgt = 0.270, rad = 0.040;
    var pitch = Math.atan2(hgt, turns * Math.PI * 2 * rad);
    var arc = (turns * Math.PI * 2 * rad) / segs;
    var ribbonMat = amberMat("warm", EMISSIVE.idle);   /* a frozen trace idles; only a live one fires */
    var segGeo = box("rib.seg", (arc / Math.cos(pitch)) * 1.06, 0.022, 0.004);
    for (var s = 0; s < segs; s++) {
      var t = s / (segs - 1), ang = t * turns * Math.PI * 2;
      var m = put(g, segGeo, ribbonMat, Math.cos(ang) * rad, y0 + t * hgt, Math.sin(ang) * rad);
      m.rotation.y = -(ang + Math.PI / 2);
      m.rotateZ(pitch);     /* the helix pitch, applied in the segment's own frame */
    }

    /* time encoding — cold ticks up the shell, evidence not ornament */
    for (var k = 0; k < 7; k++) {
      put(g, box("rib.tick", 0.014, 0.0030, 0.0030), inkMat(k % 3 === 0 ? 0.45 : 0.14),
        0.0715, 0.080 + k * 0.038, 0);
    }

    put(g, cyl("rib.cap", 0.080, 0.072, 0.035, 8), bodyMat("deep"), 0, 0.3925, 0);
    put(g, cyl("rib.crown", 0.056, 0.072, 0.030, 8), bodyMat("shell"), 0, 0.425, 0);
    put(g, cyl("rib.stud", 0.028, 0.040, 0.020, 8), bodyMat("deep"), 0, 0.450, 0);
    return g;
  }

  /* ---- 5. WA-13 WATCH VERDICT CORE — 0.39 m ------------------------------------------------
     A flat engraved wafer, lying face-up: the concentric field IS the engraving. The judgment
     core is a hexagon glyph (six-glyph grammar), warm — the verdict exists and is final. */
  /* ORIENTATION FIX (replica-lab 2026-07-21): C3 cell 5 stands this one on edge with its
     verdict FACE to the reader — its 0.39 m is the face diameter, and SPEC.height says 0.39.
     Built flat (every radius is easier to reason about in XZ), then stood up as one group, so
     the object's real Y extent finally equals the number its own record publishes. A wafer
     lying flat read as a plate on the floor and contradicted its own dimension line. */
  function buildWafer(gOut) {
    var g = new THREE.Group();
    g.rotation.x = Math.PI / 2;      /* local +Y (the engraved face) -> world +Z, facing out */
    g.position.y = 0.195;            /* the face's radius: the standing disc rests on y = 0 */
    gOut.add(g);

    put(g, cyl("waf.disc", 0.195, 0.195, 0.032, 10), bodyMat("shell"), 0, 0.016, 0);
    put(g, cyl("waf.seal", 0.170, 0.186, 0.010, 10), bodyMat("deep"), 0, 0.036, 0);

    concentric(g, 0.0415, [0.052, 0.088, 0.124, 0.158], [0.45, 0.28, 0.28, 0.14]);

    /* authority channels — six radial cuts, the wafer's only asymmetry-free grammar */
    for (var i = 0; i < 6; i++) {
      var a = (i / 6) * Math.PI * 2;
      var ch = put(g, box("waf.chan", 0.115, 0.0035, 0.0035), inkMat(i % 2 ? 0.14 : 0.28),
        Math.cos(a) * 0.108, 0.0418, Math.sin(a) * 0.108);
      ch.rotation.y = -a;
    }

    /* integrity clasps on the rim — local X is RADIAL under rotation.y, so the thin dimension
       goes first or the clasps push the wafer past its 0.39 m rule */
    for (var c = 0; c < 5; c++) {
      var ca = (c / 5) * Math.PI * 2 + 0.3;
      var cl = put(g, box("waf.clasp", 0.014, 0.026, 0.030), bodyMat("deep"),
        Math.cos(ca) * 0.186, 0.016, Math.sin(ca) * 0.186);
      cl.rotation.y = -ca;
    }

    /* THE ONE AMBER: the judgment core, a hexagon seal at the centre of the field */
    put(g, glyph("hexagon", 0.024, 0.010), amberMat("warm", EMISSIVE.idle), 0, 0.043, 0);
    put(g, torus("waf.corering", 0.034, 0.0035, 6, 28), inkMat(0.70), 0, 0.0435, 0).rotation.x = -Math.PI / 2;
    return gOut;
  }

  /* ---- 6. WA-14 DATA MONOLITH — 0.50 m -----------------------------------------------------
     A stepped obelisk: foundation clip, compression stack, shaft, data prism. The inscription
     is the one amber — high-density knowledge that EXISTS but is not decompressed. */
  function buildMonolith(g) {
    put(g, glyph("square", 0.145, 0.022), bodyMat("deep"), 0, 0.011, 0);
    put(g, box("mon.clip", 0.166, 0.020, 0.166), bodyMat("deep"), 0, 0.032, 0);

    var steps = [[0.135, 0.030, 0.057], [0.118, 0.028, 0.086], [0.104, 0.026, 0.113]];
    steps.forEach(function (s, i) {
      put(g, box("mon.step" + i, s[0], s[1], s[0]), bodyMat("shell"), 0, s[2], 0);
      var r = put(g, torus("mon.stepline" + i, s[0] * 0.72, 0.0030, 6, 20),
        inkMat(i === 0 ? 0.28 : 0.14), 0, s[2] + s[1] / 2 + 0.001, 0);
      r.rotation.x = -Math.PI / 2;
    });

    var shaft = put(g, cyl("mon.shaft", 0.038, 0.054, 0.280, 4), bodyMat("shell"), 0, 0.266, 0);
    shaft.rotation.y = Math.PI / 4;
    var prism = put(g, cyl("mon.prism", 0.0, 0.038, 0.094, 4), bodyMat("crystal"), 0, 0.453, 0);
    prism.rotation.y = Math.PI / 4;

    /* inscription layers — cold rules with ONE amber column of live-looking density.
       No text, no numerals: an invented readout would be a fabricated number (HONESTY LAW). */
    for (var i2 = 0; i2 < 9; i2++) {
      var y = 0.156 + i2 * 0.024;
      var wdt = 0.062 - i2 * 0.0032;
      put(g, box("mon.rule" + i2, wdt, 0.0025, 0.0025), inkMat(i2 % 3 === 0 ? 0.28 : 0.08),
        0, y, 0.048 - i2 * 0.0018);
    }
    var insMat = amberMat("warm", 0.40);
    for (var k = 0; k < 5; k++) {
      put(g, box("mon.ins", 0.016, 0.007, 0.003), insMat, 0, 0.192 + k * 0.030, 0.0455 - k * 0.0022);
    }
    return g;
  }

  /* ---- 7. WA-15 TRUST SPHERE — 0.43 m ------------------------------------------------------
     An icosphere lattice with metric nodes at the twelve vertices. The calibration core is warm:
     a snapshot of trust EXISTS; it is not being computed right now. */
  function buildSphere(g) {
    /* 0.43 m overall (C3 rule) governs BOTH axes: height = plinth + diameter, and the
       interface ring must stay inside it — hence the 1.02 factor, not a decorative halo */
    var Rs = 0.203, cy = Rs + 0.021;

    put(g, icosa("sph.hull", Rs * 0.985, 1), glassMat(0.08), 0, cy, 0);
    put(g, icosa("sph.lattice", Rs, 1), inkMat(0.45, true), 0, cy, 0);
    put(g, icosa("sph.inner", Rs * 0.62, 0), inkMat(0.14, true), 0, cy, 0);

    /* metric nodes — one octahedron per icosahedron vertex, deduped off the real attribute */
    var src = icosa("sph.nodesrc", Rs, 0).attributes.position;
    var seen = {}, nodeGeo = octa("sph.node", 0.0125), nodeMat = bodyMat("shell");
    for (var i = 0; i < src.count; i++) {
      var x = src.getX(i), y = src.getY(i), z = src.getZ(i);
      var key = x.toFixed(3) + "|" + y.toFixed(3) + "|" + z.toFixed(3);
      if (seen[key]) continue;
      seen[key] = 1;
      put(g, nodeGeo, nodeMat, x, cy + y, z);
    }

    /* interface ring + plinth — the sphere is an instrument, not a ball */
    put(g, torus("sph.iface", Rs * 1.02, 0.0055, 6, 44), inkMat(0.28), 0, cy, 0).rotation.x = -Math.PI / 2;
    put(g, cyl("sph.plinth", 0.052, 0.066, 0.020, 8), bodyMat("deep"), 0, 0.010, 0);
    put(g, cyl("sph.stem", 0.014, 0.014, 0.030, 6), bodyMat("shell"), 0, 0.032, 0);

    /* THE ONE AMBER: the calibration core, suspended at the centre */
    put(g, octa("sph.core", 0.026), amberMat("warm", EMISSIVE.idle), 0, cy, 0);
    return g;
  }

  /* ---- 8. WA-16 OUTREACH CAPSULE — 0.47 m --------------------------------------------------
     Sealed both ends. ONE amber delivery port, and it is HOT — the only hot amber in the whole
     catalog. The message inside stays dark: it has not been sent. Only the hand can send it. */
  function buildOutreach(g) {
    put(g, cyl("out.foot", 0.052, 0.052, 0.012, 12), bodyMat("deep"), 0, 0.006, 0);
    put(g, cyl("out.lower", 0.075, 0.052, 0.048, 12), bodyMat("shell"), 0, 0.036, 0);
    put(g, cyl("out.body", 0.075, 0.075, 0.350, 12), bodyMat("shell"), 0, 0.235, 0);
    put(g, cyl("out.upper", 0.052, 0.075, 0.048, 12), bodyMat("shell"), 0, 0.434, 0);
    put(g, cyl("out.seal", 0.040, 0.052, 0.012, 12), bodyMat("deep"), 0, 0.464, 0);

    /* stasis bands + sleeve facets */
    [0.120, 0.330].forEach(function (y) {
      put(g, torus("out.band", 0.0775, 0.0060, 6, 28), inkMat(0.28), 0, y, 0).rotation.x = -Math.PI / 2;
    });
    for (var i = 0; i < 12; i++) {
      var a = (i / 12) * Math.PI * 2;
      put(g, box("out.facet", 0.0030, 0.350, 0.0030), inkMat(i % 3 === 0 ? 0.14 : 0.08),
        Math.cos(a) * 0.0752, 0.235, Math.sin(a) * 0.0752);
    }

    /* the message core — inside, cold, unlit. An unsent message has earned no light. */
    put(g, box("out.msg", 0.030, 0.110, 0.030), bodyMat("deep"), 0, 0.235, 0);

    /* THE DELIVERY PORT — recessed, ringed by the concentric motif, hot */
    var pz = 0.0745;
    put(g, cyl("out.portwell", 0.026, 0.030, 0.010, 12), bodyMat("deep"), 0, 0.235, pz - 0.004)
      .rotation.x = Math.PI / 2;
    var port = put(g, cyl("out.port", 0.0110, 0.0110, 0.006, 8), amberMat("hot", EMISSIVE.fired), 0, 0.235, pz);
    port.rotation.x = Math.PI / 2;
    put(g, torus("out.portring1", 0.0195, 0.0032, 6, 24), inkMat(0.70), 0, 0.235, pz);
    put(g, torus("out.portring2", 0.0300, 0.0028, 6, 28), inkMat(0.45), 0, 0.235, pz - 0.001);
    put(g, torus("out.portring3", 0.0420, 0.0025, 6, 32), inkMat(0.14), 0, 0.235, pz - 0.002);
    return g;
  }

  var BUILD = {
    ingot: buildIngot, capsule: buildCapsule, rotlink: buildRotLink, ribbon: buildRibbon,
    wafer: buildWafer, monolith: buildMonolith, sphere: buildSphere, outreach: buildOutreach
  };

  /* ---- SPECIMEN RODS (A2) ------------------------------------------------------------------
     One anatomy, six decay states. THE LAW OF THIS FUNCTION: a state moves emissiveIntensity
     and surface integrity, and NOTHING else. The core emissive colour is #ffb000 in every state
     including `dead` (where its intensity is simply 0). No state swaps a hue, ever.
     Emissive tiers ride engine.js's verified idle/fired pair; the decayed tiers step below idle
     because a decaying rod is less alive, not a different colour of alive. */
  var DECAY = {
    fresh:    { emissive: EMISSIVE.fired, integrity: 1.00, sleeve: 0.28 },
    stable:   { emissive: EMISSIVE.idle,  integrity: 0.96, sleeve: 0.28 },
    drifting: { emissive: 0.22,           integrity: 0.86, sleeve: 0.14 },
    cooling:  { emissive: 0.14,           integrity: 0.78, sleeve: 0.14 },
    rotting:  { emissive: 0.06,           integrity: 0.52, sleeve: 0.08 },
    dead:     { emissive: 0.00,           integrity: 0.28, sleeve: 0.08 }
  };
  var STATES = ["fresh", "stable", "drifting", "cooling", "rotting", "dead"];
  var ROD = { height: 0.440, staves: 10, radius: 0.041 };

  function buildVessel(g, state) {
    var d = DECAY[state];
    var wear = 1 - d.integrity;
    var seed = 101 + STATES.indexOf(state) * 37;

    /* base lock ring + lower collar — the crumbling base at low integrity */
    put(g, fractured("rod.foot", function () {
      return new THREE.CylinderGeometry(0.044, 0.050, 0.030, 8);
    }, wear * 0.016, seed), bodyMat("deep"), 0, 0.015, 0);
    put(g, torus("rod.lock", 0.0480, 0.0060, 6, 20), inkMat(d.integrity > 0.7 ? 0.45 : 0.14), 0, 0.031, 0)
      .rotation.x = -Math.PI / 2;
    put(g, cyl("rod.collarL", 0.046, 0.046, 0.030, 8), bodyMat("shell"), 0, 0.045, 0);

    /* the housing sleeve: discrete staves. Integrity removes them — a hole is honest, a dark
       texture is not. Survivors carry deterministic tilt and offset scaled by wear. */
    var keep = Math.max(4, Math.round(ROD.staves * (0.35 + 0.65 * d.integrity)));
    var staveGeo = fractured("rod.stave", function () {
      return new THREE.BoxGeometry(0.020, 0.284, 0.011);
    }, wear * 0.010, seed + 3);
    var staveMat = bodyMat("shell");
    for (var i = 0; i < ROD.staves; i++) {
      if (i >= keep) continue;
      var a = (i / ROD.staves) * Math.PI * 2;
      var rr = ROD.radius + (hash01(i + seed) - 0.5) * wear * 0.012;
      var s = put(g, staveGeo, staveMat,
        Math.cos(a) * rr, 0.205 + (hash01(i + seed + 11) - 0.5) * wear * 0.020, Math.sin(a) * rr);
      s.rotation.y = -a;
      s.rotation.z = (hash01(i + seed + 21) - 0.5) * wear * 0.30;
      s.rotation.x = (hash01(i + seed + 31) - 0.5) * wear * 0.22;
    }

    /* quartz sleeve — clouds by legal ink opacity as integrity falls; never by hue */
    put(g, cyl("rod.quartz", 0.032, 0.032, 0.284, 10), glassMat(d.sleeve), 0, 0.205, 0);

    /* the model core — the ONE amber, same ink at every state */
    put(g, cyl("rod.core", 0.013, 0.013, 0.240, 6), amberMat("hot", d.emissive), 0, 0.205, 0);
    put(g, torus("rod.coupler", 0.0175, 0.0028, 6, 16), inkMat(0.28), 0, 0.110, 0).rotation.x = -Math.PI / 2;
    put(g, torus("rod.coupler", 0.0175, 0.0028, 6, 16), inkMat(0.28), 0, 0.300, 0).rotation.x = -Math.PI / 2;

    /* upper collar + polar seal cap */
    put(g, cyl("rod.collarU", 0.046, 0.046, 0.030, 8), bodyMat("shell"), 0, 0.365, 0);
    put(g, fractured("rod.cap", function () {
      return new THREE.CylinderGeometry(0.028, 0.046, 0.035, 8);
    }, wear * 0.012, seed + 5), bodyMat("deep"), 0, 0.3975, 0);
    put(g, cyl("rod.stud", 0.014, 0.028, 0.025, 8), bodyMat("shell"), 0, 0.4275, 0);

    /* shed shards: what fell off, still on the bench. Only below the integrity line. */
    if (d.integrity < 0.60) {
      var chips = Math.round((0.60 - d.integrity) * 22);
      for (var c = 0; c < chips; c++) {
        var ca = hash01(c + seed + 41) * Math.PI * 2;
        var cd = 0.052 + hash01(c + seed + 51) * 0.028;
        var chip = put(g, octa("rod.chip" + (c % 3), 0.006 + (c % 3) * 0.003), bodyMat("shell"),
          Math.cos(ca) * cd, 0.006 + hash01(c + seed + 61) * 0.006, Math.sin(ca) * cd);
        chip.rotation.set(hash01(c + 71) * 3, hash01(c + 81) * 3, hash01(c + 91) * 3);
      }
    }
    return g;
  }

  /* ---- the public seam ---------------------------------------------------------------- */

  function fail(what) {
    /* E1 §5: a module failure reaches #err — it never vanishes into a console */
    var el = document.getElementById("err");
    if (el) { el.textContent = "ARTIFACTS " + what; el.style.display = "block"; }
    return null;
  }

  function make(id, opts) {
    var key = String(id || "").toLowerCase();
    key = BUILD[key] ? key : (ALIAS[key] || key);
    if (!BUILD[key]) return fail("UNKNOWN ARTIFACT " + String(id).toUpperCase());
    var o = opts || {};
    var g = new THREE.Group();
    g.name = "artifact:" + key;
    BUILD[key](g);
    if (o.scale) g.scale.setScalar(o.scale);
    if (o.spin !== undefined) g.rotation.y = o.spin;
    /* userData carries the sheet's OWN facts (code, name, metres, provenance) — never a number
       this module invented. A holder that wants a readout prints these or prints dashes. */
    g.userData = {
      kind: "artifact", id: key, code: SPEC[key].code, label: SPEC[key].name,
      height: SPEC[key].height, glyph: SPEC[key].glyph, provenance: SPEC[key].provenance
    };
    return g;
  }

  function vessel(state, opts) {
    var st = String(state || "stable").toLowerCase();
    if (!DECAY[st]) return fail("UNKNOWN DECAY STATE " + String(state).toUpperCase());
    var o = opts || {};
    var g = new THREE.Group();
    g.name = "vessel:" + st;
    buildVessel(g, st);
    if (o.scale) g.scale.setScalar(o.scale);
    if (o.spin !== undefined) g.rotation.y = o.spin;
    g.userData = {
      kind: "vessel", state: st, height: ROD.height,
      emissive: DECAY[st].emissive, integrity: DECAY[st].integrity
    };
    return g;
  }

  function init(game) {
    GAME = game;
    if (typeof THREE === "undefined") return fail("THREE MISSING — LOAD ORDER");
    /* no listeners, no timers, no fetches: this module's only resources are GPU resources.
       Warming the caches at init makes the first make() free of a build spike mid-flight. */
    inkMat(0.70); inkMat(0.45); inkMat(0.28); inkMat(0.14); inkMat(0.08);
    bodyMat("shell"); bodyMat("deep"); bodyMat("crystal");
    if (GAME && GAME.state) GAME.state.artifacts = { SPEC: SPEC, STATES: STATES };
    return true;
  }

  function dispose() {
    /* E1 §3.1: this module OWNS every geometry and material it hands out (they are SHARED
       across every group it built, so a holder must never dispose them — it calls this).
       r128 dispose() is idempotent, so ENGINE's generic scene sweep double-hitting these is
       harmless; ownership still lives here. */
    var i;
    for (i = 0; i < R.geoms.length; i++) R.geoms[i].dispose();
    for (i = 0; i < R.mats.length; i++) R.mats[i].dispose();
    R.geoms.length = 0;
    R.mats.length = 0;
    GC = {};
    MC = {};
    if (GAME && GAME.state) GAME.state.artifacts = null;
    GAME = null;
  }

  return {
    make: make, vessel: vessel, init: init, dispose: dispose,
    IDS: ["ingot", "capsule", "rotlink", "ribbon", "wafer", "monolith", "sphere", "outreach"],
    STATES: STATES, SPEC: SPEC
  };
})();
