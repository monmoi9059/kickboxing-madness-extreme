import re
with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Let's find how leg width or muscle size is drawn
matches = re.finditer(r'leg|width', content, re.IGNORECASE)
for m in list(matches)[:10]:
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 50)
    print(content[start:end])
