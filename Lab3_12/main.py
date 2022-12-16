# This is a sample Python script.
import math
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import random
import linecache
import tkinter

DB_FILE_PATH = "db.txt"
INDEX_FILE_PATH = "dense_index.txt"
LZ = 178  # Bytes in record(approximation)
LK = 4  # Bytes in int(in task)
KZ = 100  # Number of rows(in task)
LB = 39*100  # Bytes in a block
number_of_lines = 100
window = tkinter.Tk()
window.title("My app")
result_field = tkinter.Label(text="Results will be displayed there!")
result_field.grid(row=6, column=0)


def build_index_file(db_file_path=DB_FILE_PATH):
    # Index file row = key_value; db_row_id; \n
    with open(INDEX_FILE_PATH, "w") as index_file:
        for i in range(0, KZ):
            with open(DB_FILE_PATH, "r") as file:
                for j, content in enumerate(file):
                    value = int(content.split(" ")[0])
                    if i == value:
                        index_file.write(str(i) + " " + str(j+1) + "\n")
    return i


def search(row_id=None):
    number_of_reads = 0
    try:
        if not row_id:
            primary_key = int(entry_input_field.get())
        else:
            primary_key = row_id
    except:
        result_field.configure(text=f"Incorrect format given!")
        return
    # Using binary search to find item
    upper_index = number_of_lines
    lower_index = 0
    while lower_index <= upper_index:
        middle_index = (upper_index + lower_index) // 2
        value = linecache.getline(INDEX_FILE_PATH, middle_index + 1)
        number_of_reads += 1
        if not value:
            result_field.configure(text=f"Item was not found! \n Number of reads: {str(number_of_reads)}")
            return "Item not found"
        if int(value.split(" ")[0]) == primary_key:
            result_field.configure(text=f"Row in DB was found! \n Row details: {linecache.getline(DB_FILE_PATH, int(value.split(' ')[1]))} \n Number of reads: {str(number_of_reads)}")
            return value
        elif middle_index < primary_key:
            lower_index = middle_index + 1
        else:
            upper_index = middle_index - 1
    result_field.configure(text=f"Item was not found! \n Number of reads: {str(number_of_reads)}")
    return "Item not found"


def add():
    global number_of_lines
    row = str(number_of_lines) + " " + " ".join(entry_input_field.get().split(" ")) + "\n"
    with open(DB_FILE_PATH, "a+") as file:
        file.write(row)
        file.close()
    with open(INDEX_FILE_PATH, "a+") as file1:
        file1.write(row.split(" ")[0] + " " + str(number_of_lines + 1) + "\n")
        file1.close()
    linecache.clearcache()
    number_of_lines += 1
    result_field.configure(text=f"Data was successfully added!")
    return


def update():
    try:
        global number_of_lines
        data = entry_input_field.get().split(" ")
        row_id = int(data[0])
        value = str(data[1])
        index_value = int(search(row_id).split(" ")[1].replace("\n", ""))
        with open(DB_FILE_PATH, "r+") as file1:
            lines = []
            for index, line in enumerate(file1):
                if index == index_value-1:
                    lines.append(str(row_id) + " " + value + "\n")
                else:
                    lines.append(line)
            file1.write("")
            file1.close()
        with open(DB_FILE_PATH, "w") as file1:
            file1.writelines(lines)
        print("DB file was successfully updated!")
        result_field.configure(text="DB file was successfully updated!")
        linecache.clearcache()
        return "Success!"
    except:
        result_field.configure(text="Incorrect format")


def delete():
    global number_of_lines
    try:
        row_id = int(entry_input_field.get())
        search_result = search(row_id).split(" ")
        index_value1 = int(search_result[0])
        index_value2 = int(search_result[1].replace("\n", ""))
        with open(INDEX_FILE_PATH, "r+") as file:
            lines = []
            for index, line in enumerate(file):
                if int(line.split(" ")[0]) == index_value1:
                    lines.append("")
                else:
                    lines.append(line)
            file.write("")
        with open(INDEX_FILE_PATH, "w") as file:
            file.writelines(lines)
        with open(DB_FILE_PATH, "r+") as file1:
            lines = []
            for index, line in enumerate(file1):
                if index == index_value2-1:
                    lines.append("\n")
                else:
                    lines.append(line)
            file1.write("")
        with open(DB_FILE_PATH, "w") as file1:
            file1.writelines(lines)
        print("Row was successfully deleted!")
        result_field.configure(text=f"Row was successfully deleted!")
        linecache.clearcache()
        number_of_lines -= 1
        return "Success!"
    except:
        result_field.configure(text=f"Incorrect format given or incorrect row!")
        return


# LZ - length of a record in file
# LK - size of a key
# KZ - number of records in file
# LB - size of a block
def generate_db_file():
    random_data = []
    letters = "abcdefghijklmnopqrstuvwxyz"
    for i in range(0, KZ):
        random_data.append((str(i)
                            + " "
                            + "".join([letters[random.randint(0, 25)] for j in range(0, LB//100 + 1)]))[0:(LB//100)-1]
                           + "\n")
    random.shuffle(random_data)

    with open(DB_FILE_PATH, "w") as file:
        for record in random_data:
            file.write(record)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    generate_db_file()
    number_of_lines = build_index_file() + 1
    add_label = tkinter.Label(text="Add element(format: string data without key)")
    delete_label = tkinter.Label(text="Delete element(format: key_value of element)")
    search_label = tkinter.Label(text="Search element(format: key_value of element)")
    update_label = tkinter.Label(text="Update element(format: key_value + string updated data separated by space)")
    entry_input_field = tkinter.Entry()
    add_button = tkinter.Button(text="Add", command=add)
    delete_button = tkinter.Button(text="Delete", command=delete)
    search_button = tkinter.Button(text="Search", command=search)
    update_button = tkinter.Button(text="Update", command=update)
    add_button.grid(row=1, column=1)
    add_label.grid(row=1, column=0)
    delete_button.grid(row=2, column=1)
    delete_label.grid(row=2, column=0)
    search_button.grid(row=3, column=1)
    search_label.grid(row=3, column=0)
    update_button.grid(row=4, column=1)
    update_label.grid(row=4, column=0)
    entry_input_field.grid(row=5, column=0)
    window.mainloop()
    '''
        Tests(does not work anymore because I rewrote application to tkinker, but you can still use values): 
        print(search(0))

        add("xlidspimnbcpztuazwtlnkjgxuygmqchuy")
        print(search(100, number_of_lines))
    
        add("xlidspimnbcpztuazwtlnkjgxuygmqchuy")
        print(search(109, number_of_lines))
    
        update(109, "abcdefghij")
        print(search(109, number_of_lines))
    
        delete(0)
        print(search(100, number_of_lines))
        print(search(109, number_of_lines))
    '''

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
