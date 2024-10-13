from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import tensorflow

# print(ICASSP_2022_MODEL_PATH)

predict_and_save(
    ["data/songs/billi_vocal.wav"],
    "data/",
    True,
    True,
    False,
    False,
    ICASSP_2022_MODEL_PATH,
)
