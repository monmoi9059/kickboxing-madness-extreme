import re

with open('hairstyles_upgrade.html', 'r') as f:
    content = f.read()

# Fix checkGameEnd (inline code)
content = content.replace(
'''                    if (playerStats.rank >= opponents.length) {
                        document.getElementById('goat-screen').classList.remove('hidden');
                    } else {
                        document.getElementById('result-screen').classList.remove('hidden');
                    }''',
'''                    document.getElementById('result-screen').classList.remove('hidden');'''
)

with open('hairstyles_upgrade.html', 'w') as f:
    f.write(content)
