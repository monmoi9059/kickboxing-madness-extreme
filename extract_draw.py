import sys

with open('EFLTG.html', 'r') as f:
    content = f.read()

start = content.find("            draw(ctx) {")
if start == -1:
    print("Could not find draw(ctx) {")
    sys.exit(1)

# Find the end of the draw method (matching braces)
brace_count = 0
end = -1
in_draw = False

for i in range(start, len(content)):
    if content[i] == '{':
        brace_count += 1
        in_draw = True
    elif content[i] == '}':
        brace_count -= 1

    if in_draw and brace_count == 0:
        end = i + 1
        break

if end != -1:
    with open('draw_method.js', 'w') as f:
        f.write(content[start:end])
    print("Extracted draw method to draw_method.js")
else:
    print("Could not find end of draw method")
