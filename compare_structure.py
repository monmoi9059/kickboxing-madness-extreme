import sys

def get_structure(file):
    with open(file, "r") as f:
        content = f.read()
    if file.endswith(".html"):
        content = content.split("<script>")[1].split("</script>")[0]

    lines = content.split('\n')
    for i, l in enumerate(lines):
        if "update(" in l or "draw(" in l or "function checkCollisions" in l or "class Fighter" in l or "class Particle" in l:
            print(f"{i}: {l.strip()}")

print("=== test.js ===")
get_structure("test.js")
print("\n=== html ===")
get_structure("hairstyles_upgrade.html")
