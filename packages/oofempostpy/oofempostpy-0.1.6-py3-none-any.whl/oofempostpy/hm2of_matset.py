def hm2of_matset(input_file, output_file):

    with open(input_file, 'r') as inp_file:
        lines = inp_file.readlines()
    
    nodes_section = False
    elements_section = False
    elset_steel = []
    current_section = None
    node_data = []
    element_data = []
    nsets = {}

    for line in lines:
        if line.startswith('**'):
            # Skip comment lines
            continue
        line = line.strip()

        # Handle nodes section
        if line.startswith('*NODE'):
            nodes_section = True
            elements_section = False
            current_section = 'nodes'
            continue
        elif line.startswith('*ELEMENT'):
            nodes_section = False
            elements_section = True
            current_section = 'elements'
            continue
        elif line.startswith('*ELSET') and 'ELSET=steel' in line:
            current_section = 'elset_steel'
            continue
        elif line.startswith('*NSET'):
            current_section = 'nsets'
            nset_name = line.split('=')[-1]
            nsets[nset_name] = []
            continue

        # Collect node data
        if nodes_section and current_section == 'nodes':
            node_data.append(line)

        # Collect element data
        elif elements_section and current_section == 'elements':
            element_data.append(line)

        # Collect ELSET data for steel elements (multiple lines)
        elif current_section == 'elset_steel':
            elset_steel.extend([int(x) for x in line.split(',') if x.strip()])

        # Collect NSET data
        elif current_section == 'nsets':
            nsets[nset_name].extend([int(x) for x in line.split(',') if x.strip()])

    # Write to output file
    with open(output_file, 'w') as out_file:
        # Write nodes section
        out_file.write("###################### N O D E ########################\n")
        for node in node_data:
            parts = node.split(',')
            node_id = parts[0]
            coords = ' '.join(parts[1:])
            out_file.write(f"node {node_id} coords {len(parts)-1} {coords.strip()}\n")

        # Write elements section
        out_file.write("################# E L E M E N T ##################\n")
        for element in element_data:
            parts = [int(x) for x in element.split(',')]
            element_id = parts[0]
            nodes = parts[1:]
            mat_id = 2 if element_id in elset_steel else 1  # Assign mat 2 to steel elements
            nodes_str = ' '.join(map(str, nodes))
            out_file.write(f"Quad1PlaneStrain {element_id} nodes {len(nodes)} {nodes_str} mat {mat_id} crossSect 1\n")

        # Write sets section
        out_file.write("###################### S E T ########################\n")
        for set_name, set_nodes in nsets.items():
            out_file.write(f"Set {set_name} nodes {len(set_nodes)} {' '.join(map(str, set_nodes))}\n")