import re
with open('EFLTG.html', 'r') as f:
    content = f.read()

# I see the base width is set to things like 10 * w + (this.stats.neckGirth || 0) * 0.5;
# But the user complains that characters don't look realistic BEFORE upgrades.
# Let's check how the muscle base stats look.
# Maybe I should just increase the base stat? "more shapes is needed for muscles and all"
# Oh wait, the previous code in `replace_body.py` from earlier in this task had a completely different `drawDetailedLimb`?
# Wait! Let me check what the user said:
# "the upgrade that made the character shapes more complexe and realistic seems to have been scraped we need it back we need the characters to look realistic cefore upgrades so more shapes is needed for muscles and all"

