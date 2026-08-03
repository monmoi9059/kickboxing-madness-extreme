import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Let's inspect the `updatePreview` function carefully.
preview_start = content.find("function updatePreview()")
preview_end = content.find("}", content.find("requestAnimationFrame(updatePreview);", preview_start)) + 1
print(content[preview_start:preview_end])
