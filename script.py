# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import os
import re
import xlsxwriter
import subprocess

workdir = os.getcwd()
print ("El directorio actual es: "+ workdir)
database = raw_input("El directorio por defecto para la base de datos es /home/mike/mike_data/projects/darkhorse/db-05-2018/hd2_informative.dmnd\nSi su directorio es este, presione la tecla intro. En caso contrario, especifique su directorio a continuacion: ")
if database == (""):
    database = ("/home/mike/mike_data/projects/darkhorse/db-05-2018/hd2_informative.dmnd")
directorio_fasta = raw_input("Especifique el directorio donde se encuentra su archivo FASTA, sin incluir el nombre de este: ")
fasta = raw_input("Especifique el nombre de su archivo FASTA: ")
output = fasta.replace(".fasta",".daa")
output_tab = fasta.replace(".fasta",".m8")
dir_dark = raw_input("El directorio por defecto para darkhorse es /home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/bin/darkhorse2.pl\nSi su directorio es este, presione la tecla intro. En caso contrario, especifique el directorio donde tiene instalado darkhorse2.pl")
if dir_dark == (""):
    dir_dark = ("/home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/bin/darkhorse2.pl")
config_file = raw_input("El directorio por defecto para el archivo de configuración es /home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/config\nSi su directorio es este, presiones la tecla intro. En caso contrario, especifique el directorio a continuacion: ")
if config_file == (""):
    config_file = ("/home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/config")
exclude_list = raw_input("El directorio por defecto para la lista de exclusion es /home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/templates/exclude_list_template\nSi su directorio es este, presiones la tecla intro. En caso contrario, especifique el directorio a continuacion: ")
if exclude_list == (""):
    exclude_list = ("/home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/templates/exclude_list_template")

diamond_blast = subprocess.check_call(["diamond","blastp","-d",database,"-q", directorio_fasta+"/"+ fasta,"-a", directorio_fasta + "/" + output,"-e","1e-10","-t",".","--max-target-seqs","200","--more-sensitive"])
diamond_view = subprocess.check_call(["diamond","view","-a",directorio_fasta + "/" + output,"-f","tab","-o",directorio_fasta + "/" + output_tab])
darkhorse = subprocess.check_call(["perl",dir_dark,"-c",config_file,"-t",directorio_fasta + "/" + output_tab,"-e",exclude_list,"-g",directorio_fasta + "/" + fasta])

lista_directorios = (os.listdir("."))

patron = re.compile("calcs.*")
for i in lista_directorios:
    match = patron.search(i)
    if match != (None):
        carpeta = match.group()

lista_archivos = (os.listdir(carpeta))

patron = re.compile(".*smry")
for i in lista_archivos:
    match = patron.search(i)
    if match != (None):
        archivo = match.group()
f = open("./" + carpeta + "/" + archivo, "r")
w = f.read()
elemento = ""
lista = []
for i in w:
    if i == "\t":
        lista.append(elemento)
        elemento = ""
    elif i == "\n":
        lista.append(elemento)
        elemento = ""
    else:
        elemento += i
workbook = xlsxwriter.Workbook("resultados.xlsx")
worksheet = workbook.add_worksheet()
row = 0
col = 0
for i in range(0, len(lista), 17):
    worksheet.write(row,col, lista[i])
    worksheet.write(row,col+1, lista[i+1])
    worksheet.write(row,col+2, lista[i+2])
    worksheet.write(row,col+3, lista[i+3])
    worksheet.write(row,col+4, lista[i+4])
    worksheet.write(row,col+5, lista[i+5])
    worksheet.write(row,col+6, lista[i+6])
    worksheet.write(row,col+7, lista[i+7])
    worksheet.write(row,col+8, lista[i+8])
    worksheet.write(row,col+9, lista[i+9])
    worksheet.write(row,col+10, lista[i+10])
    worksheet.write(row,col+11, lista[i+11])
    worksheet.write(row,col+12, lista[i+12])
    worksheet.write(row,col+13, lista[i+13])
    worksheet.write(row,col+14, lista[i+14])
    worksheet.write(row,col+15, lista[i+15])
    worksheet.write(row,col+15, lista[i+16])
    row += 1
workbook.close()
workbook = os.rename(workdir + "/" + "resultados.xlsx", directorio_fasta + "/" + "resultados.xlsx")
