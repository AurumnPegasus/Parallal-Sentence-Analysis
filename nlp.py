import stanza
import json

class NLP:

    def __init__(self, lang, sentences):
        self.sentences = sentences
        nlp_lang = stanza.Pipeline(lang)
        document = self.get_doc(sentences)
        self.doc = nlp_lang(document)
        self.n = len(sentences)

    def get_doc(self, sentences):
        document = ""
        for i in sentences:
            document += i + ' '
        return document

    def get_dependencies(self):
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
                all.append({
                    'index': i,
                    'sentence': self.sentences[i],
                    'dependancy': None
                })

        return json.loads(json.dumps(all))