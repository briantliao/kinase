from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.environ.get('OPENAI_KEY')

model = 'whisper-1'

def get_vtt_transcript(file_name):
  print(f'Getting transcript from {file_name}')
  audio_file = open(file_name, 'rb')
  transcript = openai.Audio.transcribe(
    model,
    audio_file,
    response_format='vtt',
    prompt='Welcome to today\'slecture, silence, inaudible.',
    language='en'
  )
  print(f'File {file_name} transcript len: {len(transcript.splitlines())} lines')
  return transcript

def write_transcript_to_file(transcript, transcript_file_name):
  with open(transcript_file_name, 'w') as f:
    f.write(transcript)


file_name = 'videos/CHEM 1A - 2019-08-30/segment004/segment004.mp3'
transcript = get_vtt_transcript(file_name)
print(transcript)