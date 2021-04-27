# HPCC Job & Node Data

This project utilizes the Slurm API configured with the TTU HPCC in order to retrieve current system job and node information and consolidate the job id's with the nodes information. This is performed by first retrieving jobs information and nodes information. The job id's are then scraped with their corresponding CPU nodes being used. The nodes are then parsed in order to add the job id's to each one. This information is then written to a txt file in JSON format for usability and readability.
