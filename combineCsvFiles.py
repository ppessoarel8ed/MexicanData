import pandas as pd
import os
#______________________________________
#lists of keywords
rfc=['rfc']
name=['RAZÓN','razon','nombre','Contribuyente']
date=['Publicación DOF presuntos','Publicación página SAT presuntos','date','Publicación página SAT definitivo','fecha']
type_rfc=['PERSONA']
#______________________________________
#encoding types
encodings = ["utf-8","utf-8-sig", "iso-8859-1", "latin1", "cp1252"]
#______________________________________
#methods
def check_and_fit_header(df):
    for column in df.columns.values.tolist():
        for code in rfc:
            if code.strip().lower() in column.strip().lower(): #header is ok
                return df       
    row=-1
    while row<=100 and row<len(df)-1:
        row+=1
        for column in df.loc[row].tolist():
            for code in rfc:
                if code.strip().lower() in str(column).strip().lower(): #found header 
                    df=df.set_axis(df.loc[row].tolist(), axis=1)
                    df=df.loc[row+1:]
                    df.reset_index(drop=True, inplace=True)
                    return df
    return 0 #generate error
##
def get_column_from_partial(df,column): #this function is to get from file how certain column type is called
    for item in column:
        for column_type in df.columns.values.tolist():
            if item.strip().lower() in str(column_type).strip().lower(): #header is ok
                return column_type
            
    return '' #not found 
#______________________________________

#______________________________________
#main code
def combine_csv_files(csv_path):

    csv_files=os.listdir(os.getcwd()+'/'+csv_path)

    df_output=pd.DataFrame(columns=['RFC','Legal Name','Date processed','Person or Company','Source File'])
    for file in csv_files:
        print('start reading file: '+csv_path+'/'+file,end='\r')
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_path+'/'+file,encoding=encoding)
                break
            except Exception as e:  # or the error you receive
                pass
        
        df=check_and_fit_header(df)
        rfc_=get_column_from_partial(df,rfc)
        name_=get_column_from_partial(df,name)
        date_=get_column_from_partial(df,date)
        type_rfc_=get_column_from_partial(df,type_rfc)

        #print(rfc_,' - ',name_,' - ',date_,' - ',type_rfc_)
        #print(df.columns.values.tolist())
        rfc_partial=df[rfc_]
        name_partial=df[name_]

        if date_=='':
            date_partial=['']*len(df)
        else:
            date_partial=df[date_]

        if type_rfc_=='':
            type_rfc_partial=['']*len(df)
        else:
            type_rfc_partial=df[type_rfc_]
        
        source_file_partial=[file]*len(df)

        df_partial=pd.DataFrame({
                    'RFC':rfc_partial,
                    'Legal Name':name_partial,
                    'Date processed':date_partial,
                    'Person (F) or Company (M)': type_rfc_partial,
                    'Source File': source_file_partial
                })
        
        df_output=pd.concat([df_output,df_partial], ignore_index=True)
        print('finished reading file: '+file)

    #df_output=df_output.sort_values('Source File', ascending=False).drop_duplicates(subset=['RFC', 'Legal Name'], keep='last')

    #df_output.to_csv((os.getcwd()+'\\combined_mexican_data.csv'), index=False, encoding='utf-8-sig')
    print('Finished combining all csv files')
    return df_output
