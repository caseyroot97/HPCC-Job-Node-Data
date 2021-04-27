import os
import sys
import json
import time
import requests
import refresh_key
from process_data import add_jobs_to_nodes

def get_key() -> str:
    f = open("slurm_key.txt", "r")
    keyTime = float(f.readline())
    currTime = time.time()
    oneHour = 3600
    # If the current time is more than one hour past the key time then the key needs to be refeshed
    if(currTime - keyTime > oneHour):
        f.close()
        refresh_key
        f = open("slurm_key.txt", "r")
    key = f.readline()
    f.close()
    return key


def fetch_slurm_jobs() -> list:
    token = get_key()
    headers = {'X-SLURM-USER-NAME': 'caroot', 'X-SLURM-USER-TOKEN': token }
    resp = requests.get('http://10.100.21.252:6820/slurm/v0.0.36/jobs', headers=headers)
    data = json.loads(resp.text)
    return data

def fetch_slurm_nodes() -> list:
    token = get_key()
    headers = {'X-SLURM-USER-NAME': 'caroot', 'X-SLURM-USER-TOKEN': token }
    resp = requests.get('http://10.100.21.252:6820/slurm/v0.0.36/nodes', headers=headers)
    data = json.loads(resp.text)
    return data

if __name__ == '__main__':
    timeStamp = time.strftime("%Y_%m_%d-%H_%M_%S")

    jobs = fetch_slurm_jobs()
    # f = open("slurm_jobs/"+timeStamp+".txt", "w")
    # f.write(json.dumps(jobs, indent=4))
    # f.close()

    nodes = fetch_slurm_nodes()
    # f = open("slurm_nodes/"+timeStamp+".txt", "w")
    # f.write(json.dumps(nodes, indent=4))
    # f.close()

    add_jobs_to_nodes(nodes, jobs)