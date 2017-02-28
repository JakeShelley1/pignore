from urllib2 import urlopen, URLError, HTTPError
import zipfile, StringIO
import os, sys, shutil, re

# Enhancement: Allow multiple args for merging gitignores
# Enhancement: Save my own gitignore

# Globals
data_path = os.path.join(os.environ["HOME"], ".pignore-data/") # Where data files will be stored

# Helper method:
# Return True if params exist in set s and remove params from s
# Return False if not
def check_for_params(params, s):
    if (len(set(params) & set(s)) != 0):
        return True
    return False 

# Show help docs
def print_help(showFlair=False):
    print("")
    print(" <`--'\> ____  __  ___  __ _   __  ____  ____") 
    print(" /. .  \(  _ \(  )/ __)(  ( \ /  \(  _ \(  __)")
    print("(`')  ,| ) __/ )(( (_ \/    /(  O ))   / ) _)")
    print(" `-._,_/(__)  (__)\___/\_)__) \__/(__\_)(____)")
    
    print("\nUsage: pignore <command> [OPTIONS]\n")
    print("where <command> is:")
    print("   g | generate   generate a gitignore file")
    print("   u | update     update gitignore stored files")
    print("   s | save       save current directory gitignore file")
    print("\nUse 'pignore <command> -h' to get more detail")
    print("\nMost popular supported gitignores:")
    print("   python, swift, java, laravel, dart, javascript,")
    print("   temp, temp, temp, temp, ...\n")
    print("Use 'pignore list' to see full list\n")

# Print detailed help for chosen command
def print_detail_help(cmd):
    print("")
    if (cmd == "update"):
        print("pignore update (no args)")
    elif (cmd == "generate"):
        print("Usage:")
        print("pignore generate [<gitignore_name>]")
    elif (cmd == "save"):
        print("Usage:")
        print("pignore save <new_gitignore_name> (can only contain characters A-z, 1-9)")
    print("")

# Print version number
def print_version():
    print("1.0")

# Print error, exit on completion
def throw_error(error):
    print("\nError: %s" % error)
    print("Use 'pignore --help' to learn more\n")
    exit(1)

# Parse options
def parse_options(args):
    options = []

    # Search for options in arg list
    for arg in args:
        # Check if arg is an option
        if (arg[0] == "-"):
            options.append(arg)

    return options

# Save current gitignore file into pignore-data
def save(name):
    # Check for .pignore-data file, create one if it doesn't exist
    if (os.path.exists(data_path) == False):
        os.makedirs(data_path)

    # Check if gitignore exists
    if (os.path.exists(".gitignore") == False):
        throw_error("Could not find gitignore current directory")

    # Check for valid name (must be 1-9, a-z, A-Z)
    if (re.match("^[a-zA-Z0-9_]*$", name)):
        print("Saving gitignore file..."),
        with open(os.path.join(data_path, name + ".user.gitignore"), "wb") as safe_file:
            gitignore = open(".gitignore")
            safe_file.write(gitignore.read())
            gitignore.close

        print("Done")
        print("Saved file can be generated with 'pignore generate %s'" % name)
    else:
        throw_error("Invalid name. Name can only contain characters A-z, 1-9")

# Generate gitignore
def generate(params):
    # Check for .pignore-data file
    if (os.path.exists(data_path) == False):
        throw_error("Could not find any data files! Use 'pignore update' to get latest gitignores\n")

    if (len(params) == 0):
        throw_error("No gitignore names given! Use 'pignore generate [<gitignore_name>]'")

    # Ensure that args are valid files
    for p in set(params):
        p += ".gitignore"
        if (os.path.exists(os.path.join(data_path, p)) == False):
            throw_error("Could not find file '%s.gitignore'.\nUse 'pignore list' to see available gitignores\nUse 'pignore update' to get latest gitignore" % p[:-10])

    write_option = None
    
    # Check for existing gitignore and set write option
    if (os.path.isfile(".gitignore")):
        while (write_option == None):
            overwrite = raw_input("Found existing gitignore file. Overwrite (y/n)? ")
            if (overwrite == "y"):
                write_option = "wb"
                print("Overwriting existing gitignore..."),
            elif (overwrite == "n"):
                write_option = "a"
                print("Appending to existing gitignore..."),
            else:
                print("Your response %s was not one of the expected responses: y, n" % overwrite)
    else:
        write_option = "wb"
        print("Writing gitignore..."),

    for p in set(params):
        p += ".gitignore"
        with open(".gitignore", write_option) as gitignore:
            f = open(os.path.join(data_path, p))
            gitignore.write(f.read())
        write_option = "a" # Set write to append after first param
    print("Done")



# Setup .pignore-data folder
def setup_folder():
    print("Preparing files..."), 
    for root, dirs, files in os.walk(data_path):
        path = root.split(os.sep)
        for f in files:
            if (f.endswith(".gitignore")):
                src = os.path.join("/".join(path), f) # Path to source file
                dst = os.path.join(data_path, f) # Path to file destination
                # *******Might need to look at this later for saving files*******
                if (src == dst):
                    continue
                shutil.move(src, data_path + f) # Move file to pignore-data folder

    print("Done")

    print("Cleaning up..."),
    # Delete extra folder
    for root, dirs, files in os.walk(data_path):
        for d in dirs:
            shutil.rmtree(os.path.join(data_path, d)) # Delete file containing gitignores
    print("Done")
    print("Files can be found in " + data_path)

# Load data from github to .pignore-data file
def update_data():
    # Check for .pignore-data file, create one if it doesn't exist
    if (os.path.exists(data_path) == False):
        os.makedirs(data_path)

    url = "http://github.com/github/gitignore/zipball/master/"

    try:
        zip_name = "master.zip"
        f = urlopen(url)
        print "Downloading gitignore files from " + url

        # Open our local file for writing
        with open(os.path.join(data_path, zip_name), "wb") as local_file:
            local_file.write(f.read())

        # Unzip
        with zipfile.ZipFile(os.path.join(data_path, zip_name), "r") as z:
            z.extractall(data_path)

        # Remove zip file
        os.remove(os.path.join(data_path, zip_name))

    #handle errors
    except:
        throw_error("Connection error! Could not update gitignore data")

    setup_folder()

    print("Use 'pignore generate' to generate a gitignore")

def main():
    # Remove default arg
    args = sys.argv[1:]

    # No arguments
    if (len(args) == 0):
        print_help()
        return

    # Options can be any index
    # Commands must be first index

    # Override for version flag
    if (check_for_params(["--version", "-v"], args)):
        print_version()
        return

    # Check for update
    if (args[0] == "update" or args[0] == "u"):
        if ("-h" in set(args)):
            print_detail_help("update")
            return
        update_data()
        return

    # Check for generate
    if (args[0] == "generate" or args[0] == "g"):
        if ("-h" in set(args)):
            print_detail_help("generate")
            return
        generate(args[1:]) # send all args after command
        return

    if (args[0] == "save" or args[0] == "s"):
        if ("-h" in set(args)):
            print_detail_help("save")
            return
        if (len(args) > 1):
            save(args[1]) # send all args after command
        else:
            throw_error("No name was provided! Use 'pignore save <name>'")
        return

    # Check for help flag
    if (check_for_params(["--help", "-h"], args)):
        print_help()
        return

    # Incorrect usage
    print_help()

if __name__ == '__main__':
    main()
