def summate(values): 
	total = 0
	for value in values:
		total += value   
	return total
	
assert summate([1, 2, 3]) == 6