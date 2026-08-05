import re

with open("test.js", "r") as f:
    content = f.read()

# Make appearances really distinct. Add more variety to sizes.
old_code = """                    for (let i = 0; i < numChoices; i++) {
                        let diff = 0.7 + (Math.random() * 0.6);
                        if (playerStats.losses && playerStats.losses > 0) {
                            diff *= Math.pow(0.8, playerStats.losses); // Weaker opponents and lower rewards if lost
                        }

                        let newOpp = JSON.parse(JSON.stringify(baseOpp));"""

new_code = """                    for (let i = 0; i < numChoices; i++) {
                        let diff = 0.7 + (Math.random() * 0.6);
                        if (playerStats.losses && playerStats.losses > 0) {
                            diff *= Math.pow(0.8, playerStats.losses); // Weaker opponents and lower rewards if lost
                        }

                        let randBaseIndex = Math.floor(Math.random() * opponents.length);
                        let newOpp = JSON.parse(JSON.stringify(opponents[randBaseIndex]));"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open("test.js", "w") as f:
        f.write(content)
    print("Patched random base opponents successfully!")
else:
    print("Could not find old_code for random base opponents.")
