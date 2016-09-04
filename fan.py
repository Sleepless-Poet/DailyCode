'''
This program is a social network model.
Author: Jetlee, to my friend Fan.
'''


import random
import pdb
import time
import matplotlib.pyplot as plt
import math

def compute_degree(num=0, p1=0, p2=0, p3=0, p4=0):
	# define a list to store the node, the index represent the node's name,
	# the element '[degree, prefer]' represents the degree of k'th and the 
	# probabilistic of node
	node = {i:[0,0,[], 0] for i in range(num)}	# {node_idx:[degree, prefer_probabilistic, [linked nodes], inverse_prefer_probabilistic]}
	extra_node_pre = {i:0 for i in range(num)}	# records the the probabilistic of node 
	extra_node_pre_abs = {i:0 for i in range(num)}
	min_pre, max_pre = 0, 0
	degree_sum = 0

	# define different operation, 1) add a node, 2) add a edge 3) reconnet
	# two nodes, 4) delete a edge
	records = -1 	# ensure the possion distribution
	while len(node) < 100:
		r = random.uniform(0,1)	# produce a random number
		if r <= p1:
			degree_sum += 2
			node[len(node)] = [0, 0, [], 0]	# add a new node
			extra_node_pre[len(node)] = 0
			extra_node_pre, node = add_node(extra_node_pre, degree_sum, node)
			while records == -1:
				p1 = possion(len(node))
				p2 = random.uniform(0,1-p1)
				p3 = random.uniform(0,1-p1-p2)
				p4 = 1-p1-p2-p3
				if p1 and p2 and p3 and p4:
					records = 1
			if p1 <= 0.001:
				p1=0.001
				p2=0.2562
				p3=0.3964
				p4=0.3464

		elif p1 < r <= p1+p2:
			degree_sum += 2
			extra_node_pre, node = add_edge(extra_node_pre, degree_sum, node)


		elif degree_sum != 0 and p1+p2 < r <= p1+p2+p3:
			if sum(extra_node_pre.values()) != 0:
				extra_node_pre, node = reconnet(extra_node_pre, degree_sum, node)


		elif degree_sum >= 2 and p1+p2+p3 < r <= 1:
			if sum(extra_node_pre.values()) != 0:
				degree_sum -= 2
				extra_node_pre_abs ,extra_node_pre, node = del_edge(extra_node_pre, degree_sum, 
					extra_node_pre_abs, node)

		else:
			if p1+p2+p3+p4 != 1:
				print 'The p1+p2+p3+p4 is not equal 1!'
				return
		print len(node)

	print 'p1=%s,p2=%s,p3=%s,p4=%s'%(p1,p2,p3,p4)
	return node

def add_node(extra_node_pre, degree_sum, node):
	#temp = extra_node_pre.values()
	#print node
	new_node = len(node)-1
	if degree_sum == 2:
		r0 = random.randint(0, len(node)-2)
		node[r0][0] += 1
		node[new_node][0] += 1
		node[r0][2].append(new_node)
		node[new_node][2].append(r0)
	else:
		pos0 = new_node
		while pos0 == new_node:
			pre0 =  random.uniform(0,1)	# produce a probabilistic, chose a node to add 1-degree
			'''
			TODO
			'''
			pos0 = position(pre0, extra_node_pre, node)
		node[pos0][0] += 1
		node[new_node][0] += 1
		node[pos0][2].append(new_node)
		node[new_node][2].append(pos0)

	# compute the probabilistic of node
	for idx in node:
		node[idx][1] = node[idx][0]/float(degree_sum)
		extra_node_pre[idx] = node[idx][1]
	#print node
	return extra_node_pre, node

def position(pre0, extra_node_pre, node):
	temp = extra_node_pre.values()
	temp.sort()
	pos0 = 0
	pre_sum = 0

	flag0 = True
	for item in temp:
		pre_sum += item
		if flag0 and pre_sum <= pre0:
			continue
		else:
			flag0 = False
			pos0 = item

	#print 'chose probabilistic pos0=%d, pos1=%d'%(pos0, pos1)
	flag0 = True
	for idx in node:
		if flag0 and node[idx][1] == pos0:
			flag0 = False
			pos0 =  idx
			break

	return pos0

def possion(k):
    """ 
    poisson distribution 
    return a integer random number, L is the mean value 
    """  
    L = 3
    e = math.exp(-L) 
    p = (L**k)*e/math.factorial(k)
    return p

def add_edge(extra_node_pre, degree_sum, node):
	"TODO: add a edge into the network, such as 'a->b', chose 'a' randomly, then chose 'b' according to the prefer"
	
	if degree_sum == 2:
		node1 = random.randint(0, len(node)-1)
		node2 = random.randint(0, len(node)-1)
		while node1 == node2:
			node1 = random.randint(0, len(node)-1)
			node2 = random.randint(0, len(node)-1)
		node[node1][0] += 1
		node[node1][2].append(node2)
		node[node1][1] = 0.5
		extra_node_pre[node1] = node[node1][1]
		node[node2][0] += 1
		node[node2][2].append(node1)
		node[node2][1] = 0.5
		extra_node_pre[node2] = node[node2][1]
		return extra_node_pre, node


	node1 = random.randint(0, len(node)-1)
	prob = 0
	records = -1
	node2 = -1
	start = time.clock()
	while records == -1:
		#pdb.set_trace()
		r_node2 = random.uniform(0,1)
		for idx in extra_node_pre:
			if prob <= r_node2 <= prob + extra_node_pre[idx]:
				node2 = idx
				break
			prob += extra_node_pre[idx]
		#pdb.set_trace()
		if node2 != -1 and node1 != node2 and (node2 not in node[node1][2]):
			records = 1
		if time.clock() - start > 2:
			node1 = random.randint(0, len(node)-1)

	node[node1][0] += 1
	node[node1][2].append(node2)
	node[node2][0] += 1
	node[node2][2].append(node1)

	# compute the probabilistic of node
	for idx in node:
		node[idx][1] = node[idx][0]/float(degree_sum)
		extra_node_pre[idx] = node[idx][1]
	#print node
	return extra_node_pre, node

def reconnet(extra_node_pre, degree_sum, node):
	"TODO: change two nodes' edge, like: a->b to a'->b"
	# chose a node according to the prefer probabilistic
	r = random.uniform(0, 1)
	prob = 0

	for idx in extra_node_pre:
		if prob <= r <= prob + extra_node_pre[idx]:
			node1 = idx
			break
		prob += extra_node_pre[idx]

	start = time.clock()
	#node2 = random.randint(0, len(node)-1)
	record2 = -1
	while record2 == -1:
		if time.clock() - start > 5:
			return extra_node_pre, node
		node2 = random.randint(0, len(node)-1)
		if node2 != node1 and node[node2][2] != []:
			# chose a edge randomly
			for node3 in node[node2][2]:
				if node3 != node1 and (node3 not in node[node1][2]):
					#pdb.set_trace()
					record2 = node3
					break
		print 'reconnet:%d,%d\n'%(node1, node2)

	node3 = record2
	node[node1][0] += 1
	node[node1][2].append(node3)
	node[node2][0] -= 1
	node[node2][2].remove(node3)
	node[node3][2].remove(node2)
	node[node3][2].append(node1)

	# compute the probabilistic of node
	for idx in node:
		node[idx][1] = node[idx][0]/float(degree_sum)
		extra_node_pre[idx] = node[idx][1]
	#print node
	return extra_node_pre, node

def del_edge(extra_node_pre, degree_sum, extra_node_pre_abs, node):
	"Finished: delete a edge, chose a node1 randomly, then chose a node2 according prefer inverse"
	
	# compute the inverse prefer to chose the edge
	for idx in node:
		node[idx][3] = (1-node[idx][1])/(len(node)-2)
		extra_node_pre_abs[idx] = node[idx][3]
	node1 = random.randint(0, len(node)-1)
	while node[node1][0] == 0 or node[node1][2] == []:
		node1 = random.randint(0, len(node)-1)
	temp_node_set = node[node1][2]

	# compute the sum of connected to node1
	s = 0
	for r_node in temp_node_set:
		s += node[r_node][3]
	
	# according to the inverse probabilistic, find the node2
	node2_prob = random.uniform(0, s)
	prob = 0
	#pdb.set_trace()
	for node2 in temp_node_set:
		if prob <= node2_prob <= prob+extra_node_pre_abs[node2]:
			record = node2
			break
		prob += extra_node_pre_abs[node2]
	# delete the edge

	node[node1][2].remove(record)
	node[node1][0] -= 1
	node[record][2].remove(node1)
	node[record][0] -= 1

	# recompute the prefer probabilistic
	if degree_sum != 0:
		for idx in node:
			node[idx][1] = node[idx][0]/float(degree_sum)
			extra_node_pre[idx] = node[idx][1]

	return extra_node_pre_abs ,extra_node_pre, node 




if __name__ == '__main__':
	num = 50
	p1, p2, p3, p4 = 0.35, 0.25, 0.2, 0.2
	node = compute_degree(num=num, p1=p1, p2=p2, p3=p3, p4=p4)
	result = {}
	for idx in node:
		if node[idx][0] in result:
			result[node[idx][0]] += 1
		else:
			result[node[idx][0]] = 1

	x = []
	y = []
	s = len(result) 
	for idx in result:
		x.append(idx)
		y.append(result[idx]/float(s))
	print x, y

	plt.plot(x, y)
	plt.show()

	f = open('text.txt', 'w')
	f.write('network is:\n')
	for i in node:
		f.write(str(i)+str(node[i]))

	f.write('\n\n\nresult is:\n')
	for j in range(len(x)):
		f.write(str(x[j])+':'+str(y[j])+', ')
	f.close()


	'''node = {0:[0,0, []], 1:[0,0,[]], 2:[0,0,[]], 3:[0,0,[]]}
	extra_node_pre = {0:0, 1:0, 2:0, 3:0}
	degree_sum = 2
	for i in range(3):
		node[len(node)] = [0, 0, [], 0]
		extra_node_pre[len(extra_node_pre)] = 0
		extra_node_pre, node = add_node(extra_node_pre, degree_sum, node)
		degree_sum += 2
	print node, '\n'
	
	degree_sum=6
	extra_node_pre = {0: 0.0, 1: 0.5, 2: 0.0, 3: 0.0, 4: 0.16666666666666666, 5: 0.16666666666666666, 
			6: 0.16666666666666666}
	extra_node_pre_abs = {0: 0, 1: 0, 2: 0.0, 3: 0.0, 4: 0, 5: 0, 6: 0}
	node ={0: [0, 0.0, [], 0], 1: [3, 0.5, [4, 5, 6], 0], 2: [0, 0.0, [],0], 3: [0, 0.0, [], 0], 
			4: [1, 0.16666666666666666, [1], 0], 5: [1, 0.16666666666666666, [1], 0], 
			6: [1, 0.16666666666666666, [1], 0]}
	print add_edge(extra_node_pre, degree_sum+2, node)
	'''











