from flask import Flask, render_template, request, jsonify   #调用flask工具中的Flask类
from transformers import pipeline, WhisperTokenizer, WhisperProcessor, WhisperForConditionalGeneration
from pathlib import Path
from llm_api_tests import get_output, say
from wake_up import wake_up
from change import change

app = Flask(__name__)         #定义一个实例对象叫app,引用flask类

MODEL_PATH1 = Path(
    r"C:\Users\LJyan\Documents\2023courseHW\SSP\ssp_final\model_output\whisper-small-cn1\checkpoint-20")

pipe = pipeline(
    task="automatic-speech-recognition",
    model="openai/whisper-small",
)

pipe.model = WhisperForConditionalGeneration.from_pretrained("Ancci/whisper-small-cn1")
pipe.tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-small", language="Chinese", task="transcribe")
pipe.processor = WhisperProcessor.from_pretrained("openai/whisper-small",
                                                  language="Chinese", task="transcribe")

if_wake_up = False

@app.route('/')
def index():
    return render_template("index1.html")


@app.route('/wakeup', methods=['POST'])
def wakeup():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        file_path = 'received_audio.wav'
        audio_file.save(file_path)
        if change(file_path, file_path):
            if wake_up(file_path):
                say('你好，我在')
                global if_wake_up
                if_wake_up = True
                print(if_wake_up)
                return jsonify({'text': '网易精灵', 'output': '你好，我在'})
            else:
                return jsonify({'text': ' ', 'output': '识别失败'})

    return 'No audio file received.'


@app.route('/upload', methods=['POST'])
def upload():
    global if_wake_up
    print(if_wake_up)
    if if_wake_up:
        if 'audio' in request.files:
            audio_file = request.files['audio']
            file_path = 'received_audio.wav'
            audio_file.save(file_path)

            # transcription = pipe('received_audio.wav')["text"]
            transcription = pipe('received_audio.wav', generate_kwargs={'language': 'zh'})["text"]
            print(f'Audio file processed successfully. {transcription}')

            txt = get_output(transcription)

            return jsonify({'text': transcription, 'output': txt})

        return 'No audio file received.'
    return 'Not wake up, please first wake up the assistant'


if __name__ == '__main__':
    app.run(debug=True)
