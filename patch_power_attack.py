import re

with open("test.js", "r") as f:
    content = f.read()

# Add attackHoldTime to Fighter constructor
old_constructor = """                this.currentMove = null;
                this.hasHit = false;
                this.lastBlockTime = 0;"""

new_constructor = """                this.currentMove = null;
                this.hasHit = false;
                this.lastBlockTime = 0;
                this.attackHoldTime = 0;
                this.isPowerAttack = false;"""

if old_constructor in content:
    content = content.replace(old_constructor, new_constructor)

# When initiating an attack, initialize power attack tracking
old_initiate = """                fighter.attackKey = attackKey;
                fighter.keyReleased = false; // Prevent holding button

                // Add forward momentum for flying moves"""

new_initiate = """                fighter.attackKey = attackKey;
                fighter.keyReleased = false; // Prevent holding button
                fighter.attackHoldTime = 0;
                fighter.isPowerAttack = false;

                // Add forward momentum for flying moves"""

if old_initiate in content:
    content = content.replace(old_initiate, new_initiate)

# Update logic: track if key is held for 0.1s (100ms) to trigger power attack
old_update = """                // Timers & Stamina
                this.animTime += dt;
                if (this.stateTimer > 0) {
                    this.stateTimer -= dt;
                    if (this.stateTimer <= 0 && this.state !== 'ko') {
                        this.changeState('idle');
                    }
                }"""

new_update = """                // Timers & Stamina
                this.animTime += dt;

                // Power attack check
                if (this.currentMove && this.attackKey && !this.hasHit) {
                    // Check if the key that initiated the attack is still held down
                    let keyHeld = false;
                    if (this.isPlayer) {
                        // For player, check actual key state
                        keyHeld = keys[this.attackKey];
                    } else {
                        // AI holds attacks randomly for 150ms sometimes
                        if (this.aiHoldDuration === undefined) this.aiHoldDuration = Math.random() < 0.3 ? 150 : 0;
                        keyHeld = this.attackHoldTime < this.aiHoldDuration;
                    }

                    if (keyHeld) {
                        this.attackHoldTime += dt;
                        if (this.attackHoldTime >= 100) {
                            this.isPowerAttack = true;
                        }
                    }
                }

                if (this.stateTimer > 0) {
                    this.stateTimer -= dt;
                    if (this.stateTimer <= 0 && this.state !== 'ko') {
                        this.changeState('idle');
                    }
                }"""

if old_update in content:
    content = content.replace(old_update, new_update)

with open("test.js", "w") as f:
    f.write(content)
print("Patched power attack successfully!")
