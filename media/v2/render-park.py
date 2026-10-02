"""Render the approved source animation at native1080p; one process, six CPU threads.
Usage: blender -b media/v2/common-ground-park.blend --threads 6 --python media/v2/render-park.py
"""
import bpy, os, json, time
ROOT=os.path.dirname(os.path.abspath(__file__));scene=bpy.context.scene
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100
scene.render.fps=30;scene.render.threads_mode='FIXED';scene.render.threads=6
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
    prefs.compute_device_type='METAL';prefs.get_devices()
    for device in prefs.devices:device.use=device.type=='METAL'
    if any(d.type=='METAL' for d in prefs.devices):scene.cycles.device='GPU'
except Exception:scene.cycles.device='CPU'
os.makedirs(os.path.join(ROOT,'park-frames'),exist_ok=True)
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8';scene.render.filepath=os.path.join(ROOT,'park-frames','frame_');scene.frame_start=1;scene.frame_end=300
poses=[]
for frame in [1,35,49,63,77,85,99,113,127,145,200,250,300]:
    scene.frame_set(frame);poses.append({'frame':frame,'camera':list(scene.camera.location),'ortho_scale':scene.camera.data.ortho_scale,'components':{o.name:list(o.location) for o in bpy.data.objects if o.type=='EMPTY' and '€' in o.name}})
manifest={'kind':'Original schematic illustration, not software footage','native_resolution':[1920,1080],'fps':30,'frames':300,'range':[1,300],'selected_ids':['trees','path','meadow','table'],'costs_kEUR':[14,12,4,7],'total_kEUR':37,'values_are':'illustrative design inputs','source':'common-ground-park.blend','build_script':'build-park.py','render_script':'render-park.py','engine':'CYCLES','samples':32,'denoising':True,'device':scene.cycles.device,'cpu_threads':6,'original_frames':'park-frames/frame_0001.png through frame_0300.png','poses':poses,'status':'rendering','started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
manifest_path=os.path.join(ROOT,'park-render-manifest.json');json.dump(manifest,open(manifest_path,'w'),indent=2)
scene.frame_set(1);started=time.monotonic();bpy.ops.render.render(animation=True)
manifest.update({'status':'rendered','render_seconds':round(time.monotonic()-started,3),'finished_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())});json.dump(manifest,open(manifest_path,'w'),indent=2)
print('PARK_RENDER_COMPLETE',manifest['render_seconds'])
