import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# We want to replace the torso, head, and facial features.
# Let's target the exact block we extracted earlier.
# Search for: // Draw Neck ... to end of // Battle Damage

start_marker = "// Draw Neck"
end_marker = "// Front Leg"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find body section to replace.")
    exit(1)

new_body_code = """// Draw Neck
                ctx.fillStyle = skin;
                ctx.strokeStyle = outline;
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(t.neck.x - neckW/2, t.neck.y + 10*h);
                ctx.quadraticCurveTo(t.neck.x - neckW*0.3, t.neck.y - 5*h, t.head.x - neckW*0.2, t.head.y + headRadius*0.6);
                ctx.lineTo(t.head.x + neckW*0.6, t.head.y + headRadius*0.6);
                ctx.quadraticCurveTo(t.neck.x + neckW*0.4, t.neck.y - 5*h, t.neck.x + neckW/2, t.neck.y + 10*h);
                ctx.closePath();
                ctx.fill(); ctx.stroke();

                // Draw Torso (More sculpted, realistic pecs/lats)
                ctx.beginPath();
                let upperChestW = chestW * 1.05;
                let waistW = hipW * 0.9;

                // Left shoulder/lat
                ctx.moveTo(t.neck.x - trapsW, t.neck.y);
                let midY = (t.neck.y + t.pelvis.y) / 2;
                // Lat spread curve
                ctx.bezierCurveTo(t.neck.x - upperChestW/2, t.neck.y + 15*h,
                                  t.neck.x - waistW/2, midY,
                                  t.pelvis.x - hipW/2, t.pelvis.y);
                // Beltline
                ctx.lineTo(t.pelvis.x + hipW/2, t.pelvis.y);
                // Right lat/shoulder
                ctx.bezierCurveTo(t.neck.x + waistW/2, midY,
                                  t.neck.x + upperChestW/2, t.neck.y + 15*h,
                                  t.neck.x + trapsW, t.neck.y);
                // Traps bridging to neck
                ctx.quadraticCurveTo(t.neck.x, t.neck.y - 10*h, t.neck.x - trapsW, t.neck.y);
                ctx.closePath();
                ctx.fill(); ctx.stroke();

                // Draw Pecs (Pectoralis Major)
                ctx.strokeStyle = outline;
                ctx.lineWidth = 1.5;
                ctx.globalAlpha = 0.5;
                ctx.beginPath();
                let pecY = t.neck.y + 25*h;
                let pecDrop = 12*h;
                // Left Pec
                ctx.moveTo(t.neck.x, pecY);
                ctx.quadraticCurveTo(t.neck.x - upperChestW*0.3, pecY + pecDrop, t.neck.x - upperChestW*0.4, t.neck.y + 12*h);
                // Right Pec
                ctx.moveTo(t.neck.x, pecY);
                ctx.quadraticCurveTo(t.neck.x + upperChestW*0.3, pecY + pecDrop, t.neck.x + upperChestW*0.4, t.neck.y + 12*h);
                // Cleavage line
                ctx.moveTo(t.neck.x, t.neck.y + 10*h);
                ctx.lineTo(t.neck.x, pecY);
                ctx.stroke();
                ctx.globalAlpha = 1.0;

                // Chest Tattoo
                if (tattoo === 'chest_piece') {
                    ctx.fillStyle = 'rgba(0,0,0,0.4)';
                    ctx.beginPath();
                    ctx.moveTo(t.neck.x, t.neck.y + 10);
                    ctx.quadraticCurveTo(t.neck.x - trapsW*0.5, t.neck.y + 15, t.neck.x - trapsW*0.6, t.neck.y + 25);
                    ctx.quadraticCurveTo(t.neck.x, t.neck.y + 35, t.neck.x, t.neck.y + 40);
                    ctx.quadraticCurveTo(t.neck.x, t.neck.y + 35, t.neck.x + trapsW*0.6, t.neck.y + 25);
                    ctx.quadraticCurveTo(t.neck.x + trapsW*0.5, t.neck.y + 15, t.neck.x, t.neck.y + 10);
                    ctx.closePath();
                    ctx.fill();
                }

                // Six Pack (Stamina Mutation) - more realistic sculpted abs
                if (hasAbs && this.state !== 'ko') {
                    ctx.strokeStyle = outline;
                    ctx.lineWidth = 1.5;
                    ctx.globalAlpha = 0.4;
                    let absTop = t.neck.y + 32*h;
                    let absBottom = t.pelvis.y - 8*h;
                    ctx.beginPath();
                    // Linea alba (center line)
                    ctx.moveTo(t.neck.x, absTop);
                    ctx.lineTo(t.pelvis.x, absBottom);

                    let absW = hipW * 0.25;
                    let numAbs = 3;
                    let absSpacing = (absBottom - absTop) / numAbs;

                    for(let i=1; i<numAbs; i++) {
                        let y = absTop + (i * absSpacing);
                        // Left block curve
                        ctx.moveTo(t.neck.x, y);
                        ctx.quadraticCurveTo(t.neck.x - absW, y - 3*h, t.neck.x - absW*1.2, y + 2*h);
                        // Right block curve
                        ctx.moveTo(t.neck.x, y);
                        ctx.quadraticCurveTo(t.neck.x + absW, y - 3*h, t.neck.x + absW*1.2, y + 2*h);
                    }
                    ctx.stroke();
                    ctx.globalAlpha = 1.0;
                }

                // Shorts
                ctx.fillStyle = shorts;
                ctx.beginPath();
                ctx.moveTo(t.pelvis.x - hipW/2 - 2, t.pelvis.y - 10*h);
                ctx.lineTo(t.pelvis.x + hipW/2 + 2, t.pelvis.y - 10*h);
                // Curve the bottom of the shorts for a 3D feel
                ctx.lineTo(t.pelvis.x + hipW/2, t.pelvis.y + 20*h);
                ctx.quadraticCurveTo(t.pelvis.x, t.pelvis.y + 25*h, t.pelvis.x - hipW/2, t.pelvis.y + 20*h);
                ctx.closePath();
                ctx.fill(); ctx.stroke();

                // Draw Head with More Complex/Realistic Side Profile
                ctx.fillStyle = skin;
                ctx.strokeStyle = outline;
                ctx.lineWidth = 2;
                ctx.beginPath();

                let hrX = headRadius * 0.9; // Horizontal radius
                let hrY = headRadius * 1.05; // Vertical radius

                // Start at top of forehead
                ctx.moveTo(t.head.x, t.head.y - hrY);
                // Back of head curve
                ctx.bezierCurveTo(t.head.x - (f*hrX*1.2), t.head.y - hrY,
                                  t.head.x - (f*hrX*1.2), t.head.y + hrY*0.6,
                                  t.head.x - (f*hrX*0.4), t.head.y + hrY*0.9);
                // Neck/Jaw transition
                ctx.lineTo(t.head.x, t.head.y + hrY);

                // Front profile: Chin, Mouth, Nose, Brow
                let chinLevel = this.stats.chinSize || 0;
                let chinExt = f * (hrX * 0.2 + (chinLevel * 3 * w));
                let chinDrop = hrY * 0.1 + (chinLevel * 2 * h);

                // Jaw to Chin
                ctx.lineTo(t.head.x + (f*hrX*0.3) + chinExt, t.head.y + hrY + chinDrop);
                // Chin to Lower Lip
                ctx.quadraticCurveTo(t.head.x + (f*hrX*0.5) + chinExt, t.head.y + hrY*0.8,
                                     t.head.x + (f*hrX*0.7), t.head.y + hrY*0.6);
                // Lips
                ctx.lineTo(t.head.x + (f*hrX*0.8), t.head.y + hrY*0.5); // Upper lip
                // Nose
                ctx.lineTo(t.head.x + (f*hrX*1.1), t.head.y + hrY*0.2); // Nose tip
                ctx.lineTo(t.head.x + (f*hrX*0.8), t.head.y); // Nose bridge
                // Brow ridge
                ctx.quadraticCurveTo(t.head.x + (f*hrX*0.9), t.head.y - hrY*0.2,
                                     t.head.x + (f*hrX*0.7), t.head.y - hrY*0.4);
                // Forehead up to top
                ctx.quadraticCurveTo(t.head.x + (f*hrX*0.5), t.head.y - hrY,
                                     t.head.x, t.head.y - hrY);
                ctx.closePath();
                ctx.fill(); ctx.stroke();

                // Eye (Realistic almond shape)
                ctx.fillStyle = 'rgba(0,0,0,0.8)';
                ctx.beginPath();
                let eyeX = t.head.x + (f * hrX * 0.4);
                let eyeY = t.head.y - hrY * 0.1;
                let eyeW = hrX * 0.25;
                let eyeH = hrY * 0.1;
                ctx.ellipse(eyeX, eyeY, eyeW, eyeH, f === 1 ? Math.PI*0.1 : -Math.PI*0.1, 0, Math.PI*2);
                ctx.fill();

                // Eyebrow
                ctx.strokeStyle = app.haircolor || '#000';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(eyeX - (f*eyeW), eyeY - eyeH*1.5);
                ctx.quadraticCurveTo(eyeX, eyeY - eyeH*2, eyeX + (f*eyeW*1.2), eyeY - eyeH*1.2);
                ctx.stroke();

                // Hair Rendering
                const hStyle = app.hairstyle || 'bald';
                if (hStyle !== 'bald') {
                    ctx.fillStyle = app.haircolor || '#000000';
                    if (hStyle === 'short') {
                        ctx.beginPath();
                        let startA = f === 1 ? Math.PI*0.8 : Math.PI*0.2;
                        let endA = f === 1 ? Math.PI*2.1 : Math.PI*1.9;
                        ctx.arc(t.head.x - (f * headRadius*0.1), t.head.y - headRadius*0.2, headRadius*1.05, startA, endA);
                        ctx.fill();
                    } else if (hStyle === 'mohawk') {
                        ctx.beginPath();
                        ctx.moveTo(t.head.x + (f*headRadius*0.5), t.head.y - headRadius*0.8);
                        ctx.quadraticCurveTo(t.head.x, t.head.y - headRadius*2.5, t.head.x - (f*headRadius*0.8), t.head.y - headRadius*0.2);
                        ctx.quadraticCurveTo(t.head.x - (f*headRadius*0.4), t.head.y - headRadius*1.5, t.head.x + (f*headRadius*0.5), t.head.y - headRadius*0.8);
                        ctx.fill();
                    } else if (hStyle === 'afro') {
                        ctx.beginPath();
                        ctx.arc(t.head.x - (f*headRadius*0.2), t.head.y - headRadius*0.6, headRadius*1.4, 0, Math.PI*2);
                        // Add some bumpy texture to afro
                        for(let i=0; i<8; i++) {
                            let angle = (i/8) * Math.PI*2;
                            ctx.arc(t.head.x - (f*headRadius*0.2) + Math.cos(angle)*headRadius*1.2,
                                    t.head.y - headRadius*0.6 + Math.sin(angle)*headRadius*1.2,
                                    headRadius*0.4, 0, Math.PI*2);
                        }
                        ctx.fill();
                    } else if (hStyle === 'spiky') {
                        ctx.beginPath();
                        for(let s = -0.5; s <= 1; s += 0.4) {
                            let spikeX = t.head.x - (f * s * headRadius);
                            let spikeTipX = spikeX - (f * headRadius * 0.6);
                            ctx.moveTo(spikeX + headRadius*0.2, t.head.y - headRadius*0.6);
                            ctx.quadraticCurveTo(spikeTipX + (f*headRadius*0.2), t.head.y - headRadius*1.4, spikeTipX, t.head.y - headRadius*1.9);
                            ctx.quadraticCurveTo(spikeX, t.head.y - headRadius*1.0, spikeX - headRadius*0.2, t.head.y - headRadius*0.6);
                        }
                        ctx.fill();
                    }
                }

                // Facial Hair
                if (fHair !== 'none') {
                    ctx.fillStyle = app.haircolor || '#000000';
                    let chinY = t.head.y + hrY + chinDrop;
                    let faceFrontX = t.head.x + (f*hrX*0.7);

                    if (fHair === 'beard') {
                        ctx.beginPath();
                        ctx.moveTo(t.head.x + (f*hrX*0.2), t.head.y);
                        ctx.quadraticCurveTo(faceFrontX, t.head.y + hrY*0.5, t.head.x + (f*hrX*0.4) + chinExt, chinY + hrY*0.1);
                        ctx.lineTo(t.head.x, chinY);
                        ctx.quadraticCurveTo(t.head.x - (f*hrX*0.4), t.head.y + hrY*0.8, t.head.x - (f*hrX*0.2), t.head.y);
                        ctx.fill();
                    } else if (fHair === 'mustache') {
                        ctx.beginPath();
                        ctx.moveTo(faceFrontX - (f*hrX*0.2), t.head.y + hrY*0.3);
                        ctx.quadraticCurveTo(faceFrontX + (f*hrX*0.3), t.head.y + hrY*0.3, faceFrontX + (f*hrX*0.1), t.head.y + hrY*0.5);
                        ctx.lineTo(faceFrontX - (f*hrX*0.1), t.head.y + hrY*0.4);
                        ctx.fill();
                    } else if (fHair === 'goatee') {
                        ctx.beginPath();
                        ctx.arc(t.head.x + (f*hrX*0.4) + chinExt, chinY - hrY*0.1, hrY*0.3, 0, Math.PI*2);
                        ctx.fill();
                    }
                }

                // Battle Damage (Bruises and Bleeding based on HP percentage)
                let hpPercent = this.stats.hp / this.stats.maxHp;
                if (hpPercent < 0.7) {
                    let damageLevel = 1.0 - hpPercent;

                    // Body bruising
                    ctx.fillStyle = `rgba(75, 0, 130, ${damageLevel * 0.4})`;
                    ctx.beginPath();
                    ctx.ellipse(t.pelvis.x + (f * hipW*0.2), t.pelvis.y - 15*h, hipW*0.3, 10*h, 0, 0, Math.PI*2);
                    ctx.fill();

                    // Face bruising
                    ctx.fillStyle = `rgba(50, 0, 50, ${damageLevel * 0.5})`;
                    ctx.beginPath();
                    ctx.ellipse(eyeX, eyeY + eyeH*1.5, eyeW*1.5, eyeH*1.5, 0, 0, Math.PI*2);
                    ctx.fill();

                    if (hpPercent < 0.4) {
                        ctx.strokeStyle = `rgba(180, 0, 0, ${damageLevel * 0.8})`;
                        ctx.lineWidth = 2;
                        // From nose
                        ctx.beginPath();
                        ctx.moveTo(t.head.x + (f * hrX * 0.9), t.head.y + hrY*0.3);
                        ctx.quadraticCurveTo(t.head.x + (f * hrX * 0.8), t.head.y + hrY*0.6, t.head.x + (f * hrX * 0.6), t.head.y + hrY*0.8);
                        ctx.stroke();
                        // Chest streak
                        ctx.beginPath();
                        ctx.moveTo(t.neck.x + (f * trapsW * 0.4), t.neck.y + 10*h);
                        ctx.lineTo(t.pelvis.x + (f * hipW * 0.2), t.pelvis.y - 5*h);
                        ctx.stroke();
                    }
                }

                """

new_content = content[:start_idx] + new_body_code + content[end_idx:]

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(new_content)

print("Replaced body logic!")
