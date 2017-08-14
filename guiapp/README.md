# PathISTabs
A nifty program that dumps Natural Language Search text/PDF results into spreadsheet tabular format. 


Copath_NLS_Parser
=================

CoPath (Anatomic Pathology Information System) Natural Language Search Parser


Input: 
TXT file from a Copath NLS (no race)

Output:  
1. Tab-delimited text file (/TABDELIM_CASES_OUT_x (x=time serial).txt)
SURG_NUM -> ACCESS_DATE -> SIGN_DATE -> SEX -> AGE -> NAME -> MRN_NUM -> MRN -> DIAGNOSIS
2. JSON formated file with SURG_NUMs as keys (/JSON_CASES_x (x=time serial).txt)
[{SURG_NUM: [ACCESS_DATE, SIGN_DATE, SEX, AGE, NAME, MRN_NUM, MRN, DIAGNOSIS],...]],...}]
3. JSON formated file with MRNs as keys (/JSON_MRN_x (x=time serial).txt)
[{MRN, CASES: [{SURG_NUM, ACCESS_DATE, SIGN_DATE, SEX, AGE, DIAGNOSIS}, {}], NAMES: [NAME1, NAME2,], ALIAS_MRNS: [MRN1, MRN2,] }, {}]



COPATH HACK BUGS: CASES dx WITH LEADING -, + OR = (OPERATORS) CAUSE TRUNCATION WHEN EXPORTED TO EXCEL
Does not pickup Jackso South or Jackson North BMs (SB) - done 07/04/14