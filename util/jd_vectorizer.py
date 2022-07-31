from nltk.corpus import stopwords
import re, pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer

def vectorize(document):

    lines = document.read().split(".")
    text = ""
    for line in lines:
        line = line.replace("\n", " ")
        text += line

    df = pandas.DataFrame(columns = ["text"])
    df.loc[0] = text

    df = clean_text(df)

    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    df['text'] = df['text'].apply(lambda x:' '.join([lemmatizer.lemmatize(word) for word in x.split() if word not in (stop_words)]))
    df['text'][0]
    tf = TfidfVectorizer(max_features=200)
    data = pandas.DataFrame(tf.fit_transform(df['text']).toarray(),columns=tf.get_feature_names_out())
    return data

def clean_text(df):
    df['text']= df['text'].str.replace('\n',' ')
    df['text']= df['text'].str.replace('\r',' ')
    df['text']= df['text'].str.replace('\t',' ')
    df['text'] = df['text'].apply(lambda x: re.sub(r'[0-9]',' ',x))
    df['text'] = df['text'].apply(lambda x: re.sub(r'[/(){}\[\]\|@,;.:-]',' ',x))
    df['text']= df['text'].apply(lambda s:s.lower() if type(s) == str else s)
    df['text']= df['text'].str.replace('  ',' ')
    return df

