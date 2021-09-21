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
    res = about_reader.find("packageId").text
    return res


enabled = get_enabled_mods(config.mod_config_path)

mods = get_available_mod_paths(config.mod_path)
# cleanup
redundant = []
print("\nattempt to remove:")
for modPath in mods:
    mod_name = get_mod_name(modPath)

    if mod_name not in enabled:
        redundant.append(modPath)
        print(" " + mod_name)
print("\nremove redundant mods?")
sec = input("y/n\n")
if sec is "y":
    for redundant_path in redundant:
        shutil.rmtree(config.mod_path + "\\" + redundant_path)
print("done")
