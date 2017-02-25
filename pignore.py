from urllib2 import urlopen, URLError, HTTPError
import zipfile, StringIO
import os, sys, shutil

# Enhancement: Allow multiple args for merging gitignores
# Enhancement: Save my own gitignore

# Globals
data_path = os.path.join(os.environ["HOME"], ".pignore-data/") # Where data files will be stored

# Helper method for if given parameters given are in given set
def check_for_params(params, s):
    if (len(set(params) & s) != 0):
        return True
    return False 

# Show help docs
def print_help(showFlair=False):
    # Only show flair if user asked for help
    if (showFlair):
        print(" <`--'\> ____  __  ___  __ _   __  ____  ____") 
        print(" /. .  \(  _ \(  )/ __)(  ( \ /  \(  _ \(  __)")
        print("(`')  ,| ) __/ )(( (_ \/    /(  O ))   / ) _)")
        print(" `-._,_/(__)  (__)\___/\_)__) \__/(__\_)(____)")
    
    print("\nUsage: pignore <command> [OPTIONS]\n")
    print("Supported gitignores:")
    print("   python, swift, java, laravel, dart, javascript,")
    print("   temp, temp, temp, temp")
    exit(1)

# Print version number
def print_version():
    print("1.0")
    exit(1)

# Print error
def throw_error(error):
    print("\nError: %s" % error)
    print("Use --help to learn more\n")

# Parse options
def parse_options(args):
    options = set()

    # Search for options in arg list
    for arg in args:
        # Check if arg is an option
        if (arg[0] == "-"):
            options.add(arg)

    return options

# Get gitignore
def generate(language):
    # Check for .pignore-data file
    if (os.path.exists(data_path) == False):
        throw_error("Couldn't find data file! Please use 'pignore update' to get latest gitignores.\n")
        exit(1)

    # write_option = None
    
    # # Check for existing gitignore and set write option
    # if (os.path.isfile(".gitignore")):
    #     while (write_option == None):
    #         overwrite = raw_input("Found existing gitignore file. Overwrite (y/n)? ")
    #         if (overwrite == "y"):
    #             write_option = "wb"
    #         elif (overwrite == "n"):
    #             write_option = "a"
    #         else:
    #             print("Your response %s was not one of the expected responses: y, n" % overwrite)
    # else:
    #     write_option = "wb"

# Setup .pignore-data folder with gitignore
def setup_folder():
    remove_list = []

    print("Preparing files..."), 
    for root, dirs, files in os.walk(data_path):
        path = root.split(os.sep)
        # Write 
        for f in files:
            if (f.endswith("gitignore")):
                with open(os.path.join(data_path, f), "wb") as container_file:
                    container_file.write(f)
            else:
                remove_list.append(f)
    print("Done")

    print("Cleaning up..."),
    # Delete extra folder
    for root, dirs, files in os.walk(data_path):
        for d in dirs:
            shutil.rmtree(os.path.join(data_path, d)) # Delete file containing gitignores
    print("Done")
    print("Files can be found in " + data_path)


def update_data():
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
    except HTTPError, e:
        print ("HTTP Error:", e.code, url)
    except URLError, e:
        print ("URL Error:", e.reason, url)

    setup_folder()

    print("Done! Use 'pignore g [OPTIONS]' to generate a gitignore")
    exit(1)


def main():
    # Remove default arg
    args = set(sys.argv[1:])

    # No arguments
    if (len(args) == 0):
        print_help(True)

    options = parse_options(args)
    args = args - options # Remove options from args

    # Override for version flag
    if (check_for_params(["--version", "-v"], options)):
        print_version()

    # Override for help flag
    if (check_for_params(["-h", "--help"], options)):
        print_help(True)

    if (check_for_params(["update", "u"], args)):
        update_data()

    if (check_for_params(["g", "generate"], args)):
        generate()

if __name__ == '__main__':
    main()
