import azure.cognitiveservices.speech as speechsdk

# Replace with your Azure Speech API Key and Region
speech_key = "<API KEY>"
service_region = "<AI Srevice Region>"

# Configure the Speech SDK
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Create a speech recognizer using the default microphone
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Speak into your microphone...")

# Start recognition
result = speech_recognizer.recognize_once()

# Check the result
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print(f"Recognized: {result.text}")
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print(f"Speech recognition canceled: {cancellation_details.reason}")
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print(f"Error details: {cancellation_details.error_details}")
