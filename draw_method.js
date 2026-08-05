            draw(ctx) {
                ctx.save();

                const app = this.stats.appearance || { h: 1, w: 1, skin: this.isPlayer ? '#e2e8f0' : '#4b5563', shorts: this.isPlayer ? '#3b82f6' : '#ef4444', gloves: this.isPlayer ? '#ef4444' : '#22c55e' };
                const h = app.h;
                const w = app.w;

                // Add a dynamic shadow to ground the fighters
                ctx.fillStyle = 'rgba(0,0,0,0.4)';
                ctx.beginPath();
                ctx.ellipse(this.x + this.width/2, ctx.canvas.height - 15, 35 * w, 8, 0, 0, Math.PI*2);
                ctx.fill();

                // Translate: Center X, align Y so feet hit the floor perfectly regardless of Height scale
                ctx.translate(this.x + this.width/2, (this.y + this.height) - (90 * h));

                // --- MUSCLE MUTATION MATH ---
                // The higher the stat goes over base (100 HP, 10 Pwr, 5 Def), the more visually massive they get
                let chestBase = 26; // Base width
                let hpBonus = Math.max(0, this.stats.maxHp - 100) * 0.15; // 20hp upgrade = +3 width
                let chestW = (chestBase + hpBonus) * w;

                let bicepBase = 10;
                let powerBonus = Math.max(0, this.stats.power - 10) * 1.5; // 3 pwr upgrade = +4.5 width
                let bicepW = (bicepBase + powerBonus) * w;

                let trapsBase = 12;
                let defBonus = Math.max(0, this.stats.defense - 5) * 1.5; // 2 def upgrade = +3 width
                let trapsW = (trapsBase + defBonus) * w;

                // Calculate new distinct muscle widths
                let neckW = 10 * w + (this.stats.neckGirth || 0) * 0.5;
                let deltoidW = 14 * w + (this.stats.deltoidSize || 0) * 1.2;
                let forearmW = 8 * w + (this.stats.forearmSize || 0) * 1.5;
                let thighW = 22 * w + (this.stats.thighSize || 0) * 0.4 + (this.stats.speedBonus || 0) * 3;
                let calfW = 14 * w + (this.stats.calfSize || 0) * 1.2 + (this.stats.speedBonus || 0) * 2;
                let jointW = 10 * w; // Base width for knees/elbows

                // Abs show if maxStamina is upgraded at least once (base is 100, upgrade is +15)
                let hasAbs = this.stats.maxStamina >= 115;

                // Color theme
                const skin = app.skin;
                const outline = 'rgba(0,0,0,0.6)'; // Universal dark outline
                const shorts = app.shorts;
                const gloves = app.gloves;

                const f = this.facing; // Facing multiplier

                // --- FLUID ANIMATION ENGINE ---
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

                // 3. Define Target Pose based on State
                let targetT = JSON.parse(JSON.stringify(baseT));
                let isAttack = false;
                let attackIntensity = 0;

                if (this.currentMove && this.state !== 'hit' && this.state !== 'ko' && this.state !== 'dodge' && this.state !== 'block') {
                    isAttack = true;
                    // Calculate animation progress (0 to 1)
                    let p = (this.currentMove.dur - this.stateTimer) / this.currentMove.dur;
                    // Sine wave creates natural ease-in / ease-out extension (0 -> 1 -> 0)
                    const animScale = this.isPowerAttack ? 1.0 : 0.6;
                    attackIntensity = Math.sin(p * Math.PI) * animScale;

                    if (this.state === 'jab') {
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
                    }} else if (this.state === 'block') {
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
                } else if (this.state === 'dodge' || this.state === 'duck') {
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
                } else if (this.state === 'hit') {
                    let p = (300 - this.stateTimer) / 300;
                    let hitIntensity = Math.pow(1 - p, 3); // Snaps back violently, recovers slowly
                    targetT.head.x -= 40*f*w * hitIntensity;
                    targetT.head.y -= 20*h * hitIntensity;
                    targetT.neck.x -= 25*f*w * hitIntensity;
                    targetT.pelvis.x -= 10*f*w * hitIntensity;
                    targetT.fHand.x -= 20*f*w * hitIntensity;
                    targetT.bHand.x -= 20*f*w * hitIntensity;
                } else if (this.state === 'ko') {
                    targetT.head = {x: -60*f, y: 80};
                    targetT.neck = {x: -40*f, y: 70};
                    targetT.pelvis = {x: 10*f, y: 75};
                    targetT.fHand = {x: -30*f, y: 85};
                    targetT.bHand = {x: 30*f, y: 85};
                    targetT.fFoot = {x: 70*f, y: 90};
                    targetT.bFoot = {x: 40*f, y: 90};
                    targetT.fKnee = {x: 50*f, y: 85};
                    targetT.bKnee = {x: 20*f, y: 85};
                }

                // Dynamically extend attack visuals based on limbMod so it matches hitbox reach and prevents bunching
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
                if (isAttack) {
                    for (let joint in targetT) {
                        targetT[joint].x = lerp(baseT[joint].x, targetT[joint].x, attackIntensity);
                        targetT[joint].y = lerp(baseT[joint].y, targetT[joint].y, attackIntensity);
                    }
                }

                // Smoothly Lerp Actual Current Joints to the Target Joints every frame
                let smoothFactor = this.state === 'ko' ? 0.08 : 0.35;
                for (let joint in this.joints) {
                    this.joints[joint].x = lerp(this.joints[joint].x, targetT[joint].x, smoothFactor);
                    this.joints[joint].y = lerp(this.joints[joint].y, targetT[joint].y, smoothFactor);
                }

                let t = this.joints; // Pass finalized smoothed joints to renderer

                // Helper to draw a capsule (limbs)
                const drawCapsule = (p1, p2, width, color) => {
                    ctx.beginPath();
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';
                    ctx.lineWidth = width;
                    ctx.strokeStyle = color;
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                };

                // --- RENDER ORDER (Back to Front) ---

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
                    let botchedLevel = app.limbLengthMod ? Math.floor(app.limbLengthMod / 20) : 0;
                    let jiggleX = 0; let jiggleY = 0;
                    if (botchedLevel > 0 && this.state !== 'ko') {
                        jiggleX = (Math.random() - 0.5) * botchedLevel * 2;
                        jiggleY = (Math.random() - 0.5) * botchedLevel * 2;
                    }

                    let dx = endJoint.x - startJoint.x;
                    let dy = endJoint.y - startJoint.y;
                    let dist = Math.sqrt(dx*dx + dy*dy);

                    if (dist > limbLength) {
                        dx = (dx / dist) * limbLength;
                        dy = (dy / dist) * limbLength;
                        dist = limbLength;
                    }

                    let l = limbLength / 2;
                    let cosAngle = (dist*dist) / (2 * l * dist);
                    if (cosAngle > 1) cosAngle = 1;
                    let angle = Math.acos(cosAngle);

                    let baseAngle = Math.atan2(dy, dx);
                    let midAngle = baseAngle + (bendDir * angle);

                    let midX = startJoint.x + Math.cos(midAngle) * l + jiggleX;
                    let midY = startJoint.y + Math.sin(midAngle) * l + jiggleY;

                    // Tapered limbs: Upper limb is full width, lower limb is slightly thinner (0.8x)
                    let lowerWidth = width * 0.75;

                    // Helper to draw a segment
                    const drawSegment = (p1x, p1y, p2x, p2y, w, col, isFill) => {
                        ctx.beginPath();
                        ctx.lineCap = 'round';
                        ctx.lineJoin = 'round';
                        ctx.lineWidth = isFill ? w - 2 : w;
                        ctx.strokeStyle = col;
                        ctx.moveTo(p1x, p1y);
                        ctx.lineTo(p2x, p2y);
                        ctx.stroke();
                    };

                    // Draw Outline
                    drawSegment(startJoint.x, startJoint.y, midX, midY, width, outlineCol, false);
                    drawSegment(midX, midY, endJoint.x, endJoint.y, lowerWidth, outlineCol, false);

                    // Draw Fill (using arc trick to make a smooth elbow/knee joint)
                    drawSegment(startJoint.x, startJoint.y, midX, midY, width, fillCol, true);

                    // Draw a circle at the joint to smooth the transition
                    ctx.fillStyle = fillCol;
                    ctx.beginPath();
                    ctx.arc(midX, midY, (width-2)/2, 0, Math.PI*2);
                    ctx.fill();

                    drawSegment(midX, midY, endJoint.x, endJoint.y, lowerWidth, fillCol, true);

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
                    } // Fixed missing brace here

                    // Botched Stitches!
                    if (botchedLevel > 0) {
                        ctx.strokeStyle = 'red';
                        ctx.lineWidth = 1.5;
                        ctx.beginPath();
                        ctx.moveTo(midX - width/2, midY - 5);
                        ctx.lineTo(midX + width/2, midY + 5);
                        ctx.moveTo(midX - width/2, midY + 5);
                        ctx.lineTo(midX + width/2, midY - 5);
                        ctx.stroke();

                        if (botchedLevel > 1) {
                            ctx.fillStyle = 'silver';
                            ctx.fillRect(midX - 3, midY - 15, 6, 30);
                            ctx.strokeRect(midX - 3, midY - 15, 6, 30);
                        }
                    }
                };

                const armLength = (75 * h) + (app.limbLengthMod || 0);
                const legLength = (80 * h) + (app.limbLengthMod || 0);

                // Back Arm (Bicep mutated)
                let bBend = f; // Bend backwards (elbows back)
                drawDetailedLimb(t.neck, t.bHand, bBend, armLength, bicepW, forearmW, jointW, deltoidW, outline, skin, true);

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
                drawDetailedLimb(t.pelvis, t.bFoot, -f, legLength, thighW, calfW, jointW, 0, outline, skin);

                // Torso and Neck
                let hipW = Math.max(20, chestW * 0.85);

                // Draw Neck
                ctx.fillStyle = skin;
                ctx.strokeStyle = outline;
                ctx.lineWidth = 2;
                ctx.beginPath();
                // Neck connects t.neck to base of head
                ctx.moveTo(t.neck.x - neckW/2, t.neck.y + 5*h);
                ctx.lineTo(t.neck.x + neckW/2, t.neck.y + 5*h);
                ctx.lineTo(t.head.x + neckW/2, t.head.y);
                ctx.lineTo(t.head.x - neckW/2, t.head.y);
                ctx.closePath();
                ctx.fill(); ctx.stroke();

                // Draw Torso
                ctx.beginPath();
                ctx.moveTo(t.neck.x - trapsW, t.neck.y);
                ctx.lineTo(t.neck.x + trapsW, t.neck.y);
                let midY = (t.neck.y + t.pelvis.y) / 2;
                ctx.quadraticCurveTo(t.neck.x + trapsW*0.9, midY, t.pelvis.x + hipW/2, t.pelvis.y);
                ctx.lineTo(t.pelvis.x - hipW/2, t.pelvis.y);
                ctx.quadraticCurveTo(t.neck.x - trapsW*0.9, midY, t.neck.x - trapsW, t.neck.y);
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
                ctx.moveTo(t.pelvis.x - hipW/2 - 2, t.pelvis.y - 10*h);
                ctx.lineTo(t.pelvis.x + hipW/2 + 2, t.pelvis.y - 10*h);
                ctx.lineTo(t.pelvis.x + hipW/2, t.pelvis.y + 20*h);
                ctx.lineTo(t.pelvis.x - hipW/2, t.pelvis.y + 20*h);
                ctx.closePath();
                ctx.fill(); ctx.stroke();

                // Head
                ctx.fillStyle = skin;
                ctx.beginPath();
                const headRadius = 16 * ((h+w)/2);
                // Make the head slightly oval to better represent a side profile
                ctx.ellipse(t.head.x, t.head.y, headRadius*0.95, headRadius*1.1, 0, 0, Math.PI*2);
                ctx.fill(); ctx.stroke();

                // Mega Chad Chin
                let chinLevel = this.stats.chinSize || 0;
                if (chinLevel > 0) {
                    ctx.fillStyle = skin;
                    ctx.strokeStyle = outline;
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    // Extend chin forward and down
                    let chinW = headRadius * 0.5 + (chinLevel * 3 * w);
                    let chinH = headRadius * 0.3 + (chinLevel * 2 * h);

                    let startX = t.head.x + (f * headRadius * 0.3);
                    let startY = t.head.y + headRadius * 0.5;

                    ctx.moveTo(startX, startY);
                    ctx.lineTo(startX + (f * chinW), startY);
                    ctx.lineTo(startX + (f * chinW * 0.9), startY + chinH);
                    ctx.lineTo(t.head.x, startY + chinH * 0.8);
                    ctx.closePath();
                    ctx.fill(); ctx.stroke();
                }

                // Eye (to establish side profile)
                ctx.fillStyle = 'rgba(0,0,0,0.8)';
                ctx.beginPath();
                // Place eye on the front half of the face
                let eyeX = t.head.x + (f * headRadius * 0.4);
                let eyeY = t.head.y - headRadius * 0.1;
                ctx.arc(eyeX, eyeY, headRadius*0.15, 0, Math.PI*2);
                ctx.fill();

                // Hair Rendering (adjusted for side profile)
                const hStyle = app.hairstyle || 'bald';
                if (hStyle !== 'bald') {
                    ctx.fillStyle = app.haircolor || '#000000';
                    if (hStyle === 'short') {
                        ctx.beginPath();
                        // Hair hugs the top and back of the head
                        let startA = f === 1 ? Math.PI*0.8 : Math.PI*0.2;
                        let endA = f === 1 ? Math.PI*2.1 : Math.PI*1.9;
                        ctx.arc(t.head.x - (f * headRadius*0.1), t.head.y - headRadius*0.2, headRadius*1.05, startA, endA);
                        ctx.fill();
                    } else if (hStyle === 'mohawk') {
                        ctx.beginPath();
                        // Mohawk spans from front-top to back-bottom
                        ctx.moveTo(t.head.x + (f*headRadius*0.5), t.head.y - headRadius*0.8);
                        ctx.lineTo(t.head.x, t.head.y - headRadius*2.2);
                        ctx.lineTo(t.head.x - (f*headRadius*0.8), t.head.y - headRadius*0.2);
                        ctx.fill();
                    } else if (hStyle === 'afro') {
                        ctx.beginPath();
                        // Shift afro slightly back for side profile
                        ctx.arc(t.head.x - (f*headRadius*0.2), t.head.y - headRadius*0.6, headRadius*1.4, 0, Math.PI*2);
                        ctx.fill();
                    } else if (hStyle === 'spiky') {
                        ctx.beginPath();
                        // Spikes angled backward
                        for(let s = -0.5; s <= 1; s += 0.4) {
                            let spikeX = t.head.x - (f * s * headRadius);
                            let spikeTipX = spikeX - (f * headRadius * 0.5);
                            ctx.moveTo(spikeX + headRadius*0.2, t.head.y - headRadius*0.6);
                            ctx.lineTo(spikeTipX, t.head.y - headRadius*1.8);
                            ctx.lineTo(spikeX - headRadius*0.2, t.head.y - headRadius*0.6);
                        }
                        ctx.fill();
                    }
                }

                // Facial Hair (adjusted for side profile)
                if (fHair !== 'none') {
                    ctx.fillStyle = app.haircolor || '#000000';
                    let faceFrontX = t.head.x + (f * headRadius * 0.9);
                    let chinY = t.head.y + headRadius * 0.9;
                    let jawX = t.head.x;

                    if (fHair === 'beard') {
                        // Traces jawline and chin
                        ctx.beginPath();
                        ctx.moveTo(t.head.x + (f*headRadius*0.2), t.head.y);
                        ctx.lineTo(faceFrontX, t.head.y + headRadius*0.5);
                        ctx.lineTo(t.head.x + (f*headRadius*0.5), chinY + headRadius*0.2);
                        ctx.lineTo(jawX - (f*headRadius*0.2), t.head.y + headRadius*0.8);
                        ctx.lineTo(t.head.x - (f*headRadius*0.1), t.head.y + headRadius*0.2);
                        ctx.fill();
                    } else if (fHair === 'mustache') {
                        // Simple angled line above mouth
                        ctx.beginPath();
                        ctx.ellipse(faceFrontX - (f*headRadius*0.1), t.head.y + headRadius*0.4, headRadius*0.4, headRadius*0.1, f === 1 ? Math.PI*0.1 : -Math.PI*0.1, 0, Math.PI*2);
                        ctx.fill();
                    } else if (fHair === 'goatee') {
                        // Just on the chin
                        ctx.beginPath();
                        ctx.arc(t.head.x + (f*headRadius*0.7), chinY, headRadius*0.35, 0, Math.PI*2);
                        ctx.fill();
                    }
                }

                // Battle Damage (Bruises and Bleeding based on HP percentage)
                let hpPercent = this.stats.hp / this.stats.maxHp;
                if (hpPercent < 0.7) {
                    let damageLevel = 1.0 - hpPercent; // 0.3 at 70%, 0.9 at 10%

                    // Body bruising
                    ctx.fillStyle = `rgba(75, 0, 130, ${damageLevel * 0.4})`; // Purple bruise
                    ctx.beginPath();
                    ctx.ellipse(t.pelvis.x + (f * hipW*0.2), t.pelvis.y - 15*h, hipW*0.3, 10*h, 0, 0, Math.PI*2); // Ribs
                    ctx.fill();

                    // Face bruising (black eye / swollen cheek)
                    ctx.fillStyle = `rgba(50, 0, 50, ${damageLevel * 0.5})`;
                    ctx.beginPath();
                    ctx.arc(t.head.x + (f * headRadius * 0.5), t.head.y, headRadius*0.3, 0, Math.PI*2);
                    ctx.fill();

                    if (hpPercent < 0.4) {
                        // Blood trickles
                        ctx.strokeStyle = `rgba(180, 0, 0, ${damageLevel * 0.8})`;
                        ctx.lineWidth = 2;

                        // From nose/mouth
                        ctx.beginPath();
                        ctx.moveTo(t.head.x + (f * headRadius * 0.8), t.head.y + headRadius*0.2);
                        ctx.lineTo(t.head.x + (f * headRadius * 0.6), t.head.y + headRadius*0.7);
                        ctx.stroke();

                        // From eye
                        ctx.beginPath();
                        ctx.moveTo(t.head.x + (f * headRadius * 0.4), t.head.y + headRadius*0.1);
                        ctx.lineTo(t.head.x + (f * headRadius * 0.2), t.head.y + headRadius*0.8);
                        ctx.stroke();

                        // Chest streak
                        ctx.beginPath();
                        ctx.moveTo(t.neck.x + (f * trapsW * 0.4), t.neck.y + 10*h);
                        ctx.lineTo(t.pelvis.x + (f * hipW * 0.2), t.pelvis.y - 5*h);
                        ctx.stroke();
                    }
                }

                // Front Leg
                drawDetailedLimb(t.pelvis, t.fFoot, -f, legLength, thighW, calfW, jointW, 0, outline, skin);

                // Front Arm (Bicep mutated)
                let fBend = f; // Bend backwards (elbows back)
                drawDetailedLimb(t.neck, t.fHand, fBend, armLength, bicepW, forearmW, jointW, deltoidW, outline, skin, true);

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
ctx.restore();
            }