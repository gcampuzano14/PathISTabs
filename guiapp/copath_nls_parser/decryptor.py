import re
import rsa
from rsa.bigfile import decrypt_bigfile
import inputgui
from easygui import enterbox

# compile executable: python -O D:\path_to\pyinstaller-2.0\pyinstaller.py --onefile COPATHNLSHACK_DECRYPTOR_v1.PY
# ########additional Input GUI parameters and GUI call#########
title = "COPATH.NLS DECRYPTOR"
msg_fileopenbox = "Choose an encrypted *.txt file\nRemember to grab private-key"
file_type = "*.txt"
file_extension = ".txt"
msg_enterbox = "Enter the name for the folder to save decrypted file\nDefault: ~\COPATHNLS_OUTPUT_"
inputfile, outdir = inputgui.inputstuff(title, msg_fileopenbox, file_type, file_extension, msg_enterbox)

pk = enterbox(msg='Enter Private Key.', title=' ', default='', strip=True, image=None, root=None)
pkelements = pk.split(",")
privkey = rsa.PrivateKey(int(pkelements[0]), int(pkelements[1]), int(pkelements[2]), int(pkelements[3]), int(pkelements[4]))


fileid = re.compile(".*CRYPTO_(.*)\.txt")

outfileex = fileid.match(inputfile)
output = outfileex.group(1)


outputfile = outdir + "/DECRYPTED_" + output + ".txt"

with open(inputfile, 'rb') as infile, open(outputfile, 'wb') as outfile:
    decrypt_bigfile(infile, outfile, privkey)
