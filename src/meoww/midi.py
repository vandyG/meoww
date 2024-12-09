"""TODO: Docstring."""

from pathlib import Path

from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict_and_save


def convert_to_midi(audio_file: Path, output_path: Path) -> None:
    """Convert audio files to MIDI.

    Args:
        audio_file (Path): _description_
    """
    predict_and_save(
        audio_path_list=[audio_file],
        output_directory=output_path,
        save_midi=True,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
    )


if __name__ == "__main__":
    convert_to_midi(Path("data/htdemucs/Adele - Hello/vocals.flac"), Path("data/"))
