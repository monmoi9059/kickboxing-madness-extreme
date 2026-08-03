import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Remove the extra curly brace
old_str = """                if (move.isFlying) {
                    fighter.vx = fighter.facing * (moveName === 'superman_punch' ? 8 : 6);
                }
            }
        }
        }"""
new_str = """                if (move.isFlying) {
                    fighter.vx = fighter.facing * (moveName === 'superman_punch' ? 8 : 6);
                }
            }
        }"""

content = content.replace(old_str, new_str)

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
