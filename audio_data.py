import librosa
from datasets import DatasetDict, load_from_disk, Audio, Dataset
import os
import numpy as np

filenames = os.listdir('specific_data/test/audio')

data = []
for name in filenames:
    audio_data, sample_rate = librosa.load(f'specific_data/test/audio/{name}', sr=48000)
    print(audio_data)
    f = open(f'specific_data/test/label/{name[:-4]}.txt','r',encoding='UTF-8')
    label = f.read()
    dic = {'audio': {'array': audio_data, 'sampling_rate': sample_rate}, 'sentence': label}
    data.append(dic)

custom_dataset = Dataset.from_dict({
    'audio': [item['audio'] for item in data],
    'sentence': [item['sentence'] for item in data]
})


common_voice = DatasetDict()

common_voice["test"] = custom_dataset

print(custom_dataset)

common_voice["test"].save_to_disk('Data_cache/specific/test')

# print(common_voice["train"][:5])
# print(common_voice["test"][:5])
# common_voice = common_voice.cast_column("audio", Audio(sampling_rate=16000))
#
# common_voice = common_voice.map(prepare_dataset, remove_columns=common_voice.column_names["test"], num_proc=1)
