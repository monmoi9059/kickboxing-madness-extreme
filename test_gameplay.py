import re

with open('EFLTG.html', 'r') as f:
    content = f.read()

# Right now `initiateAttack` executes the attack immediately.
# And then, inside `Fighter.update`, if the key is still held, it accumulates `attackHoldTime`.
# If `attackHoldTime >= 100`, `isPowerAttack` becomes true.
# BUT wait! The attack animation is already playing! The active frames are from e.g. 100 to 200 ms.
# So if they hold it, `isPowerAttack` is set to true just in time for the active frames, and damage is multiplied.
# But what if we change it so they hold the key to charge up, and the attack only happens when they release?
# If we do that, we need a new state: `charging`.
