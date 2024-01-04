import torch
import torch.nn as nn
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import numpy as np
import tensorflow as tf
import os
import librosa
import tensorflow_io as tfio

#from tensorflow_io.core.python.experimental.audio_ops import trim


class Ourclassifer(nn.Module):
    def __init__(self, in_dim, n_hidden1, n_hidden2, out_dim=1, drop_prob1=0.5, drop_prob2=0.5):
        super(Ourclassifer, self).__init__()
        self.layer1 = nn.Linear(in_dim, n_hidden1)
        self.layer2 = nn.Linear(n_hidden1, n_hidden2)
        self.layer3 = nn.Linear(n_hidden2, out_dim)

        self.relu1 = nn.ReLU()
        self.relu2 = nn.ReLU()

        self.drop1 = nn.Dropout(drop_prob1)
        self.drop2 = nn.Dropout(drop_prob2)

        self.sigmoid = nn.Sigmoid()
        self.device = torch.device("cuda") if torch.cuda.is_available else torch.device("cpu")
        self.to(self.device)

    def forward(self, x):
        x = x.sum(dim=1)
        hidden_1_out = self.relu1(self.layer1(x))
        hidden_1_out = self.drop1(hidden_1_out)

        hidden_2_out = self.relu2(self.layer2(hidden_1_out))
        hidden_2_out = self.drop2(hidden_2_out)
        out = self.layer3(hidden_2_out)
        out = self.sigmoid(out)
        return out


class ExtendedWav2Vec2ForCTC(Wav2Vec2ForCTC):
    """
    In ESPNET there is a LayerNorm layer between encoder output and CTC classification head.
    """

    def __init__(self, config):
        super().__init__(config)
        self.myhead = Ourclassifer(in_dim=config.hidden_size, n_hidden1=config.hidden_size,
                                   n_hidden2=config.hidden_size)
        self.freeze_feature_extractor()
        self.freeze_base_model()
        self.lm_head = torch.nn.Sequential(
            torch.nn.LayerNorm(config.hidden_size),
            self.myhead
        )
        for param in self.lm_head.parameters():
            param.requires_grad = True
        self.to(self.myhead.device)


def get_voice_position(audio, noise_floor):
    audio = audio - np.mean(audio)
    audio = audio / np.max(np.abs(audio))
    return tfio.audio.trim(audio, axis=0, epsilon=noise_floor)


def wake_up(file_path):
    model_save_path = "../saved_model"
    processor = Wav2Vec2Processor.from_pretrained("kehanlu/mandarin-wav2vec2-aishell1")
    model = ExtendedWav2Vec2ForCTC.from_pretrained("kehanlu/mandarin-wav2vec2-aishell1")
    model.load_state_dict(torch.load(os.path.join(model_save_path + f"/final_wakeup_model.pth")))
    model.eval()
    sample_rate = 16000
    NOISE_FLOOR = 0.2

    audio_tensor = tfio.audio.AudioIOTensor(file_path)
    # print(audio_tensor)
    audio = tf.cast(audio_tensor[:], tf.float32)
    voice_start, voice_end = get_voice_position(audio, NOISE_FLOOR)
    voice_start = voice_start.numpy()[0]
    voice_end = voice_end.numpy()[0]

    valid_audio = audio_tensor[voice_start:voice_end].numpy().reshape(-1).astype(np.float32)

    inputs = processor(valid_audio, sampling_rate=sample_rate, return_tensors="pt")
    inputs['input_values'] = inputs['input_values'].to(model.device)
    logits = model(**inputs).logits
    # print(logits.item())
    if logits.item() > 0.5:
        return True
    return False
