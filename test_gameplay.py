import re

with open('EFLTG.html', 'r') as f:
    content = f.read()

# Make sure there is only one Fighter class definition now? No, there are still two.
# Wait, why are there two Fighter classes?
# Maybe one is for preview (Gym) and one is for the actual combat screen?
# Let's check how many times "class Fighter" appears.

matches = [m.start() for m in re.finditer(r"class Fighter", content)]
print(matches)
