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


## DEBUG prints info
DEBUG = True


## input HMM (True) or FAA (False) ?
HMM_OR_FAA = True


## Configuration for E_VALUE
E_VALUE_ENABLE = True
E_VALUE = 20.0


## E_VALUE (True) or SCORE (False) ?
E_VALUE_OR_SCORE = True


## FULL_SEQUENCE (True) or BEST_1_DOMAIN (False) ?
FULL_SEQUENCE_OR_BEST_1_DOMAIN = True

