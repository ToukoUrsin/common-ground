"""Original procedural score and effects. No samples or third-party music.
Machine alignment guides the edit; this is not a claim of subjective listening.
"""
from pathlib import Path
import json, math, wave
import numpy as np
P=Path(__file__).resolve().parent; SR=48000; D=73.2; N=round(D*SR)
rng=np.random.default_rng(210926)
music=np.zeros((N,2),np.float64); effects=np.zeros_like(music)
def note(dst,start,duration,midi,amp=.06,pan=0,kind='felt'):
 n=round(duration*SR); t=np.arange(n)/SR; f=440*2**((midi-69)/12)
 if kind=='felt':
  env=(1-np.exp(-t*80))*np.exp(-t/1.4)*(1-np.minimum(t/duration,1))**.4
  y=(np.sin(2*np.pi*f*t+.7*np.sin(2*np.pi*f*2*t)*np.exp(-t*7))+.16*np.sin(2*np.pi*f*3*t)*np.exp(-t*5))*env
 elif kind=='air':
  env=np.sin(np.pi*np.minimum(t/duration,1))**1.7
  y=(np.sin(2*np.pi*f*t)+.23*np.sin(2*np.pi*f*2.002*t))*env
 else:
  env=(1-np.exp(-t*250))*np.exp(-t*25)
  y=(np.sin(2*np.pi*f*t)+rng.normal(0,.1,n))*env
 out=y[:,None]*amp*np.array([math.sqrt((1-pan)/2),math.sqrt((1+pan)/2)])
 i=round(start*SR); end=min(N,i+n)
 if i>=0:dst[i:end]+=out[:end-i]
# Sparse original motif. The dissonant interval enters with the explicit conflict,
# then opens into a wider F-major/add-nine voicing at the repair.
for start,chord in [(0,[50,57,64]),(7,[53,60,67]),(13,[50,57,65]),(20,[48,55,62]),(28,[50,56,63]),(33,[50,51,57]),(38.15,[53,60,67,69]),(43.65,[58,65,72]),(49.3,[53,60,67]),(55.35,[50,57,65]),(64.7,[53,60,67]),(69.12,[53,60,65])]:
 for k,m in enumerate(chord):note(music,start+k*.23,4.8,m,.047,(-.6+k*.4))
 note(music,start,5.8,chord[0]-12,.024,0,'air')
for start,seq in [(7.6,[72,69,67]),(14.2,[69,67,65]),(39,[72,74,77]),(45,[77,74,72]),(56,[72,69,67]),(66,[69,72,77])]:
 for k,m in enumerate(seq):note(music,start+k*.62,2.1,m,.032,[-.3,.3,0][k])
for j in range(28):note(effects,19.55+j*.17,.16,69+(j%4)*3,.010,math.sin(j)*.4,'wood')
for t,m in [(3.76,38),(28.4,45),(38.15,53),(43.65,72),(45.15,74),(46.53,77),(47.89,81),(52.3,79),(55.35,84),(61.45,49),(63.7,50),(69.12,77)]:note(effects,t,.65,m,.048,0,'wood')
# A real change in space: open the stereo field after the repaired plan.
for dst,name in [(music,'music.wav'),(effects,'sound.wav')]:
 fade=np.minimum(np.arange(N)/(SR*.12),1)*np.minimum((N-1-np.arange(N))/(SR*1.1),1)
 dst*=fade[:,None]
 pcm=np.clip(dst,-.95,.95); peak=float(np.max(np.abs(pcm)))
 with wave.open(str(P/name),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((pcm*32767).astype('<i2').tobytes())
 print(name,'peak dBFS',round(20*np.log10(max(peak,1e-9)),2))
(P/'audio-provenance.json').write_text(json.dumps({'score':'Original procedural composition, synthesized by audio.py; no sampled music','sample_rate':SR,'stems':['music.wav','sound.wav'],'narration':'ElevenLabs stock synthetic voice; exact local Whisper alignment in alignment.json','subjectively_listened':False,'mix_review':'Pending full normal-speed audio/video review'},indent=2))
