"""TODO: Docstring."""

from pathlib import Path

import librosa
import numpy as np
from mido import Message, MidiFile, MidiTrack


def convert_to_midi(audio_file: Path, output_path: Path) -> None:
    """Convert audio files to MIDI.

    Args:
        audio_file (Path): _description_
    """
    # Step 1: Load the audio file
    y, sr = librosa.load(audio_file)

    rms = librosa.feature.rms(y=y)
    velocities = np.interp(rms.flatten(), (rms.min(), rms.max()), (50, 127)).astype(int)  # Map to MIDI range

    # Detect onsets for each note
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time")

    # Estimate durations based on the time between onsets or other techniques
    durations = np.diff(onsets, append=onsets[-1] + 0.5)  # Example with a constant tail duration
    midi_durations = [int(dur * 480 / sr) for dur in durations]  # Convert to MIDI ticks

    # Step 2: Extract pitches using pyin, which works better with vocals
    pitches, voiced_flags, _ = librosa.pyin(y, fmin=librosa.note_to_hz("C2"), fmax=librosa.note_to_hz("C7"), sr=sr)

    # Filter only voiced pitches
    notes = [(librosa.hz_to_midi(p), t) for t, p in enumerate(pitches) if voiced_flags[t]]

    # If lengths don't match, truncate to the length of the shorter list
    min_length = min(len(notes), len(midi_durations))
    notes = notes[:min_length]
    midi_durations = midi_durations[:min_length]

    # Step 3: Create MIDI file
    midi_file = MidiFile()
    track = MidiTrack()
    midi_file.tracks.append(track)

    for i, (note, t) in enumerate(notes):
        velocity = int(velocities[i])
        duration = int(midi_durations[i])
        # Add note_on event
        track.append(Message("note_on", note=int(note), velocity=velocity, time=int(t * sr)))

        # Add note_off event with calculated duration
        track.append(Message("note_off", note=int(note), velocity=velocity, time=duration))

    # Step 4: Save MIDI file
    output_file = "output.mid"
    midi_file.save(output_path / output_file)


if __name__ == "__main__":
    convert_to_midi(Path("data/htdemucs/Adele - Hello/vocals.flac"), Path("data/"))
