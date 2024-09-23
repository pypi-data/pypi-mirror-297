import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

def main():
  #Loading the documents
  documents = open("documents.txt")
  content = documents.readlines()
  print(content[:5])

  #Grouping them into paragraphs
  paragraphs = []
  temp = ""
  for i in content:
    if i=='\n':
      paragraphs.append(temp)
      temp = ""
    else:
      temp += i

  paragraphs[:2]

  #Basic Text Preprocessing 1. Remove Special Characters 2. Lowercasing
  def preprocess(text):
    text = re.sub('[^A-Za-z0-9]+   ', '', text)
    text = text.lower()
    text = text.replace("\n"," ")
    text = text.replace("\ufeff","")
    return text

  preprocessed_paragraphs = []
  for i in paragraphs:
    preprocessed_paragraphs.append(preprocess(i))

  preprocessed_paragraphs[:2]

  """## Inverted Index"""

  #Loading the keywords
  keywords = open("keywords.txt")
  keywords = keywords.readlines()
  keywords = [i.replace("\n","") for i in keywords]
  keywords[:3]

  #Inverted Index: {keyword:[list of documents containing keyword]}
  inverted_index = {}
  for keyword in keywords:
    inverted_index[keyword] = []

  for keyword in keywords:
    for i_doc in range(len(preprocessed_paragraphs)):
      if keyword in preprocessed_paragraphs[i_doc]:
        inverted_index[keyword].append(i_doc)

  print(inverted_index)

  """## Boolean Queries"""

  #Converting preprocessed paragraphs into binary bag of words
  vectorizer = CountVectorizer()
  binary_bog = vectorizer.fit_transform(preprocessed_paragraphs)
  binary_bog_values  = binary_bog.toarray()
  features_bog = list(vectorizer.get_feature_names_out())

  df_bog  = pd.DataFrame(binary_bog_values,columns=features_bog)
  df_bog.head(2)

  #Binary Query using And Or
  query = "reasoning AND home OR group"
  words = query.split()
  res_df = None
  character = 0
  while character < len(words):

    if words[character]=="OR":
      res_df = res_df | df_bog[words[character+1]]
      character += 2
    elif words[character]=="AND":
      res_df = res_df & df_bog[words[character+1]]
      character += 2
    else:
      res_df = df_bog[words[character]]
      character += 1

  res_df = list(res_df)

  #List of documents satisfying the given query
  documents_index = []
  for i in range(len(res_df)):
    if res_df[i]>0:
      documents_index.append(i)
    else:
      continue
  print("Satisfied Results Document Index:",documents_index)
  print("Query:",query)
  print("Results:")
  for i in range(len(documents_index[:5])):
    print("TOP ",i+1,":",paragraphs[documents_index[i]])

  """## Ranked Queries
  Test queries using standard TF/IDF weighting and cosine similarity.
  The search method receives a query and returns a ranked list of documents from the index.
  Each document has a similarity score that quantifies the similarity between the document and
  the query. The searcher method explain also allows you understand numerical calculation of the
  similarity between a query and a document.
  """

  def cosine_distance(v1,v2):
    return np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

  def retriever(content,query,top_k):
    result = {}
    for i in range(len(content)):
      result[i] = cosine_distance(content[i],query)

    result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1],reverse=True)}
    return list(result.keys())[:top_k]

  vectorizer = TfidfVectorizer()
  tfidf_para = vectorizer.fit_transform(preprocessed_paragraphs).toarray()

  query = ["international machine learning conference".lower()]
  tfidf_query = list(vectorizer.transform(query).toarray()[0])
  top_k = 5

  results = retriever(tfidf_para,tfidf_query,top_k)
  results

  for i in range(len(results)):
    print("TOP ",i+1,":",paragraphs[results[i]])

