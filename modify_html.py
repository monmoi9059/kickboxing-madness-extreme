import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

customization_html = """
                        <div class="flex justify-between items-center bg-gray-900 p-3 rounded-lg border border-gray-700">
                            <label class="text-sm text-gray-300 font-bold">Facial Hair</label>
                            <select id="custom-facialhair" class="bg-gray-800 text-white text-sm rounded border border-gray-600 p-1 cursor-pointer">
                                <option value="none">None</option>
                                <option value="beard">Beard</option>
                                <option value="mustache">Mustache</option>
                                <option value="goatee">Goatee</option>
                            </select>
                        </div>
                        <div class="flex justify-between items-center bg-gray-900 p-3 rounded-lg border border-gray-700">
                            <label class="text-sm text-gray-300 font-bold">Tattoos</label>
                            <select id="custom-tattoos" class="bg-gray-800 text-white text-sm rounded border border-gray-600 p-1 cursor-pointer">
                                <option value="none">None</option>
                                <option value="tribal_band">Tribal Band</option>
                                <option value="chest_piece">Chest Piece</option>
                            </select>
                        </div>
                        <div class="flex justify-between items-center bg-gray-900 p-3 rounded-lg border border-gray-700">
                            <label class="text-sm text-gray-300 font-bold">Gloves</label>
                            <select id="custom-glovetype" class="bg-gray-800 text-white text-sm rounded border border-gray-600 p-1 cursor-pointer">
                                <option value="boxing">Boxing</option>
                                <option value="mma">MMA</option>
                            </select>
                        </div>
"""

# Insert into HTML
insert_marker = '</select>\n                        </div>\n                        <div class="flex justify-between items-center bg-gray-900 p-3 rounded-lg border border-gray-700">\n                            <label class="text-sm text-gray-300 font-bold">Hair Color</label>'
new_content = content.replace(insert_marker, '</select>\n                        </div>' + customization_html + '\n                        <div class="flex justify-between items-center bg-gray-900 p-3 rounded-lg border border-gray-700">\n                            <label class="text-sm text-gray-300 font-bold">Hair Color</label>')

# Update Javascript listeners array
js_marker = "['height', 'weight', 'skin', 'shorts', 'hairstyle', 'haircolor']"
new_content = new_content.replace(js_marker, "['height', 'weight', 'skin', 'shorts', 'hairstyle', 'haircolor', 'facialhair', 'tattoos', 'glovetype']")

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(new_content)
