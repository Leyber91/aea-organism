/* boot.js — GAME object birth.
   Governance: E1_CODE_ARCHITECTURE.md §2.2 (the one boundary rule: window.GAME is the
   ONLY global the game adds — state refs + one event bus, no other cross-module globals),
   §2.1 (frame-hook registry seam: GAME.onFrame/offFrame, released in dispose),
   §7 item 0 (GAME birth in the boot section) · §5 (error surfaces: onerror -> #err). */
(function () {
  "use strict";

  var topics = {};
  var hooks = [];

  var GAME = {
    state: {
      /* refs land here as modules birth them (aliasing, never relocation — E1 §2.2) */
      flags: { still: false, title: false, pose: "boot" }
    },
    bus: {
      on: function (t, fn) { (topics[t] = topics[t] || []).push(fn); return fn; },
      off: function (t, fn) {
        var a = topics[t]; if (!a) return;
        var i = a.indexOf(fn); if (i >= 0) a.splice(i, 1);
      },
      emit: function (t, d) {
        var a = topics[t]; if (!a) return;
        for (var i = 0; i < a.length; i++) a[i](d);
      }
    },
    onFrame: function (fn) { hooks.push(fn); return fn; },
    offFrame: function (fn) { var i = hooks.indexOf(fn); if (i >= 0) hooks.splice(i, 1); },
    frame: function (dt, t) { for (var i = 0; i < hooks.length; i++) hooks[i](dt, t); }
  };

  /* ?still harness flags (04 §7): still = fixed camera, no input.
     &title=1 shows the boot scrim in a still; &pose=flight poses probe mid-flight. */
  var q = new URLSearchParams(location.search);
  GAME.state.flags.still = q.has("still");
  GAME.state.flags.title = q.get("title") === "1";
  GAME.state.flags.pose = q.get("pose") || "boot";

  /* honesty plumbing: every uncaught error is painted, never swallowed (E1 §1.1) */
  window.onerror = function (msg, src, line) {
    var el = document.getElementById("err");
    if (el) {
      el.textContent = "ERR " + msg + " @ " + String(src || "").split("/").pop() + ":" + line;
      el.style.display = "block";
    }
  };

  window.GAME = GAME;
})();
