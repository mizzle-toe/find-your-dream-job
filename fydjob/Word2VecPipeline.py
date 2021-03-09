'''
1. Look for a saved model and if present, load it
    2. If not, instantiate empty model 
    3. Add a new field to df with processed text 
    4. Build vocab 
    5. Train and save model 
6. Prediction
'''


from gensim.models import Word2Vec
import os
import fydjob
import json


home_path = os.path.dirname(fydjob.__file__)
model_path = os.path.join(home_path, 'data', 'models', 'w2v_model_baseline.model')

class WordPipeline:

    def __init__(self, path = model_path):
        '''
        pass a path for the saved model file to instanciate a trained model or
        instanciate a empty model without an argument
        '''
        if os.path.exists(path):
            self.w2v_model = Word2Vec.load(path)
        else:
            #TODO: DEFINE PIPELINE FOR BUILDING THE MODEL
            
            self.w2v_model = Word2Vec(min_count=20,
                             window=2,
                             size=20,
                             sample=6e-5,
                             alpha=0.03,
                             min_alpha=0.0007,
                             negative=20,
                        )
            
    def process_text_field(self, df):
        ''''''
        

    def build_vocab(self,text_field):
        "build vocabulary for the w2v model"
        self.w2v_model.build_vocab(text_field, progress_per=10000)


    def train(self,df):
        "train the model on the text"
        self.w2v_model.train(df, total_examples=self.w2v_model.corpus_count,
                                 epochs=30, report_delay=1)

    def most_similar(self,query,topn = 10):
        "return the most similar words in the vector space"

        return self.w2v_model.wv.most_similar(query, topn =topn)


    def most_similar_skills(self,query,n_recommendations):
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


















