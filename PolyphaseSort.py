from typing import TextIO
import time


class PolyphaseSort:

    @staticmethod
    def create_tapes(tape_number: int):
        for i in range(tape_number):
            with open(str(i) + ".txt", "w") as new_file:
                new_file.close()

    @staticmethod
    def read_number(file: TextIO):
        r = file.read(1)
        curr = file.read(1)
        end_symbols = [" ", ""]
        while curr not in end_symbols:
            r += curr
            curr = file.read(1)
        return r.strip()

    @staticmethod
    def adjust_pointer(file: TextIO, position: int):
        file.seek(position, 0)

    @staticmethod
    def new_initial_distribution(input_path: str, tape_1_path: str, tape_2_path: str, count=10000):
        flag = 0
        with open(input_path, "r") as i:
            with open(tape_1_path, "w") as a:
                with open(tape_2_path, "w") as b:
                    value = 1
                    while value:
                        arr = []
                        counter = count
                        while value and counter:
                            value = PolyphaseSort.read_number(i)
                            if value:
                                arr.append(int(value))
                            else:
                                break
                            counter -= 1
                        print("Sorting...")
                        start_time = time.time()
                        arr.sort()
                        end_time = time.time()
                        print("Sorting took " + str(end_time-start_time) + " seconds")
                        if flag:
                            a.write(" ".join(str(i) for i in arr))
                            a.write(" ")
                            flag = 0
                        else:
                            b.write(" ".join(str(i) for i in arr))
                            b.write(" ")
                            flag = 1

    @staticmethod
    def old_initial_distribution(input_path: str, tape_1_path: str, tape_2_path: str):
        flag = 0
        with open(input_path, "r") as i:
            with open(tape_1_path, "w") as a:
                with open(tape_2_path, "w") as b:
                    current_str = PolyphaseSort.read_number(i)
                    current = int(current_str)
                    previous = current
                    while current_str:
                        current = int(current_str)
                        if previous <= current:
                            if flag:
                                b.write(current_str + " ")
                            else:
                                a.write(current_str + " ")
                        else:
                            if flag:
                                flag = 0
                                a.write(current_str + " ")
                            else:
                                flag = 1
                                b.write(current_str + " ")
                        current_str, previous = PolyphaseSort.read_number(i), current

    @staticmethod
    def merging(tape_1_path: str, tape_2_path: str, output_path: str):
        with open(output_path, "w") as o:
            with open(tape_1_path, "w+") as a:
                with open(tape_2_path, "w+") as b:
                    pass

    @staticmethod
    def count_sequences(file_path: str):
        count = 0
        with open(file_path, "r") as f:
            curr = PolyphaseSort.read_number(f)
            prev = curr
            if curr:
                count = 1
            while curr:
                if curr == "N":
                    count += 1
                elif int(curr) < int(prev):
                    count += 1
                prev = curr
                curr = PolyphaseSort.read_number(f)
        return count

    @staticmethod
    def find_closest_fibonacci(number: int):
        fibonacci = [0, 1]
        index = 1
        while number > fibonacci[index]:
            index += 1
            fibonacci.append(fibonacci[index-2] + fibonacci[index-1])
        return [fibonacci[index-2], fibonacci[index-1], fibonacci[index]]

    @staticmethod
    def find_min_index(array: list[int]):
        if array[0] > array[1]:
            return [1, 0]
        else:
            return [0, 1]

    @staticmethod
    def optimize_to_fibonacci():
        number_seq = [PolyphaseSort.count_sequences("0.txt"), PolyphaseSort.count_sequences("1.txt")]

        if not number_seq[0] or not number_seq[1]:
            return False

        closest_fibonacci = PolyphaseSort.find_closest_fibonacci(number_seq[0] + number_seq[1])
        print("Closest Fibonacci number: " + str(closest_fibonacci))
        print("Number Of Sequences in Tapes: " + str(number_seq))
        minimum = min(number_seq[0], number_seq[1])
        minimum_index_sorted = PolyphaseSort.find_min_index(number_seq)
        print("Minimum number of Sequences in Tape: " + str(minimum))
        if closest_fibonacci[0] < minimum:
            closest_fibonacci = PolyphaseSort.find_closest_fibonacci(closest_fibonacci[2]+1)
            print("New Fibonacci: " + str(closest_fibonacci))
        print("Adjusting to fibonacci start...")
        start_time = time.time()
        with open(str(minimum_index_sorted[0]) + ".txt", "a") as a:
            with open(str(minimum_index_sorted[1]) + ".txt", "a") as b:
                while number_seq[minimum_index_sorted[0]] < closest_fibonacci[0]:
                    a.write("N ")
                    number_seq[minimum_index_sorted[0]] += 1
                while number_seq[minimum_index_sorted[1]] < closest_fibonacci[1]:
                    b.write("N ")
                    number_seq[minimum_index_sorted[1]] += 1
        end_time = time.time()
        print("Adjusting to fibonacci ended")
        print("Adjusting to fibonacci time: " + str(end_time-start_time) + " seconds")
        return True

    @staticmethod
    def merge(tape_1_path: str, tape_2_path: str, output_path: str, tape_start_position=0):
        with open(tape_1_path, "r+") as a:
            with open(tape_2_path, "r+") as b:
                with open(output_path, "w") as o:
                    if tape_start_position: b.seek(tape_start_position, 0)
                    tape_1_pos, tape_2_pos = a.tell(), tape_start_position
                    tape_1_curr, tape_2_curr = PolyphaseSort.read_number(a), PolyphaseSort.read_number(b)
                    if not tape_1_curr or not tape_2_curr:
                        print("Sequence is sorted")
                        return 1
                    else:
                        if tape_1_curr != "N" and tape_2_curr != "N":
                            tape_1_curr, tape_2_curr = int(tape_1_curr), int(tape_2_curr)
                            tape_1_prev, tape_2_prev = tape_1_curr, tape_2_curr
                        while tape_1_curr and tape_2_curr:
                            while tape_1_curr != "N" and tape_2_curr != "N" \
                                    and tape_1_curr >= tape_1_prev and tape_2_curr >= tape_2_prev:
                                if tape_1_curr < tape_2_curr:
                                    o.write(str(tape_1_curr) + " ")
                                    tape_1_pos = a.tell()
                                    tape_1_prev = tape_1_curr
                                    tape_1_curr = PolyphaseSort.read_number(a)
                                else:
                                    o.write(str(tape_2_curr) + " ")
                                    tape_2_pos = b.tell()
                                    tape_2_prev = tape_2_curr
                                    tape_2_curr = PolyphaseSort.read_number(b)
                                if not tape_1_curr:
                                    PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                    PolyphaseSort.copy_rest(b, o)
                                    a.truncate(0)
                                    position = b.tell()
                                    a.close()
                                    b.close()
                                    o.close()
                                    PolyphaseSort.merge(output_path, tape_2_path, tape_1_path, position)
                                    return 1
                                elif not tape_2_curr:
                                    PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                    PolyphaseSort.copy_rest(a, o)
                                    b.truncate(0)
                                    position = a.tell()
                                    a.close()
                                    b.close()
                                    o.close()
                                    PolyphaseSort.merge(output_path, tape_1_path, tape_2_path, position)
                                    return 1
                                elif tape_1_curr == "N":
                                    PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                    PolyphaseSort.copy_rest(b, o)
                                    tape_2_pos = b.tell()
                                    tape_2_curr = PolyphaseSort.read_number(b)
                                    break
                                elif tape_2_curr == "N":
                                    PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                    PolyphaseSort.copy_rest(a, o)
                                    tape_1_pos = a.tell()
                                    tape_1_curr = PolyphaseSort.read_number(a)
                                    break
                                else:
                                    tape_1_curr, tape_2_curr = int(tape_1_curr), int(tape_2_curr)
                                    if tape_1_curr < tape_1_prev:
                                        PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                        PolyphaseSort.copy_rest(b, o)
                                        tape_2_pos = b.tell()
                                        tape_2_curr = PolyphaseSort.read_number(b)
                                        tape_1_prev = tape_1_curr
                                        if not tape_2_curr:
                                            b.truncate(0)
                                            a.close()
                                            b.close()
                                            o.close()
                                            PolyphaseSort.merge(output_path, tape_1_path, tape_2_path, tape_1_pos)
                                            return 1
                                        elif tape_2_curr == "N":
                                            PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                            PolyphaseSort.copy_rest(a, o)
                                            tape_1_pos = a.tell()
                                            tape_1_curr = PolyphaseSort.read_number(a)
                                            break
                                        else:
                                            tape_2_curr = int(tape_2_curr)
                                            tape_2_prev = tape_2_curr
                                    elif tape_2_curr < tape_2_prev:
                                        PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                        PolyphaseSort.copy_rest(a, o)
                                        tape_1_pos = a.tell()
                                        tape_1_curr = PolyphaseSort.read_number(a)
                                        tape_2_prev = tape_2_curr
                                        if not tape_1_curr:
                                            a.truncate(0)
                                            a.close()
                                            b.close()
                                            o.close()
                                            PolyphaseSort.merge(output_path, tape_2_path, tape_1_path, tape_2_pos)
                                            return 1
                                        elif tape_1_curr == "N":
                                            PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                            PolyphaseSort.copy_rest(b, o)
                                            tape_2_pos = b.tell()
                                            tape_2_curr = PolyphaseSort.read_number(b)
                                            break
                                        else:
                                            tape_1_curr = int(tape_1_curr)
                                            tape_1_prev = tape_1_curr
                            while tape_1_curr == "N" or tape_2_curr == "N":
                                if tape_1_curr == "N" and tape_2_curr:
                                    PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                    PolyphaseSort.copy_rest(b, o)
                                    tape_1_pos = a.tell()
                                    tape_2_pos = b.tell()
                                    tape_1_curr = PolyphaseSort.read_number(a)
                                    tape_2_curr = PolyphaseSort.read_number(b)
                                elif tape_2_curr == "N" and tape_1_curr:
                                    PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                    PolyphaseSort.copy_rest(a, o)
                                    tape_1_pos = a.tell()
                                    tape_2_pos = b.tell()
                                    tape_1_curr = PolyphaseSort.read_number(a)
                                    tape_2_curr = PolyphaseSort.read_number(b)
                                elif not tape_2_curr:
                                    b.truncate(0)
                                    a.close()
                                    b.close()
                                    o.close()
                                    PolyphaseSort.merge(output_path, tape_1_path, tape_2_path, tape_1_pos)
                                    return 1
                                elif not tape_1_curr:
                                    a.truncate(0)
                                    a.close()
                                    b.close()
                                    o.close()
                                    PolyphaseSort.merge(output_path, tape_2_path, tape_1_path, tape_2_pos)
                                    return 1
                        if not tape_1_curr:
                            a.truncate(0)
                            a.close()
                            b.close()
                            o.close()
                            PolyphaseSort.merge(output_path, tape_2_path, tape_1_path, tape_2_pos)
                            return 1
                        if not tape_2_curr:
                            b.truncate(0)
                            a.close()
                            b.close()
                            o.close()
                            PolyphaseSort.merge(output_path, tape_1_path, tape_2_path, tape_1_pos)
                            return 1

    @staticmethod
    def copy_rest(tape: TextIO, output: TextIO):
        print("Copy rest started")
        pos = tape.tell()
        curr = PolyphaseSort.read_number(tape)
        prev = curr
        if curr == '':
            return
        if curr == "N":
            output.write(curr + " ")
        else:
            while curr and curr != "N" and int(curr) >= int(prev):
                print(curr)
                output.write(curr + " ")
                prev = curr
                pos = tape.tell()
                curr = PolyphaseSort.read_number(tape)
            PolyphaseSort.adjust_pointer(tape, pos)
        print("Copy rest ended")
