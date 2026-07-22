/* bench.js — THE BENCH: the P0 plate, born as a module (E1 §2.1 — never lives in the spine file).
   Governance: E4_UX_P0.md at THE P0-CUT (BINDING) — states COMPOSE/RUN/HALT + the LAST/BEST
   rider; grammar §6 exact; trace §8 (packet advances ONLY on real trace rows, T+ live readout
   between, no interpolated progress); failure §9 (instant, located, HELD); refusals as
   receipts, never tooltips [GRAFT-A4] · P0 SPEC ADDENDUM (run contract: POST /api/construct/run
   -> run_id immediately, GET ?id= live status polled by run_id; zone REQUIRED, private-default,
   public explicit; per-link ms from the harness's perf_counter — printed, never invented
   client-side; trust law evaluated server-side at fire time — refusals land here as receipts) ·
   E1 §2.2/§3.1 (init(GAME)/dispose(); every listener/timer/fetch owned in R and released;
   the probe is read from GAME.state.engine.scene — proximity is derived from engine state,
   never duplicated) · 04 §0 (choreography ms; two-ink; hold 600ms ring; reduced motion) ·
   A11 (scarcity: a virgin plate is ALL structure ink; the T+ counter is the plate's one
   display-size number and exists only while a run is live).
   Bus law (E1 §2.2): run:link has NO listener in this build yet — nothing is emitted;
   the first real listener plumbs the emit. Speculative emits are the named defect class.
   Layout target: samples/bench_sample.html. */
window.BENCH = (function () {
  "use strict";

  var GAME = null;

  /* ---- resource registry (E1 §3.1: listeners, timers, and fetches are resources) ---- */
  var R = { listeners: [], timers: [], aborts: [] };
  function listen(t, ty, fn, cap) { t.addEventListener(ty, fn, !!cap); R.listeners.push([t, ty, fn, !!cap]); return fn; }
  function timer(id) { R.timers.push(id); return id; }
  function abortable() { var c = new AbortController(); R.aborts.push(c); return c; }
  function dropAbort(c) { var i = R.aborts.indexOf(c); if (i >= 0) R.aborts.splice(i, 1); }

  /* ---- anchors + law constants ---- */
  var SLAB = { x: 0, y: 1.1, z: 26 };     /* engine.js NEXUS — the proven anchor (E4 §4) */
  var RANGE = 12;                          /* the ~12 m prompt law (E4 §4) */
  var ZONES = ["private", "sensitive", "public"];  /* grid.ZONES vocabulary — real words only */
  var PLANT_TOTAL = 15;                    /* grid.PLANTS census — the foundry row's 15 sites */
  var POLL_MS = 300, API_TIMEOUT_MS = 6000;
  /* dock camera: fixed high oblique over the slab, foundry row in the middle distance
     behind the plate (E4 §4 + §8.3 [GRAFT-B1] — the siting IS the graft) */
  var CAM = { pos: new THREE.Vector3(-6, 13, 6), look: new THREE.Vector3(1, 0.8, 40) };

  /* the ONE curated task (P0 addendum: bench-task v0; tier_floor pinned local/keyless
     server-side — the client never picks a tier, the TAP strip prints that truth) */
  var TASK = { id: "t-01", line: "T-01 FIRST DRAW · OPEN TARGET", check: "check: a real answer returns · beat your record, any axis" };

  /* chip rows mirror modules.json v0 — each names the REAL entry point it wraps
     (registry law, P0 addendum). glyph: circle = seed family, pent = axis (A11 §3.3). */
  var PARTS = {
    tap:      { nm: "TAP",      slot: "head", glyph: "circ", entry: "energy.draw" },
    scaffold: { nm: "SCAFFOLD", slot: "mid",  glyph: "pent", entry: "prompt scaffold" },
    governor: { nm: "GOVERNOR", slot: "mid",  glyph: "circ", entry: "grid.METER.can_spend" },
    ladder:   { nm: "LADDER",   slot: "mid",  glyph: "circ", entry: "energy.ladder" },
    scorer:   { nm: "SCORER",   slot: "tail", glyph: "circ", entry: "receipt scorer" }
  };
  var RAIL = ["tap", "scaffold", "governor", "ladder", "scorer"];

  /* ---- state ---- */
  var S = {
    still: false, benchBoot: false,
    live: false,               /* mirrors engine controls-live: first observed keydown */
    near: false, docked: false,
    state: "COMPOSE",          /* COMPOSE | RUN | HALT */
    head: null, mid: [], tail: null,
    ghost: null, cursor: 0,    /* cursor indexes the rendered gap list */
    sel: null,                 /* {t:"head"|"mid"|"tail", i} */
    strip: false,
    zone: "private",           /* the zone law: private-default; public only by the dial */
    grid: null,                /* /state snapshot: {online, win, quota, rods} | false = CARRIER LOST */
    run: null,                 /* live run: {rid, n, t0, parts, links, packetEl, tplusEl, stops} */
    runCount: 0,
    last: null, best: null,    /* session pass rows only — P1 builds the book over runs.json */
    firstPass: {},             /* per construct id, THIS SESSION — the once-EVER law completes
                                  at P1 when history surfaces (named gap, not a fake) */
    failTick: null,            /* seat that keeps the structure tick for the visit (E4 §9) */
    hold: null                 /* HOLD-C: {t0, drain, drainFrom, drainT0} */
  };

  var D = {};                  /* dom refs */
  var probeRef = null, camOn = false;

  /* ---- audio (04 §0: WebAudio oscillators only, zero assets) ---- */
  var AC = null, humOsc = null, humGain = null;
  function ac() {
    if (S.still) return null;
    if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { AC = null; } }
    return AC;
  }
  function blip(freq, ms, ramp) {
    var a = ac(); if (!a) return;
    try {
      var o = a.createOscillator(), g = a.createGain();
      o.type = "square"; o.frequency.value = freq || 520;
      if (ramp) o.frequency.linearRampToValueAtTime(ramp, a.currentTime + (ms || 40) / 1000);
      g.gain.value = 0.05;
      g.gain.setTargetAtTime(0, a.currentTime + (ms || 40) / 1000, 0.01);
      o.connect(g); g.connect(a.destination);
      o.start(); o.stop(a.currentTime + (ms || 40) / 1000 + 0.05);
    } catch (e) { }
  }
  function sting() { blip(660, 40); timer(setTimeout(function () { blip(880, 40); }, 90)); }
  function humStart() {
    var a = ac(); if (!a || humOsc) return;
    try {
      humOsc = a.createOscillator(); humGain = a.createGain();
      humOsc.type = "triangle"; humOsc.frequency.value = 55; humGain.gain.value = 0.05;
      humOsc.connect(humGain); humGain.connect(a.destination); humOsc.start();
    } catch (e) { humOsc = null; }
  }
  function humStop() {
    if (!humOsc) return;
    try { humOsc.stop(); humOsc.disconnect(); humGain.disconnect(); } catch (e) { }
    humOsc = humGain = null;
  }

  /* ---- api: every fetch abortable + timed out (E1 §3.1.7 — the bench poller ships
     with abort from day one; a hung carrier can never lock the plate forever) ---- */
  function api(method, url, body) {
    var c = abortable();
    var to = timer(setTimeout(function () { c.abort(); }, API_TIMEOUT_MS));
    var opt = { method: method, signal: c.signal };
    if (body) { opt.headers = { "Content-Type": "application/json" }; opt.body = JSON.stringify(body); }
    return fetch(url, opt).then(function (res) {
      clearTimeout(to); dropAbort(c);
      if (!res.ok) { var e = new Error("http"); e.status = res.status; throw e; }
      return res.json();
    }, function (err) { clearTimeout(to); dropAbort(c); throw err; });
  }

  /* ---- construct spec v0.1.0 (P0 addendum: zone REQUIRED; parts are module ids;
     rods stay empty — the task's tier_floor pins the tier server-side) ---- */
  function seatedParts() {
    var p = [];
    if (S.head) p.push(S.head);
    for (var i = 0; i < S.mid.length; i++) p.push(S.mid[i]);
    if (S.tail) p.push(S.tail);
    return p;
  }
  function specNow() {
    var parts = seatedParts(), wiring = [];
    for (var i = 0; i + 1 < parts.length; i++) wiring.push([parts[i], parts[i + 1]]);
    return { construct_version: "0.1.0", id: "c-01", parts: parts, wiring: wiring, rods: {}, policies: {}, zone: S.zone };
  }

  /* ================= DOM ================= */

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html !== undefined) n.innerHTML = html;
    return n;
  }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  function buildDom() {
    D.prompt = el("div", "", "F — THE BENCH");
    D.prompt.id = "bprompt";
    document.body.appendChild(D.prompt);

    D.wrap = el("div"); D.wrap.id = "bench";
    D.plate = el("div", "pan deep plate");
    D.plate.innerHTML =
      '<i class="ck tl"></i><i class="ck tr"></i><i class="ck bl"></i><i class="ck br"></i>' +
      '<div class="hd" style="--i:1"><span>THE BENCH · c-01</span><span class="lab s60" id="b-meter">WINDOW —s · QUOTA —</span></div>' +
      '<div class="rgn task" style="--i:2"><div class="t-line" id="b-task"></div><div class="t-check">' + esc(TASK.check) + "</div></div>" +
      '<div class="spine" id="b-spine" style="--i:3"></div>' +
      '<div class="strip" id="b-strip"></div>' +
      '<div class="railwrap" id="b-rail" style="--i:4"></div>' +
      '<div class="rider" style="--i:5"><span id="b-lastbest">LAST —.——s · BEST —.——s</span><span id="b-zone"></span></div>' +
      '<div class="runlog" id="b-log" style="--i:6"></div>' +
      '<div class="ctl-line" style="--i:7"><span class="k" id="b-run"></span>' +
      '<span class="k" id="b-clear">CLEAR <b>[HOLD C]</b><svg id="b-cring" width="14" height="14" viewBox="0 0 14 14">' +
      '<circle cx="7" cy="7" r="5.5" fill="none" stroke="rgba(120,155,175,1)" stroke-width="1.5" stroke-dasharray="34.56" stroke-dashoffset="34.56" transform="rotate(-90 7 7)"></circle></svg></span>' +
      '<span class="k">EXIT <b>[F]</b></span></div>';
    D.wrap.appendChild(D.plate);
    document.body.appendChild(D.wrap);

    D.meter = D.plate.querySelector("#b-meter");
    D.task = D.plate.querySelector("#b-task");
    D.spine = D.plate.querySelector("#b-spine");
    D.strip = D.plate.querySelector("#b-strip");
    D.rail = D.plate.querySelector("#b-rail");
    D.lastbest = D.plate.querySelector("#b-lastbest");
    D.zone = D.plate.querySelector("#b-zone");
    D.log = D.plate.querySelector("#b-log");
    D.runchip = D.plate.querySelector("#b-run");
    D.cring = D.plate.querySelector("#b-cring").firstChild;

    /* right-click is UNSEAT grammar, never the browser menu, plate-wide (E4 §6) */
    listen(D.plate, "contextmenu", function (e) { e.preventDefault(); });
  }

  /* ---- run log: four lines, receipts land as they happen (E4 §5 — 04 §5 tier 1 depth) ---- */
  function logLine(text, hot) {
    var n = el("div", "ln" + (hot ? " hotln" : ""), esc(text));
    D.log.appendChild(n);
    while (D.log.children.length > 4) D.log.removeChild(D.log.firstChild);
  }
  function receipt(text) { logLine("> " + text); }

  /* ---- renders (every displayed value recomputed from state at render — 04 §0) ---- */
  function zoneWord() { return S.zone.toUpperCase(); }

  function renderHeader() {
    if (S.grid === false) { D.meter.textContent = "CARRIER LOST"; return; }
    if (!S.grid) { D.meter.textContent = "WINDOW —s · QUOTA —"; return; }
    /* /state exposes the live rpm fraction, not window seconds — the fraction is the
       REAL number so it is what prints (honesty law over the letter; seconds need a
       /state field that does not exist yet) */
    D.meter.textContent = "WINDOW " + S.grid.win + " · QUOTA " + S.grid.quota + " LIVE";
  }

  function renderTask() {
    D.task.textContent = "TASK  " + TASK.line + " · ZONE " + zoneWord();
    D.zone.textContent = "ZONE " + zoneWord();
  }

  function renderRider() {
    var f = function (ms) { return ms === null ? "—.——s" : (ms / 1000).toFixed(2) + "s"; };
    D.lastbest.textContent = "LAST " + f(S.last) + " · BEST " + f(S.best);
    D.zone.textContent = "ZONE " + zoneWord();
  }

  function chipHtml(id, ghost) {
    var p = PARTS[id];
    return '<span class="glyph ' + (p.glyph === "pent" ? "pent" : "") + '"></span>' +
      '<span class="nm">' + p.nm + "</span>" +
      (ghost ? "" : '<span class="st" data-part="' + id + '">' + esc(chipStat(id)) + "</span>");
  }
  function chipStat(id) {
    var g = S.grid;
    if (id === "tap") return "PLANTS " + (g ? g.online + "/" + PLANT_TOTAL : "—/—");
    if (id === "scaffold") return "—";                       /* no live template source at P0 */
    if (id === "governor") return g && g.rpm ? g.rpm + "RPM" : "—/—RPM";
    if (id === "ladder") return "RODS " + (g ? g.rods : "—");
    if (id === "scorer") return "4 AXES";
    return "";
  }

  /* gap list actually rendered, in spine order — the cursor walks THIS list */
  function gapList() {
    var gaps = [];
    if (!S.head) gaps.push({ t: "head" });
    if (S.ghost && PARTS[S.ghost].slot === "mid") {
      for (var i = 0; i <= S.mid.length; i++) gaps.push({ t: "mid", i: i });
    } else if (S.mid.length === 0) {
      gaps.push({ t: "mid", i: 0 });   /* the virgin plate's middle break in the hairline */
    }
    if (!S.tail) gaps.push({ t: "tail" });
    return gaps;
  }

  function renderSpine() {
    var gaps = gapList();
    if (S.cursor >= gaps.length) S.cursor = Math.max(0, gaps.length - 1);
    D.spine.innerHTML = "";
    D.spine.appendChild(el("span", "end", "GRID"));
    D.spine.appendChild(el("span", "wire trunk"));

    var gi = 0;
    function gapNode(g) {
      var idx = gi++;
      var n = el("span", "gap" + (idx === S.cursor ? " cur" : ""));
      if (S.ghost && idx === S.cursor) { n.className += " holds"; n.innerHTML = '<span class="chip ghost">' + chipHtml(S.ghost, true) + "</span>"; }
      n.onclick = function () { S.cursor = idx; seatAttempt(g); };
      return n;
    }
    function chipNode(id, slotRef) {
      var selected = S.sel && S.sel.t === slotRef.t && S.sel.i === slotRef.i;
      var n = el("span", "chip seated" + (selected ? " sel" : ""), chipHtml(id, false));
      if (S.failTick && S.failTick.t === slotRef.t && S.failTick.i === slotRef.i) n.appendChild(el("i", "ftick"));
      n.onclick = function () { selectSeat(slotRef, id); };
      n.oncontextmenu = function (e) { e.preventDefault(); unseat(slotRef, id); };
      return n;
    }

    if (S.head) D.spine.appendChild(chipNode(S.head, { t: "head", i: 0 }));
    else D.spine.appendChild(gapNode({ t: "head" }));
    D.spine.appendChild(el("span", "wire"));

    var midGaps = gaps.filter(function (g) { return g.t === "mid"; });
    if (midGaps.length) {
      /* interleave: gap(0) mid[0] gap(1) mid[1] ... (only the ghost-legal gaps render) */
      var withInserts = S.ghost && PARTS[S.ghost].slot === "mid";
      for (var i = 0; i <= S.mid.length; i++) {
        if (withInserts || (S.mid.length === 0 && i === 0)) {
          D.spine.appendChild(gapNode({ t: "mid", i: i }));
          if (i < S.mid.length) D.spine.appendChild(el("span", "wire"));
        }
        if (i < S.mid.length) {
          D.spine.appendChild(chipNode(S.mid[i], { t: "mid", i: i }));
          D.spine.appendChild(el("span", "wire"));
        }
      }
      if (!withInserts && S.mid.length === 0) D.spine.appendChild(el("span", "wire"));
    } else {
      for (var m = 0; m < S.mid.length; m++) {
        D.spine.appendChild(chipNode(S.mid[m], { t: "mid", i: m }));
        D.spine.appendChild(el("span", "wire"));
      }
    }

    if (S.tail) D.spine.appendChild(chipNode(S.tail, { t: "tail", i: 0 }));
    else D.spine.appendChild(gapNode({ t: "tail" }));
    D.spine.appendChild(el("span", "wire trunk"));
    D.spine.appendChild(el("span", "end", "&gt; RECORD"));
  }

  function renderRail() {
    D.rail.innerHTML = '<span class="lab s60 railtag">PARTS</span>';
    RAIL.forEach(function (id, i) {
      var seatedNow = S.head === id || S.tail === id || S.mid.indexOf(id) >= 0;
      var n = el("span", "chip rchip" + (seatedNow ? " onspine" : "") + (S.ghost === id ? " picked" : ""),
        '<span class="idx">' + (i + 1) + "</span>" + chipHtml(id, false));
      n.onclick = function () { pick(id); };
      D.rail.appendChild(n);
    });
  }

  function renderCtl() {
    if (S.state === "RUN") { D.runchip.innerHTML = 'PLATE LOCKED — RUN LIVE'; D.runchip.classList.add("live"); return; }
    D.runchip.classList.remove("live");
    if (S.state === "HALT") { D.runchip.innerHTML = "RUN — HALTED"; return; }  /* true state, amber withdrawn */
    if (S.head !== "tap") D.runchip.innerHTML = "RUN — NO TAP, NO DRAW";
    else if (S.tail !== "scorer") D.runchip.innerHTML = "RUN — UNSCORED · NO RECORD WITHOUT SCORER";
    else D.runchip.innerHTML = "RUN <b>[SPACE]</b> · EST 1u";  /* one draw part in the pool: TAP */
  }

  function renderStrip() {
    if (!S.strip || !S.sel || seatId(S.sel) !== "tap") { D.strip.style.display = "none"; D.strip.innerHTML = ""; S.strip = false; return; }
    /* THE P0-CUT item 3: the strip ships for TAP only — the one writable (the zone law) */
    D.strip.style.display = "block";
    D.strip.innerHTML =
      '<div class="ln">TAP — POWER INLET · WRAPS energy.draw</div>' +
      '<div class="ln">&gt; zone: <span class="zval">' + zoneWord() + '</span> · <span class="lab s60">[ / ] CYCLES · PUBLIC IS EXPLICIT</span></div>' +
      '<div class="ln">&gt; tier: pinned by task tier_floor · local/keyless</div>' +
      '<div class="ln">&gt; prompt_source: task ' + TASK.id + "</div>";
  }

  function renderAll() {
    renderHeader(); renderTask(); renderSpine(); renderRail(); renderRider(); renderCtl(); renderStrip();
  }

  /* ================= COMPOSE grammar ================= */

  function seatId(ref) {
    if (!ref) return null;
    if (ref.t === "head") return S.head;
    if (ref.t === "tail") return S.tail;
    return S.mid[ref.i] || null;
  }

  function pick(id) {
    if (S.state !== "COMPOSE") { lockRefuse(); return; }
    if (S.head === id || S.tail === id || S.mid.indexOf(id) >= 0) { receipt("the " + PARTS[id].nm + " is seated — X unseats"); return; }
    S.ghost = id;
    var gaps = gapList(), want = PARTS[id].slot;
    for (var i = 0; i < gaps.length; i++) if (gaps[i].t === want || (want === "mid" && gaps[i].t === "mid")) { S.cursor = i; break; }
    blip(520, 40);
    renderSpine(); renderRail();
  }

  function moveCursor(dir) {
    var gaps = gapList();
    if (!gaps.length) return;
    S.cursor = (S.cursor + dir + gaps.length) % gaps.length;
    renderSpine();
  }

  function seatAttempt(g) {
    if (S.state !== "COMPOSE") { lockRefuse(); return; }
    if (!S.ghost) return;
    var id = S.ghost, slot = PARTS[id].slot;
    if (g.t === "head" && slot !== "head") { receipt("the head holds the TAP — power enters first"); return; }
    if (g.t === "tail" && slot !== "tail") { receipt("the tail holds the SCORER — the measure closes the wire"); return; }
    if (g.t === "mid" && slot === "head") { receipt("a TAP holds the head — it is the power inlet"); return; }
    if (g.t === "mid" && slot === "tail") { receipt("a SCORER holds the tail — every task ends measured"); return; }
    if (g.t === "head") { S.head = id; receipt("seated TAP at the head"); }
    else if (g.t === "tail") { S.tail = id; receipt("seated SCORER at the tail"); }
    else { S.mid.splice(g.i, 0, id); receipt("seated " + PARTS[id].nm + " on the spine"); }
    S.ghost = null; S.cursor = 0;
    blip(520, 40);
    renderSpine(); renderRail(); renderCtl();
    /* seat closes the wire: hairlines redraw left-to-right 180ms (04 §0) */
    var ws = D.spine.querySelectorAll(".wire");
    for (var i = 0; i < ws.length; i++) ws[i].classList.add("draw");
  }

  function selectSeat(ref, id) {
    if (S.state !== "COMPOSE") { lockRefuse(); return; }
    S.sel = ref;
    S.strip = (id === "tap");
    blip(520, 40);
    renderSpine(); renderStrip();
  }

  function unseat(ref, id) {
    if (S.state !== "COMPOSE") { lockRefuse(); return; }
    if (ref.t === "head") S.head = null;
    else if (ref.t === "tail") S.tail = null;
    else S.mid.splice(ref.i, 1);
    if (S.sel && S.sel.t === ref.t && S.sel.i === ref.i) { S.sel = null; S.strip = false; }
    if (S.failTick && S.failTick.t === ref.t && S.failTick.i === ref.i) S.failTick = null;
    receipt("unseated " + PARTS[id].nm + " — returned to the rail");
    renderSpine(); renderRail(); renderCtl(); renderStrip();
  }

  function cycleZone(dir) {
    if (S.state !== "COMPOSE") { lockRefuse(); return; }
    if (!S.strip) return;   /* the dial lives on TAP's strip — public is an explicit act */
    var i = (ZONES.indexOf(S.zone) + dir + ZONES.length) % ZONES.length;
    S.zone = ZONES[i];
    receipt("zone set — " + zoneWord());
    renderTask(); renderRider(); renderStrip();
  }

  function clearPlate() {
    S.head = null; S.mid = []; S.tail = null;
    S.ghost = null; S.sel = null; S.strip = false; S.cursor = 0; S.failTick = null;
    blip(300, 80, 900);      /* rising blip at completion (04 §0) */
    receipt("plate cleared — parts returned to the rail");
    renderAll();
  }

  function lockRefuse() {
    /* in RUN all non-exit input is refused by the lock line (E4 §6): flare 120ms, decay */
    if (S.state !== "RUN") return;
    D.runchip.classList.remove("flare"); void D.runchip.offsetWidth;
    D.runchip.classList.add("flare");
  }

  /* ================= RUN — the live trace ================= */

  function fire() {
    if (S.state !== "COMPOSE") { lockRefuse(); return; }
    if (S.head !== "tap") { receipt("no power inlet — a construct draws through a TAP"); return; }
    S.strip = false; S.sel = null; S.failTick = null;
    renderStrip(); renderSpine();

    S.runCount++;
    var n = S.runCount;
    S.state = "RUN";
    S.run = { rid: null, n: n, t0: performance.now(), parts: seatedParts(), done: 0, liveAt: -1, tMs: 0, halted: false };
    renderCtl();
    logLine("RUN r-" + pad2(n) + " · T+0.00s");
    buildPacket();

    GameAPI.ignite(specNow(), TASK.id).then(function (j) {
      if (!S.run || S.run.n !== n) return;
      if (!j || j.ok === false || !(j.run_id || (j.run && j.run.run_id))) {
        /* the carrier ANSWERED with a refusal — the honesty seam, printed verbatim (j.refused) */
        receipt((j && (j.refused || j.error)) ? (j.refused || j.error) : "run refused — no run_id returned");
        endToCompose();
        return;
      }
      S.run.rid = j.run_id || j.run.run_id;
      schedulePoll();
    }, function (err) {
      if (!S.run || S.run.n !== n) return;
      if (err && err.status) {
        /* the carrier answered wrong — no run exists; the plate unlocks, the receipt stands */
        receipt("/game/ignite · HTTP " + err.status + " — NO RUN");
        endToCompose();
      } else carrierLost("POST /game/ignite unreachable");
    });
  }

  function pad2(n) { return (n < 10 ? "0" : "") + n; }

  function schedulePoll() {
    if (!S.run || !S.run.rid) return;
    var rid = S.run.rid, n = S.run.n;
    GameAPI.run(rid).then(function (j) {
      if (!S.run || S.run.n !== n) return;
      applyStatus(normalizeRun(j));
      if (S.run && S.run.n === n && !S.run.halted && S.state === "RUN")
        timer(setTimeout(schedulePoll, POLL_MS));
    }, function () {
      if (!S.run || S.run.n !== n) return;
      carrierLost("GET /game/run unreachable — RUN r-" + pad2(n) + " STATE UNKNOWN");
    });
  }

  function normalizeRun(j) {
    var r = (j && j.run) ? j.run : (j || {});
    /* the seam returns bench_core.run_status verbatim; this adapter maps its REAL fields onto the
       plate's render contract — link.state from the measured ok, verdict from the scorer's pass.
       Nothing is invented: a receipt DICT is folded to its measured one-liner (model · chars / PASS). */
    var links = (r.links || r.trace || []).map(function (L) {
      var rc = L.receipt;
      if (rc && typeof rc === "object") {
        if ("pass" in rc) rc = rc.pass ? "PASS" : "EXPECT MISSED";
        else if (rc.model) rc = (rc.plant ? rc.plant + "/" : "") + rc.model + (rc.chars != null ? " · " + rc.chars + " chars" : "");
        else rc = "DONE";
      }
      return { seq: L.seq, part: L.part, ms: L.ms, ok: L.ok, tried: L.tried, receipt: rc,
               state: L.state || (L.ok ? "DONE" : "FAIL") };
    });
    var verdict = r.verdict || ((r.pass !== undefined && r.pass !== null) ? { pass: !!r.pass } : null);
    return {
      state: String(r.state || r.status || "RUNNING").toUpperCase(),
      links: links,
      total_ms: (r.total_ms !== undefined) ? r.total_ms : null,
      cost_u: (r.cost_u !== undefined) ? r.cost_u : null,
      verdict: verdict,
      error: r.error || null
    };
  }

  /* packet stops: entry trunk, each chip center, exit — measured from the LOCKED layout */
  function buildPacket() {
    var chips = D.spine.querySelectorAll(".chip.seated");
    var wires = D.spine.querySelectorAll(".wire");
    var stops = [];
    stops.push(wires.length ? wires[0].offsetLeft + 2 : 0);                       /* entry: the left trunk */
    for (var i = 0; i < chips.length; i++) stops.push(chips[i].offsetLeft + chips[i].offsetWidth / 2);
    var lastW = wires[wires.length - 1];
    stops.push(lastW ? lastW.offsetLeft + lastW.offsetWidth - 2 : 0);             /* exit: the right trunk */
    S.run.stops = stops;
    S.run.chips = chips;
    S.run.wires = wires;

    var p = el("i", "packet"), t = el("span", "tplus", "T+0.00s");
    D.spine.appendChild(p); D.spine.appendChild(t);
    S.run.packetEl = p; S.run.tplusEl = t;
    packetTo(0);
  }

  function packetTo(stopIdx) {
    var r = S.run; if (!r || !r.packetEl) return;
    var x = r.stops[Math.min(stopIdx, r.stops.length - 1)];
    r.packetEl.style.left = x + "px";
    r.tplusEl.style.left = x + "px";
  }

  function glyphFire(i, on) {
    var r = S.run; if (!r || !r.chips || !r.chips[i]) return;
    var g = r.chips[i].querySelector(".glyph");
    if (g) g.classList[on ? "add" : "remove"]("fire");
  }

  function tName(ms) { return ms === null ? "T+—" : "T+" + (ms / 1000).toFixed(2) + "s"; }

  function applyStatus(run) {
    var r = S.run; if (!r) return;
    var links = run.links;

    /* the packet advances ONLY on real trace rows — never interpolated (E4 §8.2) */
    for (var i = r.done; i < links.length; i++) {
      var L = links[i] || {};
      var st = String(L.state || "").toUpperCase();
      var partNm = PARTS[L.part] ? PARTS[L.part].nm : String(L.part || "?").toUpperCase();
      if (st === "LIVE") {
        if (r.liveAt !== i) {
          r.liveAt = i;
          packetTo(i + 1);            /* sits ON the working part — hot, still (the wait IS the drama) */
          glyphFire(i, true);
        }
        break;                         /* nothing beyond the live link is real yet */
      }
      if (st === "DONE" || st === "PASS" || st === "OK") {
        if (r.liveAt === i) glyphFire(i, false);
        packetTo(i + 1);
        r.tMs += (typeof L.ms === "number" ? L.ms : 0);
        var cum = (typeof L.ms === "number") ? r.tMs : null;
        /* reroute marks: a fall-through on the draw renders as resilience, not failure
           (P0 addendum, the honest kill) */
        if (L.tried && L.tried.length > 1) {
          markReroutes(i, L.tried.length - 1);
          logLine("HOP " + (i + 1) + " · " + partNm + " · " + (L.tried.length - 1) + " DEAD · FELL THROUGH · " + tName(cum));
        }
        logLine("HOP " + (i + 1) + " · " + partNm + " · " + (L.receipt ? L.receipt : "DONE") + " · " + tName(cum));
        flareStat(i);
        blip(520, 40);
        r.done = i + 1;
        continue;
      }
      if (st === "FAIL") {
        haltAt(i, L, run);
        return;
      }
    }

    if (run.state === "FAIL" && !r.halted) {
      /* terminal fail with no located link row: the harness named the cause, not a wire */
      haltAt(Math.max(0, r.done), { part: r.parts[Math.max(0, r.done)], receipt: run.error || "REFUSED" }, run, true);
      return;
    }
    if (run.state === "PASS" || run.state === "DONE") {
      finishPass(run);
    }
  }

  function markReroutes(linkIdx, n) {
    var r = S.run;
    var wire = r.wires[Math.min(linkIdx + 1, r.wires.length - 1)];
    if (!wire) return;
    for (var k = 0; k < Math.min(n, 4); k++) {
      var m = el("i", "rr");
      m.style.left = (wire.offsetLeft + 6 + k * 7) + "px";
      D.spine.appendChild(m);
      if (!r.marks) r.marks = [];
      r.marks.push(m);
    }
  }

  function flareStat(i) {
    var r = S.run; if (!r.chips[i]) return;
    var stEl = r.chips[i].querySelector(".st");
    if (!stEl) return;
    stEl.classList.remove("vflare"); void stEl.offsetWidth;
    stEl.classList.add("vflare");    /* hot 120ms -> warm 600ms (attack/decay law) */
  }

  function finishPass(run) {
    var r = S.run;
    packetTo(r.stops.length - 1);
    var totalMs = (typeof run.total_ms === "number") ? run.total_ms : null;
    var cost = (run.cost_u !== null && run.cost_u !== undefined) ? run.cost_u : null;
    if (run.verdict && run.verdict.pass === false) {
      /* the scorer measured a miss — a located fail at the tail */
      haltAt(r.parts.length - 1, { part: "scorer", receipt: "EXPECT MISSED", ms: null }, run, false);
      return;
    }
    if (run.verdict) {
      logLine("r-" + pad2(r.n) + " · PASS · SPEED " + (totalMs !== null ? (totalMs / 1000).toFixed(2) + "s" : "—") +
        " · COST " + (cost !== null ? cost + "u" : "—") + " · ZONE " + zoneWord(), true);
      if (totalMs !== null) {
        S.last = totalMs;
        if (S.best === null || totalMs < S.best) S.best = totalMs;
      }
      if (!S.firstPass["c-01"]) { S.firstPass["c-01"] = true; firstRunRitual(); }
    } else {
      /* no scorer seated: the run ran, nothing measured it — the control line warned */
      logLine("r-" + pad2(r.n) + " DONE · UNSCORED · NO RECORD");
    }
    renderRider();
    endToCompose();
    refreshGrid();   /* the meter genuinely recovering is part of the truth (E4 §9) */
  }

  /* A CONSTRUCT'S FIRST RUN — the sanctioned ritual (E4 §8.4 [GRAFT-B3]): once per
     construct THIS SESSION; the once-EVER law completes at P1 with served history */
  function firstRunRitual() {
    var r = S.run; if (!r) return;
    sting();
    var order = [];
    for (var i = 0; i < r.parts.length; i++) if (r.parts[i] === "scaffold") order.push(i); /* pentagon first */
    for (var j = 0; j < r.parts.length; j++) if (r.parts[j] !== "scaffold") order.push(j); /* circles in wire order */
    order.forEach(function (idx, k) {
      timer(setTimeout(function () {
        var c = r.chips && r.chips[idx]; if (!c) return;
        c.classList.add("ritual");
        timer(setTimeout(function () { c.classList.remove("ritual"); }, 260));
      }, k * 120));
    });
  }

  /* ---- FAILURE: instant, located, HELD (E4 §9 [GRAFT-A3]) ---- */
  function haltAt(linkIdx, L, run, unlocated) {
    var r = S.run; if (!r || r.halted) return;
    r.halted = true;
    var partId = L.part || r.parts[linkIdx];
    var partNm = PARTS[partId] ? PARTS[partId].nm : String(partId || "?").toUpperCase();

    /* the packet stops ON the wire where it died and cools in place, 900ms */
    var wire = r.wires[Math.min(linkIdx + 1, r.wires.length - 1)];
    if (wire && r.packetEl) {
      var x = wire.offsetLeft + wire.offsetWidth / 2;
      r.packetEl.style.left = x + "px";
      r.tplusEl.style.left = x + "px";
      r.packetEl.classList.add("cool");
      var w = el("i", "wmark", "x");
      w.style.left = x + "px";
      D.spine.appendChild(w);
      r.wmark = w;
    }
    var cum = (typeof L.ms === "number") ? (r.tMs + L.ms) : null;
    receipt("HALTED AT " + partNm + " · " + (L.receipt || run.error || "FAILED") + " · " + tName(cum));
    receipt("r-" + pad2(r.n) + " APPENDED · FAILED AT HOP " + (linkIdx + 1) + " · COST " +
      ((run.cost_u !== null && run.cost_u !== undefined) ? run.cost_u : "—") + "u");

    /* everything eases to 0.35; the failing name holds at 1.0 (failure = amber withdrawn) */
    S.state = "HALT";
    D.plate.classList.add("halt");
    if (r.chips && r.chips[linkIdx]) r.chips[linkIdx].classList.add("fail");
    glyphFire(linkIdx, false);
    if (r.tplusEl) r.tplusEl.classList.add("cool");   /* the light goes out of the counter too */
    renderCtl();

    /* the failed seat keeps a structure tick for the visit (settled story cools) */
    var seatRef = seatRefOfIndex(linkIdx);
    if (seatRef) S.failTick = seatRef;
    /* frame HOLDS until any input. no sound but the hum — silence is the failure sting. */
  }

  function seatRefOfIndex(i) {
    var idx = 0;
    if (S.head) { if (i === idx) return { t: "head", i: 0 }; idx++; }
    for (var m = 0; m < S.mid.length; m++) { if (i === idx) return { t: "mid", i: m }; idx++; }
    if (S.tail && i === idx) return { t: "tail", i: 0 };
    return null;
  }

  function carrierLost(why) {
    /* honest on fetch failure: the game cannot see the entity and says exactly that (A10) */
    receipt("CARRIER LOST — " + why);
    S.grid = false;
    renderHeader();
    endToCompose();
  }

  function endToCompose() {
    teardownTrace(false);
    S.run = null;
    S.state = "COMPOSE";
    renderCtl();
  }

  function haltRelease() {
    /* any input returns to COMPOSE (E4 §9) — the held frame ends, the tick survives */
    D.plate.classList.remove("halt");
    teardownTrace(true);
    S.run = null;
    S.state = "COMPOSE";
    renderSpine(); renderCtl();
  }

  function teardownTrace(keepNothing) {
    var r = S.run; if (!r) return;
    if (r.packetEl && r.packetEl.parentNode) r.packetEl.parentNode.removeChild(r.packetEl);
    if (r.tplusEl && r.tplusEl.parentNode) r.tplusEl.parentNode.removeChild(r.tplusEl);
    if (r.wmark && r.wmark.parentNode) r.wmark.parentNode.removeChild(r.wmark);
    if (r.marks) r.marks.forEach(function (m) { if (m.parentNode) m.parentNode.removeChild(m); });
    if (r.chips) for (var i = 0; i < r.chips.length; i++) r.chips[i].classList.remove("fail", "ritual");
  }

  /* ================= /state — the real meter (dashes when unknown, never invented) ================= */

  function refreshGrid() {
    if (S.still) return;   /* the harness still is deterministic: no network, dashes stand */
    GameAPI.state().then(function (j) {
      var plants = (j && j.energy && j.energy.plants) || [];
      var quota = 0, hasCap = false;
      plants.forEach(function (p) { if (p.rpd_cap) { hasCap = true; quota += Math.max(0, p.rpd_cap - (p.rpd || 0)); } });
      var kp = null;
      for (var i = 0; i < plants.length; i++) if (plants[i].plant === "pollinations") kp = plants[i];
      var rods = ((j && j.energy && j.energy.rods) || []).filter(function (r) { return !r.cooling; }).length;
      S.grid = {
        online: plants.length,
        win: kp ? (kp.rpm_now || 0) + "/" + (kp.rpm_cap || "—") : "—/—",
        rpm: kp ? (kp.rpm_now || 0) + "/" + (kp.rpm_cap || "—") : null,
        quota: hasCap ? quota : "—",
        rods: rods
      };
      renderHeader(); renderRail();
    }, function () {
      S.grid = false;
      renderHeader(); renderRail();
    });
  }

  /* ================= dock / undock ================= */

  function dock() {
    if (S.docked) return;
    S.docked = true;
    camOn = true;
    D.prompt.style.display = "none";
    var hints = document.getElementById("hints");
    if (hints) hints.style.display = "none";   /* the plate admits no navigation chrome (E4 §13) */

    /* flight keys captured while docked: release any held movement so the probe settles —
       the engine owns its key map; synthetic keyups speak to it through its own listener */
    ["w", "a", "s", "d", "q", "e"].forEach(function (k) {
      window.dispatchEvent(new KeyboardEvent("keyup", { key: k }));
    });

    D.wrap.classList.add("on");
    D.plate.classList.remove("closing", "deal");
    void D.plate.offsetWidth;
    D.plate.classList.add("deal");             /* brackets 140ms · rows 160ms @30ms stagger (04 §0) */
    blip(520, 40);
    humStart();                                 /* 55Hz gain 0.05 while docked (04 §0, E4 extension) */
    renderAll();
    refreshGrid();
  }

  function undock() {
    if (!S.docked) return;
    S.docked = false;
    camOn = false;                              /* chaseCam resumes and eases home by itself */
    humStop();
    blip(520, 40);
    D.plate.classList.remove("deal");
    D.plate.classList.add("closing");           /* 200ms fade+scale(.98) — close beats open */
    timer(setTimeout(function () {
      if (!S.docked) { D.wrap.classList.remove("on"); D.plate.classList.remove("closing"); }
    }, 210));
    var hints = document.getElementById("hints");
    if (hints) hints.style.display = "";
    /* a live run continues server-side; the poller keeps its own life (run contract) */
  }

  function escCascade() {
    if (S.strip) { S.strip = false; S.sel = null; renderStrip(); renderSpine(); return; }
    undock();
  }

  /* ================= input (capture phase: the plate owns keys while docked) ================= */

  function onKeyDown(e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (!S.docked) {
      if (!S.live) { S.live = true; return; }   /* first key wakes flight (engine consumes it too) */
      if ((e.key === "f" || e.key === "F") && S.near && !S.still) {
        e.stopPropagation(); e.preventDefault();
        dock();
      }
      return;
    }

    /* DOCKED: flight never sees keys; M/K/C-as-comms and every OS verb are inert (E4 §6) */
    e.stopPropagation();
    var k = e.key;

    if (k === "f" || k === "F" || k === "Escape") { e.preventDefault(); escCascade(); return; }

    if (S.state === "HALT") { e.preventDefault(); haltRelease(); return; }
    if (S.state === "RUN") { e.preventDefault(); lockRefuse(); return; }

    /* COMPOSE */
    if (k >= "1" && k <= "5") { e.preventDefault(); pick(RAIL[+k - 1]); return; }
    if (k === "ArrowLeft") { e.preventDefault(); moveCursor(-1); return; }
    if (k === "ArrowRight") { e.preventDefault(); moveCursor(1); return; }
    if (k === "Enter") { e.preventDefault(); var g = gapList()[S.cursor]; if (g && S.ghost) seatAttempt(g); return; }
    if (k === "x" || k === "X") { e.preventDefault(); if (S.sel) unseat(S.sel, seatId(S.sel)); return; }
    if (k === "[") { e.preventDefault(); cycleZone(-1); return; }
    if (k === "]") { e.preventDefault(); cycleZone(1); return; }
    if (k === " ") { e.preventDefault(); if (!e.repeat) fire(); return; }
    if ((k === "c" || k === "C") && !e.repeat) { e.preventDefault(); holdStart(); return; }
  }

  function onKeyUp(e) {
    /* keyups pass through even docked — the engine must clear its own held keys */
    if ((e.key === "c" || e.key === "C") && S.hold && !S.hold.drain) holdRelease();
  }

  function onMouseDown(e) {
    if (!S.docked) return;
    if (D.plate.contains(e.target)) {
      if (S.state === "HALT") { haltRelease(); return; }   /* any input ends the held frame */
      return;                                               /* plate clicks reach their chips */
    }
    e.stopPropagation();                                    /* drag-look suspended with flight */
    if (S.state === "HALT") haltRelease();
  }

  function onWheel(e) {
    if (S.docked) e.stopPropagation();                      /* wheel is flight grammar — inert */
  }

  function onBlur() {
    if (S.hold && !S.hold.drain) holdRelease();             /* a lost keyup never wedges the ring */
  }

  /* ---- HOLD C — the one destructive act: 600ms ring, release-early drains 150ms (04 §0) ---- */
  var RING = 34.56;
  function holdStart() {
    if (S.state !== "COMPOSE") { lockRefuse(); return; }
    if (S.hold) return;
    S.hold = { t0: performance.now(), drain: false };
    D.cring.parentNode.parentNode.classList.add("holding");
  }
  function holdRelease() {
    if (!S.hold) return;
    var p = Math.min(1, (performance.now() - S.hold.t0) / 600);
    S.hold = { drain: true, drainFrom: p, drainT0: performance.now() };
  }
  function holdFrame() {
    if (!S.hold) return;
    var p;
    if (S.hold.drain) {
      p = S.hold.drainFrom * (1 - (performance.now() - S.hold.drainT0) / 150);
      if (p <= 0) { holdEnd(0); return; }
    } else {
      p = Math.min(1, (performance.now() - S.hold.t0) / 600);
      if (p >= 1) { clearPlate(); holdEnd(0); return; }
    }
    D.cring.style.strokeDashoffset = String(RING * (1 - p));
  }
  function holdEnd() {
    S.hold = null;
    D.cring.style.strokeDashoffset = String(RING);
    var host = D.cring.parentNode.parentNode;
    host.classList.remove("holding");
  }

  /* ================= per-frame (registered via GAME.onFrame, released in dispose) ================= */

  var v3 = null;
  function frame(dt) {
    var eng = GAME.state.engine;
    if (!eng) return;

    /* proximity from the engine's own probe — read, never tracked twice (E1 §2.2) */
    if (!S.still) {
      if (!probeRef) probeRef = eng.scene.getObjectByName("probe");
      if (probeRef) {
        var dx = probeRef.position.x - SLAB.x, dz = probeRef.position.z - SLAB.z;
        S.near = (dx * dx + dz * dz) <= RANGE * RANGE;
      }
      /* the prompt stands above the slab, in the world's own projection (E4 §4) */
      if (!S.docked && S.near) {
        if (!v3) v3 = new THREE.Vector3();
        v3.set(SLAB.x, SLAB.y + 3.2, SLAB.z).project(eng.camera);
        if (v3.z < 1) {
          D.prompt.style.display = "block";
          D.prompt.style.left = ((v3.x * 0.5 + 0.5) * window.innerWidth) + "px";
          D.prompt.style.top = ((-v3.y * 0.5 + 0.5) * window.innerHeight) + "px";
        } else D.prompt.style.display = "none";
      } else D.prompt.style.display = "none";
    }

    /* dock camera: one damped move to the fixed high oblique, then stillness (A11 §6.6).
       Runs after chaseCam in the frame order, so the override is total while docked. */
    if (camOn && !S.still) {
      var k = 1 - Math.exp(-9 * dt);
      eng.camera.position.lerp(CAM.pos, dt === 0 ? 1 : k);
      eng.camera.lookAt(CAM.look);
    }

    /* T+ live readout: real elapsed wall-clock while the run lives — the counter IS the
       animation; the packet itself moves only on real rows (E4 §8.2) */
    if (S.state === "RUN" && S.run && S.run.tplusEl) {
      S.run.tplusEl.textContent = "T+" + ((performance.now() - S.run.t0) / 1000).toFixed(2) + "s";
    }

    holdFrame();
  }

  /* ================= init / dispose ================= */

  function init(game) {
    try {
      GAME = game;
      S.still = !!GAME.state.flags.still;
      var q = new URLSearchParams(location.search);
      S.benchBoot = q.get("bench") === "1";

      buildDom();
      renderAll();

      listen(window, "keydown", onKeyDown, true);   /* capture: the plate wins while docked */
      listen(window, "keyup", onKeyUp, true);
      listen(window, "mousedown", onMouseDown, true);
      listen(window, "wheel", onWheel, true);
      listen(window, "blur", onBlur);

      GAME.onFrame(frame);

      /* ?still&bench=1 — the docked virgin plate, deterministic (no network), for the harness (E4 §13).
         ?bench=1 (live, no ?still) — the same docked plate WITH the network up, so a headless verify can
         seat + IGNITE a real run without first flying to a beacon. The ignition itself is 100% real. */
      if (S.benchBoot) {
        S.docked = true;
        var eng = GAME.state.engine;
        if (eng) { eng.camera.position.copy(CAM.pos); eng.camera.lookAt(CAM.look); }
        D.wrap.classList.add("on");
        D.plate.classList.add("deal");
        renderAll();
        if (!S.still) refreshGrid();   /* live: pull the real meter into the header */
      }
    } catch (err) {
      /* module init failures reach #err, never vanish in a promise (E1 §5) */
      var e = document.getElementById("err");
      if (e) { e.textContent = "ERR BENCH INIT " + (err && err.message); e.style.display = "block"; }
      throw err;
    }
  }

  function dispose() {
    /* E1 §3.1 in order: frame hook, fetches, timers, listeners, audio, DOM, refs */
    GAME.offFrame(frame);
    R.aborts.forEach(function (c) { try { c.abort(); } catch (e) { } });
    R.timers.forEach(function (id) { clearTimeout(id); });
    R.listeners.forEach(function (l) { l[0].removeEventListener(l[1], l[2], l[3]); });
    R.aborts.length = R.timers.length = R.listeners.length = 0;
    humStop();
    if (AC) { try { AC.close(); } catch (e) { } AC = null; }
    if (D.wrap && D.wrap.parentNode) D.wrap.parentNode.removeChild(D.wrap);
    if (D.prompt && D.prompt.parentNode) D.prompt.parentNode.removeChild(D.prompt);
    var hints = document.getElementById("hints");
    if (hints) hints.style.display = "";
    D = {}; probeRef = null; camOn = false;
    S.docked = false; S.run = null;
    GAME = null;
  }

  return { init: init, dispose: dispose };
})();
