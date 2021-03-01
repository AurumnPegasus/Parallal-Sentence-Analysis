import stanza
import json

class NLP:
    '''
        Explanation: Used to analyse the given sentences in languages and return tagged data

        Class Variables:
            lang: Specifies the language
            sentences: A list of strings with sentences
    '''

    def __init__(self, lang, sentences):
        '''
            Explanation: Initialisation function, used to initialise class variables and process data.
                         Uses the library stanza to annotate all the sentences
        '''
        self.sentences = sentences
        nlp_lang = stanza.Pipeline(lang)
        document = self.get_doc(sentences)
        self.doc = nlp_lang(document)
        self.n = len(sentences)

    def get_doc(self, sentences):
        '''
            Explanation: Converts list of sentences into a single string.

            Parameters:
                sentences: List of sentences

            Return:
                document: String containing all sentences seperated by space
        '''
        document = ""
        for i in sentences:
            document += i + ' '
        return document

    def get_dependencies(self):
        '''
            Explanation: Converts each annotated sentence into JSON list

            JSON Format:
                index: Contains index number of sentence
                sentence: Contains sentence as a string
                dependancy:
                    [
                        word: Contains word as a string
                        head: Contains the head of the word wrt sentence
                        relation: Contains the relation of the word wrt head
                        pos: Contains the UPOS tag
                    ]
        '''
        all = []

        for i in range(self.n):
            try:
                heads = []
                relations = []
                words = []
                pos = []
                depend = []
                for head, rel, dep in self.doc.sentences[i].dependencies:
                    heads.append(head.text)
                    relations.append(rel)
                    words.append(dep.text)

                for token in self.doc.sentences[i].words:
                    pos.append(token.upos)
                    
                for j in range(len(words)):
                    depend.append({
                        'word': words[j],
                        'head': heads[j],
                        'relation': relations[j],
                        'pos': pos[j]
                    })
                
                all.append({
                    'index': i, 
                    'sentence': self.sentences[i],
                    'dependancy': depend
                })
            except:
                # Handling cases where sentences do not end properly (stanza requires sentence to end with fullstop)
                all.append({
                    'index': i,
                    'sentence': self.sentences[i],
                    'dependancy': None
                })

        return json.loads(json.dumps(all))