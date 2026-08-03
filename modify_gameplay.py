import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# 1. Update Fighter constructor to scale width, height, and speed based on height/weight multipliers
constructor_start = content.find("class Fighter {")
constructor_end = content.find("this.joints = {", constructor_start)

if constructor_start != -1:
    new_constructor = """class Fighter {
            constructor(x, y, facing, stats, isPlayer) {
                this.x = x;
                this.y = y;
                this.facing = facing; // 1 for right, -1 for left
                this.stats = JSON.parse(JSON.stringify(stats));
                this.stats.hp = this.stats.maxHp;
                this.stats.stamina = this.stats.maxStamina;
                this.isPlayer = isPlayer;

                const app = this.stats.appearance || { h: 1, w: 1 };
                const hScale = app.h || 1;
                const wScale = app.w || 1;

                // Height affects hitboxes (width/height) and reach (via a multiplier in combat logic)
                this.width = 60 * hScale;
                this.height = 180 * hScale;

                // Speed is inversely proportional to weight. Heavier = slower. Taller = slightly slower to get moving.
                // Base speed is 4.
                this.speed = 4 * (1 / wScale) * (1 / ((hScale - 1) * 0.5 + 1));

                // Power is amplified by weight.
                this.stats.power = this.stats.power * wScale;

                this.vx = 0;
                this.vy = 0;
                this.isGrounded = false;

                this.state = 'idle'; // idle, walk, hit, ko, block, dodge, attack states...
                this.stateTimer = 0;
                this.animTime = 0;
                this.keyReleased = true;

                this.currentMove = null;
                this.hasHit = false;
                this.lastBlockTime = 0;

                """
    content = content[:constructor_start] + new_constructor + content[constructor_end:]

# 2. Update reach calculation to factor in height
reach_start = content.find("// Calculate reach hitbox")
reach_end = content.find("const defStartX = defender.x;", reach_start)

if reach_start != -1:
    new_reach = """// Calculate reach hitbox
                        const appH = attacker.stats.appearance ? (attacker.stats.appearance.h || 1) : 1;
                        let reachStartX = attacker.x + (attacker.width/2);
                        // Taller fighters have longer reach
                        let scaledReach = move.reach * appH;
                        let reachEndX = reachStartX + (scaledReach * attacker.facing);
                        if (attacker.facing === -1) {
                            let temp = reachStartX; reachStartX = reachEndX; reachEndX = temp;
                        }

                        """
    content = content[:reach_start] + new_reach + content[reach_end:]

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
