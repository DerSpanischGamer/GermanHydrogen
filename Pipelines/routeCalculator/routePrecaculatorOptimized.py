import json
import copy

with open("lines.json", 'r') as file:
	Lines = json.load(file)

with open("diameters.json", 'r') as file:
	Diameters = json.load(file)

with open("lengths.json", 'r') as file:
	Lenghts = json.load(file)

i = 0
j = 0

diamDiff = 0 # % Between 0 and 1. It represents the % that we accept for a bigger pipe to receiver from a smaller one. For example a 200mm can give to a 220mm with diamDiff = 0.1 (10%)

Nodes = {}
Conections = {}

onlyReceivers = ['DE13A', 'DE217', 'DE21E', 'DE259', 'DE27D', 'DE713', 'DEA32', 'DEF02', 'DEF0A', 'DEF0B'] # These districts only receive, so no point in searching through them

toRedo = [] # These are connexions that reached the max_depth

def guardar(txt):
	print("Guardando datos")
	with open("connections" + txt + ".json", 'w') as file:
		json.dump(Conections, file, indent = 4)

def getLength(path):
	distance = 0
	
	for i in range(len(path) - 1):
		distance += Lenghts[path[i]][path[i + 1]]
    
	return distance

# Init
for L in Lines:
	if (not L[0] in Nodes): Nodes[L[0]] = set()
	if (not L[1] in Nodes): Nodes[L[1]] = set()

for L in Lines: Nodes[L[0]].add(L[1])

# Delete those that only receive since they don't send
for rec in onlyReceivers:
	if (rec in Conections): del Conections[rec]

# Verify diameters
for L in Lines:
	if (not L[0] in Diameters):
		print("Missing node", L[0])
		continue
	
	if (not L[1] in Diameters[L[0]]): print("Missing diameter for connexion", L[0], L[1])

def find_all_paths(graph, start, end, path = [], depth = 0, max_depth = None):
	if (max_depth is not None and depth > max_depth): return [-1]
	
	path = path + [start]
	if start == end: return [path]
	if start not in graph: return []
	
	paths = []
	
	for node in graph[start]:
		if node not in path and node != "XX":  # Ignore the routes that go outside Germany
			if(len(path) >= 2 and Diameters[path[-2]][start] >= Diameters[start][node] * (1 + diamDiff)): continue
			
			newpaths = find_all_paths(graph, node, end, path, depth + 1, None)
			for newpath in newpaths:
				paths.append(newpath)
	
	return paths

for start_node in Nodes:
	print("Done", i, "/", len(Nodes))
	i += 1
	
	if (start_node in onlyReceivers): continue
	
	if (start_node == "XX"): continue
	j = 0
	for end_node in Nodes:
		print("Node", i, "doing", j, '/', len(Nodes))
		j += 1
		
		if (end_node == "XX"): continue
		if (start_node == end_node): continue
		
		routes = find_all_paths(Nodes, start_node, end_node, max_depth = None)
		
		if (routes == [-1]):	# We reached the max_depth, we can redo them later with an increased bound
			toRedo.append([start_node, end_node])
			print("Redo the relation between", toRedo[-1][0], "and", toRedo[-1][1])
			continue
		
		if (not routes == None and len(routes) == 0): continue
			
		if (not start_node in Conections): Conections[start_node] = {}
		
		# Keep the shortest route
		routeToWrite = []
		
		if (len(routes) > 1):
			
			length = float("inf")
			
			for route in routes:
				lRoute = getLength(route)
				
				if (lRoute < length):
					lRoute = length
					routeToWrite = route
			
		else: routeToWrite = routes[0]
		
		Conections[start_node][end_node] = copy.deepcopy(routeToWrite)


guardar("_O_10")

cnt = 0
depths = [25, 37, 50, 60, 75, 100, 125, 150, 175, 200, 225, 250, 300, 500, None]

while (len(toRedo) > 0):
	antes = len(toRedo)
	m_Depth = depths[cnt]
	
	print("Going into the next layer with a depth of", m_Depth)
	
	toDrop = []
	
	for pair in toRedo:
		print("Redoing", toRedo.index(pair), '/', len(toRedo), "depth", m_Depth)
		routes = find_path(Nodes, pair[0], pair[1], max_depth = m_Depth)
		
		if (routes == [-1]):	# We reached the max_depth, we can redo them later with an increased bound
			print("Redo the relation between", pair[0], "and", pair[1])
			continue
		
		if (not routes == None and len(routes) == 0): continue
			
		if (not pair[0] in Conections): Conections[pair[0]] = {}
		
		toDrop.append(toRedo.index(pair))
		Conections[pair[0]][pair[1]] = copy.deepcopy(routes)
	
	
	toDrop.sort(reverse = True)

	for index in toDrop:
		if 0 <= index < len(toRedo):
			toRedo.pop(index)
		else: print("Fuck")
	
	cnt += 1
	print("Before", antes, "now", len(toRedo))
	
	guardar("_O_" + str(m_Depth))

guardar("_O_final")