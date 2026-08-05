import re
with open("hairstyles_upgrade.html", "r") as f:
    content = f.read()

# Wait, if `Class Fighter at 380`, then the first `let targetT` at 328 is BEFORE Fighter class!
# Let's inspect around 328.
