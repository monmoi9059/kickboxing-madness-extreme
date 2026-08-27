import re

with open('EFLTG.html', 'r') as f:
    content = f.read()

# Let's locate the attack easing section
start_marker = "const animScale = this.isPowerAttack ? 1.0 : 0.6;"
end_marker = "if (this.state === 'jab') {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    new_ease = """const animScale = this.isPowerAttack ? 1.0 : 0.6;
                    // Snappy Easing: Reach full extension quickly, hold briefly, then pull back
                    // p goes from 0 (start) to 1 (end)
                    let t_val = 0;
                    if (p < 0.2) {
                        // Very fast extension (easeOutQuad)
                        let t = p / 0.2;
                        t_val = t * (2 - t);
                    } else if (p < 0.4) {
                        // Hold max extension momentarily
                        t_val = 1.0;
                    } else {
                        // Smooth retraction
                        let t = (p - 0.4) / 0.6;
                        t_val = 1 - (t * t); // easeInQuad
                    }
                    attackIntensity = t_val * animScale;
                    """
    content = content[:start_idx] + new_ease + content[end_idx:]


# And let's update the poses to be more dynamic and dramatic
poses_start = content.find("if (this.state === 'jab') {")
poses_end = content.find("} else if (this.state === 'block') {")

if poses_start != -1:
    new_poses = """if (this.state === 'jab') {
                        targetT.fHand = {x: 100*f*w, y: -65*h}; // Snap jab out further
                        targetT.bHand = {x: -5*f*w, y: -60*h}; // Guard tight
                        targetT.head.x += 10*f;
                        targetT.pelvis.x += 10*f; targetT.pelvis.y -= 5*h; // Plant down and step in
                        targetT.fFoot.x += 15*f; // Step in on jab
                        targetT.bKnee.x += 10*f; // Slight rotation
                        targetT.bFoot.x += 5*f; // Drag back foot slightly
                    } else if (this.state === 'cross') {
                        targetT.bHand = {x: 110*f*w, y: -60*h}; // Fully extend cross
                        targetT.fHand = {x: -25*f*w, y: -65*h}; // Pull guard back to chin
                        targetT.head.x += 25*f; targetT.head.y -= 8*h; // Lean into the punch
                        targetT.pelvis.x += 35*f; // Huge core rotation
                        targetT.bKnee.x += 35*f; targetT.bKnee.y += 10*h; // Back hip turns entirely over
                        targetT.bFoot.x += 20*f; targetT.bFoot.y -= 10*h; // Pivot completely on back foot
                        targetT.fKnee.x -= 15*f; // Front hip clears path
                        targetT.fFoot.x += 10*f; // Small step
                    } else if (this.state === 'body_jab') {
                        targetT.pelvis.y += 45*h; targetT.head.y += 45*h; // Level change deeper
                        targetT.head.x += 20*f;
                        targetT.fHand = {x: 95*f*w, y: 10*h}; // Punch lower
                        targetT.bHand = {x: -5*f*w, y: -45*h};
                        targetT.fKnee.x += 25*f; targetT.fFoot.x += 20*f; // Deep lunge step
                    } else if (this.state === 'body_cross') {
                        targetT.pelvis.y += 45*h; targetT.head.y += 45*h; // Level change
                        targetT.pelvis.x += 30*f; targetT.head.x += 30*f;
                        targetT.bHand = {x: 100*f*w, y: 10*h}; // Lower punch
                        targetT.fHand = {x: -25*f*w, y: -45*h};
                        targetT.bKnee.x += 30*f; targetT.bFoot.x += 15*f; targetT.bFoot.y -= 10*h; // Deep pivot
                        targetT.fFoot.x += 10*f;
                    } else if (this.state === 'low_kick') {
                        targetT.bFoot = {x: 90*f*w, y: 75*h}; // Heavy chop down
                        targetT.pelvis.x -= 20*f; targetT.head.x -= 25*f; targetT.head.y += 10*h; // Lean away from counter
                        targetT.fHand.x -= 40*f; targetT.bHand.x += 45*f; // Huge arm swing for torque
                        targetT.fFoot.x -= 15*f; // Plant foot pivots out
                        targetT.bKnee = {x: 45*f*w, y: 60*h}; // Chamber knee first
                    } else if (this.state === 'high_kick') {
                        targetT.bFoot = {x: 100*f*w, y: -85*h}; // High extension
                        targetT.pelvis.x -= 30*f; targetT.head.x -= 45*f; targetT.head.y += 25*h; // Deep lean back to get height
                        targetT.fHand.x -= 45*f; targetT.bHand.x += 60*f; // Massive arm whip
                        targetT.fFoot.x -= 20*f; // Plant foot step
                        targetT.bKnee = {x: 45*f*w, y: -20*h}; // Chamber high
                    } else if (this.state === 'superman_punch') {
                        // Launch forward, back leg kicks out behind, back hand strikes
                        targetT.pelvis.y -= 45*h; targetT.head.y -= 35*h; targetT.head.x += 50*f;
                        targetT.bHand = {x: 120*f*w, y: -55*h};
                        targetT.fHand = {x: -35*f*w, y: -55*h};
                        targetT.bFoot = {x: -90*f*w, y: -25*h}; // Kick back much harder (superman pose)
                        targetT.fFoot = {x: -15*f*w, y: 60*h}; // Front leg tucked under
                    } else if (this.state === 'flying_knee') {
                        // Leap, drive front knee up
                        targetT.pelvis.y -= 60*h; targetT.head.y -= 50*h; targetT.head.x -= 20*f;
                        targetT.bHand = {x: -25*f*w, y: -80*h}; targetT.fHand = {x: 45*f*w, y: -10*h}; // Grab head motion
                        targetT.bFoot = {x: -35*f*w, y: 70*h}; // Back leg dangles
                        targetT.fFoot = {x: 65*f*w, y: 0}; // Knee forward driven high
                        targetT.fKnee = {x: 80*f*w, y: -10*h}; // Point of impact is the knee
                    } else if (this.state === 'flying_kick') {
                        // Switch kick mid-air
                        targetT.pelvis.y -= 55*h; targetT.pelvis.x += 35*f;
                        targetT.head.y -= 35*h; targetT.head.x -= 35*f;
                        targetT.fFoot = {x: -50*f*w, y: 50*h}; // Tuck front leg deep
                        targetT.bFoot = {x: 120*f*w, y: -55*h}; // Extend back leg fully like a whip
                        targetT.fHand.x -= 45*f; targetT.bHand.x += 55*f; // Arm swing
                    }"""
    content = content[:poses_start] + new_poses + content[poses_end:]

with open('EFLTG.html', 'w') as f:
    f.write(content)
