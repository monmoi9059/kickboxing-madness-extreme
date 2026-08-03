import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Enhance procedural animations by updating the base pose and breathing
# Specifically: better idle bouncing, footwork shuffling
def update_animations():
    global content

    # Let's locate the FLUID ANIMATION ENGINE section
    start_marker = "// --- FLUID ANIMATION ENGINE ---"
    end_marker = "// 3. Define Target Pose based on State"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    new_anim_code = """// --- FLUID ANIMATION ENGINE ---
                // Enhance idle breathing
                let breathe = Math.sin(this.animTime * 0.004);
                let bounce = breathe * 2.5;
                let chestExpand = breathe * 2;

                // 1. Base Idle Pose (with natural breathing bounce and active stance)
                let baseT = {
                    head: {x: 5*f*w, y: -70*h + bounce},
                    neck: {x: 0, y: -50*h},
                    pelvis: {x: -5*f*w, y: 10*h + bounce*1.2},
                    fHand: {x: 25*f*w, y: -45*h + bounce*1.5},
                    bHand: {x: 0, y: -35*h + bounce*1.5},
                    fFoot: {x: 35*f*w, y: 90*h},
                    bFoot: {x: -30*f*w, y: 90*h - 5}, // Back foot slightly raised on toes
                    fKnee: {x: 30*f*w, y: 50*h + bounce}, // Added knees to allow elbows/knees to render correctly in idle
                    bKnee: {x: -20*f*w, y: 45*h + bounce}
                };

                // Add chest expansion for breathing (visual only through trap stretching)
                trapsW += chestExpand;

                // 2. Add Walk Stride Offsets (Footwork Shuffle)
                if (this.state === 'walk') {
                    let stride = Math.sin(this.animTime * 0.015) * 30; // Faster, slightly wider step
                    let stepHeight = Math.abs(Math.cos(this.animTime * 0.015)) * 10;

                    if (stride > 0) { // Front foot moving
                        baseT.fFoot.x += stride * f;
                        baseT.fFoot.y -= stepHeight;
                    } else { // Back foot moving
                        baseT.bFoot.x -= stride * f;
                        baseT.bFoot.y -= stepHeight;
                    }

                    baseT.pelvis.y -= Math.abs(stride) * 0.2;
                    baseT.fHand.x += stride * 0.2 * f;
                    baseT.fHand.y -= stepHeight * 0.5;
                    baseT.bHand.x -= stride * 0.2 * f;
                    baseT.bHand.y -= stepHeight * 0.5;
                    baseT.head.y -= stepHeight * 0.3;
                }

                """

    if start_idx != -1 and end_idx != -1:
        content = content[:start_idx] + new_anim_code + content[end_idx:]
    else:
        print("Could not find animation code to replace")

update_animations()

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
