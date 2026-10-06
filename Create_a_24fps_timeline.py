import opentimelineio as otio


def create_timeline():
    timeline = otio.schema.Timeline(
        name="24fps_5_clip_timeline"
    )

    # V1 - five video clips, 30 frames each
    video_track = otio.schema.Track(
        name="V1",
        kind="Video"
    )

    for i in range(5):
        clip = otio.schema.Clip(
            name=f"Video_{i + 1:03d}",
            source_range=otio.opentime.TimeRange(
                start_time=otio.opentime.RationalTime(0, 24),
                duration=otio.opentime.RationalTime(30, 24)
            )
        )

        video_track.append(clip)

    # A1 - one audio clip, 150 frames total
    audio_track = otio.schema.Track(
        name="A1",
        kind="Audio"
    )

    audio_clip = otio.schema.Clip(
        name="Audio_001",
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, 24),
            duration=otio.opentime.RationalTime(150, 24)
        )
    )

    audio_track.append(audio_clip)

    # Add tracks to timeline
    timeline.tracks.append(video_track)
    timeline.tracks.append(audio_track)

    return timeline


if __name__ == "__main__":

    output_file = "my_timeline.otio"

    timeline = create_timeline()

    otio.adapters.write_to_file(
        timeline,
        output_file
    )

    print(f"Created: {output_file}")