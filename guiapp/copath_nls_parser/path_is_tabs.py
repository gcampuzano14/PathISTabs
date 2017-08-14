import open_diff_os
import inputgui
from easygui_copath import choicebox, multchoicebox, buttonbox, msgbox, boolbox
import os
import re
import json
import rsa
from rsa.bigfile import encrypt_bigfile
from datetime import datetime

# compile executable: python -O 7pathto/pyinstaller-2.0\pyinstaller.py --onefile copath_nls_hack_v1.py


def file_read():
    # Input GUI - set vars
    openfile, out_dir, choice_site, choice_spec, encryption = input_gui()
    # clean headers
    outtext_temp = cleaner(openfile)
    # get chunks
    case_list, switch = mapper(outtext_temp, choice_site, choice_spec)
    if switch == 0:
        os.rmdir(out_dir)
        quit()
    else:
        print "2"
        print out_dir
        open_diff_os.openFolder(out_dir)
    fin_data, json_mrn, json_cases = reducer(case_list, choice_site)
    arr = [["JSON_CASES", json_cases], ["JSON_MRN", json_mrn], ["TABDELIM_CASES_OUT", fin_data], ["TEMP_CLEAN", outtext_temp]]

    if encryption == 1:
        crypt_dir = out_dir + "\\CRYPT"
        os.mkdir(crypt_dir)
        crypt_codes = ""

    for e in arr:
        print "22"
        fil = str(e[0]) + ".txt"
        print "33"
        filename = os.path.join(out_dir, fil)
        print "44"
        # filename = out_dir + "/" + e[0] + ".txt"
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
                encrypt_bigfile(infile, outfile, pubkey)

    if encryption == 1:
        filecrypts = crypt_dir + "/CRYPT_KEYS.txt"
        os.open(filecrypts, os.O_RDWR | os.O_CREAT)
        with open(filecrypts, 'wb') as out:
            out.write(str(crypt_codes))


def reducer(case_list, choice_site):

    print "\nMaking datasets...\n"

    nobreakdx = re.compile(r"\n", re.MULTILINE)

    case_dic_access = {}
    case_dic_mrn = {}
    json_structure = []
    case_full = {}
    templist = []

    # JSON access cases dictionary; returns "case_dic_access"
    # JMH structure of e [0.SURG_NUM, 1.ACCESSION_DATE, 2.SIGNOUT_DATE, 3.SEX, 4.AGE, 5.NAME, 6.MRN, 7. DX]
    # UM structure of e [0.SURG_NUM, 1.ACCESSION_DATE, 2.SEX, 3.AGE, 4.NAME, 5.MRN, 6.SIGNOUT_DATE, 7. DX]
    for e in case_list:
        dxtext = e[7]
        dxtext = nobreakdx.sub(" ", dxtext)

        if e[0] in case_dic_access:
            case_fuse = str(case_dic_access[e[0]]["DX"]) + "<<<FUSE>>>" + dxtext
            case_dic_access[e[0]]["DX"] = case_fuse
        else:
            if choice_site == "JMH Copath NLSIIa":
                access_date = datetime.strptime(e[1], '%m/%d/%Y')
                sign_date = datetime.strptime(e[2], '%m/%d/%Y')
                case_dic_access[e[0]] = {"ACCESS_DATE": str(access_date), "SIGN_DATE":  str(sign_date), "SEX": e[3], "AGE": e[4], "NAME": e[5], "MRN":  e[6], "DX": dxtext}
            else:
                access_date = datetime.strptime(e[1], '%m/%d/%Y')
                sign_date = datetime.strptime(e[6], '%m/%d/%Y')
                case_dic_access[e[0]] = {"ACCESS_DATE": str(access_date), "SIGN_DATE":  str(sign_date), "SEX": e[2], "AGE": e[3], "NAME": e[4], "MRN": e[5], "DX": dxtext}

    # JSON mrn dictionary
    for e in case_dic_access:
        case_dict = {"SURG_NUM": e, "ACCESS_DATE": case_dic_access[e]["ACCESS_DATE"], "SIGN_DATE":  case_dic_access[e]["SIGN_DATE"], "SEX": case_dic_access[e]["SEX"], "AGE": case_dic_access[e]["AGE"], "DX": case_dic_access[e]["DX"]}

        if case_dic_access[e]["MRN"] in case_dic_mrn:
            if case_dic_mrn[case_dic_access[e]["MRN"]]["NAMES"] == case_dic_access[e]["NAME"]:
                case_dic_mrn[e["MRN"]]["CASES"].append(case_dict)
            else:
                case_dic_mrn[case_dic_access[e]["MRN"]]["NAMES"].append(case_dic_access[e]["NAME"])
                case_dic_mrn[case_dic_access[e]["MRN"]]["CASES"].append(case_dict)
        else:
            case_dic_mrn[case_dic_access[e]["MRN"]] = {"NAMES": [case_dic_access[e]["NAME"]], "CASES": [case_dict]}

    for e in case_dic_mrn:
        case_full = {"MRN": e, "NAMES": case_dic_mrn[e]["NAMES"], "CASES": case_dic_mrn[e]["CASES"]}
        json_structure.append(case_full)

    count = 0
    for e in json_structure:
        sorted_cases = sorted(e["CASES"], key=lambda a: a["ACCESS_DATE"])
        json_structure[count]["CASES"] = sorted_cases
        count += 1

    json_mrn = json.dumps(json_structure, encoding="latin-1", indent = 2)
    json_cases = json.dumps(case_dic_access, encoding="latin-1", indent = 2)

    # CREATE TAB-DELIMITED DATA
    fin_data = "SURGINAL_NUMBER\tACCESS_DATE\tSIGN_DATE\tSEX\tAGE\tNAME\tMRN\tDIAGNOSIS\n"
    count = 0
    for e in case_dic_access:
        # List of truncated cases
        if len(case_dic_access[e]["DX"]) > int(32759):
            templist.append(str(e))
        t = ''.join([str(e), "\t", str(case_dic_access[e]["ACCESS_DATE"]), "\t", str(case_dic_access[e]["SIGN_DATE"]), "\t", str(case_dic_access[e]["SEX"]), "\t", str(case_dic_access[e]["AGE"]), "\t", str(case_dic_access[e]["NAME"]), "\t", str(case_dic_access[e]["MRN"]), "\t", str(case_dic_access[e]["DX"]), "\t", "=IF(ISERROR(SEARCH(I$1,$H", str(count+2), ",1)),0,1)", "\n"])
        fin_data = ''.join([fin_data, t])

        count += 1

    if len(templist) > 0:
        print "The following cases have > 32759 characters in the DX field, thus, this field will be truncated if opened in MS Excel.\n CASES THAT WILL BE TRUNCATED: " + str(templist)

    if count > 99:
        print "\nTOTAL SPECIMENS PARSED: " + str(len(case_dic_access)) + ". TOTAL PATIENTS: " + str(len(json_structure)) + ', BAM!!\nJSON_MRN.txt file cases/patient are sorted by "ACCESS_DATE"'
    elif count == 0:
        print "\nNO CASES ARE AVAILABLE IN THE OUTPUT. MAKE SURE YOU USE AN ACCEPTED FILE FORMAT"
    else:
        print "\nTOTAL SPECIMENS PARSED: " + str(len(case_dic_access)) + ". TOTAL PATIENTS: " + str(len(json_structure)) + '\nJSON_MRN.txt file cases/patient are sorted by "ACCESS_DATE"'

    return fin_data, json_mrn, json_cases


def mapper(outtext_temp, choice_site, choice_spec):
    case_list = []
    len_types = len(choice_spec)
    count = 1
    full_count = 0
    for e in choice_spec:
        types_left = len_types - count
        if choice_site == "JMH Copath NLSIIa":
            all_cases = re.findall(r"(" + e + "\d{2}-\d+)\s{1}Accession\s{1}Date:\s{1}(\d+/\d+/\d{4})\s{1}\d{2}:\d{2}\s{1}Sign-Out\s{1}Date:\s{1}(\d+/\d+/\d{4})\s{1}\d{2}:\d{2}\s?\n"
            "Gender:\s{1}(.+?)\s{1}Age:\s{1}(.+?)\s?\nPatient:\s{1}(.+?)\s{1}MRN:\s{1}(.*?)\s?\n(.+?)"
            "(?=[A-Z]{1,2}\d{2}-\d+\s{1}Accession\s{1}Date:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s{1}Sign-Out\s{1}Date:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s?\n)", outtext_temp, re.S)
        else:
            all_cases = re.findall(r"(" + e + "\d{2}-\d+)\s{1}Accession\s{1}Date:\s{1}(\d+/\d+/\d{4})\s{1}\d{2}:\d{2}\s?\nGender:\s{1}(.+?)\s{1}Age:\s{1}(.+?)\s?\n"
            "Patient:\s{1}(.+?)\s{1}MRN:\s{1}(.*?)\s?\nSign-Out\s{1}Date:\s{1}(\d+/\d+/\d{4})\s{1}\d{2}:\d{2}\s?\n(.+?)"
            "(?=[A-Z]{1,2}\d{2}-\d+\s{1}Accession\s{1}Date:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s?\n)", outtext_temp, re.S)

        if len(all_cases) == 0 and len(case_list) == 0 and types_left == 0:
            msgbox(msg='NO CASES ARE AVAILABLE IN THE OUTPUT. MAKE SURE YOU USE AN ACCEPTED FILE FORMAT', title='COPATH.NLS', ok_button='OK', image=None, root=None)
            raw_input("Press enter to continue")
            return 0, 0
        count += 1

        # CONVERT TUPLES FROM REGEX TO A LIST OF LISTS
        for a in all_cases:
            li = list(a)
            case_list.append(li)
        case_count = str(len(all_cases))
        print 'NUMBER OF "%s" CASES: '%(str(e)) + str(case_count)
        full_count = full_count + int(case_count)

    # returns a list of list of cases captured with regex all_cases [[SURG_NUM, ACCESSION_DATE, SIGNOUT_DATE, SEX, AGE, NAME, MRN, DX], [...], ...]
    return case_list, 1


def cleaner(filetext):

    dateline = re.compile(r"^Date/Time\s{1}Printed:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s?$\n", re.MULTILINE)
    selecrit = re.compile(r"^Selection\s{1}Criteria:.*?\s?$\n", re.MULTILINE)
    nliis = re.compile(r"^Natural\s{1}Language\s{1}Ila\s{1}Search.*?\s?$\n", re.MULTILINE)
    speclass = re.compile(r"^Specimen\s{1}Class:\s{1}.+\s?$\n", re.MULTILINE)
    textsearch = re.compile(r"^Text\s{1}Search:\s{1}.+\s?$\n", re.MULTILINE)
    accessrange = re.compile(r"^Accession\s{1}Date:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s{1}To\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s?$\n", re.MULTILINE)
    signrange = re.compile(r"^Sign-Out\s{1}Date:\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s{1}To\s{1}\d+/\d+/\d{4}\s{1}\d{2}:\d{2}\s?$\n", re.MULTILINE)
    textprinte = re.compile(r"^Text\s{1}Type\s{1}to\s{1}Print:\s{1}.+\s?$\n", re.MULTILINE)
    agesex = re.compile(r"Age:\s{1}.+?\nGender:\s{1}.+?\s?$\n", re.MULTILINE)
    genderline = re.compile(r"Gender:\s{1}(All\s{1}Values|Male|Female)\s?$\n", re.MULTILINE)
    partype = re.compile(r"^Part\s{1}Type:\s{1}.+\s?$\n", re.MULTILINE)
    pagesubjmh = re.compile(r"^University\s{1}of\s{1}Miami:\s{1}Miller\s{1}School\s{1}of\s{1}Medicine\s{1}Page\s{1}\d+\s{1}of\s{1}\d+", re.MULTILINE)
    pagesubum = re.compile(r"^Jackson\s{1}Memorial\s{1}Hospital\s{1}Page\s{1}\d+\s{1}of\s{1}\d+", re.MULTILINE)
    totspec = re.compile(r"^Total\s{1}Number\s{1}of\s{1}Specimen\(s\):\s{1}\d+", re.MULTILINE)

    regex_collect = [genderline,dateline, selecrit, nliis, speclass, textsearch, accessrange, signrange, textprinte, agesex,  partype, pagesubjmh, pagesubum, totspec]

    with open(filetext, "r+") as fucked:
        titler = fucked.read()
        t = titler
        for e in regex_collect:
            t = e.sub(" ", t)
    t = t + "X11-111 Accession Date: 1/11/1111 11:11 Sign-Out Date: 1/1/1111 11:11\n"

    return t


def input_gui():
    msg = """
    This program will parse text files created from PDF dumps obtained from CoPath Natural Language Search IIa (no race).\n\n
    ________INSTRUCTIONS________\n
    1. When prompted, select a text file (*.txt) containing the dumped NLS\n
    2. Select directory were output will be saved\n
    2. Select the CoPath version (JMH or UM) used to obtain the original PDF\n
    3. Select the case types (letter of accessioning numbers) you want to parse\n
    4. Hold for a bit... results will be out in a few seconds.\n\n
    ___________OUTPUT___________\n
    1. Tab-delimited text file (/TABDELIM_CASES_OUT_(x=time serial).txt)\n
        a. STRUCTURE: SURG_NUM -> ACCESS_DATE -> SIGN_DATE -> SEX -> AGE -> NAME -> MRN -> DIAGNOSIS\n
    2. JSON formated file with SURG_NUMs as keys (/JSON_CASES_(x=time serial).txt)\n
        a.STRUCTURE: {SURG_NUM : [ACCESS_DATE, SIGN_DATE, SEX, AGE, NAME, MRN, DIAGNOSIS],...]],...}\n
    3. JSON formated file with MRNs as keys (/JSON_MRN_(x=time serial).txt)\n
        a.STRUCTURE: {MRN : [NAME, [[SURG_NUM, ACCESS_DATE, SIGN_DATE, SEX, AGE, DIAGNOSIS],...]],...}\n\n
    __________ABOUT_____________\n
    Source: https://github.com/gcampuzano14
    This free and open-source software\n\n
            """
    title = "COPATH.NLS!"
    btnchoices = ["Lets do it!", "Cancel"]
    intro = buttonbox(msg=msg, title=title, choices=btnchoices, image=None)
    if intro == "Lets do it!":
        pass
    else:
        quit()

    # ########additional Input GUI parameters and GUI call#########
    msg_fileopenbox = "Choose a *.txt file"
    file_type = "*.txt"
    file_extension = ".txt"
    msg_enterbox = "Enter the name for the project search\nDefault: ~\COPATHNLS_OUTPUT_"
    openfile, out_dir = inputgui.inputstuff(title, msg_fileopenbox, file_type, file_extension, msg_enterbox)

    msg = "Select the Copath from were the NLIIa extracted"
    sites = ["JMH Copath NLSIIa", "UM Copath NLSIIa"]

    choice_site = choicebox(msg, title, sites)
    if choice_site == "JMH Copath NLSIIa":
        specs = ["S", "US", "T", "C", "H", "M", "F", "A", "SS", "NS"]
    else:
        specs = ["US", "UT", "UB", "M", "UC"]

    msg = "Select all the specimen class letters that apply"
    choice_spec = multchoicebox(msg, title, specs)

    encryption = boolbox(msg='Do you want to encrypt output', title=title, choices=('Yes', 'No'), image=None)

    return openfile, out_dir, choice_site, choice_spec, encryption

file_read()
raw_input("Press enter to continue")
