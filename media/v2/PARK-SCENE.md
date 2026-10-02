# Common Ground — original schematic park, v2

Prepared September 21–22, 2026. This is **a schematic illustration**, not a recording of software, a survey, a construction proposal, a measured benefit, or an accessibility certification. The final film editor supplies the disclosure. No company reference imagery or private material is incorporated.

## Exact plan represented

The actual `engine.mjs` definitions determine the four illustrated components: **trees €14k + path €12k + meadow €4k + table €7k = €37k**. Their illustrative design points are shade 9 / access 15 / play 9 / water 8, against minima 9 / 12 / 8 / 7. The application separately verifies the full 4,096-combination search and exported receipt. The original €30k case is infeasible; the exploded assembly does not represent a feasible €30k design.

- **Trees:** four young trees, permeable establishment soil, and support stakes. Foliage is a schematic future-shade illustration.
- **Path:** continuous broad loop, entrance, and amenity connections. Detailed dimensions, slopes, surfaces, furniture clearances and approach interfaces remain to be designed and reviewed.
- **Meadow:** flat wildflower patch with 1,250 modeled leaf blades, 64 flowers, and an interpretation sign. It is not a rain garden or basin.
- **Table:** open-ended timber table, two movable chairs, and abstract scale figures including a wheelchair companion. There is no separately selected park-bench intervention.

The clay plinth, existing ground and studio floor are presentation context, not additional selected interventions. No canopy, fountain, lighting intervention, inclusive-play installation, mural, or added permeable-paving intervention is shown.

## Deliverables and provenance

`build-park.py` procedurally creates every model, material, light and animated transform in Blender 5.2. It uses a fixed seed of 37 and no external artwork, textures, fonts or downloaded models. `common-ground-park.blend` is the editable source: native 1920 × 1080, 30 fps, frames 1–300, Cycles 32 samples, denoising, saved at frame 200. The render helper selects the Metal GPU and caps CPU workers at six. There is one render process for this shot.

The first preview had washed-out materials and clipped the plinth. Revised material values correctly convert sRGB to scene-linear color; a wider camera now leaves the full plinth within the frame. `park-preview-assembled.png` and `park-preview-exploded.png` are the approved composition previews. They are not used as upscaled video sources.

The original full-resolution animation resumed on the existing PID21206 after root confirmed the `commonground-continuation` queue grant at05:33:31Z. Frames1–117 were preserved; 119 frames were saved at the latest bounded checkpoint. `park-render-checkpoint.json` records the pause and authorized continuation. Root has a lightweight process-exit watcher that owns queue release. No new renderer or encode was started; sustained CPU encoding needs a separate grant. `park-render-manifest.json` holds the rendering settings and will be finalized when the same process completes. `park-motion-review-partial-115.mp4` is explicitly a partial review clip: the first 115 actual native frames, 3.833 seconds. It is not the completed shot.

## Motion and edit contract

The slow camera arc includes a subtle push. The four raised assemblies lower smoothly in this order:

| Component | Start frame / time | Settled frame / time |
|---|---:|---:|
| Loop | 35 / 1.13 s | 85 / 2.80 s |
| Meadow | 49 / 1.60 s | 99 / 3.27 s |
| Grove | 63 / 2.07 s | 113 / 3.73 s |
| Table | 77 / 2.53 s | 127 / 4.20 s |

Times use frame 1 as time zero. Frames 128–300 retain the assembled plan while the camera completes its arc. The deliberate exploded-view motion is not a physics simulation; figures rise and lower with their associated table assembly. The movie contains no audio or baked typography. Its upper-left negative space is reserved for the final edit's large budget figures and component labels.

Use the editor's disclosure **“Schematic of verified €37k selection · illustrative costs.”** The model illustrates the solver-selected IDs, not an automatically generated park, measured impact, verified access design or real app footage. Narration may list components in a different order; the edit must attach each label to its actual object without falsely presenting the motion as synchronized software behavior.

## Reproduce and verify

Run from the Common Ground repository:

```sh
# Rebuild editable source and two composition previews only.
/opt/homebrew/bin/blender -b --threads 2 --python media/v2/build-park.py -- --preview

# Native animation: one render process, Metal GPU if available, six CPU workers.
/opt/homebrew/bin/blender -b media/v2/common-ground-park.blend --threads 6 --python media/v2/render-park.py

# After rendering: audit all animated transforms and camera bounds without rendering.
/opt/homebrew/bin/blender -b media/v2/common-ground-park.blend --threads 2 --python media/v2/verify-park-motion.py

# Preserve all source PNGs, encode H.264 at native size, hash frames and fully decode output.
python3 media/v2/package-park.py
```

The packaging script refuses an incomplete sequence. It creates the ten-second `common-ground-park-1080p.mp4`, per-frame `park-frames-manifest.json`, technical `park-ffprobe.json`, and `park-SHA256SUMS`. Encoding and filtering are capped at two threads. `park-motion-QA.json` checks all 300 transforms for monotonic lowering, no vertical overshoot, stable final positions and conservative camera-frame bounds. Neither a passing mathematical check nor isolated still inspection establishes subjective motion or soundtrack acceptance; the final editor must view the assembled film at normal speed.
