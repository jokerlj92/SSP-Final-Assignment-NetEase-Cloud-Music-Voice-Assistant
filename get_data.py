from datasets import load_dataset, DatasetDict, Audio, load_from_disk
from transformers import WhisperFeatureExtractor, WhisperTokenizer, WhisperProcessor
from huggingface_hub import notebook_login

notebook_login()

# common_voice["train"] = load_dataset("mozilla-foundation/common_voice_11_0", "hi", split="validation", use_auth_token=True)

# common_voice = load_dataset("mozilla-foundation/common_voice_11_0", "zh-CN", split="validation", use_auth_token=True)
# common_voice = common_voice.remove_columns(["accent", "age", "client_id", "down_votes", "gender", "locale", "path", "segment", "up_votes"])
# train_percentage = 0.8  # 训练集所占比例
# common_voice = common_voice.train_test_split(train_size=train_percentage)
#
# common_voice.save_to_disk(dataset_dict_path='./Data_cache/raw_data')

common_voice = DatasetDict()

common_voice["train"] = load_from_disk("./Data_cache/raw_data/train")
common_voice["test"] = load_from_disk("./Data_cache/raw_data/test")

feature_extractor = WhisperFeatureExtractor.from_pretrained("openai/whisper-small")
tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-small", language="Hindi", task="transcribe")
common_voice = common_voice.cast_column("audio", Audio(sampling_rate=16000))

def prepare_dataset(batch):
    # load and resample audio data from 48 to 16kHz
    audio = batch["audio"]
    # compute log-Mel input features from input audio array
    batch["input_features"] = feature_extractor(audio["array"], sampling_rate=audio["sampling_rate"]).input_features[0]
    # encode target text to label ids
    batch["labels"] = tokenizer(batch["sentence"]).input_ids
    return batch


common_voice = common_voice.map(prepare_dataset, remove_columns=common_voice.column_names["train"], num_proc=1)
common_voice.save_to_disk(dataset_dict_path='./Data_cache/fea_data')