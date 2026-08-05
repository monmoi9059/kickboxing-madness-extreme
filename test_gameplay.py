import json
with open("test.js", "r") as f:
    print("Found 'losses' in test.js:", 'losses: 0' in f.read())
