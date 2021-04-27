import os
import sys
import json
import time
import requests
import refresh_key
from process_data import add_jobs_to_nodes

# Updates the key for the red raider cluster if an hour has past since the last time it was used
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

    # Gets current jobs and nodes from the red raider cluster
    jobs = fetch_slurm_jobs()
    nodes = fetch_slurm_nodes()

    # Adds the jobs_ids to the corresponding nodes and exports it as a txt file to the slurm_nodes_with_jobs folder
    add_jobs_to_nodes(nodes, jobs)