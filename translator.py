from deep_translator import GoogleTranslator
import deepl
class Translator:

    def __init__(self, dest_lang, translator_name):
        self.translator_name = translator_name

        if translator_name == 'google':
            self.language_code_map = {'zh-cn':'zh-CN','es':'es'}
            self.translator = GoogleTranslator
            self.dest_lang = self.language_code_map[dest_lang]

        elif translator_name == 'deepl':
            self.language_code_map = {'zh-cn':'zh','es':'es'}
            self.translator = deepl.Translator('Deepl Key')
            self.dest_lang = self.language_code_map[dest_lang]

    def fwd_translate_batch(self, sentence_list):
        if self.translator_name == 'google':
            return self.translator(source='en', target=self.dest_lang).translate_batch(sentence_list)
        elif self.translator_name == 'deepl':
            return [sent.text for sent in self.translator.translate_text(sentence_list,target_lang=self.dest_lang)]            

    def back_translate_batch(self,sentence_list):
        if self.translator_name == 'google':
            return self.translator(source=self.dest_lang, target='en').translate_batch(sentence_list)
        elif self.translator_name == 'deepl':
            return [sent.text for sent in self.translator.translate_text(sentence_list,target_lang='EN-US')] 

