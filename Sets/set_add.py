if __name__=='__main__':
	n = int(raw_input())
	st = set()
	for i in range (n):
		country = raw_input()
		st.add(country)

	print (len(st))