import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Replace draw function logic
def replace_draw_function():
    global content

    # Locate draw(ctx)
    start_str = "            draw(ctx) {"
    start_idx = content.find(start_str)

    # We want to keep the start up to the app const
    # Let's find the RENDER ORDER part to replace
    render_start = content.find("// --- RENDER ORDER (Back to Front) ---")
    render_end = content.find("ctx.restore();\n            }", render_start)

    if render_start == -1 or render_end == -1:
        print("Could not find render order section")
        return

    new_render_code = """// --- RENDER ORDER (Back to Front) ---

                const fHair = app.facialhair || 'none';
                const tattoo = app.tattoos || 'none';
                const gType = app.glovetype || 'boxing';

                // Helper for 2-part limb
                const drawLimb = (p1, p2, width1, width2, color) => {
                    ctx.beginPath();
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';

                    // Simple hack: draw one capsule. A more advanced version would calculate the mid joint (elbow/knee)
                    // For now, let's keep it simple or implement inverse kinematics if requested.
                    // Given the current skeleton only has Hand, Neck, etc. we will stick to 1 segment, but add detail.
                    ctx.lineWidth = width1;
                    ctx.strokeStyle = color;
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                };

                const drawDetailedLimb = (startJoint, endJoint, bendDir, limbLength, width, outlineCol, fillCol, hasTattoo = false) => {
                    // Calculate midpoint (elbow/knee)
                    let dx = endJoint.x - startJoint.x;
                    let dy = endJoint.y - startJoint.y;
                    let dist = Math.sqrt(dx*dx + dy*dy);

                    // If distance is too long, constrain it (prevent tearing)
                    if (dist > limbLength) {
                        dx = (dx / dist) * limbLength;
                        dy = (dy / dist) * limbLength;
                        dist = limbLength;
                    }

                    // Calculate elbow/knee joint using trigonometry
                    // Assuming upper and lower limbs are equal length (limbLength / 2)
                    let l = limbLength / 2;
                    // Law of cosines to find angle
                    let cosAngle = (dist*dist) / (2 * l * dist);
                    if (cosAngle > 1) cosAngle = 1;
                    let angle = Math.acos(cosAngle);

                    let baseAngle = Math.atan2(dy, dx);
                    let midAngle = baseAngle + (bendDir * angle);

                    let midX = startJoint.x + Math.cos(midAngle) * l;
                    let midY = startJoint.y + Math.sin(midAngle) * l;

                    // Draw Outline
                    ctx.beginPath();
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';
                    ctx.lineWidth = width;
                    ctx.strokeStyle = outlineCol;
                    ctx.moveTo(startJoint.x, startJoint.y);
                    ctx.lineTo(midX, midY);
                    ctx.lineTo(endJoint.x, endJoint.y);
                    ctx.stroke();

                    // Draw Fill
                    ctx.beginPath();
                    ctx.lineWidth = width - 2;
                    ctx.strokeStyle = fillCol;
                    ctx.moveTo(startJoint.x, startJoint.y);
                    ctx.lineTo(midX, midY);
                    ctx.lineTo(endJoint.x, endJoint.y);
                    ctx.stroke();

                    // Tattoos on Upper Arm
                    if (hasTattoo && tattoo !== 'none') {
                        ctx.strokeStyle = 'rgba(0,0,0,0.5)';
                        if (tattoo === 'tribal_band') {
                            ctx.lineWidth = 3;
                            let tX = startJoint.x + Math.cos(midAngle) * (l*0.4);
                            let tY = startJoint.y + Math.sin(midAngle) * (l*0.4);
                            let tX2 = startJoint.x + Math.cos(midAngle) * (l*0.5);
                            let tY2 = startJoint.y + Math.sin(midAngle) * (l*0.5);
                            ctx.beginPath();
                            ctx.moveTo(tX, tY);
                            ctx.lineTo(tX2, tY2);
                            ctx.stroke();
                        }
                    }
                };

                const armLength = 75 * h;
                const legLength = 80 * h;

                // Back Arm (Bicep mutated)
                let bBend = this.state === 'dodge' ? f : -f; // Bend direction
                drawDetailedLimb(t.neck, t.bHand, bBend, armLength, bicepW, outline, skin, true);

                // Back Glove
                ctx.fillStyle = gloves;
                ctx.strokeStyle = outline;
                ctx.lineWidth = 2;
                ctx.beginPath();
                if (gType === 'mma') {
                    ctx.arc(t.bHand.x, t.bHand.y, 8, 0, Math.PI*2);
                } else {
                    ctx.arc(t.bHand.x, t.bHand.y, 12, 0, Math.PI*2); // Boxing
                }
                ctx.fill(); ctx.stroke();

                // Back Leg
                drawDetailedLimb(t.pelvis, t.bFoot, f, legLength, 12, outline, skin);

                // Torso (Traps and Chest mutated)
                ctx.fillStyle = skin;
                ctx.strokeStyle = outline;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(t.neck.x - trapsW, t.neck.y); // Traps left
                ctx.lineTo(t.neck.x + trapsW, t.neck.y); // Traps right
                ctx.lineTo(t.pelvis.x + chestW/2, t.pelvis.y); // Hip right
                ctx.lineTo(t.pelvis.x - chestW/2, t.pelvis.y); // Hip left
                ctx.closePath();
                ctx.fill(); ctx.stroke();

                // Chest Tattoo
                if (tattoo === 'chest_piece') {
                    ctx.fillStyle = 'rgba(0,0,0,0.4)';
                    ctx.beginPath();
                    ctx.moveTo(t.neck.x, t.neck.y + 10);
                    ctx.lineTo(t.neck.x - trapsW*0.6, t.neck.y + 25);
                    ctx.lineTo(t.neck.x, t.neck.y + 40);
                    ctx.lineTo(t.neck.x + trapsW*0.6, t.neck.y + 25);
                    ctx.closePath();
                    ctx.fill();
                }

                // Six Pack (Stamina Mutation)
                if (hasAbs && this.state !== 'ko') {
                    ctx.strokeStyle = outline;
                    ctx.lineWidth = 1.5;
                    ctx.globalAlpha = 0.5;
                    let absY = t.neck.y + 35;
                    ctx.beginPath();
                    // Center line
                    ctx.moveTo(t.neck.x, absY); ctx.lineTo(t.pelvis.x, t.pelvis.y - 5);
                    // Horizontal lines
                    ctx.moveTo(t.neck.x - 5, absY + 5); ctx.lineTo(t.neck.x + 5, absY + 5);
                    ctx.moveTo(t.neck.x - 6, absY + 15); ctx.lineTo(t.neck.x + 6, absY + 15);
                    ctx.stroke();
                    ctx.globalAlpha = 1.0;
                }

                // Shorts
                ctx.fillStyle = shorts;
                ctx.beginPath();
                ctx.moveTo(t.pelvis.x - chestW/2 - 2, t.pelvis.y - 10*h);
                ctx.lineTo(t.pelvis.x + chestW/2 + 2, t.pelvis.y - 10*h);
                ctx.lineTo(t.pelvis.x + chestW/2, t.pelvis.y + 20*h);
                ctx.lineTo(t.pelvis.x - chestW/2, t.pelvis.y + 20*h);
                ctx.closePath();
                ctx.fill(); ctx.stroke();

                // Head
                ctx.fillStyle = skin;
                ctx.beginPath();
                const headRadius = 16 * ((h+w)/2);
                ctx.arc(t.head.x, t.head.y, headRadius, 0, Math.PI*2);
                ctx.fill(); ctx.stroke();

                // Hair Rendering
                const hStyle = app.hairstyle || 'bald';
                if (hStyle !== 'bald') {
                    ctx.fillStyle = app.haircolor || '#000000';
                    if (hStyle === 'short') {
                        ctx.beginPath();
                        ctx.arc(t.head.x, t.head.y - headRadius*0.2, headRadius*1.05, Math.PI, 2*Math.PI);
                        ctx.fill();
                    } else if (hStyle === 'mohawk') {
                        ctx.beginPath();
                        ctx.moveTo(t.head.x - headRadius*0.4, t.head.y - headRadius*0.7);
                        ctx.lineTo(t.head.x, t.head.y - headRadius*2.2);
                        ctx.lineTo(t.head.x + headRadius*0.4, t.head.y - headRadius*0.7);
                        ctx.fill();
                    } else if (hStyle === 'afro') {
                        ctx.beginPath();
                        ctx.arc(t.head.x, t.head.y - headRadius*0.6, headRadius*1.5, 0, Math.PI*2);
                        ctx.fill();
                    } else if (hStyle === 'spiky') {
                        ctx.beginPath();
                        for(let s = -1; s <= 1; s += 0.5) {
                            ctx.moveTo(t.head.x + s*headRadius*0.9, t.head.y - headRadius*0.4);
                            ctx.lineTo(t.head.x + (s+0.2)*headRadius*1.2, t.head.y - headRadius*1.8);
                            ctx.lineTo(t.head.x + (s+0.4)*headRadius*0.9, t.head.y - headRadius*0.4);
                        }
                        ctx.fill();
                    }
                }

                // Facial Hair
                if (fHair !== 'none') {
                    ctx.fillStyle = app.haircolor || '#000000';
                    let faceX = t.head.x + (f * headRadius * 0.7); // Front of face
                    let faceY = t.head.y;

                    if (fHair === 'beard') {
                        ctx.beginPath();
                        ctx.arc(t.head.x, t.head.y, headRadius*1.1, 0, Math.PI); // Bottom half of face
                        ctx.fill();
                    } else if (fHair === 'mustache') {
                        ctx.beginPath();
                        ctx.ellipse(faceX, faceY + headRadius*0.2, headRadius*0.5, headRadius*0.15, 0, 0, Math.PI*2);
                        ctx.fill();
                    } else if (fHair === 'goatee') {
                        ctx.beginPath();
                        ctx.arc(faceX, faceY + headRadius*0.6, headRadius*0.3, 0, Math.PI*2);
                        ctx.fill();
                    }
                }

                // Front Leg
                drawDetailedLimb(t.pelvis, t.fFoot, f, legLength, 12, outline, skin);

                // Front Arm (Bicep mutated)
                let fBend = f;
                if (this.state === 'block') fBend = -f;
                drawDetailedLimb(t.neck, t.fHand, fBend, armLength, bicepW, outline, skin, true);

                // Front Glove
                ctx.fillStyle = gloves;
                ctx.strokeStyle = outline;
                ctx.lineWidth = 2;
                ctx.beginPath();
                if (gType === 'mma') {
                    ctx.arc(t.fHand.x, t.fHand.y, 8, 0, Math.PI*2);
                } else {
                    ctx.arc(t.fHand.x, t.fHand.y, 13, 0, Math.PI*2);
                }
                ctx.fill(); ctx.stroke();
"""

    content = content[:render_start] + new_render_code + content[render_end:]

replace_draw_function()

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
