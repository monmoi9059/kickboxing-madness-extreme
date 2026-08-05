import sys
with open("hairstyles_upgrade.html", "r") as f:
    content = f.read()

scriptContent = content.split("<script>")[1].split("</script>")[0]
lines = scriptContent.split('\n')

open_count = 0
for i, line in enumerate(lines):
    for c in line:
        if c == '{': open_count += 1
        elif c == '}': open_count -= 1
    if i == 937: print(f"Line 937 brace count: {open_count}")
    if i == 938: print(f"Line 938 brace count: {open_count}")

# Wait, the final brace count being 1 means we are missing a closing brace somewhere?
# Or wait, there's an EXTRA open brace?
# Because 1 means we left 1 block open at the very end of script.
