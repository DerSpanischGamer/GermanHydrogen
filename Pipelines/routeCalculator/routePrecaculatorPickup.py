import json
import copy

with open("lines.json", 'r') as file:
	Lines = json.load(file)

with open("diameters.json", 'r') as file:
	Diameters = json.load(file)

with open("connections10.json", 'r') as file:
	Conections = json.load(file)

i = 0
j = 0

Nodes = {}

onlyReceivers = ['DE13A', 'DE217', 'DE21E', 'DE259', 'DE27D', 'DE713', 'DEA32', 'DEF02', 'DEF0A', 'DEF0B'] # These districts only receive, so no point in searching through them

toRedo = [] # These are connexions that reached the max_depth

def guardar(txt):
	print("Guardando datos")
	with open("connections" + txt + ".json", 'w') as file:
		json.dump(Conections, file, indent = 4)

# Init
for L in Lines:
	if (not L[0] in Nodes): Nodes[L[0]] = set()
	if (not L[1] in Nodes): Nodes[L[1]] = set()

for L in Lines: Nodes[L[0]].add(L[1])

# Verify diameters
for L in Lines:
	if (not L[0] in Diameters):
		print("Missing node", L[0])
		continue
	
	if (not L[1] in Diameters[L[0]]): print("Missing diameter for connexion", L[0], L[1])

def find_path(graph, start, end, path = [], depth = 0, max_depth = 10):
	if (max_depth is not None and depth > max_depth):
		return [-1]
	
	path = path + [start]
	if start == end: 
		return path
	if not start in graph: 
		return None
	
	for node in graph[start]:
		if (node not in path and node != "XX"):
			if (path[-1] != start and Diameters[path[-1]][start] >= Diameters[start][end]): 
				continue
			
			newpath = find_path(graph, node, end, path, depth+1, max_depth)
			if newpath: 
				return newpath
	
	return None

for origin in Conections:
	for destination in Conections[origin]:
		if (Conections[origin][destination]): toRedo.append([origin, destination])

cnt = 5
depths = [25, 37, 50, 60, 75, 100, 125, 150, 200, 250, 300, 500, None]

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
	
	guardar(str(m_Depth))

guardar("final")