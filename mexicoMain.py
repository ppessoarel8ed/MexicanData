import os
from downloadFiles import download_files
from extractPdfs import extract_data
import pandas as pd
import datetime

#Step1: If pdf and csv folders exist, delete all content in them
#---------------------------------------------------------------------------------------------------------------------
pdf_path='pdf_files'
csv_path='csv_files'
# output_path='treated_files'
# if os.path.exists(pdf_path):
#     for file in os.listdir(pdf_path):
#         os.remove(pdf_path+'/'+file)
# if os.path.exists(csv_path):
#     for file in os.listdir(csv_path):
#         os.remove(csv_path+'/'+file)
# # Creating folders if they dont exist
# if not os.path.exists(pdf_path):
#     os.makedirs(pdf_path)
# if not os.path.exists(csv_path):
#     os.makedirs(csv_path)
# if not os.path.exists(output_path):
#     os.makedirs(output_path)

# #Step2: Downloading files calling function
# #---------------------------------------------------------------------------------------------------------------------
# download_files(pdf_path,csv_path)

#Step3: Extracting data from pdfs using auxiliar function
#---------------------------------------------------------------------------------------------------------------------
extract_data(pdf_path,csv_path)

#Step4: Merging all csv files into one using auxiliar function
#---------------------------------------------------------------------------------------------------------------------
from combineCsvFiles import combine_csv_files
df = combine_csv_files(csv_path)

#Step5: treating df and saving the output
#---------------------------------------------------------------------------------------------------------------------
#sort values using columns RFC and Legal Name
df=df.sort_values(['RFC','Legal Name'], ascending=False)
df=df.drop_duplicates(subset=['RFC', 'Legal Name'], keep='first')
df['Person or Company']=df['Person or Company'].upper()
df['Person or Company']=df['Person or Company'].apply(lambda x: 'Person' if 'F'==x.strip() or 'FISICA' in x or 'F¡sica'.upper() in x else x)
df['Person or Company']=df['Person or Company'].apply(lambda x: 'Company' if 'M'==x.strip() or 'MORAL' in x or 'F¡sica'.upper() in x else x)

today = datetime.date.today()
project_date = today.strftime("%Y-%m-%d")
df.to_csv(output_path+'/combined_mexican_data_'+project_date+'.csv',index=False)
print('Done!')
