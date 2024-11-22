from multigraphe import Multigraph
import random
import math

# Question 1 : Fonction random_multi(m, n) 
def random_multi(n,m):
  multi = Multigraph()
  for i in range(1, n + 1):
    multi.add_node({i})
  
  for _ in range(m):
    u , v = random.sample(range(1,n+1),k=2)
    multi.add_edge({u}, {v})
  return multi

# Question 1 : Fonction illustration_multi()
def illustration_multi():
  multigraph = Multigraph()
  for i in range(1,8):
    multigraph.add_node({i})
  multigraph.add_edge({1}, {2})
  multigraph.add_edge({1}, {5})
  multigraph.add_edge({5}, {2})  
  multigraph.add_edge({5}, {6})  
  multigraph.add_edge({2}, {6})  
  multigraph.add_edge({2}, {3})  
  multigraph.add_edge({6}, {7})  
  multigraph.add_edge({3}, {7})
  multigraph.add_edge({3}, {4})
  multigraph.add_edge({4}, {7})    
  return multigraph

# Question 2 : Fonction contraction(multi,u,v)
def contraction(multi, u, v):
  new_node = u.union(v)
  multi.add_node(new_node)
  for neighbor, edge_count in multi.neighbors(u).items():
    if (neighbor != v):
      for _ in range(edge_count):
        multi.add_edge(new_node, neighbor)
  for neighbor, edge_count in multi.neighbors(v).items():
    if (neighbor != u):
      for _ in range(edge_count):
        multi.add_edge(new_node, neighbor)
  multi.remove_node(u)
  multi.remove_node(v)
def test_contraction(multi):
  edges = [[{2},{6}], [{2,6},{5}], [{4},{7}], [{2,5,6},{1}], [{1,2,6,5},{3}]]
  print("\n[ Debut du test de contraction(illustration_multi()) ]\n")
  for x in edges:
    print("\n\tContraction de l'arêt ",x)
    contraction(multi,x[0],x[1])
    multi.display()
  print("\n[ Fin du test de contraction(illustration_multi()) ]\n")

# Question 3 : Fonction random_arete(multi)
def random_arete(multi):
  edges = {}
  for u in multi.graph:
    for v, edge_count in multi.graph[u].items():
      if u != v:
        if (v, u) not in edges :
          edges[(u, v)] = edge_count
  if not edges:
    return None
  weights , edge_list = [], []
  for edge, weight in edges.items():
    edge_list.append(edge)
    weights.append(weight)
  return random.choices(edge_list, weights=weights)[0]

# Question 4 : karger(multi)
def karger(multi):
  while multi.n > 2 :
    r = random_arete(multi)
    if not r :
      return multi
    contraction(multi,r[0],r[1])
  return multi

def test_karger(multi):
  print("\n[ Debut du test de karger(multi) ]\n")
  karger(multi)
  multi.display()
  print("\n[ Fin du test de karger(multi) ]\n")

# Question 5 : karger_certitude(multi,certitude)
def karger_certitude(multi,certitude) :
  c = -math.log(1 - certitude)
  k = math.ceil((c * pow(multi.n,2)) / 2)
  current_cut = multi
  print(f"\trepetition = {k}")
  for _ in range(k):
    if current_cut.m == 0 :
      return current_cut
    tmp = karger(current_cut.deep_copy())
    if tmp.m < current_cut.m :
      current_cut = tmp
  return current_cut

def test_karger_certitude(multi,certitude):
  if certitude >= 1:
    certitude = 0.99
  print("\n[ Debut du test de karger_certitude(multi) ]\n")
  multi = karger_certitude(multi,certitude)
  multi.display()
  print("\n[ Fin du test de karger_certitude(multi) ]\n")


# Exemple d'utilisation
if __name__ == "__main__" : 

  # m = random_multi(7,10)
  # m.display()
  # test_karger(m.deep_copy())
  # test_karger_certitude(m.deep_copy(),certitude=0.99)

  test_contraction(illustration_multi())
  test_karger(illustration_multi())
  test_karger_certitude(illustration_multi(),certitude=0.99)
