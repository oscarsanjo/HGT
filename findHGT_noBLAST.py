# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

from Bio import Entrez
from Bio import SeqIO
from Bio import AlignIO
import xlrd
import subprocess
import os
import re
import xlsxwriter
import subprocess
import shutil
import argparse
import time

#Functions
#Get sequences of HGT candidates
def obtain_seq(xlsx):
    sec_hgt = []
    wb = xlrd.open_workbook(xlsx)
    sheet = wb.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        if float(sheet.cell_value(i,5)) < 0.55:
            sec_hgt.append(sheet.cell_value(i,0))
        else:
            break
    return sec_hgt
#Copy sequence of the HGT candidate
def copy_seq(sequence1, file):
    for i in SeqIO.parse(file, "fasta"):
        if i.id == sequence1:
            sequence1 = (re.match("(.*\|.*\|.*)\|", sequence1).group(1))
            sequence1_out = (">" + sequence1 + "\n" + (str(i.seq)))
    return sequence1_out
#Create list with basthits of HGT candidate
def blast_hits(sequenceid, folder):
    sequenceid = re.escape(sequenceid)
    f = open(folder,"r")
    f = f.read()
    ID_list = re.findall(sequenceid +"\t(.*?)\t", f)
    return ID_list
#Create FASTA file with HGT candidate + blasthits sequences
def output_file(sequence3, ID_list, name_file, folder, organism):
    Entrez.email = "oscarsanjo@usal.es"
    Entrez.api_key = "7de6badacc07057ed38b7bc5fe4ea5088009"
    fasta_in_file_temp = open((folder + "/" + "temp.fasta"),"w+")
    name_file = name_file.replace("|","_")
    sequence3 = sequence3.replace("|","_")
    fasta_in_file_temp.write(sequence3)
    ID_list = list(dict.fromkeys(ID_list))
    for i in ID_list:
        done = False
        while not done:
            try:
                handle = Entrez.efetch(db = "protein", id = i, rettype = "gp", retmode = "xml" )
                record = Entrez.read(handle)
                non_self = re.search(organism,record[0]["GBSeq_organism"])
                if non_self == None:
                    fasta_in_file_temp.write(("\n" + ">" + record[0]["GBSeq_organism"] + "_"+ i + "\n" + record[0]["GBSeq_sequence"].upper()))
                handle.close()
                done = True
            except:
                print ("An error has occurred. Trying again...")
                time.sleep(10)
    fasta_in_file_temp = open((folder + "/" + "temp.fasta"),"r")
    text = fasta_in_file_temp.read()
    text_replaced = text.replace(" ","_")
    directory_fasta_in_file = (folder + "/" + "BLASThits" + "/" + "BLASThits_" + name_file + ".fasta")
    fasta_in_file = open((directory_fasta_in_file),"w+")
    fasta_in_file.write(text_replaced)
    fasta_in_file.close()
    fasta_in_file_temp = os.remove(folder + "/" + "temp.fasta")
    return directory_fasta_in_file
#Alignment with mafft
def alignment(input_fasta, folder, query):
    directory = (folder + "/" + "alignments" +  "/" + "alignment_" + query.replace("|","_"))
    output_fasta = open(directory,"w+")
    maff = subprocess.check_call(["mafft", "--quiet", "--auto", input_fasta], stdout = output_fasta)
    return directory
#Conversion of alignment into phylip format
def convert_phylip(input_align, folder, query):
    output_phylip = (folder + "/" + "phylip" + "/" + query.replace("|","_"))
    phylip = AlignIO.convert(input_align, "fasta", output_phylip, "phylip-relaxed")
    return output_phylip
#Build phylogenetic tree
def build_phylo_tree(input_phylip, folder, query):
    folder_tree = (folder + "/" + "trees" + "/" + query.replace("|","_"))
    os.mkdir(folder_tree)
    phyml = subprocess.check_call(["phyml","--quiet", "-i", input_phylip, "-d", "aa", "-b","4","--no_memory_check"])
    shutil.move((input_phylip + "_phyml_boot_stats.txt"), folder_tree)
    shutil.move((input_phylip + "_phyml_boot_trees.txt"), folder_tree)
    shutil.move((input_phylip + "_phyml_stats.txt"), folder_tree)
    shutil.move((input_phylip + "_phyml_tree.txt"), folder_tree)
    return folder_tree

#Help
parser = argparse.ArgumentParser(description ="This program allows you to automatize the search of HGT candidates from a FASTA file")
parser.add_argument("-d", "--database", type=str, metavar = "", default = "/home/mike/mike_data/projects/darkhorse/db-05-2018/hd2_informative.dmnd",help = "DIAMOND database folder. Default directory: /home/mike/mike_data/projects/darkhorse/db-05-2018/hd2_informative.dmnd")
parser.add_argument("-f", "--fasta_directory", type=str,metavar = "", help = "FASTA file directory")
parser.add_argument("-f2", "--fasta_name", type=str,metavar = "", help = "FASTA file name")
parser.add_argument("-o", "--output", type=str,metavar = "", help = "Directory where you want to saver your output")
parser.add_argument("-dh", "--darkhorse", type=str, metavar = "", default = "/home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/bin/darkhorse2.pl",help = "Folder where you have installed Darkhorse. Default directory: /home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/bin/darkhorse2.pl")
parser.add_argument("-c", "--config", type=str, metavar = "", default = "/home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/config", help = "Darkhorse config file directory. Default directory: /home/mike/mike_data/projects/darkhorse/Darkhorse2-DarkHorse-2.0_rev08/config")
parser.add_argument("-e", "--exclude", type=str, metavar = "", default = "/home/oscar/exclude",help = "Darkhorse exclude file directory. Default directory: home/oscar/exclude")
parser.add_argument("-org", "--organism", type=str, metavar = "",help = "Query organism name in NCBI database. This is used to avoid self-matches in alignments")
args= parser.parse_args()
#Type in command line, in this order: database directory, fasta directory, fasta file name, folder where you want to set the outputs, darkhorse folder, config file folder, exclude list folder.
output = (args.fasta_name).replace(".fasta",".daa")
output_tab = (args.fasta_name).replace(".fasta",".m8")
output_data = (args.fasta_name).replace("fasta","")
#DIAMOND BLAST and Darkhorse subprocesses
#diamond_blast = subprocess.check_call(["diamond","blastp","-d",args.database,"-q", args.fasta_directory,"-a", args.output + "/" + output,"-e","1e-10","-t",".","--max-target-seqs","200","--more-sensitive"])
#diamond_view = subprocess.check_call(["diamond","view","-a",args.output + "/" + output,"-f","tab","-o",args.output + "/" + output_tab])
darkhorse = subprocess.Popen(["perl",args.darkhorse,"-c",args.config,"-t",args.output + "/" + output_tab,"-e",args.exclude,"-g",args.fasta_directory])
pid = str(darkhorse.pid)
darkhorse.wait()
#Get directories for saving files
workdir = os.getcwd()
lista_directorios = (os.listdir(workdir))
#Creates the folder raw_data
os.mkdir(args.output + "/" + "raw_data")
#Regular expressions for finding out files that will be saved in raw_data
patron = re.compile("calcs_" + pid + ".*")
patron2 = re.compile(output_data + "filt70.*")
for i in lista_directorios:
    match = patron.match(i)
    match2 = patron2.match(i)
    if match != (None):
        b = match.group(0)
        shutil.move(workdir + "/" + str(b), args.output + "/" + "raw_data")
    elif match2 != (None):
        c = match2.group(0)
        shutil.move(workdir + "/" + str(c), args.output + "/" + "raw_data")
#Creates an .xlsx file
print "Creating .xlsx file..."
f = open(args.output + "/" + "raw_data" + "/" + str(b) + "/" + pid + "_smry", "r")
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
workbook = xlsxwriter.Workbook("results_" + pid + ".xlsx")
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
workbook = shutil.move(workdir + "/" + "results_" + pid + ".xlsx", args.output +"/")
#Creates folders for storing outputs
os.mkdir(args.output + "/" + "outputs")
os.mkdir(args.output + "/" + "outputs" + "/" + "BLASThits")
os.mkdir(args.output + "/" + "outputs" + "/" + "alignments")
os.mkdir(args.output + "/" + "outputs" + "/" + "phylip")
os.mkdir(args.output + "/" + "outputs" + "/" + "trees")
print ("Getting HGT candidates...")
a = obtain_seq(args.output + "/" + "results_" + pid + ".xlsx")
txt_HGT = open(args.output + "/" + "HGT_IDs.txt","w+")
for i in a:
    txt_HGT.write(i + "\n")
txt_HGT.close()
for i in a:
    queue = str((a.index(i) + 1)) + "/" + str(len(a))
    print ("Getting original sequence... " + queue)
    b1 = copy_seq(i, args.fasta_directory)
    print ("Getting BLAST hits from original sequence... " + queue)
    c1 = blast_hits(i, (args.output + "/" + output_tab))
    print ("Generating fasta file... " + queue)
    d1 = output_file(b1,c1,i,(args.output + "/" + "outputs"),args.organism)
    print ("Aligning... " + queue)
    e1 = alignment(d1,(args.output + "/" + "outputs"),i)
    print ("Converting to pyhlip... " + queue)
    f1 = convert_phylip(e1,(args.output + "/" + "outputs"),i)
    print ("Building phylogenetic tree... " + queue)
    g1 = build_phylo_tree(f1,(args.output + "/" + "outputs"),i)
