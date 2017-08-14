#!/usr/bin/env python
import os
import re
import csv

def fil():
    
    filetext = os.path.join(os.path.dirname(__file__),'meditech_data','RAW')
    #filetext = "C:/Users/gcampuzanozuluaga/Dropbox/Programming/Python/APPS/meditech_data/MT/RAW"
    outtext_temp = os.path.join(os.path.dirname(__file__),'meditech_data','CLEANEDTEMP')
    outtext = os.path.join(os.path.dirname(__file__),'meditech_data','CLEANED')
    #outtext_temp = "C:/Users/gcampuzanozuluaga/Dropbox/Programming/Python/APPS/meditech_data/CLEANEDTEMP"
    #outtext = "C:/Users/gcampuzanozuluaga/Dropbox/Programming/Python/APPS/meditech_data/CLEANED"
    
    outxml = os.path.join(os.path.dirname(__file__),'meditech_data','MEDITECH_NLS.xml')
    #outxml = "C:/Users/gcampuzanozuluaga/Dropbox/Programming/Python/APPS/meditech_data/MEDITECH_NLS.xml"
    
    outtabdelim = os.path.join(os.path.dirname(__file__),'meditech_data','TAB_DELIM_MEDITECH_NLS.txt')
    #outjson = "C:/Users/gcampuzanozuluaga/Dropbox/Programming/Python/APPS/meditech_data/MT/XML/MEDITECH_NLS.xml"
    #outtabdelim = "C:/Users/gcampuzanozuluaga/Dropbox/Programming/Python/APPS/meditech_data/TAB_DELIM_MEDITECH_NLS.txt"
    
    os.open(outxml, os.O_RDWR | os.O_CREAT)
    with open(outxml, "w+") as out:
        out.write("<UMH_PATHOLOGY>\n")
    for f in os.listdir(filetext):
        path = os.path.join(filetext, f)
        clean_name = f[:-4] + "_CLEAN.TXT"
        clean_path_temp = os.path.join(outtext_temp, clean_name)
        clean_path = os.path.join(outtext, clean_name)
        cleaner(path, clean_path_temp, clean_path)
        mapper(f, clean_path, outxml, outtabdelim)
    with open(outxml, "a+") as out:
        out.write("</UMH_PATHOLOGY>\n")    
   # with open(outxml, "r") as out:
    #    t = out.read()
   # with open(outxml, "w") as out:
        # u = t.encode('latin1','xmlcharrefreplace').decode('utf8','xmlcharrefreplace')
        # u = u.decode("utf-8").replace(u"\u2022", "*").u.encode("utf-8")
        # out.write(u)  

def mapper(filename, text, outxml, outtabdelim):
    # text = "C:/Users/germancz/Dropbox/MEDITECH_NLS_2005.TXT_PROCESSED.txt"
    
    logger = os.path.join(os.path.dirname(__file__),'meditech_data','meditech_case_log.txt')
    #logger = "C:/Users/gcampuzanozuluaga/Dropbox/Programming/Python/APPS/meditech_data/MT/XML/meditech_case_log.txt"
    
    os.open(text, os.O_RDWR)
    with open(text, "r+") as log:
        t = log.read()
    print "mapping"

    ptnameb = re.findall(r"PATIENT:\s*([\w\s]*\w),?(\D*?\w*)?\s+ACCT\s*#:\s*(\S+)?\s*LOC:?.*?U\s*#:\s*(\S+)?\s*\n*"
                         "AGE\/SEX:\s+(\d+)\/(\w{1})\s+DOB:(\d*\/*\d*\/*\d*)\s*?.*?\n*.*?\n*"
                         "Path\s+#:\s+(\d+:\w+:\w+)\s+\w+\s+Received:\s+(\d{2}\/\d{2}\/\d{2})\s*-\s*\d{4}\s+"
                            "Collected:\s*(\S+)\s*\n*(.*?)(\d+\/\d+\/\d+)\s*\d{4}\s*?\n*?.*?\n?(?=PATIENT:)", t, re.S)
    newlistt = []
    count = 0
    print "creating list"
    arr = (ptnameb, newlistt)
    for e in arr[0]:
        #print e
        li = list(e)
        arr[1].append(li)
        count += 1
        print count 
    os.open(logger, os.O_RDWR | os.O_CREAT)
    with open(logger, "a+") as log:
        t = str(filename) + ": \n" + "COUNT: " + str(count) + "\n" 
        log.write(t)
    reducer (newlistt, outxml, outtabdelim)

def reducer(newlistt, outxml, outtabdelim):   
   # outxml = "C:/Users/gcampuzanozuluaga/Dropbox/MT/XML/MEDITECH_NLS.xml"
    tabinit = " "*2 + "<MEDITECH_PATHOLOGY>\n" + " "*4
    tabend = " "*2 + "</MEDITECH_PATHOLOGY>\n"
    with open(outxml, "a+") as out:
        # out.write("<UMH_PATHOLOGY>\n")
        for e in newlistt:
            t = e[7].rfind(":") + 1
            nice_accession = e[7][t:]

            xml = (tabinit
                        + "<FIRST_NAME>" + e[0] + "</FIRST_NAME>\n"
                        + " "*4 + "<LAST_NAME>" + e[1] + "</LAST_NAME>\n"  
                        + " "*4 + "<AGE>" + e[4] + "</AGE>\n" 
                        + " "*4 + "<SEX>" + e[5] + "</SEX>\n" 
                        + " "*4 + "<DOB>" + e[6] + "</DOB>\n"                   
                        + " "*4 + "<ACCOUNT_NUM>" + e[2] + "</ACCOUNT_NUM>\n" 
                        + " "*4 + "<U_NUMBER>" + e[3] + "</U_NUMBER>\n" 
                        + " "*4 + "<ACCESSION_NUMBER_RAW>" + e[7] + "</ACCESSION_NUMBER_RAW>\n"
                        + " "*4 + "<ACCESSION_NUMBER>" + nice_accession + "</ACCESSION_NUMBER>\n"  
                        + " "*4 + "<RECEIVED>" + e[8] + "</RECEIVED>\n" 
                        + " "*4 + "<COLLECTED>" + e[9] + "</COLLECTED>\n" 
                        + " "*4 + "<SIGNOUT_DATE>" + e[11] + "</SIGNOUT_DATE>\n"    
                        + " "*4 + "<TEXT>" + "<![CDATA[\n" + e[10] + "\n]]>" + "</TEXT>\n"
                    + tabend)

            #print xml
            out.write(xml)
            
    os.open(outtabdelim, os.O_RDWR | os.O_CREAT)       
    with open(outtabdelim, 'wb') as csvfile:
        result_writer = csv.writer(csvfile, delimiter = "\t")
    #with open(outtabdelim, "w+") as outtab:
        result_writer.writerow(["FIRST_NAME", " SECOND_NAME", " U_NUMBER", " DOB", " AGE", " SEX", " ACCESSION_NUMBER", " RECEIVED", " SIGNOUT_DATE", " DX"])

        for e in newlistt:
            
            dxtext = str(e[10]).replace("\n"," ")
            dxtext = dxtext.replace("\f"," ")
            dxtext = re.sub(r"\s{2,}"," ", dxtext, re.S)
            dxtext = re.sub(r'^[-+=*\/]{1,}','', dxtext)
            dx = dxtext.lower()
            if "malignant" in dx or "malignancy" in dx or "carcinoma" in dx or "cancer" in dx or "neoplasm" in dx or "sarcoma" in dx or "lymphoma" in dx or "blastoma" in dx:
                t = e[7].rfind(":") + 1
                nice_accession = e[7][t:]
                t = e[7].rfind(":") + 1
                nice_accession = e[7][t:]
                patientstr = [str(e[0]), str(e[1]), str(e[3]), str(e[6]), str(e[4]), str(e[5]), str(e[1]), nice_accession, str(e[8]), str(e[11]), dxtext ]
                result_writer.writerow(patientstr)
                
                #outtab.write(patientstr)
     #   out.write("</UMH_PATHOLOGY>\n")
        # print count
        
def cleaner(filetext, outtext_temp, outtext):
    continuedline = re.compile(r"\n.*\(Continued\)\s*\n", re.MULTILINE)
    disclaimer = re.compile(r"\s*This\sreport\sis\sprivileged,\sconfidential\sand\sexempt\sfrom\sdisclosure\sunder\sapplicable\slaw\.\s*\n"
                            "\s+If\syou\sreceive\sthis\sreport\sinadvertently,\splease\scall\s\(305\)\s325-5587\sand\s*\n"
                            "\s+return\sthe\sreport\sto\sus\sby\smail\.\s*\n", re.MULTILINE) 
    disclaimer_two = re.compile(r"\s*This\sreport\sis\sprivileged,\sconfidential\sand\sexempt\sfrom\sdisclosure\sunder\sapplicable\slaw\.\s*\n"
                            "\s+If\syou\sreceive\sthis\sreport\sinadvertently,\splease\scall\s\(305\)\s325-5587\sand", re.MULTILINE)
    headings = re.compile(r"\s*?RUN\s+DATE:\s+\d{2}\/\d{2}\/\d{2}\s+ADVANCED\s+PATHOLOGY\s+ASSOCIATES\s+PAGE\s+\d+\s*\n"
                          "\s*RUN\s+TIME:\s+\d{4}\s+\*\*\*\sFINAL\sREPORT\s\*\*\*\s*\n+"
                          "\s*SURGICAL\s+PATHOLOGY\s+REPORT\s*\n\s+1400\s+NW\s+12th\s+Avenue,\s+Miami,\s+FL\s+33136\s*\n"
                          "\s+Telephone:\s+305-325-5587\s+FAX:\s+305-325-5899\s*\n", re.MULTILINE)
    lines = re.compile(r"-{5,}", re.MULTILINE)
    doub_space = re.compile(r"\n\n", re.MULTILINE)
    illegalxml = re.compile(u'[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF\u0192]')
    # illegalxml = re.compile(u"[\x00-\x08\x0b\x0c\x0e-\x1F\u0000-\uD800-\uDFFF\u000B\u000C\u000E-\u001F\u007F-\u0084\u0086-\u009F\uD800-\uDFFF"
                       #     "\uFDD0-\uFDFEF\uFFFE\uFFFF\u0192]")
    os.open(filetext, os.O_RDWR)
    with open(filetext, "r+") as log:
        titler = log.read()
        t = continuedline.sub("", titler)
        t = disclaimer.sub("", t)
        t = disclaimer_two.sub("", t)
        t = headings.sub("", t)
     #   t = middle_case.sub(,t)
        t = lines.sub("\n", t)
        t = illegalxml.sub("?", t)
        nline = doub_space.findall(t)
        while len(nline) > 0:
            t = doub_space.sub("\n", t)
            nline = doub_space.findall(t)
            print "newlines"

    os.open(outtext_temp, os.O_RDWR | os.O_CREAT)
    with open(outtext_temp, "w+") as out:
        out.write(t)
    with open(outtext_temp, "a") as endline:
        endline.write("\nPATIENT: XXXX,XXXXX\n")
        
    inbetween(outtext_temp, outtext)

def inbetween(outtext_temp, outtext):
    # text = "C:/Users/gcampuzanozuluaga/Dropbox/MT/CLEANED/MEDITECH_NLS_2011_CLEAN.TXT"
   # outtext = "C:/Users/gcampuzanozuluaga/Dropbox/MT/CLEANED/TESTOUT.TXT"
    
    os.open(outtext_temp, os.O_RDWR)
    with open(outtext_temp, "r+") as log:
        t = log.read()
    prevline = 0
    count = 0 
    splitstuff = t.splitlines()
    linecount = 0
    for line in splitstuff:
       # print line
        if re.match(r"PATIENT:\s*(?:[\w\s]*\w),?(?:\D*?\w*)?\s+ACCT\s*#:\s*(?:\S+)?\s*LOC:?.*?U\s*#:\s*(?:\S+)?\s*", line):
           # print "pte"
            patient_head = line + "\n" + splitstuff[linecount + 1] + "\n" + splitstuff[linecount + 2]
            prevline = linecount + 5
            indicatepte = 1
        if linecount > prevline:
            if len(line) > 0:
                indicatepte = 0
            else:
                pass
        if re.match(r"Path\s+#:\s+(\d+:\w+:\w+)\s+\w+\s+Received:\s+(\d{2}\/\d{2}\/\d{2})\s*-\s*\d{4}\s+Collected:\s*(\S+)\s*", line): 
            count += 1
            if indicatepte == 0:
                line = patient_head + "\n" + line
                splitstuff[linecount] = line
                #print line
        linecount += 1 
    os.open(outtext, os.O_RDWR | os.O_CREAT)
    with open(outtext, "w+") as out:
        for e in splitstuff:
            t = e + "\n"
            out.write(t)   
    print count
fil()      
