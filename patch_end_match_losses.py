import re

with open("test.js", "r") as f:
    content = f.read()

# Add losses counter to playerStats.
old_code = """        let playerStats = {
            hp: 100, maxHp: 100,
            power: 10,
            defense: 5,
            stamina: 100, maxStamina: 100, staminaRegen: 15, speedBonus: 0,
            neckGirth: 0, deltoidSize: 0, forearmSize: 0, thighSize: 0, calfSize: 0, chinSize: 0,
            money: 0, rank: 0,"""

new_code = """        let playerStats = {
            hp: 100, maxHp: 100,
            power: 10,
            defense: 5,
            stamina: 100, maxStamina: 100, staminaRegen: 15, speedBonus: 0,
            neckGirth: 0, deltoidSize: 0, forearmSize: 0, thighSize: 0, calfSize: 0, chinSize: 0,
            money: 0, rank: 0, losses: 0,"""

if old_code in content:
    content = content.replace(old_code, new_code)
else:
    print("Could not find old_code for stats.")

# Reset losses on win, increment on loss
old_code_end = """                if (playerWon) {
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
                    currentOpponentChoices = [];"""

new_code_end = """                if (playerWon) {
                    const opp = currentOpponentChoices[selectedOpponentIndex];
                    playerStats.money += opp.reward;
                    playerStats.rank++;
                    playerStats.losses = 0; // Reset losses on win
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
                    playerStats.losses = (playerStats.losses || 0) + 1; // Increment losses
                    currentOpponentChoices = [];"""

if old_code_end in content:
    content = content.replace(old_code_end, new_code_end)
    with open("test.js", "w") as f:
        f.write(content)
    print("Patched end match for losses successfully!")
else:
    print("Could not find old_code for end match losses.")
