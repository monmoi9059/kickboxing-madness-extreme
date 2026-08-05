import re

with open("test.js", "r") as f:
    content = f.read()

# We want to change what happens when the player loses.
old_code = """                if (playerWon) {
                    const opp = currentOpponentChoices[selectedOpponentIndex];
                    playerStats.money += opp.reward;
                    playerStats.rank++;
                    currentOpponentChoices = [];
                    document.getElementById('result-title').textContent = "YOU WON!";
                    document.getElementById('result-title').className = "text-5xl font-black mb-4 text-green-500";
                    document.getElementById('result-money').textContent = opp.reward;

                    document.getElementById('result-screen').classList.remove('hidden');
                } else {
                    const opp = currentOpponentChoices[selectedOpponentIndex];
                    const loserBonus = Math.floor(opp.reward * 0.25); // Give 25% of reward for losing
                    playerStats.money += loserBonus;

                    document.getElementById('result-title').textContent = "KNOCKED OUT";
                    document.getElementById('result-title').className = "text-5xl font-black mb-4 text-red-500";
                    document.getElementById('result-money').textContent = loserBonus;
                    document.getElementById('result-screen').classList.remove('hidden');
                }"""

new_code = """                if (playerWon) {
                    const opp = currentOpponentChoices[selectedOpponentIndex];
                    playerStats.money += opp.reward;
                    playerStats.rank++;
                    currentOpponentChoices = [];
                    document.getElementById('result-title').textContent = "YOU WON!";
                    document.getElementById('result-title').className = "text-5xl font-black mb-4 text-green-500";
                    document.getElementById('result-money').textContent = opp.reward;

                    document.getElementById('result-screen').classList.remove('hidden');
                } else {
                    const opp = currentOpponentChoices[selectedOpponentIndex];
                    const loserBonus = Math.floor(opp.reward * 0.25); // Give 25% of reward for losing
                    playerStats.money += loserBonus;
                    playerStats.rank = Math.max(0, playerStats.rank - 1);
                    currentOpponentChoices = [];

                    document.getElementById('result-title').textContent = "KNOCKED OUT";
                    document.getElementById('result-title').className = "text-5xl font-black mb-4 text-red-500";
                    document.getElementById('result-money').textContent = loserBonus;
                    document.getElementById('result-screen').classList.remove('hidden');
                }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("test.js", "w") as f:
        f.write(content)
    print("Patched end match successfully!")
else:
    print("Could not find old_code for end match.")
