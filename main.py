# Godot GDextension C++ Auto Installer for any project 
# Available for : Linux, Windows



# BUILDING STEPS
    # STEP 0 : Verify game project folder
    # STEP 1 : Verify user godot version with godot executable file
    # STEP 2 : Verify Python, Git, Scons, C++ Compiler, install if there are no ones
    # STEP 3 : Verify the installations
    # STEP 4 : Go to game project folder
    # STEP 5 : Create a bin(project.gdextension + lib.so) folder and a "cpp"(godot-cpp + src) folder inside project folder
    # STEP 6 : go to the godot cpp repository 
    # STEP 7 : check again godot version and check API version targeted by godot-cpp
    # STEP 8 : go to the "cpp" project folder and do git clone https://github.com/godotengine/godot-cpp.git
    # STEP 9 : verify versions
    # STEP 10 : go to cpp
    # STEP 11 : make SConstruct file for current API Version or get it from template
    # STEP 12 : Target ../bin folder and src/ folder inside SCons file
    # STEP 13 : go to cpp/src/ and create register_types.cpp and .h and extension.cpp and extension.h or get it from template
    # STEP 14 : make testing class inside extension files
    # STEP 15 : go to project/bin and make extension.gdextension file and put minimal godot version support of the project or get it from template
    # STEP 16 : go to cpp/SConstruct and compile  with SConstruct file and set platform with user os
    # STEP 17 : Launch godot, open the project, search for the testing class


# LOGIC 
    # CHECK OS, GODOT VERSIONS, API, AND DEPEDENCIES
    # BUILDING FOLDERS INSIDE SELECTED GAME PROJECT
    # INSTALL GODOT CPP REPO 
    # COPY PASTE SCONS AND CPP FILES IN FOLDERS
    # RUN COPYIED SCONS TO COMPILE CPP
    # RUN GODOT AND SELECTED PROJECT


# SECURITY CHECKS 
    # CHECK OS 
    # CHECK DEPEDENCIES, DO NOT RE INSTALL IF ALREADY HERE
        # CHECK GIT
        # CHECK PYTHON
        # CHECK C++ COMPILER(DEPENDS OS OS)
    # ASKING FOR USER IF HE WANTS TO INSTALL THESE DEPEDENCIES
    # CHECK CPP FOLDER AND ASK USER IF THEY WANT TO ERASE IT
    # CAT EVERY OUTPUT IN A LOG FILE, PARSE IT, FORM IT, PRINT IT IN GUI


# NEEDED IMPORTS 
import sys, os, subprocess, setproctitle


# GLOBAL VARIABLES
CURRENT_PATH = ""
GAME_PATH = ""
CPP_PATH = "cpp"
SRC_PATH = "src"

REG_FILES = ["register_types.cpp", "register_types.h"]
EXT_FILES = ["extension.cpp", "extension.h"]
SCONS = "SConstruct"
SCONS_PATH = ""

LIBNAME = "EXTENSION-NAME" # SEND TO SCONSTRUCT
PROJ_DIR = "project" # SEND TO SCONSTRUCT

GD_VER = (0,0,0)
API_VER = (0,0,0)

USR_OS = ""

CPP_REPO = "https://github.com/godotengine/godot-cpp.git"
TEMPLATE_REPO = "https://github.com/godotengine/godot-cpp-template"


# INIT GLOBAL VARIABLE IF USER ASKED TO MODIFY THEM
def init() : pass



# FUNCTIONS RELATIVE TO EVERY SECURITY CHECKS
def check_os() : pass

def check_dep() : pass

def check_cpp() : pass

def check_gdext() : pass







# FUNCTIONS RELATIVE TO EVERY STEPS 

# STEP 0
def get_gameproj_fold() : pass

# STEP 1
def get_gd_ver() : pass

# STEP 2
def verif_dep() : pass
def install_dep() : pass

# STEP 3
def verif_installs() : pass

# STEP 4-5
def mk_ext_folds() : pass

# STEP 6-7
def verif_again() : pass

# STEP 8
def clone_repo() : pass



# STEP 9-10-11 
def set_scons() : pass

# STEP 12-13-14
def set_cpp() : pass

# STEP 15
def set_gdext() : pass



# STEP 16
def comp() : pass

# STEP 17
def run_godot() : pass



# CALL EVERY FUNCTION IN A CORRECT FUNCTIONNING ORDER AFTER INIT()
def run() : pass 