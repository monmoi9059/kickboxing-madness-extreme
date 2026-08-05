import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# I removed headRadius in my replacement snippet earlier.
# Let's add it right before it's first used (neck curve).
# Find "// Draw Neck"

hr_decl = "const headRadius = 16 * ((h+w)/2);"
target = "                // Draw Neck\n"
new_content = content.replace(target, target + "                " + hr_decl + "\n")

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(new_content)

print("Added headRadius!")
