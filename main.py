from nlp import NLP
from analysis import Analysis

class Main:

    def __init__(self):
        self.sent_en = self.get_sent('data/english.txt')
        self.sent_hi = self.get_sent('data/hindi.txt')
        self.lang_en = 'en'
        self.lang_hi = 'hi'
    
    def get_sent(self, fileName):
        f = open(fileName, 'r')
        lines = f.readlines()
        sentences = []
        for line in lines:
            sentences.append(line.strip())

        return sentences

    def get_json(self, lang, sentences):
        nlp = NLP(lang, sentences)
        return nlp.get_dependencies()

    def main(self):
        parse_en = self.get_json(self.lang_en, self.sent_en)
        parse_hi = self.get_json(self.lang_hi, self.sent_hi)
        analysis = Analysis(parse_en, parse_hi)
        analysis.drive()


m = Main()
m.main()