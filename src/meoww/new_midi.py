import pretty_midi
import librosa
import numpy as np
import soundfile as sf


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
    f0, voiced_flag, voiced_probs = librosa.pyin(
        meow, fmin=librosa.note_to_hz("C1"), fmax=librosa.note_to_hz("C8")
    )
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

    # Shift pitch of meow by the calculated number of semitones without altering the length
    shifted_meow = librosa.effects.pitch_shift(y=meow, sr=sr, n_steps=n_steps, bins_per_octave=12)

    return shifted_meow


# Adjust the length of the meow to match the note duration
def adjust_meow_length(meow, sr, note_duration):
    required_length = int(sr * note_duration)  # Convert note duration to samples

    # If meow is longer than required, trim it
    if len(meow) > required_length:
        return meow[:required_length]

    # If meow is shorter than required, pad with zeros (silence)
    elif len(meow) < required_length:
        padding = np.zeros(required_length - len(meow))
        return np.concatenate([meow, padding])

    # If the meow length matches the note duration, return as is
    else:
        return meow


# Superimpose the meows on the vocal MIDI notes
def midi_to_meows(midi_data, meow, sr, original_pitch):
    combined_audio = np.zeros(
        int(midi_data.get_end_time() * sr)
    )  # Create empty audio array for output

    for instrument in midi_data.instruments:
        if not instrument.is_drum:  # Ensure we're only processing pitched instruments
            for note in instrument.notes:
                midi_note = note.pitch
                start_time = int(note.start * sr)  # Convert start time to samples
                end_time = int(note.end * sr)  # Convert end time to samples
                note_duration = note.end - note.start

                # Resample meow to match the pitch of the MIDI note
                shifted_meow = pitch_shift_meow(meow, sr, midi_note, original_pitch)

                # Adjust the meow's length to match the note duration
                adjusted_meow = adjust_meow_length(shifted_meow, sr, note_duration)

                # Overlay the meow onto the combined_audio at the correct position
                combined_audio[start_time : start_time + len(adjusted_meow)] += adjusted_meow[
                    : len(combined_audio) - start_time
                ]

    return combined_audio


# Save the result as a WAV file
def save_meows_to_wav(meow_audio, sr, output_file):
    sf.write(output_file, meow_audio, sr)


# Main function to process the MIDI and meow and combine them
def midi_to_meow_vocals(midi_file, meow_wav_file, output_file):
    # Load MIDI and Meow files
    midi_data = load_midi(midi_file)
    meow, sr = load_meow(meow_wav_file)

    # Estimate the original pitch of the meow
    original_pitch = estimate_meow_pitch(meow, sr)
    if original_pitch is None:
        print("Could not estimate the pitch of the cat meow.")
        return
    print(f"Estimated original meow pitch: {original_pitch} Hz")

    # Process the MIDI notes and generate meow vocals
    meow_audio = midi_to_meows(midi_data, meow, sr, original_pitch)

    # Save the final output as a WAV file
    save_meows_to_wav(meow_audio, sr, output_file)
    print(f"Meow vocals superimposed on MIDI saved to {output_file}")


# Example usage
midi_file = "data/songs/jb.mid"  # MIDI file of the vocals
meow_wav_file = "data/meoww/meow-1.wav"  # Meow recording
output_file = "data/songs/meow_vocals_output.wav"  # Output file

midi_to_meow_vocals(midi_file, meow_wav_file, output_file)
