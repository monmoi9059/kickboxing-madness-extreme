import re

with open("test.js", "r") as f:
    content = f.read()

old_code = "money: 0, rank: 0, losses: 0,"
new_code = "money: 0, rank: 0, losses: 0, wins: 0,"

if old_code in content:
    content = content.replace(old_code, new_code)

old_code2 = """                    playerStats.rank++;
                    playerStats.losses = 0; // Reset losses on win"""
new_code2 = """                    playerStats.rank++;
                    playerStats.wins = (playerStats.wins || 0) + 1; // Track wins
                    playerStats.losses = 0; // Reset losses on win"""

if old_code2 in content:
    content = content.replace(old_code2, new_code2)

with open("test.js", "w") as f:
    f.write(content)
print("Patched wins successfully!")
