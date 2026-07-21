/* engine.js — scene, atmosphere, ground, world, probe, flight, loop.
   Governance: E2_VISUAL_DIRECTION.md (Move 5 FIRST: sRGB tail + sub-1/255 dither, tune
   once post-gamma; Move 6 photographic horizon; §2 tells = review law) ·
   E1_CODE_ARCHITECTURE.md §2.2 (init(GAME)/dispose(), no cross-module globals),
   §3.1 (dispose checklist: geometries/materials/textures tracked; timers+listeners are
   resources; context-loss pair -> CARRIER LOST) · A11_SIGNATURE.md (two-ink law, the one
   image, scarcity budget) · A4 (bloom locked 0.65/0.4/0.5; ACES + exposure 1.1 is a
   decision, not a default — E2 §4.1).
   r128 law: sRGBEncoding exists, outputColorSpace does NOT; composer targets are linear,
   so the LAST pass does the sRGB encode (E2 §3.9). */
window.ENGINE = (function () {
  "use strict";

  var GAME, renderer, scene, camera, composer, bloomPass, finalPass, clock, raf = null;
  var skyMat, running = false, elapsed = 0;

  /* ---- resource registry (E1 §3.1: every geometry/material/texture/listener/timer owned) ---- */
  var R = { geoms: [], mats: [], texs: [], listeners: [], timers: [] };
  function geo(g) { R.geoms.push(g); return g; }
  function mat(m) { R.mats.push(m); return m; }
  function tex(t) { R.texs.push(t); return t; }
  function listen(target, type, fn) { target.addEventListener(type, fn); R.listeners.push([target, type, fn]); return fn; }
  function timer(id) { R.timers.push(id); return id; }

  /* ---- palette: authored display-space, linearized ONCE (E2 Move 5 — the sRGB tail
     restores the tuned look by construction; custom shader uniforms pre-linearized) ---- */
  function lin(hex) { return new THREE.Color(hex).convertSRGBToLinear(); }
  var INK = {
    voidC:    lin(0x050a10),   /* zenith / the void            */
    horizon:  lin(0x0b141d),   /* fog == clear == horizon base */
    cold:     lin(0x24394a),   /* structure-ink luminance band (Move 6) */
    structure:lin(0x789baf),   /* rgba(120,155,175) — the structure ink */
    warm:     lin(0xd4a24c),
    hot:      lin(0xffb000)
  };
  /* T-066 EMISSIVE-TUNE substrate: tiers verified post-gamma, never re-tuned pre-gamma */
  var EMISSIVE = { idle: 0.35, fired: 1.0 };

  /* ---- final pass: LinearToSRGB + interleaved-gradient-noise dither, amplitude
     under 1/255 (E2 §3.7/§3.8 — sub-perceptual banding repair, never visible style) ---- */
  var FinalShader = {
    uniforms: { tDiffuse: { value: null } },
    vertexShader:
      "varying vec2 vUv;" +
      "void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
    fragmentShader:
      "uniform sampler2D tDiffuse; varying vec2 vUv;" +
      "void main(){" +
      "  vec4 c = texture2D(tDiffuse, vUv);" +
      "  vec3 l = clamp(c.rgb, 0.0, 1.0);" +
      "  vec3 s = mix(l*12.92, 1.055*pow(l, vec3(1.0/2.4)) - 0.055, step(vec3(0.0031308), l));" +
      "  float n = fract(52.9829189 * fract(dot(gl_FragCoord.xy, vec2(0.06711056, 0.00583715))));" +
      "  gl_FragColor = vec4(s + (n - 0.5) * (1.0/255.0), c.a);" +
      "}"
  };

  /* ---- sky: authored photographic horizon (E2 Move 6 + §4.1 authored-sky law).
     ShaderMaterial skips the renderer's tone map, so the r128 ACES curve is inlined —
     sky and fogged ground must pass the SAME curve or the horizon seams. ---- */
  var SkyShader = {
    vertexShader:
      "varying vec3 vPos;" +
      "void main(){ vPos = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
    fragmentShader:
      "uniform vec3 uZenith, uHorizon, uCold, uWarm;" +
      "uniform float uBand, uExposure;" +
      "varying vec3 vPos;" +
      "vec3 rrt(vec3 v){ vec3 a = v*(v+0.0245786)-0.000090537; vec3 b = v*(0.983729*v+0.4329510)+0.238081; return a/b; }" +
      "vec3 aces(vec3 c){" +
      "  const mat3 mi = mat3(0.59719,0.07600,0.02840, 0.35458,0.90834,0.13383, 0.04823,0.01566,0.83777);" +
      "  const mat3 mo = mat3(1.60475,-0.10208,-0.00327, -0.53108,1.10813,-0.07276, -0.07367,-0.00605,1.07602);" +
      "  c *= uExposure / 0.6; return clamp(mo * rrt(mi * c), 0.0, 1.0);" +
      "}" +
      "void main(){" +
      "  float h = normalize(vPos).y;" +
      "  float up = clamp(h, 0.0, 1.0);" +
      "  vec3 col = mix(uHorizon, uZenith, pow(up, 0.55));" +          /* authored ramp, no default */
      "  col += uCold * pow(1.0 - abs(h), 10.0) * 0.35;" +             /* graded luminance band above the line (Move 6) */
      "  col += uWarm * pow(max(1.0 - abs(h - 0.012), 0.0), 60.0) * uBand;" + /* breathing amber band, capped 0.10-0.18 (A11 §4.1) */
      "  gl_FragColor = vec4(aces(col), 1.0);" +
      "}"
  };

  function buildAtmosphere() {
    scene.fog = new THREE.FogExp2(INK.horizon.getHex(), 0.011); /* fog color == clear color == horizon (E2 §4.1) */
    renderer.setClearColor(INK.horizon, 1);

    skyMat = mat(new THREE.ShaderMaterial({
      side: THREE.BackSide, depthWrite: false, fog: false,
      uniforms: {
        uZenith: { value: INK.voidC }, uHorizon: { value: INK.horizon },
        uCold: { value: INK.cold }, uWarm: { value: INK.warm },
        uBand: { value: 0.14 }, uExposure: { value: 1.1 }
      },
      vertexShader: SkyShader.vertexShader, fragmentShader: SkyShader.fragmentShader
    }));
    var dome = new THREE.Mesh(geo(new THREE.SphereGeometry(820, 48, 30)), skyMat);
    dome.name = "sky";
    scene.add(dome);
  }

  function skyUpdate(t) {
    /* the one sanctioned atmospheric breath, capped 0.10-0.18 (A11 §4.1); phase-fixed in ?still */
    skyMat.uniforms.uBand.value = 0.14 + 0.04 * Math.sin(t * 0.5);
  }

  /* ---- THE GROUND (E2 Move 1): no GridHelper, ever — the floor cites the map.
     Concentric structure-ink hairlines centered on the nexus, STATIC at idle (the
     Guardian's ruling: ring motion is event-only), fading by distance; plus the
     world-space value-noise term (Taste B1, ±3% luminance, xz-stable so it cannot swim). ---- */
  var NEXUS = { x: 0, z: 26 };            /* world anchors — the proven coordinates */
  var FOUNDRY = { x0: -113, x1: 113, z: 70, sites: 15 };
  var SOCKET = { x: 106, z: 78 };

  function buildGround() {
    var gmat = mat(new THREE.MeshStandardMaterial({
      color: lin(0x071018), roughness: 0.96, metalness: 0.0
    }));
    gmat.onBeforeCompile = function (sh) {
      sh.uniforms.uNexus = { value: new THREE.Vector2(NEXUS.x, NEXUS.z) };
      sh.uniforms.uInk = { value: INK.structure };
      sh.vertexShader = "varying vec3 vWpos;\n" + sh.vertexShader.replace(
        "#include <begin_vertex>",
        "#include <begin_vertex>\n vWpos = (modelMatrix * vec4(transformed, 1.0)).xyz;");
      sh.fragmentShader = (
        "varying vec3 vWpos;\nuniform vec2 uNexus;\nuniform vec3 uInk;\n" +
        "float vhash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }\n" +
        "float vnoise(vec2 p){ vec2 i = floor(p); vec2 f = fract(p); f = f*f*(3.0-2.0*f);\n" +
        "  return mix(mix(vhash(i), vhash(i+vec2(1.0,0.0)), f.x), mix(vhash(i+vec2(0.0,1.0)), vhash(i+vec2(1.0,1.0)), f.x), f.y); }\n" +
        sh.fragmentShader
          .replace("#include <color_fragment>",
            "#include <color_fragment>\n" +
            "  diffuseColor.rgb *= 1.0 + (vnoise(vWpos.xz * 0.16) - 0.5) * 0.06;\n")
          .replace("#include <emissivemap_fragment>",
            "#include <emissivemap_fragment>\n" +
            "  float rd = length(vWpos.xz - uNexus);\n" +
            "  float rm = mod(rd, 22.0);\n" +
            "  float ring = 1.0 - smoothstep(0.0, 0.55, min(rm, 22.0 - rm));\n" +
            "  totalEmissiveRadiance += uInk * ring * exp(-rd * 0.0065) * 0.05;\n"));
    };
    var ground = new THREE.Mesh(geo(new THREE.PlaneGeometry(1800, 1800)), gmat);
    ground.rotation.x = -Math.PI / 2;
    ground.name = "ground";
    scene.add(ground);

    /* the void's own light: dim, cool, authored — silhouettes read against fog, not albedo */
    scene.add(new THREE.HemisphereLight(0x24394a, 0x050a10, 0.7));
  }

  /* ---- THE WORLD (minimal per E4 §13: the nexus gains the slab — P0's only world
     addition; everything else is the proven coordinate frame rendered under E2 law).
     Move 2: vertical vertex-color gradients — base into the ground shadow, barely
     lighter at silhouette top. Even spacing broken by deterministic jitter (tell §2.4).
     Windows: sparse, warm, few — idle amber belongs to the SOCKET only (A11 §4.1:
     amber is earned; the socket earned it at FIRST LIGHT). Slab: dark, waiting
     (E4 §4 — an unrun bench has earned none). Roads: Move 7 structure-ink idle,
     per-strip CanvasTexture falloff ramp — never uniform neon, never amber. ---- */

  function hash01(n) { var s = Math.sin(n * 127.31) * 43758.5453; return s - Math.floor(s); }

  /* one unit mass, vertex-color gradient authored once, scaled per site (Move 2) */
  function unitMassGeometry() {
    var g = geo(new THREE.BoxGeometry(1, 1, 1, 1, 4, 1));
    var pos = g.attributes.position, col = [];
    for (var i = 0; i < pos.count; i++) {
      var t = pos.getY(i) + 0.5;                       /* 0 base .. 1 top */
      var k = 0.35 + 0.6 * Math.pow(t, 1.5);           /* darker into the ground shadow */
      if (t > 0.94) k *= 1.22;                          /* the barely-lighter top band */
      col.push(k, k, k);
    }
    g.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
    return g;
  }

  function rampTexture(stops) {
    /* 1D alpha ramp for road strips (Move 7: UV falloff baked per strip) */
    var c = document.createElement("canvas"); c.width = 1; c.height = 64;
    var x = c.getContext("2d"), gr = x.createLinearGradient(0, 0, 0, 64);
    stops.forEach(function (s) { gr.addColorStop(s[0], "rgba(255,255,255," + s[1] + ")"); });
    x.fillStyle = gr; x.fillRect(0, 0, 1, 64);
    return tex(new THREE.CanvasTexture(c));
  }

  function buildWorld() {
    var massGeo = unitMassGeometry();
    var massMat = mat(new THREE.MeshStandardMaterial({
      color: lin(0x17242f), roughness: 0.92, metalness: 0.0, vertexColors: true
    }));

    /* the foundry row — 15 sites on the proven line, spacing broken deterministically */
    var span = FOUNDRY.x1 - FOUNDRY.x0;
    for (var i = 0; i < FOUNDRY.sites; i++) {
      var bx = FOUNDRY.x0 + (span * i) / (FOUNDRY.sites - 1) + (hash01(i + 1) - 0.5) * 7;
      var bz = FOUNDRY.z + (hash01(i + 31) - 0.5) * 9;
      var masses = 1 + Math.floor(hash01(i + 61) * 3);   /* 1..3 stacked masses per site */
      for (var m2 = 0; m2 < masses; m2++) {
        var h = 9 + hash01(i * 7 + m2 * 13 + 2) * 26 * (m2 === 0 ? 1 : 0.55);
        var w = 5 + hash01(i * 11 + m2 * 17 + 3) * 9;
        var d = 5 + hash01(i * 13 + m2 * 19 + 4) * 4;
        var mesh = new THREE.Mesh(massGeo, massMat);
        mesh.scale.set(w, h, d);
        mesh.position.set(bx + (m2 ? (hash01(i + m2 * 43) - 0.5) * (w + 6) : 0), h / 2, bz + (m2 ? (hash01(i + m2 * 53) - 0.5) * 5 : 0));
        scene.add(mesh);
      }
    }

    /* THE SOCKET (+106, 78) — the keyless plant that answered first; its sparse warm
       windows are the frame's only idle amber (earned at FIRST LIGHT, A11 §5) */
    var sock = new THREE.Mesh(massGeo, massMat);
    sock.scale.set(8, 13, 6); sock.position.set(SOCKET.x, 6.5, SOCKET.z);
    scene.add(sock);
    var winGeo = geo(new THREE.PlaneGeometry(0.8, 1.15));
    var winMat = mat(new THREE.MeshStandardMaterial({
      color: lin(0x0a0806), emissive: INK.warm, emissiveIntensity: EMISSIVE.idle
    }));
    [[-2.2, 8.6], [1.4, 7.1], [-0.6, 5.2], [2.4, 4.0], [-2.0, 2.6]].forEach(function (wpos) {
      var wq = new THREE.Mesh(winGeo, winMat);
      wq.position.set(SOCKET.x + wpos[0], wpos[1], SOCKET.z + 3.02);
      scene.add(wq);
    });

    /* the nexus slab (0, 26) — dark, waiting; spine = one structure-ink hairline */
    var slab = new THREE.Mesh(geo(new THREE.BoxGeometry(12, 1.1, 7)),
      mat(new THREE.MeshStandardMaterial({ color: lin(0x060b12), roughness: 0.9 })));
    slab.position.set(NEXUS.x, 0.55, NEXUS.z);
    scene.add(slab);
    var spineMat = mat(new THREE.MeshBasicMaterial({ color: lin(0x2a3b47) }));
    var spine = new THREE.Mesh(geo(new THREE.PlaneGeometry(11.2, 0.12)), spineMat);
    spine.rotation.x = -Math.PI / 2;
    spine.position.set(NEXUS.x, 1.115, NEXUS.z);
    scene.add(spine);

    /* roads as wires — structure ink at idle, falloff per strip (Move 7); the trunk
       visibly wires the slab into the grid (E4 GRAFT-B2) */
    function strip(wdt, len, cx, cz, alongX, ramp) {
      var mtl = mat(new THREE.MeshBasicMaterial({
        color: lin(0x3a4f5e), transparent: true, opacity: 0.55,
        alphaMap: ramp, depthWrite: false
      }));
      var p = new THREE.Mesh(geo(new THREE.PlaneGeometry(wdt, len)), mtl);
      p.rotation.x = -Math.PI / 2;
      if (alongX) p.rotation.z = Math.PI / 2;
      p.position.set(cx, 0.06, cz);
      scene.add(p);
    }
    strip(1.2, 40, NEXUS.x, (NEXUS.z + 4 + FOUNDRY.z - 2) / 2, false,
      rampTexture([[0, 0.95], [0.55, 0.5], [1, 0.22]]));                 /* nexus -> row */
    strip(1.0, span + 14, 0, FOUNDRY.z + 6, true,
      rampTexture([[0, 0.15], [0.5, 0.7], [1, 0.15]]));                  /* the row trunk */
    strip(1.0, 10, SOCKET.x, FOUNDRY.z + 6 + 5, false,
      rampTexture([[0, 0.2], [1, 0.75]]));                               /* spur to the socket */
  }

  /* ---- THE PROBE + FLIGHT (A11 §2: never the biggest thing in frame, always the
     most certain — warm shell, pooled in its own point light, range 30; emissive
     tamed per the GPU lesson: real bloom runs far hotter than swiftshader).
     Handling triple is law (E1/A4): accel 95 · damping exp(-3.1dt) · vmax 52. ---- */
  var probe, probeLight;
  var FLIGHT = { accel: 95, damp: 3.1, vmax: 52 };
  var vel = new THREE.Vector3(), yaw = 0, pitch = -0.06;
  var keys = {}, dragging = false, lastX = 0, lastY = 0, controlsLive = false;

  /* THE PROBE — built to B7_probe_hardware (PH-01 A11-CORE) anatomy, at canon scale:
     1.2 m total span (03_TECHNICAL_TARGETS). Concept sheets replaced the turnaround —
     the design language was extracted straight into geometry (E5 §1: hero forms are
     primitives; a drawing between concept and code buys nothing when the modeller is us).
     Parts: octahedral core · ring-drive gimbal (2 rings, crossed axes) · 4 axial fins ·
     amber core aperture. Amber lives ONLY at the aperture (A11 amber census). */
  var probeAperture, probeGimbal = [];
  function buildProbe() {
    probe = new THREE.Group();
    var R = 0.6;                                     /* half-span: 1.2 m total */

    /* 1. CORE — dark faceted body, NOT an emitter (the sticker lesson) */
    probe.add(new THREE.Mesh(geo(new THREE.OctahedronGeometry(R * 0.72)),
      mat(new THREE.MeshStandardMaterial({
        color: lin(0x11141c), emissive: INK.warm, emissiveIntensity: 0.10,
        roughness: 0.45, metalness: 0, flatShading: true
      }))));

    /* 2. CORE APERTURE — the single amber source, at the geometric centre, facing forward */
    probeAperture = new THREE.Mesh(geo(new THREE.CircleGeometry(R * 0.19, 6)),
      mat(new THREE.MeshBasicMaterial({ color: lin(0xffb000) })));
    probeAperture.position.z = R * 0.50;             /* sits in the forward facet */
    probe.add(probeAperture);

    /* 3. RING-DRIVE GIMBAL — two thin rings on crossed axes (B7: ring drive gimbal) */
    [[0, 0, 0], [Math.PI / 2, 0, Math.PI / 2.6]].forEach(function (rot, i) {
      var ring = new THREE.Mesh(geo(new THREE.TorusGeometry(R * (0.92 - i * 0.13), 0.012, 6, 44)),
        mat(new THREE.MeshStandardMaterial({
          color: lin(0x0d1017), emissive: INK.warm,
          emissiveIntensity: 0.22, roughness: 0.5, metalness: 0
        })));
      ring.rotation.set(rot[0] + Math.PI / 2, rot[1], rot[2]);
      probeGimbal.push(ring); probe.add(ring);
    });

    /* 4. FOUR AXIAL FINS — thin tapered blades on the equator, 90 deg apart (B7: axial fin x4) */
    var finGeo = new THREE.CylinderGeometry(0.006, 0.055, R * 0.66, 3);
    for (var f = 0; f < 4; f++) {
      var fin = new THREE.Mesh(geo(finGeo),
        mat(new THREE.MeshStandardMaterial({
          color: lin(0x141821), roughness: 0.55, metalness: 0, flatShading: true
        })));
      var a = f * Math.PI / 2 + Math.PI / 4;
      fin.position.set(Math.cos(a) * R * 0.60, 0, Math.sin(a) * R * 0.60);
      fin.rotation.z = Math.PI / 2; fin.rotation.y = -a;
      probe.add(fin);
    }

    probeLight = new THREE.PointLight(lin(0xd4a24c).getHex(), 1.3, 30);
    probe.add(probeLight);
    probe.position.set(0, 9, 150);   /* the proven spawn */
    probe.name = "probe";
    scene.add(probe);
  }

  function flightUpdate(dt) {
    if (dt === 0) { probe.rotation.y = 0.6; return; }  /* still frames: fixed pose */
    probe.rotation.y += dt * 0.5;  /* self-rotation — the player's body (A4 §9 closed table) */
    if (!controlsLive) return;
    var f = new THREE.Vector3(-Math.sin(yaw), 0, -Math.cos(yaw));
    var r = new THREE.Vector3(-f.z, 0, f.x);
    var a = new THREE.Vector3();
    if (keys.w) a.add(f);
    if (keys.s) a.sub(f);
    if (keys.d) a.add(r);
    if (keys.a) a.sub(r);
    if (keys.q) a.y += 1;
    if (keys.e) a.y -= 1;
    if (a.lengthSq() > 0) vel.addScaledVector(a.normalize(), FLIGHT.accel * dt);
    vel.multiplyScalar(Math.exp(-FLIGHT.damp * dt));
    if (vel.length() > FLIGHT.vmax) vel.setLength(FLIGHT.vmax);
    probe.position.addScaledVector(vel, dt);
    if (probe.position.y < 1.6) probe.position.y = 1.6;
  }

  function chaseCam(dt, snap) {
    /* the camera is a damped instrument — steady enough to be believed (A11 §6.6) */
    var off = new THREE.Vector3(Math.sin(yaw) * 16, 6.5 - pitch * 10, Math.cos(yaw) * 16);
    var tgt = probe.position.clone().add(off);
    camera.position.lerp(tgt, snap ? 1 : 1 - Math.exp(-4 * dt));
    camera.lookAt(probe.position.clone().add(
      new THREE.Vector3(-Math.sin(yaw) * 24, -1 + pitch * 26, -Math.cos(yaw) * 24)));
  }

  /* ---- boot composition (the one image, A11 §2: probe lower third, horizon high,
     the dark field owns the frame; still camera = the official portrait pose) ---- */
  var STILL = {
    /* aimed a touch right so the socket's earned windows sit in the frame's right
       third (A11 §2: one or two warm windows on the dark row, middle distance) */
    camPos: new THREE.Vector3(0, 12.5, 172),
    lookAt: new THREE.Vector3(22, 7, 40)
  };
  var bootEase = false;

  function titleShow() {
    var t = document.getElementById("title");
    if (t) t.classList.remove("out");
  }
  function titleHide() {
    var t = document.getElementById("title");
    if (t) t.classList.add("out");
  }
  function hintsLive(settled) {
    /* keys arrive HERE, in flight — never a legend wall (E2 §6 title law; 04 §1
       clauses 1-2: loud window 12s from controls-live, then quiet permanently) */
    var h = document.getElementById("hints");
    if (!h) return;
    h.innerHTML = "<span>W A S D FLY</span><span>Q E RISE FALL</span><span>DRAG LOOK</span>";
    if (!settled) {
      h.classList.add("loud");
      timer(setTimeout(function () { h.classList.remove("loud"); }, 12000));
    }
  }

  function controlsGoLive() {
    if (controlsLive) return;
    controlsLive = true;
    titleHide();
    hintsLive(false);
  }

  function bindInput() {
    listen(window, "keydown", function (e) {
      if (!controlsLive) { controlsGoLive(); return; }
      keys[e.key.toLowerCase()] = true;
    });
    listen(window, "keyup", function (e) { keys[e.key.toLowerCase()] = false; });
    listen(renderer.domElement, "mousedown", function (e) {
      if (!controlsLive) { controlsGoLive(); return; }
      dragging = true; lastX = e.clientX; lastY = e.clientY;
    });
    listen(window, "mouseup", function () { dragging = false; });
    listen(window, "mousemove", function (e) {
      if (!dragging) return;
      yaw -= (e.clientX - lastX) * 0.003;
      pitch = Math.max(-0.5, Math.min(0.5, pitch + (e.clientY - lastY) * 0.002));
      lastX = e.clientX; lastY = e.clientY;
    });
  }

  function onResize() {
    var w = window.innerWidth, h = window.innerHeight;
    camera.aspect = w / h; camera.updateProjectionMatrix();
    renderer.setSize(w, h); composer.setSize(w, h);
  }

  function loop() {
    raf = requestAnimationFrame(loop);
    if (!running) return;
    var dt = Math.min(clock.getDelta(), 0.05);
    if (GAME.state.flags.still) { dt = 0; } else { elapsed += dt; }
    skyUpdate(elapsed);
    flightUpdate(dt);
    if (!GAME.state.flags.still) {
      if (controlsLive) {
        chaseCam(dt, false);
      } else {
        /* boot ease: the camera settles onto the official portrait while the title breathes */
        var k = 1 - Math.exp(-0.9 * dt);
        camera.position.lerp(STILL.camPos, k);
        camera.lookAt(STILL.lookAt);
      }
    }
    GAME.frame(dt, elapsed); /* frame-hook seam (E1 §2.1) — future modules register here */
    composer.render();
  }

  function init(game) {
    GAME = game;
    clock = new THREE.Clock();

    renderer = new THREE.WebGLRenderer({ antialias: false, powerPreference: "high-performance" });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(1);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;   /* a decision, not a default (E2 §4.1) */
    renderer.toneMappingExposure = 1.1;
    /* outputEncoding stays Linear: the composer's LAST pass does the sRGB encode (E2 Move 5) */
    document.body.appendChild(renderer.domElement);

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 2000);
    camera.position.copy(STILL.camPos);
    camera.lookAt(STILL.lookAt);

    /* HalfFloat chain target: the default 8-bit target quantizes the LINEAR scene before
       the sRGB tail, which no sub-1/255 dither can repair — banding law, E2 §2 tell 6 */
    composer = new THREE.EffectComposer(renderer, new THREE.WebGLRenderTarget(
      window.innerWidth, window.innerHeight,
      { minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, format: THREE.RGBAFormat, type: THREE.HalfFloatType }));
    composer.addPass(new THREE.RenderPass(scene, camera));
    bloomPass = new THREE.UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight), 0.65, 0.4, 0.5); /* LOCKED (A4 §8) */
    composer.addPass(bloomPass);
    finalPass = new THREE.ShaderPass(FinalShader);
    finalPass.renderToScreen = true;
    composer.addPass(finalPass);

    buildAtmosphere();
    buildGround();
    buildWorld();
    buildProbe();

    /* harness poses (04 §7): ?still = the portrait · &pose=flight = mid-flight frame ·
       &title=1 = the boot scrim over the live scene */
    var F = GAME.state.flags;
    /* TURNAROUND HARNESS (2026-07-21): the engine renders its own model sheet. ?still&pose=turn&view=front|side|top|iso
       frames the probe alone against the void at true 1.2 m span — the orthographic study the
       image generator could not produce, taken from the real object instead of a drawing of it. */
    if (F.still && F.pose === "turn") {
      var view = (new URLSearchParams(location.search).get("view") || "iso");
      probe.position.set(0, 9, 150);
      probeLight.intensity = 0.25;         /* study light: geometry must read, not glow */
      scene.add(new THREE.HemisphereLight(lin(0x2a3646).getHex(), lin(0x090c12).getHex(), 1.15));
      var D = 12, P = probe.position;      /* 1.2 m object at fov 14 -> ~40% of frame */
      if (view === "front")     camera.position.set(P.x, P.y, P.z + D);
      else if (view === "side") camera.position.set(P.x + D, P.y, P.z);
      else if (view === "top")  camera.position.set(P.x, P.y + D, P.z + 0.001);
      else                      camera.position.set(P.x + D * 0.62, P.y + D * 0.45, P.z + D * 0.62);
      camera.fov = 14;                     /* long lens ~ orthographic */
      camera.updateProjectionMatrix();
      camera.lookAt(P);
    } else if (F.still && F.pose === "flight") {
      probe.position.set(26, 16, 118);
      yaw = -0.38; pitch = -0.04;
      chaseCam(0, true);
      hintsLive(true);
    } else {
      camera.position.copy(F.still ? STILL.camPos : STILL.camPos.clone().add(new THREE.Vector3(0, 26, 58)));
      camera.lookAt(STILL.lookAt);
    }
    if (F.still) {
      if (F.title) titleShow();
    } else {
      titleShow();
      bindInput();
    }

    /* context-loss pair (E1 §3.1.8): freeze and say so — a frozen world with a lit HUD is a lie */
    listen(renderer.domElement, "webglcontextlost", function (e) {
      e.preventDefault(); running = false;
      var el = document.getElementById("err");
      if (el) { el.textContent = "CARRIER LOST — GPU CONTEXT DROPPED · AWAITING RESTORE"; el.style.display = "block"; }
    });
    listen(renderer.domElement, "webglcontextrestored", function () {
      running = true;
      var el = document.getElementById("err");
      if (el) { el.textContent = ""; el.style.display = "none"; }
    });

    listen(window, "resize", onResize);

    GAME.state.engine = { scene: scene, camera: camera, renderer: renderer };
    running = true;
    loop();
  }

  function dispose() {
    /* E1 §3.1 checklist, in order: stop the loop, release timers+listeners, walk the scene */
    if (raf !== null) { cancelAnimationFrame(raf); raf = null; }
    running = false;
    R.timers.forEach(function (id) { clearTimeout(id); });
    R.listeners.forEach(function (l) { l[0].removeEventListener(l[1], l[2]); });
    scene.traverse(function (o) {
      if (o.geometry) o.geometry.dispose();
      if (o.material) {
        var mats = Array.isArray(o.material) ? o.material : [o.material];
        mats.forEach(function (m) {
          ["map", "emissiveMap", "alphaMap"].forEach(function (slot) { if (m[slot]) m[slot].dispose(); });
          m.dispose();
        });
      }
    });
    R.geoms.length = R.mats.length = R.texs.length = R.listeners.length = R.timers.length = 0;
    bloomPass.dispose();
    composer.renderTarget1.dispose(); composer.renderTarget2.dispose();
    renderer.dispose();
    if (renderer.domElement.parentNode) renderer.domElement.parentNode.removeChild(renderer.domElement);
    GAME.state.engine = null;
    scene = camera = composer = bloomPass = finalPass = skyMat = renderer = null;
  }

  return { init: init, dispose: dispose };
})();
