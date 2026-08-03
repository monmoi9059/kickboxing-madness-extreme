import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# 1. Update Block Animation (high vs low block)
block_anim_start = content.find("} else if (this.state === 'block') {")
block_anim_end = content.find("} else if (this.state === 'dodge') {")

if block_anim_start != -1:
    new_block_anim = """} else if (this.state === 'block') {
                    targetT.fHand = {x: 15*f*w, y: -65*h};
                    targetT.bHand = {x: 0, y: -70*h};
                    targetT.head.x -= 12*f; targetT.head.y += 8*h;
                    targetT.pelvis.y += 8*h; // Crunch down tight
                } else if (this.state === 'low_block') {
                    targetT.fHand = {x: 20*f*w, y: -20*h}; // Drop front hand to block body
                    targetT.bHand = {x: 0, y: -60*h}; // Keep back hand up
                    targetT.head.x -= 15*f; targetT.head.y += 20*h;
                    targetT.pelvis.y += 30*h; // Squat down
                    targetT.fFoot.x += 10*f*w; targetT.bFoot.x -= 10*f*w; // Widen stance
                """
    content = content[:block_anim_start] + new_block_anim + content[block_anim_end:]

# 2. Update Dodge Animation (ducking, directional)
dodge_anim_start = content.find("} else if (this.state === 'dodge') {")
dodge_anim_end = content.find("} else if (this.state === 'hit') {")

if dodge_anim_start != -1:
    new_dodge_anim = """} else if (this.state === 'dodge' || this.state === 'duck') {
                    targetT.pelvis.y += 45*h; targetT.head.y += 45*h; // Deep duck
                    targetT.fHand = { x: 15*f*w, y: -30*h };
                    targetT.bHand = { x: 5*f*w, y: -40*h };
                    if (this.state === 'dodge') {
                        // Directional dodge leans head away
                        targetT.head.x -= 30*f*w; targetT.neck.x -= 25*f*w;
                        targetT.fFoot.x += 20*f*w; targetT.bFoot.x -= 15*f*w;
                    } else {
                        // Just slip/duck
                        targetT.head.x += 15*f*w; // Slip outside
                    }
                """
    content = content[:dodge_anim_start] + new_dodge_anim + content[dodge_anim_end:]

# 3. Update Input handling for defense
input_start = content.find("// Dodge (Bob and Weave")
input_end = content.find("// Attacks (With Shift modifiers)")

if input_start != -1:
    new_input = """// Dodge / Duck
                if (keys.s && pFighter.isGrounded && ['idle','walk'].includes(pFighter.state) && pFighter.keyReleased) {
                    if (pFighter.stats.stamina >= 15) {
                        pFighter.stats.stamina -= 15;
                        if (keys.a || keys.d) {
                            // Directional Dodge
                            pFighter.changeState('dodge', 400);
                            pFighter.vx = (keys.d ? 1 : -1) * 3; // Slide in direction
                        } else {
                            // Duck / Slip
                            pFighter.changeState('duck', 400);
                        }
                        pFighter.keyReleased = false;
                    }
                }

                // Block (High / Low)
                if (keys.o && pFighter.isGrounded && ['idle','walk','block','low_block'].includes(pFighter.state)) {
                    let blockState = keys.shift ? 'low_block' : 'block';
                    if (pFighter.state !== blockState) pFighter.changeState(blockState, 9999);
                    pFighter.lastBlockTime = Date.now();
                } else if (!keys.o && (pFighter.state === 'block' || pFighter.state === 'low_block') && Date.now() - pFighter.lastBlockTime > 50) {
                    pFighter.changeState('idle'); // Stop blocking when key released
                }

                """
    content = content[:input_start] + new_input + content[input_end:]

# 4. Update Damage Logic (Block mitigations and Dodge i-frames)
dmg_start = content.find("let isDodged = false;")
dmg_end = content.find("if (isDodged) {")

if dmg_start != -1:
    new_dmg_logic = """let isDodged = false;
                            // I-frames for dodge/duck
                            if ((defender.state === 'dodge' || defender.state === 'duck') && (400 - defender.stateTimer) < 300) {
                                // High attacks miss ducking/dodging opponents completely
                                if (move.type === 'high') {
                                    isDodged = true;
                                } else if (defender.state === 'dodge') {
                                    isDodged = true; // directional dodge avoids everything in first 300ms
                                }
                            }

                            attacker.hasHit = true;

                            """
    content = content[:dmg_start] + new_dmg_logic + content[dmg_end:]

# 5. Fix blocking mitigation math
block_dmg_start = content.find("if (defender.state === 'block') {")
block_dmg_end = content.find("} else {", block_dmg_start)

if block_dmg_start != -1:
    new_block_dmg = """if (defender.state === 'block' || defender.state === 'low_block') {
                                    dmg -= defender.stats.defense;

                                    // High block vs High attack = good. Low block vs Low attack = good.
                                    if ((defender.state === 'block' && move.type === 'high') ||
                                        (defender.state === 'low_block' && move.type === 'low')) {
                                        dmg *= 0.2; // Perfect block (80% mitigation)
                                    } else {
                                        dmg *= 0.6; // Wrong block (40% mitigation)
                                    }
                                """
    content = content[:block_dmg_start] + new_block_dmg + content[block_dmg_end:]


with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
