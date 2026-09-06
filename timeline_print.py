import sys
import opentimelineio as otio

# Get the OTIO file path from the command line
path = sys.argv[1]

# Load the OTIO file
timeline = otio.adapters.read_from_file(path)

# Get the video track v1 and print the clips
video_track = timeline.video_tracks()

if video_track:
    v1 = video_track[0]

    for clip in v1:
        if isinstance(clip, otio.schema.Clip):
            range_in_track = v1.range_of_child(clip)
            last_frame = (
                range_in_track.end_time_exclusive())

            print( 
                f"{clip.name} " 
                f"- Timecode in: {range_in_track.start_time.to_timecode(rate=24)} " 
                f"- Timecode out: {last_frame.to_timecode()} " 
                f"- Source: {clip.source_range}" 
            )