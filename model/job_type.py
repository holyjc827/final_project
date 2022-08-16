from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas
import re
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, mean_absolute_error, make_scorer
from nltk.stem import WordNetLemmatizer
from IPython.core.debugger import set_trace

import sys
sys.path.append('util')
import jd_vectorizer

df = pandas.read_csv("./job_posting.csv")
df = df.drop(['job_id', 'location', 'department', 'company_profile', 'salary_range', 'benefits', 'telecommuting', 'has_company_logo', 'has_questions', 'employment_type', 'required_experience', 'required_education', 'industry', 'fraudulent'], axis=1)
df = df.dropna().reset_index(drop=True)

df['text'] = df['title'] + " " + df['description'] + " " + df['requirements']
too_big = df['function'].value_counts()[df['function'].value_counts() > 100].index.tolist()
too_less = df['function'].value_counts()[df['function'].value_counts() < 100].index.tolist()

mask = (df.function == "Writing/Editing") | (df.function == "Advertising") | (df.function ==  "Design") | (df.function == "Marketing") | (df.function == "Art/Creative")
df.loc[mask, 'function'] = 'Creative'

mask = (df.function == "Administrative") | (df.function == "Legal") | (df.function == "Training") | (df.function == "Public Relations") | (df.function == "Human Resources") | (df.function ==  "Customer Service") | (df.function == "Health Care Provider") | (df.function == "Education") | (df.function == "Consulting")
df.loc[mask, 'function'] = 'Service'

mask = (df.function == "Accounting/Auditing") | (df.function == "Financial Analyst")
df.loc[mask, 'function'] = 'Finance'

mask = (df.function == "Engineering") | (df.function == "Science") | (df.function == "Distribution") | (df.function == "Supply Chain") | (df.function == "Research") | (df.function == "Data Analyst") | (df.function == "Manufacturing") | (df.function ==  "Information Technology") | (df.function == "Quality Assurance") | (df.function == "Production")
df.loc[mask, 'function'] = 'Science/Engineering'

mask = (df.function == "Business Development") | (df.function == "Purchasing") | (df.function == "Strategy/Planning") | (df.function == "General Business") | (df.function == "Business Analyst") | (df.function == "Management") | (df.function ==  "Product Management") | (df.function == "Project Management")
df.loc[mask, 'function'] = 'Business'

# for job_type in too_big:
#     df.drop(df.index[df['function']==job_type][100:], inplace=True)

# for job_type in too_less:
#     df.drop(df.index[df['function']==job_type], inplace=True)
df.fillna(" ", inplace = True)
df = df.reset_index()
le = LabelEncoder()
df['job_type'] = le.fit_transform(df['function'])
mapping = dict(zip(le.classes_, range(1, len(le.classes_)+1)))

df = df.drop(['title', 'description', 'function', 'requirements'], axis=1)
df = jd_vectorizer.clean_text(df)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
df['text'] = df['text'].apply(lambda x:' '.join([lemmatizer.lemmatize(word) for word in x.split() if word not in (stop_words)]))
df['text'][0]

tf = TfidfVectorizer(max_features=199)
data = pandas.DataFrame(tf.fit_transform(df['text']).toarray(),columns=tf.get_feature_names_out())
df.drop(['text'],axis=1,inplace=True)
main_df = pandas.concat([df,data],axis=1)


columns = main_df.columns.tolist()
columns = [c for c in columns if c not in ["job_type"]]
target = "job_type"
X = main_df[columns]
Y = main_df['job_type']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

rfc = RandomForestClassifier(n_estimators=200 ,bootstrap=True)
rfc.fit(X_train, Y_train)

rf_pred = rfc.predict(X_test)
f1_score(Y_test, rf_pred.round(), average = 'macro')
print(classification_report(Y_test, rf_pred))

filename = 'rfc_final.pkl'
pickle.dump(rfc, open(filename, 'wb'))
print("Best model is saved.")