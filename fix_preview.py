import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Wait to call requestAnimationFrame until Fighter is defined.
# Moving the CHARACTER PREVIEW LOGIC below Fighter and COMBAT LOGIC

# 1. Cut the preview logic
preview_start = content.find("// --- CHARACTER PREVIEW LOGIC ---")
preview_end = content.find("requestAnimationFrame(updatePreview);", content.find("requestAnimationFrame(updatePreview);", preview_start) + 1) + len("requestAnimationFrame(updatePreview);\n")

preview_code = content[preview_start:preview_end]
content = content[:preview_start] + content[preview_end:]

# 2. Paste it before window.onload or end of script
end_script = content.find("updateGymUI();")
content = content[:end_script] + preview_code + "\n        " + content[end_script:]

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
