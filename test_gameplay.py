import re

with open('EFLTG.html', 'r') as f:
    content = f.read()

# Let's check how the combat logic uses the draw function, and make sure that the damage and collision boxes are aligned.
print("drawDetailedLimb found:", content.count("drawDetailedLimb"))
print("targetT logic found:", content.count("targetT"))
print("attackIntensity found:", content.count("attackIntensity"))
print("easeOutQuad found:", content.count("easeOutQuad"))
