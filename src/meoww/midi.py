import pretty_midi
import librosa
import numpy as np
import soundfile as sf
import math


# Load the MIDI file
def load_midi(midi_file):
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    return midi_data


# Load the cat meow WAV file
def load_meow(wav_file):
    meow, sr = librosa.load(wav_file, sr=None)
    return meow, sr


# Estimate the original pitch of the meow using librosa's pyin function
def estimate_meow_pitch(meow, sr):
    # pyin returns a pitch contour; we take the median pitch where it's not 'None'
    f0, voiced_flag, voiced_probs = librosa.pyin(
        meow, fmin=librosa.note_to_hz("C1"), fmax=librosa.note_to_hz("C8")
    )
    # Remove 'None' values from pitch estimation and calculate median pitch
    f0_clean = f0[~np.isnan(f0)]
    if len(f0_clean) > 0:
        return np.median(f0_clean)
    else:
        return None  # No pitch detected


# Resample the meow to match the MIDI note's pitch
def pitch_shift_meow(meow, sr, midi_note, original_pitch):
    if original_pitch is None:
        # If pitch estimation failed, return the original meow unmodified
        return meow

    # MIDI note 69 is A4 (440 Hz), convert to frequency
    target_freq = pretty_midi.note_number_to_hz(midi_note)

    # Calculate the number of semitones to shift
    n_steps = np.log2(target_freq / original_pitch) * 12  # Convert frequency ratio to semitones

    # Shift pitch of meow by the calculated number of semitones
    shifted_meow = librosa.effects.pitch_shift(y=meow, sr=sr, n_steps=n_steps, bins_per_octave=12)

    return shifted_meow


# Convert MIDI notes to meows
def midi_to_meows(midi_data, meow, sr, original_pitch):
    combined_meow = np.array([])

    for instrument in midi_data.instruments:
        prev_note = instrument.notes[0]
        # combined_notes = []
        for note in instrument.notes[1:]:
            # Get the note's pitch (MIDI note number) and duration
            midi_note = note.pitch
            # duration = note.end - note.start

            if (
                (midi_note == prev_note.pitch)
                # or (
                #     abs(
                #         pretty_midi.note_number_to_hz(prev_note.pitch)
                #         - pretty_midi.note_number_to_hz(midi_note)
                #     )
                #     < 20
                # )
                and abs(note.start - prev_note.end) < 0.5
            ):
                prev_note.end = note.end
                continue

            # Resample meow to match the pitch of the MIDI note
            shifted_meow = pitch_shift_meow(meow, sr, prev_note.pitch, original_pitch)

            # Adjust the length of the meow to match the note duration
            stretched_meow = librosa.effects.time_stretch(
                shifted_meow, rate=len(shifted_meow) / (sr * (prev_note.end - prev_note.start))
            )

            # Concatenate the meows
            combined_meow = np.concatenate([combined_meow, stretched_meow])
            prev_note = note

    return combined_meow


# Save the result as a WAV file
def save_meows_to_wav(meow_audio, sr, output_file):
    sf.write(output_file, meow_audio, sr)


# Main function
def midi_to_meow_vocals(midi_file, meow_wav_file, output_file):
    midi_data = load_midi(midi_file)
    meow, sr = load_meow(meow_wav_file)

    # Estimate the original pitch of the meow
    original_pitch = estimate_meow_pitch(meow, sr)
    if original_pitch is None:
        print("Could not estimate the pitch of the cat meow.")
        return
    print(original_pitch)

    meow_audio = midi_to_meows(midi_data, meow, sr, original_pitch)

    save_meows_to_wav(meow_audio, sr, output_file)
    print(f"Meow vocals generated and saved to {output_file}")


# Example usage
midi_file = "data/basic_pitch_transcription(9).mid"
meow_wav_file = "data/meoww/meow-1.wav"
output_file = "data/songs/meow_vocals.wav"

midi_to_meow_vocals(midi_file, meow_wav_file, output_file)
