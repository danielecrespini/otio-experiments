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
            track_range = v1.range_of_child(clip)
            last_frame = (
                track_range.end_time_exclusive()
                - otio.opentime.RationalTime(1, track_range.duration.rate)
            )

            print(
                clip.name,
                "- Timecode in:",
                otio.opentime.to_timecode(
                    clip.range_in_parent().start_time,
                    rate=24
                ),
                "- Timecode out:",
                last_frame.to_timecode(),
                "- Source:",
                clip.source_range
            )