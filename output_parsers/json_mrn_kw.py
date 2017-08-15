import json
import re
import os
import csv
import inputgui


def main():
    # ########additional Input GUI parameters and GUI call#########
    title = "COPATH.NLS PARSER"
    msg_fileopenbox = "Choose a *.txt file"
    file_type = "*.txt"
    file_extension = ".txt"
    msg_enterbox = "Enter the name for the project search\nDefault: ~\COPATHNLS_OUTPUT_"
    openfile, out_dir, savedir, filepath = inputgui.inputstuff(title, msg_fileopenbox, file_type, file_extension, msg_enterbox)
    output_file = os.path.join(out_dir, "casesout.txt")
    kwlist = ["acute", "leukemia"]
    mrnlist = os.path.join(filepath, "mrns.txt")
    with open(mrnlist, "r+") as mathclist:
        matchlist = mathclist.read().split(",")
    temp_list, remainder = parser(openfile, kwlist, matchlist)
    print "TOTAL CASES: " + str(len(temp_list))  # tabulator(new_dict)
    findstuff(temp_list, output_file, remainder)


def parser(openfile, kwlist, matchlist=None):
    print(kwlist)
    with open(openfile, "r+") as insect:
        total_cases = insect.read()
    fullpatients = json.loads(total_cases)
    patientlist = []
    templist = []
    inlist = []
    if matchlist is not None:
        for ptn in fullpatients:
            cases = ptn["CASES"]
            if ptn['MRN'] in matchlist:
                patientlist.append(ptn)
                inlist.append(ptn['MRN'])
    else:
        patientlist = fullpatients
    for ptn in patientlist:
        cases = ptn["CASES"]
        done = 0
        for case in cases:
            if done == 1:
                break
            else:
                for kw in kwlist:
                    if kw.lower() in case['DX'].lower():
                        templist.append(ptn)
                        print("i will break")
                        done = 1
                        break
    print len(matchlist)
    print len(patientlist)
    remainder = list(set(inlist) - set(matchlist))
    print remainder
    return templist, remainder


def findstuff(templist, output_file, remainder):

    with open(output_file, 'wb') as csvfile:
        result_writer = csv.writer(csvfile)
        headings = ['REAL_MRN', 'NUM_MRN', 'NAMES', 'SEX', 'CASE1_SURGNUM', 'CASE1_ACCESS_DATE', 'CASE1_AGE', 'CASE1_DX', 'CASE1_CELLULARTY', 'CASE1_CELLUL', 'CASE1_FISHPROBE']
        result_writer.writerow(headings)
        for ptn in templist:
            casesptn = []
            fullpatient = []
            for case in ptn['CASES']:
                dxstr = case['DX']
                casesptn = [str(case['SURG_NUM']), str(case['ACCESS_DATE']), str(case['AGE']), str(dxstr)]
                cellularity = re.findall('([^\.!?:;]*CELLULARITY[^\.]*)[\.!?]', dxstr, re.S | re.IGNORECASE)
                cellular = re.findall('([^\.!?:;]*CELLULAR[^\.]*)[\.!?]', dxstr, re.S | re.IGNORECASE)
                fishprobe = re.findall('(nuc\sish[^\.]*?\])', dxstr, re.S)
                # fishresult = re.findall('(nuc\sish[^\.]*?\])',dxstr, re.S)
                arr = [cellularity, cellular, fishprobe]
                for e in arr:
                    casesptn.append(str(e))
                fullpatient = fullpatient + casesptn
            patient = [str(ptn['MRN']), str(ptn['ALIAS_MRNS']), str(ptn["NAMES"]), str(ptn['CASES'][0]['SEX'])] + fullpatient
            result_writer.writerow(patient)
        for e in remainder:
            result_writer.writerow([e])

main()
