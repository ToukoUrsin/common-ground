"""Reproducible 100-second narrated edit using only real recorded UI frames.

Run with Python + Pillow, ffmpeg and ffprobe. No UI state is drawn or fabricated.
The source sequences are chronological. Holds are retimed for narration; one
brief blank scroll frame is omitted. Captions identify the preset reset.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json
import re
import subprocess
import textwrap

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'raw' / 'rendered'
OUT.mkdir(parents=True, exist_ok=True)
DURATION = 100.0
FONT_ROOT = Path('/System/Library/Fonts/Supplemental')
font = lambda size: ImageFont.truetype(str(FONT_ROOT / 'Arial.ttf'), size)
fonts = {size: font(size) for size in (16, 19, 25, 30)}

# Timeline durations refer to output seconds, while source timestamps remain
# available in edit-manifest.json to distinguish recorded motion from holds.
settings = [
    (1,34.7,{0:17.2},set()),
    (2,9.0,{0:1.0},set()),
    (3,8.6,{0:.8},set()),
    (4,8.3,{0:.45},set()),
    (5,10.8,{0:.7},set()),
    (6,8.9,{0:.3},{6}),  # blank capture during scroll; no information removed
    (7,19.7,{0:.2,7:11.4},set()),
]
segments=[]
time=0.0
for scene,total,holds,omitted in settings:
    source=json.loads((ROOT/f'raw/scene{scene}/frames.json').read_text())
    kept=[(i,item) for i,item in enumerate(source) if i not in omitted]
    consumed=0
    for pos,(index,item) in enumerate(kept):
        if pos==len(kept)-1:
            duration=total-consumed
        else:
            duration=holds.get(index,max(.05, source[index+1]['t']-item['t']))
        if duration<=0: raise ValueError('Scene duration must exceed motion.')
        segments.append({'scene':scene,'frame':item['name'],'start':round(time,6),'duration':round(duration,6),'source_timestamp':item['t']})
        time+=duration;consumed+=duration
assert abs(time-DURATION)<.001

cards=[
 (0,11.8,'01 / THE QUESTION','What did the beautiful drawing leave out?','Different priorities. A limited budget. A decision people must understand.','RECORDED WORKING PROTOTYPE'),
 (11.8,18.6,'COMMON GROUND','A place for all of us.','An explanation for every tradeoff.','ILLUSTRATIVE POCKET PARK'),
 (18.6,34.7,'02 / SET THE COMMITMENTS','4,096 combinations. 145 feasible plans.','Budget €55k · minimum commitments to shade, access, play and water.','ILLUSTRATIVE COSTS & SCORES'),
 (34.7,43.7,'03 / PROTECT WHAT MATTERS','Keep inclusive play. Reconsider the rest.','A resident protects a favorite. The plan changes around that commitment.','HUMAN PRIORITIES FIRST'),
 (43.7,52.3,'04 / THE BUDGET CHANGES','€30k. No feasible plan.','Budget scenario: original minimums. This preset resets the protected favorite.','NO SILENTLY DROPPED TARGETS'),
 (52.3,60.6,'05 / INSPECT THE CONFLICT','Show exactly what cannot hold together.','Budget, shade, access and rain commitments form a verified conflict.','MACHINE-CHECKED EXPLANATION'),
 (60.6,71.4,'06 / FIND A FEASIBLE REPAIR','€7k more preserves every original minimum.','Explore the €37k scenario. The proposed repair is checked against all requirements.','REPAIR THE FULL SCENARIO'),
 (71.4,80.3,'07 / TAKE IT TO THE WORKSHOP','Export the assumptions and the certificate.','The complete scenario stays inspectable. Computation runs in the browser.','LOCAL BROWSER COMPUTATION'),
 (80.3,92.6,'08 / THE NEXT REAL STEP','A facilitated pilot with residents.','Working design prototype. Illustrative costs and scores. No field impact claimed.','BUILD WITH LOCAL EXPERTISE'),
 (92.6,100,'COMMON GROUND','Make the compromise visible.','A shared place begins with a conversation people can actually see.','A PLACE FOR ALL OF US'),
]

def render_frame(segment,card,ident):
    source_path=ROOT/f"raw/scene{segment['scene']}/{segment['frame']}"
    canvas=Image.new('RGB',(1920,1080),'#f9f8f4')
    image=Image.open(source_path).convert('RGB').resize((1728,972),Image.Resampling.LANCZOS)
    canvas.paste(image,(96,0))
    draw=ImageDraw.Draw(canvas)
    draw.rectangle((0,972,1920,1080),fill='#203a30')
    draw.rectangle((0,972,1920,974),fill='#c99b80')
    _,_,eyebrow,title,subtitle,badge=card
    draw.text((62,987),eyebrow,font=fonts[16],fill='#bed0b7')
    draw.text((62,1011),title,font=fonts[30],fill='#fffdf7')
    draw.text((62,1050),subtitle,font=fonts[19],fill='#e1e6dc')
    badge_width=draw.textlength(badge,font=fonts[16])
    draw.text((1858-badge_width,988),badge,font=fonts[16],fill='#d9c5ac')
    output=OUT/f'{ident:04d}.png'
    canvas.save(output)
    return output

concat=[];composite_segments=[]
for segment in segments:
    start=segment['start'];end=start+segment['duration']
    for card in cards:
        a,b=max(start,card[0]),min(end,card[1])
        if b-a<=.00001: continue
        path=render_frame(segment,card,len(composite_segments))
        concat.extend([f"file '{path}'",f'duration {b-a:.6f}'])
        composite_segments.append({**segment,'output_start':round(a,6),'output_duration':round(b-a,6),'caption':card[3]})
concat.append(f"file '{path}'")
(OUT/'frames.ffconcat').write_text('ffconcat version 1.0\n'+'\n'.join(concat)+'\n')

# Sentence timestamps aligned to the narration's audible pause boundaries.
# A 1.5-second visual lead-in is applied consistently to audio and captions.
starts=[.05,3.8357,6.2262,8.35,11.7961,13.298,17.3771,19.6287,24.8328,30.2448,33.6258,37.4264,40.3577,42.3728,45.5789,47.7547,52.747,55.743,58.2116,59.8564,64.7885,67.9911,70.0504,75.1542,79.0949,81.7205,88.9389,91.2312]
ends=[3.1754,5.5625,8.05,11.1366,12.9125,16.4976,19.1802,24.1718,29.6407,32.9181,36.7652,39.8296,41.6296,44.9175,46.9611,52.1292,55.1069,57.5146,59.3142,63.9065,67.4465,69.3923,74.3912,78.7153,81.0738,88.3425,90.6248,95.4434]
sentences=[s.strip() for s in re.findall(r'[^.!?]+[.!?]', (ROOT/'narration.txt').read_text().replace('\n',' '))]
assert len(sentences)==len(starts)==len(ends),len(sentences)
def timestamp(seconds):
    ms=round(seconds*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'
srt=[]
for i,(start,end,sentence) in enumerate(zip(starts,ends,sentences),1):
    srt.append(f'{i}\n{timestamp(start+1.5)} --> {timestamp(end+1.5)}\n'+textwrap.fill(sentence,72)+'\n')
(ROOT/'common-ground-demo.en.srt').write_text('\n'.join(srt))
manifest={'duration':DURATION,'resolution':[1920,1080],'frame_rate':30,'source':'Actual browser CDP capture frames from a running local prototype. No generated UI states.','editing':'Chronological within each scene; holds retimed for narration. One brief blank scroll frame omitted. Lower thirds are editorial captions. Audio begins at 1.5s.','scenario_reset':'Budget scenario uses original minimums and resets the previously protected favorite; explicitly disclosed on-screen.','audio_sha256':hashlib.sha256((ROOT/'narration.mp3').read_bytes()).hexdigest(),'segments':composite_segments}
(ROOT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
command=['ffmpeg','-y','-hide_banner','-loglevel','warning','-f','concat','-safe','0','-i',str(OUT/'frames.ffconcat'),'-i',str(ROOT/'narration.mp3'),'-i',str(ROOT/'common-ground-demo.en.srt'),'-filter_complex','[0:v]fps=30,format=yuv420p,fade=t=in:st=0:d=0.5,fade=t=out:st=99.4:d=0.6[v];[1:a]adelay=1500|1500,apad,alimiter=limit=0.95[a]','-map','[v]','-map','[a]','-map','2:0','-t','100','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','192k','-c:s','mov_text','-metadata:s:s:0','language=eng','-metadata','title=Common Ground — A place for all of us','-metadata','comment=Recorded working prototype. Illustrative costs and scores; no field impact claimed. Holds edited for narration.','-movflags','+faststart',str(ROOT/'common-ground-demo.mp4')]
print('Rendering',len(composite_segments),'real-source frame segments.',flush=True)
subprocess.run(command,check=True)
print(ROOT/'common-ground-demo.mp4')
