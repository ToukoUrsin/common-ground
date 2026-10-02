"""Common Ground v2: reproducible 73.2s editorial film.
Real exported browser frames, original data animation, original Blender scene.
The montage is edited and retimed; it is not a continuous live benchmark.
Run --preview first, then --render after all300 park frames exist.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,json,math,subprocess,hashlib
import numpy as np
P=Path(__file__).resolve().parent; RAW=P/'raw'; W,H,FPS,D=1920,1080,30,73.2
BG='#f5f2e9'; INK='#213d33'; MUTED='#66756a'; RUST='#ac7351'; LINE='#d9ddd2'; GREEN='#689678'
FONT='/System/Library/Fonts/Avenir Next.ttc'; SERIF='/System/Library/Fonts/Supplemental/Georgia.ttf'
fonts={}
def font(n,serif=False):
 key=n,serif
 if key not in fonts:fonts[key]=ImageFont.truetype(SERIF if serif else FONT,n)
 return fonts[key]
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def lerp(a,b,u):return a+(b-a)*ease(u)
def txt(im,pos,text,n=36,color=INK,serif=False):ImageDraw.Draw(im).text(pos,text,font=font(n,serif),fill=color)
def wrap(im,pos,text,width,n=32,color=MUTED):
 draw=ImageDraw.Draw(im);line=''; y=pos[1]
 for word in text.split():
  if draw.textlength((line+' '+word).strip(),font=font(n))>width:
   txt(im,(pos[0],y),line,n,color);y+=n*1.4;line=word
  else:line=(line+' '+word).strip()
 if line:txt(im,(pos[0],y),line,n,color)
def canvas():return Image.new('RGB',(W,H),BG)
def label(im,k,title):txt(im,(78,48),k,22,MUTED);txt(im,(76,91),title,57,INK,True)
def footer(im,text):txt(im,(78,1016),text,23,MUTED)
cache={}
def src(name):
 if name not in cache:cache[name]=Image.open(RAW/name).convert('RGB')
 return cache[name]
def window(im,name,rect,dest):
 # Exact real browser pixels; cropping and scaling never modify their contents.
 a=src(name).crop(tuple(round(v) for v in rect));x,y,w,h=dest
 im.paste(a.resize((round(w),round(h)),Image.Resampling.LANCZOS),(round(x),round(y)))
def outline(im,box,color=RUST,w=4):ImageDraw.Draw(im).rounded_rectangle(tuple(round(x) for x in box),radius=8,outline=color,width=w)
M=json.loads((P/'combination-matrix.json').read_text())['matrix']; assert len(M)==4096
assert sum(x['fits']['30'] for x in M)==0 and sum(x['fits']['37'] for x in M)==1
proposal=json.loads((RAW/'actual-export-37k.json').read_text());assert proposal['result']['count']==1
beats=[(0,3.76,'opening'),(3.76,7.05,'impossible'),(7.05,10.5,'studio'),(10.5,19.55,'commitments'),(19.55,24.97,'enumeration'),(24.97,28.4,'zero'),(28.4,35.4,'certificate'),(35.4,38.15,'options'),(38.15,40.2,'repair'),(40.2,49.3,'park'),(49.3,52.3,'export'),(52.3,55.35,'open'),(55.35,61.45,'receipt'),(61.45,64.7,'tamper'),(64.7,69.12,'next'),(69.12,D,'close')]
def park_frame(t,final=False):
 idx=min(300,max(1,round(1+t*30)))
 path=P/f'park-frames/frame_{idx:04d}.png'
 if not path.exists():
  if final:raise FileNotFoundError(path)
  path=P/'park-preview-assembled.png'
 return Image.open(path).convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
def frame(t,final=False):
 im=canvas(); draw=ImageDraw.Draw(im)
 if t<3.76:
  txt(im,(82,64),'COMMON GROUND / A SHARED DECISION',23,MUTED)
  txt(im,(72,168),'€30,000',170,INK,True)
  txt(im,(83,380),'Four commitments.',58,INK,True)
  labs=[('SHADE','9'),('ACCESS','12'),('PLAY','8'),('RAIN','7')]
  for j,(name,n) in enumerate(labs):
   u=ease((t-.6-j*.35)/.65); x=84+j*447; y=round(584+45*(1-u))
   if u>0:
    draw.line((x,y,x+390,y),fill=LINE,width=2);txt(im,(x,y+24),name,25,MUTED);txt(im,(x,y+66),n,96,INK,True)
  footer(im,'Illustrative community workshop · costs and design points are assumptions')
 elif t<7.05:
  u=ease((t-3.76)/.45);txt(im,(80,67),'THE FIRST HONEST ANSWER',23,MUTED)
  txt(im,(65,178),'0',300,RUST,True);txt(im,(375,317),'feasible plans',82,INK,True)
  window(im,'conflict-certificate-full.png',(640,395,1925,730),(385,530,1285,335))
  footer(im,'Recorded prototype result · all 4,096 combinations checked')
 elif t<10.5:
  window(im,'studio-zero.png',(0,0,2560,1440),(0,0,W,H))
  draw=ImageDraw.Draw(im);draw.rectangle((0,820,W,H),fill=INK)
  txt(im,(79,850),'Common Ground',80,'#fffdf6',True);txt(im,(82,952),'Make the conflict visible, before anyone builds.',34,'#d8e1d3')
 elif t<19.55:
  label(im,'01 / THE COMMITMENTS','Start with what the community needs.')
  window(im,'conflict-certificate-full.png',(95,0,620,770),(100,230,525,770))
  window(im,'studio-zero.png',(105,910,596,1425),(750,244,650,682))
  # The original priorities are shown unmodified. The editorial explanation is outside the UI.
  wrap(im,(1450,275),'Shade. Access. Play. Rain.',370,42,INK)
  wrap(im,(1450,572),'Illustrative design points. Not measured impacts.',370,32,MUTED)
  if t<16.3:
   row=max(0,min(3,int((t-12.3)/.72)));outline(im,(93,235+row*145,632,345+row*145),GREEN)
  footer(im,'Real browser inputs · original minimums: 9 / 12 / 8 / 7')
 elif t<24.97:
  label(im,'02 / EXHAUSTIVE SEARCH','Every combination gets checked.')
  shown=min(4096,int(max(0,(t-19.55)/3.85)*4096)); size=9;gap=3;x0=87;y0=205
  for i in range(4096):
   x=x0+(i%64)*(size+gap);y=y0+(i//64)*(size+gap)
   draw.rectangle((x,y,x+size,y+size),fill=INK if i<shown else '#e0e2d9')
  txt(im,(1060,258),f'{shown:,}',146,INK,True);txt(im,(1070,453),'of 4,096 subsets',38,MUTED)
  txt(im,(1070,602),'12 interventions',44,INK);wrap(im,(1070,685),'Each dot represents an actual subset. All costs and constraints are evaluated.',700,34)
  footer(im,'Visualization of real exhaustive results · animation timing is editorial')
 elif t<28.4:
  label(im,'03 / THE BUDGET DOES NOT FIT','The commitments cannot all hold.')
  txt(im,(76,262),'€30k',133,INK,True);txt(im,( 80,443),'Original minimums preserved',31,MUTED)
  window(im,'conflict-certificate-full.png',(635,390,1940,742),(620,258,1240,334))
  txt(im,(630,662),'4,096 checked',61,INK);txt(im,(630,763),'0 feasible',112,RUST,True)
  footer(im,'Nothing was quietly dropped to produce a pretty plan.')
 elif t<35.4:
  label(im,'04 / INSPECT THE REASON','A conflict you can explain.')
  window(im,'conflict-certificate-full.png',(103,795,2460,1239),(78,274,1768,333))
  active=max(0,min(3,int((t-29.05)/.67)))
  if t<33.5:outline(im,(834,338+active*34,1210,366+active*34),RUST)
  wrap(im,(95,702),'Removing any one requirement in this conflict makes that subset feasible.',1000,44,INK)
  wrap(im,(1265,720),'Other constraints still matter. Every proposed repair is rechecked against the full scenario.',560,31,MUTED)
  footer(im,'Recorded certificate · independent verification · no silently relaxed requirement')
 elif t<38.15:
  label(im,'05 / MAKE THE TRADEOFF EXPLICIT','Lower a target. Or change the budget.')
  window(im,'conflict-certificate-full.png',(635,390,1940,742),(130,285,1660,448))
  outline(im,(141,505,463,578),GREEN,5)
  footer(im,'Three actual single-requirement repairs · the full scenario is checked for each')
 elif t<40.2:
  label(im,'06 / PRESERVE EVERY MINIMUM','€7k more makes a plan possible.')
  window(im,'repair-click-full.png',(630,380,1940,715),(90,285,1740,445))
  footer(im,'Actual repair button applied:budget €30k → €37k · minimums unchanged')
 elif t<49.3:
  im=park_frame((t-40.2)*1.0989,final)
  txt(im,(75,45),'SCHEMATIC OF THE VERIFIED SELECTION',22,MUTED)
  txt(im,(67,88),'€37k',137,INK,True)
  txt(im,(76,258),'1 feasible plan',37,INK)
  components=[(43.65,'A grove of trees','€14k'),(45.15,'An accessible loop','€12k'),(46.53,'A wildflower patch','€4k'),(47.89,'A table for everyone','€7k')]
  for j,(start,title,cost) in enumerate(components):
   if t>=start:
    yy=round(360+j*105+25*(1-ease((t-start)/.4)))
    txt(im,(78,yy),title,32,INK);txt(im,(78,yy+43),cost,28,RUST)
  footer(im,'Original 3D illustration · selected components and illustrative costs match the exported result')
 elif t<52.3:
  label(im,'07 / TAKE THE EVIDENCE WITH YOU','Export the actual proposal.')
  u=ease((t-49.3)/1.1)
  window(im,'export-click-full.png',(0,0,2560,800),(90,240,1740,544))
  txt(im,(98,850),'common-ground-proposal.json',43,INK)
  footer(im,'Actual browser export · source scenario, intervention definitions and result travel together')
 elif t<55.35:
  label(im,'08 / REOPEN THE FILE','A proposal that can be checked.')
  window(im,'receipt-empty-full.png',(200,300,2350,900),(90,232,1740,486))
  txt(im,(95,787),'Open. Recompute. Compare.',57,INK,True)
  txt(im,(99,877),'No stored “verified” flag is trusted.',32,MUTED)
  footer(im,'Real local file reader · imported the JSON exported from the studio')
 elif t<61.45:
  window(im,'receipt-verified.png',(260,0,2300,1440),(170,30,1580,1000))
  # Outline only the real receipt cells currently discussed.
  if t<57.77:outline(im,(1240,63,1675,185),GREEN,3)
  elif t<59.1:outline(im,(238,225,465,376),GREEN,3)
  else:outline(im,(233,541,1675,792),GREEN,3)
  footer(im,'Actual file replay · 4,096 subsets rechecked · 1 feasible · all four minimums satisfied')
 elif t<64.7:
  label(im,'09 / CHECK THE FAILURE PATH','Changed result. Verification fails.')
  txt(im,(83,258),'result.count',46,MUTED);txt(im,(82,321),'1 becomes 999',76,RUST,True)
  window(im,'receipt-rejected.png',(220,850,2340,1160),(90,586,1740,254))
  footer(im,'Actual negative test: altered saved count · previous success state removed')
 elif t<69.12:
  im=park_frame(6.5+(t-64.7)*.65,final)
  txt(im,(77,50),'THE NEXT REAL STEP',24,MUTED)
  txt(im,(73,103),'A real workshop.',76,INK,True)
  wrap(im,(79,240),'Local costs. Local knowledge. Residents at the table.',680,40,INK)
  footer(im,'Working prototype · illustrative data · no pilot or measured community impact claimed')
 else:
  txt(im,(78,80),'COMMON GROUND',24,MUTED)
  txt(im,(72,261),'Make the',115,INK,True);txt(im,(72,418),'compromise visible.',115,INK,True)
  txt(im,(81,699),'toukoursin.github.io/common-ground',39,RUST)
  txt(im,(81,843),'Original prototype by Touko Ursin · September 2026',27,MUTED)
  txt(im,(81,892),'Built with AI assistance · synthetic narration · original 3D and score',25,MUTED)
  if t>72.1:
   im=Image.blend(im,Image.new('RGB',(W,H),BG),ease((t-72.1)/1.1))
 return im

def timestamp(s):
 ms=round(s*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
def captions():
 a=json.loads((P/'alignment.json').read_text());chunks=[];current=[]
 for w in a['words']:
  current.append(w)
  if len(' '.join(x['text'] for x in current))>=58 or w['text'].endswith(('.', '?', '!')):
   chunks.append(current);current=[]
 if current:chunks.append(current)
 (P/'common-ground-v2.en.srt').write_text('\n\n'.join(f"{i+1}\n{timestamp(c[0]['start'])} --> {timestamp(max(c[-1]['end'],c[0]['start']+.2))}\n"+' '.join(x['text'] for x in c) for i,c in enumerate(chunks))+'\n')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--render',action='store_true');args=ap.parse_args();captions()
 manifest={'duration':D,'resolution':[W,H],'fps':FPS,'shots':[{'start':a,'end':b,'name':c} for a,b,c in beats],'source_note':__doc__,'creative_review':'Pending independent full normal-speed viewing with sound. Machine checks do not substitute.','source_frames':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in RAW.glob('*.png')},'timings':'Local Whisper alignment, machine estimates; narration not subjectively listened to.'}
 (P/'edit-manifest.json').write_text(json.dumps(manifest,indent=2))
 if args.preview:
  times=[1.8,5.5,8.9,14.4,22.1,26.7,31.2,36.6,39.2,46.9,50.8,53.5,59.4,63.1,66.1,70.4]
  sheet=Image.new('RGB',(1920,1080),BG)
  for i,t in enumerate(times):
   x=(i%4)*480;y=(i//4)*270;f=frame(t);f.save(P/f'preview-{t:04.1f}.jpg',quality=91);f=f.resize((480,270),Image.Resampling.LANCZOS);sheet.paste(f,(x,y));ImageDraw.Draw(sheet).text((x+4,y+4),str(t),fill='red')
  sheet.save(P/'contact-sheet.jpg',quality=94)
 if args.render:
  assert (P/'park-frames/frame_0300.png').exists(),'Full native3D sequence must finish first'
  cmd=['ffmpeg','-y','-hide_banner','-loglevel','warning','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-threads','2','-preset','medium','-crf','17','-pix_fmt','yuv420p',str(P/'picture-v2.mp4')]
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
  for n in range(round(D*FPS)):
   proc.stdin.write(frame(n/FPS,True).tobytes())
   if n%300==0:print(f'picture {n}/{round(D*FPS)}',flush=True)
  proc.stdin.close();assert proc.wait()==0
  subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','warning','-i',str(P/'picture-v2.mp4'),'-i',str(P/'narration.mp3'),'-i',str(P/'music.wav'),'-i',str(P/'sound.wav'),'-filter_complex_threads','2','-filter_complex','[1:a]loudnorm=I=-16:TP=-2:LRA=7,apad=whole_dur=73.2,asplit=2[v][side];[2:a]volume=0.48[m];[m][side]sidechaincompress=threshold=0.04:ratio=3:attack=12:release=320[duck];[v][duck][3:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.89[a]','-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-threads','2','-b:a','256k','-ar','48000','-t',str(D),'-movflags','+faststart',str(P/'common-ground-v2.mp4')],check=True)
if __name__=='__main__':main()
