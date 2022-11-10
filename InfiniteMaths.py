from random import randint, choice
from time import sleep
d = {'rs':0}
while True:
	sign = choice("+-/*%*/-+")
	if sign == "*": upper = 999
	else:           upper = 99999
	n1 = randint(1,upper)
	n2 = randint(1,n1)
	exec(f"rs = {n1}{sign}{n2}",d)
	rs = d["rs"]
	if sign == '/': print(f" {n1:>5} {sign} {n2:<5} = {rs: >10.3f}")
	else:           print(f" {n1:>5} {sign} {n2:<5} = {rs: >6d}")
	sleep(choice((1,1,1,1,2,2,3,4,5,6))/8)

