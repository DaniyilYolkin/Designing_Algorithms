if __name__ == "__main__":
    with open("source.txt", "r") as source:
        s = source.read(2)
        print(s)

    # source.seek(0, 0) - // Reset file pointer
    # source.read(num) - // num - number of symbols to read
    # source.tell() - // returns current pointer position
    # source.seek(offset, whence) - // offset - position of r/w pointer of the file
    # // whence values: 0/1/2 - seek pointer from current/starting/ending position of the file

'''
    print("Iteration " + str(iteration_count))
    print(str(tape_1_curr))
    print(str(tape_2_curr))
'''

'''
    def merge(tape_1_path: str, tape_2_path: str, output_path: str, tape_start_position=0):
        print()
        iteration_count = 1
        with open(tape_1_path, "r+") as a:
            with open(tape_2_path, "r+") as b:
                with open(output_path, "w") as o:
                    if tape_start_position:
                        b.seek(tape_start_position, 0)
                    tape_1_pos = a.tell()
                    tape_2_pos = b.tell()
                    tape_1_curr = PolyphaseSort.read_number(a)
                    tape_2_curr = PolyphaseSort.read_number(b)
                    while tape_1_curr or tape_2_curr:
                        if tape_1_curr == "N":
                            PolyphaseSort.adjust_pointer(b, tape_2_pos)
                            PolyphaseSort.copy_rest(b, o)
                        elif tape_2_curr == "N":
                            PolyphaseSort.adjust_pointer(a, tape_1_pos)
                            PolyphaseSort.copy_rest(a, o)
                        else:
                            tape_1_curr = int(tape_1_curr)
                            tape_2_curr = int(tape_2_curr)
                            tape_1_prev = tape_1_curr
                            tape_2_prev = tape_2_curr
                            while tape_1_curr >= tape_1_prev and tape_2_curr >= tape_2_prev:
                                if tape_1_curr < tape_2_curr:
                                    o.write(str(tape_1_curr) + " ")
                                    PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                    tape_1_pos = a.tell()
                                else:
                                    o.write(str(tape_2_curr) + " ")
                                    PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                    tape_2_pos = b.tell()

                                print("Iteration " + str(iteration_count))
                                print(str(tape_1_curr))
                                print(str(tape_2_curr))

                                iteration_count += 1
                                tape_1_prev = tape_1_curr
                                tape_2_prev = tape_2_curr
                                tape_1_curr = PolyphaseSort.read_number(a)
                                tape_2_curr = PolyphaseSort.read_number(b)

                                if tape_1_curr == "N" or tape_1_curr == "":
                                    break
                                elif tape_2_curr == "N" or tape_2_curr == "":
                                    break
                                else:
                                    tape_1_curr = int(tape_1_curr)
                                    tape_2_curr = int(tape_2_curr)
                            if tape_1_curr < tape_1_prev and tape_2_curr >= tape_2_prev:
                                PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                PolyphaseSort.copy_rest(b, o)
                            elif tape_1_curr >= tape_1_prev and tape_2_curr < tape_2_prev:
                                PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                PolyphaseSort.copy_rest(a, o)

                        tape_1_curr = PolyphaseSort.read_number(a)
                        tape_2_curr = PolyphaseSort.read_number(b)
'''

'''
        with open(tape_1_path, "r+") as a:
            with open(tape_2_path, "r+") as b:
                with open(output_path, "w") as o:
                    if tape_start_position:
                        b.seek(tape_start_position, 0)
                    tape_1_pos, tape_2_pos = a.tell(), b.tell()
                    tape_1_curr, tape_2_curr = PolyphaseSort.read_number(a), PolyphaseSort.read_number(b)
                    if not tape_1_curr or not tape_2_curr:
                        print("Sequence is sorted")
                        return
                    else:
                        if tape_1_curr == "N":
                            PolyphaseSort.adjust_pointer(b, tape_2_pos)
                            PolyphaseSort.copy_rest(b, o)
                        elif tape_2_curr == "N":
                            PolyphaseSort.adjust_pointer(a, tape_1_pos)
                            PolyphaseSort.copy_rest(a, o)
                        else:
                            tape_1_curr = int(tape_1_curr)
                            tape_2_curr = int(tape_2_curr)
                            tape_1_prev = tape_1_curr
                            tape_2_prev = tape_2_curr
                            while tape_1_curr and tape_2_curr:
                                if tape_1_curr != "N" and tape_2_curr != "N":
                                    while tape_1_curr >= tape_1_prev and tape_2_curr >= tape_2_prev:
                                        if tape_1_curr < tape_2_curr:
                                            o.write(str(tape_1_curr) + " ")
                                            PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                            tape_1_pos = a.tell()
                                        else:
                                            o.write(str(tape_2_curr) + " ")
                                            PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                            tape_2_pos = b.tell()
                                        tape_1_prev = tape_1_curr
                                        tape_2_prev = tape_2_curr

                                        tape_1_curr, tape_2_curr = PolyphaseSort.read_number(a), PolyphaseSort.read_number(b)
                                        if tape_1_curr and tape_2_curr and tape_1_curr != 'N' and tape_2_curr != 'N':
                                            tape_1_curr = int(tape_1_curr)
                                            tape_2_curr = int(tape_2_curr)
                                        else:
                                            break
                                    if not tape_1_curr or tape_1_curr == "N":
                                        break
                                    elif not tape_2_curr or tape_2_curr == "N":
                                        break
                                    elif tape_1_curr < tape_1_prev:
                                        PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                        PolyphaseSort.copy_rest(b, o)
                                        tape_1_pos, tape_2_pos = a.tell(), b.tell()
                                        tape_2_curr = int(PolyphaseSort.read_number(b))
                                        tape_2_prev = tape_2_curr
                                        tape_1_prev = tape_1_curr
                                    elif tape_2_curr < tape_2_prev:
                                        PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                        PolyphaseSort.copy_rest(a, o)
                                        tape_1_pos, tape_2_pos = a.tell(), b.tell()
                                        tape_1_curr = int(PolyphaseSort.read_number(a))
                                        tape_1_prev = tape_1_curr
                                        tape_2_prev = tape_2_curr
                                else:
                                    while tape_1_curr and tape_2_curr:
                                        if tape_1_curr == "N":
                                            PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                            PolyphaseSort.copy_rest(b, o)
                                            tape_2_pos = b.tell()
                                        elif tape_2_curr == "N":
                                            PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                            PolyphaseSort.copy_rest(a, o)
                                            tape_1_pos = a.tell()
                                        tape_1_curr, tape_2_curr = PolyphaseSort.read_number(a), PolyphaseSort.read_number(b)
                                    if not tape_1_curr:
                                        PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                    else:
                                        PolyphaseSort.adjust_pointer(a, tape_1_pos)
                            if not tape_1_curr:
                                PolyphaseSort.adjust_pointer(b, tape_2_pos)
                            else:
                                PolyphaseSort.adjust_pointer(a, tape_1_pos)
'''

'''
print("source.txt: ")
    PolyphaseSort.initial_distribution("source.txt", "0.txt", "1.txt")
    PolyphaseSort.optimize_to_fibonacci()
    end_time = time.time()
    print("Total time: " + str(end_time - start_time) + " seconds")
'''

'''
                    while tape_1_curr and tape_2_curr:
                        while (tape_1_curr == "N" and tape_2_curr != "") or (tape_2_curr == "N" and tape_1_curr != ""):
                            if tape_1_curr == "N":
                                PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                PolyphaseSort.copy_rest(b, o)
                                PolyphaseSort.read_number(b)
                                tape_1_pos, tape_2_pos = a.tell(), b.tell()
                                tape_2_curr = PolyphaseSort.read_number(b)
                                tape_1_curr = PolyphaseSort.read_number(a)
                            elif tape_2_curr == "N":
                                PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                PolyphaseSort.copy_rest(a, o)
                                tape_1_pos, tape_2_pos = a.tell(), b.tell()
                                tape_1_curr = PolyphaseSort.read_number(a)
                                tape_2_curr = PolyphaseSort.read_number(b)
                        if tape_1_curr == "N" and tape_2_curr == "":
                            b.truncate(0)
                            PolyphaseSort.merge(output_path, tape_1_path, tape_2_path, tape_1_pos)
                        elif tape_2_curr == "N" and tape_1_curr == "":
                            a.truncate(0)
                            PolyphaseSort.merge(output_path, tape_2_path, tape_1_path, tape_2_pos)
                        else:
                            tape_1_curr, tape_2_curr = int(tape_1_curr), int(tape_2_curr)
                            tape_1_prev, tape_2_prev = tape_1_curr, tape_2_curr
                            while tape_1_curr >= tape_1_prev and tape_2_curr >= tape_2_prev:
                                tape_1_curr, tape_2_curr = int(tape_1_curr), int(tape_2_curr)
                                if tape_1_curr < tape_2_curr:
                                    o.write(str(tape_1_curr) + " ")
                                    PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                else:
                                    o.write(str(tape_2_curr) + " ")
                                    PolyphaseSort.adjust_pointer(a, tape_1_pos)

                                tape_1_pos, tape_2_pos = a.tell(), b.tell()
                                tape_1_prev, tape_2_prev = tape_1_curr, tape_2_curr
                                tape_1_curr, tape_2_curr = PolyphaseSort.read_number(a), PolyphaseSort.read_number(b)

                                if not tape_1_curr or not tape_2_curr or tape_1_curr == "N" or tape_2_curr == "N":
                                    break
                                else:
                                    tape_1_curr, tape_2_curr = int(tape_1_curr), int(tape_2_curr)
'''

'''
                    while tape_1_curr and tape_2_curr and tape_1_curr != "N" and tape_2_curr != "N":
                        tape_1_curr, tape_2_curr = int(tape_1_curr), int(tape_2_curr)
                        tape_1_prev, tape_2_prev = tape_1_curr, tape_2_curr
                        while tape_1_curr >= tape_1_prev and tape_2_curr >= tape_1_prev:
                            if tape_1_curr < tape_2_curr:
                                o.write(str(tape_1_curr) + " ")
                                PolyphaseSort.adjust_pointer(b, tape_2_pos)
                            else:
                                o.write(str(tape_2_curr) + " ")
                                PolyphaseSort.adjust_pointer(a, tape_1_pos)
                            tape_1_pos, tape_2_pos = a.tell(), b.tell()
                            tape_1_prev, tape_2_prev = tape_1_curr, tape_2_curr
                            tape_1_curr, tape_2_curr = PolyphaseSort.read_number(a), PolyphaseSort.read_number(b)
                            if not tape_1_curr or not tape_2_curr:
                                break
                            elif tape_1_curr == "N":
                                PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                PolyphaseSort.copy_rest(b, o)
                                tape_1_prev, tape_2_prev = tape_1_curr, tape_2_curr
                                tape_1_pos, tape_2_pos = a.tell(), b.tell()
                                tape_2_curr = PolyphaseSort.read_number(b)
                                break
                            elif tape_2_curr == "N":
                                PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                PolyphaseSort.copy_rest(a, o)
                                tape_1_prev, tape_2_prev = tape_1_curr, tape_2_curr
                                tape_1_pos, tape_2_pos = a.tell(), b.tell()
                                tape_2_curr = PolyphaseSort.read_number(b)
                                break
                            else:
                                tape_1_curr, tape_2_curr = int(tape_1_curr), int(tape_2_curr)
                                if tape_1_curr < tape_1_prev:
                                    PolyphaseSort.adjust_pointer(b, tape_2_pos)
                                    PolyphaseSort.copy_rest(b, o)
                                    tape_2_prev = tape_2_curr
                                    tape_2_pos = b.tell()
                                    tape_2_curr = PolyphaseSort.read_number(b)
                                    if tape_2_curr and tape_2_curr != "N":
                                        tape_2_curr = int(tape_2_curr)
                                    break
                                elif tape_2_curr < tape_2_prev:
                                    PolyphaseSort.adjust_pointer(a, tape_1_pos)
                                    PolyphaseSort.copy_rest(a, o)
                                    tape_1_prev = tape_1_curr
                                    tape_1_pos = a.tell()
                                    tape_1_curr = PolyphaseSort.read_number(a)
                                    if tape_1_curr and tape_1_curr != "N":
                                        tape_1_curr = int(tape_1_curr)
                                    break
                    if not tape_1_curr and not tape_2_curr:
                        print("Sequence is sorted")
                        return
                    elif not tape_1_curr and (tape_2_curr != "N" and int(tape_2_curr) >= int(tape_2_prev)):
                        PolyphaseSort.adjust_pointer(b, tape_2_pos)
                        PolyphaseSort.copy_rest(b, o)
                        # Fix zone
                        a.truncate(0)
                        position = b.tell()
                        a.close()
                        b.close()
                        o.close()
                        PolyphaseSort.merge(output_path, tape_2_path, tape_1_path, position)
                        return
                    elif not tape_2_curr and (tape_1_curr != "N" and int(tape_1_curr) >= int(tape_1_prev)):
                        PolyphaseSort.adjust_pointer(a, tape_1_pos)
                        PolyphaseSort.copy_rest(a, o)
                        # Fix zone
                        b.truncate(0)
                        position = a.tell()
                        a.close()
                        b.close()
                        o.close()
                        PolyphaseSort.merge(output_path, tape_1_path, tape_2_path, position)
                        return
                    elif not tape_1_curr and (tape_2_curr == "N" or int(tape_2_curr) < int(tape_2_prev)):
                        # Fix zone
                        position = b.tell()
                        a.truncate(0)
                        a.close()
                        b.close()
                        o.close()
                        PolyphaseSort.merge(output_path, tape_2_path, tape_1_path, position)
                        return
                    elif not tape_2_curr and (tape_1_curr == "N" or int(tape_1_curr) < int(tape_1_prev)):
                        # Fix zone
                        b.truncate(0)
                        position = a.tell()
                        a.close()
                        b.close()
                        o.close()
                        PolyphaseSort.merge(output_path, tape_1_path, tape_2_path, position)
                        return
                    while tape_1_curr == "N" or tape_2_curr == "N":
                        if tape_1_curr == "N" and tape_2_curr:
                            PolyphaseSort.adjust_pointer(b, tape_2_pos)
                            PolyphaseSort.copy_rest(b, o)
                            tape_1_pos, tape_2_pos = a.tell(), b.tell()
                            tape_1_curr = PolyphaseSort.read_number(a)
                            tape_2_curr = PolyphaseSort.read_number(b)
                            if not tape_2_curr:
                                # Fix zone
                                b.truncate(0)
                                position = a.tell()
                                a.close()
                                b.close()
                                o.close()
                                PolyphaseSort.merge(output_path, tape_1_path, tape_2_path, position)
                                return
                            elif not tape_1_curr:
                                # Fix zone
                                a.truncate(0)
                                position = b.tell()
                                a.close()
                                b.close()
                                o.close()
                                PolyphaseSort.merge(output_path, tape_2_path, tape_1_path, position)
                                return
                        elif tape_2_curr == "N" and tape_1_curr:
                            PolyphaseSort.adjust_pointer(a, tape_1_pos)
                            PolyphaseSort.copy_rest(a, o)
                            tape_1_pos, tape_2_pos = a.tell(), b.tell()
                            tape_2_curr = PolyphaseSort.read_number(b)
                            tape_1_curr = PolyphaseSort.read_number(a)
                            if not tape_1_curr:
                                # Fix zone
                                a.truncate(0)
                                position = b.tell()
                                a.close()
                                b.close()
                                o.close()
                                PolyphaseSort.merge(output_path, tape_2_path, tape_1_path, position)
                                return
                            elif not tape_2_curr:
                                # Fix zone
                                b.truncate(0)
                                position = a.tell()
                                a.close()
                                b.close()
                                o.close()
                                PolyphaseSort.merge(output_path, tape_1_path, tape_2_path, position)
                                return


'''