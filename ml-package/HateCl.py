import pickle


class HateCl:
    def __init__(self):
        self.classifier = pickle.load(open('randomforest.sav', 'rb'))

    def predict(self, text):
        classified_text = self.classifier.predict_proba([text])[:, 1]
        return classified_text[0]

    # working on
    def refit(self, samples):
        old_df = pickle.load(open('data.sav', 'rb'))
        old_df = old_df.append({'hate': samples[0][1], 'sentence': samples[0][0]}, ignore_index=True)
        print(old_df)


hatecl = HateCl()
hatecl.refit([('Achei horrível', 1)])