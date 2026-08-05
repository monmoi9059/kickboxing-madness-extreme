import sys

with open("test.js", "r") as f:
    js = f.read()

with open("hairstyles_upgrade.html", "r") as f:
    html = f.read()

# Instead of patching individual lines and fighting with duplicate sections,
# Let's just completely replace the `<script>` contents of hairstyles_upgrade.html
# with the contents of test.js. They are supposed to be identical.

prefix = html.split("<script>")[0] + "<script>\n"
suffix = "\n</script>" + html.split("</script>")[1]

with open("hairstyles_upgrade.html", "w") as f:
    f.write(prefix + js + suffix)

print("Copied test.js into hairstyles_upgrade.html")
