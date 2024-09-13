import os
from openai import AzureOpenAI
import json
import azure.cognitiveservices.speech as speechsdk


client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-02-01"
)

#deployment_name='gpt35turbo-lr-dev0'
deployment_name='gpt4o-lr-dev0'

response = client.chat.completions.create(
    model=deployment_name,
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": "Write in JSON format a short description of a cherry tree. One key of the json is for italian and one for english, content must be the same, only translated un the key 'text'."},
    ]
)

out_gpt = json.loads(response.choices[0].message.content)

english_text = out_gpt['english']['text']
italian_text = out_gpt['italian']['text']

print(f'PATIENT recieved the following information>>> {english_text}')


api_key = ''
region = 'eastus'

os.environ['SPEECH_KEY'] = api_key
os.environ['SPEECH_REGION'] = region

speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

#speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
speech_config.speech_synthesis_voice_name='it-IT-FabiolaNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

speech_synthesizer_result = speech_synthesizer.speak_text_async(italian_text)

if speech_synthesizer_result.get().reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    speech_synthesizer_result.get()
    audio_data = speech_synthesizer_result.get().audio_data
    with open('output2.mp3','wb') as file:
        file.write(audio_data)












