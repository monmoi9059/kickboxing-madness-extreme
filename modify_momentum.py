import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Add momentum for flying moves
momentum_func_start = content.find("function initiateAttack(fighter, moveName) {")
momentum_func_end = content.find("}", content.find("fighter.keyReleased = false;", momentum_func_start)) + 1

if momentum_func_start != -1:
    new_momentum = """function initiateAttack(fighter, moveName) {
            const move = moves[moveName];
            if (fighter.stats.stamina >= move.cost && fighter.state !== 'hit' && fighter.state !== 'ko') {
                fighter.stats.stamina -= move.cost;
                fighter.changeState(moveName, move.dur, move);
                fighter.keyReleased = false; // Prevent holding button

                // Add forward momentum for flying moves
                if (move.isFlying) {
                    fighter.vx = fighter.facing * (moveName === 'superman_punch' ? 8 : 6);
                }
            }
        }"""
    content = content[:momentum_func_start] + new_momentum + content[momentum_func_end:]

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
