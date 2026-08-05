import re

with open("test.js", "r") as f:
    content = f.read()

# Replace the jab block exactly
old_jab = """                    if (this.state === 'jab') {
                        targetT.fHand = {x: 85*f*w, y: -65*h};
                        targetT.bHand = {x: 0, y: -60*h}; // Guard high
                        targetT.head.x += 10*f;
                        targetT.pelvis.x += 5*f; targetT.pelvis.y -= 5*h; // Plant down slightly
                        targetT.fFoot.x += 5*f; // Slight step
                        targetT.bKnee.x += 10*f; // Slight rotation
                    } else if (this.state === 'cross') {
                        targetT.bHand = {x: 95*f*w, y: -60*h};
                        targetT.fHand = {x: -15*f*w, y: -65*h}; // Pull back guard
                        targetT.head.x += 20*f; targetT.head.y -= 5*h;
                        targetT.pelvis.x += 25*f; // Deep rotation
                        targetT.bKnee.x += 25*f; // Back hip turns over
                        targetT.bFoot.x += 15*f; targetT.bFoot.y -= 5*h; // Pivot on ball of back foot
                        targetT.fKnee.x -= 10*f; // Front hip pulls back
                    } else if (this.state === 'body_jab') {
                        targetT.pelvis.y += 35*h; targetT.head.y += 35*h;
                        targetT.head.x += 15*f;
                        targetT.fHand = {x: 75*f*w, y: -5*h};
                        targetT.bHand = {x: 0, y: -45*h};
                        targetT.fKnee.x += 15*f; targetT.fFoot.x += 10*f;
                    } else if (this.state === 'body_cross') {
                        targetT.pelvis.y += 35*h; targetT.head.y += 35*h;
                        targetT.pelvis.x += 25*f; targetT.head.x += 20*f;
                        targetT.bHand = {x: 85*f*w, y: -5*h};
                        targetT.fHand = {x: -15*f*w, y: -45*h};
                        targetT.bKnee.x += 20*f; targetT.bFoot.x += 10*f; targetT.bFoot.y -= 5*h; // Pivot
                    } else if (this.state === 'low_kick') {
                        targetT.bFoot = {x: 65*f*w, y: 65*h};
                        targetT.pelvis.x -= 15*f; targetT.head.x -= 20*f; targetT.head.y += 5*h;
                        targetT.fHand.x -= 25*f; targetT.bHand.x += 35*f; // Big arm swing for torque
                        targetT.fFoot.x -= 10*f; // Plant foot steps out
                    } else if (this.state === 'high_kick') {
                        targetT.bFoot = {x: 75*f*w, y: -75*h};
                        targetT.pelvis.x -= 25*f; targetT.head.x -= 35*f; targetT.head.y += 15*h; // Deep lean back
                        targetT.fHand.x -= 30*f; targetT.bHand.x += 45*f; // Whip arms
                        targetT.fFoot.x -= 15*f; // Plant foot steps out
                    }"""

new_jab = """                    if (this.state === 'jab') {
                        targetT.fHand = {x: 120*f*w, y: -65*h}; // Extended past max reach to force full extension
                        targetT.bHand = {x: 0, y: -60*h}; // Guard high
                        targetT.head.x += 10*f;
                        targetT.pelvis.x += 5*f; targetT.pelvis.y -= 5*h; // Plant down slightly
                        targetT.fFoot.x += 5*f; // Slight step
                        targetT.bKnee.x += 10*f; // Slight rotation
                    } else if (this.state === 'cross') {
                        targetT.bHand = {x: 130*f*w, y: -60*h}; // Extended past max reach
                        targetT.fHand = {x: -15*f*w, y: -65*h}; // Pull back guard
                        targetT.head.x += 20*f; targetT.head.y -= 5*h;
                        targetT.pelvis.x += 25*f; // Deep rotation
                        targetT.bKnee.x += 25*f; // Back hip turns over
                        targetT.bFoot.x += 15*f; targetT.bFoot.y -= 5*h; // Pivot on ball of back foot
                        targetT.fKnee.x -= 10*f; // Front hip pulls back
                    } else if (this.state === 'body_jab') {
                        targetT.pelvis.y += 35*h; targetT.head.y += 35*h;
                        targetT.head.x += 15*f;
                        targetT.fHand = {x: 110*f*w, y: -5*h}; // Extended past max reach
                        targetT.bHand = {x: 0, y: -45*h};
                        targetT.fKnee.x += 15*f; targetT.fFoot.x += 10*f;
                    } else if (this.state === 'body_cross') {
                        targetT.pelvis.y += 35*h; targetT.head.y += 35*h;
                        targetT.pelvis.x += 25*f; targetT.head.x += 20*f;
                        targetT.bHand = {x: 120*f*w, y: -5*h}; // Extended past max reach
                        targetT.fHand = {x: -15*f*w, y: -45*h};
                        targetT.bKnee.x += 20*f; targetT.bFoot.x += 10*f; targetT.bFoot.y -= 5*h; // Pivot
                    } else if (this.state === 'low_kick') {
                        targetT.bFoot = {x: 110*f*w, y: 65*h}; // Extended past max reach
                        targetT.pelvis.x -= 15*f; targetT.head.x -= 20*f; targetT.head.y += 5*h;
                        targetT.fHand.x -= 25*f; targetT.bHand.x += 35*f; // Big arm swing for torque
                        targetT.fFoot.x -= 10*f; // Plant foot steps out
                    } else if (this.state === 'high_kick') {
                        targetT.bFoot = {x: 120*f*w, y: -75*h}; // Extended past max reach
                        targetT.pelvis.x -= 25*f; targetT.head.x -= 35*f; targetT.head.y += 15*h; // Deep lean back
                        targetT.fHand.x -= 30*f; targetT.bHand.x += 45*f; // Whip arms
                        targetT.fFoot.x -= 15*f; // Plant foot steps out
                    }"""

if old_jab in content:
    content = content.replace(old_jab, new_jab)
    with open("test.js", "w") as f:
        f.write(content)
    print("Patched animations successfully!")
else:
    print("Could not find old_jab.")
