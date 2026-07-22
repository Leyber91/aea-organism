/* core/api.js - THE ONLY SERVER-TALKER (first light).
   Every game call goes through the honest seam at /game/*. Receipt-aware by contract:
     - a refusal answers HTTP 200 + {ok:false, refused:'<clause>'}  -> read, never thrown
     - a real HTTP error (4xx/5xx) throws an Error with .status      -> the plate can print it
     - an unreachable / timed-out carrier rejects                    -> CARRIER LOST
   Abort + timeout so a hung carrier can never lock the plate forever. No build step: a plain
   global (window.GameAPI), loaded before bench.js; bench.js's three fetch sites route through it. */
(function () {
  "use strict";
  var TIMEOUT_MS = 15000;

  function call(method, url, body) {
    var ctl = ("AbortController" in window) ? new AbortController() : null;
    var to = setTimeout(function () { if (ctl) { ctl.abort(); } }, TIMEOUT_MS);
    var opt = { method: method };
    if (ctl) { opt.signal = ctl.signal; }
    if (body) { opt.headers = { "Content-Type": "application/json" }; opt.body = JSON.stringify(body); }
    return fetch(url, opt).then(function (res) {
      clearTimeout(to);
      if (!res.ok) { var e = new Error("http " + res.status); e.status = res.status; throw e; }
      return res.json();                 /* a 200 refusal returns its {ok:false, refused} body */
    }, function (err) { clearTimeout(to); throw err; });
  }

  window.GameAPI = {
    /* compose -> IGNITE: POST the construct spec to the real bench. {ok,run_id} | {ok:false,refused} */
    ignite: function (spec, task) { return call("POST", "/game/ignite", { spec: spec, task: task }); },
    /* poll the live trace by run_id */
    run: function (rid) { return call("GET", "/game/run?id=" + encodeURIComponent(rid)); },
    /* the folded live snapshot - the real meter (dashes when unknown, never invented) */
    state: function () { return call("GET", "/game/state"); }
  };
})();
