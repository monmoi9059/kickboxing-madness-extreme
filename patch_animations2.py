import re

with open('EFLTG.html', 'r') as f:
    content = f.read()

ease_start = content.find("const animScale = this.isPowerAttack ? 1.0 : 0.6;")
if ease_start != -1:
    ease_end = content.find("if (this.state === 'jab') {", ease_start)
    new_ease = """const animScale = this.isPowerAttack ? 1.0 : 0.6;
                    // Snappy Easing: Reach full extension quickly, hold, pull back
                    // p goes from 0 (start) to 1 (end)
                    let t_val = 0;
                    if (p < 0.3) {
                        // Fast extension (easeOutQuad)
                        let t = p / 0.3;
                        t_val = t * (2 - t);
                    } else {
                        // Slower retraction (easeInQuad from 1 to 0)
                        let t = (p - 0.3) / 0.7;
                        t_val = 1 - (t * t);
                    }
                    attackIntensity = t_val * animScale;
                    """
    content = content[:ease_start] + new_ease + content[ease_end:]

poses_start = content.find("if (this.state === 'jab') {")
poses_end = content.find("} else if (this.state === 'block') {")

if poses_start != -1:
    new_poses = """if (this.state === 'jab') {
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
                    } else if (this.state === 'superman_punch') {
                        // Launch forward, back leg kicks out behind, back hand strikes
                        targetT.pelvis.y -= 30*h; targetT.head.y -= 25*h; targetT.head.x += 35*f;
                        targetT.bHand = {x: 105*f*w, y: -55*h};
                        targetT.fHand = {x: -25*f*w, y: -55*h};
                        targetT.bFoot = {x: -70*f*w, y: -15*h}; // Kick back hard
                        targetT.fFoot = {x: -10*f*w, y: 50*h}; // Tucked
                    } else if (this.state === 'flying_knee') {
                        // Leap, drive front knee up
                        targetT.pelvis.y -= 45*h; targetT.head.y -= 40*h; targetT.head.x -= 15*f;
                        targetT.bHand = {x: -15*f*w, y: -70*h}; targetT.fHand = {x: 35*f*w, y: -20*h};
                        targetT.bFoot = {x: -25*f*w, y: 60*h};
                        targetT.fFoot = {x: 60*f*w, y: 0}; // Knee forward driven high
                    } else if (this.state === 'flying_kick') {
                        // Switch kick mid-air
                        targetT.pelvis.y -= 35*h; targetT.pelvis.x += 25*f;
                        targetT.head.y -= 25*h; targetT.head.x -= 25*f;
                        targetT.fFoot = {x: -35*f*w, y: 40*h}; // Tuck front
                        targetT.bFoot = {x: 110*f*w, y: -45*h}; // Extend back fully
                        targetT.fHand.x -= 35*f; targetT.bHand.x += 45*f; // Arm swing
                    }"""
    content = content[:poses_start] + new_poses + content[poses_end:]

with open('EFLTG.html', 'w') as f:
    f.write(content)
