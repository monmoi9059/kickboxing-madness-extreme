import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

target = "                // Power is amplified by weight.\n                this.stats.power = this.stats.power * wScale;"

new_logic = """                // Apply Muscle Bonus Stats
                this.stats.maxHp += (this.stats.neckGirth || 0) * 2;
                this.stats.maxHp += (this.stats.chinSize || 0) * 2;
                this.stats.hp = this.stats.maxHp;

                this.stats.power += (this.stats.deltoidSize || 0) * 0.5;
                this.stats.defense += (this.stats.forearmSize || 0) * 0.5;
                this.stats.defense += (this.stats.chinSize || 0) * 0.5;

                this.stats.maxStamina += (this.stats.thighSize || 0) * 2;
                this.stats.stamina = this.stats.maxStamina;

                this.speed += (this.stats.calfSize || 0) * 0.2;

                // Power is amplified by weight.
                this.stats.power = this.stats.power * wScale;"""

content = content.replace(target, new_logic)

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)

print("Patched Fighter constructor to apply muscle upgrades to combat stats!")
