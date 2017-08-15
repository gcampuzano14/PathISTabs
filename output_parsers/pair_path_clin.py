import csv
import re

clin_list = []
path = "...\MRNs.txt"

data = csv.DictReader(open(path, 'rU'))
path_mrns = []
non_digits = re.compile(r"\D", re.MULTILINE)

for line in data:
    mrn = non_digits.sub("", line["MRN"])
    path_mrns.append(int(mrn))

print(clin_list)
print(path_mrns)

diff = list(set(path_mrns) - set(clin_list))
print(diff)
difft = list(set(diff) - set(path_mrns))

print(len(path_mrns), len(clin_list))

print(difft)
print(len(difft))

newlist = []
for e in clin_list:
    if e in path_mrns:
        newlist.append(e)

print(newlist)
print(len(newlist))
