# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

from sys import argv
import os
import re
import xlsxwriter
import subprocess
#Type in command line, in this order: database directory, fasta directory, fasta file name, folder where you want to set the diamond output, darkhorse folder, config file folder, exclude list folder. If you type default in any query, the defaults folders will be used

workdir = os.getcwd()
if argv[1] == ("default"):
    argv[1] = ("/home/mike/mike_data/projects/darkhorse/db-05-2018/hd2_informative.dmnd")
if argv[5] == ("default"):
    argv[5] = ("/home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/bin/darkhorse2.pl")
if argv[6] == ("default"):
    argv[6] = ("/home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/config")
if argv[7] == ("default"):
    argv[7] = ("/home/oscar/exclude")
    
output = (argv[3]).replace(".fasta",".daa")
output_tab = (argv[3]).replace(".fasta",".m8")

diamond_blast = subprocess.check_call(["diamond","blastp","-d",argv[1],"-q", argv[2],"-a", argv[4] + "/" + output,"-e","1e-10","-t",".","--max-target-seqs","200","--more-sensitive"])
diamond_view = subprocess.check_call(["diamond","view","-a",argv[4] + "/" + output,"-f","tab","-o",argv[4] + "/" + output_tab])
darkhorse = subprocess.check_call(["perl",argv[5],"-c",argv[6],"-t",argv[4] + "/" + output_tab,"-e",argv[7],"-g",argv[2]])

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
workbook = os.rename(workdir + "/" + "resultados.xlsx", argv[4] + "/" + "resultados.xlsx")
