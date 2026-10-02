"""Read-only transform and camera-framing audit; no rendering and no source save.

Run after the render: blender -b media/v2/common-ground-park.blend --threads 2 --python media/v2/verify-park-motion.py
"""
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
import json
from pathlib import Path

scene = bpy.context.scene
ROOT = Path(__file__).resolve().parent
groups = [obj for obj in scene.objects if obj.type == "EMPTY" and "€" in obj.name]
geometry = [obj for obj in scene.objects if obj.type == "MESH" and obj.name != "Studio floor"]
trajectory = {obj.name: [] for obj in groups}
camera = []
bounds = []
for frame in range(1, 301):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    projected = []
    for obj in geometry:
        for corner in obj.bound_box:
            projected.append(world_to_camera_view(scene, scene.camera, obj.matrix_world @ Vector(corner)))
    bounds.append({"frame": frame, "left": min(point.x for point in projected),
                   "right": max(point.x for point in projected), "bottom": min(point.y for point in projected),
                   "top": max(point.y for point in projected)})
    for obj in groups:
        trajectory[obj.name].append(list(obj.location))
    camera.append(list(scene.camera.location))

reports = {}
for name, positions in trajectory.items():
    heights = [position[2] for position in positions]
    maximum_step = max((Vector(b) - Vector(a)).length for a, b in zip(positions, positions[1:]))
    settled = max(abs(value) for position in positions[127:] for value in position) < 1e-6
    monotonic = all(after <= before + 1e-6 for before, after in zip(heights, heights[1:]))
    no_overshoot = min(heights) >= -1e-6 and max(heights) <= heights[0] + 1e-6
    reports[name] = {"monotonic_lowering": monotonic, "no_vertical_overshoot": no_overshoot,
                     "settled_after_frame127": settled, "maximum_translation_per_frame": maximum_step}

out_of_frame = [item for item in bounds if item["left"] < 0 or item["right"] > 1 or item["bottom"] < 0 or item["top"] > 1]
report = {"kind": "Mathematical checks of the original animation, not a claim of subjective playback review",
          "checked_frames": 300, "components": reports, "mesh_bounds_exclude": ["Studio floor"],
          "out_of_frame_bounds": out_of_frame,
          "smallest_canvas_margin_fraction": min(min(item["left"], 1 - item["right"], item["bottom"], 1 - item["top"]) for item in bounds),
          "camera_maximum_translation_per_frame": max((Vector(b) - Vector(a)).length for a, b in zip(camera, camera[1:])),
          "limitations": ["Bounding boxes are conservative and do not test occlusion.",
                          "Intentional raised schematic assemblies include their figures; this is not a physics simulation.",
                          "No automated test establishes absence of shading shimmer or perceptual discomfort."]}
(ROOT / "park-motion-QA.json").write_text(json.dumps(report, indent=2) + "\n")
assert not out_of_frame, out_of_frame[:3]
assert all(item["monotonic_lowering"] and item["no_vertical_overshoot"] and item["settled_after_frame127"] for item in reports.values())
print(json.dumps(report, indent=2))
