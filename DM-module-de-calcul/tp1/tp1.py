import random
import math
import time
import matplotlib.pyplot as plt

# question 1
def estime_sqrt2(k):
  cpt = 0
  for i in range(k):
    x = random.uniform(0, 2)
    # x = random.uniform(-2, 2)
    if pow(x,2) <= 2:
      cpt += 1
  return 2 * cpt/k
def test_1():
  print("[ Début du test de la question 1 ]")
  print("\tmath.sqrt(2) = ", math.sqrt(2))
  for i in range(1,7,1):
    k = pow(10,i)
    print(f"\testime_sqrt2({k}) = {estime_sqrt2(k)}")
  print("[ Fin du test de la question 1 ]\n")

""" 
  Estime la n-ième racine de a en utilisant Monte Carlo.
  Arguments:
  a -- La valeur pour laquelle on veut estimer la n-ième racine
  n -- L'ordre de la racine
  k -- Le nombre d'échantillons Monte Carlo
  
  Retourne:
  Une estimation de la n-ième racine de a.
"""
def estimate_root_n(a, n, k):
  count = 0
  for _ in range(k):
    x = random.uniform(-a, a)  # Génère un x aléatoire dans [-a, a]
    if pow(x,n) <= a:  # Vérifie si x^n <= a
      count += 1
  return (count / k) * a
def test_estimate_root_n(a=2,n=2):
  print(f"\nmath.sqrt({a}) = {math.sqrt(a)}")
  for i in range(1,8,1):
    k = pow(10,i)
    print(f"estimate_root_n({a, n, k}) = {estimate_root_n(a,n,k)}")

# question 2
def estime_sqrt2_certitude(epsilon, certitude):
  # Calcul du nombre minimal d'échantillons n
  n = math.ceil(math.log(2 / (1 - certitude)) / (2 * pow(epsilon,2)))
  print(f"\tn = {n}")
  return estime_sqrt2(n)

def test_2(epsilon = 0.01,certitude = 0.99):
  print("[ Début du test de la question 2 ]")
  estimation = estime_sqrt2_certitude(epsilon, certitude)
  print(f"\tEstimation avec ε={epsilon}, certitude={certitude} : {estimation}")
  print("[ Fin du test de la question 2 ]")

# question 3
def select_mediane_tri(l):
  s = sorted(l)
  # print(f"\tSorted list : {s}")
  n = len(s)
  return s[n//2 - 1 if n%2 == 0 else n//2 ]

# question 4 
def select_mediane_procedure(S):
  n = len(S)
  m = pow(n, 3 / 4) 
  r = sorted(random.choices(S, k=math.floor(m)))
  rang_ra = max(1, math.floor(m / 2 - math.sqrt(n)))
  rang_rb = min(math.floor(m / 2 + math.sqrt(n)), math.floor(m))
  a = r[rang_ra - 1]
  b = r[rang_rb - 1]

  rang_sa, rang_sb, cardP = 0, 0, 0
  P = []
  for x in S:
    if x < a: rang_sa += 1
    if x < b: rang_sb += 1
    if a <= x <= b:
      P.append(x)
      cardP += 1
  # Vérifications
  n1 = math.ceil(n / 2)
  if rang_sa > n1 or rang_sb < n1 or cardP >= 4 * m : return "ECHEC"
  P.sort()
  return P[n1 - rang_sa - 1]
def test_3_4(n,m,k):
  print("[ Début du test de la question 3 et 4 ]")
  print(f"\tn % 2 = {n % 2}")
  for i in range(k):
    s = random.sample(range(0,m),n)
    print(f"\tselect_mediane_tri(s) = {select_mediane_tri(s)}")
    print(f"\tselect_mediane_procedure(s) = {select_mediane_procedure(s)}")
  print("[ Fin du test de la question 3 et 4 ]\n")

# question 5
def select_mediane_vegas(s):
  mediane = select_mediane_procedure(s)  
  while mediane == "ECHEC":
    mediane = select_mediane_procedure(s)   
  return mediane
def test_5(n,m):
  s = random.sample(range(0,m),n)
  print("[ Début du test de la question 5 ]")
  print("\tMédiane (Vegas) :", select_mediane_vegas(s))
  expected = select_mediane_tri(s)
  print("\tMédiane exacte :", expected)
  print("[ Fin du test de la question 5 ]\n")

# question 6
def compare_algos(n, k):
  tri_times = []
  vegas_times = []
  for _ in range(k):
    S = random.sample(range(1, n*10), n)
    start = time.time()
    select_mediane_tri(S)
    tri_times.append(time.time() - start)
    
    start = time.time()
    select_mediane_vegas(S)
    vegas_times.append(time.time() - start)
  mean_tri = sum(tri_times) / k
  mean_vegas = sum(vegas_times) / k
  return mean_tri, mean_vegas

def generate_comparison_graph(k=10,sizes=[1000, 5000, 10000, 20000, 50000, 100000]):
  tri_times = []
  vegas_times = []
  
  for n in sizes:
    mean_tri, mean_vegas = compare_algos(n, k)
    tri_times.append(mean_tri)
    vegas_times.append(mean_vegas)
  
  plt.figure(figsize=(10, 6))
  plt.plot(sizes, tri_times, label="select_mediane_tri (Tri)", marker='o')
  plt.plot(sizes, vegas_times, label="select_mediane_vegas (Vegas)", marker='o')
  plt.xlabel("Taille des tableaux (n)")
  plt.ylabel("Temps moyen (secondes)")
  plt.title("Comparaison des temps moyens des algorithmes")
  plt.legend()
  plt.grid(True)
  plt.show()

if __name__ == "__main__":
  test_1()
  test_2(epsilon=0.001)
  test_3_4(n=1000, m=10000,k=2)
  test_5(n=1000,m=10000)
  generate_comparison_graph()
