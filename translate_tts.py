import requests, uuid, json
import os
import io
from pydub import AudioSegment
from pydub.playback import play
import azure.cognitiveservices.speech as speechsdk

def play_audio_from_bytes(audio_data, format='mp3'):
    audio_data_io = io.BytesIO(audio_data)
    audio_segment = AudioSegment.from_file(audio_data_io, format=format)
    play(audio_segment)

# Add your key and endpoint
key_translate = ""
endpoint_translate = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location_translate = "eastus"

path = '/translate'
constructed_url = endpoint_translate + path

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': ['it']
}

headers = {
    'Ocp-Apim-Subscription-Key': key_translate,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location_translate,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# You can pass more than one object in body.
body = [{
    'text': 'I would really like to drive your car around the block a few times!'
}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()
text = response[0]['translations'][0]['text']


api_key = ''
region = 'eastus'

os.environ['SPEECH_KEY'] = api_key
os.environ['SPEECH_REGION'] = region

speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

speech_synthesizer_result = speech_synthesizer.speak_text_async(text)

if speech_synthesizer_result.get().reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    speech_synthesizer_result.get()
    audio_data = speech_synthesizer_result.get().audio_data
    with open('output1.mp3','wb') as file:
        file.write(audio_data)





