import re

with open("test.js", "r") as f:
    content = f.read()

# Make appearances really distinct. Add more variety to sizes.
old_code = """                        newOpp.appearance = {
                            h: 0.8 + Math.random() * 0.4,
                            w: 0.8 + Math.random() * 0.4,"""

new_code = """                        newOpp.appearance = {
                            h: 0.7 + Math.random() * 0.6, // Wider range of heights
                            w: 0.7 + Math.random() * 0.7, // Wider range of widths"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("test.js", "w") as f:
        f.write(content)
    print("Patched appearance successfully!")
else:
    print("Could not find old_code for appearance.")
