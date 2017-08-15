import re


class get_data_mrn():

    def get_json_cases(json_cases):
        kw = "leukemia"
        kwth = "acute"
        kwnot = "lymphoblastic"
        mrns = "MRN\n"

    def get_json_mrn(json_mrn):
        kw = "leukemia"
        kwth = "acute"
        kwnot = "lymphoblastic"
        mrns = "MRN\n"

        with open(openfile, "r+") as insect:
            total_mrn = insect.read()
        full_mrn = json.loads(total_mrn)

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

    def get_tabdelimited(tabdelimited):
        long_ass_string_allcases = "MRN\tNAME\tCASES\n"
        nobreakdx = re.compile(r"\n", re.MULTILINE)

        for e in t:
            long_ass_string_allcases = long_ass_string_allcases + e["MRN"] + "\t" + e["NAMES"][0]  + "\t"
            for a in e["CASES"]:
                dxtext = a["DX"]
                dxtext = nobreakdx.sub(" ", dxtext)
                long_ass_string_allcases = long_ass_string_allcases + a["SURG_NUM"] + "\t" + a["ACCESS_DATE"] + "\t" + a["SIGN_DATE"] + "\t" + a["SEX"] + "\t" + a["AGE"] + "\t" + dxtext  + "\t"
            long_ass_string_allcases = long_ass_string_allcases + "\n"

        return long_ass_string_allcases


class get_data_cases():

    def get_json_cases(json_cases):
        kw = "leukemia"
        kwth = "acute"
        kwnot = "lymphoblastic"
        mrns = "MRN\n"

    def get_tabdelimited(tabdelimited):
        long_ass_string_allcases = "MRN\tNAME\tCASES\n"
        nobreakdx = re.compile(r"\n", re.MULTILINE)

        for e in t:
            long_ass_string_allcases = long_ass_string_allcases + e["MRN"] + "\t" + e["NAMES"][0]  + "\t"
            for a in e["CASES"]:
                dxtext = a["DX"]
                dxtext = nobreakdx.sub(" ", dxtext)
                long_ass_string_allcases = long_ass_string_allcases + a["SURG_NUM"] + "\t" + a["ACCESS_DATE"] + "\t" + a["SIGN_DATE"] + "\t" + a["SEX"] + "\t" + a["AGE"] + "\t" + dxtext  + "\t"
            long_ass_string_allcases = long_ass_string_allcases + "\n"

        return long_ass_string_allcases
