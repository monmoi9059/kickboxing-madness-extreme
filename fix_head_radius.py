import re

with open('EFLTG.html', 'r') as f:
    content = f.read()

# I messed up moving headRadius properly!
# Let's fix headRadius definition in the draw method again.
neck_start = content.find("// Draw Neck")
if neck_start != -1:
    new_code = """// Draw Neck
                const headRadius = 16 * ((h+w)/2);"""
    content = content.replace("// Draw Neck", new_code, 1)
    with open('EFLTG.html', 'w') as f:
        f.write(content)
    print("Fixed headRadius!")
else:
    print("Could not find insertion point.")
