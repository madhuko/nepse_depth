# %%
import json,glob,os
from datetime import date
# %%
td=date.today().strftime("%Y%m%d")
files_to_merge=glob.glob("./files/{}*".format(td))
with open("./files/m_{}".format(td),'a') as writer:
     for file in files_to_merge:
        with open(file,'r') as filer:
            writer.write(filer.read()+"\n")
        os.remove(file)