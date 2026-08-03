
        // --- GAME DATA & STATE ---
        let playerStats = {
            hp: 100, maxHp: 100,
            power: 10,
            defense: 5,
            stamina: 100, maxStamina: 100, staminaRegen: 15,
            money: 0, rank: 0,
            appearance: { h: 1.0, w: 1.0, skin: '#e2e8f0', shorts: '#3b82f6', gloves: '#ef4444', hairstyle: 'short', haircolor: '#000000' }
        };

        const upgradeCosts = {
            maxHp: { base: 50, mult: 1.4, name: "Max Health (Chest Width)", val: 20 },
            power: { base: 60, mult: 1.5, name: "Power (Bicep Size)", val: 3 },
            defense: { base: 40, mult: 1.4, name: "Defense (Traps Size)", val: 2 },
            maxStamina: { base: 40, mult: 1.3, name: "Max Stamina (Abs)", val: 15 },
            staminaRegen: { base: 50, mult: 1.5, name: "Cardio", val: 3 },
            botchedSurgery: { base: 200, mult: 2.0, name: "Botched Limb Lengthening (-Stamina)", val: 1 }
        };

        let upgradeLevels = { maxHp: 0, power: 0, defense: 0, maxStamina: 0, staminaRegen: 0, botchedSurgery: 0 };

        const opponents = [
            { name: "Glass Joe", desc: "A weak local amateur.", stats: { maxHp: 80, power: 5, defense: 2, maxStamina: 80, staminaRegen: 10, appearance: { h: 0.85, w: 0.8, skin: '#fcd34d', shorts: '#ef4444', gloves: '#3b82f6', hairstyle: 'short', haircolor: '#fbbf24' } }, reward: 100 },
            { name: "Iron Mike", desc: "Hits hard, but gasses out quick.", stats: { maxHp: 120, power: 18, defense: 5, maxStamina: 90, staminaRegen: 8, appearance: { h: 0.95, w: 1.15, skin: '#b45309', shorts: '#000000', gloves: '#ef4444', hairstyle: 'bald', haircolor: '#000000' } }, reward: 250 },
            { name: "Slippery Pete", desc: "Fast and elusive kickboxer.", stats: { maxHp: 110, power: 12, defense: 10, maxStamina: 150, staminaRegen: 25, appearance: { h: 1.1, w: 0.9, skin: '#fca5a5', shorts: '#10b981', gloves: '#eab308', hairstyle: 'afro', haircolor: '#451a03' } }, reward: 500 },
            { name: "The Crusher", desc: "A massive, immovable object.", stats: { maxHp: 250, power: 25, defense: 20, maxStamina: 120, staminaRegen: 12, appearance: { h: 1.2, w: 1.4, skin: '#cbd5e1', shorts: '#1e3a8a', gloves: '#000000', hairstyle: 'mohawk', haircolor: '#dc2626' } }, reward: 1000 },
            { name: "The Reaper", desc: "The Undisputed Champion.", stats: { maxHp: 350, power: 35, defense: 30, maxStamina: 200, staminaRegen: 30, appearance: { h: 1.05, w: 1.1, skin: '#111827', shorts: '#7f1d1d', gloves: '#dc2626', hairstyle: 'spiky', haircolor: '#ffffff' } }, reward: 5000 }
        ];

        // --- ENGINE VARIABLES ---
        const canvas = document.getElementById('game-canvas');
        const ctx = canvas.getContext('2d');
        let pFighter, oFighter;
        let lastTime = 0;
        let gameLoopId;
        const keys = { w: false, a: false, s: false, d: false, u: false, i: false, j: false, k: false, o: false, shift: false };
        let pComboCount = 0, oComboCount = 0;
        let lastHitTime = 0;
        const state = { inFight: false };

        // --- INPUT HANDLING (Fixed the S key and Boolean flipping) ---
        window.addEventListener('keydown', (e) => {
            if(!state.inFight) return;
            let key = e.key.toLowerCase();
            if (e.key === 'Shift') key = 'shift';

            if (keys.hasOwnProperty(key)) {
                keys[key] = true; // MUST BE TRUE
            }
        });

        window.addEventListener('keyup', (e) => {
            let key = e.key.toLowerCase();
            if (e.key === 'Shift') key = 'shift';

            if (keys.hasOwnProperty(key)) {
                keys[key] = false; // MUST BE FALSE
                if (['u','i','j','k','s'].includes(key) && pFighter) {
                    pFighter.keyReleased = true; // Allow next action
                }
            }
        });

        // --- MATH & UTILS ---
        function lerp(start, end, amt) {
            return (1 - amt) * start + amt * end;
        }

        // --- FIGHTER CLASS (Includes 2.5D Renderer & Muscles) ---
        class Fighter {
            constructor(x, y, facing, stats, isPlayer) {
                this.x = x;
                this.y = y;
                this.facing = facing; // 1 for right, -1 for left
                this.stats = JSON.parse(JSON.stringify(stats));
                this.stats.hp = this.stats.maxHp;
                this.stats.stamina = this.stats.maxStamina;
                this.isPlayer = isPlayer;

                const app = this.stats.appearance || { h: 1, w: 1 };
                const hScale = app.h || 1;
                const wScale = app.w || 1;

                // Height affects hitboxes (width/height) and reach (via a multiplier in combat logic)
                this.width = 60 * hScale;
                this.height = 180 * hScale;
                this.limbMod = app.limbLengthMod || 0;


                // Speed is inversely proportional to weight. Heavier = slower. Taller = slightly slower to get moving.
                // Base speed is 4.
                this.speed = 4 * (1 / wScale) * (1 / ((hScale - 1) * 0.5 + 1));

                // Power is amplified by weight.
                this.stats.power = this.stats.power * wScale;

                this.vx = 0;
                this.vy = 0;
                this.isGrounded = false;

                this.state = 'idle'; // idle, walk, hit, ko, block, dodge, attack states...
                this.stateTimer = 0;
                this.animTime = 0;
                this.keyReleased = true;

                this.currentMove = null;
                this.hasHit = false;
                this.lastBlockTime = 0;

                this.joints = {
                    head: {x: 0, y: -70}, neck: {x: 0, y: -50}, pelvis: {x: 0, y: 10},
                    fHand: {x: 20, y: -40}, bHand: {x: -10, y: -30},
                    fFoot: {x: 20, y: 90}, bFoot: {x: -20, y: 90},
                    fKnee: {x: 25, y: 50}, bKnee: {x: -15, y: 50}
                };
            }

            changeState(newState, duration = 0, moveData = null) {
                this.state = newState;
                this.stateTimer = duration;
                this.animTime = 0;
                this.currentMove = moveData;
                this.hasHit = false;
            }

            update(dt) {
                // Physics
                this.vy += 0.8; // Gravity
                this.y += this.vy;
                this.x += this.vx;

                // Floor collision
                const floorY = canvas.height - 20;
                if (this.y + this.height > floorY) {
                    this.y = floorY - this.height;
                    this.vy = 0;
                    this.isGrounded = true;
                } else {
                    this.isGrounded = false;
                }

                // Arena bounds
                if (this.x < 0) this.x = 0;
                if (this.x + this.width > canvas.width) this.x = canvas.width - this.width;

                // Friction
                if (this.state !== 'walk' && this.isGrounded) {
                    this.vx *= 0.8;
                }

                // Timers & Stamina
                this.animTime += dt;
                if (this.stateTimer > 0) {
                    this.stateTimer -= dt;
                    if (this.stateTimer <= 0 && this.state !== 'ko') {
                        this.changeState('idle');
                    }
                }

                if (this.state === 'idle' || this.state === 'walk') {
                    if (this.stats.stamina < this.stats.maxStamina) {
                        this.stats.stamina += (this.stats.staminaRegen * dt) / 1000;
                        if (this.stats.stamina > this.stats.maxStamina) this.stats.stamina = this.stats.maxStamina;
                    }
                }
            }

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

                // --- MUSCLE MUTATION MATH (Capped for aesthetic limits) ---
                let chestW = Math.min(45, 20 + (this.stats.maxHp / 15)) * w;
                let bicepW = Math.min(22, 8 + (this.stats.power / 4)) * w;
                let trapsW = Math.min(25, 10 + (this.stats.defense / 2.5)) * w;
                let hasAbs = this.stats.maxStamina >= 120;

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
                    attackIntensity = Math.sin(p * Math.PI);

                    if (this.state === 'jab') {
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
                    } else if (this.state === 'block') {
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
                    // Botched surgery visual: If limb length is wildly upgraded, make it look disjointed/crooked
                    let botchedLevel = app.limbLengthMod ? Math.floor(app.limbLengthMod / 20) : 0;

                    // Add some terrifying jiggle to the joint if severely botched
                    let jiggleX = 0; let jiggleY = 0;
                    if (botchedLevel > 0 && this.state !== 'ko') {
                        jiggleX = (Math.random() - 0.5) * botchedLevel * 2;
                        jiggleY = (Math.random() - 0.5) * botchedLevel * 2;
                    }

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

                    let midX = startJoint.x + Math.cos(midAngle) * l + jiggleX;
                    let midY = startJoint.y + Math.sin(midAngle) * l + jiggleY;

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

                        // Metal Pins
                        if (botchedLevel > 1) {
                            ctx.fillStyle = 'silver';
                            ctx.fillRect(midX - 3, midY - 15, 6, 30);
                            ctx.strokeRect(midX - 3, midY - 15, 6, 30);
                        }
                    }
                }
                };

                const armLength = (75 * h) + (app.limbLengthMod || 0);
                const legLength = (80 * h) + (app.limbLengthMod || 0);

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
ctx.restore();
            }
        }

        // --- COMBAT LOGIC ---
        const moves = {
            jab:            { type: 'high', dmg: 5,  cost: 10, dur: 250, reach: 65,  active: [100, 200] },
            cross:          { type: 'high', dmg: 12, cost: 18, dur: 400, reach: 75,  active: [200, 300] },
            body_jab:       { type: 'low',  dmg: 7,  cost: 12, dur: 300, reach: 60,  active: [150, 250] },
            body_cross:     { type: 'low',  dmg: 15, cost: 20, dur: 450, reach: 70,  active: [250, 350] },
            low_kick:       { type: 'low',  dmg: 10, cost: 15, dur: 350, reach: 60,  active: [150, 250] },
            high_kick:      { type: 'high', dmg: 20, cost: 30, dur: 600, reach: 70,  active: [350, 450] },
            superman_punch: { type: 'high', dmg: 25, cost: 35, dur: 700, reach: 90,  active: [400, 550], isFlying: true },
            flying_knee:    { type: 'high', dmg: 22, cost: 30, dur: 650, reach: 75,  active: [350, 500], isFlying: true },
            flying_kick:    { type: 'high', dmg: 30, cost: 45, dur: 800, reach: 100, active: [500, 650], isFlying: true }
        };

        function initiateAttack(fighter, moveName) {
            const move = moves[moveName];
            if (fighter.stats.stamina >= move.cost && fighter.state !== 'hit' && fighter.state !== 'ko') {
                fighter.stats.stamina -= move.cost;
                fighter.changeState(moveName, move.dur, move);
                fighter.keyReleased = false; // Prevent holding button

                // Add forward momentum for flying moves
                if (move.isFlying) {
                    fighter.vx = fighter.facing * (moveName === 'superman_punch' ? 8 : 6);
                }
            }
        }

        let particles = [];
        function createParticles(x, y) {
            for(let i=0; i<5; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 10,
                    vy: (Math.random() - 0.5) * 10 - 5,
                    life: 1.0
                });
            }
        }

        function drawParticles(ctx) {
            ctx.fillStyle = 'rgba(255, 0, 0, 0.7)';
            for(let i=particles.length-1; i>=0; i--) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy;
                p.life -= 0.05;
                if(p.life <= 0) { particles.splice(i, 1); continue; }
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.life * 4, 0, Math.PI*2);
                ctx.fill();
            }
        }

        function checkCollisions() {
            [pFighter, oFighter].forEach(attacker => {
                if (attacker.currentMove && !attacker.hasHit) {
                    const move = attacker.currentMove;
                    const t = attacker.stateTimer;
                    const elapsed = move.dur - t;

                    // Check if attack is in active frames
                    if (elapsed >= move.active[0] && elapsed <= move.active[1]) {
                        const defender = (attacker === pFighter) ? oFighter : pFighter;

                        // Calculate reach hitbox
                        const appH = attacker.stats.appearance ? (attacker.stats.appearance.h || 1) : 1;
                        let reachStartX = attacker.x + (attacker.width/2);
                        // Taller fighters have longer reach
                        let scaledReach = (move.reach * appH) + (attacker.stats.appearance ? (attacker.stats.appearance.limbLengthMod || 0) : 0);
                        let reachEndX = reachStartX + (scaledReach * attacker.facing);
                        if (attacker.facing === -1) {
                            let temp = reachStartX; reachStartX = reachEndX; reachEndX = temp;
                        }

                        const defStartX = defender.x;
                        const defEndX = defender.x + defender.width;

                        // Collision detected!
                        if (reachStartX < defEndX && reachEndX > defStartX) {

                            // DODGE I-FRAMES LOGIC
                            // If defender is dodging, and in the first 300ms, they are invincible!
                            let isDodged = false;
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

                            if (isDodged) {
                                // Whiff completely
                            } else {
                                // Calculate Damage
                                let dmg = move.dmg + (attacker.stats.power * 0.5);

                                // Blocking logic
                                if (defender.state === 'block' || defender.state === 'low_block') {
                                    dmg -= defender.stats.defense;

                                    // High block vs High attack = good. Low block vs Low attack = good.
                                    if ((defender.state === 'block' && move.type === 'high') ||
                                        (defender.state === 'low_block' && move.type === 'low')) {
                                        dmg *= 0.2; // Perfect block (80% mitigation)
                                    } else {
                                        dmg *= 0.6; // Wrong block (40% mitigation)
                                    }
                                } else {
                                    dmg -= defender.stats.defense * 0.5;
                                }
                                if (dmg < 1) dmg = 1;

                                defender.stats.hp -= dmg;
                                defender.changeState('hit', 300);
                                createParticles(reachEndX, defender.y + (defender.height / 2));

                                // UI SHAKE
                                canvas.classList.remove('shake-anim');
                                void canvas.offsetWidth; // trigger reflow
                                canvas.classList.add('shake-anim');

                                // COMBO SYSTEM
                                if (attacker === pFighter) {
                                    pComboCount++; oComboCount = 0; lastHitTime = Date.now();
                                } else {
                                    oComboCount++; pComboCount = 0; lastHitTime = Date.now();
                                }
                            }
                        }
                    }
                }
            });
        }

        // --- GAME LOOP & AI ---
        function gameLoop(timestamp) {
            if (!state.inFight) return;

            const dt = timestamp - lastTime;
            lastTime = timestamp;

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Combo Timeout
            if (Date.now() - lastHitTime > 1500) { pComboCount = 0; oComboCount = 0; }

            // PLAYER INPUT HANDLING (Only if not hit/ko)
            if (pFighter.state !== 'hit' && pFighter.state !== 'ko') {
                let moving = false;

                // Movement
                if (keys.a && ['idle','walk','block'].includes(pFighter.state)) {
                    pFighter.vx = -pFighter.speed; pFighter.facing = -1; moving = true;
                }
                if (keys.d && ['idle','walk','block'].includes(pFighter.state)) {
                    pFighter.vx = pFighter.speed; pFighter.facing = 1; moving = true;
                }

                // Jump
                if (keys.w && pFighter.isGrounded && ['idle','walk'].includes(pFighter.state)) {
                    pFighter.vy = -12;
                }

                // Dodge / Duck
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

                // Attacks (With Shift modifiers)
                if (pFighter.isGrounded && ['idle','walk'].includes(pFighter.state) && pFighter.keyReleased) {
                    if (keys.u) initiateAttack(pFighter, keys.shift ? 'body_jab' : 'jab');
                    if (keys.i) initiateAttack(pFighter, keys.shift ? 'body_cross' : 'cross');
                    if (keys.j) initiateAttack(pFighter, 'low_kick');
                    if (keys.k) initiateAttack(pFighter, 'high_kick');
                } else if (!pFighter.isGrounded && pFighter.keyReleased) {
                    // Flying moves
                    if (keys.i) initiateAttack(pFighter, 'superman_punch');
                    if (keys.u || keys.j) initiateAttack(pFighter, 'flying_knee');
                    if (keys.k) initiateAttack(pFighter, 'flying_kick');
                }

                if (moving && pFighter.state === 'idle') pFighter.changeState('walk', 9999);
                if (!moving && pFighter.state === 'walk') pFighter.changeState('idle');
            }

            // AI LOGIC
            if (oFighter.state !== 'hit' && oFighter.state !== 'ko') {
                const dist = Math.abs(pFighter.x - oFighter.x);
                oFighter.facing = (pFighter.x < oFighter.x) ? -1 : 1;

                if (oFighter.state === 'block' && Date.now() - oFighter.lastBlockTime > 800) {
                    oFighter.changeState('idle'); // Stop blocking eventually
                }

                if (dist > 120 && ['idle','walk'].includes(oFighter.state)) {
                    // Move closer
                    oFighter.vx = (pFighter.x > oFighter.x) ? oFighter.speed : -oFighter.speed;
                    if (oFighter.state === 'idle') oFighter.changeState('walk', 9999);
                } else {
                    // In range
                    if (oFighter.state === 'walk') oFighter.changeState('idle');

                    if (oFighter.state === 'idle') {
                        const rand = Math.random();

                        // Reactive dodge
                        if (pFighter.state !== 'idle' && pFighter.state !== 'walk' && rand < 0.05 && oFighter.stats.stamina >= 15) {
                            oFighter.stats.stamina -= 15;
                            oFighter.changeState('dodge', 400);
                            oFighter.vx = oFighter.facing * -2;
                        }
                        // Random Attacks
                        else if (rand < 0.02) initiateAttack(oFighter, 'jab');
                        else if (rand < 0.04) initiateAttack(oFighter, 'cross');
                        else if (rand < 0.05) initiateAttack(oFighter, 'body_jab');
                        else if (rand < 0.06) initiateAttack(oFighter, 'body_cross');
                        else if (rand < 0.07) initiateAttack(oFighter, 'low_kick');
                        else if (rand < 0.08) initiateAttack(oFighter, 'high_kick');
                        // Block
                        else if (rand < 0.09 && pFighter.state !== 'idle') {
                            oFighter.changeState('block', 9999);
                            oFighter.lastBlockTime = Date.now();
                        }
                    }
                }
            }

            // Update & Draw
            pFighter.update(dt);
            oFighter.update(dt);

            checkCollisions();

            pFighter.draw(ctx);
            oFighter.draw(ctx);
            drawParticles(ctx);

            updateHUD();
            checkKO();

            if (state.inFight) {
                gameLoopId = requestAnimationFrame(gameLoop);
            }
        }

        // --- UI UPDATES ---
        function updateHUD() {
            // Bars
            document.getElementById('p-hp-bar').style.width = Math.max(0, (pFighter.stats.hp / pFighter.stats.maxHp) * 100) + '%';
            document.getElementById('p-hp-text').textContent = `${Math.ceil(Math.max(0, pFighter.stats.hp))}/${pFighter.stats.maxHp}`;
            document.getElementById('p-stamina-bar').style.width = Math.max(0, (pFighter.stats.stamina / pFighter.stats.maxStamina) * 100) + '%';

            document.getElementById('o-hp-bar').style.width = Math.max(0, (oFighter.stats.hp / oFighter.stats.maxHp) * 100) + '%';
            document.getElementById('o-hp-text').textContent = `${Math.ceil(Math.max(0, oFighter.stats.hp))}/${oFighter.stats.maxHp}`;
            document.getElementById('o-stamina-bar').style.width = Math.max(0, (oFighter.stats.stamina / oFighter.stats.maxStamina) * 100) + '%';

            // Status Texts (Block / Dodge)
            const updateStatus = (fighter, elId) => {
                const el = document.getElementById(elId);
                if (fighter.state === 'block') {
                    el.textContent = 'BLOCKING'; el.style.opacity = 1; el.style.color = '#60a5fa';
                } else if (fighter.state === 'dodge') {
                    el.textContent = 'DODGED!'; el.style.opacity = 1; el.style.color = '#4ade80';
                } else {
                    el.style.opacity = 0;
                }
            };
            updateStatus(pFighter, 'p-status');
            updateStatus(oFighter, 'o-status');

            // Combos
            const pComboEl = document.getElementById('p-combo');
            if (pComboCount >= 2) { pComboEl.textContent = `${pComboCount} HIT COMBO!`; pComboEl.style.opacity = 1; }
            else { pComboEl.style.opacity = 0; }

            const oComboEl = document.getElementById('o-combo');
            if (oComboCount >= 2) { oComboEl.textContent = `${oComboCount} HIT COMBO!`; oComboEl.style.opacity = 1; }
            else { oComboEl.style.opacity = 0; }
        }

        function checkKO() {
            if (pFighter.stats.hp <= 0 && pFighter.state !== 'ko') {
                pFighter.changeState('ko', 99999);
                endMatch(false);
            }
            if (oFighter.stats.hp <= 0 && oFighter.state !== 'ko') {
                oFighter.changeState('ko', 99999);
                endMatch(true);
            }
        }

        function endMatch(playerWon) {
            document.getElementById('ko-overlay').classList.remove('opacity-0');

            setTimeout(() => {
                state.inFight = false;
                cancelAnimationFrame(gameLoopId);

                document.getElementById('combat-screen').classList.add('hidden');
                document.getElementById('ko-overlay').classList.add('opacity-0');

                if (playerWon) {
                    const opp = opponents[playerStats.rank];
                    playerStats.money += opp.reward;
                    playerStats.rank++;
                    document.getElementById('result-title').textContent = "YOU WON!";
                    document.getElementById('result-title').className = "text-5xl font-black mb-4 text-green-500";
                    document.getElementById('result-money').textContent = opp.reward;

                    if (playerStats.rank >= opponents.length) {
                        document.getElementById('goat-screen').classList.remove('hidden');
                    } else {
                        document.getElementById('result-screen').classList.remove('hidden');
                    }
                } else {
                    const opp = opponents[playerStats.rank];
                    const loserBonus = Math.floor(opp.reward * 0.25); // Give 25% of reward for losing
                    playerStats.money += loserBonus;

                    document.getElementById('result-title').textContent = "KNOCKED OUT";
                    document.getElementById('result-title').className = "text-5xl font-black mb-4 text-red-500";
                    document.getElementById('result-money').textContent = loserBonus;
                    document.getElementById('result-screen').classList.remove('hidden');
                }
            }, 2500); // Wait 2.5 seconds to watch KO animation before showing results
        }

        // --- MENU LOGIC ---
        function updateGymUI() {
            document.getElementById('player-money').textContent = playerStats.money;

            if (playerStats.rank < opponents.length) {
                const opp = opponents[playerStats.rank];
                document.getElementById('opp-name').textContent = opp.name;
                document.getElementById('opp-desc').textContent = opp.desc;

                document.getElementById('opp-hp').textContent = opp.stats.maxHp;
                document.getElementById('opp-pow').textContent = opp.stats.power;
                document.getElementById('opp-def').textContent = opp.stats.defense;
                document.getElementById('opp-stam').textContent = opp.stats.maxStamina;

                document.getElementById('my-hp').textContent = playerStats.maxHp;
                document.getElementById('my-pow').textContent = playerStats.power;
                document.getElementById('my-def').textContent = playerStats.defense;
                document.getElementById('my-stam').textContent = playerStats.maxStamina;
            }

            const container = document.getElementById('upgrades-container');
            container.innerHTML = '';

            for (const [key, data] of Object.entries(upgradeCosts)) {
                const level = upgradeLevels[key];
                const cost = Math.floor(data.base * Math.pow(data.mult, level));
                const canAfford = playerStats.money >= cost;

                const btn = document.createElement('button');
                btn.className = `w-full p-3 rounded flex justify-between items-center transition ${canAfford ? 'bg-blue-600 hover:bg-blue-500 text-white' : 'bg-gray-700 text-gray-500 cursor-not-allowed'}`;
                btn.innerHTML = `
                    <div class="text-left">
                        <div class="font-bold">${data.name} <span class="text-xs bg-gray-900 px-1 rounded ml-1">Lvl ${level}</span></div>
                        <div class="text-xs opacity-75">+${data.val} per upgrade</div>
                    </div>
                    <div class="font-bold">$${cost}</div>
                `;

                if (canAfford) {
                    btn.onclick = () => {
                        playerStats.money -= cost;
                        upgradeLevels[key]++;

                        if (key === 'botchedSurgery') {
                            // Increases limb length drastically, reduces stamina
                            playerStats.appearance.limbLengthMod = (playerStats.appearance.limbLengthMod || 0) + 20;
                            playerStats.maxStamina = Math.max(10, playerStats.maxStamina - 20); // Penalty
                            if (playerStats.stamina > playerStats.maxStamina) playerStats.stamina = playerStats.maxStamina;
                        } else {
                            playerStats[key] += data.val;
                        }
                        // --- CHARACTER PREVIEW LOGIC ---
        const previewCanvas = document.getElementById('preview-canvas');
        const previewCtx = previewCanvas.getContext('2d');
        let previewFighter = null;

        function updatePreview() {
            // Create a dummy fighter for the preview
            if (!previewFighter) {
                previewFighter = new Fighter(150, 0, 1, playerStats, true);
                previewFighter.state = 'idle';
            }

            // Sync stats
            previewFighter.stats.appearance = JSON.parse(JSON.stringify(playerStats.appearance));
            previewFighter.width = 60 * (playerStats.appearance.h || 1);
            previewFighter.height = 180 * (playerStats.appearance.h || 1);
            previewFighter.limbMod = playerStats.appearance.limbLengthMod || 0;

            // Clear and draw
            previewCtx.clearRect(0, 0, previewCanvas.width, previewCanvas.height);

            // Center the fighter in the preview canvas
            previewCtx.save();
            // Scale down slightly to fit the small canvas
            previewCtx.scale(0.8, 0.8);
            // Center X, align Y to bottom
            let targetX = (previewCanvas.width / 0.8) / 2 - (previewFighter.width / 2);
            let targetY = (previewCanvas.height / 0.8) - previewFighter.height + 40;

            previewFighter.x = targetX;
            previewFighter.y = targetY;

            // Animate
            previewFighter.animTime = performance.now();

            previewFighter.draw(previewCtx);
            previewCtx.restore();

            if (!state.inFight) {
                requestAnimationFrame(updatePreview);
            }
        }

        // Start preview loop
        requestAnimationFrame(updatePreview);

        updateGymUI();
                    };
                }
                container.appendChild(btn);
            }
        }

        document.getElementById('btn-fight').addEventListener('click', () => {
            document.getElementById('hub-screen').classList.add('hidden');
            document.getElementById('combat-screen').classList.remove('hidden');
            document.getElementById('combat-screen').classList.add('flex');

            const oppData = opponents[playerStats.rank];
            document.getElementById('hud-opp-name').textContent = oppData.name.toUpperCase();

            pFighter = new Fighter(100, 0, 1, playerStats, true);
            oFighter = new Fighter(700, 0, -1, oppData.stats, false);

            pComboCount = 0; oComboCount = 0;

            state.inFight = true;
            cancelAnimationFrame(updatePreview);
            lastTime = performance.now();
            requestAnimationFrame(gameLoop);
        });

        document.getElementById('btn-continue').addEventListener('click', () => {
            document.getElementById('result-screen').classList.add('hidden');
            document.getElementById('hub-screen').classList.remove('hidden');
            requestAnimationFrame(updatePreview);
            updateGymUI();
        });

        document.getElementById('btn-restart').addEventListener('click', () => {
            location.reload();
        });


        // --- CUSTOMIZATION LISTENERS ---
        ['height', 'weight', 'skin', 'shorts', 'hairstyle', 'haircolor', 'facialhair', 'tattoos', 'glovetype'].forEach(key => {
            document.getElementById(`custom-${key}`).addEventListener('input', (e) => {
                let val = e.target.value;
                if (key === 'height' || key === 'weight') {
                    val = parseFloat(val);
                    document.getElementById(`val-${key}`).textContent = val.toFixed(2) + 'x';
                    playerStats.appearance[key === 'height' ? 'h' : 'w'] = val;
                } else {
                    playerStats.appearance[key] = val;
                }
            });
        });


        // Lock physical traits if a fight has occurred
        function checkTraitLocks() {
            if (playerStats.rank > 0) {
                document.getElementById('custom-height').disabled = true;
                document.getElementById('custom-height').classList.add('opacity-50', 'cursor-not-allowed');
                document.getElementById('custom-weight').disabled = true;
                document.getElementById('custom-weight').classList.add('opacity-50', 'cursor-not-allowed');
                // Optional: add a tiny lock icon or note
                if (!document.getElementById('lock-note')) {
                    const note = document.createElement('div');
                    note.id = 'lock-note';
                    note.className = 'text-xs text-red-400 mt-2 text-center';
                    note.innerText = 'Genetics locked after pro debut.';
                    document.getElementById('custom-weight').parentElement.appendChild(note);
                }
            }
        }

// Initialize Gym on load
        updateGymUI();
        checkTraitLocks();
