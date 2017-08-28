import os
import shutil
import re
import json
from datetime import datetime
import appmodules.open_diff_os as open_diff_os


def meditech_parse(params):

    openfile = params['openfile']
    out_dir = params['out_dir']
    choice_site = params['choice_site']
    choice_spec = params['choice_spec']

    outtext_temp = os.path.join(out_dir, 'CLEANEDTEMP')
    os.mkdir(outtext_temp)
    outtext = os.path.join(out_dir, 'CLEANED')

    os.mkdir(outtext)

    # clean headers
    outtexttemp = cleaner(openfile)

    # get chunks
    caselist, case_counts = mapper(outtexttemp, choice_spec)

    print(caselist)
    print(case_counts)

    if len(caselist) == 0:
        shutil.rmtree(out_dir)
        parsed_cases_counts = {'specimens': str(0), 'patients': str(0)}
        excel_truncation = str(0)
    else:
        print('\nMAKING OUTPUT DIRECTORY: ' + out_dir)

        open_diff_os.openFolder(out_dir)
    # reduce chunks
        fin_data, json_mrn, json_cases, parsed_cases_counts, excel_truncation = reducer(caselist, choice_site)

        arr = [["JSON_CASES", json_cases], ["JSON_MRN", json_mrn], ["TABDELIM_CASES_OUT", fin_data], ["TEMP_CLEAN", outtexttemp]]
        for e in arr:
            fil = str(e[0]) + ".txt"
            filename = os.path.join(out_dir, fil)
            print('filename: ' + filename)
            os.open(filename, os.O_RDWR | os.O_CREAT)
            with open(filename, 'wb') as out:
                out.write(str(e[1]))

    return case_counts, parsed_cases_counts, excel_truncation


def mapper(text,  choice_spec):
    caselist = []
    lentypes = len(choice_spec)
    count = 1
    case_counts = {}
    for e in choice_spec:
        typesleft = lentypes - count
        allcases = re.findall(r"PATIENT:\s*([\w\s]*\w),?(\D*?\w*)?\s+ACCT\s*#:\s*(\S+)?\s*LOC:?.*?U\s*#:\s*(\S+)?\s*\n*"
                              "AGE\/SEX:\s+(\d+)\/(\w{1})\s+DOB:(\d*\/*\d*\/*\d*)\s*?.*?\n*.*?\n*"
                              "Path\s+#:\s+(\d+:\w+:\w+)\s+\w+\s+Received:\s+(\d{2}\/\d{2}\/\d{2})\s*-\s*\d{4}\s+"
                              "Collected:\s*(\S+)\s*\n*(.*?)(\d+\/\d+\/\d+)\s{1,}\d{4}\D{1}\s*?\n*?.*?\n?(?=PATIENT:)", text, re.S)
        if len(allcases) == 0 and len(caselist) == 0 and typesleft == 0:
            # inputgui.msgbox(msg='NO CASES ARE AVAILABLE IN THE OUTPUT. MAKE SURE YOU USE AN ACCEPTED FILE FORMAT', title='COPATH.NLS.HACK', ok_button='OK', image=None, root=None)
            # raw_input("Press enter to continue")
            case_count = 0
            case_counts[str(e)] = str(case_count)
            return caselist, case_counts
        count += 1
        li = [list(a) for a in allcases]
        caselist = caselist + li
        case_count = str(len(allcases))
        case_counts[str(e)] = str(case_count)
        print('"%s" CASES: '%(str(e)) + str(case_count))

    return caselist, case_counts


def reducer(caselist, choice_site):
    print("\nMaking datasets...")
    # nobreakdx = re.compile(r"\n{1,}", re.S)
    # nospace = re.compile(r"\s{2,}", re.S)
    case_dic_access = {}
    case_dic_mrn = {}
    json_structure = []
    case_full = {}
    templist = []
    parsed_cases_counts = {}
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
                                        "NAME": ','.join([case[0], case[1]]), "MRN":  case[3], "MRN_NUM": case[3], "DX": dxtext}
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
            case_dic_mrn[case_dic_access[case]["MRN_NUM"]] = {"NAMES": [case_dic_access[case]["NAME"]], "CASES": [case_dict], 'MRNS' : [case_dic_access[case]["MRN"]]}
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
        print("The following cases have > 32759 characters in the DX field, thus, this field will be truncated if opened in MS Excel.\n CASES THAT WILL BE TRUNCATED: " + str(templist))
        excel_truncation = str(templist)
    if count > 99:
        print("\nTOTAL SPECIMENS PARSED: " + str(len(case_dic_access)) + ". TOTAL PATIENTS: " + str(len(json_structure)) +
              ', BAM!!\nJSON_MRN.txt file cases/patient are sorted by "ACCESS_DATE"')
        excel_truncation = str(0)
    elif count == 0:
        print("\nNO CASES ARE AVAILABLE IN THE OUTPUT. MAKE SURE YOU USE AN ACCEPTED FILE FORMAT")
        parsed_cases_counts = {'specimens': str(0), 'patients': str(0)}
    else:
        print("\nTOTAL SPECIMENS PARSED: " + str(len(case_dic_access)) + ". TOTAL PATIENTS: " + str(len(json_structure)) +
              '\nJSON_MRN.txt file cases/patient are sorted by "ACCESS_DATE"')
        parsed_cases_counts = {'specimens': str(len(case_dic_access)), 'patients': str(len(json_structure))}

    return fin_data, json_mrn, json_cases, parsed_cases_counts, excel_truncation


def cleaner(filetext):
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
    regex_collect = [continuedline, disclaimer, disclaimer_two,
                     headings, lines, illegalxml]
    with open(filetext, "r+") as effed:
        cleanstr = effed.read()
        for e in regex_collect:
            cleanstr = e.sub(" ", cleanstr)
        nline = doub_space.findall(cleanstr)
        while len(nline) > 0:
            t = doub_space.sub("\n", t)
            nline = doub_space.findall(t)
    cleanstr = " ".join([cleanstr, "\nPATIENT: XXXX,XXXXX\n"])
    # inbetween(outtext_temp, outtext)

    return cleanstr


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
        linecount += 1
    os.open(outtext, os.O_RDWR | os.O_CREAT)
    with open(outtext, "w+") as out:
        for e in splitstuff:
            t = e + "\n"
            out.write(t)
    print(count)
