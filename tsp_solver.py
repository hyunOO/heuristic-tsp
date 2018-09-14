import sys
import numpy as np

# x is a list which contains the values of x coordinates
x = []
# y is a list which contains the values of y coordinates
y = []
# node is a total number of nodes
node = 0

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

def random_permutation(node):
	return np.random.permutation(node)

def calculate_distance(node_list):
	dist = 0
	for i in range(len(node_list) - 1):
		dist += np.square(x[node_list[i + 1]] - x[node_list[i]]) + np.square(y[node_list[i + 1]] - y[node_list[i]])
	dist += np.square(x[node_list[len(node_list) - 1]] - x[node_list[0]]) + np.square(y[node_list[len(node_list) - 1]] - y[node_list[0]])
	return dist

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
	return dist

def longest_common(list1, list2):
	lcs = [[0 for j in range(len(list1) + 1)] for i in range(len(list2) + 1)]
	for i in range(len(list1) + 1):
		lcs[i][0] = 0
	for j in range(len(list2) + 1):
		lcs[0][j] = 1
	for i in range(len(list1)):
		for j in range(len(list2)):
			if list1[i] == list2[j]:
				lcs[i + 1][j + 1] = lcs[i][j] + 1
			else:
				lcs[i + 1][j + 1] = np.maximum(lcs[i + 1][j], lcs[i][j + 1])
	return lcs

def backtrack(list1, list2, i, j):
	lcs = longest_common(list1, list2)
	if i == -1 or j == -1:
		return []
	if list1[i] == list2[j]:
		result = []
		mid = backtrack(list1, list2, i - 1, j - 1)
		if mid is not None:
			for k in range(len(mid)):
				result.append(mid[k])
		result.append(list1[i])
		return result
	mid = []
	if lcs[i + 1][j] >= lcs[i][j + 1]:
		mid = list(set().union(mid, backtrack(list1, list2, i, j - 1)))
	if lcs[i][j + 1] >= lcs[i + 1][j]:
		mid = list(set().union(mid, backtrack(list1, list2, i - 1, j)))
	return mid

def diff(list1, list2):
	set2 = set(list2)
	return [i for i in list1 if i not in list2]

def crossover(ind1, ind2):
	global node
	ext_ind1 = []
	for i in range(2):
		for j in range(count):
			ext_ind1.append(ind1[j])
	ext_ind2 = []
	for i in range(2):
		for j in range(count):
			ext_ind2.append(ind2[j])
	if longest_common(ext_ind1, ext_ind2) == 0:
		break
	longest = backtrack(ext_ind1, ext_ind2, 2 * node - 1, 2 * node - 1)

print(longest_common([1, 2, 3, 5], [3, 5, 6, 7]))
print(backtrack([1, 2, 3, 9, 11], [0, 2, 3, 6, 7], 4, 4))
print(diff([1, 2, 3, 4, 5], [4, 5]))
