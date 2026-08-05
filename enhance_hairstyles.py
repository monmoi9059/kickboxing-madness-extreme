import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Add new hairstyles to HTML dropdown
html_target = """<option value="spiky">Spiky</option>"""
html_new = html_target + """
                                <option value="dreadlocks">Dreadlocks</option>
                                <option value="mullet">Mullet</option>
                                <option value="pompadour">Pompadour</option>
                                <option value="long">Long Hair</option>"""

content = content.replace(html_target, html_new)

# Update array of hairstyles in random generation
js_target = "const hStyles = ['short', 'bald', 'mohawk', 'afro', 'spiky'];"
js_new = "const hStyles = ['short', 'bald', 'mohawk', 'afro', 'spiky', 'dreadlocks', 'mullet', 'pompadour', 'long'];"
content = content.replace(js_target, js_new)


# Now update the Hair Rendering in draw()
# We need to add hair physics by utilizing `this.vx`, `this.vy`, and `breathe`
# Replace the old `// Hair Rendering` block
render_target_start = "// Hair Rendering"
render_target_end = "// Facial Hair"

start_idx = content.find(render_target_start)
end_idx = content.find(render_target_end)

if start_idx == -1 or end_idx == -1:
    print("Could not find hair rendering block")
    exit(1)

new_hair_code = """// Hair Rendering with Simple Physics
                const hStyle = app.hairstyle || 'bald';
                if (hStyle !== 'bald') {
                    ctx.fillStyle = app.haircolor || '#000000';
                    ctx.strokeStyle = app.haircolor || '#000000';

                    // Simple physics variables derived from movement and state
                    let sway = (this.vx || 0) * -2; // Moves opposite to velocity
                    if (this.state === 'dodge') sway = f * -15; // Big sway on dodge
                    if (this.state === 'hit') sway = f * 10;
                    if (this.state === 'ko') sway = f * 25; // Fall back

                    // Add bounce from breathing/idle
                    let hairBounce = bounce * 0.5;

                    if (hStyle === 'short') {
                        ctx.beginPath();
                        let startA = f === 1 ? Math.PI*0.8 : Math.PI*0.2;
                        let endA = f === 1 ? Math.PI*2.1 : Math.PI*1.9;
                        ctx.arc(t.head.x - (f * hrX*0.1), t.head.y - hrY*0.2, hrX*1.05, startA, endA);
                        ctx.fill();
                    } else if (hStyle === 'mohawk') {
                        ctx.beginPath();
                        ctx.moveTo(t.head.x + (f*hrX*0.5), t.head.y - hrY*0.8);
                        // The tip of the mohawk sways
                        let tipX = t.head.x + sway*0.5;
                        ctx.quadraticCurveTo(t.head.x + sway*0.2, t.head.y - hrY*2.5, t.head.x - (f*hrX*0.8), t.head.y - hrY*0.2);
                        ctx.quadraticCurveTo(t.head.x - (f*hrX*0.4), t.head.y - hrY*1.5, t.head.x + (f*hrX*0.5), t.head.y - hrY*0.8);
                        ctx.fill();
                    } else if (hStyle === 'afro') {
                        ctx.beginPath();
                        // Afro lags behind movement slightly (squash and stretch)
                        let stretch = Math.abs(sway) * 0.5;
                        ctx.ellipse(t.head.x - (f*hrX*0.2) + sway*0.2, t.head.y - hrY*0.6 + hairBounce,
                                    hrX*1.4 + stretch, hrY*1.4 - stretch*0.5,
                                    0, 0, Math.PI*2);
                        // Bumpy texture
                        for(let i=0; i<8; i++) {
                            let angle = (i/8) * Math.PI*2;
                            ctx.arc(t.head.x - (f*hrX*0.2) + sway*0.2 + Math.cos(angle)*hrX*1.2,
                                    t.head.y - hrY*0.6 + hairBounce + Math.sin(angle)*hrY*1.2,
                                    hrX*0.4, 0, Math.PI*2);
                        }
                        ctx.fill();
                    } else if (hStyle === 'spiky') {
                        ctx.beginPath();
                        for(let s = -0.5; s <= 1; s += 0.4) {
                            let spikeX = t.head.x - (f * s * hrX);
                            let spikeTipX = spikeX - (f * hrX * 0.6) + sway;
                            ctx.moveTo(spikeX + hrX*0.2, t.head.y - hrY*0.6);
                            ctx.quadraticCurveTo(spikeTipX + (f*hrX*0.2), t.head.y - hrY*1.4, spikeTipX, t.head.y - hrY*1.9 + hairBounce);
                            ctx.quadraticCurveTo(spikeX, t.head.y - hrY*1.0, spikeX - hrX*0.2, t.head.y - hrY*0.6);
                        }
                        ctx.fill();
                    } else if (hStyle === 'dreadlocks') {
                        ctx.lineWidth = hrX * 0.3;
                        ctx.lineCap = 'round';
                        for(let i = -1; i <= 1.5; i += 0.5) {
                            ctx.beginPath();
                            let rootX = t.head.x - (f * i * hrX * 0.8);
                            let rootY = t.head.y - hrY * 0.8;
                            ctx.moveTo(rootX, rootY);
                            // Dreads hang down and sway heavily
                            let endX = rootX + sway * (1.5 + Math.random());
                            let endY = rootY + hrY * 2.5 + hairBounce * 2;
                            let cp1X = rootX + sway*0.5;
                            let cp1Y = rootY + hrY;
                            ctx.quadraticCurveTo(cp1X, cp1Y, endX, endY);
                            ctx.stroke();
                        }
                    } else if (hStyle === 'mullet') {
                        // Business in front
                        ctx.beginPath();
                        ctx.arc(t.head.x - (f * hrX*0.1), t.head.y - hrY*0.4, hrX*1.05, Math.PI*0.8, Math.PI*2.2);
                        ctx.fill();
                        // Party in back (swaying)
                        ctx.beginPath();
                        let backRootX = t.head.x - (f * hrX * 1.0);
                        let backRootY = t.head.y - hrY * 0.2;
                        ctx.moveTo(backRootX, backRootY);
                        ctx.quadraticCurveTo(backRootX + sway*1.5, backRootY + hrY*1.5, backRootX - (f*hrX*0.5) + sway, backRootY + hrY*2.5);
                        ctx.lineTo(t.head.x - (f * hrX * 0.5), t.head.y + hrY * 0.5);
                        ctx.fill();
                    } else if (hStyle === 'pompadour') {
                        ctx.beginPath();
                        // Big slicked back curve
                        ctx.moveTo(t.head.x + (f*hrX*0.8), t.head.y - hrY*0.5);
                        // Front swoop that bounces
                        ctx.bezierCurveTo(t.head.x + (f*hrX*1.5) + sway*0.2, t.head.y - hrY*2.5 + hairBounce,
                                          t.head.x - (f*hrX*0.5) + sway*0.5, t.head.y - hrY*2.5,
                                          t.head.x - (f*hrX*1.2), t.head.y - hrY*0.2);
                        // Back into the neck
                        ctx.quadraticCurveTo(t.head.x - (f*hrX*0.8), t.head.y - hrY, t.head.x + (f*hrX*0.8), t.head.y - hrY*0.5);
                        ctx.fill();
                    } else if (hStyle === 'long') {
                        ctx.beginPath();
                        // Hair line
                        ctx.moveTo(t.head.x + (f*hrX*0.5), t.head.y - hrY*0.8);
                        // Flowing back and down
                        ctx.quadraticCurveTo(t.head.x - (f*hrX) + sway*0.5, t.head.y - hrY,
                                             t.head.x - (f*hrX*1.5) + sway*1.5, t.head.y + hrY*1.5 + hairBounce);
                        // Bottom edge of hair
                        ctx.quadraticCurveTo(t.head.x - (f*hrX) + sway, t.head.y + hrY*2,
                                             t.head.x - (f*hrX*0.5), t.head.y + hrY);
                        ctx.fill();
                    }
                }

                """

new_content = content[:start_idx] + new_hair_code + content[end_idx:]

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(new_content)

print("Added hairstyles with physics!")
