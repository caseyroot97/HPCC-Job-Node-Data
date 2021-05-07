import json
import time

def add_jobs_to_nodes(nodes, jobs):
    
    node_dict = {}

    for object in jobs['jobs']:
        job_id = object['job_id']
        nodes_str = object['nodes']

        if nodes_str != "":

            # Separates nodes by number (ex. "cpu-3-5" to "3-5" or "cpu-23-[1-3,5]" to "23-[1-3,5]")
            nodes_str = nodes_str[4:]
            nodes_list = nodes_str.split(",cpu-")

            # Separates first number from the rest (ex. ['3','5'] or ['23','[1-3,5]'])
            for node in nodes_list:
                node = node.split("-", 1)
                major_number = node[0]
                minor_number = node[1]

                # Check if the second number is a set and separates them (ex. ['1-3', '5'])
                if minor_number[0] == "[":
                    minor_number = minor_number[1:-1]
                    minor_number = minor_number.split(",")
                    for job_node in minor_number:

                        # Separates if the numbers are a range
                        nodes_range = job_node.split("-")

                        # Adds all the nodes in the range
                        if len(nodes_range)>1:
                            loops = int(nodes_range[1])-int(nodes_range[0])+1
                            for x in range(0, loops):
                                if "cpu-" + major_number + "-" + job_node not in node_dict:
                                    node_dict["cpu-" + major_number + "-" + str(int(nodes_range[0]) + x)] = [job_id]
                                else:
                                    node_dict["cpu-" + major_number + "-" + str(int(nodes_range[0]) + x)].append(job_id)
                        
                        # Adds the job to a single node if it's in the set
                        else:
                            if "cpu-" + major_number + "-" + job_node not in node_dict:
                                node_dict["cpu-" + major_number + "-" + job_node] = [job_id]
                            else:
                                node_dict["cpu-" + major_number + "-" + job_node].append(job_id)

                # Adds the job to a single node not in a set
                else:
                    if "cpu-" + major_number + "-" + minor_number not in node_dict:
                        node_dict["cpu-" + major_number + "-" + minor_number] = [job_id]
                    else:
                        node_dict["cpu-" + major_number + "-" + minor_number].append(job_id)

    # Adds all the jobs in the dictionary to the correct nodes in JSON format
    for node in nodes['nodes']:
        if node['name'] in node_dict:
            node['jobs'] = node_dict.get(node['name'])
        else:
            node['jobs'] = []

    # Exports the nodes with jobs as a JSON file
    timeStamp = time.strftime("%Y_%m_%d-%H_%M_%S")
    f = open("slurm_nodes_with_jobs/"+timeStamp+".txt", "w")
    f.write(json.dumps(nodes, indent=4))
    f.close()