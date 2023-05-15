from pvrecorder import PvRecorder
import wave, struct 
import whisper

#load all audio input devices 

#for index, device in enumerate(PvRecorder.get_audio_devices()):
#    print(f"[{index}] {device}")


#setting up the recorder device
recorder = PvRecorder(device_index=-1, frame_length=512) #(32 milliseconds of 16 kHz audio)
audio = []
path = 'audio_recording.wav'


#loading the whisper model. We can try "tiny = 32x speed; base and medium they are better but slower"
tiny = whisper.load_model("tiny")
fp16=False


#when the text warning appears about "something is deprecated" we can talk intho the mic
try:
    recorder.start()
    while True:
        frame = recorder.read()
        audio.extend(frame)
except KeyboardInterrupt:
    recorder.stop()
    with wave.open(path, 'w') as f:
        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))
finally:
    recorder.delete()

#to exit press control+c


result=tiny.transcribe(path)
print(result["text"])