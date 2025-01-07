import azure.cognitiveservices.speech as speechsdk

# Replace with your Azure Speech API Key and Region
speech_key = "<API KEY>"
service_region = "<AI Srevice Region>"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"

audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

result = speech_synthesizer.speak_text_async("Good morning this is an AI Quick Labs Demo!").get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized successfully.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print(f"Speech synthesis canceled: {cancellation_details.reason}")
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print(f"Error details: {cancellation_details.error_details}")
