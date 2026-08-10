import sys

with open('build.yaml', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Look back up to 5 lines to see if we are currently inside the Dactyl block
    context = "".join(lines[max(0, i-5):i])

    # 1. Remove the studio snippet for Dactyl
    if 'snippet: studio-rpc-usb-uart' in line and 'dactyl_manuform' in context:
        continue  # Skip adding this line to the new file

    # 2. Remove the CONFIG_ZMK_STUDIO=y flag for Dactyl
    if 'cmake-args:' in line and 'CONFIG_ZMK_STUDIO=y' in line and 'dactyl_manuform' in context:
        line = line.replace('-DCONFIG_ZMK_STUDIO=y ', '').replace('-DCONFIG_ZMK_STUDIO=y', '')

    new_lines.append(line)

with open('build.yaml', 'w') as f:
    f.writelines(new_lines)

print("✅ Disabled ZMK Studio for Dactyl Manuform builds.")
