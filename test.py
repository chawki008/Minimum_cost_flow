import copy
class Edge:
	def __init__ (self,s="S",d="P",b=0,c=0,f=0,cost=0):
		self.s = s
		self.d = d
		self.b = b
		self.c = c
		self.f = f
		self.cost = cost


	def indic(self):
		if self.b <= self.f <= self.c :
			return 0
		return self.f-self.c if self.f > self.c else self.b-self.f

	def __str__(self):
		return "(" + self.s + "," + self.d+ "," + str(self.b)+ "," + str(self.c)+ "," + str(self.f) + "," + str(self.cost) + ")"

class Graph:
	def __init__ (self , vertices_num):
		self.graph = {"Er":[[],[]]}
		self.S ='S'
		self.P = 'P'
		self.vertices_num = vertices_num



	def fill (self,vertex, edge, direction = 1 ):
		if (vertex not in self.graph):
			self.graph[vertex]=[[],[]]
		self.graph[vertex][direction].append(edge)
		if (vertex == edge.d):
			return
		self.fill(edge.d,edge,1-direction)


	def __str__(self):
		string = "Graph : \n"
		for i in self.graph:
			string += i + ":\n{IN : "
			for j in self.graph[i][0]:
				string += "(" + j.s + "," + j.d + "," + str(j.b) + "," + str(j.c)+ "," + str(j.f) + "," + str(j.cost) + ") "
			string += "\nOUT :"
			for j in self.graph[i][1]:
				string += "(" + j.s + "," + j.d + "," + str(j.b)+ "," + str(j.c) + "," + str(j.f) + "," + str(j.cost) + ")"
			string += "}\n\n"
		return string


	def indic(self):
		indic = 0
		for i in self.graph:
			for j in self.graph[i][0]:
				indic += j.indic()
		return indic


	def get_u3_u2_sets(self):
		u = [[],[]]
		for i in self.graph:
			for j in self.graph[i][0]:
				if (j.f > j.c):
					u[0].append(j)
				elif(j.f < j.b):
					u[1].append(j)
		return u


	def update (self,gr1):
		for i in self.graph:
			for j in range(self.graph[i][0]):
				self.graph[i][0][j].f = gr1.graph[i][0][j].f


	def maximum(self,u2):
		u0 = max(u2, key = lambda e : e.c)
		return u0
	def minimum(self,u3):
		u0 = min (u3 , key = lambda e : e.c)
		return u0




	def maximum_flow(self):
		return 500

	def mark(self,Y,A,delta):
		graph = self.graph
		for i in Y:
			for j in graph[i][1]:
				if j.d not in Y:
					if j.f < j.c:
						Y.append(j.d)
						A[j.d] = j
						delta[j.d] = min(delta[j.s] , j.c - j.f)
						return True
			for j in graph[i][0]:
				if j.s not in Y:
					if j.f > j.b:
						Y.append(j.s)
						A[j.s] = j
						delta[j.s] = min(delta[j.d],j.f - j.b)
						return True
		return False


	def  mark_gen(self):
		A = {}
		delta = {self.S : self.maximum_flow()}
		Y = [self.S]
		mark = True
		while mark and self.P not in Y:
			mark = self.mark(Y,A,delta)
		if not mark:
			delta[self.P] = -1
		return (mark,delta[self.P],A)



	def flow_max_gen(self):
		mark,epsilon,A = self.mark_gen()
		while mark:
			C_plus = []
			C_minus = []
			x = self.P
			while x != self.S:
				u = A[x]
				if x == u.d:
					C_plus.append(u)
					x = u.s
				else:
					C_minus.append(u)
					x = u.d
			for u in C_plus:
				u.f += epsilon
			for u in C_minus:
				u.f -= epsilon
			mark,epsilon,A = self.mark_gen()
		return epsilon


	def get_updated_graph(self,s,p):
		gr1 = Graph(self.vertices_num)
		gr1.graph = copy.deepcopy(self.graph)
		gr1.S = s
		gr1.P = p
		for i in gr1.graph:
			for j in gr1.graph[i][0]:
				j.b = min (j.f ,j.b)
				j.c = max(j.f ,j.c)
		return gr1


	def feasible_flow(self):
		indic = self.indic()
		existFlow = True
		ur = Edge()
		while indic != 0 and existFlow:
					u3,u2 = self.get_u3_u2_sets()
					if u3:
						alpha = -1
						u0 = self.minimum(u3)
						ur.c = u0.f - u0.c
						s,p = u0.s,u0.d
					elif u2:
						alpha = 1
						u0 = self.maximum(u2)
			 			ur.c = u0.b - u0.f
			 			s,p = u0.d,u0.s
			 		gr1 = self.get_updated_graph(s,p)
					ur.f = gr1.flow_max_gen()
					if ur.f == ur.c:
						self.update(gr1)
						u0.f += alpha*ur.f
					else:
						existFlow = False
					indic = self.indic()
		return existFlow


	def  infinit(self):
		maxi = 0
		for i in self.graph:
			if(self.graph[i][0]):
				maxi = max(maxi,max(self.graph[i][0] ,key = lambda e : e.cost).cost)
		return maxi*self.vertices_num+1

	def minD(self,S,d):
		return min({i:d[i] for i in d if i not in S} , key = lambda e : d[e])



	def get_all_paths(self,A,l=[]):
		paths = []
		l.append(A)
		if not self.graph[A][1]:
			return [[A]]
		for i in self.graph[A][1]:
			if i.d in l:
				return[["Er",i.d]]
			lpaths = self.get_all_paths(i.d,l)
			for lpath in lpaths:
				paths.append(lpath)
		for p in paths:
			p.append(A)
		return paths

	def get_cycles(self):
		cycles = []
		paths = self.get_all_paths("A")
		for path in paths:
			if "Er" in path:
				p = path[1:path[2:].index(path[1])+3]
				cycles.append(p)
		return cycles

	def check_if_negative_cycle(self,cycle):
		summ = 0
		for i in range(len(cycle)-1,1,-1) :
			summ += self.find_edge_where_vertices(cycle[i],cycle[i-1]).cost
		return "Negative cycle" if summ < 0 else "Not negative cycle"

	def find_edge_where_vertices(self,S,D):
		for i in self.graph[S][1]:
			if i.d == D:
				return i
		return None

	def get_residual_network(self):
		residual = Graph(self.vertices_num)
		# residual.graph = copy.deepcopy(self.graph)
		for vertice in self.graph:
			for ed in self.graph[vertice][1]:
				edge = copy.deepcopy(ed)
				if edge.f ==edge.c:
					edge.cost  = -edge.cost
					edge.s,edge.d = edge.d , edge.s
					residual.fill(edge.s,edge)
				elif edge.f > edge.b:
					edge_inv = Edge(edge.d,edge.s,0,0,edge.f,-edge.cost)
					residual.fil(edge.d,edge_inv)
					edge.f = edge.c-edge.f
					residual.fill(edge.s,edge)
		return residual


	def cancel_cycle(self,cycle):
		minimum = self.maximum_flow()
		edges = []
		for i in range(len(cycle)-1,1,-1):
			edge_min = residual.find_edge_where_vertices(cycle[i],cycle[i-1])
			minimum = min(minimum, edge_min.f)
			edge = self.find_edge_where_vertices(cycle[i],cycle[i-1])
			if edge == None:
				edge = self.find_edge_where_vertices(cycle[i-1],cycle[i])
			edges.append(edge)
		for edge in edges:
			edges.f += minimum



	def dijkstra(self):
		infinit = self.infinit()
		d ={}
		for j in self.graph:
			d[j] = infinit
		S = ['S']
		d['S'] = 0
		A = {'S':-1}
		xPivot = 'S'
		while len(S) < len(self.graph) and d[xPivot] < infinit:
			for i in self.graph[xPivot][1]:
				if i.d not in S:
					x = i.d
					if d[x] > d[xPivot] + i.cost:
						d[x] = d[xPivot] + i.cost
						A[x] = i
			xPivot = self.minD(S,d)

			S.append(xPivot)
		sRacine = len(S)==len(self.graph)
		return (d,A,sRacine)




class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg









