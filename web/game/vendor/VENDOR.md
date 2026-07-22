# game/vendor — THIRD-PARTY CODE QUARANTINE

Everything in this folder is VENDOR code: three.js r128 (Copyright 2010-2021 Three.js
Authors, MIT license) — the core build plus its official examples/js post-processing and
control addons. NONE of it is first-party; NONE of it is ever edited (byte-identical to
upstream r128). Our code lives in game/js and is written from scratch under the
anti-anchor law (BOOK ledger #32).

| file | what it is |
|---|---|
| three.min.js | three.js r128 core, UMD global build |
| EffectComposer.js / RenderPass.js / ShaderPass.js / CopyShader.js / LuminosityHighPassShader.js / UnrealBloomPass.js | the official r128 post-processing chain (bloom) |
| OrbitControls.js | official r128 camera addon (harness/debug use only) |

Load order is law (E1): three.min.js -> CopyShader -> LuminosityHighPass -> EffectComposer
-> ShaderPass -> RenderPass -> UnrealBloomPass. The root-level copies of these files remain
ONLY because the legacy views (/world, /city, /mind) load them flat; they retire with the
legacy views at parity (tracked in the registry).
