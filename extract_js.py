import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# We need to find the main script block
match = re.search(r"<script>(.*?)</script>", content, re.DOTALL)
if match:
    with open('test.js', 'w') as f:
        f.write(match.group(1))
else:
    print("No script found")
