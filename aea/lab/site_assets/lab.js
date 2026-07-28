/* THE PROBE - lab evidence. The page builds itself from data/index.json.
 *
 * Nothing here knows the name of any experiment. Add a run to state/lab/runs/, rebuild the
 * manifest, and its section appears. That is the whole point: the first version baked the numbers
 * into markup and was stale the moment the next cell landed.
 *
 * THE HONESTY LAW, IN CODE. `dash()` is the only formatter used for a measurement. A value that is
 * absent renders as an em dash. It never renders as 0, never as "n/a", and is never omitted, because
 * a missing measurement is information and hiding it is the fallacy this lab keeps catching itself in.
 */
'use strict';

const D = document;
const $ = (s, r) => (r || D).querySelector(s);
const el = (t, a, kids) => {
  const n = D.createElement(t);
  for (const k in (a || {})) {
    if (k === 'class') n.className = a[k];
    else if (k === 'html') n.innerHTML = a[k];
    else if (k.startsWith('on')) n.addEventListener(k.slice(2), a[k]);
    else n.setAttribute(k, a[k]);
  }
  (kids || []).forEach(c => n.appendChild(typeof c === 'string' ? D.createTextNode(c) : c));
  return n;
};

/* An absent measurement is a dash. Never a zero standing in for a thing nobody measured. */
const dash = (v, f) => (v === null || v === undefined || v === '') ? '—'
  : (f ? f(v) : String(v));
const pct = v => dash(v, x => x.toFixed(2));
const wilson = d => (d && d.wilson95 && d.wilson95[0] !== null)
  ? d.wilson95[0].toFixed(2) + '–' + d.wilson95[1].toFixed(2) : '—';

const REGIME_TAG = { FULL: 'on', TAIL: 'warn', NONE: 'off' };
const STATUS_WHY = {
  NO_EVIDENCE: 'No reply text was stored. This run can never be re-read, so a defect found later in '
    + 'its reader can only be fixed by buying every call again.',
  PARTIAL_EVIDENCE: 'Only the last 320 characters of each reply were kept. Four recorded defects '
    + 'came from that slice, including one that erased a real creature.',
  NEVER_RUN: 'No stored run at all.',
  COMPLETE: null
};

/* The ten decisions between a reply and a number. Amber steps can change a score. */
const PIPELINE = [
  [0, 'The call returns text. <code>overseer.inspect()</code> flags it — empty, truncated '
    + 'mid-word, echoing the prompt, leaking reasoning. A flag is a note, never a score.'],
  [0, 'The naive read. <code>stated()</code> takes the number the reply appears to state. The floor '
    + 'every organism has, because a bare call’s only capacity is that a value comes back.'],
  [0, 'The readout, if seated. <code>read_work()</code> ignores what the reply claims and reads its '
    + 'WORKING — enumerated lines, a labelled total, a solved equation.'],
  [0, 'The guard, if seated. <code>Validation</code> may DECLINE. An abstention ends the read; it is '
    + 'not a wrong answer and is never counted as one.'],
  [0, 'The container extracts the running value. <code>checkpoint</code> reads its own STATE line, '
    + '<code>free</code> splits off its NOTE, the others take the stated answer.'],
  [1, 'The strict anchor, and THIS IS WHAT SCORES. Every step must end <code>ANSWER: &lt;integer&gt;'
    + '</code>. The lab’s own reader runs beside it and their DISAGREEMENT RATE is the '
    + 'instrument’s error bar on itself.'],
  [1, 'Three outcomes, not two. Anchor equals truth is a hit, differs is a miss, and <b>no anchor at '
    + 'all is a PARSE FAILURE counted apart</b> — otherwise a container that changes format '
    + 'compliance masquerades as one that changes capability.'],
  [1, 'The sequence is the unit. A chain counts only if it completed every step AND its last step '
    + 'hit. Sixteen steps of one chain are not sixteen independent trials.'],
  [1, 'The cell gets a Wilson 95% interval. No flat band: at n=8 two arms from the SAME distribution '
    + 'differ by 0.10 most of the time, so the old band was calibrated to noise.'],
  [1, 'The comparison is paired. The same chain runs under every container, compared by McNemar '
    + 'exact on discordant pairs, which removes task difficulty from the comparison entirely.']
];

let INDEX = null;
let TAB = 'overview';

async function boot() {
  try {
    INDEX = await (await fetch('data/index.json', { cache: 'no-store' })).json();
  } catch (e) {
    $('#main').innerHTML = '<p class="loading">Could not read <code>data/index.json</code>. Build it '
      + 'with <code>python -m aea.lab.site</code>, then serve with <code>--serve</code>. '
      + 'Opening this file directly from disk will not work, because the page fetches its data.</p>';
    return;
  }
  const s = INDEX.summary || {};
  $('#meta').innerHTML = ['<span><b>built</b> ' + INDEX.built + '</span>',
    '<span><b>experiments</b> ' + INDEX.experiments.length + '</span>',
    '<span><b>re-scorable</b> ' + (s.COMPLETE || 0) + '</span>',
    '<span><b>partial</b> ' + (s.PARTIAL_EVIDENCE || 0) + '</span>',
    '<span><b>no evidence</b> ' + (s.NO_EVIDENCE || 0) + '</span>'].join('');

  const tabs = $('#tabs');
  const mk = (id, label) => {
    const b = el('button', { role: 'tab', onclick: () => { TAB = id; render(); } }, [label]);
    b.dataset.id = id; tabs.appendChild(b);
  };
  mk('overview', 'Coverage');
  mk('pipeline', 'How a reply is judged');
  INDEX.experiments.filter(x => x.status !== 'NEVER_RUN')
    .forEach(x => mk(x.id, x.id.replace(/_.*/, '')));
  render();
}

function render() {
  D.querySelectorAll('#tabs button').forEach(b =>
    b.setAttribute('aria-selected', String(b.dataset.id === TAB)));
  const m = $('#main');
  m.innerHTML = '';
  if (TAB === 'overview') return overview(m);
  if (TAB === 'pipeline') return pipeline(m);
  return experiment(m, TAB);
}

function overview(m) {
  const s = INDEX.summary || {};
  m.appendChild(el('h2', {}, ['What the archive actually keeps']));
  m.appendChild(el('p', {
    class: 'lede', html:
      'Replies are stored in three regimes and only one can be read again. <strong>' + (s.COMPLETE || 0)
      + ' experiments kept the full reply. ' + (s.PARTIAL_EVIDENCE || 0) + ' kept the last 320 '
      + 'characters only. ' + (s.NO_EVIDENCE || 0) + ' kept nothing at all.</strong> An experiment '
      + 'with no readable evidence keeps its card here and states the command that would fill it. '
      + 'A missing measurement is information.'
  }));
  const grid = el('div', { class: 'grid' });
  INDEX.experiments.forEach(x => {
    const gap = x.status !== 'COMPLETE';
    const c = el('div', { class: 'card' + (gap ? ' gap' : '') });
    c.appendChild(el('h4', {}, [x.id]));
    c.appendChild(el('div', {
      class: 'row', html: '<span class="tag ' + (REGIME_TAG[x.regime] || 'off') + '">' + x.regime
        + '</span><span><b>replies</b> ' + dash(x.replies || null) + '</span>'
    }));
    c.appendChild(el('div', {
      class: 'row', html: '<span><b>runs</b> ' + x.runs.length + '</span><span><b>cells</b> '
        + dash(x.cells || null) + '</span>'
    }));
    const why = STATUS_WHY[x.status];
    if (why) {
      c.appendChild(el('p', { class: 'why' }, [why]));
      c.appendChild(el('p', { class: 'why', html: 'Reboot: <code>' + x.reboot_command + '</code>' }));
    } else {
      c.appendChild(el('a', {
        class: 'open', tabindex: '0',
        onclick: () => { TAB = x.id; render(); window.scrollTo(0, 0); }
      }, ['open evidence']));
    }
    grid.appendChild(c);
  });
  m.appendChild(grid);
}

function pipeline(m) {
  m.appendChild(el('h2', {}, ['How a reply becomes a pass or a fail']));
  m.appendChild(el('p', {
    class: 'lede', html: 'Ten decisions stand between what the rod said and the number in a verdict '
      + 'line. The amber steps are the ones that can change a score. Every one of them has been '
      + 'wrong at least once, and each wrong one is recorded in <code>aea/lab/METHOD.md</code>.'
  }));
  const ol = el('ol', { class: 'pipe' });
  PIPELINE.forEach(([gate, body]) =>
    ol.appendChild(el('li', { class: gate ? 'gate' : '', html: '<p>' + body + '</p>' })));
  m.appendChild(ol);
}

async function experiment(m, id) {
  const entry = INDEX.experiments.find(x => x.id === id);
  m.appendChild(el('p', { class: 'loading' }, ['Reading ' + id + '…']));
  let run;
  try {
    run = await (await fetch('data/' + id + '/latest.json', { cache: 'no-store' })).json();
  } catch (e) {
    m.innerHTML = '<p class="loading">No readable run for ' + id + '.</p>';
    return;
  }
  if (TAB !== id) return;                       /* the user moved on while this was loading */
  m.innerHTML = '';

  m.appendChild(el('h2', {}, [id]));
  m.appendChild(el('div', {
    class: 'meta', html: '<span><b>run</b> ' + run.run_id + '</span><span><b>design</b> '
      + dash(run.design_id) + '</span><span><b>status</b> ' + dash(run.status) + '</span>'
      + '<span><b>started</b> ' + dash(run.at) + '</span><span><b>regime</b> '
      + '<span class="tag ' + (REGIME_TAG[run.regime] || 'off') + '">' + run.regime + '</span></span>'
  }));

  if (run.verdict && run.verdict.length) {
    m.appendChild(el('h3', {}, ['Verdict, as the run wrote it']));
    m.appendChild(el('pre', { class: 'reply' }, [run.verdict.join('\n')]));
  }

  if (run.pilots && run.pilots.length) {
    m.appendChild(el('h3', {}, ['Calibration']));
    m.appendChild(table(
      ['Rod', 'Per-step', 'Ideal length', 'Chosen', 'Predicted', 'In range'],
      run.pilots.map(p => [
        { k: 1, v: p.rod }, { n: 1, v: pct(p.per_step_accuracy) }, { n: 1, v: dash(p.ideal_length) },
        { n: 1, v: p.length_chosen, fire: 1 }, { n: 1, v: pct(p.predicted_sequence_rate) },
        { v: p.in_range ? '<span class="fired">yes</span>'
          : '<span class="tag warn">descriptive only</span>', html: 1 }])));
  }

  if (run.cells && run.cells.length) {
    m.appendChild(el('h3', {}, ['Cells — never pooled across rods']));
    const has = k => run.cells.some(c => c[k]);
    const head = ['Arm', 'Rod', 'Len', 'Correct', 'Wilson 95%'];
    if (has('token_retrieval')) head.push('Token recall');
    if (has('parse_fail_steps')) head.push('Parse fail', 'Reader disagree');
    m.appendChild(table(head, run.cells.map(c => {
      const co = c.correct || {}, tk = c.token_retrieval || {};
      const r = [{ k: 1, v: dash(c.form || c.arm) }, { v: dash(c.rod) },
        { n: 1, v: dash(c.length) },
        { n: 1, html: 1, v: dash(co.k) + '/' + dash(co.n)
          + '<span class="bar"><i style="width:' + Math.min(100, (co.rate || 0) * 100) + '%"></i></span>' },
        { n: 1, v: wilson(co) }];
      if (has('token_retrieval')) r.push({ n: 1, v: dash(tk.k) + '/' + dash(tk.n), fire: tk.k > 0 });
      if (has('parse_fail_steps')) {
        r.push({ n: 1, v: pct((c.parse_fail_steps || {}).rate) });
        r.push({ n: 1, v: pct((c.read_disagreement || {}).rate) });
      }
      return r;
    })));
  }

  m.appendChild(el('h3', {}, ['The replies']));
  m.appendChild(el('p', {
    class: 'lede', html: run.replies_total
      ? 'Showing <strong>' + run.replies_shown + ' of ' + run.replies_total + '</strong> stored '
        + 'replies' + (run.replies_omitted ? ' — the cap is stated rather than silent; the rest '
        + 'are in the run JSON' : '') + '. Open any row for the full text and the judgement chain.'
      : '<strong>This run stored no reply text.</strong> ' + STATUS_WHY.NO_EVIDENCE
  }));
  (run.replies || []).forEach(r => m.appendChild(reply(r)));
}

function table(head, rows) {
  const t = el('table');
  t.appendChild(el('thead', { html: '<tr>' + head.map(h =>
    '<th' + (/^(len|correct|wilson|token|parse|reader|per-step|ideal|chosen|predicted)/i.test(h)
      ? ' class="num"' : '') + '>' + h + '</th>').join('') + '</tr>' }));
  const tb = el('tbody');
  rows.forEach(cells => {
    const tr = el('tr');
    cells.forEach(c => {
      const td = el('td', { class: (c.k ? 'k ' : '') + (c.n ? 'num ' : '') + (c.fire ? 'fired' : '') });
      if (c.html) td.innerHTML = c.v; else td.textContent = c.v;
      tr.appendChild(td);
    });
    tb.appendChild(tr);
  });
  t.appendChild(tb);
  return el('div', { class: 'scroll' }, [t]);
}

function reply(r) {
  const c = r.ctx || {};
  const state = r.parse_fail ? 'PARSE FAIL' : (r.hit ? 'HIT' : (r.hit === false ? 'MISS' : '—'));
  const cls = r.parse_fail ? 'warn' : (r.hit ? 'on' : 'off');
  const who = [c.chain !== undefined ? 'chain ' + c.chain + '.' + dash(c.sample) : null,
    c.step !== undefined ? 'step ' + c.step : null,
    c.trial !== undefined ? 'trial ' + c.trial : null].filter(Boolean).join(' · ') || 'reply';
  const d = el('details', { class: 'rep' });
  d.appendChild(el('summary', {
    html: '<span class="sid">' + who + '</span>'
      + '<span class="dim">' + dash(c.form || c.arm) + '</span>'
      + '<span class="spre">' + esc((r.text || '').replace(/\n/g, ' ').slice(0, 150)) + '</span>'
      + '<span class="tag ' + cls + '">' + state + '</span>'
  }));
  const b = el('div', { class: 'body' });
  b.appendChild(el('pre', { class: 'reply' }, [r.text || '']));
  const rd = el('div', { class: 'readers' });
  [['truth', r.truth], ['ANSWER anchor · scores', r.anchored, r.hit],
    ['lab reader', r.value], ['read by', r.read_by],
    ['rod', c.rod], ['flags', (r.flags || []).join(', ') || null]]
    .forEach(([lab, v, fire]) => rd.appendChild(el('div', {
      class: 'rd', html: '<div class="lab">' + lab + '</div><div class="val'
        + (fire ? ' fired' : '') + '">' + esc(dash(v)) + '</div>'
    })));
  b.appendChild(rd);
  if (r.read_disagrees) {
    b.appendChild(el('p', { class: 'note' }, ['The strict anchor and the lab’s own reader '
      + 'disagree on this reply. One of them is wrong, and this is the disagreement the cells table '
      + 'counts.']));
  }
  d.appendChild(b);
  return d;
}

const esc = s => String(s).replace(/[&<>]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[m]));

boot();
