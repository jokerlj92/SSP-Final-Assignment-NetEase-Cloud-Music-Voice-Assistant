from pydub import AudioSegment
import os
from tensorflow.io import gfile
def read_audio_file(file_path):
    audio = AudioSegment.from_file(file_path)
    return audio

def convert_to_mono(audio):
    mono_audio = audio.set_channels(1)
    return mono_audio

def save_audio_file(audio, output_path):
    audio.set_frame_rate(16000).export(output_path, format='wav')

def check_output_file(output_path):
    if os.path.isfile(output_path):
        print("音频文件转换成功")
        return True
    else:
        print("音频文件转换失败")
        return False
def change(file_path, output_path):
    audio = read_audio_file(file_path)
    mono_audio = convert_to_mono(audio)
    save_audio_file(mono_audio, output_path)
    return check_output_file(output_path)
