import os
import json
import fydjob
import joblib
from gensim.models import Word2Vec
from fydjob.W2VUtils import remove_number
from fydjob.W2VUtils import remove_punctuation_mod
from fydjob.W2VUtils import remove_stopwords
from fydjob.W2VUtils import lemmatize_words
from fydjob.W2VUtils import to_lower
from nltk.tokenize import sent_tokenize

home_path = os.path.dirname(fydjob.__file__)

class Word2VecPipeline:
    def __init__(self, df=None):
        print("Starting Word2Vec...")
        self.filepath = os.path.join(home_path, 'data', 'models', 'w2v_model_baseline.model')        
        self.df = df
        self.w2v_model = None
        self.text_field = None
        
        if os.path.exists(self.filepath):
            self.load_model()
        else:
            self.process_text_field()
            self.instantiate_model()
            self.build_vocab()
            self.train()
            self.save_model()
            

    def save_model(self):
        ''''saves the model as a .model file '''
        self.w2v_model.save(self.filepath)
        print("Saved model at", self.filepath)
        
    def load_model(self):
        '''Load the model.'''
        self.w2v_model = joblib.load(self.filepath)
        print("Loaded model from", self.filepath)
        
    def instantiate_model(self):
        ''''''
        self.w2v_model = Word2Vec(min_count=20,
                                    window=2,
                                    size=20,
                                    sample=6e-5,
                                    alpha=0.03,
                                    min_alpha=0.0007,
                                    negative=20,
                                    )
        
    def process_text_field(self):
        '''
        preprocess piple that returns a formatted text corpus as a list of
        tokens
        '''
        df = self.df.copy()
        df["job_text"] = df["job_text"].apply(to_lower)\
                                    .apply(remove_number)\
                                    .apply(lambda x : x.replace('\n',' '))\
                                    .apply(remove_punctuation_mod)\
                                    .apply(lambda x: sent_tokenize(x))\
                                    .apply(remove_stopwords)\
                                    .apply(lemmatize_words)
        sentences = df["job_text"].tolist()
        text_field = []
        for second in sentences:
            for first in second:
                text_field.append(first)
        self.text_field = text_field

    def build_vocab(self):
        "build vocabulary for the w2v model"
        self.w2v_model.build_vocab(self.text_field, progress_per=10000)


    def train(self):
        "train the model on the text"
        self.w2v_model.train(self.text_field, 
                             total_examples=self.w2v_model.corpus_count,
                             epochs=30, report_delay=1)

    def most_similar(self,query,topn = 10):
        "return the most similar words in the vector space"
        return self.w2v_model.wv.most_similar(query, topn =topn)
    
    def in_vocab(self, word):
        '''Return a bool indicating if word is in vocab.'''
        return word in self.w2v_model.wv.vocab

    def most_similar_skills(self,query,n_recommendations=10):
        '''
        returns the the number of similar skills specified in the n_recommendations
        argument based a string or list input or print error message when skill
        is not found
        '''

        if type(query) == str:
            query = query.lower()
        elif type(query) == list:
            query = [x.lower() for x in query]

        with open(os.path.join(home_path,"data","dicts","skills_dict.json")) as json_file:
            self.dictionary = json.load(json_file)

        term_list = []
        for cat in self.dictionary.keys():
            for word in self.dictionary[cat]:
                term_list.append(word)

        try:
            model_skills = self.most_similar(query,topn=100)
            skill_words = []
            for i in range(len(model_skills)):
                skill_words.append(model_skills[i][0])

            similar_skills = [skill for skill in skill_words if skill in term_list][0:n_recommendations]

            return similar_skills
        except:
            print("Sorry,word not found")









