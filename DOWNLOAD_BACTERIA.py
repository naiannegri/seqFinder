##########################################
##                                      ##
## FEDERAL UNIVERSITY OF RIO DE JANEIRO ##
##             SAGE / COPPE             ##
##                                      ##
##   GENOME SWEEPER, SEQUENCE FINDER!   ##
##                                      ##
## Authors: Naiane Negri, Jonas Degrave ##
##                                      ##
## Version: 0.1                         ##
## Date: 4 July 2017                    ##
## Description: first version           ##
##                                      ##
## Version: 0.2                         ##
## Date: 1 August 2017                  ##
## Description: accepts config file     ##
##                                      ##
##########################################

## INSTRUCTIONS:
##
## 0a) If needed, run ./../DOWNLOAD_BACTERIA.py to ftp fetch files from NCBI online database.
## 0b) Edit ./../DIR.txt with NCBI ftp path and ./../INDEX.txt with desired bacteria names.
## 0c) Run GET_BACTERIA.py to fetch *.faa.gz GENOMES from ./../BACTERIA/ folders.
##
## 1) Place genomes inside GENOMES_FAA folder;
## 2) Place sequences inside SEQUENCES_FAA or SEQUENCES_HMM folder;
## 3) Edit SEQUENCE_FINDER_CONFIG.py with desired configurations;
## 4) Run RUN_SEQUENCE_FINDER.py and wait;
## 5) Check results folder, import CSV file into an excel/sheets editor;
## 6) Plot nice graphics!


import os

##### Paralel mode, use with caution!
PARALLEL = False

##### Descobrindo o caminho para o banco do NCBI.

try:
	arq = open("DIR.txt", "r")
	DIR = arq.read()
	arq.close()
except:
	print "[ERROR] Could not open DIR.txt to find root ftp directory!"


##### Descobrindo a lista de bacterias desejadas.
try:
	arq = open("INDEX.txt", "r")
	INDEX = arq.read()
	arq.close()
except:
	print "[ERROR] Could not open INDEX.txt to find desired bacteria!"


##### Processando a lista de bacterias.
INDEX = INDEX.split()

LEN = len(INDEX)
K = 0

for BACTERIA in INDEX:
	K += 1
	print "#####"
	print "##### BAIXANDO %d de %d (%.2f%%): %s"%(K, LEN, 100.0*K/LEN, BACTERIA)
	print "#####"

	if PARALLEL == True:
		os.system("rsync --copy-links --recursive --times --verbose rsync://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/%s/ ./BACTERIAS/%s/ &"%(BACTERIA, BACTERIA))
	elif PARALLEL == False:
		os.system("rsync --copy-links --recursive --times --verbose rsync://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/%s/ ./BACTERIAS/%s/"%(BACTERIA, BACTERIA))

