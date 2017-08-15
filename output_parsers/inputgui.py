import os
import re
import datetime
from easygui_labcuro import fileopenbox, diropenbox, enterbox, msgbox


def inputstuff(title, msg_fileopenbox, file_type, file_extension, msg_enterbox):
    now = (str(datetime.datetime.now())[0:4] + str(datetime.datetime.now())[5:7] +
           str(datetime.datetime.now())[8:10] + str(datetime.datetime.now())[11:13] +
           str(datetime.datetime.now())[14:16] + str(datetime.datetime.now())[17:19] +
           str(datetime.datetime.now())[20:len(str(datetime.datetime.now()))-1])
    openfile = fileopenbox(title=title, msg=msg_fileopenbox, filetypes=file_type)
    if openfile[-4:] == file_extension:
        pass
    else:
        msgbox(msg='NO OUTPUT PRODUCED!!\nMAKE SURE YOU USE AN ACCEPTED FILE FORMAT', title=title, ok_button='OK', image=None, root=None)
        raw_input("Press enter to continue")
        quit()
    filepath = os.path.dirname(os.path.abspath(openfile))
    openfile_temp = openfile.replace("\\", "/")
    print(openfile_temp)
    p = re.compile(".*/(.+)\.txt")
    a = p.match(openfile_temp)
    default_name = a.group(1)

    q = re.compile("(.+)/.+\.txt")
    b = q.match(openfile_temp)
    default_dir = b.group(1)

    name_project = enterbox(msg=msg_enterbox, title=title, default=default_name, strip=True, image=None, root=None)
    name_project = name_project.replace("\s", "_")

    savedir = diropenbox(msg="Choose a directory to save output", title="", default=default_dir)

    if len(name_project) > 0:
        print("1")
        savedir = os.path.join(savedir, name_project)
        # savedir = savedir + "/" + name_project
    else:
        savedir = os.path.join(savedir, default_name + "_")
        # savedir = savedir + "/" + default_name + "_"
    out_dir = str(savedir) + "_" + str(now)
    os.mkdir(out_dir,)

    return openfile, out_dir, savedir, filepath
