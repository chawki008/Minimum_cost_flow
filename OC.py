import Graph as G


# print("Enter the number of Edges ")
# N = input()
# graph = G.Graph()
# for i in range(N):
# 	print("Enter source vertice")
# 	s = raw_input()
# 	print("Enter destination vertice")
# 	d = raw_input()
# 	print("Enter minimum capacity")
# 	b = input()
# 	print("Enter maximum capacity")
# 	c = input()
# 	print("Enter current flow")
# 	f = input()
# 	print("Enter cost")
# 	cost = input()
# 	edge = G.Edge(s,d,b,c,f,cost)
# 	graph.fill(edge.s,edge)
# 	print("Edge has been formed succesfully\n")

edge1 = G.Edge('B','A',7,9,0,7)
edge2 = G.Edge('A','F',1,5,0,0)
edge3 = G.Edge('A','E',5,6,0,1)
edge4 = G.Edge('E','D',3,9,0,3)
edge5 = G.Edge('F','C',1,4,0,2)
edge6 = G.Edge('E','F',1,5,0,1)
edge7 = G.Edge('C','B',0,7,0,5)
edge100 = G.Edge('B','D',0,5,0,4)
edge101 = G.Edge('D','C',3,5,0,0)
graph = G.Graph(10,'A','C')
graph.fill('B',edge1)
graph.fill('A',edge3)
graph.fill('A',edge2)
graph.fill('E',edge4)
graph.fill('F',edge5)
graph.fill('E',edge6)
graph.fill('C',edge7)
graph.fill('B',edge100)
graph.fill('D',edge101)
print("Graph has been constructed succesfully\n\n")
print("Press Enter to check if there is a feasible flow ")
raw_input()
feasible ,coupe= graph.feasible_flow()
if(feasible):
	print("The graph has a feasible flow \n")
	print("THE UPDATED GRAPH ")
	print(graph)
	print("Press Enter to get the residual network ")
	raw_input()
	r1 = graph.get_residual_network()
	print("THE RESIDUAL NETWORK")
	print(r1)
	for root in graph.graph.keys()[1:]:   
		print("Press Enter to check if "+ root +" is a root")
		raw_input()
		cycle_A , negative_cycle = r1.shortest_path_general(root)
		if not cycle_A:
			print(root + " is not a root")
		elif negative_cycle:
			print(root + " is a root\n")
			while negative_cycle:
				print("The residual network has a negative cycle")
				print("THE NEGATIVE CYCLE")
				print(cycle_A)
				print("Press Enter to cancel the cycle")
				raw_input()
				graph.cancel_cycle(cycle_A)
				print("Cycle has been canceled ...")
				r1 = graph.get_residual_network()
				cycle_A , negative_cycle = r1.shortest_path_general(root)
			break
		else:
			print(root + " is a root")
			break	
	print ("The shortest path")
	for i in cycle_A:
		print(i)	 	
	print("Minimum Cost Flow")
	flow_min  = 0  
	for i in graph.graph:
		for j in graph.graph[i][1]:
			flow_min += j.f*j.cost
	print(flow_min)	
else:
	print(coupe)
	print("the graph has no feasible flow")	

