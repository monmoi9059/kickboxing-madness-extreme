import re

with open("test.js", "r") as f:
    content = f.read()

# Notice that inside the loop, the stats are using `baseOpp` instead of the newly randomly selected base opponent or `newOpp`!!
old_code = """                        newOpp.stats.maxHp = Math.floor(baseOpp.stats.maxHp * diff * cycleMulti * hpMult);
                        newOpp.stats.power = Math.floor(baseOpp.stats.power * diff * cycleMulti * powMult);
                        newOpp.stats.defense = Math.floor(baseOpp.stats.defense * diff * cycleMulti * defMult);
                        newOpp.stats.maxStamina = Math.floor(baseOpp.stats.maxStamina * diff * cycleMulti * stamMult);
                        newOpp.stats.staminaRegen = Math.floor(baseOpp.stats.staminaRegen * diff * (1 + (cycleMulti-1)*0.1) * regenMult);"""

new_code = """                        newOpp.stats.maxHp = Math.floor(newOpp.stats.maxHp * diff * cycleMulti * hpMult);
                        newOpp.stats.power = Math.floor(newOpp.stats.power * diff * cycleMulti * powMult);
                        newOpp.stats.defense = Math.floor(newOpp.stats.defense * diff * cycleMulti * defMult);
                        newOpp.stats.maxStamina = Math.floor(newOpp.stats.maxStamina * diff * cycleMulti * stamMult);
                        newOpp.stats.staminaRegen = Math.floor(newOpp.stats.staminaRegen * diff * (1 + (cycleMulti-1)*0.1) * regenMult);"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("test.js", "w") as f:
        f.write(content)
    print("Patched random opponents bugs successfully!")
else:
    print("Could not find old_code for random opponents bugs.")
