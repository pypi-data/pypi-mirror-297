import os
import datetime
import argparse
import json
from jinja2 import Template

# Get the current date and time
def date(reporting=None)->str:
    """
    Returns the current date and time as a string in the format "YYYY-MM-DD-HH-MM"

    :return: A string representing the current date and time
    """
    if reporting is not None:
        return datetime.datetime.now().strftime("%Y-%m-%d")
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

def save_config(data:json)->bool:
    """
    Saves the configuration to a file named "glog.json".

    :param data: The configuration data to be saved
    :return: True if the save is successful, False otherwise
    """
    try:
        with open("glog.json", "w") as f:
            json.dump(data, f, indent=3)
        return True
    
    except Exception as e:
        print(f"Error saving glog.json: {e}")
        return False
    
    
# Constants and templates
# initialize local data for GLogger if not present

output_folder = "ch-logs"  # Set the output folder
chtypes = ["ADDED", "CHANGED", "DELETED", "REMOVED", "FIXED", "SECURITY"]

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

try:
    # Load the JSON data
    with open("glog.json", "r") as f:
        data = json.load(f)    
except:
    # or Initialize the JSON data
    data = {"build_number": 0, "version_number": [0, 0, 0]}  

# get app_title from config, initialize if not present
if "app_title" not in data:
    app_title = input("What is the name for this application?\n> ")
    data["app_title"] = app_title
    
else:
    app_title = data["app_title"]

# get developer from config, initialize if not present
if "developer" not in data:
    developer = input("Who is the developer?\n> ")
    data["developer"] = developer
else:
    developer = data["developer"]

# get developer's link from config, initialize if not present
if "dev_link" not in data:
    dev_link = input("What is the developer's link?\n> ")
    data["dev_link"] = dev_link
else:
    dev_link = data["dev_link"]
    
# refresh or backup the glog.json configuration
save_config(data)

chlog_title = f"# Changelog for {app_title}\n\n"
chlog_footer = f"# **GLogger created & maintained by:** [{developer}]({dev_link})"
anchor = "\n\n<!--  NEW CHANGES   /-->\n\n"

changelog_file = "changelog.md" # Set the changelog file
if not os.path.exists(changelog_file):
    with open(changelog_file, "w") as f:
        f.write(chlog_title)
        f.write(anchor)
        f.write(chlog_footer)


def create_artifact():
    os.system("cls")

    # get the changelog type
    for i, a in enumerate(chtypes):
        print(f"{i+1}. {a}")
        
    selection = int(input(f"Enter the log type: \n> ").strip())
    if selection > len(chtypes) or selection < 1:
        print("Invalid selection, exiting without changes.")
        exit(1)
    artifact_type = chtypes[selection - 1]

    # Get the commit message from the user
    artifact_message = input(f"Enter the commit message (include --r or --f to initiate semantic versioning): \n{artifact_type}> ".strip())
    if artifact_message == "":
        print("Empty commit message, exiting without changes.")
        exit(1)

    # Check for minimum length
    if len(artifact_message) < 10:
        raise ValueError("Entry must be at least 10 characters long")

    # Create the changelog file name
    artifact_file = f"{output_folder}/{date()}-{artifact_type}.md"

    # Create the changelog file
    try:
        with open(artifact_file, "w") as f:
            f.write(date() + "\n")
            f.write(artifact_type + "\n")
            f.write(artifact_message + "\n")
            f.write(data["developer"] + "\n")

        print(f"Changelog Artifact created: {artifact_file}")
        
    except Exception as e:
        print(f"Error creating Artifact: [{artifact_file}]\n{e}")


def semantic_versioning(build, version, content):
    build += 1

    if "--r" in content.lower():
        version[0] += 1
        version[1] = 0
        version[2] = 0
    
    elif "--f" in content.lower():
        version[1] += 1
        version[2] = 0
    
    else:
        # new fix version
        version[2] += 1
    
    return build, version
    

def collect_changelogs(data):

    # Get the current build and version numbers
    build_number:int = data["build_number"] # int
    version_number:list = data["version_number"] # [0, 0, 0]

    # Get the list of changelog files
    changelog_files = [f for f in os.listdir(output_folder) if f.endswith(".md")]

    if len(changelog_files) == 0:
        print("No changelog files found. Exiting without changes.")
        exit(0)

    # Sort the changelog files by date
    # changelog_files.sort(key=lambda f: datetime.datetime.strptime(f.split("-")[1].split(".")[0], "%Y-%m-%d-%H-%M"))
    changelog_files.sort()

    # # Create the new changelog content
    # with open(changelog_file, "r") as f:
    #     old_changelog_content = "\n" + f.read()

    context = {}
    changes = {x.upper(): [] for x in chtypes}
    contributors = set()
    
    # Iterate over the sorted changelog files
    for file in changelog_files:
        # Read the file content
        with open(os.path.join(output_folder, file), "r") as f:
            content = f.read()
        
        _, a_type, a_msg, a_dev = content.splitlines()

        build_number, version_number = semantic_versioning(build_number, version_number, content)
        replaced_content = content.replace("--f", "new feature version").replace("--r", "new release version")
        
        changes[a_type.upper()].append(replaced_content.strip().capitalize())
        contributors.add(a_dev.strip()) # add this dev to the set of contributors

    # updatate the changelog json
    data["build_number"] = build_number
    data["version_number"] = version_number

    save_config(data)

    try:
        # gather the header and metadata for the changelog
        context = {
            "build_number": build_number,
            "version_number": ".".join(str(x) for x in version_number),
            "date": date("ymd"),
            "title": f"Changelog for Application: {data['app_title']}",
            "contributors": ",".join(sorted(contributors)),
        }

        # build the header and metadata portion of the changelog
        with open("template.md", "r") as f:
            output = Template(f.read()).render(**context)
        print(f"Changelog Header: Successfully created.")
        
        # assemble the sections data & template of the changelog
        changes = {x:y for x, y in changes.items() if y}
        sect_temp = Template(open("template_sections.md", "r").read())

        # append the populated sections to the changelog
        for sect, chgs in changes.items():
            this_sect = sect_temp.render(artifact_type=sect, artifact_list=chgs)
            output += this_sect
        print(f"Changelog Sections: Successfully created.")
        print(f"Changelog Text: Successfully created.")
        
    except Exception as e:
        print(f"Error building changelog text: {e}")


    try:
        # append the previous changelog content
        with open(changelog_file, "r") as f:
            output += f.read()

        # Write the new changelog content back to file
        with open(changelog_file, "w") as f:
            f.write(output)

        print(f"Changelog updated: {changelog_file}")

        # remove old changelogs
        for file in changelog_files:
            os.remove(os.path.join(output_folder, file))

    except Exception as e:
        print(f"Error updating changelog: {e}")


def main():
    parser = argparse.ArgumentParser(description="Changelog generator")
    parser.add_argument("-c", "--collect", action="store_true", help="Collect existing changelogs and update the main changelog file")
    args = parser.parse_args()

    if args.collect:
        collect_changelogs(data)
    else:
        create_artifact()

if __name__ == "__main__":
    main()