import os
import urllib.request
import re

print("Starting Miryoku to Selenium migration for Dactyl Manuform...")

# 1. Download Dactyl Manuform shield files from the ZMK outboard repo
shield_dir = "config/boards/shields/dactyl_manuform_4x5"
os.makedirs(shield_dir, exist_ok=True)

base_url = "https://raw.githubusercontent.com/nathanielks/zmk/add-shield-dactyl-manuform-4x5/app/boards/shields/dactyl_manuform_4x5"
shield_files = [
    "Kconfig.shield",
    "Kconfig.defconfig",
    "dactyl_manuform_4x5.conf",
    "dactyl_manuform_4x5.overlay",
    "dactyl_manuform_4x5_left.overlay",
    "dactyl_manuform_4x5_right.overlay"
]

for f in shield_files:
    url = f"{base_url}/{f}"
    path = os.path.join(shield_dir, f)
    if not os.path.exists(path):
        print(f"Downloading {f}...")
        try:
            urllib.request.urlretrieve(url, path)
        except Exception as e:
            print(f"Failed to download {f}: {e}")

# 2. Update build.yaml to include the Dactyl builds
build_yaml_path = "build.yaml"
with open(build_yaml_path, "r") as f:
    build_yaml = f.read()

dactyl_build = """
# Gallium Dactyl Manuform 4x5 + nice!nano v2
- board: nice_nano@2//zmk
  shield: dactyl_manuform_4x5_left
  artifact-name: gallium_dactyl_left
  snippet: studio-rpc-usb-uart
  cmake-args: -DCONFIG_ZMK_STUDIO=y -DCONFIG_ZMK_POINTING=y -DCONFIG_ZMK_MOUSE=y
- board: nice_nano@2//zmk
  shield: dactyl_manuform_4x5_right
  artifact-name: gallium_dactyl_right
  snippet: studio-rpc-usb-uart
  cmake-args: -DCONFIG_ZMK_STUDIO=y -DCONFIG_ZMK_POINTING=y -DCONFIG_ZMK_MOUSE=y
"""

if "dactyl_manuform_4x5_left" not in build_yaml:
    if "###\n# Resets" in build_yaml:
        build_yaml = build_yaml.replace("###\n# Resets", dactyl_build + "\n###\n# Resets")
    else:
        build_yaml += dactyl_build
    with open(build_yaml_path, "w") as f:
        f.write(build_yaml)
    print("Updated build.yaml")

# 3. Create config/dactyl_manuform_4x5.keymap
# This maps the 42-key Selenium logical layout to the 46-key Dactyl physical matrix.
# The 2 "extra" keys (inner thumbs) are mapped to Bootloader and None.
keymap_path = "config/dactyl_manuform_4x5.keymap"
keymap_content = """// Gallium on Dactyl Manuform 4x5 (46-key shield)
#define SELENIUM_KEYMAP_BINDINGS(LOUT1,  LROW1,  RROW1,  ROUT1, \\
                                 LOUT2,  LROW2,  RROW2,  ROUT2, \\
                                 LOUT3,  LROW3,  RROW3,  ROUT3, \\
                                 LT1, LT2, LT3,  RT3, RT2, RT1) \\
    LROW1               RROW1 \\
    LROW2               RROW2 \\
    LROW3               RROW3 \\
    &none &none         &none &none \\
    LT1 LT2             RT2 RT1 \\
    LT3 &bootloader     &none RT3 \\
    &none &none         &none &none

#include <aekeynox/selenium.keymap>
"""
with open(keymap_path, "w") as f:
    f.write(keymap_content)
print(f"Created {keymap_path}")

# 4. Create config/dactyl_manuform_4x5.conf
conf_path = "config/dactyl_manuform_4x5.conf"
conf_content = """# Gallium custom Kconfigs
CONFIG_ZMK_KSCAN_DEBOUNCE_PRESS_MS=1
CONFIG_ZMK_KSCAN_DEBOUNCE_RELEASE_MS=5
CONFIG_ZMK_DISPLAY=y
CONFIG_ZMK_DISPLAY_STATUS_SCREEN_BUILT_IN=y
CONFIG_ZMK_EXT_POWER=y
CONFIG_ZMK_SLEEP=y
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000
"""
with open(conf_path, "w") as f:
    f.write(conf_content)
print(f"Created {conf_path}")

# 5. Update settings.h to enable Vim Navigation
settings_path = "include/aekeynox/settings.h"
with open(settings_path, "r") as f:
    settings = f.read()

if "#define VIM_NAVIGATION" not in settings:
    settings = settings.replace("// #define VIM_NAVIGATION", "#define VIM_NAVIGATION")
    if "#define VIM_NAVIGATION" not in settings:
        settings += "\n#define VIM_NAVIGATION\n"
    with open(settings_path, "w") as f:
        f.write(settings)
    print("Updated settings.h")

# 6. Update selenium.keymap (Inject Gallium Base Layer)
selenium_keymap_path = "include/aekeynox/selenium.keymap"
with open(selenium_keymap_path, "r") as f:
    selenium_keymap = f.read()

gallium_base = """base_layer: base_layer {
    display-name = "Base";
    bindings = <SELENIUM_KEYMAP_BINDINGS(
        &kp TAB    ,  &kp B  &kp L  &kp D  &kp C  &kp V   ,   &kp J  &kp Y  &kp O      &kp U     &kp COMMA ,  &kp BACKSPACE ,
        &kp ESCAPE ,  HRM_N  HRM_R  HRM_T  HRM_S  &kp G   ,   &kp P  HRM_H  HRM_A      HRM_E     HRM_I     ,  &kp ENTER     ,
        &kp LSHIFT ,  &kp X  &kp Q  &kp M  &kp W  &kp Z   ,   &kp K  &kp F  &kp SQT    &kp SEMI  &kp DOT   ,  &kp RSHIFT    ,
        LTHUMB_TUCK , LTHUMB_HOME , LTHUMB_REACH   ,   RTHUMB_REACH , RTHUMB_HOME , RTHUMB_TUCK
    )>;
};"""

start_str = "base_layer: base_layer {"
end_str = "};"
start_idx = selenium_keymap.find(start_str)
if start_idx != -1:
    end_idx = selenium_keymap.find(end_str, start_idx)
    if end_idx != -1:
        selenium_keymap = selenium_keymap[:start_idx] + gallium_base + selenium_keymap[end_idx + len(end_str):]
        with open(selenium_keymap_path, "w") as f:
            f.write(selenium_keymap)
        print("Updated selenium.keymap with Gallium base layer")

# 7. Update hold_taps.dtsi (Inject Gallium Timeless HRMs)
hold_taps_path = "include/aekeynox/hold_taps.dtsi"
with open(hold_taps_path, "r") as f:
    hold_taps = f.read()

hrm_aliases = """
/* Gallium GASC Home Row Mods */
#define HRM_N &hml LGUI
#define HRM_R &hml LALT
#define HRM_T &hml LSHFT
#define HRM_S &hml LCTRL

#define HRM_H &hmr RCTRL
#define HRM_A &hmr RSHFT
#define HRM_E &hmr RALT
#define HRM_I &hmr RGUI
"""

if "HRM_N" not in hold_taps:
    hrm_aliases_insert_point = "/**\n* Thumb Keys\n*/"
    if hrm_aliases_insert_point in hold_taps:
        hold_taps = hold_taps.replace(hrm_aliases_insert_point, hrm_aliases + "\n" + hrm_aliases_insert_point)
        with open(hold_taps_path, "w") as f:
            f.write(hold_taps)
        print("Added HRM aliases to hold_taps.dtsi")

hrm_behaviors = """
    /* Gallium Timeless HRMs - Left Hand */
    OMIT_IF_NO_REF hml: timeless_hrm_left {
        compatible = "zmk,behavior-hold-tap";
        #binding-cells = <2>;
        flavor = "balanced";
        tapping-term-ms = <280>;
        quick-tap-ms = <175>;
        require-prior-idle-ms = <150>;
        bindings = <&kp>, <&kp>;
        hold-trigger-on-release;
        /* Dactyl 46-key matrix: Right hand alphas + Right thumbs */
        hold-trigger-key-positions = <23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45>;
    };

    /* Gallium Timeless HRMs - Right Hand */
    OMIT_IF_NO_REF hmr: timeless_hrm_right {
        compatible = "zmk,behavior-hold-tap";
        #binding-cells = <2>;
        flavor = "balanced";
        tapping-term-ms = <280>;
        quick-tap-ms = <175>;
        require-prior-idle-ms = <150>;
        bindings = <&kp>, <&kp>;
        hold-trigger-on-release;
        /* Dactyl 46-key matrix: Left hand alphas + Left thumbs */
        hold-trigger-key-positions = <0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22>;
    };
"""

if "timeless_hrm_left" not in hold_taps:
    last_brace = hold_taps.rfind("};")
    if last_brace != -1:
        hold_taps = hold_taps[:last_brace] + hrm_behaviors + hold_taps[last_brace:]
        with open(hold_taps_path, "w") as f:
            f.write(hold_taps)
        print("Added hml and hmr behaviors to hold_taps.dtsi")

print("\nMigration script completed successfully!")
print("Please review the changes, commit, and push to your fork.")
