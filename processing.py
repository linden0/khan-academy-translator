from moviepy.editor import *
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from synchronize import format_transcript,assemble_translated_transcript,identify_pauses,insert_pauses
import pafy
import os
import json, csv
from accuracy import bert_score_accuracy,sbert_accuracy
from translator import Translator

class DataFileSystem:
    def __init__(self, dir, vid):
        self.dir = dir
        self.vid = vid
        self.translated_dir = os.path.join(dir, 'translated_videos')
        self.intermediate_dir = os.path.join(dir, 'intermediate_files', vid)
        self.sentences_dir = os.path.join(dir, 'sentences')
        os.makedirs(self.translated_dir, exist_ok=True)
        os.makedirs(self.intermediate_dir, exist_ok=True)
        os.makedirs(self.sentences_dir, exist_ok=True)

    def csv_path(self):
        return os.path.join(self.sentences_dir, f'{self.vid}.csv')

    def write_csv(self, bertscore_F1, bertscore_P, bertscore_R, sbert,
                sentences, back_sentences, trans_sentences):

        with open(self.csv_path(), 'w') as csvfile:
            fieldnames = ['bertscore_F1', 'bertscore_P', 'bertscore_R',
                        'sbert', 'sent_orig', 'sent_back', 'sent_trans']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(sentences)):
                writer.writerow({'bertscore_F1': bertscore_F1[i],
                                'bertscore_P': bertscore_P[i],
                                'bertscore_R': bertscore_R[i],
                                'sbert': sbert[i],
                                'sent_orig': sentences[i],
                                'sent_back': back_sentences[i],
                                'sent_trans': trans_sentences[i]})

def process_video(language, url, path, download_path, translator, gen_output_video=True):
    #get video id
    video_id = pafy.new(url).videoid

    # find or create input/output folders
    filesys = DataFileSystem(path, video_id)

    # check if video has been translated
    if (os.path.exists(os.path.join(filesys.sentences_dir, video_id+'.csv'))):
        print('already translated')
        return

    # grab video transcript and download video
    transcript = YouTubeTranscriptApi.get_transcript(video_id)


    #reformat transcript so each item is sentence, not fragment
    formatted_transcript = format_transcript(transcript)
    if formatted_transcript is None:
        print(url + ' has a punctuation error, cannot format transcript')
        return


    # translate text to target language
    translator = Translator(language, translator)
    original_sentences = [sent_obj['text'] for sent_obj in formatted_transcript]
    translated_sentences = translator.fwd_translate_batch(original_sentences)

    #calculate accuracy
    back_sentences = translator.back_translate_batch([trans_sent for trans_sent in translated_sentences])
    bert_mean,bert_P,bert_R,bert_F1 = bert_score_accuracy(original_sentences, back_sentences)
    sbert_mean,sbert_scores = sbert_accuracy(original_sentences, back_sentences)

    filesys.write_csv(bert_F1, bert_P, bert_R, sbert_scores, original_sentences, back_sentences, translated_sentences)


    if gen_output_video:
        if not os.path.exists(os.path.join(download_path, 'english_original_video_'+ video_id+ '.mp4')):
            YouTube('http://youtube.com/watch?v=' + video_id).streams.get_highest_resolution().download(download_path, filename='english_original_video_' + video_id + '.mp4')
            print('downloaded ' + video_id +'.mp4')
        else:
            print('using cached video')

        #create translated version of formatted_text and save translated audio file
        buffer_output_path = os.path.join(filesys.intermediate_dir, 'temp_audio_buffer.wav')
        translated_audio_output_path = os.path.join(filesys.intermediate_dir, 'audio_without_pauses.wav')
        translated_formatted_transcript = assemble_translated_transcript(formatted_transcript, translated_sentences,
            language, buffer_output_path, translated_audio_output_path)

        #create audio/video neccessary pause lists
        print('creating pause lists')
        pauses = identify_pauses(formatted_transcript,translated_formatted_transcript)
        video_pause_list = pauses['video_pause_list']
        audio_pause_list = pauses['audio_pause_list']

        #add neccessary pauses to video/audio
        print('inserting pauses')
        video_input_path = os.path.join(download_path,'english_original_video_'+video_id+'.mp4')
        video_output_path = os.path.join(filesys.intermediate_dir,'video_with_pauses.mp4')
        audio_input_path = os.path.join(filesys.intermediate_dir,'audio_without_pauses.wav')
        audio_output_path = os.path.join(filesys.intermediate_dir,'audio_with_pauses.wav')
        insert_pauses(video_pause_list,audio_pause_list,formatted_transcript,video_input_path,video_output_path,audio_input_path,audio_output_path)

        #export final result
        print('building final video')
        final_audio = AudioFileClip(audio_output_path)
        final_video = VideoFileClip(video_output_path)
        translated_video = final_video.set_audio(final_audio)
        translated_video.write_videofile(os.path.join(filesys.translated_dir,video_id+'_result.mp4'), audio_bitrate='3000k')

