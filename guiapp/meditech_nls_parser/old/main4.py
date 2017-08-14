#!/usr/bin/env python
import os
import re
import unicodedata

def map():
    text = "C:/Users/germancz/Dropbox/outtest2012.txt"
    os.open(text, os.O_RDWR)  # check if file exists, else create
    with open(text, "r+") as log:  # title to text log - runonly once
        t = log.read()
    print "mapping"
#    ptnamea = re.findall(r"(E\d+)\s(\D+)\s+(\d+)\/(\D{1})\s+<.+>\s+\((E\d+)\)\s+(.+)\s+(\D+,\D+)(\n)",t,re.S&re.M)   
    ptnameb = re.findall(r"(E\d+)\s(\D+)\s+(\d+)\/(\D{1})\s+<.+?>\s+\((E\d+)\)\s+(.+?)\n+(.+?Final:\s+\D+\S\s+.+?)(?=E\d+\s\D+\s+\d+\/\D{1}\s+<.+?>)", t, re.S)   
    
    newlisto = []
    newlistt = []
    finaldict = {}
    
    print "creating list"
    arr = (ptnameb, newlistt)
#    arr = (ptnamea,newlisto],[ptnameb,newlistt])
 #   for i in arr:
    for e in arr[0]:
      #  print e
        li = list(e)
        arr[1].append(li)

    # print newlistt
    # print len(newlistt)

    for e in newlistt:
        testlen = re.findall(r"Specimen:\s+(\d{2}:\w+:\D+\w+)\s+\w+\s+Received:\s+", e[6], re.S)
        if len(testlen) > 1:
            print "multi: ", e[0]
            templist = []
            temp = re.findall(r"(Specimen:\s+\d{2}:\w+:\D+\w+\s+\w+\s+Received:\s+"
                         "\d{2}\/\d{2}\/\d{2}-\d+\s+Spec\s{1}Type:\s+\w+\s+.+?TISSUES:\s+.+?Final:\s+\D+\S\s+\d{2}\/\d{2}\/\d{2}\s+)", e[6], re.S)
            for o in temp:
                
                newvars = re.findall(r"Specimen:\s+(\d{2}:\w+:\D+\w+)\s+\w+\s+Received:\s+"
                         "(\d{2}\/\d{2}\/\d{2})-\d+\s+Spec\s{1}Type:\s+\w+\s+.+?TISSUES:\s+(.+)Final:\s+(\D+\S[^\W]).+\s+(\d{2}\/\d{2}\/\d{2})\s+", o, re.S)
                for a in newvars:
                    li = list(a)
                    templist.append(li)
                    if e[0] in finaldict:
                        print "appended"
                   #     print "111newstuff: ", e[0]
                        finaldict[e[0]].append([e[0], e[1], e[2], e[3], e[4], e[5], templist[0][0], templist[0][1], templist[0][2], templist[0][3], templist[0][4]])
                   #     print "111newstuff: ", templist[0][0],templist[0][1],templist[0][2],templist[0][3],templist[0][4]
                    else:
                        print "new"
                     #   print "1222newstuff: ", e[0]
                        finaldict[e[0]] = [e[0], e[1], e[2], e[3], e[4], e[5], templist[0][0], templist[0][1], templist[0][2], templist[0][3], templist[0][4]]
                     #   print "1222newstuff: ", templist[0][0],templist[0][1],templist[0][2],templist[0][3],templist[0][4]
        else:
            print "single: ", e[0]
            templist = []
            newvars = re.findall(r"Specimen:\s+(\d{2}:\w+:\D+\w+)\s+\w+\s+Received:\s+"
                         "(\d{2}\/\d{2}\/\d{2})-\d+\s+Spec\s{1}Type:\s+\w+\s+.+?TISSUES:\s+(.+)Final:\s+(\D+\S[^\W]).+\s+(\d{2}\/\d{2}\/\d{2})\s+", e[6], re.S)
            # print newvars
            for a in newvars:
                li = list(a)
                templist.append(li)
            if e[0] in finaldict:
                print "appended"
               # print "2111newstuff: ", e[0]
                finaldict[e[0]].append([e[0], e[1], e[2], e[3], e[4], e[5], templist[0][0], templist[0][1], templist[0][2], templist[0][3], templist[0][4]])
              #  print "2111newstuff: ", templist[0][0],templist[0][1],templist[0][2],templist[0][3],templist[0][4]
            else:
                print "new"
              #  print "2222newstuff: ", e[0],e[1]
             #   print e[6]
                # print templist
                finaldict[e[0]] = [e[0], e[1], e[2], e[3], e[4], e[5], templist[0][0], templist[0][1], templist[0][2], templist[0][3], templist[0][4]]
              #  print "2222newstuff: ", templist[0][0],templist[0][1],templist[0][2],templist[0][3],templist[0][4]
    reduce (finaldict)

def reduce(finaldict):
    illegalxml = re.compile(u'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF\u0192]')   
    outxml = "C:/Users/germancz/Dropbox/out_data_2012.xml"
    tabinit = " "*2 + "<MEDITECH_PATHOLOGY>\n" + " "*4
    tabend = " "*2 + "</MEDITECH_PATHOLOGY>\n"
    os.open(outxml, os.O_RDWR | os.O_CREAT)  # check if file exists, else create
    with open(outxml, "w+") as out:  # title to text log - runonly once
        out.write("<UMH_PATHOLOGY>\n")

        for key in finaldict:
            
            if type(finaldict[key][0]) == str:
                t = finaldict[key][6].rfind(":") + 1
                nice_accession = finaldict[key][6][t:]

                
                xml = (tabinit
                            + "<EVENT_NUMBER>" + finaldict[key][0] + "</EVENT_NUMBER>\n"
                            + " "*4 + "<NAME>" + finaldict[key][1] + "</NAME>\n" 
                            + " "*4 + "<AGE>" + finaldict[key][2] + "</AGE>\n" 
                            + " "*4 + "<SEX>" + finaldict[key][3] + "</SEX>\n" 
                            + " "*4 + "<ALTERNATIVE_EVENT_NUMBER>" + finaldict[key][4] + "</ALTERNATIVE_EVENT_NUMBER>\n" 
                            + " "*4 + "<SITE_CLINICIAN>" + finaldict[key][5] + "</SITE_CLINICIAN>\n" 
                            + " "*4 + "<ACCESSION_NUMBER>" + nice_accession + "</ACCESSION_NUMBER>\n" 
                            + " "*4 + "<ACCESSION_NUMBER_RAW>" + finaldict[key][6] + "</ACCESSION_NUMBER_RAW>\n" 
                            + " "*4 + "<RECEIVED_DATE>" + finaldict[key][7] + "</RECEIVED_DATE>\n" 
                            + " "*4 + "<DIAGNOSIS>" + "<![CDATA[\n" + finaldict[key][8] + "\n]]>" + "</DIAGNOSIS>\n" 
                     #       + " "*4 + "<CLINICAL_HISTORY>" + "<![CDATA[\n" + finaldict[key][9] + "\n]]>" + "</CLINICAL_HISTORY>\n" 
                      #      + " "*4 + "<GROSS_DESCRIPTION>" + "<![CDATA[\n" + finaldict[key][10] + "\n]]>" + "</GROSS_DESCRIPTION>\n"
                       #     + " "*4 + "<FINAL_DIAGNOSIS>" + "<![CDATA[\n" + finaldict[key][11] + "\n]]>" + "</FINAL_DIAGNOSIS>\n"
                            + " "*4 + "<PATHOLOGIST>" + finaldict[key][9] + "</PATHOLOGIST>\n"
                            + " "*4 + "<SIGNED_OUT_DATE>" + finaldict[key][10] + "</SIGNED_OUT_DATE>\n" 
                            + tabend)
                xml = illegalxml.sub("?", xml)
                print xml
                
                
                out.write(xml)

            else:
                for a in finaldict[key]:
                    t = a[6].rfind(":") + 1
                    nice_accession = a[6][t:]

                    xml = (tabinit
                            + "<EVENT_NUMBER>" + a[0] + "</EVENT_NUMBER>\n"
                            + " "*4 + "<NAME>" + a[1] + "</NAME>\n" 
                            + " "*4 + "<AGE>" + a[2] + "</AGE>\n" 
                            + " "*4 + "<SEX>" + a[3] + "</SEX>\n" 
                            + " "*4 + "<ALTERNATIVE_EVENT_NUMBER>" + a[4] + "</ALTERNATIVE_EVENT_NUMBER>\n" 
                            + " "*4 + "<SITE_CLINICIAN>" + a[5] + "</SITE_CLINICIAN>\n" 
                            + " "*4 + "<ACCESSION_NUMBER>" + nice_accession + "</ACCESSION_NUMBER>\n" 
                            + " "*4 + "<ACCESSION_NUMBER_RAW>" + a[6] + "</ACCESSION_NUMBER_RAW>\n" 
                            + " "*4 + "<RECEIVED_DATE>" + a[7] + "</RECEIVED_DATE>\n" 
                            + " "*4 + "<DIAGNOSIS>" + "<![CDATA[\n" + a[8] + "\n]]>" + "</DIAGNOSIS>\n" 
                           # + " "*4 + "<CLINICAL_HISTORY>" + "<![CDATA[\n" + a[9] + "\n]]>" + "</CLINICAL_HISTORY>\n" 
                          #  + " "*4 + "<GROSS_DESCRIPTION>" + "<![CDATA[\n" + a[10] + "\n]]>" + "</GROSS_DESCRIPTION>\n"
                         #   + " "*4 + "<FINAL_DIAGNOSIS>" + "<![CDATA[\n" + a[11] + "\n]]>" + "</FINAL_DIAGNOSIS>\n"
                            + " "*4 + "<PATHOLOGIST>" + a[9] + "</PATHOLOGIST>\n"
                            + " "*4 + "<SIGNED_OUT_DATE>" + a[10] + "</SIGNED_OUT_DATE>\n" 
                            + tabend)
                    xml = illegalxml.sub("?", xml)
                    print xml
                    
                    out.write(xml)
    
        out.write("</UMH_PATHOLOGY>\n")


def cleaner():
    
    filetext = "C:/Users/germancz/Dropbox/test2012.txt"
    outtext = "C:/Users/germancz/Dropbox/outtest2012.txt"
    headings = re.compile(r"-+RUN DATE:.*University\sof\sMiami\sHospital\sLAB\s\*LIVE\*\s+PAGE\s+\d*\s*\n"
                          "RUN TIME:.*Pathology\sSpec#\sRange\sReport.*BATCH.*\nRUN USER:.*\n-+\n\s+"
                          "FOR\sINTERNAL\sUSE\sONLY\.\s+NOT\sPART\sOF\sTHE\sMEDICAL\sRECORD\.\s*\n-{5,}", re.MULTILINE)
    lines = re.compile(r"-{5,}", re.MULTILINE)
    doub_space = re.compile(r"\n\n", re.MULTILINE)

    os.open(filetext, os.O_RDWR)  # check if file exists, else create
    with open(filetext, "r+") as log:  # title to text log - runonly once
        titler = log.read()
        t = headings.sub("", titler)
        t = lines.sub("\n", t)
        nline = doub_space.findall(t)
        while len(nline) > 0:
            t = doub_space.sub("\n", t)
            nline = doub_space.findall(t)
            print "newlines"


    os.open(outtext, os.O_RDWR | os.O_CREAT)  # check if file exists, else create
    with open(outtext, "w+") as out:  # title to text log - runonly once
        out.write(t)
    with open(outtext, "a") as endline:  # title to text log - runonly once
        endline.write("\nE000000 XXXXX,XXXXX 00/X <XXXXXX> (E000000000) XXXXX XXXXX XXXXXX,XXXXX\n")
        
cleaner()
map()
