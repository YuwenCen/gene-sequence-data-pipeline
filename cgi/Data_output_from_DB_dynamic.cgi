#! /usr/bin/env python3

import oracledb as cx_Oracle
import cgi


def main():
    contents = processInput()
    print(contents)


def processInput():

    con = cx_Oracle.connect("yuwen/12345@10.0.2.15:1521/xe")
    cur = con.cursor()

    # nucleotides
    nucList = ['A', 'C', 'G', 'T']

    # store results
    fList = [() for i in range(4)]

    for i in range(4):

        myDict = {'nuc': nucList[i]}

        # format string mechanism (%)
        obj = cur.execute(
            '''select gi, freq_%(nuc)s
               from beeGenes,
                    (select max(freq_%(nuc)s) as max_%(nuc)s
                     from beeGenes)
               where freq_%(nuc)s = max_%(nuc)s''' % myDict
        )

        gi_str = ""
        freq_val = None

        for x in obj:
            gi_str += x[0] + "<br>"
            freq_val = x[1]

        gi_str = gi_str.rstrip("<br>")

        fList[i] = (gi_str, freq_val)

    # prepare substitutions for template
    myTuple = ()
    for t in range(4):
        myTuple = myTuple + fList[t]

    cur.close()
    con.close()

    return makePage("see_result_template.html", myTuple)


def fileToStr(fileName):
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents


def makePage(templateFileName, substitutions):
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate % substitutions


try:
    print("Content-type: text/html\n")
    main()
except:
    cgi.print_exception()
