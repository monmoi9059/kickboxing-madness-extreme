import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Replace muscle mutation math to allow significant scaling based on upgrades
old_math = """                // --- MUSCLE MUTATION MATH (Capped for aesthetic limits) ---
                let chestW = Math.min(45, 20 + (this.stats.maxHp / 15)) * w;
                let bicepW = Math.min(22, 8 + (this.stats.power / 4)) * w;
                let trapsW = Math.min(25, 10 + (this.stats.defense / 2.5)) * w;
                let hasAbs = this.stats.maxStamina >= 120;"""

new_math = """                // --- MUSCLE MUTATION MATH ---
                // The higher the stat goes over base (100 HP, 10 Pwr, 5 Def), the more visually massive they get
                let chestBase = 26; // Base width
                let hpBonus = Math.max(0, this.stats.maxHp - 100) * 0.15; // 20hp upgrade = +3 width
                let chestW = (chestBase + hpBonus) * w;

                let bicepBase = 10;
                let powerBonus = Math.max(0, this.stats.power - 10) * 1.5; // 3 pwr upgrade = +4.5 width
                let bicepW = (bicepBase + powerBonus) * w;

                let trapsBase = 12;
                let defBonus = Math.max(0, this.stats.defense - 5) * 1.5; // 2 def upgrade = +3 width
                let trapsW = (trapsBase + defBonus) * w;

                // Abs show if maxStamina is upgraded at least once (base is 100, upgrade is +15)
                let hasAbs = this.stats.maxStamina >= 115;"""

content = content.replace(old_math, new_math)

# Fix chest width drawing to actually use chestW dynamically for the pelvis width too, so the shorts get wider!
shorts_start = content.find("// Shorts")
shorts_end = content.find("ctx.fill(); ctx.stroke();", shorts_start)

if shorts_start != -1:
    new_shorts = """// Shorts
                ctx.fillStyle = shorts;
                ctx.beginPath();
                // Wider hips based on chest width
                let hipW = Math.max(20, chestW * 0.85);
                ctx.moveTo(t.pelvis.x - hipW/2 - 2, t.pelvis.y - 10*h);
                ctx.lineTo(t.pelvis.x + hipW/2 + 2, t.pelvis.y - 10*h);
                ctx.lineTo(t.pelvis.x + hipW/2, t.pelvis.y + 25*h);
                ctx.lineTo(t.pelvis.x - hipW/2, t.pelvis.y + 25*h);
                ctx.closePath();
                ctx.fill(); ctx.stroke();"""
    # Just a small manual fix to ensure shorts adjust right.
    pass

# We need to fix the torso to connect to the wider hips
torso_start = content.find("// Torso (Traps and Chest mutated)")
torso_end = content.find("ctx.fill(); ctx.stroke();", torso_start)

if torso_start != -1:
    new_torso = """// Torso (Traps and Chest mutated)
                let hipW = Math.max(20, chestW * 0.85); // Hips scale slightly with chest so you don't look like a dorito
                ctx.fillStyle = skin;
                ctx.strokeStyle = outline;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(t.neck.x - trapsW, t.neck.y); // Traps left
                ctx.lineTo(t.neck.x + trapsW, t.neck.y); // Traps right
                ctx.lineTo(t.pelvis.x + hipW/2, t.pelvis.y); // Hip right
                ctx.lineTo(t.pelvis.x - hipW/2, t.pelvis.y); // Hip left
                ctx.closePath();
                ctx.fill(); ctx.stroke();"""
    content = content[:torso_start] + new_torso + content[torso_end + len("ctx.fill(); ctx.stroke();"):]

    # Do shorts next to match
    shorts_start2 = content.find("// Shorts")
    shorts_end2 = content.find("ctx.fill(); ctx.stroke();", shorts_start2)
    new_shorts = """// Shorts
                ctx.fillStyle = shorts;
                ctx.beginPath();
                ctx.moveTo(t.pelvis.x - hipW/2 - 2, t.pelvis.y - 10*h);
                ctx.lineTo(t.pelvis.x + hipW/2 + 2, t.pelvis.y - 10*h);
                ctx.lineTo(t.pelvis.x + hipW/2, t.pelvis.y + 20*h);
                ctx.lineTo(t.pelvis.x - hipW/2, t.pelvis.y + 20*h);
                ctx.closePath();
                ctx.fill(); ctx.stroke();"""
    content = content[:shorts_start2] + new_shorts + content[shorts_end2 + len("ctx.fill(); ctx.stroke();"):]


with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
