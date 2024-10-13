from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import tensorflow

# print(ICASSP_2022_MODEL_PATH)

model_output, midi_data, note_events = predict_and_save(
    ["/home/vandy/work/meoww/data/songs/vocals.wav"],
    "data/",
    True,
    True,
    False,
    False,
    ICASSP_2022_MODEL_PATH,
)
