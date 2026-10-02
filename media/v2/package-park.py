"""Package the original native-resolution PNG sequence, preserving every source frame.

Run only after render-park.py completes: python3 media/v2/package-park.py
No source images are altered. ffmpeg is capped at two encoder/filter threads.
"""
from pathlib import Path
import hashlib
import json
import struct
import subprocess
import time

ROOT = Path(__file__).resolve().parent
manifest_path = ROOT / "park-render-manifest.json"
manifest = json.loads(manifest_path.read_text())
assert manifest["status"] in ("rendered", "packaged"), "Wait for the Blender render to finish."
expected = [ROOT / "park-frames" / f"frame_{i:04d}.png" for i in range(1, 301)]
actual = sorted((ROOT / "park-frames").glob("frame_*.png"))
assert actual == expected, "The original sequence must contain exactly frames 1 through 300."

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

frames = []
for i, path in enumerate(expected, 1):
    header = path.read_bytes()[:24]
    assert header[:8] == b"\x89PNG\r\n\x1a\n", path.name
    dimensions = struct.unpack(">II", header[16:24])
    assert dimensions == (1920, 1080), (path.name, dimensions)
    frames.append({"frame": i, "presentation_seconds": round((i - 1) / 30, 6),
                   "path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
                   "width": 1920, "height": 1080, "sha256": sha256(path)})

output = ROOT / "common-ground-park-1080p.mp4"
command = ["/opt/homebrew/bin/ffmpeg", "-hide_banner", "-y", "-xerror", "-threads", "2",
           "-framerate", "30", "-start_number", "1", "-i", str(ROOT / "park-frames/frame_%04d.png"),
           "-frames:v", "300", "-an", "-vf", "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,setsar=1",
           "-filter_threads", "2", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
           "-pix_fmt", "yuv420p", "-threads", "2", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-colorspace", "bt709", "-color_range", "tv", "-movflags", "+faststart", str(output)]
with (ROOT / "park-encode.log").open("w") as log:
    subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)
probe_command = ["/opt/homebrew/bin/ffprobe", "-v", "error", "-count_frames", "-show_streams", "-show_format", "-of", "json", str(output)]
probe = json.loads(subprocess.check_output(probe_command))
video = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
assert (video["width"], video["height"]) == (1920, 1080)
assert video["codec_name"] == "h264" and video["pix_fmt"] == "yuv420p"
assert video["avg_frame_rate"] == "30/1" and int(video["nb_read_frames"]) == 300
assert abs(float(probe["format"]["duration"]) - 10) < .001
assert not any(stream["codec_type"] == "audio" for stream in probe["streams"])
with (ROOT / "park-decode.log").open("w") as log:
    subprocess.run(["/opt/homebrew/bin/ffmpeg", "-hide_banner", "-xerror", "-threads", "2", "-i", str(output),
                    "-f", "null", "-"], check=True, stdout=log, stderr=subprocess.STDOUT)
(ROOT / "park-ffprobe.json").write_text(json.dumps(probe, indent=2) + "\n")
frame_manifest = {"kind": "Original native render frames; no upscaling", "width": 1920, "height": 1080,
                  "fps": 30, "count": 300, "source": "common-ground-park.blend", "frames": frames}
(ROOT / "park-frames-manifest.json").write_text(json.dumps(frame_manifest, indent=2) + "\n")
manifest.update({"status": "packaged", "packaged_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                 "mp4": output.name, "mp4_sha256": sha256(output), "mp4_bytes": output.stat().st_size,
                 "source_sha256": sha256(ROOT / "common-ground-park.blend"), "encode_command": command,
                 "package_script": "package-park.py", "frames_manifest": "park-frames-manifest.json",
                 "verification": {"all_300_original_frames_native_1080p": True, "missing_frames": [],
                                  "duration_seconds": 10, "mp4_decoded_frames": 300,
                                  "full_decode": "passed with -xerror", "audio": "none; editor adds soundtrack",
                                  "perceptual_motion_review": "See park-motion-QA.json and PARK-SCENE.md"}})
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
checksummed = [output, ROOT / "common-ground-park.blend", ROOT / "build-park.py", ROOT / "render-park.py",
               ROOT / "package-park.py", ROOT / "park-frames-manifest.json"]
(ROOT / "park-SHA256SUMS").write_text("".join(f"{sha256(path)}  {path.name}\n" for path in checksummed))
print(json.dumps({"output": str(output), "bytes": output.stat().st_size, "duration_seconds": 10,
                  "original_frames": len(frames), "sha256": sha256(output)}, indent=2))
