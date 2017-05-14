import copy
#Arc
class Edge:
	#constructeur
	def __init__ (self,s="S",d="P",b=0,c=0,f=0,cost=0):
		#initialisation des attributs
		self.s = s   		#Sommet source
		self.d = d 			#Sommet destination	
		self.b = b 			#Borne inferieur
		self.c = c 			#Borne superieur
		self.f = f 			#Flot courant
		self.cost = cost    #Cout unitaire
	
	#indic individuel d'un seul arc
	def indic(self):
		if self.b <= self.f <= self.c :
			return 0
		return self.f-self.c if self.f > self.c else self.b-self.f
	
	#toString()
	def __str__(self):
		return "(" + self.s + "," + self.d+ "," + str(self.b)+ "," + str(self.c)+ "," + str(self.f) + "," + str(self.cost) + ")"

#Graphe
class Graph:
	def __init__ (self , vertices_num = 10,S = '1',P ='2'):
		self.graph = {"Er":[[],[]]} #Tableau associatif ayant la structure {"Sommet" : [ [Arcs entrants] , [Arcs sortants] ] }
		self.S = S #Sommet source utilise pour calculer le flot maximale
		self.P = P #Sommet puit utilise pour calculer le flot maximale
		self.vertices_num = vertices_num #nombre de sommets
		

	#Ajouter un arc au graphe
	#prend comme parametres le sommet source et l'arc a ajouter	
	def fill (self,vertex, edge, direction = 1 ):
		if (vertex not in self.graph):
			self.graph[vertex]=[[],[]]
		self.graph[vertex][direction].append(edge)
		if (vertex == edge.d):
			return
		self.fill(edge.d,edge,1-direction)
		
	#Affichage du graphe	
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

	#calcule du flot realisable	
	def feasible_flow(self):
		indic = self.indic() 
		existFlow = True
		ur = Edge()
		while indic != 0 and existFlow:
					print ("INDIC")
					print(indic)
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
					print(u0)
			 		gr1 = self.get_updated_graph(s,p)	
					ur.f = gr1.flow_max_gen(ur.c)
					if ur.f == ur.c:
						self.update(gr1)
						u0.f += alpha*ur.f
					else:
						existFlow = False
					indic = self.indic()		
		return existFlow,gr1.coupe_minimale(self.S)			

	#indic totale du graphe	
	def indic(self):
		indic = 0
		for i in self.graph:
			for j in self.graph[i][0]:
				indic += j.indic()
		return indic

	#construction des ensembles u2 et u3 
	#u2 = {u : u.f < u.b}
	#u3 = {u : u.f > u.c}	
	def get_u3_u2_sets(self):
		u = [[],[]]
		for i in self.graph:
			for j in self.graph[i][0]:
				if (j.f > j.c):
					u[0].append(j)
				elif(j.f < j.b):
					u[1].append(j)
		return u

	#Construction du reseau R' a partir du graphe original	
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

	#Mise a jour du graphe original a partir du reseau R' apres le calcul du flot maximal sur ce reseau	
	def update (self,gr1):
		for i in self.graph:
			for j in range(len(self.graph[i][0])):
				self.graph[i][0][j].f = gr1.graph[i][0][j].f


	def maximum(self,u2):
		u0 = max(u2, key = lambda e : e.c)	
		return u0			
	def minimum(self,u3):
		u0 = min (u3 , key = lambda e : e.c)	
		return u0



	
	def maximum_flow(self):
		return 500


	#Marquage generale	
	def  mark_gen(self):
		A = {}									#les sommets associes aux arcs marques  
		delta = {self.S : self.maximum_flow()}  #flot possible a passer sur chaque arc pendant ce marquage la 
		Y = [self.S] 							#ensemble des sommets marques
		mark = True
		while mark and self.P not in Y:
			mark = self.mark(Y,A,delta)		
		if not mark:
			delta[self.P] = -1
		return (mark,delta[self.P],A)
	

	def mark(self,Y,A,delta):
		graph = self.graph
		for i in reversed(Y):   
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

	#Flot max generale	
	def flow_max_gen(self,ur_c):
		max_flow = 0
		mark1 = True
		mark,epsilon,A = self.mark_gen()
		while mark and mark1:
			if max_flow + epsilon > ur_c:
				epsilon = ur_c - max_flow
				mark1 = False
			max_flow += epsilon
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
			mark,epsilon1,A = self.mark_gen()
			if epsilon1 != -1:
				epsilon = epsilon1
				
		return max_flow	

	



	#Cout unitaire maximale 	
	def  infinit(self):
		maxi = 0
		for i in self.graph:
			if(self.graph[i][0]):
				maxi = max(maxi,max(self.graph[i][0] ,key = lambda e : e.cost).cost)
		return maxi*self.vertices_num+1	
	
	


	#Verifier si un cycle est absorbant ou pas	
	def check_if_negative_cycle(self,cycle):
		summ = 0
		for i in range(len(cycle)-1,0,-1) :
			edge = self.find_edge_where_vertices(cycle[i],cycle[i-1])
			summ += self.find_edge_where_vertices(cycle[i],cycle[i-1]).cost
		return True if summ < 0 else False	

	#Determiner l'arc a partir des sommets source et destination	
	def find_edge_where_vertices(self,S,D):
		for i in self.graph[S][1]:
			if i.d == D:
				return i 		
		return None		

	#Construire le reseau residuel (R1)	
	def get_residual_network(self):
		residual = Graph(self.vertices_num,self.S,self.P)
		for vertice in self.graph:
			for ed in self.graph[vertice][1]:
				edge = copy.deepcopy(ed)
				if edge.f ==edge.c:
					edge.cost  = -edge.cost
					edge.s,edge.d = edge.d , edge.s
					residual.fill(edge.s,edge)
				elif edge.f > edge.b:
					edge_inv = Edge(edge.d,edge.s,0,0,edge.f,-edge.cost)
					residual.fill(edge.d,edge_inv)
					edge.f = edge.c-edge.f
					residual.fill(edge.s,edge)
				else:
					edge.f=edge.c
					residual.fill(edge.s,edge)	
		return residual				

	#destruction des circuits absorbants en ameliorant le flot
	def cancel_cycle(self,cycle):
		minimum = self.maximum_flow()
		edges = []
		for i in range(len(cycle)-1,0,-1):
			alpha = 1		
			edge = self.find_edge_where_vertices(cycle[i],cycle[i-1])
			if edge == None:
				edge = self.find_edge_where_vertices(cycle[i-1],cycle[i])
				if edge.b != edge.f:
					minimum = min(minimum,edge.f - edge.b) 
				alpha = -1
			elif edge.c != edge.f:
					minimum = min(minimum, edge.c - edge.f)
					
			edges.append((edge,alpha))
		for (edge,alpha) in edges:
			edge.f += alpha*minimum	



	#Recherche generale de recherche d une arborescence des plus courts chemins	a partir d'un sommet R
	#return ([],False) si R n est pas racine
	#(cycle,True) si R racine et l arborescence contient un circuit absorbant (cycle est le circuit absorbant)
	#(A,False) si R racine et l arborescence ne contient pas un circuit absorbant (A est l'ensemble des sommets de cette arborescence des plus courts chemins)	
	def shortest_path_general(self,R):
		d,A0,sRacine = self.dijkstra(R) #d contient les distances des sommets a partir du racine , A0 les arcs amenants a chaque sommet , sRacine vrai si R est un racine 
		negative_cycle = False
		if (sRacine):
			A = A0.values() #les arcs du l arborenscence
			u=self.exist_u(d)
			A.remove(-1)
			while not negative_cycle and u != None:
				if self.has_cycle(A,u):
					cycle = [u.d]
					A0[u.d] = u	
					self.get_cycle(A0,u,u.d,cycle)
					cycle.append(u.d)
					cycle = list(reversed(cycle))
					if self.check_if_negative_cycle(cycle):
						negative_cycle = True
						return (cycle,negative_cycle)
				x = u.d 
				A.remove(A0[x])
				A.append(u)
				A0[x] = u
				delta = d[u.d] - d[u.s] - u.cost
				d[x] -= delta 
				self.update_descend(d,x,delta,A)

				u = self.exist_u(d)	
			return (A,negative_cycle)
		return ([],False)	

	def minD(self,S,d): 
		return min({i:d[i] for i in d if i not in S} , key = lambda e : d[e])

	def dijkstra(self,R):
		infinit = self.infinit()
		d ={}	
		for j in self.graph:
			d[j] = infinit
		S = [R]
		d[R] = 0
		A = {R:-1}
		xPivot = R
		while len(S) < len(self.graph) and d[xPivot] < infinit:
			for i in self.graph[xPivot][1]:
				if i.d not in S:
					x = i.d
					if d[x] > d[xPivot] + i.cost:
						d[x] = d[xPivot] + i.cost
						A[x] = i
			xPivot = self.minD(S,d)
			if d[xPivot] != infinit:
				S.append(xPivot)			
		sRacine = len(S)==(len(self.graph)-1)	
		return (d,A,sRacine)


	def get_cycle(self,A0,u,d,cycle):
		if u.s != d:
			cycle.append(self.get_cycle(A0,A0[u.s],d,cycle))		
			return(u.d)
		return u.d	


	

	def check_descendant(self,V,A,V_D):
		for i in A:
			if i.s == V_D:
				if i.s == V:
					return True
				else:		
					return (check_descendant(self,V,A,i.d))	
		return False
					
	def has_cycle(self,A,u):
		for i in A:
			if i.s == u.d:
				return (self.check_descendant(i.s,A,i.s))
				
		return False
		
	def update_descend(self,d,x,delta,A):
		
		for i in A:
			if i.s == x:
				d[i.d] -= delta
				self.update_descend(d,i.d,delta,A)

	def exist_u (self,d):
		for i in self.graph:
			for j in self.graph[i][1]:
				if d[j.d]-d[j.s] > j.cost:
					return j
		return None				
				

	def get_cycles(self):
		cycles = []
		paths = self.get_all_paths(self.S)
		for path in paths:
			if "Er" in path:
				p = path[1:path[2:].index(path[1])+3]
				cycles.append(p)
		return cycles		


	def get_all_paths(self,A,l=[]):
		paths = []
		if not self.graph[A][1]:
			return [[A]]  
		for i in self.graph[A][1]:
			if A not in l:
				l.append(A)
			if i.d not in l:
				lpaths = self.get_all_paths(i.d,l)
			else:
				lpaths = [["Er",i.d]]
			for lpath in lpaths:
				paths.append(lpath)
		l.remove(A)
		for p in paths: 
			p.append(A)
		return paths

	def coupe_minimale(self, s ,coupe=[],c=0):
		if c == self.vertices_num:
			return
		l = self.graph[s][0]
		for arc in l:
			if arc.f < arc.c:
				self.coupe_minimale(arc.s,coupe,c+1)
				coupe.append(arc.d)
		return coupe		
		
