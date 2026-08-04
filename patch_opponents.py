import re

with open("hairstyles_upgrade.html", "r") as f:
    content = f.read()

# We want to replace the inside of the for loop.
old_code = """                    const numChoices = Math.floor(Math.random() * 3) + 3; // 3 to 5
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
                    }"""

new_code = """                    const numChoices = Math.floor(Math.random() * 3) + 3; // 3 to 5
                    const fNames = ["Big", "Slippery", "Iron", "Crazy", "Fast", "Brutal", "Magic", "Lethal", "Smash", "Furious", "Venom", "Thunder", "Shadow", "Bone", "Grim", "Wild"];
                    const lNames = ["Joe", "Mike", "Pete", "Dave", "Steve", "Bob", "Ray", "Tyson", "Lee", "Ali", "Crusher", "Reaper", "Maniac", "Fist", "Hawk", "Wolf"];
                    const skins = ['#fcd34d', '#b45309', '#fca5a5', '#cbd5e1', '#111827', '#e2e8f0', '#8b5a2b', '#ffdead'];
                    const hairColors = ['#000000', '#fbbf24', '#dc2626', '#ffffff', '#451a03', '#9ca3af', '#f59e0b'];
                    const hStyles = ['short', 'bald', 'mohawk', 'afro', 'spiky'];
                    const randColor = () => '#' + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0');
                    const descs = ["A tough challenger.", "Looking for a fight.", "A dangerous striker.", "Known for stamina.", "Has a strong chin.", "Quick on their feet.", "A rising star.", "Hard-hitting brawler.", "Technically sound fighter.", "Wild and unpredictable."];

                    for (let i = 0; i < numChoices; i++) {
                        const diff = 0.7 + (Math.random() * 0.6);
                        let newOpp = JSON.parse(JSON.stringify(baseOpp));

                        const rName = fNames[Math.floor(Math.random() * fNames.length)] + " " + lNames[Math.floor(Math.random() * lNames.length)];
                        const diffName = diff < 0.9 ? "Weak " : (diff > 1.1 ? "Elite " : "");
                        newOpp.name = `${diffName}${rName} ${playerStats.rank >= opponents.length ? "V" + (Math.floor(playerStats.rank / opponents.length) + 1) : ""}`.trim();
                        newOpp.desc = descs[Math.floor(Math.random() * descs.length)];

                        let hpMult = 1, powMult = 1, defMult = 1, stamMult = 1, regenMult = 1;
                        let r = Math.random();
                        if (r < 0.25) { // Tank
                            hpMult = 1.3; defMult = 1.3; powMult = 0.8; stamMult = 0.9;
                        } else if (r < 0.5) { // Glass Cannon
                            hpMult = 0.7; defMult = 0.7; powMult = 1.4; stamMult = 0.9;
                        } else if (r < 0.75) { // Cardio machine
                            hpMult = 0.9; defMult = 0.9; powMult = 0.8; stamMult = 1.3; regenMult = 1.3;
                        } // else Balanced (1.0)

                        // Add some noise
                        hpMult *= 0.9 + Math.random() * 0.2;
                        powMult *= 0.9 + Math.random() * 0.2;
                        defMult *= 0.9 + Math.random() * 0.2;
                        stamMult *= 0.9 + Math.random() * 0.2;
                        regenMult *= 0.9 + Math.random() * 0.2;

                        newOpp.stats.maxHp = Math.floor(baseOpp.stats.maxHp * diff * cycleMulti * hpMult);
                        newOpp.stats.power = Math.floor(baseOpp.stats.power * diff * cycleMulti * powMult);
                        newOpp.stats.defense = Math.floor(baseOpp.stats.defense * diff * cycleMulti * defMult);
                        newOpp.stats.maxStamina = Math.floor(baseOpp.stats.maxStamina * diff * cycleMulti * stamMult);
                        newOpp.stats.staminaRegen = Math.floor(baseOpp.stats.staminaRegen * diff * (1 + (cycleMulti-1)*0.1) * regenMult);

                        newOpp.appearance = {
                            h: 0.8 + Math.random() * 0.4,
                            w: 0.8 + Math.random() * 0.4,
                            skin: skins[Math.floor(Math.random() * skins.length)],
                            shorts: randColor(),
                            gloves: randColor(),
                            hairstyle: hStyles[Math.floor(Math.random() * hStyles.length)],
                            haircolor: hairColors[Math.floor(Math.random() * hairColors.length)]
                        };

                        newOpp.reward = Math.floor(newOpp.reward * diff * cycleMulti);
                        newOpp.difficultyMult = diff;
                        currentOpponentChoices.push(newOpp);
                    }"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("hairstyles_upgrade.html", "w") as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find old_code.")
