# HPCC Job & Node Data

This project utilizes the Slurm API configured with the High Performance Computing Center at Texas Tech University in order to retrieve current job and node information on the RedRaider Cluster and consolidate the job ids with the nodes information. This is performed by first retrieving the job information and the node information. The job ids and CPU nodes are then scraped from the job information. The nodes from this are then parsed in order to add the job ids to each node. This information is then written to a txt file in JSON format for usability and readability.
