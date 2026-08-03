import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Let's move the Character Preview logic right after the DOM elements are cached for the engine (around line 980)

# 1. Cut the preview logic from bottom
preview_start = content.find("// --- CHARACTER PREVIEW LOGIC ---")
preview_end = content.find("requestAnimationFrame(updatePreview);", content.find("requestAnimationFrame(updatePreview);", preview_start) + 1) + len("requestAnimationFrame(updatePreview);\n")
preview_code = content[preview_start:preview_end]
content = content[:preview_start] + content[preview_end:]

# 2. Paste after state declaration
state_decl = content.find("const state = { inFight: false };")
content = content[:state_decl + len("const state = { inFight: false };")] + "\n\n        " + preview_code + "\n\n" + content[state_decl + len("const state = { inFight: false };"):]

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
