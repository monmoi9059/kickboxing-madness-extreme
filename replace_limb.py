import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

start_sig = "const drawDetailedLimb = (startJoint, endJoint, bendDir, limbLength, width, outlineCol, fillCol, hasTattoo = false) => {"
end_sig = "const armLength ="

start_idx = content.find(start_sig)
end_idx = content.find(end_sig)

if start_idx == -1 or end_idx == -1:
    print("Could not find drawDetailedLimb")
    exit(1)

new_limb_func = """const drawDetailedLimb = (startJoint, endJoint, bendDir, limbLength, upperWidth, lowerWidth, jointWidth, shoulderWidth, outlineCol, fillCol, hasTattoo = false) => {
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

                    // Helper to draw a muscular segment using bezier curves
                    const drawMuscleSegment = (p1, p2, width1, width2, isUpper, isFill, bulgeFactor=1.2) => {
                        ctx.beginPath();
                        ctx.lineWidth = isFill ? 0 : 2; // We will fill a shape rather than stroke it thick
                        ctx.strokeStyle = outlineCol;
                        ctx.fillStyle = fillCol;

                        // Calculate perpendicular vector for width
                        let pdx = p2.x - p1.x;
                        let pdy = p2.y - p1.y;
                        let pdist = Math.sqrt(pdx*pdx + pdy*pdy);
                        if (pdist === 0) return;
                        let nx = -pdy / pdist;
                        let ny = pdx / pdist;

                        // Points
                        let p1L = {x: p1.x + nx * width1/2, y: p1.y + ny * width1/2};
                        let p1R = {x: p1.x - nx * width1/2, y: p1.y - ny * width1/2};
                        let p2L = {x: p2.x + nx * width2/2, y: p2.y + ny * width2/2};
                        let p2R = {x: p2.x - nx * width2/2, y: p2.y - ny * width2/2};

                        // Midpoint for curve control
                        let m = {x: (p1.x + p2.x)/2, y: (p1.y + p2.y)/2};

                        // Control points for muscle bulge
                        let bulgeL = {x: m.x + nx * ((width1+width2)/2 * bulgeFactor), y: m.y + ny * ((width1+width2)/2 * bulgeFactor)};
                        let bulgeR = {x: m.x - nx * ((width1+width2)/2 * bulgeFactor), y: m.y - ny * ((width1+width2)/2 * bulgeFactor)};

                        // If it's the upper segment, taper into the shoulder/hip
                        if (isUpper && shoulderWidth > 0) {
                           p1L = {x: p1.x + nx * shoulderWidth/2, y: p1.y + ny * shoulderWidth/2};
                           p1R = {x: p1.x - nx * shoulderWidth/2, y: p1.y - ny * shoulderWidth/2};
                        }

                        ctx.moveTo(p1L.x, p1L.y);
                        // Left side curve (bicep/quad bulge)
                        ctx.quadraticCurveTo(bulgeL.x, bulgeL.y, p2L.x, p2L.y);

                        // End cap (joint)
                        ctx.lineTo(p2R.x, p2R.y);

                        // Right side curve (tricep/hamstring bulge)
                        ctx.quadraticCurveTo(bulgeR.x, bulgeR.y, p1R.x, p1R.y);

                        ctx.closePath();
                        if (isFill) {
                            ctx.fill();
                        } else {
                            ctx.stroke();
                        }
                    };

                    // Draw Outline first
                    drawMuscleSegment(startJoint, {x:midX, y:midY}, upperWidth, jointWidth, true, false, 1.25);
                    drawMuscleSegment({x:midX, y:midY}, endJoint, lowerWidth, jointWidth*0.8, false, false, 1.15);

                    // Draw Fill
                    drawMuscleSegment(startJoint, {x:midX, y:midY}, upperWidth, jointWidth, true, true, 1.25);
                    drawMuscleSegment({x:midX, y:midY}, endJoint, lowerWidth, jointWidth*0.8, false, true, 1.15);

                    // Smooth the joint connection
                    ctx.fillStyle = fillCol;
                    ctx.strokeStyle = outlineCol;
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.arc(midX, midY, jointWidth/2, 0, Math.PI*2);
                    ctx.fill();
                    // Optional: only stroke the joint on the outside depending on bend, but drawing full circle works well enough in 2D

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

                    // Botched Stitches!
                    if (botchedLevel > 0) {
                        ctx.strokeStyle = 'red';
                        ctx.lineWidth = 1.5;
                        ctx.beginPath();
                        ctx.moveTo(midX - jointWidth/2, midY - 5);
                        ctx.lineTo(midX + jointWidth/2, midY + 5);
                        ctx.moveTo(midX - jointWidth/2, midY + 5);
                        ctx.lineTo(midX + jointWidth/2, midY - 5);
                        ctx.stroke();

                        if (botchedLevel > 1) {
                            ctx.fillStyle = 'silver';
                            ctx.fillRect(midX - 3, midY - 15, 6, 30);
                            ctx.strokeRect(midX - 3, midY - 15, 6, 30);
                        }
                    }
                };

                """

new_content = content[:start_idx] + new_limb_func + content[end_idx:]

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(new_content)

print("Replaced drawDetailedLimb!")
