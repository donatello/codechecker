
# utility function to write a string to a file.
def write_to_disk(text, filename):
    f = file(filename, "w")
    f.write(text)
    f.close()
