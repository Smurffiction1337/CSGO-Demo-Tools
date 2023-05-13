# CSGO DEMO PARSER
### BY SMURFFICTION#1337

# Parse Demo for Kills of an certain player and renders the scene with x seconds infront and afetrwards
# Custom settings: Resolution, Framerate, Target Player, add time before and after kill

import demoinfocs
import subprocess

# Set the path to the CS:GO demo file
demo_file = 'path_to_demo.dem'

# Set the target player's name
target_player_name = 'TargetPlayer'

# Set the desired video output resolution and frame rate
resolution = '3840x2160'  # 4K resolution
fps = 300

# Set the time range (in seconds) to capture before and after each kill
time_before = 10
time_after = 10

def render_video(segment_start, segment_end, output_file):
    # Use FFmpeg to render the video segment
    command = [
        'ffmpeg',
        '-i', demo_file,
        '-vf', f'select=gte(n\\,{segment_start * fps})\\,lte(n\\,{segment_end * fps})',
        '-s', resolution,
        '-r', str(fps),
        '-c:v', 'libx264',
        '-crf', '18',
        '-preset', 'slow',
        '-pix_fmt', 'yuv420p',
        output_file
    ]
    subprocess.run(command)

def extract_audio(output_file):
    # Use FFmpeg to extract the audio from the CS:GO demo
    command = [
        'ffmpeg',
        '-i', demo_file,
        '-vn',
        '-acodec', 'copy',
        output_file
    ]
    subprocess.run(command)

def merge_audio_video(video_file, audio_file, output_file):
    # Use FFmpeg to merge the video and audio files
    command = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', '-2',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        output_file
    ]
    subprocess.run(command)

# Open the CS:GO demo
demo = demoinfocs.parse(demo_file)

# Iterate over the game events to find kills by the target player
for game_event in demo.game_events:
    if isinstance(game_event, demoinfocs.events.bomb.BombDefused) or isinstance(game_event, demoinfocs.events.bomb.BombExplode):
        # Skip bomb-related events
        continue

    if isinstance(game_event, demoinfocs.events.round.RoundEnd):
        if game_event.winner_team == demo.teams[target_player_name].team:
            # The target player's team won the round, so they made the last kill
            segment_start = max(0, game_event.time - time_before)
            segment_end = min(demo.header.playback_ticks / demo.header.tick_rate, game_event.time + time_after)
            output_video_file = f'kill_{game_event.time}.mp4'  # Use the kill time as the video file name
            output_audio_file = f'kill_{game_event.time}.aac'  # Use the kill time as the audio file name
            output_merged_file = f'kill_{game_event.time}_merged.mp4'  # Use the kill time as the merged file name

            # Render the video segment
            render_video(segment_start, segment_end, output_video_file)

            # Extract the audio from the CS:GO demo
            extract_audio(output_audio_file)

            # Merge the video and audio files

````
