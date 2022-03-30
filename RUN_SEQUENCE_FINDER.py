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


## Import system modules
import os

## Import config parameters
import SEQUENCE_FINDER_CONFIG

if SEQUENCE_FINDER_CONFIG.DEBUG:
    print "[Info] Debug Mode ON.\n"
    print "[Info] HMM_OR_FAA = %d"%(SEQUENCE_FINDER_CONFIG.HMM_OR_FAA)    
    print "[Info] E_VALUE_ENABLE = %d"%(SEQUENCE_FINDER_CONFIG.E_VALUE_ENABLE)
    print "[Info] E_VALUE = %f"%(SEQUENCE_FINDER_CONFIG.E_VALUE)
    print "[Info] E_VALUE_OR_SCORE = %d"%(SEQUENCE_FINDER_CONFIG.E_VALUE_OR_SCORE)
    print "[Info] FULL_SEQUENCE_OR_BEST_1_DOMAIN = %d\n"%(SEQUENCE_FINDER_CONFIG.FULL_SEQUENCE_OR_BEST_1_DOMAIN)

## Obtain list of sequences and genomes
SEQUENCES = os.listdir("./SEQUENCES_FAA/")
GENOMES = os.listdir("./GENOMES_FAA/")

if SEQUENCE_FINDER_CONFIG.HMM_OR_FAA:
    SEQUENCES_HMM = os.listdir("./SEQUENCES_HMM/")
    SEQUENCES = map(lambda x: x[:-4], SEQUENCES_HMM)
else:
    ## Build sequences
    SEQUENCES_FAA = os.listdir("./SEQUENCES_FAA/")
    SEQUENCES = map(lambda x: x[:-4], SEQUENCES_FAA)
    for SEQUENCE in SEQUENCES:
        print "#####\n## PROCESSING SEQUENCE: %s\n#####\n"%SEQUENCE
        os.system("hmmbuild ./SEQUENCES_HMM/%s.hmm ./SEQUENCES_FAA/%s.faa"%(SEQUENCE, SEQUENCE))

## Search genomes
LEN = len(SEQUENCES) * len(GENOMES)
K = 0
for SEQUENCE in SEQUENCES:
    SEQUENCE_HMM = "./SEQUENCES_HMM/%s.hmm"%(SEQUENCE)

    for GENOME_FAA in GENOMES:
        K += 1
        GENOME = GENOME_FAA[:-4]
        print "## %d de %d (%.2f%%) Finding SEQUENCE %s in GENOME %s\n"%(K, LEN, 100.0*K/LEN, SEQUENCE, GENOME)

        ## Condition for flag -E in hmmsearch
        if SEQUENCE_FINDER_CONFIG.E_VALUE_ENABLE:
            os.system("hmmsearch -E %f %s ./GENOMES_FAA/%s > ./GENOMES_OUT/%s__%s.out"%(SEQUENCE_FINDER_CONFIG.E_VALUE, SEQUENCE_HMM, GENOME_FAA, GENOME, SEQUENCE))
        else:
            os.system("hmmsearch %s ./GENOMES_FAA/%s > ./GENOMES_OUT/%s__%s.out"%(SEQUENCE_HMM, GENOME_FAA, GENOME, SEQUENCE))            

## Parse outputs
OUTPUTS = os.listdir("./GENOMES_OUT/")
RESULTS = []

for OUTPUT in OUTPUTS:
    ARCH = open("./GENOMES_OUT/%s"%OUTPUT, "r")
    COMBINATION = OUTPUT[:-4]

    S = ARCH.read()
    ARCH.close()

    try:
        ## Split lines
        S1 = S.split("\n")

        ## Begin of relevant results
        S2 = S1[15:]

        ## Split whitespaces
        S3 = [i.split() for i in S2 if ("hits" not in i and "inclusion" not in i)]

        ## Fetch result columns until a blank line is found
        ## Decides between E_VALUE or SCORE, between FULL_SEQUENCE or BEST_1_DOMAIN
        if SEQUENCE_FINDER_CONFIG.FULL_SEQUENCE_OR_BEST_1_DOMAIN:
            # Full Sequence
            if SEQUENCE_FINDER_CONFIG.E_VALUE_OR_SCORE:
                S4 = [float(i[0]) for i in S3[:S3.index([])]]
            else:
                S4 = [float(i[1]) for i in S3[:S3.index([])]]
        else:
            # Best 1 Domain
            if SEQUENCE_FINDER_CONFIG.E_VALUE_OR_SCORE:
                S4 = [float(i[3]) for i in S3[:S3.index([])]]
            else:
                S4 = [float(i[4]) for i in S3[:S3.index([])]]

        ## S4 contains E_VALUE/SCORES obtained by this genome for this sequence
        RESULTS += [[COMBINATION, S4]]
    except Exception, e:
        print "ERROR"
        print S2
        print e
        print S
        print len(RESULTS)

## Sorting results (https://wiki.python.org/moin/HowTo/Sorting)
SORTED_RESULTS = sorted(RESULTS, key=lambda result: result[1], reverse=True)

## Writing results
print "\n\n\n\n\n\n"
SPIT_ME_OUT_TXT = open("./RESULTS/SPIT_ME_OUT.txt", "w")
SPIT_ME_OUT_CSV = open("./RESULTS/SPIT_ME_OUT.csv", "w")
for RESULT in SORTED_RESULTS :
    print RESULT
    SPIT_ME_OUT_TXT.write(str(RESULT))
    SPIT_ME_OUT_TXT.write("\n")
    CSV = RESULT[0]+","+",".join([str(score) for score in RESULT[1]])
    # Replace CSV terminated in null values by zero values
    if CSV[-1] == ",": CSV += '0'
    SPIT_ME_OUT_CSV.write(CSV)
    SPIT_ME_OUT_CSV.write("\n")
SPIT_ME_OUT_TXT.close()
SPIT_ME_OUT_CSV.close()

