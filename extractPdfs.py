import pandas as pd
import os
import re
try: #depending on camelot version need to use one format or the other
    import camelot
except:
     import camelot.io as camelot

def extract_data(pdf_path,csv_path):
    #Can use lattice if table has grid, or 'stream' if table is separated by spaces
    pdf_files=os.listdir(os.getcwd()+'/'+pdf_path)

    output_file=pd.DataFrame()
    for file in pdf_files:
        print('start reading file: ',file)
        df = camelot.read_pdf(pdf_path+'/'+file, flavor='lattice', pages='1')
        del output_file
        headers=df[0].df.loc[0]
        if headers[1]=="":
            headers=headers[0].split('\n')
        if headers[0]=='DESCRIPCIÓN': #broken header needs to be fixed when "DESCRIPCIÓN" column is involved
            headers=headers[1:]+[headers[0]]
        output_file=pd.DataFrame(columns=headers)
        page=0
        failedAttempt=0
        while True:
            page+=1
            
            try:
                df = camelot.read_pdf(pdf_path+'/'+file, flavor='lattice', pages=str(page))
                partial_df=df[0].df.loc[1:]
                partial_df=partial_df.set_axis(headers, axis=1)
                output_file=pd.concat([output_file,partial_df], ignore_index=True)
                print('parsing page: '+str(page),end='\r')
            except:
                print('parsing page: '+str(page)+' ----- Failed',end='\r')
                failedAttempt+=1
                if failedAttempt>=10:
                    break

        #fix some broken RFC cells (mixed with index column)
        rfc_index=output_file.columns.values.tolist().index('RFC')
        if(rfc_index<0):
            print('failed getting rfc index, check column name')
            continue
        #need to do 2 checks, one if RFC is empty, other if RFC has some index to it:
        for i in range(len(output_file)): #first check
            if output_file.iloc[i, rfc_index]=='' or pd.isna(output_file.iloc[i, rfc_index]):
                #get content from previuous index
                output_file.iloc[i, rfc_index]=re.sub('(^\d*,\d*)|(^\d*)','',output_file.iloc[i, rfc_index-1].strip()).strip() #remove index that is mixed with RFC

        for i in range(len(output_file)): #second check
            if re.search('(^\d*,\d*)|(^\d*)',output_file.iloc[i, rfc_index])[0]:
                #get content from previuous index
                output_file.iloc[i, rfc_index]=re.sub('(^\d*,\d*)|(^\d*)','',output_file.iloc[i, rfc_index].strip()).strip() #remove index that is mixed with RFC

        #saving file
        output_file.to_csv((csv_path+'/'+file).replace('.pdf','.csv'), index=False, encoding='utf-8-sig')
        
    print('Finished extracting data from pdfs')
    return

