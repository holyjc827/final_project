from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas
import re
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, mean_absolute_error, make_scorer



df = pandas.read_csv("./job_posting.csv")
df = df.drop(['job_id', 'location', 'department', 'company_profile', 'salary_range', 'benefits', 'telecommuting', 'has_company_logo', 'has_questions', 'employment_type', 'required_experience', 'required_education', 'industry', 'fraudulent'], axis=1)
df = df.dropna().reset_index(drop=True)
le = LabelEncoder()
df['job_type'] = le.fit_transform(df['function'])
mapping = dict(zip(le.classes_, range(1, len(le.classes_)+1)))
df.fillna(" ", inplace = True)
df['text'] = df['title'] + " " + df['description'] + " " + df['requirements']

df = df.drop(['title', 'description', 'function', 'requirements'], axis=1)

df['text']= df['text'].str.replace('\n',' ')
df['text']= df['text'].str.replace('\r',' ')
df['text']= df['text'].str.replace('\t',' ')
df['text'] = df['text'].apply(lambda x: re.sub(r'[0-9]',' ',x))
df['text'] = df['text'].apply(lambda x: re.sub(r'[/(){}\[\]\|@,;.:-]',' ',x))
df['text']= df['text'].apply(lambda s:s.lower() if type(s) == str else s)
df['text']= df['text'].str.replace('  ',' ')

stop_words = set(stopwords.words("english"))
df['text'] = df['text'].apply(lambda x:' '.join([word for word in x.split() if word not in (stop_words)]))
df['text'][0]


tf = TfidfVectorizer(max_features=200)
data = pandas.DataFrame(tf.fit_transform(df['text']).toarray(),columns=tf.get_feature_names_out())
df.drop(['text'],axis=1,inplace=True)
main_df = pandas.concat([df,data],axis=1)


columns = main_df.columns.tolist()
columns = [c for c in columns if c not in ["job_type"]]
target = "job_type"
X = main_df[columns]
Y = main_df['job_type']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

rfc = RandomForestClassifier(n_estimators=200,bootstrap=True)
rfc.fit(X_train, Y_train)

rf_pred = rfc.predict(X_test)
f1_score(Y_test, rf_pred.round(), average = 'macro')
print(classification_report(Y_test, rf_pred))

filename = 'rfc_final.pkl'
pickle.dump(rfc, open(filename, 'wb'))
print("Best model is saved.")