<!-- GENERATED 2026-07-28 by an 8-specialist research workflow, then synthesised.
     Every value is resolved: no ranges, no principles. Implement against it directly.
     Diagnostic evidence that produced it is in diary/SESSION_LOG.md. -->

# THE BOARD — IMPLEMENTATION SPECIFICATION v1

Target: `aea/tooling/board.py` (generator) → `web/board.html` (output). Single file, no build step, no external requests. Reference viewport **1700 x 1000**, DPR 1.

Two shell dimensions change from the brief: **rail 212 → 224px**, **periphery 264 → 288px**. Reason: at 1700, `1700 − 224 − 288 = 1188`; minus `24px` work padding each side = `1140`; `(1140 − 11×12) / 12 = 84.0` — an integer 12-column centre grid. At 212/264 the column is `86.33px` and every card edge lands on a different subpixel offset.

---

## 1 · THE TOKEN BLOCK

Drop-in replacement for the `:root` emitted at `aea/tooling/board.py` L157-170. Every value final. Comments mark where specialists disagreed and why one was taken.

```css
:root{
  color-scheme:dark;

  /* ── SURFACES ── CIE L* = 1.90 / 3.88 / 7.07 / 11.97 / 17.16 / 22.19
     Every adjacent step >= dL* 2.5; card-over-ground = dL* 5.17.
     Current board ladder steps dL* 1.40 / 1.31 / 2.03 — below JND, three of five
     surfaces indistinguishable. That arithmetic IS "flat".
     DISAGREEMENT: one spec wanted panel #181e27 (L* 11.06), another canvas #0a0c10.
     Rejected both: #181e27 puts the card one step off Grafana's ELEVATED panel on a
     ground 6 L* darker than Grafana's, so cards read as floating plates, not a field;
     #0a0c10 as ground forfeits the void, which is project law. */
  --s-0:#060709;   /* ground / void — also the deepest well */
  --s-1:#0a0e14;   /* recess: table bodies, canvas wells, code */
  --s-2:#10161f;   /* panel: every card, every column */
  --s-3:#18202b;   /* raised: hover, active row, current view */
  --s-4:#212b38;   /* float: popover, menu, tooltip */
  --s-5:#2b3644;   /* pop: selected, drag ghost */

  /* ── HAIRLINES ── alpha, never opaque hex: they must survive on any surface.
     DISAGREEMENT: one spec proposed opaque #1c212a/#2b323d. Rejected — Linear,
     Vercel and GitHub all ship white-alpha borders and reserve opaque hex for text. */
  --hair-1:rgba(255,255,255,0.045);   /* grouping divider, row rule */
  --hair-2:rgba(255,255,255,0.075);   /* card edge — the default */
  --hair-3:rgba(255,255,255,0.110);   /* focused / selected edge, non-accent */
  --hair-dark:rgba(1,4,9,0.640);      /* outer separation ring */
  --toplight:rgba(255,255,255,0.055); /* inset top light edge */
  --toplight-ring:rgba(255,255,255,0.031);
  --guide:rgba(255,255,255,0.028);    /* column armature behind the centre */

  /* ── SHADOWS ── dark-mode alphas, 4-8x the light-mode value at identical geometry.
     A shadow alone cannot separate a card from #060709: black at 0.200 over the
     ground shifts it dL* -0.29 (vs -17.95 over white). The RING separates; the
     shadow only says "floating". */
  --sh-flat:0 1px 1px 0 rgba(1,4,9,0.400);
  --sh-raise:0 2px 2px rgba(0,0,0,0.322), 0 8px 8px -8px rgba(0,0,0,0.161);
  --sh-float:0 4px 24px rgba(0,0,0,0.200), 0 16px 48px -12px rgba(0,0,0,0.349);
  --sh-sunk:inset 0 1px 0 0 rgba(1,4,9,0.240),
            inset 0 0 0 1px rgba(0,0,0,0.320),
            inset 0 8px 24px -12px rgba(0,0,0,0.560);

  /* ── INK ── CR on --s-2: 15.29 / 11.22 / 6.70 / 4.71 / 3.03 / 1.85
     Tier 4 taken from the spec that measured 4.71 (clears AA) over the one that
     computed 4.06 — in a dense ops UI the "quiet" tier is read constantly.
     NEVER write dim text as rgba(255,255,255,a): it resolves to b-r +7 and reads
     as fog. These hexes carry b-r +18..+24 and read as present. */
  --ink-1:#e8edf4;   /* display numbers, claims, key values */
  --ink-2:#c2cad4;   /* body, table cells */
  --ink-3:#98a1ad;   /* micro labels, th, rail items, units */
  --ink-4:#737b86;   /* sub-lines, counts, metadata */
  --ink-5:#565d67;   /* disabled, placeholder — THE TEXT FLOOR */
  --ink-6:#3c4450;   /* structure only: gridlines, empty pips. Never text. */

  /* ── ONE HUE, SIX STATES ── L* 77.5 / 83.2 / 69.7 / 53.3 / 37.5 / 25.1 */
  --am-fired:#ffb000;   /* LIVE / FAILING / the one thing that matters now */
  --am-hot:#ffc74a;     /* pulse peak, hover on a fired element, current sample */
  --am-steady:#d4a24c;  /* WARN / LATER */
  --am-idle:#9c7a3c;    /* STALE / queued */
  --am-spent:#6b552f;   /* KILLED / retired */
  --am-trace:#463a24;   /* structure: gridline, empty pip, un-fired gauge track */
  --am-bed:rgba(255,176,0,0.055);   /* tint bed under a failing row (dL* +4.05) */
  --am-edge:rgba(255,176,0,0.220);  /* 1px border on a fired card */
  --am-mark:rgba(255,176,0,0.720);  /* 2px inset rail on a changed row */
  --am-flash:rgba(255,176,0,0.140); /* delta wash peak */
  --am-glow:0 0 0 1px rgba(255,176,0,0.220), 0 0 20px -4px rgba(255,176,0,0.160);

  /* ── TYPE ── six integer sizes. The as-built page ships TWELVE (9, 9.5, 10, 10.5,
     11, 11.5, 12.5, 13, 14, 15, 19, 25), four fractional, with adjacent ratios of
     1.04-1.09x. A ratio under 1.15x is not a perceptible step, so twelve sizes
     render as one texture. That is the typographic half of "flat".
     IBM Plex Mono is ABSENT from this machine (261 families, zero Plex); Consolas
     paints. Cascadia Mono is second so the fallback is deterministic — ui-monospace
     was removed because its Windows-Chrome resolution is undocumented and may land
     on Cascadia CODE, a ligature font. */
  --mono:"IBM Plex Mono","Cascadia Mono",Consolas,"Courier New",monospace;
  --fs-micro:11px;   /* UPPERCASE ONLY. cap-height 7.02px; x-height would be 5.39 */
  --fs-body:13px;    /* measured crispness peak: 37.2% fully-opaque stems */
  --fs-claim:15px;
  --fs-head:20px;
  --fs-stat:28px;
  --fs-hero:34px;    /* DISAGREEMENT: 34 vs 40. 34 taken — 40/44 will not fit a
                        96px strip alongside an 11px eyebrow and a 13px sub-line,
                        and 34/13 = 2.62x already clears the 2.4x focal threshold. */
  --lh-micro:16px; --lh-row:18px; --lh-body:20px;
  --lh-claim:22px; --lh-head:28px; --lh-stat:32px; --lh-hero:38px;
  --ls-micro:1px;    /* 0.0909em @11px — INTEGER advance, shares the column grid */
  --ls-brand:2px;    /* wordmark + rail group heads ONLY: nothing aligns beneath */
  --ls-body:0;
  --ls-stat:-0.5px; --ls-hero:-1px;   /* fractional legal at/above 16px */

  /* ── SPACING LATTICE ── eight legal values. The as-built CSS emits 21 distinct
     spacing numbers (2.5, 3.5, 5, 7, 9, 11, 13, 18, 22, 60 …). Nothing can align
     when nothing shares a denominator. */
  --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s6:24px; --s8:32px; --s12:48px; --s16:64px;

  /* ── SHELL ── */
  --rail-w:224px; --peri-w:288px; --strip-h:96px;
  --col-w:84px; --gutter:12px; --pitch:96px;
  --work-pad-t:20px; --work-pad-x:24px; --work-pad-b:48px;
  --band-a:96px; --band-b:168px; --band-c:228px; --band-d:288px; --band-e:384px;

  /* ── RHYTHM ── every repeating row an integer. As-built td = 3.5 + 13x1.55 + 3.5
     = 27.15px, so nine ledger rows land on nine subpixel offsets and every 1px rule
     composites at a different alpha. */
  --row:24px; --row-lg:32px; --row-sm:20px;
  --nav-row:28px; --sec-head:24px; --kv-row:24px; --hd-h:40px;

  /* ── CARDS ── */
  --card-pad-y:12px; --card-pad-x:16px;
  --r-cell:0px;   /* table rows, canvas wells, full-bleed panels */
  --r-card:3px;   /* law cards, proposal cards, stat tiles */
  --r-pop:6px;    /* popovers only. Nothing gets 8px+ — that is the consumer register */
  --measure-max:68ch; --measure-min:46ch; --card-min:372px;

  /* ── EASING ── every value read out of a shipped product or published system.
     DISAGREEMENT: four different easing sets were proposed. Carbon's productive/
     expressive split was taken as the base because it is the only system that
     separates dense-task motion from expressive motion by name, plus two curves
     verified shipped in BOTH Linear and Vercel bundles. */
  --e-state:cubic-bezier(0.2,0,0.38,0.9);      /* Carbon productive standard */
  --e-enter:cubic-bezier(0,0,0.38,0.9);        /* Carbon productive entrance */
  --e-exit:cubic-bezier(0.2,0,1,0.9);          /* Carbon productive exit */
  --e-view:cubic-bezier(0.55,0,0.1,1);         /* Linear, 12 occurrences */
  --e-decay:cubic-bezier(0,0,0.3,1);           /* Carbon expressive entrance */
  --e-overlay:cubic-bezier(0.32,0.72,0,1);     /* Linear + Vercel, shipped */
  --e-breathe:cubic-bezier(0.45,0,0.55,1);     /* easeInOutQuad — symmetric loop */
  --e-emph:cubic-bezier(0.2,0,0,1);            /* MD3. ONE element on the page. */

  /* ── DURATION ── */
  --d-tap:70ms; --d-hi:90ms; --d-ho:140ms; --d-ho-delay:30ms;
  --d-enter:150ms; --d-view-out:90ms; --d-view-in:200ms;
  --d-data:240ms; --d-phos:320ms; --d-panel:300ms;
  --d-flash:880ms; --d-mark:1200ms; --d-breathe:2400ms;
  --stagger:28ms;

  /* ── AMPLITUDE ── */
  --rise:4px; --view-rise:5px; --view-sink:-3px;

  /* ── ATMOSPHERE ── */
  --grain-px:140px;
  --lift-core:rgba(122,140,164,0.055);
  --lift-mid:rgba(122,140,164,0.022);
  --pool:rgba(255,176,0,0.020);
  --glow-core:0 0 1px  rgba(255,206,122,0.400);
  --glow-mid: 0 0 7px  rgba(255,176,0,0.150);
  --glow-halo:0 0 26px rgba(255,138,0,0.070);
  --glow-far: 0 0 64px rgba(255,120,0,0.030);
}
```

**Base rule** (replaces `body{}` at board.py L~158):

```css
html,body{background:var(--s-0);color:var(--ink-2);margin:0;overflow:hidden}
body{
  font-family:var(--mono); font-size:var(--fs-body);
  line-height:var(--lh-body); letter-spacing:var(--ls-body); font-weight:400;
  font-variant-ligatures:none;
  font-feature-settings:"calt" 0,"liga" 0,"dlig" 0;   /* Cascadia Code IS installed;
      consola.ttf exposes calt+dlig. A board rendering code identifiers must never
      silently ligate != -> => into glyphs the source never contained. */
  font-variant-numeric:tabular-nums lining-nums;      /* tnum is a no-op in Consolas
      (digits already share advance 0.5498em) — kept as fallback insurance. lnum
      locks out onum, which Consolas DOES expose. */
}
/* -webkit-font-smoothing:antialiased DELETED (board.html L11): no-op on Windows
   DirectWrite, thins already coverage-starved stems on macOS. */
```

**Weight law:** no rule anywhere sets `font-weight` other than 400. Consolas ships only 400 and 700 on this machine; the 400→700 ink-mass jump is +24.5% at 13px and +47.1% at 16px — violent and size-unstable. Hierarchy is built from six weightless levers: size (6 steps), colour (6 steps), case, tracking, leading, grid position.

**Type role test:** no two roles sit within 1.15x in size unless they also differ by a colour step or by case. Grep the generated HTML for `font-size:\d+\.` — must return zero matches.

---

## 2 · COMPONENT SPECS

### 2.1 The shell

```css
.app{display:grid;height:100vh;
  grid-template-columns:var(--rail-w) 1fr var(--peri-w);
  grid-template-rows:var(--strip-h) 1fr}
.rail{grid-row:2;box-shadow:inset -1px 0 0 var(--hair-1)}
.work{grid-row:2;overflow-y:auto;overscroll-behavior:contain}
.side{grid-row:2;box-shadow:inset 1px 0 0 var(--hair-1)}
```

- Column rules are `inset box-shadow`, never `border` — a border adds to the box and pushes the 84px grid off by 1px.
- **The shell never animates.** Rail, strip, column rules and card frames paint opaque at frame 0. Screenshot at t=0 must show the full 224/1188/288 skeleton drawn.
- Rail and periphery never reflow, scroll-jump or repaint on view change.
- z-order: `#field` 0 → `#grain` 1 → `.app` 2 → `.pop` 40 → `.scrim` 30.

### 2.2 Top strip — 96px

```css
.strip{grid-column:1/-1;height:96px;display:grid;
  grid-template-columns:var(--rail-w) 1fr var(--peri-w);
  box-shadow:inset 0 -1px 0 var(--hair-2)}

.brand{padding:0 20px;display:flex;flex-direction:column;justify-content:center;gap:6px;
  box-shadow:inset -1px 0 0 var(--hair-1)}
.brand b{font-size:var(--fs-micro);line-height:var(--lh-micro);
  letter-spacing:var(--ls-brand);text-transform:uppercase;color:var(--am-fired)}
.brand .up{font-size:var(--fs-body);line-height:var(--lh-row);color:var(--ink-4)}

.answers{display:grid;grid-template-columns:repeat(3,372px);gap:12px;
  padding:12px 24px;align-content:center}
.ans{display:flex;flex-direction:column;justify-content:center}
.ans .lab{font-size:var(--fs-micro);line-height:16px;letter-spacing:var(--ls-micro);
  text-transform:uppercase;color:var(--ink-3)}
.ans .val{font-size:var(--fs-hero);line-height:38px;letter-spacing:var(--ls-hero);
  color:var(--ink-1);font-variant-numeric:tabular-nums lining-nums;white-space:nowrap}
.ans .val.hot{color:var(--am-fired);
  text-shadow:var(--glow-core),var(--glow-mid),var(--glow-halo),var(--glow-far)}
.ans .sub{font-size:var(--fs-body);line-height:18px;color:var(--ink-4);
  display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden}
```

Vertical arithmetic: `12 + 16 + 38 + 18 + 12 = 96px` exactly.

**The display tier renders NUMBERS AND SHORT VERDICT TOKENS ONLY.** Never prose, and never truncated prose. The current strip renders `Wire impasse/unstick into the wake, and st` at 19px — cut mid-word, the loudest element on the page, and a honesty-law violation (a truncated string is not the value). Render the **count** at 34px and the sentence at 13px `--ink-4` beneath, wrapped, one line, ellipsis via line-clamp.

Absent value: `content:"\2014"` in `--ink-5`. Never a zero, never a guess.

Periphery slot of the strip (288 x 96) carries the LIVE dot + last-poll age + the loops-closed burn bar (§2.11).

### 2.3 The rail — 224 x 904

```css
.rail{display:grid;grid-template-rows:auto 384px 224px;align-content:start}
.rail h4{height:24px;line-height:24px;margin:24px 16px 0;
  font-size:var(--fs-micro);letter-spacing:var(--ls-brand);
  text-transform:uppercase;color:var(--ink-4)}
.rail button{
  display:flex;align-items:center;justify-content:space-between;
  height:28px;padding:0 16px 0 14px;width:100%;
  border:0;background:transparent;color:var(--ink-3);
  font:inherit;font-size:var(--fs-body);line-height:var(--lh-row);
  box-shadow:inset 2px 0 0 transparent;cursor:pointer;text-align:left;
  transition:background-color var(--d-ho) var(--e-state) var(--d-ho-delay),
             color            var(--d-ho) var(--e-state) var(--d-ho-delay);
}
.rail button:hover{background:rgba(255,255,255,0.028);color:var(--ink-2);
  transition-duration:var(--d-hi);transition-delay:0ms}
.rail button[aria-current="page"]{
  background:var(--s-2);color:var(--ink-1);
  box-shadow:inset 2px 0 0 var(--am-fired)}
.rail button .n{color:var(--ink-5);font-variant-numeric:tabular-nums}
```

Rail internal left edge = 16px → text origin at x=16. There are exactly **three distinct left edges** in the whole viewport: `x=16` (rail + periphery text), `x=248` (centre text: 224 rail + 24 pad), `x=1436` (periphery text: 224+1188+24). The as-built page has six unaligned origins (rail 14, brand 16, ans 18, work 22, side 14, card 13) — no vertical armature can form.

Row budget: 3 group heads (24) + 8 nav rows (28) + 3 top-margins (24) = 368px.
`1fr` slot → **384px live tick tail**: 16 rows x 24px, 11px `--ink-4`, timestamp left / event right, amber only on a failure row. This is the rail's dead-space answer — a standing instrument, not padding.
Bottom **224 x 224**: the import-graph thumbnail, fixed, never changes with the selected view.

### 2.4 Cards — the four-layer recipe

The single largest structural change. Cards currently carry `border:1px solid #222831` (CR 1.36:1 against the panel) and `0 6px 18px -12px #000` (invisible on a #060709 ground by construction). Replace both:

```css
.card{
  background:var(--s-2);
  border:0;                        /* the ring replaces the border */
  border-radius:var(--r-card);
  padding:var(--card-pad-y) var(--card-pad-x);
  box-shadow:
    inset 0 0 0 1px var(--toplight-ring),   /* 1 inner light ring  */
    inset 0 1px 0 0 var(--toplight),        /* 2 the top light edge */
    0 0 0 1px var(--hair-dark),             /* 3 outer dark ring    */
    var(--sh-flat);                         /* 4 contact shadow     */
  transition:background-color var(--d-ho) var(--e-state) var(--d-ho-delay),
             box-shadow       var(--d-ho) var(--e-state) var(--d-ho-delay);
}
.card:hover{
  background:var(--s-3);           /* dL* +4.90 — the SURFACE moves, not the border */
  box-shadow:
    inset 0 0 0 1px var(--toplight-ring),
    inset 0 1px 0 0 rgba(255,255,255,0.080),
    0 0 0 1px var(--hair-dark),
    var(--sh-raise);
  transition-duration:var(--d-hi);transition-delay:0ms;
}
.card:active{background:var(--s-2);box-shadow:
  inset 0 0 0 1px var(--toplight-ring),inset 0 1px 3px 0 rgba(0,0,0,0.400),
  0 0 0 1px var(--hair-dark)}
.card.lit{                          /* fired — ONE per view, budget enforced */
  box-shadow:
    inset 2px 0 0 0 var(--am-fired),
    inset 0 0 0 1px var(--am-edge),
    inset 0 1px 0 0 var(--toplight),
    0 0 0 1px var(--hair-dark),
    0 0 20px -4px rgba(255,176,0,0.160);
}
.card.kill{background:var(--s-1);box-shadow:var(--sh-sunk)}
/* NOT opacity:.72 — that drags the text below the Lc30 floor.
   Recede by dropping the SURFACE and keep the ink legible. */

.well{background:var(--s-1);border-radius:var(--r-cell);box-shadow:var(--sh-sunk)}
.pop{background:var(--s-4);border-radius:var(--r-pop);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,0.102),
             inset 0 1px 0 0 rgba(255,255,255,0.090),
             0 0 0 1px var(--hair-dark),var(--sh-float)}
```

Hover changes the surface, never the border: `#10161f → #18202b` is `dL* +4.90` and reads instantly; brightening a hairline from 0.075 to 0.110 is a 1px change nobody sees. **No `translateY` lift, no `scale`** — in a 12px-gutter grid a 1px lift re-rasterises text AA on every hover.

**Rest opacity:** `.tag,.pill,.rail button .n{opacity:0.55;transition:opacity var(--d-ho) var(--e-state)}` → `1` on parent hover. Flatness is largely every element being equally present.

Card header, when a card has one:
```css
.card__hd{height:40px;margin:-12px -16px 12px;padding:0 16px;
  display:flex;align-items:center;justify-content:space-between;
  font-size:var(--fs-micro);line-height:16px;letter-spacing:var(--ls-micro);
  text-transform:uppercase;color:var(--ink-4);
  background:linear-gradient(180deg,rgba(255,255,255,0.022),rgba(255,255,255,0));
  box-shadow:inset 0 -1px 0 var(--hair-1)}
```

### 2.5 Tables — 24px rows

```css
.tbl{width:100%;border-collapse:collapse;table-layout:fixed;
     font-variant-numeric:tabular-nums lining-nums}
.tbl th{
  position:sticky;top:0;z-index:2;
  height:32px;padding:0 12px 0 0;text-align:left;font-weight:400;
  font-size:var(--fs-micro);line-height:var(--lh-micro);
  letter-spacing:var(--ls-micro);text-transform:uppercase;color:var(--ink-3);
  background:var(--s-2);
  box-shadow:inset 0 -1px 0 var(--hair-2),0 1px 2px rgba(1,4,9,0.600);
}
.tbl td{
  height:24px;padding:3px 12px 3px 0;line-height:var(--lh-row);
  vertical-align:middle;color:var(--ink-2);
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  box-shadow:inset 0 -1px 0 rgba(255,255,255,0.030);
}
.tbl td.r{text-align:right;color:var(--ink-1)}   /* digit ink raggedness at 13px = 0.69px */
.tbl td.u{color:var(--ink-5);font-size:var(--fs-micro)}
.tbl tbody tr{transition:background-color var(--d-ho) var(--e-state) var(--d-ho-delay)}
.tbl tbody tr:hover{background:rgba(255,255,255,0.028);
  transition-duration:var(--d-hi);transition-delay:0ms}
.tbl tbody tr[aria-selected="true"]{background:rgba(200,207,215,0.070)}
.tbl td:empty::after{content:"\2014";color:var(--ink-5)}
/* pinned widths so a column never reflows between views */
.tbl col.num{width:88px} .tbl col.pill{width:72px} .tbl col.state{width:64px}
```

Row = `3 + 18 + 3 = 24px` exactly. **Zebra is a 1px hairline per row, never a filled alternate background** — a filled stripe at 24px creates a visible banding beat at scroll speed.

State lives on a 2px inset rule on the first cell, so the row keeps its exact 24px box:

```css
tr[data-state="pass"]  td:first-child{box-shadow:inset 2px 0 0 var(--hair-2),
                                       inset 0 -1px 0 rgba(255,255,255,0.030)}
tr[data-state="live"]  td:first-child{box-shadow:inset 2px 0 0 var(--am-fired),
                                       inset 0 -1px 0 rgba(255,255,255,0.030)}
tr[data-state="fail"]{background:var(--am-bed)}
tr[data-state="fail"] td{color:var(--am-fired)}
tr[data-state="fail"] td:first-child{box-shadow:inset 2px 0 0 var(--am-fired),
                                       inset 0 -1px 0 rgba(255,255,255,0.030)}
tr[data-state="warn"]  td:first-child{box-shadow:inset 2px 0 0 var(--am-steady),
                                       inset 0 -1px 0 rgba(255,255,255,0.030)}
tr[data-state="stale"] td:first-child{box-shadow:inset 2px 0 0 var(--am-idle),
                                       inset 0 -1px 0 rgba(255,255,255,0.030)}
```

**The PASS state spends zero amber.** Neutral `--ink-3` text and a `--hair-2` left rule. Amber appearing at all must mean something changed. This is the only discipline that survives 43 law cards and 110 graph nodes; every alternative ends with an amber page.

### 2.6 Stat tiles — 6 across, span 2, 96px tall

```css
.tiles{grid-column:1/-1;display:grid;grid-template-columns:repeat(6,180px);
       gap:12px;height:96px}
.tile{display:flex;flex-direction:column;justify-content:center;gap:2px;
      padding:0 14px}                     /* .card recipe applies */
.tile .n{font-size:var(--fs-stat);line-height:var(--lh-stat);
  letter-spacing:var(--ls-stat);color:var(--ink-1);
  font-variant-numeric:tabular-nums lining-nums}
.tile.hot .n{color:var(--am-fired);
  text-shadow:var(--glow-core),var(--glow-mid),var(--glow-halo)}
.tile .k{font-size:var(--fs-micro);line-height:16px;letter-spacing:var(--ls-micro);
  text-transform:uppercase;color:var(--ink-3)}
.tile .s{font-size:var(--fs-micro);line-height:16px;color:var(--ink-5);
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
```

`6 x 180 + 5 x 12 = 1140` exactly. Height `32 + 16 + 16 = 64` + `16px` centred slack = 96.
Number is **left-aligned in its tile** — never right-aligned against other tiles.
`.tile .s` must not truncate mid-word (the current tile shows `gather_public, produce_bri`): if the string exceeds the box, drop to the first token plus a `+n` count.

### 2.7 Law cards — 43 of them, span 4

```css
.laws{display:grid;grid-template-columns:repeat(12,84px);gap:12px}
.law{grid-column:span 4;min-height:124px;display:flex;flex-direction:column;gap:8px}
.law .id{font-size:var(--fs-micro);line-height:16px;letter-spacing:var(--ls-micro);
  text-transform:uppercase;color:var(--ink-5);
  font-variant-numeric:tabular-nums}
.law .claim{font-size:var(--fs-claim);line-height:var(--lh-claim);color:var(--ink-1);
  max-width:var(--measure-max)}
.law .paid{font-size:var(--fs-body);line-height:var(--lh-row);color:var(--ink-4);
  padding-top:8px;box-shadow:inset 0 1px 0 var(--hair-1);margin-top:auto}
.law .paid::before{content:"PAID BY ";color:var(--ink-5);
  font-size:var(--fs-micro);letter-spacing:var(--ls-micro)}
@media (max-width:1500px){.law{grid-column:span 6}}   /* span 4 would be 32ch */
@media (min-width:2100px){.law{grid-column:span 3}}   /* span 4 would exceed 68ch */
```

`span 4 = 372px`; minus `32px` padding = `340px` = **47.6ch at 13px Consolas** — clears the 46ch measure floor. The as-built `minmax(280px,1fr)` gives `254px` = 40.2ch, which is why the law cards break into ragged two-word lines. `.paid` uses `--ink-4`, not amber: the quietest line in the card must not spend the fired state.

### 2.8 Verdict columns — FINISH / LATER / KILL

```css
.board3{display:grid;grid-template-columns:repeat(3,372px);gap:12px;align-items:start}
.col{background:var(--s-1);border-radius:var(--r-cell);box-shadow:var(--sh-sunk);
     padding:0 0 12px}
.col h3{height:40px;padding:0 16px;display:flex;align-items:center;
  justify-content:space-between;
  font-size:var(--fs-micro);line-height:16px;letter-spacing:var(--ls-micro);
  text-transform:uppercase;color:var(--ink-3);
  box-shadow:inset 0 -1px 0 var(--hair-1)}
.col h3 .n{font-size:var(--fs-body);color:var(--ink-1);
  font-variant-numeric:tabular-nums}
.col .item{margin:12px 12px 0}            /* .card recipe applies */

/* the three columns carry the verdict on the LEFT RULE, not on a hue */
.col[data-v="finish"] h3{box-shadow:inset 2px 0 0 var(--am-fired),
                                    inset 0 -1px 0 var(--hair-1)}
.col[data-v="finish"] h3 .n{color:var(--am-fired)}
.col[data-v="later"]  h3{box-shadow:inset 2px 0 0 var(--am-steady),
                                    inset 0 -1px 0 var(--hair-1)}
.col[data-v="kill"]   h3{box-shadow:inset 2px 0 0 var(--am-spent),
                                    inset 0 -1px 0 var(--hair-1)}
.col[data-v="kill"] .item{background:var(--s-1);box-shadow:var(--sh-sunk)}
.col[data-v="kill"] .item .title{color:var(--ink-4);
  text-decoration:line-through;text-decoration-color:var(--am-spent)}
```

The KILL column recedes by dropping to the recessed surface and adding a strikethrough — **shape carries the category**, never opacity, because opacity drags text under the legibility floor.

### 2.9 Proposal pips — 4 gates

```css
.pips{display:flex;gap:5px;align-items:center}
.pip{width:6px;height:6px;border-radius:1px;background:transparent;
     box-shadow:inset 0 0 0 1px var(--am-trace);
     transition:background-color var(--d-tap) var(--e-state),
                box-shadow       var(--d-tap) var(--e-state)}
.pip.on  {background:var(--am-fired);
          box-shadow:0 0 0 1px var(--am-edge),0 0 12px -3px rgba(255,176,0,0.160)}
.pip.fail{background:transparent;box-shadow:inset 0 0 0 1px var(--am-fired)}
.pip.na::after{content:"";display:block;width:6px;height:1px;margin-top:2.5px;
               background:var(--ink-5)}      /* absent gate = a dash, never a guess */
.pips .lab{margin-left:6px;font-size:var(--fs-micro);letter-spacing:var(--ls-micro);
           text-transform:uppercase;color:var(--ink-5)}
```

Filled = passed, hollow-amber = failed, trace-outline = not yet run, dash = not applicable. Four states on one hue, separated by fill/stroke/dash, never by colour alone.

### 2.10 Sparkline

Two sizes only: **13px inline** inside a kv row (word-sized, per Tufte), or **36px labelled chart** in a band. Nothing between. The current `.spark{height:34px}` with `i{flex:1}` and n=2 renders two full-width amber blocks that consume **46% of the entire amber budget on the page** while carrying two data points.

```js
function spark(cv, series){
  const dpr = Math.min(devicePixelRatio || 1, 2);
  const w = cv.clientWidth, h = cv.clientHeight;
  cv.width = Math.round(w*dpr); cv.height = Math.round(h*dpr);
  const g = cv.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0); g.clearRect(0,0,w,h);

  if (!series || series.length < 3){        // honesty law: 2 points is not a trend
    g.strokeStyle = 'rgba(255,255,255,0.055)';
    g.beginPath(); g.moveTo(0,h-0.5); g.lineTo(w,h-0.5); g.stroke();
    g.fillStyle = '#565d67'; g.font = '11px "IBM Plex Mono","Cascadia Mono",Consolas,monospace';
    g.fillText('\u2014 insufficient history', 0, h/2); return;
  }
  const mn=Math.min(...series), mx=Math.max(...series), sp=(mx-mn)||1, pad=3;
  const X=i=>(i/(series.length-1))*w, Y=v=>h-pad-((v-mn)/sp)*(h-pad*2);

  g.beginPath(); g.moveTo(0,h);                       // area, amber at 0.220 -> 0
  series.forEach((v,i)=>g.lineTo(X(i),Y(v)));
  g.lineTo(w,h); g.closePath();
  const lg=g.createLinearGradient(0,0,0,h);
  lg.addColorStop(0,'rgba(255,176,0,0.220)');
  lg.addColorStop(1,'rgba(255,176,0,0.000)');
  g.fillStyle=lg; g.fill();

  g.beginPath();                                      // stroke at the SECONDARY amber
  series.forEach((v,i)=> i ? g.lineTo(X(i),Y(v)) : g.moveTo(X(i),Y(v)));
  g.strokeStyle='#d4a24c'; g.lineWidth=1.5; g.lineJoin='round'; g.lineCap='round'; g.stroke();

  const lx=X(series.length-1), ly=Y(series[series.length-1]);
  g.fillStyle='#ffb000';                              // only the live value earns full amber
  g.beginPath(); g.arc(Math.round(lx)-2, ly, 2.5, 0, 6.2832); g.fill();
}
```

### 2.11 The periphery — 288 x 904

```css
.side{display:grid;grid-template-rows:auto auto auto 1fr 288px;align-content:start}
.side section{padding:16px}
.side h4{height:24px;line-height:24px;margin:0 0 8px;
  font-size:var(--fs-micro);letter-spacing:var(--ls-brand);
  text-transform:uppercase;color:var(--ink-4)}
.kv{height:24px;display:flex;align-items:center;justify-content:space-between;gap:8px;
    font-size:var(--fs-body);line-height:var(--lh-row);
    font-variant-numeric:tabular-nums}
.kv span{color:var(--ink-3)} .kv b{font-weight:400;color:var(--ink-1)}
.kv canvas{width:48px;height:13px}       /* word-sized inline spark */
.side .heat{height:288px;box-shadow:inset 0 1px 0 var(--hair-1);padding:16px}
```

Content, top to bottom:
1. **TOKEN USAGE** — 3 kv rows (24px each) + a 36px labelled sparkline canvas = 108px + head 32 = 140px.
2. **WAKE** — 4 kv rows each with a 13px inline spark = 96 + 32 = 128px.
3. **LOOPS** — burn-down (below) = 76px.
4. `1fr` = 272px → **pre-attentive strip**: 8 capability dots at 10px, arranged 8 across x 2 rows with 11px labels, encoding pass/fail by luminance. Reason: the current right rail is 20 text key-value pairs that require foveation, so glancing at it tells you nothing.
5. Bottom **288px** — tick heatmap: 24 cols x 7 rows of 10px cells at 1px gaps = 263 x 76, plus axis labels.

**Delete the periphery's "the ledger" section** — it duplicates the status view's capability table verbatim, truncated to 4 characters (`DRAF` / `WATC` / `FORB`). Duplicated content that must be mentally reconciled is extraneous load, and the truncation breaks the honesty law.

**Burn-down** (in the strip's periphery slot, and again here):

```css
.burn{padding:0 16px;display:flex;flex-direction:column;justify-content:center;gap:6px}
.burn .row{display:flex;justify-content:space-between;align-items:baseline;
  font-size:var(--fs-micro);letter-spacing:var(--ls-micro);
  text-transform:uppercase;color:var(--ink-4)}
.burn .row b{font-weight:400;font-size:var(--fs-body);color:var(--ink-1);
  font-variant-numeric:tabular-nums}
.burn .track{position:relative;height:6px;background:var(--s-1);border-radius:0;
  box-shadow:var(--sh-sunk);overflow:hidden}
.burn i{position:absolute;inset:0 auto 0 0;display:block;transform-origin:left center;
  transform:scaleX(var(--v,0));width:100%;
  transition:transform 400ms var(--e-emph)}
.burn .killed{background:var(--am-spent)}
.burn .done  {background:var(--am-steady)}
```

Killed counts as closed — taking work off the board IS closing a loop, so the bar opens at 9/24 = 37.5%, never at zero.

### 2.12 Focus ring — double ring with a ground-coloured spacer

```css
:where(a,button,[tabindex]):focus-visible{
  outline:none;
  box-shadow:0 0 0 2px var(--s-0),0 0 0 3px var(--am-fired),
             0 0 14px -2px rgba(255,176,0,0.220)}
.card :where(a,button,[tabindex]):focus-visible{
  box-shadow:0 0 0 2px var(--s-2),0 0 0 3px var(--am-fired)}
```

The inner ring is the *surface* colour, which punches a gap so the outer ring reads even when the element is flush against a neighbour.

---

## 3 · MOTION SPEC

### 3.1 Easing and duration table

| Token | Value | Applies to |
|---|---|---|
| `--e-state` | `cubic-bezier(0.2,0,0.38,0.9)` | hover, press, surface change, row wash |
| `--e-enter` | `cubic-bezier(0,0,0.38,0.9)` | card entrance, view arrival, tooltip in |
| `--e-exit` | `cubic-bezier(0.2,0,1,0.9)` | view leave, tooltip out, dismissal |
| `--e-view` | `cubic-bezier(0.55,0,0.1,1)` | full view swap (opacity + translate together) |
| `--e-decay` | `cubic-bezier(0,0,0.3,1)` | delta flash decay, phosphor ghost |
| `--e-overlay` | `cubic-bezier(0.32,0.72,0,1)` | popover, command palette, scrim |
| `--e-breathe` | `cubic-bezier(0.45,0,0.55,1)` | the LIVE dot loop (symmetric — the only correct curve for a loop) |
| `--e-emph` | `cubic-bezier(0.2,0,0,1)` | burn-down bar only. **Budget: one element on the page.** |

| Token | ms | Applies to |
|---|---|---|
| `--d-tap` | 70 | pip flip, checkbox, filter toggle |
| `--d-hi` | 90 | hover IN (surface + colour) |
| `--d-ho` | 140 | hover OUT, with `--d-ho-delay:30ms` |
| `--d-enter` | 150 | per-card entrance |
| `--d-view-out` | 90 | outgoing view |
| `--d-view-in` | 200 | incoming view |
| `--d-data` | 240 | bar/gauge retarget (`scaleX`, never `width`) |
| `--d-panel` | 300 | popover, drawer |
| `--d-phos` | 320 | phosphor ghost of a replaced number |
| `--d-flash` | 880 | delta wash decay |
| `--d-mark` | 1200 | 2px amber rail on a changed row |
| `--d-breathe` | 2400 | the LIVE dot, infinite |

Hard bans: `transition:all`; any duration >400ms inside the work area except `--d-flash`/`--d-mark`/`--d-breathe`; animating `width`, `height`, `top`, `left`, `margin`, `font-size`; tweening digit glyphs.

**Never tween a digit.** Swap `textContent` instantly and animate the container. A counting number in a ledger is unreadable mid-flight and displays values the system never reported — a soft honesty violation.

### 3.2 What animates

| Element | Property | Duration / easing |
|---|---|---|
| card, row, rail button | `background-color`, `box-shadow` | 90 in / 140 + 30ms delay out, `--e-state` |
| pip | `background-color`, `box-shadow` | 70, `--e-state` |
| view | `opacity`, `transform` | out 90 `--e-exit`, in 200 `--e-enter` |
| bar / burn-down | `transform:scaleX()` | 240 `--e-state` (400 `--e-emph` for burn) |
| changed cell | `@keyframes fl` wash + inset rail | 880 `--e-decay` |
| replaced number | ghost span `opacity` + `blur(0→1.6px)` | 320 `--e-decay` |
| LIVE dot | `opacity .45→1→.45` | 2400 `--e-breathe`, infinite |
| graph focus | canvas lerp | in 0.180/frame, out 0.080/frame |

**Exactly one perpetual animation exists on the page:** the LIVE dot breath. It stops and drops to `opacity:0.22` with `background:#6b7480` when the last poll is older than 2x the interval. Stillness has to mean dead.

Every other repeating motion is event-driven. Stop the entity and the page must go completely still within one poll interval. Rate-limit pulses to **one per 334ms** (3/second, the WCAG flash ceiling), per element and globally. Animation duration must be `<= 30%` of the poll interval.

If more than 8 cells change in one poll, suppress the per-cell flashes and flash the panel header once — a 40-cell ledger flashing in full is a strobe field.

### 3.3 Load sequence

```
strip     t=0ms    opacity only, 90ms,  30ms stagger over 3 answers → settles 146ms
centre    t=60ms   opacity + 4px rise, 150ms, 28ms stagger capped at 6 → settles 378ms
periphery t=120ms  opacity only, 150ms, 28ms stagger capped at 6 → settles 438ms
```

Last content pixel at **378ms**, under the 400ms flow threshold. The shell is opaque at frame 0 and never sequences. Stagger floor is 17ms (one frame at 60Hz — below that consecutive items commit in the same paint and the stagger does not exist); ceiling 40ms.

```css
.rise{opacity:0;transform:translateY(var(--rise));
  animation:rise var(--d-enter) var(--e-enter) var(--dly,0ms) both}
@keyframes rise{to{opacity:1;transform:none}}
.fade{opacity:0;animation:fade 90ms linear var(--dly,0ms) both}
@keyframes fade{to{opacity:1}}
```

```js
const SEQ = {strip:[0,'fade'], centre:[60,'rise'], periph:[120,'fade']};
const STAGGER = 28, CAP = 6;
document.querySelectorAll('[data-seq]').forEach(zone => {
  const [base, cls] = SEQ[zone.dataset.seq];
  [...zone.children].forEach((el, i) => {
    el.style.setProperty('--dly', base + Math.min(i, CAP) * STAGGER + 'ms');
    el.classList.add(cls);
    el.addEventListener('animationend', () => {
      el.classList.remove(cls);
      el.style.removeProperty('--dly');
      el.style.willChange = 'auto';        // never leave compositor layers behind
    }, {once:true});
  });
});
```

`will-change` on at most 6 elements at a time (matching `CAP`), removed on `animationend`. Never on the 43 law cards or the 110 graph nodes.

### 3.4 View swap — interruptible, scroll-preserving

```js
let swapToken = 0; const scrollPos = new Map();
function showView(next, viaKeyboard=false){
  const cur = document.querySelector('.view.on');
  if (cur === next) return;
  const me = ++swapToken, work = document.querySelector('.work');
  if (cur) scrollPos.set(cur.id, work.scrollTop);
  const finish = () => {
    if (me !== swapToken) return;
    if (cur) cur.classList.remove('on','leaving');
    next.classList.add('enter','on');
    work.scrollTop = scrollPos.get(next.id) || 0;
    if (viaKeyboard){ next.classList.remove('enter'); return; }   // no entrance on key nav
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
      if (me === swapToken) next.classList.remove('enter');
    }));
  };
  if (!cur) return finish();
  cur.classList.add('leaving');
  setTimeout(finish, 60);        // 60ms overlap of a 90ms exit — no dead frame
}
```

### 3.5 prefers-reduced-motion — the exact split

**Keep** every colour, elevation and surface value identical. Do not fall back to a flatter design — the depth model is static. **Keep** opacity fades and the delta flash (colour/opacity-only change that does not alter perceived position is explicitly excluded from "motion animation" by WCAG 2.3.3, so the page stays alive rather than going dead). **Kill** every transform, translate and scale, the LIVE breath, the phosphor ghost, and the canvas simulations.

```css
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{
    animation-duration:0.01ms!important;      /* 0.01 not 0 — animationend must fire
                                                 or the JS load sequence deadlocks */
    animation-iteration-count:1!important;
    transition-duration:0.01ms!important;
    scroll-behavior:auto!important;
  }
  :root{--rise:0px;--view-rise:0px;--view-sink:0px;--stagger:0ms}
  /* KEEP: the delta flash and view opacity */
  .fl{animation:fl 400ms linear both!important}
  .view.on{opacity:1;transition:opacity 120ms linear!important}
  /* KILL: the perpetual loop, frozen at the ON state — the truth is "this is live" */
  .live{animation:none!important;opacity:1}
  .ghost{display:none}
  .card.fresh::after{animation:none;display:none}
}
```

CSS media queries do not reach `requestAnimationFrame`. Gate every canvas in JS and subscribe to the `change` event:

```js
const RM = matchMedia('(prefers-reduced-motion: reduce)');
let raf = 0;
function sync(){
  cancelAnimationFrame(raf); raf = 0;
  if (RM.matches || document.hidden){ drawStatic(); return; }   // ONE static frame
  raf = requestAnimationFrame(loop);
}
RM.addEventListener('change', sync);
document.addEventListener('visibilitychange', sync);
addEventListener('resize', ()=>{ fit(); sync(); }, {passive:true});
sync();
```

Under reduce, the force graph runs **300 sim steps synchronously**, sets `alpha=0` and draws once — the reduced-motion viewer sees the same finished picture, not a blank one.

**Delete `setTimeout(()=>location.reload(), 300000)` (board.html L161).** A hard reload every 5 minutes destroys scroll position, hover and reading position — an ejection mechanic on a page whose entire goal is dwell. Replace with a 60s fetch + regional DOM patch keyed on a `data-stamp` body attribute; if the stamp is unchanged, touch nothing.

---

## 4 · ATMOSPHERE SPEC

Four layers, in this z-order: `#field` (0) → `#grain` (1) → `.app` (2).

### 4.1 The field — lift the centre, do not darken the edge

On `#060709` a black vignette has **6 sRGB code values of headroom** and is invisible; a white-family lift has 249. Depth on near-black is built by lifting, then darkening the corners *against the lift*.

```css
#field{position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    /* 1 · the light source, one only, above the top strip */
    radial-gradient(128% 104% at 50% 30%,
      rgba(122,140,164,0.055) 0%,
      rgba(122,140,164,0.022) 34%,
      rgba(122,140,164,0.000) 72%),
    /* 2 · one warm pool under the bottom band — the dead-space depth cue */
    radial-gradient(52% 40% at 50% 88%,
      rgba(255,176,0,0.020) 0%,
      rgba(255,176,0,0.000) 100%),
    /* 3 · the vignette, contrast against the LIFT, never against the ground */
    radial-gradient(150% 120% at 50% 30%,
      rgba(0,0,0,0.000) 55%,
      rgba(0,0,0,0.340) 84%,
      rgba(0,0,0,0.620) 100%);
}
```

Measured: the centre composites `#060709 → #0c0e12` (CR 1.042:1); the corners stay `#060709`. The amber pool at alpha 0.020 shifts the ground `+5/+3/+0` code values — far below any threshold at which it could be misread as a lit state.

**Amber in the atmosphere plane is capped at alpha 0.100 fill / 0.030 halo.** The current ambient canvas draws lit nodes at 0.16 — above some *instrument* amber, which destroys both the depth model and the meaning of the accent.

### 4.2 Grain — inlined SVG, one paint, no JS loop

The field gradient spans ~10 sRGB code values and **will** band on an 8-bit panel. The grain is the dither. It is also the cheapest fix for "nothing rewards looking at it" — texture at the pixel level reads as material.

```css
:root{
  --grain:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='g' x='0' y='0' width='100%25' height='100%25'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch' seed='7'/%3E%3CfeColorMatrix type='matrix' values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0.2126 0.7152 0.0722 0 0'/%3E%3CfeComponentTransfer%3E%3CfeFuncA type='table' tableValues='0 0 0.28 1'/%3E%3C/feComponentTransfer%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23g)'/%3E%3C/svg%3E");
}
#grain{position:fixed;inset:0;z-index:1;pointer-events:none;
  background-image:var(--grain);
  background-size:var(--grain-px) var(--grain-px);
  opacity:0.42}
.card{background-image:var(--grain),linear-gradient(180deg,#131924,#0e141c);
  background-size:var(--grain-px) var(--grain-px),auto;
  background-blend-mode:overlay,normal}
```

```js
// lock one noise unit to one device pixel: grain coarser than the 1.3px stem of
// 13px mono attacks the glyph edges and reads as dirt.
document.documentElement.style.setProperty('--grain-px',
  (140 / Math.min(2, window.devicePixelRatio || 1)) + 'px');
```

`tableValues='0 0 0.28 1'` is load-bearing: raw `fractalNoise` has mean luminance ~0.5, so unshaped grain at opacity 0.42 lifts the black floor ~6 code values and turns `#060709` into `#0c0d0f`. The shaped alpha keeps mean lift `<= 2` code values with a p99 of 9-12.

**Do not animate the grain.** A full-viewport `background-position` change repaints a composited layer every frame for zero information, on a page meant to be left open all day, and static screen-space patterns *swim* under motion. One legal exception: step the tile 3 positions 90ms apart when a real tick lands.

### 4.3 Glow — a four-stop ladder, never a single blur

Radius steps ~x3 (`1 / 7 / 26 / 64`), alpha falls ~x0.45 (`0.400 / 0.150 / 0.070 / 0.030`), hue clips toward white at the core and reddens outward (`#ffce7a → #ffb000 → #ff8a00 → #ff7800`). Derived from a 5-mip bloom chain compressed to 4 CSS stops; the compression is why radius steps x3 rather than x2.

```css
.hot,.ans .val.hot,.tile.hot .n{color:var(--am-fired);
  text-shadow:var(--glow-core),var(--glow-mid),var(--glow-halo),var(--glow-far)}
```

**Delete `text-shadow:0 0 22px rgba(255,176,0,.35)` (board.html L76).** A single-hue single-radius glow is the 2015 neon tell.

Every glow carries a **1px hard contact ring** beneath it (`--am-glow` includes `0 0 0 1px rgba(255,176,0,0.220)`). Real emitters have a sharp boundary; a halo with no edge is the strongest "cheap" signal available. Cap the outermost *visible* stop at **1.5x the cap-height** of the type it sits on (26px at a 28px numeral); anything wider must drop to alpha `<= 0.030`, at which point it is a field gradient, not a halo.

Negative spread confines the halo: `0 10px 26px -16px rgba(0,0,0,0.900)` — the spread shrinks the shadow rect *before* blur, so a 26px blur never crosses the 12px grid gutter.

### 4.4 Phosphor persistence — atmosphere that is also evidence

The highest-value single mechanic here, because it survives the honesty law: it fires only when a real value changed.

```css
.val,.tile .n,.kv b{position:relative}
.ghost{position:absolute;left:0;top:0;color:var(--am-fired);pointer-events:none;
  white-space:pre;animation:phos var(--d-phos) var(--e-decay) forwards}
@keyframes phos{0%{opacity:0.55;filter:blur(0)}100%{opacity:0;filter:blur(1.6px)}}
```

```js
function setLive(el, next){
  if (el.textContent === String(next)) return;
  const g = document.createElement('span');
  g.className = 'ghost'; g.textContent = el.textContent;
  el.parentNode.appendChild(g); setTimeout(()=>g.remove(), 340);
  el.textContent = next;                       // digits swap INSTANTLY, never tween
}
```

### 4.5 The earned scanline — 420ms, once, on real data

```css
.card.fresh{overflow:hidden;position:relative}
.card.fresh::after{content:'';position:absolute;inset:0;pointer-events:none;
  background:repeating-linear-gradient(180deg,
    rgba(150,170,195,0.030) 0 1px, rgba(0,0,0,0) 1px 3px);
  mask-image:linear-gradient(180deg,transparent,#000 18%,#000 82%,transparent);
  -webkit-mask-image:linear-gradient(180deg,transparent,#000 18%,#000 82%,transparent);
  animation:sweep 420ms linear 1 forwards}
@keyframes sweep{0%{transform:translateY(-102%);opacity:0}
                 12%{opacity:1}100%{transform:translateY(102%);opacity:0}}
```

Light lines at 3px period, not dark — dark lines on `#060709` have no headroom, and a 2px period beats against the 1.3px stems of 13px mono and moirés on scroll. **Ambient scanlines are banned.**

### 4.6 Rejected outright

- **Chromatic aberration.** Per-channel offset manufactures red and cyan fringes by construction — a second and third hue on a page whose law permits one.
- **`filter:blur()` on any animating canvas.** Full-viewport GPU pass per frame. Get the same soft edge for free by drawing points as 2-stop radial sprites.
- **Ambient drift tied to frame count.** `k += 0.0035` per rAF gives a 29.9s period at 60Hz and 12.5s at 144Hz — the atmosphere's speed is currently a function of the user's monitor. Use `(now % 42000) / 42000 * 2π`. Peak drift velocity must stay under **20px/s** (≈0.5 deg/s at 60cm / 96dpi) or it crosses from soft fascination into motion capture.
- **Any element appearing abruptly.** Ambient fades in over `>= 700ms` and never animates scale. Abrupt onsets capture attention involuntarily; gradual onsets do not.

### 4.7 Acceptance gate

Screenshot at 1700x1000, apply a **6px gaussian**, and three planes must still separate: field / chrome / instruments. If they merge, the depth is in the borders, not in the composition. Then read the 400% greyscale crop and check the histogram, not the mean — grain that lifts the black floor by more than 2 code values is dirt.

---

## 5 · GRAPH SPEC — 110 nodes, ~440 edges

### 5.1 Layout runs in Python, at generation time

Ship precomputed coordinates. Zero force iterations on load. Watching a graph settle is a loading screen, not a wow moment. Keep a "re-settle" button that runs the solver live for anyone who wants it.

Two phases:
- **A** — ~10 package meta-nodes, weight `sqrt(memberCount)`, springs weighted by inter-package edge count, repulsion `/d²`, 240 iterations.
- **B** — members inside a disc of radius `0.052*sqrt(m)`. **Nodes with external edges are PINNED on the rim at `0.82R`, at the angle pointing to the centroid of their external partners.** Only internal-only nodes relax, 300 iterations, repulsion evaluated within the package only.

Phase B's rim pinning is the single highest-leverage change: every long edge then leaves from the correct side of its cluster, so cross-package traffic becomes a small number of legible trunks instead of 440 chords through the centre. The current single global pass with packages anchored on a fixed circle **is** the hairball.

### 5.2 Ink

```js
const G = {
  stage:'#05070a',                 // 2 steps BELOW the card ground: a well, not a panel
  nodeCold:'#12161c',              // ALWAYS lighter than the stage. Darker = a hole.
  line:'126,138,156', amber:'255,176,0', amberDeep:'212,162,76',
  aIntra:0.040, aInter:0.085, aSpine:0.200, aFocus:0.820, aMute:0.014,
  wIntra:0.65,  wInter:0.95,  wSpine:1.25,  wFocus:1.75,
  kIntra:0.110, kInter:0.170,      // control-point offset / chord length
  strokeCold:'rgba(126,138,156,0.420)',
  strokeWarm:'rgba(212,162,76,0.620)',
  hullFill:'rgba(126,138,156,0.022)', hullEdge:'rgba(126,138,156,0.055)',
  plate:'rgba(5,7,10,0.720)', label:'rgba(198,206,218,0.860)',
  labelDim:'#565d67', labelMax:22
};
```

Continuous alternative to the three tiers: `alpha = 0.030 + 0.170 * w^0.65`, `width = 0.60 + 1.10*w` px, where
`w = clamp01(0.30*isInterPackage + 0.45*litMin + 0.25*(log2(1+min(outdeg_src,indeg_dst))/6))`.
The 0.65 exponent, not 1.0, because alpha is perceptually compressive near black — a linear ramp erases the middle tier entirely.

### 5.3 Batched tiered edges — the highest-impact change

Measured: two crossing segments inside **one** stroked path composite to 77/255 at `globalAlpha 0.30` — identical to a single line. The same two as **separate** `stroke()` calls give 130/255. The current code strokes 440 times, so every crossing compounds and the core turns to mud.

```js
const DPR = Math.min(devicePixelRatio || 1, 2);
const TAPER_MIN = 24 * DPR, TAPER_SPAN = 120 * DPR;

function strokeTier(rgb, alpha, width, k, list, back){
  if (!list.length) return;
  cx.strokeStyle = `rgba(${rgb},${(alpha*back).toFixed(3)})`;
  cx.lineWidth = width * DPR; cx.lineCap = 'round';
  cx.beginPath();
  for (let i=0;i<list.length;i++){
    const e = list[i], [x1,y1] = px(e[0]), [x2,y2] = px(e[1]);
    const dx = x2-x1, dy = y2-y1, len = Math.hypot(dx,dy) || 1;
    cx.moveTo(x1,y1);
    const kk = k * Math.min(1, Math.max(0, (len - TAPER_MIN) / TAPER_SPAN));
    if (kk < 0.004){ cx.lineTo(x2,y2); continue; }   // short edges draw dead straight
    // apex of a quadratic = 0.5*(M+C), so the visible sagitta is exactly kk*len/2.
    // ALWAYS the left normal: uniform chirality is what makes the field read as
    // authored, and it separates reciprocal A->B / B->A pairs for free.
    cx.quadraticCurveTo(x1 + dx*0.5 - dy*kk, y1 + dy*0.5 + dx*kk, x2, y2);
  }
  cx.stroke();
}
```

Cross-package edges get Holten bundling on a 4-point control polygon, `beta = 0.85`, hubs at `t = 0.220` from each package centroid. **Bundle only across boundaries** — bundling inside a cluster destroys the local structure phase B exists to expose.

```js
const BETA = 0.85, HUB_T = 0.220;
function bundledEdge(p, q, Cp, Cq){
  const [x1,y1] = px(p), [x2,y2] = px(q);
  let h1x = Cp[0] + (Cq[0]-Cp[0])*HUB_T, h1y = Cp[1] + (Cq[1]-Cp[1])*HUB_T;
  let h2x = Cq[0] + (Cp[0]-Cq[0])*HUB_T, h2y = Cq[1] + (Cp[1]-Cq[1])*HUB_T;
  const lx = i => x1 + (x2-x1)*i/3, ly = i => y1 + (y2-y1)*i/3;
  h1x = BETA*h1x + (1-BETA)*lx(1); h1y = BETA*h1y + (1-BETA)*ly(1);
  h2x = BETA*h2x + (1-BETA)*lx(2); h2y = BETA*h2y + (1-BETA)*ly(2);
  cx.moveTo(x1,y1); cx.bezierCurveTo(h1x,h1y,h2x,h2y,x2,y2);   // caller batches
}
```

### 5.4 Node layering — halo sprite → disc → stroke → label

Bake the glow **once** to a 128px offscreen canvas with four stops. Measured: 0.189ms/frame for 110 live `createRadialGradient` calls vs **0.083ms** for sprite `drawImage`.

```js
function glowSprite(rgb, peak){
  const S=128, s=document.createElement('canvas'); s.width=s.height=S;
  const g=s.getContext('2d'), rg=g.createRadialGradient(S/2,S/2,0,S/2,S/2,S/2);
  rg.addColorStop(0.00,`rgba(${rgb},${peak.toFixed(3)})`);          // four stops:
  rg.addColorStop(0.28,`rgba(${rgb},${(peak*0.380).toFixed(3)})`);  // approximates
  rg.addColorStop(0.55,`rgba(${rgb},${(peak*0.100).toFixed(3)})`);  // 1/(1+(d/d0)^2).
  rg.addColorStop(1.00,`rgba(${rgb},0)`);                           // two stops fall
  g.fillStyle=rg; g.fillRect(0,0,S,S); return s;                    // off linearly and
}                                                                   // read cheap.
const HALO = glowSprite('255,176,0', 0.340), HALO_R = 4.6;

function radius(d){ return Math.max(3.0, Math.min(13.0, 0.62*Math.sqrt(d.m.lines))); }

function drawNode(d, back){          // back = 1.000 at rest, 0.120 when backgrounded
  const [x,y] = px(d);
  const scale = back < 1 ? 0.92 + 0.08*back : 1;   // size + alpha together = distance
  const r = radius(d) * DPR * Math.sqrt(zoom) * scale, l = d.lit;
  if (l > 0.02){
    const s = r * HALO_R * 2 * Math.min(1, l + 0.15);
    cx.globalAlpha = l * back * 0.100;             // atmosphere amber cap
    cx.drawImage(HALO, (x-s/2)|0, (y-s/2)|0, s|0, s|0);   // integer dest for drawImage
    cx.globalAlpha = 1;
  }
  cx.beginPath(); cx.arc(x, y, r, 0, 6.2832);      // paths stay float: rounding them
  cx.fillStyle = l > 0.02                          // stair-steps the curve
    ? `rgba(255,176,0,${((0.220 + 0.780*l)*back).toFixed(3)})`
    : `rgba(18,22,28,${back.toFixed(3)})`;
  cx.fill();
  cx.lineWidth = 0.9 * DPR;
  cx.strokeStyle = l > 0.02 ? `rgba(255,176,0,${(0.950*back).toFixed(3)})`
    : d.m.reachable_from_server ? `rgba(212,162,76,${(0.620*back).toFixed(3)})`
    : `rgba(126,138,156,${(0.420*back).toFixed(3)})`;
  cx.stroke();
}
```

### 5.5 The frame — depth is a function of attention

```js
let focus = null, fMix = 0;
const EASE_IN = 0.180, EASE_OUT = 0.080;   // 95% arrival in 267ms in / 600ms out
const NBR = new Map();
for (const [a,b] of E){
  if(!NBR.has(a)) NBR.set(a,new Set()); if(!NBR.has(b)) NBR.set(b,new Set());
  NBR.get(a).add(b); NBR.get(b).add(a);
}

function frame(){
  const target = focus ? 1 : 0;
  fMix = RM.matches ? target : fMix + (target - fMix) * (focus ? EASE_IN : EASE_OUT);
  const back = 1 - 0.880 * fMix;          // 1.000 -> 0.120

  cx.clearRect(0,0,W,H);
  drawRegions(back);                       // package hulls, behind everything

  const near = focus ? NBR.get(focus) : null;
  const b = {intra:[],inter:[],spine:[],focus:[],mute:[]};
  for (const e of E){
    if (focus){
      const hot = e[0]===focus || e[1]===focus || (near.has(e[0]) && near.has(e[1]));
      b[hot?'focus':'mute'].push(e);
    } else b[e.tier].push(e);
  }
  strokeTier(G.line , G.aMute , G.wIntra*0.85, G.kIntra, b.mute , 1);
  strokeTier(G.line , G.aIntra, G.wIntra     , G.kIntra, b.intra, back);
  strokeTier(G.line , G.aInter, G.wInter     , G.kInter, b.inter, back);
  strokeTier(G.amberDeep, G.aSpine, G.wSpine , G.kInter, b.spine, back);
  strokeTier(G.amber, G.aFocus, G.wFocus     , G.kInter, b.focus, 1);

  // THE WELL — after edges, before nodes. Eats the peripheral edge haze while
  // leaving node discs and halos at full strength. This is what makes a foreground.
  const S = Math.min(W,H);
  const v = cx.createRadialGradient(W/2,H/2,S*0.34,W/2,H/2,S*0.92);
  v.addColorStop(0,'rgba(0,0,0,0)'); v.addColorStop(1,'rgba(0,0,0,0.550)');
  cx.fillStyle = v; cx.fillRect(0,0,W,H);

  for (const d of N) drawNode(d, (focus && d!==focus && !near.has(d)) ? back : 1);
  drawLabels(labelCandidates());           // labels LAST, never inside the node loop
  if (!RM.matches || focus || fMix > 0.001) raf = requestAnimationFrame(frame);
}
```

### 5.6 Package hulls — the region layer that kills the hairball read

```js
function convexHull(pts){                  // Andrew monotone chain
  const p = pts.slice().sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  if (p.length < 3) return p;
  const cr=(o,a,b)=>(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0]);
  const lo=[],up=[];
  for(const q of p){while(lo.length>1&&cr(lo[lo.length-2],lo[lo.length-1],q)<=0)lo.pop();lo.push(q);}
  for(let i=p.length-1;i>=0;i--){const q=p[i];
    while(up.length>1&&cr(up[up.length-2],up[up.length-1],q)<=0)up.pop();up.push(q);}
  lo.pop(); up.pop(); return lo.concat(up);
}
function drawRegions(back){
  cx.lineJoin='round'; cx.lineCap='round';
  for (const p of PKGS){
    const h = convexHull(MEMBERS[p].map(px)); if (h.length < 3) continue;
    cx.beginPath();
    cx.moveTo((h[0][0]+h[1][0])/2,(h[0][1]+h[1][1])/2);
    for (let i=1;i<=h.length;i++){                       // corner-rounded hull
      const a=h[i%h.length], b=h[(i+1)%h.length];
      cx.quadraticCurveTo(a[0],a[1],(a[0]+b[0])/2,(a[1]+b[1])/2);
    }
    cx.closePath();
    cx.lineWidth = 18*DPR;                               // inflate ~9px by fat stroke
    cx.strokeStyle = `rgba(126,138,156,${(0.022*back).toFixed(3)})`; cx.stroke();
    cx.fillStyle   = `rgba(126,138,156,${(0.022*back).toFixed(3)})`; cx.fill();
    cx.lineWidth = 1*DPR;
    cx.strokeStyle = `rgba(126,138,156,${(0.055*back).toFixed(3)})`; cx.stroke();
  }
  cx.lineJoin='miter';
}
```

### 5.7 Labels — capped at 22, AABB collision, backing plate

Show for: hovered/selected + its 1-hop neighbours (priority 100/80), nodes with `r >= 7.5px` (40+r), any node at `zoom > 1.7` (10+r). Sort descending, place greedily, reject on AABB overlap with 3px*DPR padding, hard cap 22. Font `10.5px` — never below 10px on canvas, there is no subpixel AA. Every label gets a `rgba(5,7,10,0.720)` plate, `3px*DPR` horizontal padding, `13px*DPR` tall, drawn at integer coordinates. Cache `measureText` widths on the node.

### 5.8 Framing and idle

```css
.stage{position:absolute;inset:0;background:#05070a;overflow:hidden}
.stage::after{content:'';position:absolute;inset:0;pointer-events:none;
  box-shadow:inset 0 0 120px 40px rgba(0,0,0,0.550),
             inset 0 1px 0 0 rgba(126,138,156,0.070)}
#g{display:block;width:100%;height:100%;cursor:grab}
#g:active{cursor:grabbing}
.hud,.legend,.ctl{position:absolute;z-index:2}   /* HUD floats OVER the canvas */
```

**The graph is the ground of its view, full-bleed to the column edges.** The current map view is an iframe inside a bordered card inside a column — three nested frames, which is itself the flat, empty read.

Idle model: cancel the rAF when `alpha <= 0.005` and there is no focus; resume on `pointermove`, `visibilitychange`, or a real data delta (`reheat alpha = 0.30`). Throttle idle redraws (hover hit-test, tooltip) to 33.33ms. Cap DPR at 2. Target **3ms per draw** for 110 nodes — RAIL gives 10ms of app work per 16ms frame, and the DOM polling shares that thread. Open devtools performance on an idle board: expect zero scripting frames.

---

## 6 · LAYOUT AT 1700 x 1000 — SOLVING THE DEAD SPACE

### 6.1 The armature

```css
.work{padding:20px 24px 48px;overflow-y:auto;
  /* column guides, barely there — an armature without a data-free box */
  background-image:repeating-linear-gradient(90deg,
    var(--guide) 0 1px, transparent 1px var(--pitch));
  background-position:24px 0;
  background-size:calc(100% - 48px) 100%;
  background-repeat:no-repeat}
.bands{display:grid;grid-template-columns:repeat(12,84px);
       gap:12px;align-content:start}
.sp1{grid-column:span 1}  .sp2{grid-column:span 2}  .sp3{grid-column:span 3}
.sp4{grid-column:span 4}  .sp5{grid-column:span 5}  .sp6{grid-column:span 6}
.sp7{grid-column:span 7}  .sp12{grid-column:1/-1}
```

`span n = 96n − 12`px → 84 / 180 / 276 / 372 / 468 / 564 / 660 / 1140.

### 6.2 Every region at 1700 x 1000

```
┌ 0,0 ──────────────────────────── 1700 x 96 · STRIP ───────────────────────────┐
│ 224 BRAND        │ 1188 THREE ANSWERS (3 x 372 + 2 x 12, pad 24)  │ 288 LIVE  │
│ wordmark 11/16   │ eyebrow 11/16 · value 34/38 · sub 13/18        │ dot+age   │
│ uptime  13/18    │ broken · changed · next                        │ burn bar  │
└──────────────────┴────────────────────────────────────────────────┴───────────┘
┌ 0,96 ─ 224 x 904 RAIL ─┬─ 1188 x 904 WORK ────────────┬─ 288 x 904 PERIPHERY ─┐
│ h4 SYSTEM       24     │ pad 20 / 24 / 48             │ TOKEN USAGE     140   │
│  3 nav rows     84     │ live area 1140 x 836         │  3 kv + 36px spark    │
│ h4 WORK   +24   48     │                              │ WAKE            128   │
│  3 nav rows     84     │ band 1 TILES        96       │  4 kv + inline sparks │
│ h4 STRUCT +24   48     │  gap                12       │ LOOPS            76   │
│  2 nav rows     56     │ band 2 LEDGER SM    228      │  burn-down            │
│ ── 368 total ──        │  gap                12       │ ── 344 ──             │
│                        │ band 3 TABLES       288      │ 1fr = 272             │
│ 384 TICK TAIL          │  gap                12       │  PRE-ATTENTIVE STRIP  │
│  16 rows x 24          │ band 4 GRAPH        228      │  8 dots x 2 rows      │
│  11px, amber on fail   │ ── 876; 40px CLIPPED ──      │                       │
│                        │                              │ 288 TICK HEATMAP      │
│ 224 GRAPH THUMB        │                              │  24 x 7 x 10px cells  │
└────────────────────────┴──────────────────────────────┴───────────────────────┘
```

### 6.3 Band contents (STATUS view)

| # | Span | H | Content |
|---|---|---|---|
| 1 | 12 | 96 | 6 stat tiles at span 2 (180px each), 12px gutters |
| 2 | 12 | 228 | **Capability ledger as small multiples** — 12 canvas cells across (84 x 36) x 3 rows at 60px pitch, 11px label + run count under each = 36 capabilities |
| 3 | 5 / 7 | 288 | Invariants table (468px, 2 cols) beside the capability ledger table (660px, 4 cols) — side by side they consume 12 of 12 columns |
| 4 | 12 | 228 | Import-graph strip, full-bleed canvas well, HUD floating over it |

`96 + 12 + 228 + 12 + 288 + 12 + 228 = 876` against an 836px live area → **the graph strip is clipped 40px below the fold**. That is deliberate: content terminating flush with the fold signals "there is nothing else here"; 40px of a cut-off band is the promise of more.

### 6.4 Small multiples — the primary dead-space fix

```js
const CELL_W=84, CELL_H=36, GUT=12, LABEL=16, PITCH=CELL_H+LABEL+8;   // 60
function drawLedger(cv, items){
  const dpr = Math.min(2, devicePixelRatio||1);
  const cols = Math.max(1, Math.floor((cv.clientWidth + GUT) / (CELL_W + GUT)));
  const rows = Math.ceil(items.length / cols), h = rows*PITCH - 8;
  cv.width = Math.round(cv.clientWidth*dpr); cv.height = Math.round(h*dpr);
  cv.style.height = h + 'px';
  const g = cv.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
  g.font = '11px "IBM Plex Mono","Cascadia Mono",Consolas,monospace';
  g.textBaseline = 'top';
  items.forEach((it,i)=>{
    const x = (i%cols)*(CELL_W+GUT), y = Math.floor(i/cols)*PITCH;
    g.fillStyle='#0a0e14'; g.fillRect(x,y,CELL_W,CELL_H);              // the well
    g.fillStyle='#1a1f28'; g.fillRect(x,y+CELL_H-1,CELL_W,1);         // baseline rule
    const n = it.series.length||1, max = Math.max(1,...it.series);
    const bw = Math.max(1, Math.floor((CELL_W-(n-1))/n));             // INTEGER bars
    for (let k=0;k<n;k++){
      const bh = Math.round((it.series[k]/max)*(CELL_H-6));
      g.globalAlpha = (k===n-1) ? 1 : 0.62;
      g.fillStyle   = (k===n-1) ? '#ffb000' : '#9c7a3c';   // only the last is fired
      g.fillRect(x+k*(bw+1), y+CELL_H-1-bh, bw, bh);
    }
    g.globalAlpha = 1;
    g.fillStyle = '#98a1ad'; g.fillText(it.name.slice(0,11), x, y+CELL_H+4);
    const r = String(it.runs);
    g.fillStyle = it.fails ? '#ffb000' : '#565d67';
    g.fillText(r, x + CELL_W - g.measureText(r).width, y+CELL_H+4);
  });
}
new ResizeObserver(()=>drawLedger(cv,DATA)).observe(cv);
```

### 6.5 The density gate — falsifiable, not eyeballed

Peak legibility sits at **30-40% character-cell fill**. At 1700x1000 the centre is `1140/7.15 = 159` cols x `836/24 = 34` rows = **5406 cells**, so the target is **1620-2160 visible glyphs**. The current STATUS view renders ~600 (≈11%). Ship gate: no view renders under 1500 glyphs; if it does, it recruits a small-multiples band or the graph strip before it ships. No view leaves more than 96px of empty centre below its last band.

```js
function fill(sel='.work'){
  const el=document.querySelector(sel), cs=getComputedStyle(el);
  const adv=parseFloat(cs.fontSize)*0.5498, row=24;   // Consolas advance
  const r=el.getBoundingClientRect();
  const padX=parseFloat(cs.paddingLeft)+parseFloat(cs.paddingRight);
  const cols=Math.floor((r.width-padX)/adv), rows=Math.floor(r.height/row);
  let glyphs=0; const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
  while(w.nextNode()){
    const p=w.currentNode.parentElement;
    if(!p||getComputedStyle(p).display==='none') continue;
    glyphs+=w.currentNode.nodeValue.replace(/\s+/g,' ').trim().length;
  }
  const out={cols,rows,cells:cols*rows,glyphs,fill:+(glyphs/(cols*rows)).toFixed(3)};
  console.table(out); return out;
}
function origins(){                       // must return <= 3 distinct left edges
  const xs=new Set();
  document.querySelectorAll('.work *,.rail *,.side *').forEach(n=>{
    const b=n.getBoundingClientRect(); if(b.width) xs.add(Math.round(b.left));
  });
  console.log('distinct left edges:', xs.size, [...xs].sort((a,b)=>a-b));
}
```

### 6.6 Breakpoints

| Width | Change |
|---|---|
| `< 1180` | drop the periphery (centre would fall under 8 columns) |
| `< 1500` | law cards go `span 6` (span 4 would be 273px = 32ch, under the measure floor) |
| `> 2100` | law cards go `span 3` (span 4 would exceed 68ch) |

`.work > .view{max-width:1680px}` caps the work area so type never sets past its measure on a 3840px display, and the grid makes real columns of the remaining width instead of dead space. One exception: `#v-map{max-width:none}` — the graph genuinely wants the full width.

---

## 7 · PSYCHOLOGY RATIONALE

Each item names the decision it justifies.

1. **The page is BELOW the arousal peak, not above it.** 97.03% of the rendered frame sits in luminance band 0-31; 49.9% of the centre column is empty. Every "declutter / use whitespace" instinct is backwards here. → Justifies §6 (fill to 1620-2160 glyphs, small-multiples band, tick tail in the rail, pre-attentive strip in the periphery) rather than removing anything.

2. **Common region overrides proximity, and a hairline is the weakest region cue that exists.** Grouping must be carried by a FILL. → Justifies `--s-2 #10161f` at `dL* 5.17` over the ground and the four-layer ring recipe replacing `border:1px solid #222831` (§2.4).

3. **Three of five current surfaces are within the JND of each other** (`dL* 1.40 / 1.31 / 2.03`). The eye cannot resolve five levels, so it resolves none. → Justifies the `>= 2.5 dL*` floor, the 6-token ladder, and the rule capping *visible* levels at three per view (§1).

4. **Processing fluency drives liking, and figure-ground contrast is a direct fluency lever.** → Justifies hover moving the SURFACE (`dL* +4.90`) instead of the border (a 1px change nobody perceives) (§2.4).

5. **Low colourfulness AND low complexity both predicted higher appeal at 500ms exposure.** The two-ink law is already the research-optimal palette choice — the deficit is structural density, not hue. → Justifies spending the entire complexity budget on structure and refusing a second hue anywhere, including rejecting chromatic aberration (§4.6).

6. **Dwell hazard is front-loaded**: the risk of leaving peaks in the opening seconds and drops sharply after. → Justifies spending the whole entrance budget inside 378ms with a 28ms stagger, and putting the strip at t=0 with no delay (§3.3).

7. **First-impression judgement at 50ms correlates ~r=0.9 with 500ms judgement, and needs a focal peak to latch onto.** Nothing on the current frame exceeds 25px; 0.03% of pixels are above L=224. → Justifies `--fs-hero:34px` at `2.62x` body in the strip and the four-stop glow ladder on the one hot value (§2.2, §4.3).

8. **Prospect-refuge:** the shell is refuge, the centre is prospect. Refuge must not move. → Justifies the shell painting opaque at frame 0 and never animating, the rail and periphery never reflowing on view change, and deleting the 5-minute `location.reload()` — a hard reload is an ejection mechanic on a page whose whole goal is dwell (§2.1, §3.5).

9. **Mystery — the promise of more information if you move into the scene.** Content terminating flush with the fold says "there is nothing else here". → Justifies the 40px clip on the bottom graph band and the 10th ledger row rendering half-cut (§6.3).

10. **Soft fascination holds attention while leaving room for reflection; abrupt onset and looming capture it involuntarily.** → Justifies the 20px/s ambient velocity ceiling, the 700ms minimum ambient fade, the ban on ambient scale animation, and the 42,000ms wall-clock drift period replacing a frame-counted one (§4.6).

11. **Calm technology moves information between centre and periphery.** 20 text key-value pairs in the right rail require foveation, so glancing tells you nothing — the exact opposite of peripheral. → Justifies encoding at least three periphery values as pre-attentive marks (luminance dot row, inline sparks, tick heatmap), detected in <250ms independent of set size (§2.11).

12. **The redundancy effect: duplicated content that must be mentally reconciled is extraneous load.** The periphery's "ledger" section repeats the status table verbatim, truncated to 4 characters. → Justifies deleting it, and justifies the "display tier renders numbers and short tokens only, never truncated prose" rule — which is also a honesty-law fix, since a truncated string is not the value (§2.2, §2.11).

13. **Interrupted tasks create tension that suppresses return unless a loop is seen to close; endowed progress raised completion 19% → 34% for identical real work.** Three counts (5 FINISH / 10 LATER / 9 KILL) are all tension and no release. → Justifies the burn-down that counts KILL as closed, opening at 37.5% rather than zero (§2.11).

14. **The one-loop budget.** A second perpetual animation turns the page into wallpaper and the first one stops carrying meaning. → Justifies exactly one infinite animation (the LIVE breath), everything else event-driven, and stillness meaning dead (§3.2).

15. **Amber spent on the passing state destroys the accent.** The current sparkline burns 46% of the page's entire amber budget on a two-bar chart in the periphery. → Justifies the PASS state spending zero amber, the six-state hue-locked ramp with shape carrying category, and the 3-point minimum before a sparkline draws anything (§2.5, §2.10).

---

## 8 · IMPLEMENTATION ORDER — 12 CHANGES BY VISUAL RETURN PER LINE

All edits in `aea/tooling/board.py` unless noted. Line numbers approximate against the current 504-line file; verify with a fresh read before editing. Screenshot at exactly 1700x1000 with `--use-angle=swiftshader` and **read the PNG** after each of 1, 2, 4, 6 and 9.

| # | Change | File · lines | Return |
|---|---|---|---|
| 1 | **Replace the `:root` block wholesale** with §1. Six surfaces at `dL* >= 2.5`, alpha hairlines, six-step ink ramp, six-state amber, six integer type sizes, the 4px lattice. | `board.py` L157-170 | The single largest change. Every other item depends on it. ~120 lines, fixes the flat ladder, the 12-size type mush, and the failing `--dim` label colour at once. |
| 2 | **Card recipe → the four layers** (§2.4). Delete `border:1px solid var(--line2)` and `0 6px 18px -12px #000`; add inner ring + top light + outer dark ring + `--sh-flat`. Hover moves `background` to `--s-3`. | `board.py` L~215-225 (`.card`) | ~14 lines. This is what makes a flat rectangle read as a physical top face. Hover becomes perceptible for the first time. |
| 3 | **Row and shell geometry to integers.** `td{height:24px;line-height:18px;padding:3px 12px 3px 0}`, `th{height:32px}`, `.kv{height:24px}`, rail button 28px, strip 96px, rail 224px, periphery 288px, work pad `20px 24px 48px`. | `board.py` L157-170, L188, L236, L~260 | ~20 lines. Kills the 27.15px fractional row that makes every 1px rule composite at a different alpha. Unlocks the 84px column. |
| 4 | **The field + grain layers** (§4.1, §4.2). Add `#field` and `#grain` divs with the three-stop lift, the amber pool, the vignette, and the inlined feTurbulence data URI; one JS line to lock `--grain-px` to the device pixel. | `board.py` (new markup + ~14 CSS lines + 2 JS lines) | Highest atmosphere-per-line on the page. Gives the empty centre material texture and dithers the ground gradient's 10-code-value banding. |
| 5 | **12-column centre grid + band tiling** (§6.1-6.3). Replace `.g3{repeat(auto-fill,minmax(280px,1fr))}` with `repeat(12,84px)` + explicit spans; law cards `span 4`; band heights from `{96,168,228,288,384}`. | `board.py` L209, view emitters | ~25 lines. Takes law cards from 40.2ch (ragged two-word lines) to 47.6ch, and gives the whole page one armature. |
| 6 | **Capability ledger → small multiples band** (§6.4). Replace the table emitter with a 12-across canvas band. | `board.py` view emitter, +40 JS lines | The primary dead-space fix: converts ~9 rows of 4-column table into 36 legible capability histories in a 228px band. |
| 7 | **Motion tokens + load sequence + reduced-motion** (§3). Add the easing/duration set, the `.rise`/`.fade` classes, the `[data-seq]` JS, the interruptible `showView`, and the full `@media (prefers-reduced-motion:reduce)` block plus the JS `matchMedia` gate. | `board.py` L~172 (`.view` keyframe), + ~45 lines | The page currently has **two** transitions total and **zero** reduced-motion handling with an unconditional rAF loop. This is both the life and the accessibility fix. |
| 8 | **Delete `location.reload()`; ship fetch + regional DOM patch** keyed on `data-stamp`, 60s interval, with a 1400ms calm flash on changed regions. | generated JS at `board.html` L161 → emitter | ~25 lines. Removes the single most dwell-hostile line in the file. |
| 9 | **Graph: batched tier strokes + sprite glow + vignette-between-edges-and-nodes** (§5.3-5.5). Replace the 440 per-edge `stroke()` calls with 5 batched paths; replace the per-node `createRadialGradient` with one baked 128px sprite. | `aea/tooling/xray_graph.py` L136-154 | Measured 130/255 → 77/255 on crossings (the core stops turning to mud) and 0.189ms → 0.083ms per frame. Turns a hairball into a picture. |
| 10 | **Graph: two-phase precomputed layout with rim pinning** (§5.1). New `aea/tooling/xray_layout.py`; emit coordinates into the page; zero force ticks on load. | new file ~90 lines; `xray_graph.py` L63-98 deleted | First frame is final. Every long edge leaves from the correct side of its cluster. |
| 11 | **Top strip: hero tier + truncation kill** (§2.2). 34px tabular value, 11px eyebrow, 13px sub with `-webkit-line-clamp:1`; never render truncated prose at display size; em-dash for absent. Same fix on `.tile .s` and the periphery ledger (delete it). | `board.py` L171-181, L~230 | ~15 lines. Gives the page its only focal peak and removes three honesty-law truncations. |
| 12 | **Rail tick tail + periphery pre-attentive strip + burn-down** (§2.3, §2.11). 16 x 24px live tick rows in the rail's `1fr`; 8 luminance dots in the periphery's `1fr`; killed-counts-as-closed burn bar. | `board.py` L~185-200, L~255-270 | ~35 lines. Converts 384px of dead rail and 272px of dead periphery into standing instruments, and closes the Zeigarnik loop. |

**Verification, per the repo's own law:** a change is done when the server restarted, the 1700x1000 PNG was shot and read, `fill()` returned `>= 0.30` on every view, `origins()` returned `<= 3` distinct left edges, `grep 'font-size:\d\+\.'` returned zero matches, and the 6px-gaussian blur test still separates three planes.