import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Make sure HUD displays the ACTUAL effective stats including muscle bonuses.
# Function: updateGymUI()
# Find:
# document.getElementById('my-hp').textContent = playerStats.maxHp;
# document.getElementById('my-pow').textContent = playerStats.power;
# document.getElementById('my-def').textContent = playerStats.defense;
# document.getElementById('my-stam').textContent = playerStats.maxStamina;

target = """            document.getElementById('my-hp').textContent = playerStats.maxHp;
            document.getElementById('my-pow').textContent = playerStats.power;
            document.getElementById('my-def').textContent = playerStats.defense;
            document.getElementById('my-stam').textContent = playerStats.maxStamina;"""

new_hud = """            // Calculate effective stats for UI
            let effHp = playerStats.maxHp + (playerStats.neckGirth || 0)*2 + (playerStats.chinSize || 0)*2;
            let effPow = playerStats.power + (playerStats.deltoidSize || 0)*0.5;
            let effDef = playerStats.defense + (playerStats.forearmSize || 0)*0.5 + (playerStats.chinSize || 0)*0.5;
            let effStam = playerStats.maxStamina + (playerStats.thighSize || 0)*2;

            document.getElementById('my-hp').textContent = effHp;
            document.getElementById('my-pow').textContent = Math.floor(effPow);
            document.getElementById('my-def').textContent = Math.floor(effDef);
            document.getElementById('my-stam').textContent = effStam;"""

content = content.replace(target, new_hud)

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)

print("HUD updated to reflect actual stats!")
