with open('EFLTG.html', 'r') as f:
    content = f.read()

# Let's see the end of the file
print("--- END OF FILE ---")
print(content[-500:])

# The file seems to have a complete second copy appended!
# Let's truncate the file at the end of the first copy.
