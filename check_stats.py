import re

content = open('hairstyles_upgrade.html').read()
if "this.stats.power += (this.stats.deltoidSize || 0)" in content:
    print("Combat logic correctly implemented.")
else:
    print("Combat logic missing.")

if "let effPow = playerStats.power +" in content:
    print("UI logic correctly implemented.")
else:
    print("UI logic missing.")
