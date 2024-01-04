from transformers import WhisperFeatureExtractor, WhisperTokenizer, WhisperProcessor
from datasets import DatasetDict, load_from_disk, Audio

common_voice = DatasetDict()

common_voice["train"] = load_from_disk("specific/train")
common_voice["test"] = load_from_disk("specific/test")

feature_extractor = WhisperFeatureExtractor.from_pretrained("../whisper-small")

tokenizer = WhisperTokenizer.from_pretrained("../whisper-small", language="Chinese", task="transcribe")

processor = WhisperProcessor.from_pretrained("../whisper-small", language="Chinese", task="transcribe")

def prepare_dataset(batch):
    # load and resample audio data from 48 to 16kHz
    audio = batch["audio"]

    # compute log-Mel input features from input audio array
    batch["input_features"] = feature_extractor(audio["array"], sampling_rate=audio["sampling_rate"]).input_features[0]

    # encode target text to label ids
    batch["labels"] = tokenizer(batch["sentence"]).input_ids
    return batch

common_voice = common_voice.cast_column("audio", Audio(sampling_rate=16000))

common_voice = common_voice.map(prepare_dataset, remove_columns=common_voice.column_names["test"], num_proc=1)

common_voice["train"].save_to_disk('specific/fea_data/train')
common_voice["test"].save_to_disk('specific/fea_data/test')