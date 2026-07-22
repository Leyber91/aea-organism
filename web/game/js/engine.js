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

  /* ---- THE INSTRUMENT (R37/R39): the being as a structural place, NOT a city. An amber core (the
     mind's heart) inside concentric PRIVACY-ZONE rings whose count/order come from the REAL
     grid.ZONES (via /game/schema); radius = openness (innermost = most restrictive). The AEA organs
     sit on their zone ring at dependency depth: LIT amber ONLY when really wired, cold-blue FOG when
     not. The core burns amber ONLY when the being's heartbeat is actually alive (schema.alive) - never
     as unconditional decoration (claim ceiling + amber census). Amber lives ON the core/nodes; lights
     are clamped so it never washes the floor - the 2D two-ink law, held in 3D. ---- */

  var coreRef = null;                                   /* {mesh,light,beam} - amber only when alive */
  function zoneRadius(i) { return 26 + i * 27; }        /* ring radius from the zone's index in the real order */

  function buildCore() {
    /* structure-ink by default: DARK until the entity proves it is alive (no unconditional amber). */
    var mesh = new THREE.Mesh(geo(new THREE.IcosahedronGeometry(1.7, 0)),
      mat(new THREE.MeshStandardMaterial({
        color: lin(0x0c131c), emissive: INK.structure, emissiveIntensity: 0.16,
        roughness: 0.5, metalness: 0, flatShading: true
      })));
    mesh.position.set(NEXUS.x, 4.8, NEXUS.z); mesh.name = "core"; scene.add(mesh);
    var light = new THREE.PointLight(INK.hot.getHex(), 0.0, 34);      /* dark until alive */
    light.position.set(NEXUS.x, 5.8, NEXUS.z); scene.add(light);
    var beam = new THREE.Mesh(geo(new THREE.CylinderGeometry(0.05, 0.16, 58, 6, 1, true)),
      mat(new THREE.MeshBasicMaterial({ color: INK.hot, transparent: true, opacity: 0.0, depthWrite: false })));
    beam.position.set(NEXUS.x, 29, NEXUS.z); scene.add(beam);
    coreRef = { mesh: mesh, light: light, beam: beam };
  }

  function igniteCore() {
    /* the heartbeat has ticked: the core EARNS its amber (proven alive, not asserted). */
    if (!coreRef) return;
    var m = coreRef.mesh.material;
    m.color = lin(0x1a1206); m.emissive = INK.hot; m.emissiveIntensity = EMISSIVE.fired; m.needsUpdate = true;
    coreRef.light.intensity = 1.5;                                    /* range 34: amber ON the core */
    coreRef.beam.material.opacity = 0.13;
  }

  function buildZoneRings(zones) {
    /* concentric privacy-zone rings from the REAL grid.ZONES order; thick enough to READ as a
       boundary (not a hairline). cold-blue structure ink; radius = zone openness. */
    (zones || []).forEach(function (z, i) {
      var ring = new THREE.Mesh(geo(new THREE.TorusGeometry(zoneRadius(i), 0.35, 8, 220)),
        mat(new THREE.MeshBasicMaterial({ color: INK.structure, transparent: true, opacity: 0.6 })));
      ring.rotation.x = -Math.PI / 2; ring.position.set(NEXUS.x, 0.1, NEXUS.z);
      ring.name = "zone-" + z; scene.add(ring);
    });
  }

  function organAngles(nodes, zones) {
    var idx = {}; (zones || []).forEach(function (z, i) { idx[z] = i; });
    var byZone = {}; nodes.forEach(function (n) { (byZone[n.zone] = byZone[n.zone] || []).push(n); });
    var pos = {};
    Object.keys(byZone).forEach(function (z) {
      var list = byZone[z], zi = idx[z] || 0, r = zoneRadius(zi), base = zi * 1.3 + 0.4;
      list.forEach(function (n, i) {
        var a = base + (i * 2 * Math.PI) / Math.max(list.length, 1);
        pos[n.id] = new THREE.Vector3(NEXUS.x + Math.cos(a) * r, 5 + n.depth * 7, NEXUS.z + Math.sin(a) * r);
      });
    });
    return pos;
  }

  function buildOrgans(sch) {
    if (!scene || !sch || !sch.nodes) return;
    var pos = organAngles(sch.nodes, sch.zones);
    (sch.edges || []).forEach(function (e) {
      var a = pos[e[0]], b = pos[e[1]]; if (!a || !b) return;
      var line = new THREE.Line(geo(new THREE.BufferGeometry().setFromPoints([a, b])),
        mat(new THREE.LineBasicMaterial({ color: INK.structure, transparent: true, opacity: 0.28 })));
      line.name = "conduit"; scene.add(line);
    });
    sch.nodes.forEach(function (n) {
      var p = pos[n.id]; if (!p) return;
      var g = geo(new THREE.OctahedronGeometry(1.25, 0)), node;
      if (n.wired) {
        node = new THREE.Mesh(g, mat(new THREE.MeshStandardMaterial({
          color: lin(0x1a1206), emissive: INK.hot, emissiveIntensity: 0.7,   /* below fire: clean bloom, no maroon box */
          roughness: 0.45, metalness: 0, flatShading: true
        })));
        var nl = new THREE.PointLight(INK.warm.getHex(), 0.5, 9);             /* clamped: amber ON the node, not the floor */
        nl.position.copy(p); scene.add(nl);
      } else {
        node = new THREE.Mesh(g, mat(new THREE.MeshBasicMaterial({
          color: INK.cold, wireframe: true, transparent: true, opacity: 0.72
        })));
      }
      node.position.copy(p); node.name = "organ-" + n.id; scene.add(node);
    });
  }

  function buildInstrument() {
    buildCore();   /* dark structure-ink until the schema proves the being alive */
    if (!GAME.state.flags.still && window.GameAPI && window.GameAPI.schema) {
      window.GameAPI.schema().then(function (sch) {
        if (!scene) return;
        buildZoneRings(sch.zones);
        buildOrgans(sch);
        if (sch.alive) igniteCore();                 /* amber ONLY when the heartbeat is really ticking */
      }, function () {});
    } else {
      buildZoneRings(["sensitive", "private", "public"]);   /* ?still: neutral field, no live amber */
    }
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
    /* the arrival: an elevated oblique onto the being-as-place, so the concentric zone rings and
       the amber core read as a structure (R37/R39), not an edge-on horizon. The probe stays
       dwarfed in the lower third; the dark field still owns the frame (A11 §2). */
    camPos: new THREE.Vector3(0, 40, 118),
    lookAt: new THREE.Vector3(0, 1, 34)
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
    buildInstrument();
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
