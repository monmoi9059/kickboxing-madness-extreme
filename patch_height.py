import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

old_botched = '''                        if (key === 'botchedSurgery') {
                            // Increases limb length drastically, reduces stamina
                            playerStats.appearance.limbLengthMod = (playerStats.appearance.limbLengthMod || 0) + 20;
                            playerStats.maxStamina = Math.max(10, playerStats.maxStamina - 20); // Penalty
                            if (playerStats.stamina > playerStats.maxStamina) playerStats.stamina = playerStats.maxStamina;
                        }'''

new_botched = '''                        if (key === 'botchedSurgery') {
                            // Increases limb length drastically, reduces stamina, increases height
                            playerStats.appearance.limbLengthMod = (playerStats.appearance.limbLengthMod || 0) + 20;
                            playerStats.appearance.h = (playerStats.appearance.h || 1) + 0.05; // Make player taller
                            playerStats.maxStamina = Math.max(10, playerStats.maxStamina - 20); // Penalty
                            if (playerStats.stamina > playerStats.maxStamina) playerStats.stamina = playerStats.maxStamina;
                        }'''

content = content.replace(old_botched, new_botched)

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
