> Updated checkpoint: the old unstarted job was cancelled by root after its waiter expired. Do not resume the old command unchanged. Enqueue a fresh unique job ID and update the executor to match before waiting. No final encode has run.

# Common Ground v2 final encode

The 300 source park frames are complete. `encode-preflight.json` records the passed asset checks, source hashes, 73.2-second timeline, 2,196 final frames, seven actual UI captures, narration, music, and effects. No scene or timing changes were made during encode preparation. The only change to `edit.py` caps the existing final audio filter/codec work at two threads.

Queue helper: `/Users/touko/work/helios-one/outputs/product-film-relaunch-2026-09-21/render-queue/render_queue.py`.

Named job: `commonground-v2-final-encode-20260922-0613`; owner: `commonground`.

`encode-queued.py` waits for up to ten minutes, checking once per minute. It only renders after this exact job receives `status: granted`; it never reprioritizes the queue, signals another job, or releases any other reservation. A timeout leaves the job queued and does not render. Do not run two copies concurrently. The original continuation reservation was released by its own watcher.

To resume after a bounded waiter has exited, from this repository:

```sh
/Users/touko/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 media/v2/encode-queued.py
```

After a grant, the script composes the existing film, checks the final MP4 metadata and a complete video/audio decode, measures peak/mean levels, and extracts twelve final-film stills. It writes `encode-run.json`, `final-encode.log`, `final-volume.txt`, and `final-review/*.png`, then releases only its own reservation after its child processes have exited.

Completion requires model inspection of those final-film stills and a provenance update. Technical decoding and peak measurement are not listening, a full normal-speed review, or subjective creative approval. The script explicitly records those limits. English captions remain the SRT sidecar; the existing film mux does not embed a subtitle stream.

No browser, YouTube, external publication, or YC material is part of this encode task. Root owns publication and the decision to replace earlier submitted media.
