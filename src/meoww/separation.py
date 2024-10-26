"""TODO: Docstring."""

from pathlib import Path

import demucs.separate


def separate(path: Path, out: Path, shifts: int = 10) -> None:
    """Separate vocals from an audio file using Demucs.

    Args:
        path (Path): Path to the audio file.
        out (Path): Path to the output directory.
        shifts (int, optional): Number of shifts for the Demucs algorithm. Defaults to 10.

    Raises:
        FileNotFoundError: If the audio file specified by `path` does not exist.
        FileNotFoundError: If the output directory specified by `out` does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"File {path} does not exist.")

    if not out.exists():
        raise FileNotFoundError(f"Directory {out} does not exist.")

    demucs.separate.main(
        [
            str(path),
            "-o",
            str(out),
            "--shifts",
            f"{shifts}",
            "--two-stems",
            "vocals",
            "--flac",
        ],
    )


if __name__ == "__main__":
    separate(Path("/home/vandy/work/meoww/data/Adele - Hello.flac"), Path("data/"))
