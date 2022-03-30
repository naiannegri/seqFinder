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


import os, fnmatch

PATH_BACTERIA = "../BACTERIA/"
PATH_GENOMES_FAA = "./GENOMES_FAA/"

## SOURCE: https://stackoverflow.com/questions/1724693/find-a-file-in-python
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

## Searching Bacteria
print "#####"
print "## LOOKING FOR BACTERIA FAA.GZ FILES"
print "#####"

BACTERIA = find('*.faa.gz', PATH_BACTERIA)

print "#####"
print "## DONE!"
print "#####"

## Extracting Bacteria

LEN = len(BACTERIA)
K = 0

for BACTERIA_GZ in BACTERIA:
    PWD = BACTERIA_GZ.split("/")
    BACTERIA_TYPE = PWD[PWD.index("BACTERIA")+1]
    K += 1
    print "## Extracting (%d of %d ; %.2f%%): (%s) %s"%(K, LEN, 100.0*K/LEN, BACTERIA_TYPE, BACTERIA_GZ)
    BACTERIA_FAA = BACTERIA_GZ[:-3]
    os.system("gunzip -k -f %s"%BACTERIA_GZ)
    NEW_NAME = BACTERIA_FAA.split("/")
    NEW_NAME = NEW_NAME[:-1] + [BACTERIA_TYPE + "__" + NEW_NAME[-1]]
    NEW_NAME = "/".join(NEW_NAME)
    os.system("mv --update %s %s"%(BACTERIA_FAA, NEW_NAME))
    os.system("mv --update %s %s"%(NEW_NAME, PATH_GENOMES_FAA))
    

