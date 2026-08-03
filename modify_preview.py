import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# 1. Add Canvas into the Locker Room for Character Preview
locker_room_html = """
                    <h2 class="text-2xl font-bold mb-4">Locker Room</h2>

                    <!-- Preview Canvas -->
                    <div class="w-full h-48 bg-gray-900 border border-gray-700 rounded-lg mb-4 overflow-hidden relative">
                        <canvas id="preview-canvas" width="300" height="200" class="w-full h-full block"></canvas>
                    </div>

                    <div class="space-y-4">
"""

content = content.replace('<h2 class="text-2xl font-bold mb-4">Locker Room</h2>\n                    <div class="space-y-4">', locker_room_html)

# 2. Add Javascript to render the preview
js_injection = """
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
"""

# Inject before custom listeners
listeners_start = content.find("// --- CUSTOMIZATION LISTENERS ---")
if listeners_start != -1:
    content = content[:listeners_start] + js_injection + content[listeners_start:]


# 3. Ensure preview starts/stops correctly when fighting
btn_fight = content.find("state.inFight = true;")
if btn_fight != -1:
    content = content.replace("state.inFight = true;", "state.inFight = true;\n            cancelAnimationFrame(updatePreview);")

btn_continue = content.find("document.getElementById('hub-screen').classList.remove('hidden');")
if btn_continue != -1:
    content = content.replace("document.getElementById('hub-screen').classList.remove('hidden');", "document.getElementById('hub-screen').classList.remove('hidden');\n            requestAnimationFrame(updatePreview);")

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
