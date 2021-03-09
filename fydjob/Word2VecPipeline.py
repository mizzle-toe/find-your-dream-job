
from gensim.models import Word2Vec
import json

class WordPipeline:

    def __init__(self,path = None):
        '''
        pass a path for the saved model file to instanciate a trained model or
        instanciate a empty model without an argument
        '''


        if path:
            self.w2v_model = Word2Vec.load(path)
        else:

            self.w2v_model = Word2Vec(min_count=20,
                             window=2,
                             size=20,
                             sample=6e-5,
                             alpha=0.03,
                             min_alpha=0.0007,
                             negative=20,
                        )

    def build_vocab(self,df):
        "build vocabulary for the w2v model"
        self.w2v_model.build_vocab(df, progress_per=10000)


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


        with open("../fydjob/data/dicts/skills_dict.json") as json_file:
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


















