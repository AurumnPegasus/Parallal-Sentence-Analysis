from nlp import NLP
from analysis import Analysis

class Main:
    '''
        Explanation: Driver class which handles all other functions and classes

        Class Variables:
            sent_en: Raw text from source file in English
            sent_hi: Raw text from source file in Hindi
            lang_en: Represents English
            lang_hi: Represents Hindi
    '''

    def __init__(self):
        '''
            Explanation: Initialisation function, used to initialise class variables
        '''
        self.sent_en = self.get_sent('data/english.txt')
        self.sent_hi = self.get_sent('data/hindi.txt')
        self.lang_en = 'en'
        self.lang_hi = 'hi'
    
    def get_sent(self, fileName):
        '''
            Explanation: Given a file, it reads it and returns it as a list of strings line by line

            Parameters:
                fileName: Name of the file

            Return:
                sentences: List of string
        '''
        f = open(fileName, 'r')
        lines = f.readlines()
        sentences = []
        for line in lines:
            sentences.append(line.strip())

        return sentences

    def get_json(self, lang, sentences):
        '''
            Explanation: Creates object of class NLP to get the list of sentences in appropriate tagged JSON format

            Parameters:
                lang: Language of the list of sentences
                sentences: List of string represeting the sentences
            
            Return:
                JSON object containing annotated values
        '''
        nlp = NLP(lang, sentences)
        return nlp.get_dependencies()

    def main(self):
        '''
            Explanation: Driver function used to process sentences and send it for analysis.
        '''
        parse_en = self.get_json(self.lang_en, self.sent_en)
        parse_hi = self.get_json(self.lang_hi, self.sent_hi)
        analysis = Analysis(parse_en, parse_hi)
        analysis.drive()


# Driver code
m = Main()
m.main()