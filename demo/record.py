import pyaudio
import numpy as np
import wave
import time

class Record_wav:
    def Monitor_MIC(th, filename):
        CHUNK = 512
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000 	#录音时的采样率
        WAVE_OUTPUT_FILENAME = filename + ".wav"
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []

        while (True):
            print("ready for recording" + str(time.localtime(time.time()).tm_sec))
            for i in range(0, 5):
                data = stream.read(CHUNK)
                frames.append(data)
            audio_data = np.fromstring(data, dtype=np.short)
            temp = np.max(audio_data)
            if temp > th :
                print("detected a signal")
                print('current threshold:',temp)
                less = []
                frames2 = []
                while (True):
                    print("recording")
                    for i in range(0, 30):
                        data2 = stream.read(CHUNK)
                        frames2.append(data2)
                    audio_data2 = np.fromstring(data2, dtype=np.short)
                    temp2 = np.max(audio_data2)
                    if temp2 < th:
                        less.append(-1)
                        print("below threshold, counting: ", less)
                        #如果有连续15个循环的点，都不是声音信号，就认为音频结束了
                        if len(less) == 3:
                            break
                    else:
                        less = []
                break
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames2))
        wf.close()


Record_wav.Monitor_MIC(1000, '1')