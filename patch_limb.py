import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Fix angle math for correct IK
old_math = '''                    let cosAngle = (dist*dist) / (2 * l * dist);
                    if (cosAngle > 1) cosAngle = 1;
                    let angle = Math.acos(cosAngle);'''

new_math = '''                    let cosAngle = dist / (2 * l);
                    if (cosAngle > 1) cosAngle = 1;
                    let angle = Math.acos(cosAngle);'''

content = content.replace(old_math, new_math)

# Fix extension logic in animations by dynamically multiplying attack lengths
# I'll look for where targetT is built in jab/cross etc and inject extension based on limbMod.
# First, let's look at the attack definitions.
