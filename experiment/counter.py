def count(file_path):
    file_path += ".rel"
    # Initialize a variable to count lines
    line_count = 0

    # Open the file and read line by line
    with open(file_path, "r") as file:
        for line in file:
            line_count += 1

    million = 1000000
    line_count /= million

    # Print the total number of lines
    print(f"\n Total number of lines in the file: {line_count} (* 10^6)")

    return line_count
