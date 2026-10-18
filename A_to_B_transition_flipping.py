#!/usr/bin/env python3

import argparse
import copy
from pathlib import Path

import opentimelineio as otio


def flip_transitions(timeline):
    """Move transitions from the outgoing side of a cut to the incoming side."""
    result = copy.deepcopy(timeline)

    for track in result.tracks:
        items = tuple(track)
        original_ranges = {
            id(item): (item.range_in_parent(), item.duration())
            for item in items
            if isinstance(item, otio.schema.Transition)
        }

        for i, item in enumerate(items):
            if not isinstance(item, otio.schema.Transition):
                continue

            if i == 0 or i == len(items) - 1:
                continue

            previous = items[i - 1]
            following = items[i + 1]

            if not (
                isinstance(previous, otio.schema.Clip)
                and isinstance(following, otio.schema.Clip)
            ):
                continue

            original_range, original_duration = original_ranges[id(item)]
            item.in_offset, item.out_offset = (
                item.out_offset,
                item.in_offset,
            )

            shift = original_range.start_time - item.range_in_parent().start_time
            if shift.value:
                previous_range = previous.trimmed_range()
                new_duration = previous_range.duration + shift
                if new_duration.value < 0:
                    raise ValueError(
                        f"Cannot preserve transition timing on track "
                        f"{track.name!r}: the preceding clip would have "
                        "a negative duration."
                    )

                new_range = otio.opentime.TimeRange(
                    previous_range.start_time,
                    new_duration,
                )
                available_range = previous.media_reference.available_range
                if available_range is not None and (
                    new_range.start_time < available_range.start_time
                    or new_range.end_time_exclusive()
                    > available_range.end_time_exclusive()
                ):
                    raise ValueError(
                        f"Cannot preserve transition timing on track "
                        f"{track.name!r}: adjusting the preceding clip "
                        "would exceed its media range."
                    )

                previous.source_range = new_range

            adjusted_range = item.range_in_parent()
            if (
                adjusted_range.start_time != original_range.start_time
                or item.duration() != original_duration
            ):
                raise RuntimeError(
                    f"Failed to preserve transition timing on track "
                    f"{track.name!r}."
                )

    return result


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Move transitions to the incoming side of the cut while "
            "preserving their timeline positions and durations."
        )
    )
    parser.add_argument("input", help="Input .otio file")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = input_path.with_name(
        f"{input_path.stem}_flipped{input_path.suffix}"
    )

    timeline = otio.adapters.read_from_file(str(input_path))
    modified = flip_transitions(timeline)
    otio.adapters.write_to_file(modified, str(output_path))

    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
