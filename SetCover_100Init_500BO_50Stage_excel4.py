import numpy.matlib
import xlrd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import random
#from sklearn.datasets import make_regression

def readInput(path):
	book = xlrd.open_workbook(path) # in my case the directory contains the excel file named excel.xls
	sheet = book.sheet_by_index(0)
	n=512
	m=211

	tr_list=list(np.zeros((511,210)))
	for i in range(1,n):
		for j in range(1,m):
			x=sheet.cell_value(i,j)
			tr_list[i-1][j-1] = int(x)

	tr_list = list(np.array(tr_list).astype(int).tolist())
	return tr_list


def obj(x_start,tv,tr):

	coverageList = list()

	for i in range(len(x_start)):
		if x_start[i] == 1:
			for j in range(len(tr[i])):
				if tr[i][j] == 1:
					coverageList.append(j+1)
	if len(list(set(coverageList))) == len(tr[0]):

		return np.dot(x_start,tv)

	else:

		return 100000



def random_sel(n):
	
	x_start = list()
	
	for i in range(n):
		
		x_start.append(random.choice([0,1]))
	return x_start

def childListGen(x_start):
	childList = list()

	for i in range(len(x_start)):
		copyOfX =  list()
		copyOfX = x_start[:]
		if x_start[i]==1:

			copyOfX[i]=0
		else:
			copyOfX[i]=1
		childList.append(copyOfX[:])

	return childList

def UCB(x_new,regr1):
	x_new = np.array([x_new])

	per_tree_pred=[tree.predict(x_new) for tree in regr1.estimators_]
	tree_list=list(np.array(per_tree_pred).astype(int).tolist())
	Upper_conf_bound= regr1.predict(x_new)+(2.576 * (np.std(tree_list)))
	return Upper_conf_bound

def hillclimb(x_start, regr1):
	dataset = list()

	current_Sol = x_start[:]
	current_Sol_Val = UCB(current_Sol, regr1)
	while(True):
		childList=childListGen(current_Sol[:])
		dataset.append(current_Sol[:])
		childValues = list()
		for item in childList:
			childValues.append(UCB(item, regr1))
		index = np.argmin(childValues)
		if childValues[index]>= current_Sol_Val:
			break
		else:
			current_Sol = childList[index]
			current_Sol_Val = childValues[index]
	
	return current_Sol , current_Sol_Val,dataset

def hill_climb(regr,x_end):
	dataset = list()

	current_Sol = x_end[:]
	current_Sol_Val = regr.predict([x_end])
	while(True):
		childList=childListGen(current_Sol[:])
		dataset.append(current_Sol[:])
		childValues = list()
		for item in childList:
			childValues.append(int(regr.predict([item])[0]))
			
		index = np.argmin(childValues)
		if childValues[index] >= current_Sol_Val:
			break
		else:
			current_Sol = childList[index]
			current_Sol_Val = childValues[index]
	
	return current_Sol , current_Sol_Val,dataset



def stage(n, regr1):
	x_start = random_sel(n)
	list1 = list()
	list2 = list()
	listofX=list()
	valuesOfX=list()
	for k in range(50):	
		cur_sol,cur_val,dataset =hillclimb(x_start, regr1)
		print (str(k)+' number iteration first hillclimb is done')
		list1.append(cur_sol)
		list2.append(cur_val)
		x_end=cur_sol
		for i in range(len(dataset)):
			listofX.append(dataset[i])
		for i in range(len(dataset)):
			valuesOfX.append(UCB(listofX[i], regr1))
		X = np.array(listofX)
		regr = RandomForestRegressor(max_depth=2, random_state=0)
		
		regr.fit(X[:],valuesOfX[:])
		
		x_restart,x_restart_val,dataset=hill_climb(regr,x_end)
		print (str(k)+' number iteration second hillclimb is done')
		if x_restart == x_end:
			x_start=random_sel(n)
		else:
			x_start = x_restart
		index = np.argmin(list2)
		best_sol=list1[index]
		best_sol_val=list2[index]
		with open("Best_Soltuions_Stage_100_500_Init_LessStage.txt", 'a') as f:
			f.write(str(best_sol_val)+" is the value for the best sol: "+str(best_sol)+' at the end of iteration '+str(k)+'\n')
	return best_sol

def main():	
	path = "excel4.xlsx"
	tr = readInput(path)
	tr = np.array(tr)
	tv = list()
	for i in range(511):
		tv.append(10)

	tv = np.array(tv)

	# generate starting random solutions for Bayesian Optimization
	n = len(tv)

	dataset = list()
	dataset_values = list()
	for i in range(100):
		sol = random_sel(n)
		dataset.append(sol)
		dataset_values.append(obj(sol, tv, tr))

	# Main Bayesian Optimization loop


	for i in range(500):
		regr1 = RandomForestRegressor(max_depth=2, random_state=0)
		
		regr1.fit(dataset[:],dataset_values[:])

		x_next = stage(n, regr1)

		dataset.append(x_next)
		dataset_values.append(obj(x_next, tv, tr))

		index = np.argmin(dataset_values)
		best_sol = dataset[index]
		best_sol_val = dataset_values[index]

		with open("Best_Soltuions_BO_100_500_Init_LessStage.txt", 'a') as f:
			f.write(str(best_sol_val)+" is the value for the best sol: "+str(best_sol)+' at the end of iteration '+str(i)+'\n')


	index = np.argmin(dataset_values)
	best_sol = dataset[index]
	best_sol_val = dataset_values[index]

	print ("The best solution found by Bayesian Optimization is: "+ str(best_sol) +" which has a value of: "+ str(best_sol_val)) 

	
main()