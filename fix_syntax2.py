import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Replace double closure
old_str = """            });
        });
        });"""
new_str = """            });
        });"""

content = content.replace(old_str, new_str)

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
