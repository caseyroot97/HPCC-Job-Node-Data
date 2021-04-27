import subprocess
from time import time

# Creates a key that expires in an hour
command = ["ssh -i ~/mykey caroot@login.hpcc.ttu.edu " + "'scontrol token lifespan=3600'" + "'exit'"]
rtn_str = subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
rtn_str_array = rtn_str.splitlines()[-1:]
key = rtn_str_array[0][10:]

f = open("slurm_key.txt", "w")
f.write(str(time())+"\n")
f.write(key)
f.close()