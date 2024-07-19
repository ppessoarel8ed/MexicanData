#This script is responsible for downloading all files relevant for Mexican companies
import requests
import os

def download_files(pdf_path,csv_path):

    #Step1: Creating folders for pdf and csv files
    #---------------------------------------------------------------------------------------------------------------------
    if not os.path.exists(pdf_path):
        os.makedirs(pdf_path)
    if not os.path.exists(csv_path):
        os.makedirs(csv_path)
    #Step2: Downloading pdf files
    #---------------------------------------------------------------------------------------------------------------------
    #source: http://omawww.sat.gob.mx/PadronImportadoresExportadores/Paginas/index.html

    url_pdf=[]
    url_pdf.append('http://omawww.sat.gob.mx/PadronImportadoresExportadores/Paginas/documentos/Pad_Imp.pdf')
    url_pdf.append('http://omawww.sat.gob.mx/PadronImportadoresExportadores/Paginas/documentos/Pad_Imp_Sec.pdf')
    url_pdf.append('http://omawww.sat.gob.mx/PadronImportadoresExportadores/Paginas/documentos/Pad_Exp_Sec.pdf')
    url_pdf.append('http://omawww.sat.gob.mx/PadronImportadoresExportadores/Paginas/documentos/ImportadoresActivos_CanastaBasica.pdf')
    url_pdf.append('http://omawww.sat.gob.mx/PadronImportadoresExportadores/Paginas/documentos/ContribuyentesSuspendidos.pdf')


    chunk_size=2000 #bytes / iteration

    for url in url_pdf:
        print('downloading: ',url)
        r = requests.get(url, stream=True)
        #saving pdfs in pdf_path
        with open(os.getcwd()+'/'+pdf_path+'/'+url.split('/')[-1], 'wb') as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)

    #Step3: Downloading csv files
    #---------------------------------------------------------------------------------------------------------------------
    #second source: -- http://omawww.sat.gob.mx/cifras_sat/Paginas/inicio.html
    #Found 2 relevant links:
    url1="http://omawww.sat.gob.mx/cifras_sat/Paginas/datos/vinculo.html?page=ListCompleta69.html"
    url2="http://omawww.sat.gob.mx/cifras_sat/Paginas/datos/vinculo.html?page=ListCompleta69B.html"

    url_csv=[]
    #links from url1:
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Cancelados.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/ReduccionArt74CFF.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Condonadosart146BCFF.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Condonadosart21CFF.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/CondonadosporDecreto.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Condonados_07_15.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Cancelados_07_15.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Retornoinversiones.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Exigibles.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Firmes.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/No localizados.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Sentencias.csv')
    #links from url2:
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Listado_Completo_69-B.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Definitivos.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Desvirtuados.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/Presuntos.csv')
    url_csv.append('http://omawww.sat.gob.mx/cifras_sat/Documents/SentenciasFavorables.csv')

    for url in url_csv:
        print('downloading: ',url)
        r = requests.get(url, stream=True)
        with open(os.getcwd()+'/'+csv_path+'/'+url.split('/')[-1], 'wb') as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)

    print('Finished downloading all files')
    return

