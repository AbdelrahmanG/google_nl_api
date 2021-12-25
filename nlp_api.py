from __future__ import print_function

import streamlit as st
import pandas as pd
import numpy as np
st.title('Google Natural Language API')


#from google.colab import auth
#auth.authenticate_user()
import os
import gspread
#from oauth2client.client import GoogleCredentials

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

user_input = st.text_area("Enter your URLS (one per line)")
import tempfile
uploaded_file = st.file_uploader("Choose your API key", type="json")
try:
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as fp:
        fp.write(uploaded_file.getvalue())

except Exception as e:
  
  st.write("Please upload your API key")
    
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = fp.name
    # Code using GOOGLE_APPLICATION_CREDENTIALS


# If modifying these scopes, delete the file token.json.

#credential_path = "https://storage.googleapis.com/new-bucket-45123/sodp-dowling-49d190142c7b.json"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
########################################
#gc = gspread.authorize(Credentials)

#worksheeturl = gc.open_by_url('https://docs.google.com/spreadsheets/d/1M05QQluxzhkxfA3s0THtuLUBpmF9fG4ybs9AMEWMrpA/')
#worksheet=worksheeturl.worksheet('URLS')
#worksheet_results=worksheeturl.worksheet('Result')
#worksheet_results.clear()
##########################
# get_all_values gives a list of rows.
dff = pd.DataFrame([])
df = pd.DataFrame([])
url_row_df=pd.DataFrame([])
#rows = worksheet.get_all_values()
lines = user_input.split("\n")
rows=lines
#import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
for url_num in np.arange(0, len(rows)):
  try:
      #r1 = requests.get(url)
      try:
          r1 =Request(rows[url_num] , headers={'Accept-Language': 'en-US;q=0.7,en;q=0.3'})
          webpage = urlopen(r1).read()
      except Exception as e:
          r1 =Request(rows[url_num] ,  headers={'User-Agent': 'Mozilla/5.0'})
          webpage = urlopen(r1).read()
          
      #webpage = r1.content
      
      soup1 = BeautifulSoup(webpage, 'html.parser')
      paragraphs = soup1.find_all('p')

      list_paragraphs = []
      title = soup1.find_all('h1')
      title = title[0].get_text();
      for i in np.arange(0, len(paragraphs)):
        paragraph = paragraphs[i].get_text()
        list_paragraphs.append(paragraph)
        body = " ".join(list_paragraphs)

      article = title+". "+ body
      print(article)
      split_article = []
      n  = 9000
      for index in range(0, len(article), n):
        split_article.append(article[index : index + n])

      print(split_article)

      from google.cloud import language_v1

      import os
      #from google.colab import auth
      #auth.authenticate_user()
      #from oauth2client.service_account import ServiceAccountCredentials
      #credential_path = "https://storage.googleapis.com/new-bucket-45123/sodp-dowling-49d190142c7b.json"
      #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
      # Instantiates a client
      client = language_v1.LanguageServiceClient()
      #type_= language_v1.Document.Type.PLAIN_TEXT

      # The text to analyze
      text = u"Google, headquartered in Android phones."
      document = language_v1.Document(
        content=article, type_=language_v1.Document.Type.PLAIN_TEXT
      )

      response = client.analyze_entity_sentiment(
         document=document,
        encoding_type='UTF32',
      )
      entities = response.entities
      # Detects the sentiment of the text
      sentiment = client.analyze_sentiment(
        request={"document": document}
      ).document_sentiment
      correct_types=[]
      for entity in response.entities:
         correct_types.append(entity.type_.name)
      import json
      import pandas as pd

      result_json = response.__class__.to_json(response)
      result_dict = json.loads(result_json)

      del df
      df = pd.json_normalize(result_dict['entities'])

      #url_row = pd.Series([rows[url_num][0]])
      #url_row_df['name'] = pd.DataFrame([url_row])
      my_array = np.array(rows[url_num])
      #url_row_df = pd.DataFrame(my_array, columns = ['name'])
      #st.write(url_row_df)
      #st.dataframe(url_row_df)
      #myheader=list(df.columns)
      #myheader.remove("mentions")
      #top_h = pd.Series(myheader)
      #top_header = pd.DataFrame([myheader], columns=myheader)
      #column_headers = a_dataframe.columns.values.tolist()

      #df = df1.append(df, ignore_index=True, sort=False)

      df = df.drop('mentions', 1)
      df['type'] = correct_types
      st.write(rows[url_num])
      df.fillna('', inplace=True)
      st.write(df)
      #tempDf['type_'] = correct_types
      #df = pd.concat([url_row_df,top_header,df], ignore_index=True,axis=1)
      #st.write(df)
      #df = pd.concat([df,df])
      #df.append(pd.Series(name='site_url'))
      #df.append(pd.Series(name='NewRow'))

  except Exception as e:
    error_mssg=str(e) + ': ' + rows[url_num]
    my_array = np.array([error_mssg])
    df = pd.DataFrame(my_array, columns = ['name'])
    st.write("You cannot extract content from this page: ", rows[url_num] ,e )
  #dff = dff.append(df)
  #dff.fillna('', inplace=True)
#st.write(dff)
#from google.colab import auth
#auth.authenticate_user()
#from oauth2client.client import GoogleCredentials
#import gspread

data=[]
#gco = gspread.authorize(GoogleCredentials.get_application_default())
#worksheeturl = gco.open_by_url('https://docs.google.com/spreadsheets/d/1M05QQluxzhkxfA3s0THtuLUBpmF9fG4ybs9AMEWMrpA/')
#worksheet_results=worksheeturl.worksheet('Result')
result=dff.values.tolist()
#result=dff.T.reset_index().T.values.tolist()
#print(result)
#worksheet_results.update(None,rows[url_num][0])
#worksheet_results.update(None,result)

os.unlink(fp.name)
