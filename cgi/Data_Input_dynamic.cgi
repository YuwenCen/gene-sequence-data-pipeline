#! /usr/bin/env python3

import cgi
import oracledb as cx_Oracle

def main():
    form = cgi.FieldStorage()
    fileName = form.getfirst('thelist')
    contents = processInput(fileName)
    print(contents)


def processInput(fileName):

    # Connect to Oracle
    con = cx_Oracle.connect("yuwen/12345@10.0.2.15:1521/xe")
    cur = con.cursor()

    # Drop old table if exists
    try:
        cur.execute("drop table beeGenes")
    except:
        pass

    # Create new table
    cur.execute("""
        create table beeGenes(
            gi varchar2(20),
            sequence clob,
            freq_A number,
            freq_C number,
            freq_G number,
            freq_T number,
            freq_GC number
        )
    """)

    cur.bindarraysize = 50
    cur.setinputsizes(20, 15000, float, float, float, float, float) 
    # max length of gene is 14440

    # Read file into a long string
    infile = open(fileName, "r")
    myStr = ""

    for line in infile:
        line = line.strip()

        # Insert marker when a new gene entry starts
        if ">gi" in line:
            line += "_**gene_seq_starts_here**_"

        myStr += line

    infile.close()

    # Split by gi entries
    entries = myStr.split(">gi|")

    gi_list = []
    seq_list = []
    fA_list = []
    fC_list = []
    fG_list = []
    fT_list = []
    fGC_list = []

    # Process each entry 
    for item in entries: 
        if item.strip() == "": # used to skip empty strings eg. beginning 
            continue

        # Get gi number
        gi_end = item.find("|")
        gi = item[:gi_end]

        # Find marker
        pos = item.find("_**gene_seq_starts_here**_")
        if pos == -1: # Prevent error if we didn't find one 
            continue

        # Sequence starts after marker
        seq = item[pos + len("_**gene_seq_starts_here**_") : ]

        # Keep only A,C,G,T, eg. there's a 'w' in the first sequence 
        seq = "".join([c for c in seq if c in "ACGT"])
        if seq == "":
            continue

        L = float(len(seq))
        freqA = seq.count("A") / L
        freqC = seq.count("C") / L
        freqG = seq.count("G") / L
        freqT = seq.count("T") / L
        freqGC = freqG + freqC

        gi_list.append(gi)
        seq_list.append(seq)
        fA_list.append(freqA)
        fC_list.append(freqC)
        fG_list.append(freqG)
        fT_list.append(freqT)
        fGC_list.append(freqGC)

    cur.executemany("""
        insert into beeGenes
        values (:1,:2,:3,:4,:5,:6,:7)
    """, list(zip(gi_list, seq_list, fA_list, fC_list, fG_list, fT_list, fGC_list)))

    con.commit()
    cur.close()
    con.close()

    return makePage("done_submission_template.html",
                    "Your data have been successfully submitted and processed.")


def fileToStr(fileName):
    fin = open(fileName, "r")
    contents = fin.read()
    fin.close()
    return contents


def makePage(templateFileName, substitution):
    template = fileToStr(templateFileName)
    return template % substitution

try:
    print("Content-type: text/html\n\n")
    main()
except:
    cgi.print_exception()
