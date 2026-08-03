import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Add speed to playerStats
content = content.replace("staminaRegen: 15,", "staminaRegen: 15, speedBonus: 0,")

# Add speed upgrade to upgradeCosts
content = content.replace(
'''            staminaRegen: { base: 50, mult: 1.5, name: "Cardio", val: 3 },
            botchedSurgery: { base: 200, mult: 2.0, name: "Botched Limb Lengthening (-Stamina)", val: 1 }''',
'''            staminaRegen: { base: 50, mult: 1.5, name: "Cardio", val: 3 },
            speedBonus: { base: 75, mult: 1.6, name: "Movement Speed (Leg Muscles)", val: 0.5 },
            botchedSurgery: { base: 200, mult: 2.0, name: "Botched Limb Lengthening (-Stamina)", val: 1 }'''
)

# Add speedBonus to upgradeLevels
content = content.replace(
'''        let upgradeLevels = { maxHp: 0, power: 0, defense: 0, maxStamina: 0, staminaRegen: 0, botchedSurgery: 0 };''',
'''        let upgradeLevels = { maxHp: 0, power: 0, defense: 0, maxStamina: 0, staminaRegen: 0, speedBonus: 0, botchedSurgery: 0 };'''
)

# Fighter initialisation: Apply speedBonus to this.speed
content = content.replace(
'''                this.speed = 4 * (1 / wScale) * (1 / ((hScale - 1) * 0.5 + 1));''',
'''                this.speed = (4 * (1 / wScale) * (1 / ((hScale - 1) * 0.5 + 1))) + (stats.speedBonus || 0);'''
)

# Apply speed upgrade in buy block
buy_logic_old = '''                        if (key === 'botchedSurgery') {
                            // Increases limb length drastically, reduces stamina
                            playerStats.appearance.limbLengthMod = (playerStats.appearance.limbLengthMod || 0) + 20;
                            playerStats.maxStamina = Math.max(10, playerStats.maxStamina - 20); // Penalty
                            if (playerStats.stamina > playerStats.maxStamina) playerStats.stamina = playerStats.maxStamina;
                        } else {
                            playerStats[key] += data.val;
                            if (key === 'maxHp') playerStats.hp = playerStats.maxHp;
                            if (key === 'maxStamina') playerStats.stamina = playerStats.maxStamina;
                        }'''

buy_logic_new = '''                        if (key === 'botchedSurgery') {
                            // Increases limb length drastically, reduces stamina
                            playerStats.appearance.limbLengthMod = (playerStats.appearance.limbLengthMod || 0) + 20;
                            playerStats.maxStamina = Math.max(10, playerStats.maxStamina - 20); // Penalty
                            if (playerStats.stamina > playerStats.maxStamina) playerStats.stamina = playerStats.maxStamina;
                        } else if (key === 'speedBonus') {
                            playerStats.speedBonus = (playerStats.speedBonus || 0) + data.val;
                        } else {
                            playerStats[key] += data.val;
                            if (key === 'maxHp') playerStats.hp = playerStats.maxHp;
                            if (key === 'maxStamina') playerStats.stamina = playerStats.maxStamina;
                        }'''

content = content.replace(buy_logic_old, buy_logic_new)

# Draw detailed leg thickness based on speedBonus
# Let's find the `drawDetailedLimb` calls for legs and increase width.
# width is `22 * w` for Front Leg and `20 * w` for Back Leg
draw_leg_old_f = '''drawDetailedLimb(t.fKnee, t.fFoot, 1, legLength, 22 * w, outline, skin, tattoo !== 'none');'''
draw_leg_new_f = '''let legW = 22 * w + (this.stats.speedBonus || 0) * 4;
                drawDetailedLimb(t.fKnee, t.fFoot, 1, legLength, legW, outline, skin, tattoo !== 'none');'''
content = content.replace(draw_leg_old_f, draw_leg_new_f)

draw_leg_old_b = '''drawDetailedLimb(t.bKnee, t.bFoot, -1, legLength, 20 * w, outline, skin, tattoo !== 'none');'''
draw_leg_new_b = '''let bLegW = 20 * w + (this.stats.speedBonus || 0) * 4;
                drawDetailedLimb(t.bKnee, t.bFoot, -1, legLength, bLegW, outline, skin, tattoo !== 'none');'''
content = content.replace(draw_leg_old_b, draw_leg_new_b)

draw_leg_thigh_old_f = '''drawDetailedLimb(t.pelvis, t.fKnee, 1, legLength, 26 * w, outline, skin, tattoo !== 'none');'''
draw_leg_thigh_new_f = '''let thighW = 26 * w + (this.stats.speedBonus || 0) * 5;
                drawDetailedLimb(t.pelvis, t.fKnee, 1, legLength, thighW, outline, skin, tattoo !== 'none');'''
content = content.replace(draw_leg_thigh_old_f, draw_leg_thigh_new_f)

draw_leg_thigh_old_b = '''drawDetailedLimb(t.pelvis, t.bKnee, -1, legLength, 24 * w, outline, skin, false);'''
draw_leg_thigh_new_b = '''let bThighW = 24 * w + (this.stats.speedBonus || 0) * 5;
                drawDetailedLimb(t.pelvis, t.bKnee, -1, legLength, bThighW, outline, skin, false);'''
content = content.replace(draw_leg_thigh_old_b, draw_leg_thigh_new_b)

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
