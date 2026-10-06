import argparse
import opentimelineio as otio


def main(path):
    # Load the OTIO file
    timeline = otio.adapters.read_from_file(path)

    # Get the video track v1 and print the clips
    video_tracks = timeline.video_tracks() #video_tracks because is a list of tracks

    if not video_tracks:
        print(f"No valid video tracks in {path}")
        return

    v1 = video_tracks[0]

    for clip in v1:
        if not isinstance(clip, otio.schema.Clip):
            continue

        range_in_track = v1.range_of_child(clip)
        last_frame = (
            range_in_track.end_time_exclusive())

        print( 
            f"{clip.name} " 
            f"- Timecode in: {range_in_track.start_time.to_timecode()} " 
            f"- Timecode out: {last_frame.to_timecode()} " 
            f"- Source: {clip.source_range}" 
        )


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Print clips from an OTIO timeline",
                                     epilog="Have fun")
    parser.add_argument("path", help="Path to the OTIO timeline file")
    args = parser.parse_args()
    main(args.path) 