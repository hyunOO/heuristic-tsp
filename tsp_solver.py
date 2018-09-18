import sys
import random
import math
import csv

# x is a list which contains the values of x coordinates
x = []
# y is a list which contains the values of y coordinates
y = []
# node is a total number of nodes
node = 0
# point_list is a list of Point
point_list = []

#tournament is how many sample populations will be participate on tournament selection
tournament = 20
# population is a number of parents population
population = 100
# iteration is how many iteraions will be
iteration = 1000
# mutate is a ratio of mutation
mutate = 0.1

filename = sys.argv[1]
file = open(filename, "r")

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

class Point:
	def __init__(self, number, x, y):
		self.number = number
		self.x = x
		self.y = y
	def dist(self, point1):
		return math.sqrt(math.pow(self.x - point1.x, 2) + math.pow(self.y - point1.y, 2))

class Permutation:
	def __init__(self, permute, dist):
		self.permute = permute
		self.dist = dist

for i in range(node):
	point = Point(i, x[i], y[i])
	point_list.append(point)

# random_permutation function returns a randomly generated permutation from 1 to integer value node
def random_permutation(node):
	x = [i for i in range(node)]
	random.shuffle(x)
	return x

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

	ran_individual = []
	for i in range(20):
		ran_individual.append(random_permutation(node))
	index = 0
	dist = calculate_distance(ran_individual[0])
	for i in range(19):
		new_dist = calculate_distance(ran_individual[i + 1])
		if new_dist < dist:
			dist = new_dist
			index = i + 1
	return Permutation(ran_individual[index], dist)

def ellitism(list1, list2):
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
	rand = random.random()
	if rand < (1 / math.sqrt(node)):
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
		population_list = ellitism(population_list, child)

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
