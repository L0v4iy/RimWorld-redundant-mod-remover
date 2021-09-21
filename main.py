import os
import shutil
import xml.etree.ElementTree as ET

import config


def get_enabled_mods(config_path):
    if not os.path.isfile(config_path):
        print("No config file in '" + config_path + "'")
        raise
    mod_config_reader = ET.parse(config_path).getroot()
    string_tree = ET.tostring(mod_config_reader).decode()

    xml_p = ["activeMods"]

    for child_name in xml_p:
        string_tree = get_child(string_tree, child_name)
    mod_list = ET.fromstring(string_tree).findall("li")
    active_mods = []
    for li in mod_list:
        active_mods.append(li.text)

    return active_mods


def get_child(parent_as_string, search):
    tree = ET.fromstring(parent_as_string)
    for child in tree.iter():
        if child.tag == search:
            return ET.tostring(child).decode()
    print("No such child in context")
    raise


def get_available_mod_paths(mod_path):
    return os.listdir(mod_path)


def get_mod_name(mod_path):
    naming_file_path = config.mod_path + "\\" + modPath + "\\About\\About.xml"
    if not os.path.isfile(naming_file_path):
        print("No metadata file in '" + naming_file_path + "'")
        return
    about_reader = ET.parse(naming_file_path)
    package_name = about_reader.find("packageId")
    if package_name is not None:
        return package_name.text.lower()

    print("Mod '" + naming_file_path + "' is undefined")


enabled = get_enabled_mods(config.mod_config_path)
mods = get_available_mod_paths(config.mod_path)


def show_enabled():
    print("\nEnabled:")
    for en in enabled:
        print(" " + en)


# cleanup
show_enabled()
all_mods = []
undefined = []
redundant = []
print("\nAttempt to remove:")
for modPath in mods:
    mod_name = get_mod_name(modPath)
    all_mods.append(mod_name)
    if mod_name is None:
        undefined.append(modPath)
    elif mod_name not in enabled:
        redundant.append(modPath)
        print(" " + mod_name)

# unfound
print("\nUnfound mods:")
unfound = []
for e in enabled:
    if e not in all_mods:
        print(" " + e)
        unfound.append(e)

print("\nRemove redundant mods?")
sec = input("y/n\n")
if sec == "y":
    for redundant_path in redundant:
        shutil.rmtree(config.mod_path + "\\" + redundant_path)

    undefinedPath = config.undefined_path
    for u in undefined:
        if not os.path.isdir(undefinedPath):
            os.makedirs(undefinedPath)
        shutil.move(config.mod_path + "\\" + u, undefinedPath)
    print("Undefined mods moved to " + undefinedPath)
    print("done")
