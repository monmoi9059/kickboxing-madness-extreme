import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# 1. Fighter class relies on global `canvas` variable for floor collision and shadow positioning
# We need to pass the target canvas context or height, or check if ctx belongs to previewCanvas
# Let's dynamically get canvas height from the ctx object's canvas
# `ctx.canvas.height`

# Replace `canvas.height` inside `draw()` with `ctx.canvas.height`
content = content.replace("canvas.height - 15", "ctx.canvas.height - 15")

# For update(), floor collision uses `canvas.height`.
# In preview mode, `canvas` (the main game canvas) still exists, but its height is 437.
# The preview fighter Y is set to `targetY = (previewCanvas.height / 0.8) - previewFighter.height + 40;`
# But if we call `update()`, gravity pushes it down to the main `canvas.height` floor!
# Wait, preview doesn't call `update()`! It only calls `draw()`.
# Let's check `draw()` for hardcoded `canvas.height`
# `ctx.ellipse(this.x + this.width/2, canvas.height - 15, 35 * w, 8, 0, 0, Math.PI*2);` -> fixed

# Wait, `this.y` is set, but `canvas` might be undefined if `draw()` is called before `canvas` is initialized?
# `const canvas = document.getElementById('game-canvas');` is at the very end of the file maybe?
canvas_def = content.find("const canvas = document.getElementById('game-canvas');")
if canvas_def == -1:
    # Not found? Let's check where canvas is defined
    pass

# The issue might also be that `this.y` is used in `draw()`:
# `ctx.translate(this.x + this.width/2, (this.y + this.height) - (90 * h));`

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
