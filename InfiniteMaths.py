from random import randint, choice
from time import sleep
d = {'rs':0}
while True:
	sign = choice("+-/*")
	if sign == "+" or sign == "-": upper = 99999
	else: upper = 999
	n1 = randint(1,upper)
	n2 = randint(1,upper)
	exec(f"rs = {n1}{sign}{n2}",d)
	rs = d["rs"]
	print(f" {n1:>5} {sign} {n2:<5} = {rs: >14.7f}")
	sleep(0.125)

