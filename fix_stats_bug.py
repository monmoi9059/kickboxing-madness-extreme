import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Currently in Fighter constructor:
# this.stats.power = this.stats.power * wScale;
# This overrides the power stat, but doesn't take into account `deltoidSize` etc!
# And it doesn't do anything for chinSize (+HP, +Def).
# We should probably combine the new muscle upgrades into the raw stats in the constructor.
# Or even better, update `updateGymUI()` to add these to the core stats? No, because it says "+Power".
# Ah! In updateGymUI, it does `playerStats[key] += data.val;`
# So `playerStats.deltoidSize` goes up. But the combat damage logic looks at `attacker.stats.power`.
# So `attacker.stats.power` needs to be calculated dynamically in Fighter constructor, or `playerStats.deltoidSize` should ADD to `playerStats.power` when you upgrade it.

# Let's look at updateGymUI():
#                        } else {
#                            playerStats[key] += data.val;
#                        }
# If we upgrade Deltoid Size, `playerStats.deltoidSize` increases. But `playerStats.power` DOES NOT INCREASE.
# Same for Forearm Size (+Defense), Thigh Size (+Max Stamina), Calf Size (+Speed), Chin Size (+HP, +Def).
# We need to add these derived stats to the Fighter initialization so they actually have gameplay effects!
