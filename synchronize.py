from moviepy.editor import *
from gtts import gTTS
from pydub import AudioSegment
import os
from pathlib import Path
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print('downloading punkt tokenizer')
    nltk.download('punkt')

def format_transcript(transcript):
    """
    format transcript so each item is the start of a sentence, not sentence fragment

    :param transcript: array of dicts ([{'text':..., 'start':..., 'duration':...}])
    :return: array of dicts
    """
    #remove line breaks
    for d in transcript:
        d['text'] = d['text'].replace("\n", " ")


    #split the whole text by sentence
    full_text = ' '.join(d['text'] for d in transcript)




    sentences = nltk.tokenize.sent_tokenize(full_text)
    formatted_transcript = []
    sentence_index = 0
    cur_dict = transcript[0]
    i = 0
    while i < len(transcript):

            if (cur_dict['text'].strip()) == (sentences[sentence_index].strip()):
                formatted_transcript.append(cur_dict)
                if i == len(transcript)-1:
                    break
                cur_dict = transcript[i+1]
                sentence_index+=1
                i += 1
            else:
                i += 1
                try:
                    cur_dict['text'] += ' ' + transcript[i]['text']
                except:
                    return

                cur_dict['duration'] += transcript[i]['duration']

    return formatted_transcript

def assemble_translated_transcript(formatted_transcript, translated_sentences, language, chunk_path, translated_audio_output_path):
    """
    creates translated version of transcript, where text is translated and timestamps are adjusted appropriately
    and exports full, translated audio

    :param transcript: array of dicts
    :param language: string of destination language code
    :param translated_text: string of translated transcription text
    :param chunk_path: string (where audio chunks should be stored)
    :param translated_audio_output_path: string
    :return: array of dicts
    """
    translated_formatted_transcript = []
    running_length = 0
    translated_unpaused_audio = AudioSegment.silent(duration=formatted_transcript[0]['start'])

    f = open(os.path.dirname(translated_audio_output_path) + '/translated_sentences.txt', 'w')
    assert(os.stat(os.path.dirname(translated_audio_output_path) + '/translated_sentences.txt').st_size==0)
    for i in range(len(formatted_transcript)):
        sentence = translated_sentences[i]

        f.write(sentence + '\n')
        myobj = gTTS(text=sentence, lang=language, slow=False)
        myobj.save(chunk_path)
        audio = AudioSegment.from_file(chunk_path)
        if i == 0:
            translated_formatted_transcript.append(
                {'text': sentence, 'start': formatted_transcript[0]['start'], 'duration': audio.duration_seconds})
        else:
            translated_formatted_transcript.append(
                {'text': sentence, 'start': running_length, 'duration': audio.duration_seconds})
        translated_unpaused_audio += audio
        running_length += audio.duration_seconds
    assert(len(formatted_transcript) == len(translated_formatted_transcript))
    f.close()
    #export translated audio and delete temporary audio segements
    translated_unpaused_audio.export(translated_audio_output_path, format="wav")
    os.remove(chunk_path)

    return translated_formatted_transcript

def identify_pauses(formatted_transcript,translated_formatted_transcript):
    """
    identify pauses necessary to synchronize video and audio

    :param formatted_transcript: array of dicts
    :param translated_formatted_transcript: array of dicts
    :return: dict of video and audio pause lists (array of tuples)
    """
    video_pause_list = []
    audio_pause_list = []
    assert(len(formatted_transcript)==len(translated_formatted_transcript))
    for i in range(len(formatted_transcript) - 1):
        if i == 0:
            if formatted_transcript[i]['duration'] < translated_formatted_transcript[i]['duration']:
                video_pause_list.append((formatted_transcript[i]['duration'],
                                         translated_formatted_transcript[i]['duration'] - formatted_transcript[i][
                                             'duration']))
            elif formatted_transcript[i]['duration'] > translated_formatted_transcript[i]['duration']:
                audio_pause_list.append((translated_formatted_transcript[i]['duration'],
                                         formatted_transcript[i]['duration'] - translated_formatted_transcript[i][
                                             'duration']))
        else:
            if formatted_transcript[i]['duration'] < translated_formatted_transcript[i]['duration']:
                video_pause_list.append((formatted_transcript[i + 1]['start'],
                                         translated_formatted_transcript[i]['duration'] - formatted_transcript[i][
                                             'duration']))
            elif formatted_transcript[i]['duration'] > translated_formatted_transcript[i]['duration']:
                audio_pause_list.append((translated_formatted_transcript[i + 1]['start'],
                                         formatted_transcript[i]['duration'] - translated_formatted_transcript[i][
                                             'duration']))
    return {'video_pause_list':video_pause_list,'audio_pause_list':audio_pause_list}

def insert_pauses(video_pause_list,audio_pause_list,formatted_transcript,video_input_path,video_output_path,audio_input_path,audio_output_path):
    """
    use audio/video pause list to insert pauses

    :param video_pause_list: array of tuples
    :param audio_pause_list: array of tuples
    :param formatted_transcript: array of dicts
    :param video_input_path: string
    :param video_output_path: string
    :param audio_input_path: string
    :param audio_output_path: string
    :return: None
    """
    #implement video pauses and save
    video = VideoFileClip(video_input_path)
    video_pause_list.append((video.duration - 0.5, 0))
    clips = []
    for i, segment in enumerate(video_pause_list):
        if i == 0:

            clips.append(video.subclip(formatted_transcript[0]['start'], segment[0]))
            clips.append(CompositeVideoClip([video.to_ImageClip(segment[0]).set_duration(segment[1])]))
        else:

            clips.append(video.subclip(video_pause_list[i - 1][0], segment[0]))
            clips.append(CompositeVideoClip([video.to_ImageClip(segment[0]).set_duration(segment[1])]))

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(video_output_path, fps=video.fps, audio_bitrate="3000k")

    #implement audio pauses and save
    audio_file = audio_input_path
    audio = AudioSegment.from_file(audio_file)
    audio_pause_list.append((audio.duration_seconds,0))
    final_clip = audio[:audio_pause_list[0][0]*1000] + AudioSegment.silent(duration=audio_pause_list[0][1]*1000)

    for i,segment in enumerate(audio_pause_list):
        if i==0:
            continue
        else:

            final_clip += audio[audio_pause_list[i-1][0]*1000:segment[0]*1000]
            final_clip += AudioSegment.silent(duration=segment[1]*1000)
    final_clip.export(audio_output_path, format="wav")