import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

old_gym = '''            if (playerStats.rank < opponents.length) {
                if (currentOpponentChoices.length === 0) {
                    let baseOpp = opponents[playerStats.rank];
                    const numChoices = Math.floor(Math.random() * 3) + 3; // 3 to 5
                    for (let i = 0; i < numChoices; i++) {
                        const diff = 0.7 + (Math.random() * 0.6);
                        let newOpp = JSON.parse(JSON.stringify(baseOpp));
                        const diffName = diff < 0.9 ? "Weak " : (diff > 1.1 ? "Elite " : "");
                        newOpp.name = `${diffName}${newOpp.name}`;
                        newOpp.stats.maxHp = Math.floor(newOpp.stats.maxHp * diff);
                        newOpp.stats.power = Math.floor(newOpp.stats.power * diff);
                        newOpp.stats.defense = Math.floor(newOpp.stats.defense * diff);
                        newOpp.stats.maxStamina = Math.floor(newOpp.stats.maxStamina * diff);
                        newOpp.stats.staminaRegen = Math.floor(newOpp.stats.staminaRegen * diff);
                        newOpp.reward = Math.floor(newOpp.reward * diff);
                        newOpp.difficultyMult = diff;
                        currentOpponentChoices.push(newOpp);
                    }
                    currentOpponentChoices.sort((a, b) => a.reward - b.reward);
                    selectedOpponentIndex = 0;
                }
                renderOpponentChoices();
            }'''

new_gym = '''            if (true) {
                if (currentOpponentChoices.length === 0) {
                    let baseIndex = playerStats.rank % opponents.length;
                    let cycleMulti = 1 + Math.floor(playerStats.rank / opponents.length) * 0.5;
                    let baseOpp = opponents[baseIndex];
                    const numChoices = Math.floor(Math.random() * 3) + 3; // 3 to 5
                    for (let i = 0; i < numChoices; i++) {
                        const diff = 0.7 + (Math.random() * 0.6);
                        let newOpp = JSON.parse(JSON.stringify(baseOpp));
                        const diffName = diff < 0.9 ? "Weak " : (diff > 1.1 ? "Elite " : "");
                        newOpp.name = `${diffName}${newOpp.name} ${playerStats.rank >= opponents.length ? "V" + (Math.floor(playerStats.rank / opponents.length) + 1) : ""}`.trim();
                        newOpp.stats.maxHp = Math.floor(newOpp.stats.maxHp * diff * cycleMulti);
                        newOpp.stats.power = Math.floor(newOpp.stats.power * diff * cycleMulti);
                        newOpp.stats.defense = Math.floor(newOpp.stats.defense * diff * cycleMulti);
                        newOpp.stats.maxStamina = Math.floor(newOpp.stats.maxStamina * diff * cycleMulti);
                        newOpp.stats.staminaRegen = Math.floor(newOpp.stats.staminaRegen * diff * (1 + (cycleMulti-1)*0.1));
                        newOpp.reward = Math.floor(newOpp.reward * diff * cycleMulti);
                        newOpp.difficultyMult = diff;
                        currentOpponentChoices.push(newOpp);
                    }
                    currentOpponentChoices.sort((a, b) => a.reward - b.reward);
                    selectedOpponentIndex = 0;
                }
                renderOpponentChoices();
            }'''

content = content.replace(old_gym, new_gym)

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
