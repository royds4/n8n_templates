import json

with open("Generate subtitles on video (FFMPEG).json") as f:
    data = json.load(f)

# The user requested to update the FFmpeg command to create a 9:16 vertical split-screen.
# It seems this replaces the final ffmpeg assembly or the `Execute Command2` / `Execute Command3`.
# Wait, let's read the user request carefully:
# "Update the 'Execute Command' node that runs FFmpeg. We need to create a 9:16 vertical split-screen where the Tom Tucker video loops on the top half, and the dynamic asset (Pexels video or Chart-IMG) sits on the bottom half, synced to the TTS audio.
# Use the following exact FFmpeg command structure:
# ffmpeg -y -stream_loop -1 -i {{top_loop.mp4}} -stream_loop -1 -i {{bottom_dynamic.mp4}} -i {{voiceover.mp3}} -filter_complex \"[0:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,setsar=1[vtop]; [1:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960,setsar=1[vbot]; [vtop][vbot]vstack=inputs=2:shortest=1[stacked]; [stacked]subtitles={{captions.srt}}:force_style='FontName=Arial,FontSize=24,Alignment=2,OutlineColour=&H100000000,MarginV=100'[final_video]\" -map \"[final_video]\" -map 2:a -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k -shortest {{output.mp4}}"

# Wait, they say "synced to the TTS audio". The current workflow has `output_joined.mp4` as the top loop maybe?
# Previously, there were multiple FFmpeg nodes:
# `Execute Command` created `output.mp4` by looping `Tom Tucker News.mp4` and adding `TomTuckerAudio.mp3`.
# `Execute Command6` processed `Full{{signal}}.mp4` to `outputOllie.mp4`.
# `Execute Command7` joined `output.mp4` and `outputOllie.mp4` into `output_joined.mp4`.
# `Execute Command3` downloaded/processed a viral video into `output_background.mp4`.
# `Execute Command2` stacked `output_joined.mp4` (top) and `output_background.mp4` (bottom) into `output_reel.mp4`.
# `FFMPEG: make new video` burned subtitles into `output_reel.mp4` to create `final.mp4`.

# The user is giving us a single unified command that stacks top, bottom, adds audio, and burns subtitles all in one go.
# And they specifically mention:
#   {{top_loop.mp4}}
#   {{bottom_dynamic.mp4}}
#   {{voiceover.mp3}}
#   {{captions.srt}} -> Wait, the workflow currently generates `subtitles.ass` from `TS Audio` and `Create Ass` nodes.
# Let's see what the user exactly wrote: "Use the following exact FFmpeg command structure: ... ffmpeg -y -stream_loop -1 -i {{top_loop.mp4}} ...".
# They clearly intend for us to replace these placeholders with the actual file paths used in the workflow.

# Let's identify the files:
# top_loop.mp4 -> `output_joined.mp4` (which already has audio? Wait, if output_joined.mp4 has audio, do we need `voiceover.mp3`? The new command maps `2:a`, which is the 3rd input. So `output_joined.mp4` shouldn't provide the audio if we use `-map 2:a`. Actually, in the current workflow, `output_joined.mp4` HAS the combined audio.
# Wait, look at `Execute Command8`: it concatenates `TomTuckerAudio.mp3` and `signal.m4a` into `TomTuckerAudioFull.mp3`.
# Then `TS Audio` (Whisper) generates word timestamps for `TomTuckerAudioFull.mp3`, saved as `subtitles.ass`.
# So `voiceover.mp3` should be `TomTuckerAudioFull.mp3`.
# If we just loop the raw `Tom Tucker News.mp4` as `top_loop.mp4` and the new Pexels/Chart-IMG as `bottom_dynamic.mp4`, and `TomTuckerAudioFull.mp3` as `voiceover.mp3`, we might skip `Execute Command`, `Execute Command6`, `Execute Command7`, `Execute Command3`, `Execute Command2` entirely?
# Let's check the user prompt again: "Update the 'Execute Command' node that runs FFmpeg...".
# They say "the 'Execute Command' node". There are many. But one of them is literally named "FFMPEG: make new video". Or maybe they mean the one assembling everything?
# The prompt: "Update the 'Execute Command' node that runs FFmpeg. We need to create a 9:16 vertical split-screen where the Tom Tucker video loops on the top half, and the dynamic asset (Pexels video or Chart-IMG) sits on the bottom half, synced to the TTS audio."
# If I look at the workflow, `FFMPEG: make new video` is the node that does the final burn.
# But `Execute Command2` is the one doing the vstack right now!
# Let's combine `Execute Command2` and `FFMPEG: make new video` into a single node if the user command includes `subtitles=...`!
# The user's command: `ffmpeg -y -stream_loop -1 -i {{top_loop.mp4}} -stream_loop -1 -i {{bottom_dynamic.mp4}} -i {{voiceover.mp3}} -filter_complex "... [stacked]subtitles={{captions.srt}}:force_style='FontName=Arial,FontSize=24,Alignment=2,OutlineColour=&H100000000,MarginV=100'[final_video]" -map "[final_video]" -map 2:a ...`
# Wait, in the user's string, they use `subtitles={{captions.srt}}` but our workflow generates `subtitles.ass`. I should use `subtitles.ass`.
# Let's map the variables:
# FOLDER="/data/shared/{{$('Generate Directory').item.json.directory}}" (or `.first().json.directory`)
# top_loop.mp4 = `'/data/shared/Tom Tucker News.mp4'` or `output_joined.mp4`? The user says "Tom Tucker video loops on the top half". So just `'/data/shared/Tom Tucker News.mp4'`. But wait! What about Ollie? `output_joined.mp4` combines Tom Tucker and Ollie! Let's assume they want `output_joined.mp4` because it represents the top half content.
# Actually, the user says "where the Tom Tucker video loops on the top half". If I use `output_joined.mp4`, it already has audio, but we map `2:a` anyway so video 0 audio is ignored.
# What is bottom_dynamic.mp4?
# We recently added Pexels and Chart-IMG API downloads. These download to n8n's binary buffer.
# Where do these binary buffers get written to disk?
# Looking at the connections: `Pexels Download Success?` (True) -> `Merge6`
# `Chart-IMG Download` -> `Merge6`
# In the original workflow, `Merge6` went to `Execute Command3`, which read from `/data/shared/ViralVideos/$filename`... wait, `Execute Command3` didn't write the binary to disk!
# Oh, `HTTP Request3` output was just JSON with a `path`.
# Now, our Pexels/Chart-IMG nodes output binary data! We MUST write it to disk before FFmpeg can read it!
# But the user specifically asked to "Update the 'Execute Command' node that runs FFmpeg."

print("Analyzing what to replace...")
