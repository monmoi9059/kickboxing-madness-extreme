import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# 1. Update initial span text
content = content.replace('<span id="val-height" class="font-bold text-white">1.00x</span>', '<span id="val-height" class="font-bold text-white">6\'0"</span>')
content = content.replace('<span id="val-weight" class="font-bold text-white">1.00x</span>', '<span id="val-weight" class="font-bold text-white">180 lbs</span>')

# 2. Add formatting functions and update listeners
js_start = content.find("['height', 'weight', 'skin', 'shorts', 'hairstyle', 'haircolor', 'facialhair', 'tattoos', 'glovetype'].forEach(key => {")
js_end = content.find("});", content.find("playerStats.appearance[key] = val;", js_start)) + 3

if js_start != -1:
    new_js = """function formatHeight(multiplier) {
            let inches = Math.round(72 * multiplier); // Base 6'0"
            let feet = Math.floor(inches / 12);
            let remInches = inches % 12;
            return `${feet}'${remInches}"`;
        }

        function formatWeight(multiplier) {
            let lbs = Math.round(180 * multiplier); // Base 180 lbs
            return `${lbs} lbs`;
        }

        ['height', 'weight', 'skin', 'shorts', 'hairstyle', 'haircolor', 'facialhair', 'tattoos', 'glovetype'].forEach(key => {
            document.getElementById(`custom-${key}`).addEventListener('input', (e) => {
                let val = e.target.value;
                if (key === 'height') {
                    val = parseFloat(val);
                    document.getElementById(`val-${key}`).textContent = formatHeight(val);
                    playerStats.appearance.h = val;
                } else if (key === 'weight') {
                    val = parseFloat(val);
                    document.getElementById(`val-${key}`).textContent = formatWeight(val);
                    playerStats.appearance.w = val;
                } else {
                    playerStats.appearance[key] = val;
                }
            });
        });"""
    content = content[:js_start] + new_js + content[js_end:]

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
