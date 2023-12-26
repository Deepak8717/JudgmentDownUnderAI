import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
from joblib import Parallel, delayed
from tqdm import tqdm

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

raw_data_path = 'C:\\code\\legal_case_classification_model\\data\\raw_data\\legal_text_classification.csv'
processed_data_path = 'C:\\code\\legal_case_classification_model\\data\\processed\\processed_legal_cases.csv'

chunk_size = 1000
num_cores = 4

try:
    raw_data = pd.read_csv(raw_data_path)
except Exception as e:
    print(f"An error occured while reading the raw data: {e}")
    exit(1)



def clean_text(text, stopwords):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in text if word not in stopwords]
    cleaned_text = ' '.join(tokens)
    return cleaned_text

stopwords = stopwords.words('english')
   
def parallelize_cleaning(data):
    try:
        return Parallel(n_jobs=num_cores)(delayed(clean_text)(i, stopwords) for i in data)
    except Exception as e:
        print(f"An error occured during cleaning: {e}")
        return data

processed_data_list = []

for raw_data_chunk in tqdm(pd.read_csv(raw_data_path, chunksize=chunk_size)):
    raw_data_chunk = raw_data_chunk.fillna('')
    try:
        cleaned_title = pd.Series(parallelize_cleaning(raw_data_chunk['case_title']), index=raw_data_chunk.index)
        cleaned_text  = pd.Series(parallelize_cleaning(raw_data_chunk['case_text']), index=raw_data_chunk.index)
        raw_data_chunk['cleaned_title'] = cleaned_title
        raw_data_chunk['cleaned_text'] = cleaned_text
        processed_data_list.append(raw_data_chunk)
    except Exception as e:
        print(f"An error occured during cleaning: {e}")
    
processed_data = pd.concat(processed_data_list)




columns_to_save = ['cleaned_title', 'cleaned_text', 'case_outcome']
processed_data = processed_data[columns_to_save]
unique_outcomes = processed_data['case_outcome'].unique()

try:
    processed_data.to_csv(processed_data_path, index=False)
except Exception as e:
    print(f"An error occured while saving the processed data: {e}")
    

print(raw_data.head())
print(raw_data.describe())
print(raw_data.isnull().sum())
print(raw_data.dtypes)

# ...
