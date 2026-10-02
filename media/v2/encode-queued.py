"""Run one final encode only after this named cooperative queue reservation is granted.
A bounded queue wait is not an encode. Does not reprioritize, signal, or release other jobs.
"""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time
P=Path(__file__).resolve().parent
QUEUE=Path('/Users/touko/work/helios-one/outputs/product-film-relaunch-2026-09-21/render-queue/render_queue.py')
JOB='commonground-v2-final-encode-20260922-0613'
OWNER='commonground'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def q(action,*extra):
 run=subprocess.run([sys.executable,str(QUEUE),action,'--job',JOB,'--owner',OWNER,*extra],capture_output=True,text=True)
 try:value=json.loads(run.stdout)
 except Exception:raise RuntimeError('Queue returned invalid JSON; no render authorized')
 return run.returncode,value

def main():
 deadline=time.monotonic()+600
 last=None
 while True:
  code,result=q('acquire')
  status=result.get('status')
  if status=='granted':break
  if status!='waiting':raise RuntimeError(f'Queue refused job: {result}')
  summary={'status':status,'reason':result.get('reason'),'position':result.get('position'),'active':(result.get('active') or {}).get('id')}
  if summary!=last:print(json.dumps(summary),flush=True);last=summary
  if time.monotonic()>=deadline:
   print(json.dumps({'status':'bounded_wait_finished','job':JOB,'encode_started':False}),flush=True)
   return
  time.sleep(min(60,max(0,deadline-time.monotonic())))
 print(json.dumps({'status':'granted','job':JOB,'pid':os.getpid(),'at':stamp()}),flush=True)
 code,pid_result=q('set-pid','--pid',str(os.getpid()))
 if code!=0:raise RuntimeError('PID registration failed; retain reservation, no render')
 record={'job':JOB,'owner':OWNER,'pid':os.getpid(),'granted_at':stamp(),'grant':result,'scope':'one2196-frame composition, audio mux and technical QA; no scene changes','subjective_sound_review':False,'full_normal_speed_review':False}
 (P/'encode-run.json').write_text(json.dumps(record,indent=2)+'\n')
 try:
  pre=json.loads((P/'encode-preflight.json').read_text())
  assert pre['status']=='passed' and pre['park_manifest_status']=='rendered'
  manifest=json.loads((P/'park-render-manifest.json').read_text());assert manifest['status']=='rendered'
  pre['edit_py_sha256']=hashlib.sha256((P/'edit.py').read_bytes()).hexdigest()
  pre['execution_only_change']='Audio complex-filter and codec thread limits explicitly set to2; no scene, timing or mix changes.'
  (P/'encode-preflight.json').write_text(json.dumps(pre,indent=2)+'\n')
  record['edit_py_sha256']=pre['edit_py_sha256']
  with (P/'final-encode.log').open('w') as log:
   subprocess.run([sys.executable,str(P/'edit.py'),'--render'],cwd=P.parents[1],stdout=log,stderr=subprocess.STDOUT,check=True)
  target=P/'common-ground-v2.mp4'
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(target)]))
  video=next(s for s in probe['streams'] if s['codec_type']=='video')
  audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
  assert (video['width'],video['height'])==(1920,1080)
  assert video['codec_name']=='h264' and video['r_frame_rate']=='30/1'
  assert int(video['nb_frames'])==2196
  assert abs(float(probe['format']['duration'])-73.2)<.05
  assert audio['codec_name']=='aac' and int(audio['sample_rate'])==48000
  decode=subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(target),'-map','0:v:0','-map','0:a:0','-threads','2','-f','null','-'],capture_output=True,text=True)
  assert decode.returncode==0 and not decode.stderr.strip(),decode.stderr
  vol=subprocess.run(['ffmpeg','-hide_banner','-threads','2','-i',str(target),'-vn','-af','volumedetect','-threads','2','-f','null','-'],capture_output=True,text=True,check=True)
  (P/'final-volume.txt').write_text(vol.stderr)
  stills=P/'final-review';stills.mkdir(exist_ok=True)
  times=[1.8,5.5,14.4,22.1,31.2,39.2,42.0,46.9,59.4,63.1,66.1,70.4]
  for sec in times:
   subprocess.run(['ffmpeg','-v','error','-y','-threads','2','-ss',str(sec),'-i',str(target),'-frames:v','1','-threads','2',str(stills/f'{sec:04.1f}.png')],check=True)
  record.update({'status':'encoded_technical_checks_passed','finished_at':stamp(),'file':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'probe':probe,'full_video_audio_decode':'passed','stills_for_visual_review':times,'visual_review':'pending model inspection','captions':'English sidecar common-ground-v2.en.srt; no embedded subtitle track in existing edit.py output'})
 except Exception as exc:
  record.update({'status':'failed','finished_at':stamp(),'error':str(exc)})
  raise
 finally:
  (P/'encode-run.json').write_text(json.dumps(record,indent=2)+'\n')
  # All owned subprocess.run calls have returned before this release. Never release another job.
  code,released=q('release','--confirm-job-stopped','--note',f"CommonGround final encode worker finished: {record.get('status')}; all owned child processes exited. Full subjective review pending.")
  print(json.dumps({'release':released,'record':str(P/'encode-run.json')}),flush=True)
  if code!=0:raise RuntimeError('Owned queue release failed; inspect queue before another job')
if __name__=='__main__':main()
