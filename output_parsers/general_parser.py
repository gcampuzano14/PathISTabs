import json
import re
import os
import copathhack_output_parsers
import inputgui
from easygui import choicebox


def main():
    # ########additional Input GUI parameters and GUI call#########
    title = "COPATH.NLS PARSER"
    msg_fileopenbox = "Choose a *.txt file"
    file_type = "*.txt"
    file_extension = ".txt"
    msg_enterbox = "Enter the name for the project search\nDefault: ~\COPATHNLS_OUTPUT_"
    msg ="Select the Copath from were the NLIIa extracted"
    sites = ["JSON_CASES", "JSON_MRN"]
    choice_site = choicebox(msg, title, sites)
    if choice_site == "JSON_CASES":
        type_file = "cases"
    else:
        type_file = "mrn"
    openfile, out_dir = inputgui.inputstuff(title, msg_fileopenbox, file_type, file_extension, msg_enterbox)
    with open(openfile, "r+") as insect:
        total_json = insect.read()
    full_json = json.loads(total_json)
    if type_file == "cases":
        get_cases = copathhack_output_parsers.get_data_cases(full_json)
    else:
        get_cases = copathhack_output_parsers.get_data_cases(full_json)
    get_stuff.get_tabdelimited()
    long_ass_string_allcases = excel_crap(t)
    print(len(t))#tabulator(new_dict)

    arr = [["/JSON_CASES_OUT.txt", t], ["/MRNs.txt", mrns], ["/TABDELIM_CASES_OUT.txt", long_ass_string_allcases]]
    for e in arr:
        outtext = out_dir + str(e[0])
        os.open(outtext, os.O_RDWR | os.O_CREAT)
        with open(outtext, "w+") as out:
            out.write(str(e[1]))