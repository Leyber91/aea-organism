/* mission.js — THE MISSION ENGINE (STAGE 1, the vertical slice's missing system).
   A faithful PORT of world.html's runBeat() state machine (NOT a general framework — a data-driven
   RUNNER). It reads ONE mission JSON and drives its beats over the already-merged flight/dock/bench,
   gating every DO/PROVE on a REAL system event — nothing here is simulated (the honesty law).

   Locked at the STAGE-1 studio standup (2026-07-24, wf_9d73037c):
   - ONE-WAY DEPENDENCY: mission.js reads ONLY GAME.bus + /game/* HTTP. It never touches bench internals
     (S.run/S.run.rid); bench.js never imports mission.js. The bus is the only cross-module channel (E1 §2.2).
   - STAGE-1 beat kinds = exactly { brief, learn, do, prove }. The real bench fire IS the observation, so
     'observe' is NOT ported; the reveal is a completeMission reward, not a beat.
   - TWO-TIER DO GATE: the DO wait resolves on ANY terminal event (pass true|false|null | refused) so the
     card always gives located feedback and never hangs — but it ADVANCES to PROVE only on run:done
     pass===true. A miss re-arms at DO with a re-seat/re-fire nudge.
   - PROVE re-reads GET /game/run?id= ITSELF and asserts the REAL body: tap+scorer receipts truthy,
     verdict.pass===true, state settled, links non-empty. The HTTP body is the authority, never the event.
   - cost_u is tri-state everywhere: 0 -> FREE, positive -> Nu, null -> a dash. Never coerced.
   - Amber only on the earned PASS chip; two-ink otherwise. NO EMOJI. prefers-reduced-motion honored. */
window.MISSION = (function () {
  "use strict";

  var GAME = null;
  var RM = false;
  var M = null;                          /* the loaded mission object (DATA) */
  var BI = 0;
  var mode = "idle";                     /* idle | talk | do | prove | done */
  var awaiting = false;                  /* DO beat: armed, listening for a terminal run event */
  var doBeat = null;                     /* the current DO beat (for its located nudge lines) */
  var lastRun = null;                    /* the last run:done payload (carries the real run_id) */
  var typingTimer = null;
  var started = false;
  var D = {};
  /* THE GUIDED LADDER (the levels, chained as DATA): rung 0 the bare draw, rung 1 the reach/stake. Each is
     a mission JSON run by this one engine; the loader advances on mission complete. Rungs 2-7 are FOG until
     their parts are forged (audit 2026-07-24) — never listed here before the machinery is real. */
  var SEQ = ["m01_first_light.json", "m02_the_stake.json", "m03_the_ward.json", "m04_the_threshold.json"];
  var seqIdx = 0;

  /* THE DISTRICTS — where each rung stands in the instrument. The world is centred on the core at
     (0,26) with the privacy rings at r = 26 + i*27, so these are real places on the real map: the
     heart, the protected inner ring, and the rim where the paid reach lives. The arc becomes a
     passage — in to the mouth, out to the rim, back inside the ring, out to the threshold. */
  var DISTRICTS = {
    core: { x: 0,   z: 26,  nm: "THE CORE" },
    ring: { x: -46, z: 0,   nm: "THE INNER RING" },
    rim:  { x: 40,  z: 95,  nm: "THE RIM" }
  };
  var here = null;          /* the district this rung stands in */
  var travelHook = null;    /* the live distance readout during the DO beat */

  /* ---------- tri-state helpers (honesty grammar) ---------- */
  function costWord(c) { return c === 0 ? "FREE" : (c == null ? "—" : c + "u"); }
  function msWord(ms) { return ms == null ? "—" : Math.round(ms); }
  function fill(tmpl, run) {
    run = run || {};
    return String(tmpl == null ? "" : tmpl)
      .replace(/\{run_id\}/g, run.run_id || "—")
      .replace(/\{total_ms\}/g, msWord(run.total_ms))
      .replace(/\{cost_u\}/g, costWord(run.cost_u));
  }

  /* ---------- scoped chrome (reuses probe.css tokens — two-ink, never a new palette) ---------- */
  function style() {
    var css =
      "#mhud{position:fixed;left:16px;top:14px;z-index:40;max-width:360px;pointer-events:none;" +
      "font-family:'IBM Plex Mono',Consolas,monospace;font-variant-numeric:tabular-nums}" +
      "#mhud .m-id{font-size:10px;text-transform:uppercase;letter-spacing:.14em;color:var(--s60)}" +
      "#mhud .m-title{font-size:13px;color:var(--s100);margin-top:3px}" +
      "#mhud .m-obj{font-size:11px;color:var(--s60);margin-top:5px;line-height:1.55}" +
      "#mhud .m-obj.act{color:var(--s100)}" +
      "#mhud .m-tag{font-size:10px;text-transform:uppercase;letter-spacing:.14em;color:var(--s35);margin-top:7px}" +
      "#mhud .m-tag.pass{color:var(--warm)}" +
      "#mterm{position:fixed;right:24px;top:50%;transform:translateY(-50%);z-index:41;width:520px;max-width:calc(100vw - 48px);" +
      "display:none;pointer-events:none;background:var(--pan-deep);border:1px solid var(--rule);" +
      "font-family:'IBM Plex Mono',Consolas,monospace;font-variant-numeric:tabular-nums;color:var(--s100)}" +
      "#mterm.open{display:block;pointer-events:auto}" +
      "#mterm .m-head{font-size:10px;text-transform:uppercase;letter-spacing:.14em;color:var(--s100);" +
      "padding:11px 16px;border-bottom:1px solid var(--rule)}" +
      "#mterm .m-body{padding:14px 16px;font-size:13px;line-height:1.6;white-space:pre-wrap;min-height:64px;max-height:52vh;overflow:auto}" +
      "#mterm .m-body .code{color:var(--s60);display:block;margin:8px 0;padding-left:10px;border-left:1px solid var(--rule);white-space:pre-wrap}" +
      "#mterm .m-body .note{color:var(--s60);display:block;margin-top:8px}" +
      "#mterm .m-body .res{color:var(--s100);display:block;margin-top:10px}" +
      "#mterm .m-body .passchip{color:var(--warm);letter-spacing:.1em;margin-right:8px}" +
      "#mterm .m-body .failtx{color:var(--s100)}" +
      "#mterm .m-foot{display:flex;gap:8px;padding:11px 16px;border-top:1px solid var(--rule)}" +
      "#mterm .mbtn{font:inherit;font-size:11px;text-transform:uppercase;letter-spacing:.12em;cursor:pointer;" +
      "background:transparent;color:var(--s60);border:1px solid var(--rule);padding:6px 14px}" +
      /* the primary action reads as EMPHASIS, not amber: amber is the fired/earned state only, never chrome
         (gap review 2026-07-24 — the solid-amber button was the largest unearned amber mass on the plate) */
      "#mterm .mbtn.hot{color:var(--s100);background:rgba(255,255,255,.035);border-color:var(--s60)}";
    var s = document.createElement("style"); s.id = "mission-css"; s.textContent = css;
    document.head.appendChild(s);
  }

  function build() {
    var hud = document.createElement("div"); hud.id = "mhud";
    hud.innerHTML = '<div class="m-id"></div><div class="m-title"></div><div class="m-obj"></div><div class="m-tag"></div>';
    document.body.appendChild(hud);
    var term = document.createElement("div"); term.id = "mterm";
    term.innerHTML = '<div class="m-head"></div><div class="m-body"></div><div class="m-foot"></div>';
    document.body.appendChild(term);
    D.hud = hud; D.term = term;
    D.id = hud.querySelector(".m-id"); D.title = hud.querySelector(".m-title");
    D.obj = hud.querySelector(".m-obj"); D.tag = hud.querySelector(".m-tag");
    D.head = term.querySelector(".m-head"); D.body = term.querySelector(".m-body"); D.foot = term.querySelector(".m-foot");
  }

  /* ---------- terminal helpers ---------- */
  function openTerm() { mode = (mode === "prove") ? "prove" : "talk"; D.term.classList.add("open"); }
  function closeTerm() { D.term.classList.remove("open"); if (typingTimer) { clearTimeout(typingTimer); typingTimer = null; } }
  function foot(btns) {
    D.foot.innerHTML = "";
    btns.forEach(function (b) {
      var el = document.createElement("button");
      el.className = "mbtn" + (b.hot ? " hot" : "");
      el.textContent = b.label;
      el.onclick = function () { b.fn(el); };
      D.foot.appendChild(el);
    });
  }
  function typeInto(el, text, cps, then) {
    if (RM) { el.textContent = text; if (then) then(); return; }
    var i = 0, n = text.length;
    (function step() {
      if (i <= n) { el.textContent = text.slice(0, i); i += 2; typingTimer = setTimeout(step, cps || 12); }
      else { typingTimer = null; if (then) then(); }
    })();
  }

  /* ---------- HUD ---------- */
  function setHud(objText, act) {
    if (!M) return;
    D.id.textContent = "ACT " + M.act + " · " + M.id;
    D.title.textContent = M.title;
    D.obj.textContent = objText || M.objective || "";
    D.obj.className = "m-obj" + (act ? " act" : "");
  }
  function setTag(text, pass) { D.tag.textContent = text || ""; D.tag.className = "m-tag" + (pass ? " pass" : ""); }

  /* ---------- the beat runner (PORT of runBeat) ---------- */
  function runBeat() {
    if (!M) return;
    var b = M.beats[BI];
    if (!b) { completeMission(); return; }
    D.head.textContent = M.id + " · " + (b.title || M.title);
    D.body.innerHTML = "";
    var span = document.createElement("span"); D.body.appendChild(span);
    var next = function () { BI++; if (BI >= M.beats.length) completeMission(); else runBeat(); };

    if (b.kind === "brief" || b.kind === "ask") {
      openTerm(); foot([]);
      typeInto(span, (b.lines || []).join("\n"), 12, function () { foot([{ label: "continue", hot: true, fn: next }]); });

    } else if (b.kind === "learn") {
      openTerm();
      span.textContent = "· " + (b.title || "") + "\n";
      var code = document.createElement("span"); code.className = "code"; D.body.appendChild(code);
      var note = document.createElement("span"); note.className = "note"; D.body.appendChild(note);
      foot([]);
      typeInto(code, b.code || "", 6, function () { note.textContent = b.note || ""; foot([{ label: "continue", hot: true, fn: next }]); });

    } else if (b.kind === "do") {
      /* HANDS-OFF: close the modal, release the keys to the bench, light the objective, ARM.
         The player composes for real. bench.js emits the terminal event; we never fire it ourselves. */
      closeTerm(); mode = "do"; awaiting = true; lastRun = null; doBeat = b;
      setHud(b.label || "dock the core · seat THE DRAW + THE MEASURE · fire", true);
      setTag("awaiting a real draw", false);
      startTravel();     /* the distance to the district counts down as you actually fly it */

    } else if (b.kind === "prove") {
      mode = "prove"; openTerm(); foot([]);
      span.textContent = "verifying against the live system…";
      runAssert(b.assert, lastRun && lastRun.run_id).then(function (out) {
        var r = document.createElement("span"); r.className = "res"; D.body.appendChild(r);
        var run = out.run || lastRun || {};
        if (out.ok) {
          r.innerHTML = '<span class="passchip">PASS</span>' + esc(fill(b.pass || "the draw returned a real receipt.", run));
          setTag("PASS · a real receipt", true);
          foot([{ label: "complete", hot: true, fn: next }]);
        } else {
          r.innerHTML = '<span class="failtx">FAIL — ' + esc(fill(b.fail || "no receipt. re-seat the head and the tail, fire again.", run)) + "</span>";
          setTag("no receipt yet", false);
          foot([{ label: "back to the fire", hot: true, fn: function () { BI = firstDoIndex(); mode = "idle"; runBeat(); } }]);
        }
      });
    }
  }

  /* THE TRAVEL — the distance to this rung's district, read from the probe's real position and counted
     down as you fly it. Makes the crossing legible: you are going somewhere, not waiting somewhere. */
  function startTravel() {
    stopTravel();
    if (!GAME || !GAME.onFrame || !here) return;
    /* re-affirm the district as the beat arms — the load-time placement can lose a race with the
       world's own async build, and the dock target must never fall back to the core silently. */
    if (GAME.bus) GAME.bus.emit("beacon:set", { x: here.x, z: here.z });
    travelHook = GAME.onFrame(function () {
      if (mode !== "do") return;
      var eng = GAME.state.engine; if (!eng) return;
      var p = eng.scene && eng.scene.getObjectByName("probe"); if (!p) return;
      var dx = p.position.x - here.x, dz = p.position.z - here.z;
      var d = Math.sqrt(dx * dx + dz * dz);
      if (d > 13) setTag(here.nm + " · " + Math.round(d) + "m", false);
      else if (D.tag.textContent.indexOf("m") >= 0 || !D.tag.textContent) setTag("arrived · dock [F]", false);
    });
  }
  function stopTravel() { if (travelHook && GAME && GAME.offFrame) { GAME.offFrame(travelHook); travelHook = null; } }

  function firstDoIndex() { for (var i = 0; i < M.beats.length; i++) if (M.beats[i].kind === "do") return i; return 0; }
  function esc(s) { return String(s).replace(/</g, "&lt;"); }

  /* ---------- the honest assert: re-read GET /game/run?id= and judge the REAL body ---------- */
  function runAssert(assertId, runId) {
    if (!runId || !window.GameAPI) return Promise.resolve({ ok: false, run: null });
    return window.GameAPI.run(runId).then(function (j) {
      var r = (j && j.run) ? j.run : (j || {});
      var links = r.links || r.trace || [];
      var state = String(r.state || r.status || "").toUpperCase();
      var settled = state !== "HALTED" && state !== "FAIL" && state !== "LOST";
      var tap = null, scorer = null, ladder = null;
      for (var i = 0; i < links.length; i++) {
        if (links[i] && links[i].part === "tap") tap = links[i];
        if (links[i] && links[i].part === "scorer") scorer = links[i];
        if (links[i] && links[i].part === "ladder") ladder = links[i];
      }
      /* the real /game/run body carries pass at TOP-LEVEL (r.pass / r.run_ok) and on the scorer's
         receipt (receipt.pass) — there is NO verdict object. Read the truth where it actually lives. */
      var passed = (r.pass === true) || (r.run_ok === true) || (r.verdict && r.verdict.pass === true) ||
                   !!(scorer && scorer.receipt && scorer.receipt.pass === true);
      /* the LOCKED run_receipt assert: both frozen parts landed a truthy receipt, the scorer passed,
         the run settled, the body is ok. Receipt may be an object (tap {plant,model,chars} / scorer
         {pass,axes}) or a folded string — assert PRESENT+truthy, never "a non-empty string". */
      var ok = (j && j.ok !== false) && settled && links.length > 0 &&
               tap && tap.receipt != null && tap.receipt !== false &&
               scorer && scorer.receipt != null && scorer.receipt !== false && passed;
      /* reach_receipt (THE STAKE, M02): the LADDER must be in the trace with a truthy receipt — the reach
         PROVABLY happened. Passes on a real metered cost AND on a survived fall (both land a ladder link);
         FAILS on a bare [tap,scorer] draw (no ladder). Stronger + honester than gating cost_u>0, which would
         wrongly fail an honest survived-fall. This closes the honesty inversion (audit drift #1). */
      if (assertId === "reach_receipt") ok = ok && !!(ladder && ladder.receipt != null && ladder.receipt !== false);
      /* ward_receipt (THE WARD, M03): the LADDER is seated (the reach was attempted) but the SENSITIVE zone
         forced the draw home to the free hearth — cost 0 not because it was cheap but because the mind
         refused to leak. Assert: ladder link present + zone sensitive + cost_u exactly 0 + pass. Verified
         against the real machinery (energy.ladder selects local-only rods for a sensitive zone). */
      var zoneNow = String(r.zone || (j && j.zone) || "").toLowerCase();
      var costNow = (r.cost_u !== undefined && r.cost_u !== null) ? r.cost_u : ((j && j.cost_u !== undefined) ? j.cost_u : null);
      if (assertId === "ward_receipt") ok = ok && !!ladder && zoneNow === "sensitive" && costNow === 0;
      var pick = function (k) { return (r[k] !== undefined && r[k] !== null) ? r[k] : null; };
      return { ok: ok, run: { run_id: runId, total_ms: pick("total_ms"), cost_u: pick("cost_u"), verdict: { pass: passed } } };
    }, function () { return { ok: false, run: null }; });  /* carrier unreachable -> honest FAIL, never a fabricated pass */
  }

  /* ---------- run:done — the player fired for real (the two-tier gate) ---------- */
  function onRunDone(ev) {
    if (mode !== "do" || !awaiting) return;                 /* arm-gate: ignore stale/late events */
    if (!ev || !ev.run_id) { nudge(ev && ev.halted ? "halted" : "reseat"); return; }
    if (ev.pass === true) {
      awaiting = false; lastRun = ev; stopTravel();
      setHud((doBeat && doBeat.earned) || "it drew at the head. it closed at the tail.", true);
      setTag("a real draw landed · reading the receipt", true);
      BI++;                                                 /* the ONLY advance path: a real PASS */
      if (BI >= M.beats.length) completeMission(); else runBeat();
      return;
    }
    /* a real run that did not pass — keep DO armed, located nudge, never advance */
    lastRun = ev;
    nudge(ev.pass === null ? "reseat" : "halted");
  }

  /* ---------- run:refused — no run was ever minted (honest, must not hang) ---------- */
  function onRunRefused(ev) {
    if (mode !== "do" || !awaiting) return;
    setHud((ev && ev.reason) || "refused. re-seat the head and the tail, fire again.", true);
    setTag("refused · nothing spent", false);
  }

  function nudge(which) {
    var line = doBeat && doBeat[which];
    if (!line) line = which === "reseat" ? "unscored draw. seat THE MEASURE at the tail, then fire again."
                                         : "a rod refused. re-seat the head and the tail, fire again.";
    setHud(line, true);
    setTag(which === "reseat" ? "unscored · seat THE MEASURE" : "the draw fell · retry", false);
  }

  /* ---------- completion + reveal (the earned close) ---------- */
  function completeMission() {
    closeTerm(); mode = "done";
    var rw = M.rewards || {};
    setHud(rw.log || (M.id + " complete"), true);
    setTag("mission complete", true);
    if (rw.reveal && rw.reveal.length) {
      D.term.classList.add("open");
      D.head.textContent = M.id + " · complete";
      D.body.innerHTML = "";
      var s = document.createElement("span"); s.className = "res"; s.textContent = rw.reveal.join("\n"); D.body.appendChild(s);
      if (rw.tag) { var t = document.createElement("span"); t.className = "note"; t.textContent = "\n" + fill(rw.tag, lastRun || {}); D.body.appendChild(t); }
      var nextLabel = (seqIdx + 1 < SEQ.length) ? "the next rung" : "close";
      foot([{ label: nextLabel, hot: true, fn: advanceToNext }]);
    }
    try { localStorage.setItem("probe.mission." + M.id, "done"); } catch (e) {}
    /* the reveal ledger + the server-side sacred save (state/journey_save.json) are wired in a later
       stage — this slice persists completion honestly to local state only, and STATUS.md says so. */
    if (GAME && GAME.bus) GAME.bus.emit("mission:done", { id: M.id, reveals: (rw.reveals) || [] });
    if (!(rw.reveal && rw.reveal.length)) advanceToNext();   /* no reveal -> chain straight to the next rung */
  }

  /* advance the guided ladder: close the reveal, step to the next rung, open it straight in */
  function advanceToNext() {
    closeTerm();
    if (seqIdx + 1 < SEQ.length) {
      seqIdx++;
      try { localStorage.setItem("probe.seqIdx", String(seqIdx)); } catch (e) {}
      if (GAME && GAME.bus) GAME.bus.emit("plate:reset", {});   /* a fresh plate for the next rung */
      loadMission(true);
    }
  }

  /* ---------- cold-open: the brief opens on the first key (the ANY-KEY wake), or ?m=1 ---------- */
  function coldOpen() { if (started || !M) return; started = true; BI = 0; runBeat(); }

  /* ---------- boot ---------- */
  /* load the rung at seqIdx. autostart=true opens it straight in (the next rung after a completion);
     otherwise it waits for the ANY-KEY wake (or ?m=1), and stays dormant in the ?bench=1 sandbox. */
  function loadMission(autostart) {
    fetch("/game/data/missions/" + SEQ[seqIdx]).then(function (r) {
      if (!r.ok) throw new Error("http " + r.status);
      return r.json();
    }).then(function (data) {
      M = data; BI = 0; started = false;
      /* stand this rung in its district and light the mark there — the world now knows where to send you */
      here = DISTRICTS[M.beacon] || DISTRICTS.core;
      if (GAME && GAME.bus) GAME.bus.emit("beacon:set", { x: here.x, z: here.z });
      setHud(M.objective || "");
      if (autostart) { setTag("", false); started = true; runBeat(); return; }
      setTag("press any key", false);
      var arm = function () {
        window.removeEventListener("keydown", arm, true); window.removeEventListener("pointerdown", arm, true);
        setTimeout(coldOpen, 60);
      };
      var qp; try { qp = new URLSearchParams(location.search); } catch (e) { qp = null; }
      if (qp && qp.get("bench") === "1" && qp.get("m") !== "1") { return; }   /* bench sandbox: dormant */
      window.addEventListener("keydown", arm, true);
      window.addEventListener("pointerdown", arm, true);
      if (qp && qp.get("m") === "1") setTimeout(coldOpen, 120);
    }).catch(function (e) { setHud("mission data unreachable — " + e.message); });
  }

  function init(game) {
    GAME = game;
    try { RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { RM = false; }
    style(); build();
    GAME.bus.on("run:done", onRunDone);
    GAME.bus.on("run:refused", onRunRefused);
    /* resume at the reached rung; ?rung=N is a harness hook to load a rung directly */
    try {
      var qp0 = new URLSearchParams(location.search), rg = qp0.get("rung");
      var si = (rg != null) ? parseInt(rg, 10) : parseInt(localStorage.getItem("probe.seqIdx") || "0", 10);
      if (si >= 0 && si < SEQ.length) seqIdx = si;
    } catch (e) { seqIdx = 0; }
    loadMission(false);
  }

  return {
    init: init,
    _debug: function () { return { id: M && M.id, BI: BI, mode: mode, awaiting: awaiting, lastRun: lastRun, beats: M && M.beats.length }; }
  };
})();
