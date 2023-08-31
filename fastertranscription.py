from faster_whisper import WhisperModel
import time
from datetime import timedelta

model_size = "large-v2"

model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribefaster(file_in):
    start_time = time.time()
    segments, _ = model.transcribe(file_in)
    segments = list(segments)
    result = ''
    for segment in segments:
        result += segment.text
    end_time = time.time()
    duration = str(timedelta(seconds=end_time-start_time))
    response = {"text":result,"duration":duration}
    return response
