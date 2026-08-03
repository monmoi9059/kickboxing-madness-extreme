import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# 1. Add new moves to the dictionary
moves_start = content.find("const moves = {")
moves_end = content.find("};", moves_start)

if moves_start != -1:
    new_moves = """const moves = {
            jab:            { type: 'high', dmg: 5,  cost: 10, dur: 250, reach: 65,  active: [100, 200] },
            cross:          { type: 'high', dmg: 12, cost: 18, dur: 400, reach: 75,  active: [200, 300] },
            body_jab:       { type: 'low',  dmg: 7,  cost: 12, dur: 300, reach: 60,  active: [150, 250] },
            body_cross:     { type: 'low',  dmg: 15, cost: 20, dur: 450, reach: 70,  active: [250, 350] },
            low_kick:       { type: 'low',  dmg: 10, cost: 15, dur: 350, reach: 60,  active: [150, 250] },
            high_kick:      { type: 'high', dmg: 20, cost: 30, dur: 600, reach: 70,  active: [350, 450] },
            superman_punch: { type: 'high', dmg: 25, cost: 35, dur: 700, reach: 90,  active: [400, 550], isFlying: true },
            flying_knee:    { type: 'high', dmg: 22, cost: 30, dur: 650, reach: 75,  active: [350, 500], isFlying: true },
            flying_kick:    { type: 'high', dmg: 30, cost: 45, dur: 800, reach: 100, active: [500, 650], isFlying: true }
        """
    content = content[:moves_start] + new_moves + content[moves_end:]

# 2. Add animation logic for these moves
# Find the start of the attack animation logic
anim_start = content.find("if (this.state === 'jab') {")
anim_end = content.find("} else if (this.state === 'block') {")

if anim_start != -1 and anim_end != -1:
    new_anim_logic = """if (this.state === 'jab') {
                        targetT.fHand = {x: 75*f*w, y: -65*h};
                        targetT.bHand = {x: 5*f*w, y: -65*h};
                        targetT.head.x += 15*f; targetT.pelvis.x += 10*f;
                    } else if (this.state === 'cross') {
                        targetT.bHand = {x: 85*f*w, y: -60*h};
                        targetT.fHand = {x: -15*f*w, y: -65*h}; // Pull back guard
                        targetT.pelvis.x += 20*f; targetT.head.x += 20*f;
                    } else if (this.state === 'body_jab') {
                        targetT.pelvis.y += 30*h; targetT.head.y += 30*h;
                        targetT.fHand = {x: 65*f*w, y: -5*h};
                        targetT.bHand = {x: 5*f*w, y: -45*h};
                    } else if (this.state === 'body_cross') {
                        targetT.pelvis.y += 30*h; targetT.head.y += 30*h;
                        targetT.bHand = {x: 75*f*w, y: -5*h};
                        targetT.fHand = {x: -15*f*w, y: -45*h};
                        targetT.pelvis.x += 20*f;
                    } else if (this.state === 'low_kick') {
                        targetT.bFoot = {x: 65*f*w, y: 65*h};
                        targetT.pelvis.x -= 15*f; targetT.head.x -= 20*f;
                        targetT.fHand.x -= 15*f; targetT.bHand.x += 25*f; // Arm swing for balance
                    } else if (this.state === 'high_kick') {
                        targetT.bFoot = {x: 65*f*w, y: -70*h};
                        targetT.pelvis.x -= 25*f; targetT.head.x -= 30*f; targetT.head.y += 10*h; // Lean back
                        targetT.fHand.x -= 20*f; targetT.bHand.x += 35*f;
                    } else if (this.state === 'superman_punch') {
                        // Launch forward, back leg kicks out behind, back hand strikes
                        targetT.pelvis.y -= 30*h; targetT.head.y -= 25*h; targetT.head.x += 30*f;
                        targetT.bHand = {x: 100*f*w, y: -55*h};
                        targetT.fHand = {x: -20*f*w, y: -55*h};
                        targetT.bFoot = {x: -60*f*w, y: -10*h}; // Kick back
                        targetT.fFoot = {x: -10*f*w, y: 50*h}; // Tucked
                    } else if (this.state === 'flying_knee') {
                        // Leap, drive front knee up
                        targetT.pelvis.y -= 40*h; targetT.head.y -= 35*h; targetT.head.x -= 10*f;
                        targetT.bHand = {x: -10*f*w, y: -70*h}; targetT.fHand = {x: 30*f*w, y: -20*h}; // Guard up/down
                        targetT.bFoot = {x: -20*f*w, y: 60*h};
                        targetT.fFoot = {x: 50*f*w, y: 0}; // Knee forward
                        // NOTE: Because we use drawDetailedLimb to calc knees, we just pull the foot up and forward
                    } else if (this.state === 'flying_kick') {
                        // Switch kick mid-air
                        targetT.pelvis.y -= 30*h; targetT.pelvis.x += 20*f;
                        targetT.head.y -= 20*h; targetT.head.x -= 20*f;
                        targetT.fFoot = {x: -30*f*w, y: 40*h}; // Tuck front
                        targetT.bFoot = {x: 100*f*w, y: -40*h}; // Extend back
                        targetT.fHand.x -= 30*f; targetT.bHand.x += 40*f; // Arm swing
                    }
                    """
    content = content[:anim_start] + new_anim_logic + content[anim_end:]

# 3. Add input handling for flying moves (triggered if airborne + attack)
input_start = content.find("if (keys.u) initiateAttack(pFighter, keys.shift ? 'body_jab' : 'jab');")
input_end = content.find("}", input_start)

if input_start != -1:
    new_input = """if (keys.u) initiateAttack(pFighter, keys.shift ? 'body_jab' : 'jab');
                    if (keys.i) initiateAttack(pFighter, keys.shift ? 'body_cross' : 'cross');
                    if (keys.j) initiateAttack(pFighter, 'low_kick');
                    if (keys.k) initiateAttack(pFighter, 'high_kick');
                } else if (!pFighter.isGrounded && pFighter.keyReleased) {
                    // Flying moves
                    if (keys.i) initiateAttack(pFighter, 'superman_punch');
                    if (keys.u || keys.j) initiateAttack(pFighter, 'flying_knee');
                    if (keys.k) initiateAttack(pFighter, 'flying_kick');
                """
    content = content[:input_start] + new_input + content[input_end:]


with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
