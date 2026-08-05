with open("hairstyles_upgrade.html", "r") as f:
    content = f.read()

bad_block = """                ctx.fill(); ctx.stroke();

                // Head bob
                    baseT.head.y -= stepHeight * 0.3;
                }

                // 3. Define Target Pose based on State"""

if bad_block in content:
    # We shouldn't be defining baseT and bobbing head right after shorts rendering!
    # Wait, the shorts rendering is inside `drawDetailedFighter`, but `targetT` is part of update loop.
    print("Found the bad block! Let's see the bigger context to fix it correctly.")
else:
    print("Could not find bad block")
