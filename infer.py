from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import librosa
from scipy.signal import resample


# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
model.config.forced_decoder_ids = None

# load dummy dataset and read audio files
#ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
#sample = ds[0]["audio"]

audio_data, sample_rate = librosa.load('demo/received_audio.wav',sr=16000)

print(sample_rate)
input_features = processor(audio_data, sampling_rate=sample_rate, return_tensors="pt").input_features

# generate token ids
predicted_ids = model.generate(input_features)
# decode token ids to text
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print(transcription)