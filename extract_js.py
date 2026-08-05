import sys

with open("hairstyles_upgrade.html", "r") as f:
    content = f.read()

script = content.split("<script>")[1].split("</script>")[0]

with open("temp.js", "w") as f:
    f.write(script)
