"""Original Common Ground schematic park. Blender 5.2, no external assets.
Run: blender -b --threads 2 --python media/v2/build-park.py -- --preview
Only the actual selected tree/path/meadow/table interventions are modeled.
"""
import bpy, math, random, sys, os
from mathutils import Vector
random.seed(37)
ROOT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for block in list(bpy.data.materials):bpy.data.materials.remove(block)

def mat(name,hex,rough=.72,metal=0):
    rgb=tuple(int(hex[i:i+2],16)/255 for i in (0,2,4));rgb=tuple(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in rgb);m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*rgb,1);bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
    return m
clay=mat('Warm clay • existing site plinth','B5957A');soil=mat('Permeable soil • tree establishment','A99173');floor=mat('Warm studio backdrop','EAE5DA');ground=mat('Existing ground • sage model surface','B2B7A0');pathmat=mat('Accessible firm route • pale mineral','DDD4BD',.63);edge=mat('Model brass boundary','A79769',.42,.24);wood=mat('Community table • terracotta timber','AD7152',.68);woodlight=mat('Timber end grain','C68A62');bark=mat('Young tree bark','816E55');grassm=[mat('Meadow leaf '+str(i),h)for i,h in enumerate(['7F9671','94A780','B2BD91','8B9D74','A5AE81'])];leafm=[mat('Tree foliage '+str(i),h)for i,h in enumerate(['597E63','739372','87A27E','99AF87','648B73'])];flowercolors=[mat('Wildflower '+str(i),h)for i,h in enumerate(['C98371','DDD3A5','E7DFCB','B4A3B2'])];charcoal=mat('Diagram figures • charcoal','445C52');cream=mat('Diagram figures • limestone','D8D2BC');shirt=mat('Diagram figure • terracotta','C18A71');wheelmat=mat('Wheelchair wheels','48574C',.6)

def group(name):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);return o
site=group('00 • Existing illustrative site');groups={k:group(k) for k in ['01 • trees • €14k','02 • path • €12k','03 • meadow • €4k','04 • table • €7k']};trees,paths,meadow,table=groups.values()
def finish(o,name,m,parent=None,bevel=0):
    o.name=name;o.data.materials.append(m)
    if parent:o.parent=parent
    if bevel:
        mod=o.modifiers.new('Soft model edge','BEVEL');mod.width=bevel;mod.segments=3
        mod=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
    return o

def box(name,loc,scale,m,parent=None,bevel=.04):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,name,m,parent,bevel)
def sphere(name,loc,scale,m,parent=None,sub=2):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.scale=scale;finish(o,name,m,parent);return o

def cylinder(name,p1,p2,r,m,parent=None,vertices=12):
    a,b=Vector(p1),Vector(p2);v=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=v.length,location=(a+b)*.5);o=bpy.context.object;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();return finish(o,name,m,parent,.018 if r>.04 else 0)

def ringcurve(name,points,width,m,parent,z=.16):
    # Mesh ribbon with flat accessible top, not a raised curb.
    verts=[];N=len(points)
    for i,(x,y)in enumerate(points):
        px,py=points[(i-1)%N];nx,ny=points[(i+1)%N];dx,dy=nx-px,ny-py;norm=math.hypot(dx,dy);sx,sy=-dy/norm*width*.5,dx/norm*width*.5
        verts.extend([(x+sx,y+sy,z),(x-sx,y-sy,z),(x+sx,y+sy,z-.06),(x-sx,y-sy,z-.06)])
    faces=[]
    for i in range(N):
        a=i*4;b=((i+1)%N)*4;faces.extend([(a,a+1,b+1,b),(a+2,b+2,b+3,a+3),(a,b,b+2,a+2),(a+1,a+3,b+3,b+1)])
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);return finish(o,name,m,parent,.035)

def ellipse_patch(name,center,radii,height,m,parent):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=1,depth=height,location=(center[0],center[1],.13+height*.5));o=bpy.context.object;o.scale=(radii[0],radii[1],1);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,name,m,parent,.07)
# A physical presentation model with a low uninterrupted perimeter, not construction drawings.
box('Clay exhibition plinth',(0,0,-.42),(16.4,11.4,.84),clay,site,.24)
box('Existing soft landscape',(0,0,.045),(15.95,10.95,.15),ground,site,.2)
box('Studio floor',(0,0,-.92),(200,200,.12),floor,None,.0)
# Continuous loop using a rounded superellipse, preserving generous maneuvering space.
points=[]
for j in range(192):
    t=2*math.pi*j/192;co,si=math.cos(t),math.sin(t);points.append((6.4*math.copysign(abs(co)**.5,co),4.1*math.copysign(abs(si)**.5,si)))
ringcurve('Firm step-free continuous loop',points,.94,pathmat,paths)
box('Entrance connection',(0,-4.7,.14),(1.12,1.25,.08),pathmat,paths,.04)
box('Table connecting route',(4.72,1.45,.14),(2.75,1.05,.08),pathmat,paths,.04)
box('Grove connecting route',(-5.06,1.2,.14),(2.35,.94,.08),pathmat,paths,.04)
# Four young trees on permeable ground. Foliage remains a schematic future-shade illustration.
ellipse_patch('Grove permeable soil',(-3.1,1.5),(2.45,1.75),.06,soil,trees)
for i,(x,y,h)in enumerate([(-4.5,.72,2.25),(-3.6,2.22,2.65),(-2.1,2.24,2.5),(-1.75,.6,2.12)]):
    cylinder(f'Tree{i+1} trunk',(x,y,.18),(x+.04,y,h*.72),.085,bark,trees)
    for k in range(5):
        angle=k*2.399+i*.8;r=.38 if k else .08;end=(x+math.cos(angle)*r,y+math.sin(angle)*r,h-.38+(.16 if k%2 else 0));cylinder(f'Tree{i+1} branch{k}',(x,y,h*.48),end,.035,bark,trees,8)
        sphere(f'Tree{i+1} crown{k}',(end[0],end[1],h-.1+(k%2)*.16),(.57+.05*(k%2),.49,.7),leafm[(i+k)%len(leafm)],trees,2)
    # Simple trunk protection circle represented in the same grove assembly.
    for k in range(3):
        t=2*math.pi*k/3;cylinder(f'Tree{i+1} support{k}',(x+.27*math.cos(t),y+.27*math.sin(t),.2),(x+.25*math.cos(t),y+.25*math.sin(t),.81),.018,wood,trees,6)
# Seasonal meadow, without a basin or rain-garden component.
ellipse_patch('Wildflower patch • flat soil',(3.55,-1.66),(2.04,1.14),.065,soil,meadow)
verts=[];faces=[];mi=[]
for k in range(1250):
    theta=random.random()*2*math.pi;r=math.sqrt(random.random());x=3.55+1.93*r*math.cos(theta);y=-1.66+1.02*r*math.sin(theta);h=random.uniform(.10,.35);w=random.uniform(.018,.035);a=random.random()*math.pi;dx,dy=math.cos(a)*w,math.sin(a)*w;idx=len(verts);verts.extend([(x-dx,y-dy,.2),(x+dx,y+dy,.2),(x+.09*math.cos(a+.8),y+.09*math.sin(a+.8),.2+h)]);faces.append((idx,idx+1,idx+2));mi.append(k%len(grassm))
mesh=bpy.data.meshes.new('Individual meadow blades');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Meadow • 1250 modeled leaves',mesh);bpy.context.collection.objects.link(o);o.parent=meadow
for m in grassm:o.data.materials.append(m)
for poly,m in zip(o.data.polygons,mi):poly.material_index=m
for k in range(64):
    theta=random.random()*2*math.pi;r=math.sqrt(random.random());x=3.55+1.87*r*math.cos(theta);y=-1.66+.97*r*math.sin(theta);h=random.uniform(.31,.52)
    cylinder('Wildflower stem',(x,y,.18),(x+.025,y,.18+h),.009,grassm[k%5],meadow,5)
    for p in range(5):
        t=p*2*math.pi/5;sphere('Wildflower petal',(x+.037*math.cos(t),y+.037*math.sin(t),.18+h),(.035,.025,.017),flowercolors[k%4],meadow,1)
    sphere('Wildflower heart',(x,y,.2+h),(.018,.018,.018),woodlight,meadow,1)
# Small interpretation sign is part of the meadow proposal.
cylinder('Meadow interpretation sign post',(5.25,-1.2,.15),(5.25,-1.2,.68),.023,edge,meadow)
sign=box('Meadow interpretation sign',(5.25,-1.2,.70),(.38,.23,.04),wood,meadow,.025);sign.rotation_euler.x=.28
# Community table: open ends and generous approach. No separate bench intervention.
for k in range(7):box('Table timber plank',(1.5,1.38+(k-3)*.155,.93),(2.3,.145,.095),wood if k%2 else woodlight,table,.018)
for x in [.68,2.32]:
    for y in [1.07,1.68]:cylinder('Table leg',(x,y,.16),(x,y,.9),.065,charcoal,table)
# Two lightweight movable chairs belong to the gathering-table set, not added park benches.
for x,y in [(1.08,.40),(2.05,2.33)]:
    box('Table chair seat',(x,y,.51),(.43,.44,.07),wood,table,.04)
    for dx in [-.15,.15]:
        for dy in [-.15,.15]:cylinder('Chair leg',(x+dx,y+dy,.17),(x+dx,y+dy,.5),.021,charcoal,table,8)
    backy=y+(-.19 if y<1 else .19);box('Chair back',(x,backy,.76),(.42,.055,.38),wood,table,.035)
# Abstract human figures provide scale, not measured usage or access certification.
def person(name,x,y,parent,color,height=1.45):
    cylinder(name+' torso',(x,y,.65),(x,y,1.13),.125,color,parent)
    sphere(name+' head',(x,y,1.33),(.14,.13,.16),cream,parent,2)
    for sign in [-1,1]:cylinder(name+' leg',(x+sign*.075,y,.67),(x+sign*.11,y-.035,.16),.045,charcoal,parent)
    cylinder(name+' left arm',(x-.13,y,1.09),(x-.2,y,.81),.039,color,parent)
    cylinder(name+' right arm',(x+.13,y,1.09),(x+.18,y+.04,.82),.039,color,parent)
person('Table guest',3.1,1.15,table,shirt)
# A wheelchair companion approaches an open table end; anatomy intentionally schematic.
x,y=.02,1.36
for side in [-1,1]:
    bpy.ops.mesh.primitive_torus_add(major_segments=36,minor_segments=8,location=(x,y+side*.26,.47),major_radius=.29,minor_radius=.027,rotation=(math.pi/2,0,0));finish(bpy.context.object,'Companion wheelchair wheel',wheelmat,table)
    cylinder('Wheel axle',(x,y-.31,.47),(x,y+.31,.47),.026,wheelmat,table)
box('Wheelchair seat',(x,y,.56),(.40,.43,.06),charcoal,table,.04)
box('Wheelchair back',(x-.2,y,.79),(.055,.43,.43),charcoal,table,.04)
sphere('Seated companion torso',(x-.03,y,.92),(.14,.17,.27),cream,table,2);sphere('Seated companion head',(x-.02,y,1.29),(.135,.13,.155),cream,table,2)
for side in [-1,1]:cylinder('Seated companion leg',(x+.02,y+side*.08,.68),(x+.3,y+side*.08,.37),.047,charcoal,table)
# A fine model plate on the plinth is graphical, all large figures belong in the edit.
box('Small blank model plaque',(5.3,-5.71,-.32),(2.0,.045,.25),edge,site,.025)
# Deliberate assembly: selected components hover, then settle in four readable stages.
for g,offset,delay in [(paths,(0,0,.75),0),(meadow,(.35,-.25,1.6),14),(trees,(-.3,.15,2.25),28),(table,(.15,.1,2.7),42)]:
    g.location=offset;g.keyframe_insert(data_path='location',frame=1);g.keyframe_insert(data_path='location',frame=35+delay)
    g.location=(0,0,0);g.keyframe_insert(data_path='location',frame=85+delay);g.keyframe_insert(data_path='location',frame=300)
    if g.animation_data:
        for fc in g.animation_data.action.fcurves if hasattr(g.animation_data.action,'fcurves')else []:
            for kp in fc.keyframe_points:kp.interpolation='BEZIER'
# Camera arc. Negative-space target leaves the left third for large editorial values.
scene=bpy.context.scene
bpy.ops.object.empty_add(type='PLAIN_AXES',location=(-3.1,.2,.5));target=bpy.context.object;target.name='Camera target • editorial safe space'
bpy.ops.object.camera_add(location=(21,-29,24));cam=bpy.context.object;cam.name='Hero camera • original park arc';cam.data.type='ORTHO';cam.data.ortho_scale=25.3;cam.data.lens=52
track=cam.constraints.new(type='TRACK_TO');track.target=target;track.track_axis='TRACK_NEGATIVE_Z';track.up_axis='UP_Y'
for frame,pos,scale in [(1,(22,-29,25),29.7),(145,(20,-30,24),28.5),(300,(17,-30,23),28.1)]:cam.location=pos;cam.data.ortho_scale=scale;cam.keyframe_insert(data_path='location',frame=frame);cam.data.keyframe_insert(data_path='ortho_scale',frame=frame)
scene.camera=cam

def light(name,loc,power,size,color):
    bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.name=name;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.data.color=color;l.rotation_euler=(Vector((0,0,0))-l.location).to_track_quat('-Z','Y').to_euler()
light('Large soft key',(-7,-9,16),2200,9,(1,.87,.70));light('Quiet cool fill',(6,3,12),1200,8,(.79,.88,1));light('Warm rim',(1,9,11),1600,7,(1,.91,.77))
scene.world.color=(.40,.40,.40);scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=1920;scene.render.resolution_y=1080;scene.render.resolution_percentage=100;scene.render.fps=30;scene.frame_start=1;scene.frame_end=300
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False;scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.15
scene['description']='Schematic illustration, not live UI or verified construction design. Exactly trees14 + path12 + meadow4 + table7 = €37k illustrative repair.'
scene['selected_intervention_ids']='trees,path,meadow,table';scene['design_points']='shade9/access15/play9/water8; illustrative inputs, not measured outcomes';scene['no_extra_selected_features']='No benches, rain garden, canopy, lights or fountain.'
scene.frame_set(200);bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'common-ground-park.blend'))
if '--preview' in sys.argv:
    scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100;scene.render.filepath=os.path.join(ROOT,'park-preview-assembled.png');bpy.ops.render.render(write_still=True)
    scene.frame_set(1);scene.render.resolution_x=800;scene.render.resolution_y=450;scene.render.resolution_percentage=100;scene.render.filepath=os.path.join(ROOT,'park-preview-exploded.png');bpy.ops.render.render(write_still=True)
print('Saved original park scene. Preview frame200; animation1–300. Full animation not rendered.')
