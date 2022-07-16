# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
# Licensed under the Amazon Software License  http://aws.amazon.com/asl/

import boto3
import pyaudio
import os
import asyncio
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import Result, Transcript, TranscriptEvent
from pytictoc import TicToc
import concurrent

t = TicToc() #create instance of class
input_rate = 44100
target_rate = 32000
defaultframes = 1024
class textcolors:
    if not os.name == 'nt':
        blue = '\033[94m'
        green = '\033[92m'
        warning = '\033[93m'
        fail = '\033[91m'
        end = '\033[0m'
    else:
        blue = ''
        green = ''
        warning = ''
        fail = ''
        end = ''
recorded_frames = []
device_info = {}
useloopback = False
recordtime = 100

#Use module
p = pyaudio.PyAudio()

#Set default to first in list or ask Windows
try:
    default_device_index = p.get_default_input_device_info()
except IOError:
    default_device_index = -1

#Select Device
print (textcolors.blue + "Available devices:\n" + textcolors.end)
for i in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print (textcolors.green + str(info["index"]) + textcolors.end + ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))
    if default_device_index == -1:
        default_device_index = info["index"]

#Handle no devices available
if default_device_index == -1:
    print (textcolors.fail + "No device available. Quitting." + textcolors.end)
    exit()

#Get input or default
device_id = int(input("Choose device [" + textcolors.blue + str(default_device_index) + textcolors.end + "]: ") or default_device_index)
print ("")

#Get device info
try:
    device_info = p.get_device_info_by_index(device_id)
except IOError:
    device_info = p.get_device_info_by_index(default_device_index)
    print (textcolors.warning + "Selection not available, using default." + textcolors.end)

#Choose between loopback or standard mode
is_input = device_info["maxInputChannels"] > 0
is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
if is_input:
    print (textcolors.blue + "Selection is input using standard mode.\n" + textcolors.end)
else:
    if is_wasapi:
        useloopback = True;
        print (textcolors.green + "Selection is output. Using loopback mode.\n" + textcolors.end)
    else:
        print (textcolors.fail + "Selection is input and does not support loopback mode. Quitting.\n" + textcolors.end)
        exit()

polly = boto3.client('polly', region_name = 'us-west-2')
translate = boto3.client(service_name='translate', region_name='us-west-2', use_ssl=True)
transcription = ''
running_average = []
count = 0
total_latency = 0

async def mic_stream():
    # This function wraps the raw input stream from the microphone forwarding
    # the blocks to an asyncio.Queue.
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()
    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, indata)
        return (indata, pyaudio.paContinue)
    # Be sure to use the correct parameters for the audio stream that matches
    # the audio formats described for the source language you'll be using:
    # https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html
    print(device_info)
    #Open stream
    channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
    stream = p.open(format = pyaudio.paInt16,
                channels = channelcount,
                rate = int(device_info["defaultSampleRate"]),
                input = True,
                frames_per_buffer = defaultframes,
                input_device_index = device_info["index"],
                stream_callback=callback)
    # Initiate the audio stream and asynchronously yield the audio chunks
    # as they become available.
    stream.start_stream()
    print("started stream")
    while True:
        indata = await input_queue.get()
        yield indata

class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        global count
        global running_average
        global total_latency

        t.tic()
        # This handler can be implemented to handle transcriptions as needed.
        # In this case, we're simply printing the finished 
        results = transcript_event.transcript.results
        print("firing outputs..", results)
        if len(results) > 0:
            if len(results[0].alternatives) > 0:
                transcript = results[0].alternatives[0].transcript
                print("transcript:", transcript)

                print(results[0].channel_id)
                if hasattr(results[0], "is_partial") and results[0].is_partial == False:
                    t.tic()
                    #translate only 1 channel. the other channel is a duplicate
                    if results[0].channel_id == "ch_0":
                        trans_result = translate.translate_text(
                            Text = transcript,
                            SourceLanguageCode = params['source_language'],
                            TargetLanguageCode = params['target_language']
                        )
                        print("translated text:" + trans_result.get("TranslatedText"))
                        text = trans_result.get("TranslatedText")

                        #For doing accuracy measurements. Remove when not required.
                        with open("transcribe.txt", "a", encoding='utf-8') as f:
                            f.write(transcript + "\n")

                        with open("translate.txt", "a", encoding='utf-8') as f:
                            f.write(text + "\n")

                        await loop.run_in_executor(executor, aws_polly_tts, text)
                    t.toc("full result sent to translate and polly :")

        count += 1
        total_latency += t.tocvalue()
        running_average = total_latency/count
        if (count % 1000 == 0) == True:
            print("Average Time so far: ", running_average)

def stream_data(stream):
    """Consumes a stream in chunks to produce the response's output'"""
    print("Streaming started...")
    chunk = 1024
    if stream:
    # Note: Closing the stream is important as the service throttles on
    # the number of parallel connections. Here we are using
    # contextlib.closing to ensure the close method of the stream object
    # will be called automatically at the end of the with statement's
    # scope.
        polly_stream = p.open(
                    format = pyaudio.paInt16,
                    channels = 1,
                    rate = 16000,
                    output = True,
                    )

        #this is a blocking call..
        while True:
            data = stream.read(chunk)
            polly_stream.write(data)
            # If there's no more data to read, stop streaming
            if not data:
                stream.close()
                polly_stream.stop_stream()
                polly_stream.close()
                print("got to if not data      :) ")
                break
            # Ensure any buffered output has been transmitted and close the
            # stream
            # self.wfile.flush() CLOSE STEAM 
        print("Streaming completed.")
    else:
        # The stream passed in is empty
        print("Nothing to stream.")

def aws_polly_tts(text):
    t.tic()
    response = polly.synthesize_speech(
        Engine = 'standard',
        LanguageCode = params['lang_code_for_polly'],
        Text=text,
        VoiceId = params['voice_id'],
        OutputFormat = "pcm",
    )
    #play back into microphone
    #playback asap the buffer fills-in
    #https://aws.amazon.com/blogs/machine-learning/building-a-reliable-text-to-speech-service-with-amazon-polly/
    byte_stream = response['AudioStream']
    stream_data(byte_stream)

    t.toc("Processed Polly Stream in : ")
   
async def transcribe():
# Setup up our client with our chosen AWS region

    client = TranscribeStreamingClient(region="us-west-2")
    stream = await client.start_stream_transcription(
        language_code=params['lang_code_for_transcribe'],
        media_sample_rate_hz=int(device_info["defaultSampleRate"]),
        number_of_channels = 2,
        enable_channel_identification=True,
        media_encoding="pcm",
    )
    recorded_frames = []
    async def write_chunks(stream):
        
        # This connects the raw audio chunks generator coming from the microphone
        # and passes them along to the transcription stream.
        print("getting mic stream")
        async for chunk in mic_stream():
            t.tic()
            recorded_frames.append(chunk)
            await stream.input_stream.send_audio_event(audio_chunk=chunk)
            t.toc("chunks passed to transcribe: ")
        await stream.input_stream.end_stream()

    handler = MyEventHandler(stream.output_stream)
    await asyncio.gather(write_chunks(stream), handler.handle_events())



direction = 1
direction = int(input("Choose source and target language to translate. 1 for en to zh, 2 for zh to en [" + textcolors.blue + str(direction) + textcolors.end + "]: ") or default_device_index)
params = {}

if direction == 1:
    params['source_language'] = "en"
    params['target_language'] = "hi"
    params['lang_code_for_polly'] = "cmn-CN"
    params['voice_id'] = "Zhiyu"
    params['lang_code_for_transcribe'] = "en-US"
elif direction == 2:
    params['source_language'] = "zh"
    params['target_language'] = "en"
    params['lang_code_for_polly'] = "en-US"
    params['voice_id'] = "Joanna"
    params['lang_code_for_transcribe'] = "zh-CN"
else:
    raise Exception("Languages not implemented!")

executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
loop = asyncio.get_event_loop()
loop.run_until_complete(transcribe())
loop.close()