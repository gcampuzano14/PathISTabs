import json
import re
import os
import inputgui

# input:
# output:


def main():
    # ########additional Input GUI parameters and GUI call#########
    title = "COPATH.NLS.HACK PARSER"
    msg_fileopenbox = "Choose a *.txt file"
    file_type = "*.txt"
    file_extension = ".txt"
    msg_enterbox = "Enter the name for the project search\nDefault: ~\COPATHNLS_OUTPUT_"
    openfile, out_dir = inputgui.inputstuff(title, msg_fileopenbox, file_type, file_extension, msg_enterbox)
    with open(openfile, "r+") as insect:
        total_mrn = insect.read()
    full_mrn = json.loads(total_mrn)
    patient_list, mrns = parser(full_mrn)
    long_ass_string_allcases = tabdelim_mrn(patient_list)
    print(len(patient_list))  # tabulator(new_dict)
    arr = [["/JSON_CASES_OUT.txt", patient_list], ["/MRNs.txt", mrns], ["/TABDELIM_CASES_OUT.txt", long_ass_string_allcases]]
    for e in arr:
        outtext = out_dir + str(e[0])
        os.open(outtext, os.O_RDWR | os.O_CREAT)
        with open(outtext, "w+") as out:
            out.write(str(e[1]))


def parser(full_mrn):

    kw = "marrow"
    kwth = "marrow"
    kwnot = "lymphoblastic"
    mrns = "MRN\n"
    temp_list = []
    for e in full_mrn:
        for a in e["CASES"]:
            if kwnot in a["DX"]:
                continue
            if kw in a["DX"] and kwth in a["DX"]:
                print(e["MRN"])
                mrns = mrns + e["MRN"] + "\n"
                temp_list.append(e)
                break
    print("done parser")
    return temp_list, mrns


def tabdelim_mrn(t):
    print("doing tab")
    long_ass_string_allcases = "MRN\tNAMEs\tSURGINAL_NUMBER\tACCESS_DATE\tSIGN_DATE\tSEX\tAGE\tDIAGNOSIS\n"
    # nobreakdx = re.compile(r"\n", re.MULTILINE)
    howmany = 1
    for e in t:
        print(str(e["NAMES"][0]) + " " + str(len(t)) + " " + str(howmany))
        # long_ass_string_allcases = long_ass_string_allcases + e["MRN"] + "\t" + e["NAMES"][0]  + "\t"
        long_ass_string_allcases = ''.join([long_ass_string_allcases, e["MRN"], "\t", e["NAMES"][0] , "\t"])
        for a in e["CASES"]:
            # dxtext = a["DX"]
            # dxtext = nobreakdx.sub(" ", dxtext)
            # long_ass_string_allcases = long_ass_string_allcases + a["SURG_NUM"] + "\t" + a["ACCESS_DATE"] + "\t" + a["SIGN_DATE"] + "\t" + a["SEX"] + "\t" + a["AGE"] + "\t" + a["DX"]  + "\t"
            long_ass_string_allcases = ''.join([long_ass_string_allcases, a["SURG_NUM"], "\t", a["ACCESS_DATE"], "\t", a["SIGN_DATE"], "\t" + a["SEX"], "\t", a["AGE"], "\t", a["DX"], "\t"])
        # long_ass_string_allcases = long_ass_string_allcases + "\n"
        long_ass_string_allcases = ''.join([long_ass_string_allcases, "\n"])
        howmany += 1
    return long_ass_string_allcases

main()
