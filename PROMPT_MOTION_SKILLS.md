# Prompt-Motion Design System & Camera Directives
*Learned from prompt-motion.com analysis across 236 projects, master templates, and launch video architectures.*

---

## 1. The Core Philosophy: "Anti-AI Motion"
Standard AI motion graphics fail because they rely on low-effort procedural templates. This system enforces human-quality cinematic direction by strictly adhering to the **Banned List** and **Physical Cinema Directives**.

### The Banned List
- ❌ **No Cheap Particle Bursts:** Do not scatter random glowing dots on clicks or state changes.
- ❌ **No Cheesy Neon Blooms:** Avoid oversaturated Tron-like neon glow boundaries.
- ❌ **No Indiscriminate RGB Split / Glitch:** Glitch filters indicate unmotivated visual noise.
- ❌ **No Pseudo-Handheld Camera Shakes (`Math.random()`):** Camera movements must follow physical camera rigs, springs, or smooth Bézier curves.
- ❌ **No Dead Time:** No visual state remains static for more than 1.2 seconds without subtle continuous camera drift or kinetic evolution.
- ❌ **No Flat Enclosed Cards:** Avoid rectangular static boxes with drop shadows. Deconstruct UI into floating holographic planes in 3D coordinate space.
- ❌ **No Lazy Crossfades:** Transitions must preserve velocity and transfer momentum from the outgoing element to the incoming scene.

---

## 2. Dynamic Camera Physics & Named Moves
Every shot in a high-converting demo video must have **exactly one named, motivated camera move**. Never use chaotic free-orbit controls.

| Camera Move | Axis & Dynamics | Cinematic Intent |
|---|---|---|
| **Macro Dolly Push-In** | Accelerates along Z-axis (`translateZ: +450px`, `f/1.4` depth-of-field blur on periphery) | Directs acute focus into micro-telemetry (e.g. skin capillary rPPG waveform). |
| **Compound Orbital Arc** | Simultaneous 15° Y-axis rotation + -0.2m downward Y-crane descent | Reveals depth and spatial relationship between patient and autonomous agent. |
| **Dutch-Angle Crane Sweep** | Camera tilted 12° on Z-roll while sweeping 180° around focal point | Injects dynamic tension during agitation detection. |
| **Momentum Match-Cut** | Outgoing object exits frame at 1400px/s; incoming scene enters matching that vector | Creates seamless spatial velocity between real-world video and digital cortex. |
| **Fly-Through Focal Punch** | Camera punches through a primary UI aperture into a wider dimensional field | Transitioning from single patient biometric into Qloo's 250M+ cultural taste cluster. |

---

## 3. Layered Spatial Staging (Zero-Card Architecture)
To eliminate static card boxes, render all interfaces across three distinct 3D depth planes:

```
[Eye / Camera Viewport]
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. FORE-HUD PLANE (Z: +120px to +180px)                    │
│    - Contactless rPPG green-channel optical pulse wave      │
│    - High-frequency HRV telemetry & BPM readouts            │
│    - Monospace micro-labels, crisp high-contrast typography │
└─────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. MIDGROUND INTERFACE PLANE (Z: 0px, tilted 8°X, 14°Y)     │
│    - Deconstructed reminiscence memory anchors              │
│    - Cultural affinity score dials (98.4% Affinity)         │
│    - Spring physics: stiffness 180, damping 24              │
└─────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. DEEP FIELD CORTEX (Z: -250px to -600px)                  │
│    - Bioluminescent 3D dual-hemisphere neural point cloud   │
│    - Infinite cultural knowledge graph spline connections   │
│    - ACES tone mapping, volumetric rim lighting, ambient dust│
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Kinetic Typography & Easing Formulas
Text must never simply fade in. It enters along spline paths with word-by-word directional staggering and physical deceleration.

- **Primary Deceleration Curve:**
  ```css
  transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1); /* Snappy exponential out */
  ```
- **Spring Parameters:**
  ```javascript
  {
    stiffness: 190,
    damping: 22,
    mass: 1.0,
    velocity: 2.5
  }
  ```
- **Stagger Timing:**
  - Word-level reveal: `stagger: 0.04s`
  - Glyph / Number counter roll: `stagger: 0.02s`
  - Telemetry readouts: Instant mechanical step function (`steps(12)`) synchronized with audio click transients.

---

## 5. Biometric Lighting & Chromatic Harmony
Lighting acts as an emotional narrative driver:

1. **Baseline Calm State:** Cool indigo (`#0A0618`), deep midnight violet, subtle cyan highlights (`#38BDF8`).
2. **Sundowning Agitation Spike:** Volumetric warm amber/crimson rim light sweeps across the neural mesh (`#EF4444` to `#F59E0B`), visualizing autonomic distress.
3. **Reminiscence Resonance Lock:** Harmonious acoustic gold (`#FBBF24`) and mint cyan (`#34D399`) dissolve the crimson tension into coherent steady pulses.
