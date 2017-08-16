import os
import re
import json
import rsa
from datetime import datetime
import appmodules.open_diff_os as open_diff_os


def copath_parse(params):

    # Input GUI - set initial vars
    now = "".join([str(datetime.now())[0:4], str(datetime.now())[5:7],
                   str(datetime.now())[8:10], str(datetime.now())[11:13],
                   str(datetime.now())[14:16], str(datetime.now())[17:19],
                   str(datetime.now())[20:len(str(datetime.now()))-1]])

    openfile = params['openfile']
    out_dir = '_'.join([params['out_dir'], now])
    choice_site = params['choice_site']
    choice_spec = params['choice_spec']

    # clean headers
    outtexttemp = cleaner(openfile)

    os.mkdir(out_dir)
    # get chunks
    caselist, case_counts = mapper(outtexttemp, choice_site, choice_spec)
    if len(caselist) == 0:
        os.rmdir(out_dir)
        parsed_cases_counts = {'specimens': str(0), 'patients': str(0)}
        excel_truncation = str(0)
    else:
        print '\nMAKING OUTPUT DIRECTORY: ' + out_dir

        open_diff_os.openFolder(out_dir)
    # reduce chunks
        fin_data, json_mrn, json_cases, parsed_cases_counts, excel_truncation = reducer(caselist, choice_site)

        arr = [["JSON_CASES", json_cases], ["JSON_MRN", json_mrn], ["TABDELIM_CASES_OUT", fin_data], ["TEMP_CLEAN", outtexttemp]]
        for e in arr:
            fil = str(e[0]) + ".txt"
            filename = os.path.join(out_dir, fil)
            print 'filename: ' + filename
            os.open(filename, os.O_RDWR | os.O_CREAT)
            with open(filename, 'wb') as out:
                out.write(str(e[1]))

    return case_counts, parsed_cases_counts, excel_truncation


def reducer(caselist, choice_site):
    print choice_site
    print "\nMaking datasets..."
    case_dic_access = {}
    case_dic_mrn = {}
    json_structure = []
    case_full = {}
    templist = []
    parsed_cases_counts = {}
    # JSON access cases dictionary; returns "case_dic_access"
    # JMH structure of e [0.SURG_NUM, 1.ACCESSION_DATE, 2.SIGNOUT_DATE, 3.SEX, 4.AGE, 5.NAME, 6.MRN, 7. DX]
    # UM structure of e [0.SURG_NUM, 1.ACCESSION_DATE, 2.SEX, 3.AGE, 4.NAME, 5.MRN, 6.SIGNOUT_DATE, 7. DX]
    for case in caselist:
        dxtext = case[7].replace("\n", " ")
        dxtext = dxtext.replace("\f", " ")
        dxtext = re.sub(r"\s{2,}", " ", dxtext, re.S)
        dxtext = re.sub(r'^[-+=*\/]{1,}','', dxtext)
        if case[0] in case_dic_access:
            case_fuse = str(case_dic_access[case[0]]["DX"]) + "<<<FUSE>>> " + dxtext
            case_dic_access[case[0]]["DX"] = case_fuse
        else:
            if choice_site == "JHS":
                # clean MRN non-
                mrn = re.sub(r'\D', "", str(case[6]), re.S)
                mrn = re.sub(r'^[0]{1,}', "", mrn)
                mrn = mrn.replace('-', "")
                access_date = datetime.strptime(case[1], '%m/%d/%Y')
                sign_date = datetime.strptime(case[2], '%m/%d/%Y')
                case_dic_access[case[0]] = {"ACCESS_DATE": str(access_date), "SIGN_DATE":  str(sign_date), "SEX": case[3], "AGE": case[4],
                                            "NAME": case[5], "MRN":  case[6], "MRN_NUM": mrn, "DX": dxtext}
            else:
                mrn = re.sub(r'\D', "", str(case[5]), re.S)
                mrn = re.sub(r'^[0]', "", mrn)
                mrn = mrn.replace('-', "")
                access_date = datetime.strptime(case[1], '%m/%d/%Y')
                sign_date = datetime.strptime(case[6], '%m/%d/%Y')
                case_dic_access[case[0]] = {"ACCESS_DATE": str(access_date), "SIGN_DATE":  str(sign_date), "SEX": case[2], "AGE": case[3],
                                            "NAME": case[4], "MRN": case[5], "MRN_NUM": mrn, "DX": dxtext}
    # JSON mrn dictionary
    for case in case_dic_access:
        # print case
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
                                str(case_dic_access[e]["DX"]), "\t", "=IF(ISERROR(SEARCH(J$1,$I", str(count+2), ",1)),0,1)", "\n"])
        fin_data = ''.join([fin_data, line_tabfile])
        count += 1
    if len(templist) > 0:
        print "The following cases have > 32759 characters in the DX field, thus, this field will be truncated if opened in MS Excel.\n CASES THAT WILL BE TRUNCATED: " + str(templist)
        excel_truncation = str(templist)
    else:
        excel_truncation = str(0)
    if count > 99:
        print("\nTOTAL SPECIMENS PARSED: " + str(len(case_dic_access)) + ". TOTAL PATIENTS: " + str(len(json_structure)) +
              ', BAM!!\nJSON_MRN.txt file cases/patient are sorted by "ACCESS_DATE"')
        parsed_cases_counts = {'specimens': str(len(case_dic_access)), 'patients': str(len(json_structure))}
    elif count == 0:
        print "\nNO CASES ARE AVAILABLE IN THE OUTPUT. MAKE SURE YOU USE AN ACCEPTED FILE FORMAT"
        parsed_cases_counts = {'specimens': str(0), 'patients': str(0)}
    else:
        print("\nTOTAL SPECIMENS PARSED: " + str(len(case_dic_access)) +  ". TOTAL PATIENTS: " + str(len(json_structure)) +
              '\nJSON_MRN.txt file cases/patient are sorted by "ACCESS_DATE"')
        parsed_cases_counts = {'specimens': str(len(case_dic_access)), 'patients': str(len(json_structure))}

    return fin_data, json_mrn, json_cases, parsed_cases_counts, excel_truncation


def mapper(outtext_temp, choice_site, choice_spec):
    print 'NUMBER OF ENTRIES PER CASE TYPE (ACCESSION NUMBER MAY BE REPEATED)'
    caselist = []
    lentypes = len(choice_spec)
    count = 1
    case_counts = {}
    for e in choice_spec:
        typesleft = lentypes - count
        if choice_site == "JHS":
            allcases = re.findall(r"(?<!\S)(" + e + "\d{2}-\d+)\s{1}Accession\s{1}Date:\s{1}(\d+/\d+/\d{4})\s{1}\d{2}:\d{2}\s{1}Sign-Out\s{1}Date:\s{1}(\d+/\d+/\d{4})\s{1}\d{2}:\d{2}\s?\n"
                                  "Gender:\s{1}(.+?)\s{1}Age:\s{1}(.+?)\s?\nPatient:\s{1}(.+?)\s{1}MRN:\s{1}(.*?)\s?\n(.+?)"
                                  "(?=[A-Z]{1,2}\d{2}-\d+\s{1}Accession\s{1}Date:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s{1}Sign-Out\s{1}Date:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s?\n)", outtext_temp, re.S)
        elif choice_site == "UM":
            allcases = re.findall(r"(?<!\S)(" + e + "\d{2}-\d+)\s{1}Accession\s{1}Date:\s{1}(\d+/\d+/\d{4})\s{1}\d{2}:\d{2}\s?\nGender:\s{1}(.+?)\s{1}Age:\s{1}(.+?)\s?\n"
                                  "Patient:\s{1}(.+?)\s{1}MRN:\s{1}(.*?)\s?\nSign-Out\s{1}Date:\s{1}(\d+/\d+/\d{4})\s{1}\d{2}:\d{2}\s?\n(.+?)"
                                  "(?=[A-Z]{1,2}\d{2}-\d+\s{1}Accession\s{1}Date:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s?\n)", outtext_temp, re.S)

        if len(allcases) == 0 and len(caselist) == 0 and typesleft == 0:
            # inputgui.msgbox(msg='NO CASES ARE AVAILABLE IN THE OUTPUT. MAKE SURE YOU USE AN ACCEPTED FILE FORMAT', title='COPATH.NLS', ok_button='OK', image=None, root=None)
            # raw_input("Press enter to continue")
            case_count = 0
            case_counts[str(e)] = str(case_count)
            return caselist, case_counts
        count += 1
        li = [list(a) for a in allcases]
        caselist = caselist + li
        case_count = str(len(allcases))
        case_counts[str(e)] = str(case_count)
        print '"%s" CASES: '%(str(e)) + str(case_count)
    # returns a list of list of cases captured with regex all_cases [[SURG_NUM, ACCESSION_DATE, SIGNOUT_DATE, SEX, AGE, NAME, MRN, DX], [...], ...]
    return caselist, case_counts


def cleaner(filetext):
    dateline = re.compile(r"Date/Time\s{1}Printed:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}", re.MULTILINE)
    selecrit = re.compile(r"Selection\s{1}Criteria:.*?$\n", re.MULTILINE)
    nliis = re.compile(r"Natural\s{1}Language\s{1}Ila\s{1}Search", re.MULTILINE)
    speclass = re.compile(r"Specimen\s{1}Class:.*$\n", re.MULTILINE)
    textsearch = re.compile(r"Text\s{1}Search:\s{1}.+\s?$\n", re.MULTILINE)
    accessrange = re.compile(r"Accession\s{1}Date:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s{1}To\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}", re.MULTILINE)
    signrange = re.compile(r"Sign-Out\s{1}Date:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s{1}To\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}", re.MULTILINE)
    textprinte = re.compile(r"Text\s{1}Type\s{1}to\s{1}Print:\s{1}.+\s?$\n", re.MULTILINE)
    agesex = re.compile(r"Age:\s{1}.+?\nGender:\s{1}.+?\s?$\n", re.MULTILINE)
    genderline = re.compile(r"Gender:\s{1}(All\s{1}Values|Male|Female)\s?$\n", re.MULTILINE)
    partype = re.compile(r"Part\s{1}Type:\s{1}.+\s?$\n", re.MULTILINE)
    pagesubjmh = re.compile(r"University\s{1}of\s{1}Miami:\s{1}Miller\s{1}School\s{1}of\s{1}Medicine\s{1}Page\s{1}\d+\s{1}of\s{1}\d+", re.MULTILINE)
    pagesubum = re.compile(r"Jackson\s{1}Memorial\s{1}Hospital\s{1}Page\s{1}\d+\s{1}of\s{1}\d+", re.MULTILINE)
    totspec = re.compile(r"Total\s{1}Number\s{1}of\s{1}Specimen\(s\):\s{1}\d+", re.MULTILINE)
    regex_collect = [dateline, selecrit, nliis, speclass, textsearch, accessrange, signrange, textprinte, agesex, genderline, partype, pagesubjmh, pagesubum, totspec]
    with open(filetext, "r+") as fucked:
        cleanstr = fucked.read()
        for e in regex_collect:
            cleanstr = e.sub(" ", cleanstr)
    cleanstr = " ".join([cleanstr, "X11-111 Accession Date: 1/11/1111 11:11 Sign-Out Date: 1/1/1111 11:11\n"])

    return cleanstr
