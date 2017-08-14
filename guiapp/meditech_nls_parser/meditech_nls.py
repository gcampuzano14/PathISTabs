#!/usr/bin/env python
import csv
import os
import shutil
import re
import json
import rsa
from datetime import datetime
import appmodules.easygui_meditech as easygui_meditech
inputgui = easygui_meditech.inputgui()


def main():
    opendir, out_dir, choice_spec, encryption = input_gui()
    outtext_temp = os.path.join(out_dir, 'CLEANEDTEMP')
    os.mkdir(outtext_temp)
    outtext = os.path.join(out_dir, 'CLEANED')
    os.mkdir(outtext)
    for f in os.listdir(opendir):
        print(f)
        path = os.path.join(opendir, f)
        clean_name = f[:-4] + "_CLEAN.TXT"
        clean_path_temp = os.path.join(outtext_temp, clean_name)
        clean_path = os.path.join(outtext, clean_name)
        cleaner(path, clean_path_temp, clean_path)
    huge_string = ''
    for f in os.listdir(outtext):
        path = os.path.join(outtext, f)
        os.open(path, os.O_RDWR)
        with open(path, "r+") as chunk:
            piece_huge_string = chunk.read()
            piece_huge_string = re.sub(r'\nPATIENT: XXXX,XXXXX\n', '', piece_huge_string)
        huge_string = huge_string + '\n' + piece_huge_string

    huge_string = huge_string + '\nPATIENT: XXXX,XXXXX\n'

    fin_data, json_mrn, json_cases = mapper(huge_string)

    arr = [["JSON_CASES", json_cases], ["JSON_MRN", json_mrn], ["TABDELIM_CASES_OUT", fin_data]]
    if encryption == 1:
        crypt_dir = out_dir + "\\CRYPT"
        os.mkdir(crypt_dir)
        crypt_codes = ""
    for e in arr:
        fil = str(e[0]) + ".txt"
        filename = os.path.join(out_dir, fil)
        print 'filename: ' + filename
        os.open(filename, os.O_RDWR | os.O_CREAT)
        with open(filename, 'wb') as out:
            out.write(str(e[1]))
        if encryption == 1:
            pubkey, privkey = rsa.newkeys(128, poolsize=1)
            print str(e[0]) + " KEYS: " + str(pubkey), str(privkey)
            crypt_codes = str(crypt_codes) + str(e[0]) + " KEYS: " + str(pubkey), str(privkey) + "\n"
            filecrypt = crypt_dir + "/CRYPTO_" + e[0] + ".txt"
            os.open(filecrypt, os.O_RDWR | os.O_CREAT)
            with open(filename, 'rb') as infile, open(filecrypt, 'wb') as outfile:
                rsa.bigfile.encrypt_bigfile(infile, outfile, pubkey)
    if encryption == 1:
        filecrypts = crypt_dir + "/CRYPT_KEYS.txt"
        os.open(filecrypts, os.O_RDWR | os.O_CREAT)
        with open(filecrypts, 'wb') as out:
            out.write(str(crypt_codes))

    # shutil.rmtree(outtext_temp)


def mapper(text):
    ptnameb = re.findall(r"PATIENT:\s*([\w\s]*\w),?(\D*?\w*)?\s+ACCT\s*#:\s*(\S+)?\s*LOC:?.*?U\s*#:\s*(\S+)?\s*\n*"
                         "AGE\/SEX:\s+(\d+)\/(\w{1})\s+DOB:(\d*\/*\d*\/*\d*)\s*?.*?\n*.*?\n*"
                         "Path\s+#:\s+(\d+:\w+:\w+)\s+\w+\s+Received:\s+(\d{2}\/\d{2}\/\d{2})\s*-\s*\d{4}\s+"
                         "Collected:\s*(\S+)\s*\n*(.*?)(\d+\/\d+\/\d+)\s{1,}\d{4}\D{1}\s*?\n*?.*?\n?(?=PATIENT:)", text, re.S)
    newlistt = []
    count = 0
    print "creating list"
    arr = (ptnameb, newlistt)
    for e in arr[0]:
        li = list(e)
        arr[1].append(li)
        count += 1
    fin_data, json_mrn, json_cases = reducer(newlistt)
    return fin_data, json_mrn, json_cases


def reducer(caselist):
    print "\nMaking datasets..."
    # nobreakdx = re.compile(r"\n{1,}", re.S)
    # nospace = re.compile(r"\s{2,}", re.S)
    case_dic_access = {}
    case_dic_mrn = {}
    json_structure = []
    case_full = {}
    templist = []
    # JSON access cases dictionary; returns "case_dic_access"
    # MEDITECH structure of e [3.MRN (U_NUMBER), . SURG_NUM, 8.ACCESSION_DATE, , 5.SEX, 4.AGE, 0.FIRST NAME, 1. LAST NAME,  , 10. DX, 11.SIGNOUT_DATE]
    for case in caselist:
        dxtext = case[10].replace("\n", " ")  # DX
        dxtext = dxtext.replace("\f", " ")
        dxtext = re.sub(r"\s{2,}", " ", dxtext, re.S)
        dxtext = re.sub(r'^[-+=*\/]{1,}', '', dxtext)
        dxtext = re.sub(r'\n', '', dxtext)
        if case[7] in case_dic_access:  # accession number
            case_fuse = str(case_dic_access[case[7]]["DX"]) + "<<<FUSE>>> " + dxtext
            case_dic_access[case[7]]["DX"] = case_fuse
        else:
            access_date = datetime.strptime(case[8], '%m/%d/%y')
            sign_date = datetime.strptime(case[11], '%m/%d/%y')
            case_dic_access[case[7]] = {"ACCESS_DATE": str(access_date), "SIGN_DATE":  str(sign_date), "SEX": case[5], "AGE": case[4],
                                        "NAME": ', '.join([case[0], case[1]]), "MRN":  case[3], "MRN_NUM": case[3], "DX": dxtext}
    # JSON mrn dictionary
    for case in case_dic_access:
        # case_dic_access["MRN_NUM"]
        case_dict = {"SURG_NUM": case, "ACCESS_DATE": case_dic_access[case]["ACCESS_DATE"], "SIGN_DATE":  case_dic_access[case]["SIGN_DATE"],
                     "SEX": case_dic_access[case]["SEX"], "AGE": case_dic_access[case]["AGE"], "DX": case_dic_access[case]["DX"]}
        if case_dic_access[case]["MRN_NUM"] in case_dic_mrn:
            # NAME and MRN match... add case to MRN_NUM
            if (case_dic_access[case]["NAME"] in case_dic_mrn[case_dic_access[case]["MRN_NUM"]]["NAMES"] and
                    case_dic_access[case]["MRN"] in case_dic_mrn[case_dic_access[case]["MRN_NUM"]]["MRNS"]):
                case_dic_mrn[case_dic_access[case]["MRN_NUM"]]["CASES"].append(case_dict)
            # Only NAME matches... append MRN and add case to MRN_NUM
            elif case_dic_access[case]["NAME"] in case_dic_mrn[case_dic_access[case]["MRN_NUM"]]["NAMES"]:
                case_dic_mrn[case_dic_access[case]["MRN_NUM"]]["MRNS"].append(case_dic_access[case]["MRN"])
                case_dic_mrn[case_dic_access[case]["MRN_NUM"]]["CASES"].append(case_dict)
            # Only NAME matches... append MRN and add case to MRN_NUM
            elif case_dic_access[case]["MRN"] in case_dic_mrn[case_dic_access[case]["MRN_NUM"]]["MRNS"]:
                case_dic_mrn[case_dic_access[case]["MRN_NUM"]]["NAMES"].append(case_dic_access[case]["NAME"])
                case_dic_mrn[case_dic_access[case]["MRN_NUM"]]["CASES"].append(case_dict)
        # New MRN to dictionary... add MRN and case
        else:
            case_dic_mrn[case_dic_access[case]["MRN_NUM"]] = {"NAMES": [case_dic_access[case]["NAME"]], "CASES": [case_dict], 'MRNS': [case_dic_access[case]["MRN"]]}
    # Create list of mrn dictionaries to store as JSON; case = MRN_NUM
    for case in case_dic_mrn:
        case_full = {"MRN": case, "NAMES": case_dic_mrn[case]["NAMES"], "CASES": case_dic_mrn[case]["CASES"], "ALIAS_MRNS": case_dic_mrn[case]["MRNS"]}
        json_structure.append(case_full)
    count = 0
    # Sort cases for each MRN by accesion date
    for e in json_structure:
        sorted_cases = sorted(e["CASES"], key=lambda a: a["ACCESS_DATE"])
        json_structure[count]["CASES"] = sorted_cases
        count += 1
    # create JSON mrn and JSON cases
    json_mrn = json.dumps(json_structure, encoding="latin-1", indent=5)
    json_cases = json.dumps(case_dic_access, encoding="latin-1", indent=5)
    # CREATE TAB-DELIMITED DATA
    fin_data = "SURGINAL_NUMBER\tACCESS_DATE\tSIGN_DATE\tSEX\tAGE\tNAME\tMRN_NUM\tMRN\tDIAGNOSIS\n"
    count = 0
    for e in case_dic_access:
        # List of truncated cases
        if len(case_dic_access[e]["DX"]) > int(32759):
            templist.append(str(e))
        line_tabfile = ''.join([str(e), "\t", str(case_dic_access[e]["ACCESS_DATE"]), "\t", str(case_dic_access[e]["SIGN_DATE"]), "\t", str(case_dic_access[e]["SEX"]), "\t",
                                str(case_dic_access[e]["AGE"]), "\t", str(case_dic_access[e]["NAME"]), "\t", str(case_dic_access[e]["MRN_NUM"]), "\t", str(case_dic_access[e]["MRN"]), "\t",
                                str(case_dic_access[e]["DX"]), "\t", "=IF(ISERROR(SEARCH(I$1,$H", str(count+2), ",1)),0,1)", "\n"])
        fin_data = ''.join([fin_data, line_tabfile])
        count += 1
    if len(templist) > 0:
        print "The following cases have > 32759 characters in the DX field, thus, this field will be truncated if opened in MS Excel.\n CASES THAT WILL BE TRUNCATED: " + str(templist)
    if count > 99:
        print("\nTOTAL SPECIMENS PARSED: " + str(len(case_dic_access)) + ". TOTAL PATIENTS: " + str(len(json_structure)) +
               ', BAM!!\nJSON_MRN.txt file cases/patient are sorted by "ACCESS_DATE"')
    elif count == 0:
        print "\nNO CASES ARE AVAILABLE IN THE OUTPUT. MAKE SURE YOU USE AN ACCEPTED FILE FORMAT"
    else:
        print("\nTOTAL SPECIMENS PARSED: " + str(len(case_dic_access)) +  ". TOTAL PATIENTS: " + str(len(json_structure)) +
        '\nJSON_MRN.txt file cases/patient are sorted by "ACCESS_DATE"')
    return fin_data, json_mrn, json_cases


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
    #                        "\uFDD0-\uFDFEF\uFFFE\uFFFF\u0192]")
    os.open(filetext, os.O_RDWR)
    with open(filetext, "r+") as log:
        titler = log.read()
        t = continuedline.sub("", titler)
        t = disclaimer.sub("", t)
        t = disclaimer_two.sub("", t)
        t = headings.sub("", t)
        # t = middle_case.sub(,t)
        t = lines.sub("\n", t)
        t = illegalxml.sub("?", t)
        nline = doub_space.findall(t)
        while len(nline) > 0:
            t = doub_space.sub("\n", t)
            nline = doub_space.findall(t)

    print outtext_temp
    os.open(outtext_temp, os.O_RDWR | os.O_CREAT)
    with open(outtext_temp, "w+") as out:
        out.write(t)
    with open(outtext_temp, "a") as endline:
        endline.write("\nPATIENT: XXXX,XXXXX\n")
    inbetween(outtext_temp, outtext)


def inbetween(outtext_temp, outtext):
    os.open(outtext_temp, os.O_RDWR)
    with open(outtext_temp, "r+") as log:
        t = log.read()
    prevline = 0
    count = 0
    splitstuff = t.splitlines()
    linecount = 0
    for line in splitstuff:
        if re.match(r"PATIENT:\s*(?:[\w\s]*\w),?(?:\D*?\w*)?\s+ACCT\s*#:\s*(?:\S+)?\s*LOC:?.*?U\s*#:\s*(?:\S+)?\s*", line):
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
                # print line
        linecount += 1
    os.open(outtext, os.O_RDWR | os.O_CREAT)
    with open(outtext, "w+") as out:
        for e in splitstuff:
            t = e + "\n"
            out.write(t)
    print count


def input_gui():
    msg = """
    This program will parse text files created from PDF dumps obtained from MEDITECH Natural Language Search.\n\n
    ________INSTRUCTIONS________\n
    1. When prompted, select a text file (*.txt) containing the dumped NLS\n
    2. Select directory were output will be saved\n
    2. Select the MEDITECH version used to obtain the original PDF\n
    3. Select the case types (letter of accessioning numbers) you want to parse\n
    4. Run\n\n
    ___________OUTPUT___________\n
    1. Tab-delimited text file (/TABDELIM_CASES_OUT_x (x=time serial).txt)\n
       SURG_NUM -> ACCESS_DATE -> SIGN_DATE -> SEX -> AGE -> NAME -> MRN_NUM -> MRN -> DIAGNOSIS\n
    2. JSON formated file with SURG_NUMs as keys (/JSON_CASES_x (x=time serial).txt)\n
       [{SURG_NUM: [ACCESS_DATE, SIGN_DATE, SEX, AGE, NAME, MRN_NUM, MRN, DIAGNOSIS],...]],...}]\n
    3. JSON formated file with MRNs as keys (/JSON_MRN_x (x=time serial).txt)\n
       [{MRN, CASES: [{SURG_NUM, ACCESS_DATE, SIGN_DATE, SEX, AGE, DIAGNOSIS}, {}], NAMES: [NAME1, NAME2,], ALIAS_MRNS: [MRN1, MRN2,] }, {}]\n\n
    __________ABOUT_____________\n
    Source: https://github.com/gcampuzano14
    Developed by German Campuzano
    This free and open-source software\n\n
            """
    title = "MEDITECH.NLS"
    btnchoices = ["Run", "Abort"]
    intro = easygui_meditech.buttonbox(msg=msg,
                                       title=title,
                                       choices=btnchoices,
                                       image=None)
    if intro == "Run":
        pass
    else:
        quit()
    # additional Input GUI parameters and GUI call
    msg_fileopenbox = "Choose a *.txt file"
    msg_enterbox = "Enter the name for the project search\nDefault: ~\OUTPUT_"
    # Call inputgui class from easygui_meditech module
    opendir, out_dir, filepath = inputgui.inputstuff(title, msg_fileopenbox, msg_enterbox)
    # Case type selection
    msg = "Select all the specimen class letters that apply"
    specs = ["C", "UM", "A"]
    choice_spec = easygui_meditech.multchoicebox(msg, title, specs)
    encryption = easygui_meditech.boolbox(msg='Do you want to encrypt output',
                                          title=title,
                                          choices=('Yes', 'No'),
                                          image=None)

    return opendir, out_dir, choice_spec, encryption

if __name__ == '__main__':
    main()
