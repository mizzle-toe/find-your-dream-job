

class WordPipeline:

    def __init__(self):

        self.w2v_model = Word2Vec(min_count=20,
                         window=2,
                         size=20,
                         sample=6e-5,
                         alpha=0.03,
                         min_alpha=0.0007,
                         negative=20,
                        )

    def build_vocab(self,df):
        self.w2v_model.build_vocab(df, progress_per=10000)


    def train(self,df):
        self.w2v_model.train(df, total_examples=self.w2v_model.corpus_count,
                                 epochs=30, report_delay=1)

    def most_similar(self,query,topn = 10):

        return self.w2v_model.wv.most_similar(query, topn =topn)

    def most_similar_skills(self,query,n_recommendations):

        self.dictionary = json.load("/data/dicts/skills_dict.json")

        term_list = []
        for cat in dictionary.keys():
            for word in dictionary[cat]:
                term_list.append(word)

        try:
            model_skills = self.most_similar(query)
            skill_words = []
            for i in range(len(model_skills)):
                skill_words.append(model_skills[i][0])

            similar_skills = [skill for skill in skill_words if skill in term_list][0:n_recommendations]

            return similar_skills
        except:
            print("Sorry,word not found")
















