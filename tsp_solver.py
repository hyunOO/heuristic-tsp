import sys
import random
import math
import csv
from optparse import OptionParser

# x is a list which contains the values of x coordinates
x = []
# y is a list which contains the values of y coordinates
y = []
# node is a total number of nodes
node = 0
# point_list is a list of Point
point_list = []

parser = OptionParser()
parser.add_option("-t", type="int", dest="tournament", default=20)
parser.add_option("-p", type="int", dest="population", default=100)
parser.add_option("-i", type="int", dest="iteration", default=1000)
parser.add_option("-m", type="float", dest="mutation_prob", default=0)

filename = sys.argv[1]
(options, args) = parser.parse_args(sys.argv)
file = open(filename, "r")

#tournament is how many sample populations will be participate on tournament selection
tournament = options.tournament
# population is a number of parents population
population = options.population
# iteration is how many iteraions will be
iteration = options.iteration
# mutate is a ratio of mutation
mutation_prob = options.mutation_prob

for i in range(6):
	file.readline()

while True:
	line = file.readline()
	if 'EOF' in line:
		break
	line_list = line.replace('\n', ' ').split(' ')
	count = 0
	for i in range(len(line_list)):
		elem = line_list[i]
		if elem != '':
			if count == 1:
				x.append(float(elem))
				node +=1
			elif count == 2:
				y.append(float(elem))
			else:
				pass
			count += 1

if mutation_prob == 0:
	mutation_prob = 1/math.sqrt(node)

class Point:
	def __init__(self, number, x, y):
		self.number = number
		self.x = x
		self.y = y
	def dist(self, point1):
		return math.sqrt(math.pow(self.x - point1.x, 2) + math.pow(self.y - point1.y, 2))

class PointDistance:
	def __init__(self, number, dist):
		self.number = number
		self.dist = dist

class Node:
	def __init__(self, point, parent, child_list):
		self.point = point
		self.parent = parent
		self.child_list = child_list
	def append_child(self, child):
		self.child_list.append(child)

class Mst:
	def __init__(self, root):
		self.root = root
	def preorder(self):
		queue = [self.root]
		answer = []
		while len(queue) > 0:
			present = queue.pop()
			answer.append(present.point.number)
			child_present = present.child_list
			reversed_child = []
			for i in range(len(child_present)):
				reversed_child.append(child_present[len(child_present) - 1 - i])
			for elem in reversed_child:
				queue.append(elem)
		return answer

class Permutation:
	def __init__(self, permute, dist):
		self.permute = permute
		self.dist = dist

for i in range(node):
	point = Point(i, x[i], y[i])
	point_list.append(point)

def prims():
	global node

	start = random.randint(0, node - 1)
	node_list = [i for i in range(node)]
	start_node = Node(point_list[start], None, [])
	node_list[start] = start_node
	mst = Mst(start_node)

	in_number_list = [start]
	out_number_list = [i for i in range (node) if i != start]

	dist_list = []
	for i in range(node):
		dist_list.append(PointDistance(start, point_list[start].dist(point_list[i])))
	
	while len(in_number_list) < node:
		min_dist = sys.float_info.max
		parent_number = 0
		next_number = 0
		for i in out_number_list:
			current_dist = dist_list[i].dist
			if current_dist < min_dist:
				parent_number = dist_list[i].number
				next_number = i
				min_dist = current_dist
		parent_node = node_list[parent_number]
		next_node = Node(point_list[next_number], parent_node, [])
		node_list[next_number] = next_node
		parent_node.append_child(next_node)
		in_number_list.append(next_number)
		out_number_list.remove(next_number)
		for i in out_number_list:
			dist = point_list[next_number].dist(point_list[i])
			if dist < dist_list[i].dist:
				dist_list[i] = PointDistance(next_number, dist)	

	return mst

# random_permutation function returns a preorder traversal of MST
def random_permutation(node):
	return prims().preorder()

# calcuate_distance function takes a role of fitness function
# However, I will use this function for comparing among individuals
def calculate_distance(node_list):
	global node
	dist = point_list[node_list[node - 1]].dist(point_list[node_list[0]])
	for i in range(len(node_list) - 1):
		dist += point_list[node_list[i]].dist(point_list[node_list[i + 1]])
	return dist

# tournament_selection function proceeds tournament selection among 20 individuals
def tournament_selection():
	global node
	global tournament
	
	ran_individual = []
	for i in range(tournament):
		ran_individual.append(random_permutation(node))
	index = 0
	dist = calculate_distance(ran_individual[0])
	for i in range(tournament - 1):
		new_dist = calculate_distance(ran_individual[i + 1])
		if new_dist < dist:
			dist = new_dist
			index = i + 1
	return Permutation(ran_individual[index], dist)

def gradual_replacement(list1, list2):
	global population

	result = []
	for i in list1:
		result.append(i)
	for i in list2:
		result.append(i)
	result.sort(key = lambda x: x.dist)
	return result[0 : population]

# diff function returns a list who is in list 1 but not in list2
def diff(list1, list2):
	return [i for i in list1 if i not in list2]

def change_start(start_val, target_list):
	global node
	index = target_list.index(start_val)
	result = []
	for i in range(node):
		result.append(target_list[(index + i) % node])
	return result

# crossover function proceeds crossover between two individuals and returns a new child
def crossover(ind1, ind2):
	global node

	result = []

	ran_val = random.randint(0, node - 1)
	change_ind1 = change_start(ran_val, ind1)
	change_ind2 = change_start(ran_val, ind2)

	index = 0
	for i in range(node):
		if change_ind1[i] != change_ind2[i]:
			index = i
			break
	
	if index == node - 1:
		return ind1

	dist1 = point_list[change_ind1[index]].dist(point_list[change_ind1[index - 1]])
	dist2 = point_list[change_ind2[index]].dist(point_list[change_ind2[index - 1]])

	for i in range(index):
		result.append(change_ind1[i])
	if dist1 < dist2:
		result.append(change_ind1[index])
	else:
		result.append(change_ind2[index])

	remain_ind1 = diff(change_ind1, result)
	ran_index = random.randint(0, len(remain_ind1) - 1)
	for i in range(ran_index):
		result.append(remain_ind1[i])
	
	remain_ind2 = diff(change_ind2, result)
	for i in range(len(remain_ind2)):
		result.append(remain_ind2[i])

	return result

def mutate(permutation):
	global node
	global mutation_prob

	rand = random.random()
	if rand < mutation_prob:
		rand1 = random.randint(0, node - 1)
		rand2 = random.randint(0, node - 1)
		while rand2 == rand1:
			rand2 = random.randint(0, node - 1)
		permutation[rand1], permutation[rand2] = permutation[rand2], permutation[rand1]
	return permutation


def min_among_population(population_list):
	min_val = population_list[0]
	for i in range(len(population_list)):
		if min_val.dist < population_list[i].dist:
			min_val = population_list[i]
	return min_val

def crossover_and_mutate(permute1, permute2):
	child_permute = crossover(permute1, permute2)
	child_permute = mutate(child_permute)
	child = Permutation(child_permute, calculate_distance(child_permute))
	return child

def main():
	global population
	global iteration

	population_list = []
	children_list = []

	for i in range(population):
		ts = tournament_selection()
		population_list.append(ts)

	for j in range(iteration):
		child = []
		min_val = min_among_population(population_list)
		for i in range(population - 1):
			child.append(crossover_and_mutate(population_list[i].permute, population_list[i + 1].permute))
		child.append(crossover_and_mutate(population_list[population - 1].permute, population_list[0].permute))
		population_list = gradual_replacement(population_list, child)

	return min_val

def write_on_csv():
	min_val = main()
	min_list = min_val.permute
	print(min_val.dist)
	write_list = []
	for i in min_list:
		list_in = [i + 1]
		write_list.append(list_in)
	solution = open('solution.csv', 'w')
	with solution:
		writer = csv.writer(solution)
		writer.writerows(write_list)

write_on_csv()
