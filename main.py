import math
import time
import random
from typing import TextIO
from PolyphaseSort import *

if __name__ == "__main__":
    count = 21000000
    sorting_size = int(count / 2)
    with open("source.txt", "w") as file:
        for i in range(0, count):
            file.write(str(random.randint(1, 10000)) + " ")
    start_time = time.time()
    print("source.txt: ")
    # PolyphaseSort.new_initial_distribution("source.txt", "0.txt", "1.txt", sorting_size)
    PolyphaseSort.old_initial_distribution("source.txt", "0.txt", "1.txt")
    if PolyphaseSort.optimize_to_fibonacci():
        alg_start_time = time.time()
        PolyphaseSort.merge("0.txt", "1.txt", "2.txt")
        end_time = time.time()
        print("Sorting ended")
        print("Algorithm time: " + str(end_time - alg_start_time) + " seconds")
    end_time = time.time()
    print("Total time: " + str(end_time - start_time) + " seconds")