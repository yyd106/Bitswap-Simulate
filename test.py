
import random
import os

base_dir = os.getcwd()
file_name = os.path.join(base_dir, 'test.txt')
my_open = open(file_name, 'a')

li = list(range(5))
random.shuffle(li)
for i in li:
    my_open.write("Node " + str(i) + " is type \n")

