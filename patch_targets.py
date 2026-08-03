import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# We need to extend the reach visual of attacks by limbMod
# We can do this right after the if (this.state === ...) block before the Blend Attack Extension smoothly

old_blend = '''                // Blend Attack Extension smoothly
                if (isAttack) {'''

new_blend = '''                // Dynamically extend attack visuals based on limbMod so it matches hitbox reach and prevents bunching
                if (isAttack && this.limbMod > 0) {
                    let ext = this.limbMod;

                    // Hands/feet go further out
                    if (this.state === 'jab' || this.state === 'body_jab') targetT.fHand.x += ext * f;
                    if (this.state === 'cross' || this.state === 'body_cross') targetT.bHand.x += ext * f;
                    if (this.state === 'low_kick' || this.state === 'high_kick' || this.state === 'flying_kick') {
                        targetT.bFoot.x += ext * f;
                        targetT.pelvis.y -= ext * 0.3; // Lift torso to allow for longer leg without scrunching
                        targetT.head.y -= ext * 0.3;
                    }
                    if (this.state === 'superman_punch') targetT.bHand.x += ext * f;
                    if (this.state === 'flying_knee') targetT.fFoot.x += ext * f;
                }

                // Blend Attack Extension smoothly
                if (isAttack) {'''

content = content.replace(old_blend, new_blend)

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
