from constants import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Analysis:

    def __init__(self, en, hi):
        self.en = en
        self.hi = hi
        self.ENGLISH = GREEN
        self.HINDI = PURPLE

    def get_ngram(self, data, n):
        gram = {}

        for obj in data:
            for i in range(len(obj['dependancy'])):
                words = []
                
                if len(obj['dependancy']) < n:
                    continue

                if i == (len(obj['dependancy']) - n):
                    break

                for j in range(n):
                    words.append(obj['dependancy'][i + j]['pos'])

                ngram = ""
                for word in words:
                    ngram += word + '-'
                ngram = ngram[:-1]

                if ngram in gram:
                    gram[ngram] += 1
                else:
                    gram[ngram] = 1

        temp = [(v, k) for k, v in gram.items()]
        return sorted(temp, reverse=True)

    def unigram_graph(self, en, hi):
        tags = ['NOUN', 'PROPN', 'ADJ', 'VERB', 'ADP']
        y_eng = []
        y_hin = []
        
        for tup in en:
            if tup[1] in tags:
                y_eng.append(tup[0])
        
        for tup in hi:
            if tup[1] in tags:
                y_hin.append(tup[0])
            
        ind = np.arange(len(tags))
        plt.figure(figsize=(10, 5))
        
        width = 0.3
        
        english_patch = mpatches.Patch(color=self.ENGLISH, label='English')
        hindi_patch = mpatches.Patch(color=self.HINDI, label='Hindi')
        plt.bar(ind, y_eng, width, label='English', color=self.ENGLISH)
        plt.bar(ind + width, y_hin, width, label='Hindi', color=self.HINDI)
        plt.grid(alpha=0.4)
        plt.xlabel('POS Tags')
        plt.ylabel('Frequency')
        plt.xticks( ind + width/2, tags)
        plt.legend(loc='best')
        plt.title('Unigram POS')
        plt.savefig('graphs/unigram_POS.png')
    
    def ngram_graph(self, data, n, lang, threshold):

        title = str(n) + 'gram POS, ' + lang

        tags= []
        y = []

        for tup in data:
            if tup[0] <= threshold:
                break
            tags.append(tup[1])
            y.append(tup[0])

        plt.figure(figsize=(10, 10))
        if lang == 'hi':
            hindi_patch = mpatches.Patch(color=self.HINDI, label='Hindi')
            plt.bar(tags, y, color=self.HINDI)
            plt.legend(handles=[hindi_patch])
        else:
            english_patch = mpatches.Patch(color=self.ENGLISH, label='English')
            plt.bar(tags, y, color=self.ENGLISH)
            plt.legend(handles=[english_patch])

        plt.title(title)    
        plt.xticks(rotation=45)
        plt.grid(alpha=0.4)
        plt.xlabel('POS Tags')
        plt.ylabel('Frequency')
        plt.savefig('graphs/' + title + '.png')
    
    def ngram(self):
        unigram_en = self.get_ngram(self.en, 1)
        unigram_hi = self.get_ngram(self.hi, 1)
        self.unigram_graph(unigram_en, unigram_hi)
        bigram_en = self.get_ngram(self.en, 2)
        bigram_hi = self.get_ngram(self.hi, 2)
        self.ngram_graph(bigram_en, 2, 'en', BIGRAM_THRESHOLD)
        self.ngram_graph(bigram_hi, 2, 'hi', BIGRAM_THRESHOLD)
        trigram_en = self.get_ngram(self.en, 3)
        trigram_hi = self.get_ngram(self.hi, 3)
        self.ngram_graph(trigram_en, 3, 'en', TRIGRAM_THRESHOLD)
        self.ngram_graph(trigram_hi, 3, 'hi', TRIGRAM_THRESHOLD)

    def get_order(self, data):
        wo = {}

        for obj in data:
            word_order = ""

            for w in obj['dependancy']:
                if w['relation'] == 'nsubj' or w['relation'] == 'root' or w['relation'] == 'obj':
                    word_order += w['relation'] + ' '
                
            if word_order in wo:
                wo[word_order] += 1
            else:
                wo[word_order] = 1
                
        temp = [(v, k) for k, v in wo.items()]
        return sorted(temp, reverse=True)

    def order_graph(self, data, lang):
        wo = []
        y = []
        
        for tup in data:
            wo.append(tup[1])
            y.append(tup[0])
            
        plt.figure(figsize=(10, 5))
        if lang == 'hi':
            hindi_patch = mpatches.Patch(color=self.HINDI, label='Hindi')
            plt.bar(wo, y, color=self.HINDI)
            plt.legend(handles=[hindi_patch])
            plt.title('Word Order Hindi')
        else:
            english_patch = mpatches.Patch(color=self.ENGLISH, label='English')
            plt.bar(wo, y, color=self.ENGLISH)
            plt.legend(handles=[english_patch])
            plt.title('Word Order English')
        
        plt.grid(alpha=0.4)
        plt.xlabel('Order')
        plt.ylabel('Frequency')
        plt.savefig('graphs/Word Order, ' + lang + '.png')
    
    def word_order(self):
        hi_order = self.get_order(self.hi)[:HI_ORDER]
        en_order = self.get_order(self.en)[:EN_ORDER]
        self.order_graph(hi_order, 'hi')
        self.order_graph(en_order, 'en')
    
    def get_position(self, data, heading, property):

        after = 0
        before = 0

        for obj in data:
            word_list = []
            for w in obj['dependancy']:
                if w[heading] == property:
                    if w['head'] in word_list:
                        after += 1
                    else:
                        before += 1
                
                word_list.append(w['word'])

        return [before, after]
    
    def position_graph(self, en, hi, x, title):
        ind = np.arange(len(x))
        plt.figure(figsize=(10, 10))
        width = 0.3
        english_patch = mpatches.Patch(color=self.ENGLISH, label='English')
        hindi_patch = mpatches.Patch(color=self.HINDI, label='Hindi')
        plt.bar(ind, en, width, label='English', color=self.ENGLISH)
        plt.bar(ind + width, hi, width, label='Hindi', color=self.HINDI)
        plt.grid(alpha=0.4)
        plt.xlabel('Position')
        plt.ylabel('Frequency')
        plt.xticks( ind + width/2, x)
        plt.legend(loc='best')
        plt.title(title)
        plt.savefig('graphs/' + title + '.png')
    
    def position(self):
        en_comp = self.get_position(self.en, 'relation', 'compound')
        hi_comp = self.get_position(self.hi, 'relation', 'compound')
        en_adp = self.get_position(self.en, 'pos', 'ADP')
        hi_adp = self.get_position(self.hi, 'pos', 'ADP')
        en_adj = self.get_position(self.en, 'pos', 'ADJ')
        hi_adj = self.get_position(self.hi, 'pos', 'ADJ')
        self.position_graph(en_comp, hi_comp, ['Before', 'After'], "Position of Compound Relation")
        self.position_graph(en_adp, hi_adp, ['Preposition', 'Postposition'], "Position of Adposition")
        self.position_graph(en_adj, hi_adj, ['Before', 'After'], "Noun Adjective Order")
    
    def drive(self):
        self.ngram()
        self.word_order()
        self.position()