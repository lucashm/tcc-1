import pandas as pd
import curses, time
import sys, tty, termios
from stop_words import get_stop_words
import nltk
import unicodedata
import re


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def remove_accent_from_words(word):
    nfkd = unicodedata.normalize('NFKD', word)
    withouth_accent = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z0-9 \\\]', '', withouth_accent)

def classify_text(csv):
    df = pd.read_csv(csv)
    if(set(list(df.columns.values)) != set(['text', 'classification'])):
        df.columns = ["text"]
        df['classification'] = 'None'
        print("entrei")
    counter = 0
    data = {'text': [], 'classification': []}
    print(df.head())
    for index, row in df.iterrows():
        print (row["text"], row["classification"])
        if(row['classification'] == 'None'):
            key = get_key()
            if(key == 's'):
                print('pos!')
                row['classification'] = 'pos'
            elif(key == 'n'):
                print('neg!')
                row['classification'] = 'neg'
            else:
                break
            data['text'].append(row['text'])
            data['classification'].append(row['classification'])
        counter +=1
    
    new_df = pd.DataFrame(data=data)
    new_df.to_csv('./classificated_texts.csv', encoding='utf-8', index=False, mode='a', header=False)
    df.drop(df.index[:counter], inplace=True)
    df.to_csv(csv, encoding='utf-8', index=False)

classify_text('../text-blob/pos_tweets.1.csv')



def normalize_text(csv):
    df = pd.read_csv(csv)
    if(set(list(df.columns.values)) != set(['text', 'classification'])):
        df.columns = ["text"]
        df['classification'] = 'None'

    stop_words = get_stop_words('pt')
    for index, row in df.iterrows():
        row['text'] = row['text'].lower()
        split = row['text'].split()
        split = [remove_accent_from_words(word) for word in split]
        for word in stop_words:
            if word in split:
                split.remove(word)
        row['text'] = ' '.join(split)
    
    df.to_csv(csv, encoding='utf-8', index=False)

def text_to_stem(csv):
    df = pd.read_csv(csv)
    if(set(list(df.columns.values)) != set(['text', 'classification'])):
        df.columns = ["text"]
        df['classification'] = 'None'

    stemmer = nltk.stem.RSLPStemmer()
    for index, row in df.iterrows():
        if type(row['text']) == type('str'):
            split = row['text'].split()
            split = [stemmer.stem(word) for word in split]
            row['text'] = ' '.join(split)
    
    df.to_csv(csv, encoding='utf-8', index=False)
        

    

# text_to_stem('../text-blob/all_tweets.csv')
# normalize_text('./classificated_texts.csv')