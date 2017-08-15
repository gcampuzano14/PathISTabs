import json
import os
import inputgui
from datetime import datetime

# input: JSON file by MRN
# output: JSON file by MRN


def main():
    # ########additional Input GUI parameters and GUI call#########
    title = "COPATH.NLS PARSER"
    msg_fileopenbox = "Choose a *.txt file"
    file_type = "*.txt"
    file_extension = ".txt"
    msg_enterbox = "Enter the name for the project search\nDefault: ~\COPATHNLS_OUTPUT_"
    openfile, out_dir = inputgui.inputstuff(title, msg_fileopenbox, file_type, file_extension, msg_enterbox)

    with open(openfile, "r+") as insect:
        total_mrn = insect.read()
    full_mrn = json.loads(total_mrn)
    t, mrns = parser(full_mrn)
    long_ass_string_allcases = tabdelim_mrn(t)
    print(len(t))#tabulator(new_dict)

    arr = [["/JSON_CASES_OUT.txt", t], ["/MRNs.txt", mrns], ["/TABDELIM_CASES_OUT.txt", long_ass_string_allcases]]
    for e in arr:
        outtext = out_dir + str(e[0])
        os.open(outtext, os.O_RDWR | os.O_CREAT)
        with open(outtext, "w+") as out:
            out.write(str(e[1]))


def parser(full_mrn):

    kw = "leukemia"
    kwth = "acute"
    kwnot = "lymphoblastic"
    mrns = "MRN\n"
    temp_list = []
    for e in full_mrn:
        for a in e["CASES"]:
            if kwnot in a["DX"]:
                continue
            if kw in a["DX"] and kwth in a["DX"]:
                num, new_list = times(e["CASES"])
                if num == 1:
                    e["CASES"] = new_list
                    print(e["MRN"])
                    mrns = mrns + e["MRN"] + "\n"
                    temp_list.append(e)
                    break

    return temp_list, mrns


def times(cases):

    days_tweenbm = 20
    new_list = []
    tally = []
    for a in range(1, len(cases)):
        if a < len(cases):
            if cases[a]["ACCESS_DATE"] == cases[a-1]["ACCESS_DATE"]:
                days_diff = "0"
            else:
                days_count = datetime.strptime(cases[a]["ACCESS_DATE"], '%Y-%m-%d %H:%M:%S') - datetime.strptime(cases[a-1]["ACCESS_DATE"], '%Y-%m-%d %H:%M:%S')
                days_diff = str(days_count).split(" ")[0]
                if int(days_diff) < days_tweenbm and a != 0:
                    if len(tally) == 0:
                        new_list.append(cases[a-1])
                        new_list.append(cases[a])
                        tally.append(a-1)
                        tally.append(a)
                    elif len(tally) == 2 and tally[-1] == a-1:
                        new_list.append(cases[a])
                    else:
                        tally = []
    if len(new_list) == 3:
        num = 1
    else:
        num = 0

    return num, new_list


def tabdelim_mrn(t):
    long_ass_string_allcases = "MRN\tNAMEs\tSURGINAL_NUMBER\tACCESS_DATE\tSIGN_DATE\tSEX\tAGE\tDIAGNOSIS\n"
    # nobreakdx = re.compile(r"\n", re.MULTILINE)

    for e in t:
        long_ass_string_allcases = long_ass_string_allcases + e["MRN"] + "\t" + e["NAMES"][0] + "\t"
        for a in e["CASES"]:
            # dxtext = a["DX"]
            # dxtext = nobreakdx.sub(" ", dxtext)
            long_ass_string_allcases = long_ass_string_allcases + a["SURG_NUM"] + "\t" + a["ACCESS_DATE"] + "\t" + a["SIGN_DATE"] + "\t" + a["SEX"] + "\t" + a["AGE"] + "\t" + a["DX"] + "\t"
        long_ass_string_allcases = long_ass_string_allcases + "\n"

    return long_ass_string_allcases

main()
