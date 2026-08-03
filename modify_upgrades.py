import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# 1. Add "Botched Surgery" upgrade
upgrade_start = content.find("const upgradeCosts = {")
upgrade_end = content.find("};", upgrade_start)

if upgrade_start != -1:
    new_upgrades = """const upgradeCosts = {
            maxHp: { base: 50, mult: 1.4, name: "Max Health (Chest Width)", val: 20 },
            power: { base: 60, mult: 1.5, name: "Power (Bicep Size)", val: 3 },
            defense: { base: 40, mult: 1.4, name: "Defense (Traps Size)", val: 2 },
            maxStamina: { base: 40, mult: 1.3, name: "Max Stamina (Abs)", val: 15 },
            staminaRegen: { base: 50, mult: 1.5, name: "Cardio", val: 3 },
            botchedSurgery: { base: 200, mult: 2.0, name: "Botched Limb Lengthening (-Stamina)", val: 1 }
        """
    content = content[:upgrade_start] + new_upgrades + content[upgrade_end:]

# 2. Add to upgrade levels
level_start = content.find("let upgradeLevels = {")
level_end = content.find("};", level_start)

if level_start != -1:
    new_levels = "let upgradeLevels = { maxHp: 0, power: 0, defense: 0, maxStamina: 0, staminaRegen: 0, botchedSurgery: 0 "
    content = content[:level_start] + new_levels + content[level_end:]

# 3. Modify updateGymUI to handle the custom logic for botched surgery (reducing stamina)
gym_ui_start = content.find("btn.onclick = () => {")
gym_ui_end = content.find("};", gym_ui_start)

if gym_ui_start != -1:
    new_gym_logic = """btn.onclick = () => {
                        playerStats.money -= cost;
                        upgradeLevels[key]++;

                        if (key === 'botchedSurgery') {
                            // Increases limb length drastically, reduces stamina
                            playerStats.appearance.limbLengthMod = (playerStats.appearance.limbLengthMod || 0) + 20;
                            playerStats.maxStamina = Math.max(10, playerStats.maxStamina - 20); // Penalty
                            if (playerStats.stamina > playerStats.maxStamina) playerStats.stamina = playerStats.maxStamina;
                        } else {
                            playerStats[key] += data.val;
                        }
                        updateGymUI();
                    """
    content = content[:gym_ui_start] + new_gym_logic + content[gym_ui_end:]


# 4. Modify Fighter constructor and reach to use limbLengthMod
fighter_start = content.find("this.width = 60 * hScale;")
fighter_end = content.find("this.height = 180 * hScale;", fighter_start) + len("this.height = 180 * hScale;")

if fighter_start != -1:
    new_fighter_dims = """this.width = 60 * hScale;
                this.height = 180 * hScale;
                this.limbMod = app.limbLengthMod || 0;
                """
    content = content[:fighter_start] + new_fighter_dims + content[fighter_end:]

# Update reach logic
reach_start = content.find("let scaledReach = move.reach * appH;")
reach_end = content.find("let reachEndX", reach_start)

if reach_start != -1:
    new_reach_logic = "let scaledReach = (move.reach * appH) + (attacker.stats.appearance ? (attacker.stats.appearance.limbLengthMod || 0) : 0);\n                        "
    content = content[:reach_start] + new_reach_logic + content[reach_end:]

# 5. Lock height slider after creation (if rank > 0)
init_gym_start = content.find("// Initialize Gym on load")
if init_gym_start != -1:
    lock_logic = """
        // Lock physical traits if a fight has occurred
        function checkTraitLocks() {
            if (playerStats.rank > 0) {
                document.getElementById('custom-height').disabled = true;
                document.getElementById('custom-height').classList.add('opacity-50', 'cursor-not-allowed');
                document.getElementById('custom-weight').disabled = true;
                document.getElementById('custom-weight').classList.add('opacity-50', 'cursor-not-allowed');
                // Optional: add a tiny lock icon or note
                if (!document.getElementById('lock-note')) {
                    const note = document.createElement('div');
                    note.id = 'lock-note';
                    note.className = 'text-xs text-red-400 mt-2 text-center';
                    note.innerText = 'Genetics locked after pro debut.';
                    document.getElementById('custom-weight').parentElement.appendChild(note);
                }
            }
        }
    """
    content = content[:init_gym_start] + lock_logic + "\n" + content[init_gym_start:]

update_gym_call = content.find("updateGymUI();\n    </script>")
if update_gym_call != -1:
    content = content.replace("updateGymUI();\n    </script>", "updateGymUI();\n        checkTraitLocks();\n    </script>")


# 6. Funny visual for Botched Surgery
# Find drawDetailedLimb and arm/leg length calculations
limb_len_start = content.find("const armLength = 75 * h;")
limb_len_end = content.find("const legLength = 80 * h;", limb_len_start) + len("const legLength = 80 * h;")

if limb_len_start != -1:
    new_limb_lens = """const armLength = (75 * h) + (app.limbLengthMod || 0);
                const legLength = (80 * h) + (app.limbLengthMod || 0);"""
    content = content[:limb_len_start] + new_limb_lens + content[limb_len_end:]

draw_limb_start = content.find("const drawDetailedLimb = (startJoint, endJoint, bendDir, limbLength, width, outlineCol, fillCol, hasTattoo = false) => {")
draw_limb_end = content.find("// Calculate midpoint (elbow/knee)")

if draw_limb_start != -1:
    funny_limb_logic = """const drawDetailedLimb = (startJoint, endJoint, bendDir, limbLength, width, outlineCol, fillCol, hasTattoo = false) => {
                    // Botched surgery visual: If limb length is wildly upgraded, make it look disjointed/crooked
                    let botchedLevel = app.limbLengthMod ? Math.floor(app.limbLengthMod / 20) : 0;

                    // Add some terrifying jiggle to the joint if severely botched
                    let jiggleX = 0; let jiggleY = 0;
                    if (botchedLevel > 0 && this.state !== 'ko') {
                        jiggleX = (Math.random() - 0.5) * botchedLevel * 2;
                        jiggleY = (Math.random() - 0.5) * botchedLevel * 2;
                    }
                    """
    content = content.replace("const drawDetailedLimb = (startJoint, endJoint, bendDir, limbLength, width, outlineCol, fillCol, hasTattoo = false) => {", funny_limb_logic)

    # We need to inject jiggleX into the midX calc
    midx_start = content.find("let midX = startJoint.x + Math.cos(midAngle) * l;")
    if midx_start != -1:
        content = content.replace("let midX = startJoint.x + Math.cos(midAngle) * l;", "let midX = startJoint.x + Math.cos(midAngle) * l + jiggleX;")
        content = content.replace("let midY = startJoint.y + Math.sin(midAngle) * l;", "let midY = startJoint.y + Math.sin(midAngle) * l + jiggleY;")

    # Draw stitches for botched limbs
    tattoo_end = content.find("}\n                    }\n                };")
    if tattoo_end != -1:
        stitches = """
                    // Botched Stitches!
                    if (botchedLevel > 0) {
                        ctx.strokeStyle = 'red';
                        ctx.lineWidth = 1.5;
                        ctx.beginPath();
                        ctx.moveTo(midX - width/2, midY - 5);
                        ctx.lineTo(midX + width/2, midY + 5);
                        ctx.moveTo(midX - width/2, midY + 5);
                        ctx.lineTo(midX + width/2, midY - 5);
                        ctx.stroke();

                        // Metal Pins
                        if (botchedLevel > 1) {
                            ctx.fillStyle = 'silver';
                            ctx.fillRect(midX - 3, midY - 15, 6, 30);
                            ctx.strokeRect(midX - 3, midY - 15, 6, 30);
                        }
                    }
                """
        content = content[:tattoo_end + 22] + stitches + content[tattoo_end + 22:]

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
