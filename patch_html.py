import re

with open("hairstyles_upgrade.html", "r") as f:
    content = f.read()

# Apply the wins and losses tracking to HTML file
old_code_stats = "money: 0, rank: 0,"
new_code_stats = "money: 0, rank: 0, losses: 0, wins: 0,"

if old_code_stats in content:
    content = content.replace(old_code_stats, new_code_stats)

old_code_end = """                if (playerWon) {
                    const opp = currentOpponentChoices[selectedOpponentIndex];
                    playerStats.money += opp.reward;
                    playerStats.rank++;
                    currentOpponentChoices = []; // Force new choices
                }"""

new_code_end = """                if (playerWon) {
                    const opp = currentOpponentChoices[selectedOpponentIndex];
                    playerStats.money += opp.reward;
                    playerStats.rank++;
                    playerStats.wins = (playerStats.wins || 0) + 1; // Track wins
                    playerStats.losses = 0; // Reset losses on win
                    currentOpponentChoices = []; // Force new choices
                } else {
                    playerStats.rank = Math.max(0, playerStats.rank - 1);
                    playerStats.losses = (playerStats.losses || 0) + 1; // Increment losses
                    currentOpponentChoices = [];
                }"""

if old_code_end in content:
    content = content.replace(old_code_end, new_code_end)

# Apply the opponents diff scaling and randomness
old_code_opp = """                    for (let i = 0; i < numChoices; i++) {
                        const diff = 0.7 + (Math.random() * 0.6);
                        let newOpp = JSON.parse(JSON.stringify(baseOpp));"""

new_code_opp = """                    for (let i = 0; i < numChoices; i++) {
                        let diff = 0.7 + (Math.random() * 0.6);
                        if (playerStats.losses && playerStats.losses > 0) {
                            diff *= Math.pow(0.8, playerStats.losses); // Weaker opponents and lower rewards if lost
                        }

                        let randBaseIndex = Math.floor(Math.random() * opponents.length);
                        let newOpp = JSON.parse(JSON.stringify(opponents[randBaseIndex]));"""

if old_code_opp in content:
    content = content.replace(old_code_opp, new_code_opp)

# Apply appearances to HTML file
old_code_app = """                        newOpp.appearance = {
                            h: 0.8 + Math.random() * 0.4,
                            w: 0.8 + Math.random() * 0.4,"""
new_code_app = """                        newOpp.appearance = {
                            h: 0.7 + Math.random() * 0.6,
                            w: 0.7 + Math.random() * 0.7,"""

if old_code_app in content:
    content = content.replace(old_code_app, new_code_app)

with open("hairstyles_upgrade.html", "w") as f:
    f.write(content)
print("Patched HTML successfully!")
