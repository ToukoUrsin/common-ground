"""Offline forced alignment of the exact authored narration.

Requires existing local Whisper base.en weights + torch/whisper. No download/API.
Chunk boundaries come from an initial unprompted local transcription; that raw
transcript is preserved separately. Cross-attention DTW aligns the authored text,
so spoken number words and punctuation are preserved rather than ASR spelling.
These are machine estimates, not manually verified phonetic boundaries.
"""
from pathlib import Path
import json,hashlib,re,time
import numpy as np
import whisper,torch
from whisper.timing import find_alignment
from whisper.tokenizer import get_tokenizer
root=Path(__file__).resolve().parent
source=(root/'narration.txt').read_text().strip()
lines=source.splitlines()
chunks=[(0,10.50,' '.join(lines[0:2])),(10.50,19.55,lines[2]),(19.55,28.40,lines[3]),(28.40,38.15,lines[4]),(38.15,43.65,lines[5]),(43.65,49.30,lines[6]),(49.30,55.35,lines[7]),(55.35,64.70,lines[8]),(64.70,72.121179,' '.join(lines[9:11]))]
torch.set_num_threads(4)
model_path=Path.home()/'.cache/whisper/base.en.pt'
assert model_path.is_file(),'Expected existing local model; no downloads attempted'
model=whisper.load_model(str(model_path),device='cpu')
tokenizer=get_tokenizer(multilingual=False,language='en',task='transcribe')
audio=whisper.load_audio(str(root/'narration.mp3'))
words=[]
for start,end,text in chunks:
 part=audio[round(start*16000):round(end*16000)]
 mel=whisper.log_mel_spectrogram(whisper.pad_or_trim(part),n_mels=model.dims.n_mels)
 times=find_alignment(model,tokenizer,tokenizer.encode(' '+text),mel,num_frames=len(part)//160)
 for item in times:
  w=item.word
  if not w.startswith(' ') and words:
   words[-1]['text']+=w
   words[-1]['end']=round(start+float(item.end),3)
  else:
   words.append({'text':w.strip(),'start':round(start+float(item.start),3),'end':round(start+float(item.end),3),'token_probability':round(float(item.probability),4)})
assert ' '.join(w['text'] for w in words)==re.sub(r'\s+',' ',source)
# Sentence timings use exact words; colon/comma remain within the sentence.
sentences=[]; pending=[]
for i,w in enumerate(words):
 pending.append(i)
 if re.search(r'[.!?]$',w['text']):
  sentences.append({'text':' '.join(words[j]['text'] for j in pending),'start':words[pending[0]]['start'],'end':w['end'],'word_indices':pending})
  pending=[]
assert not pending
result={'schema':'common-ground.audio-alignment.v1','source_text':source,'duration':72.121179,'method':'Whisper base.en local forced cross-attention DTW on authored text, ASR-guided chunks','audio_sha256':hashlib.sha256((root/'narration.mp3').read_bytes()).hexdigest(),'model_sha256':hashlib.sha256(model_path.read_bytes()).hexdigest(),'subjectively_listened':False,'timing_note':'Machine estimated, 20 ms model resolution. No manual listening or phonetic verification. Chunk starts can slightly precede audible word onset.','chunks':[{'start':a,'end':b,'text':c} for a,b,c in chunks],'words':words,'sentences':sentences}
(root/'alignment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
for s in sentences: print(f"{s['start']:6.2f}–{s['end']:6.2f} {s['text']}")
