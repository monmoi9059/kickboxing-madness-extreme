import re

with open("test.js", "r") as f:
    content = f.read()

# "if we lose fight put us against weaker oponents with smaller reward pool"

# Right now when we lose:
#                 } else {
#                     const opp = currentOpponentChoices[selectedOpponentIndex];
#                     const loserBonus = Math.floor(opp.reward * 0.25); // Give 25% of reward for losing
#                     playerStats.money += loserBonus;
#                     playerStats.rank = Math.max(0, playerStats.rank - 1);
#                     currentOpponentChoices = [];

# By default, the opponents generator scales diff based on random.
# We can track consecutive losses and reduce cycleMulti or diff. Or we can just use `playerStats.rank` drop to ensure we face weaker opponents, but wait... `randBaseIndex` is now random across all opponents, not scaling with rank.
# The user asked: "if we lose fight put us against weaker oponents with smaller reward pool"
# Because we changed randBaseIndex to be completely random, they could fight the final boss (The Reaper) at rank 0, which would just have its stats multiplied by rank cycleMulti.
# Let's fix `randBaseIndex` generation to be more tied to `baseIndex`, or completely revert to using `baseOpp` but applying appearance randomization.
