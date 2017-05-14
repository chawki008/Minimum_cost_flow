class Edge:
	s
	d
	b
	c
	cost

	__init__()
	indic()
	__str__()

class Graph:
	vertices_number
	graph
	S
	P

	__init__(vertices_number)
	fill(vertex,edge,direction=1)
	__str__()
	indic()
	get_u3_u2_sets()
	update(gr1,alpha)
	maximum(u3)
	minimum(u2)
	get_updated_graph(s,p)
	maximum_flow()
	mark(Y,A,delta)
	mark_gen()
	flow_max_gen()
