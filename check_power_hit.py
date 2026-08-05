with open("test.js", "r") as f:
    lines = f.read().split('\n')

# Where is `isPowerAttack` assigned?
assigned = False
for i, l in enumerate(lines):
    if "isPowerAttack" in l and "=" in l:
        print(f"{i}: {l.strip()}")
        assigned = True

if not assigned:
    print("isPowerAttack is NEVER assigned!")
