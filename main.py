# Godot GDextension C++ Auto Installer for any project 
# Available for : Linux, Windows



# BUILDING STEPS
    # STEP 0 : Verify game project folder
    # STEP 1 : Verify user godot version with godot executable file
    # STEP 2 : Verify Python, Git, Scons, C++ Compiler, install if there are no ones
    # STEP 3 : Verify the installations
    # STEP 4 : Go to game project folder
    # STEP 5 : Create a bin(project.gdextension + lib.so) folder and a "cpp"(godot-cpp + src folders) folder inside project folder
        # game project
            # res
            # bin
            # cpp
                # godot-cpp src
    # STEP 6 : go to the godot cpp repository 
    # STEP 7 : check again godot version and check API version targeted by godot-cpp
    # STEP 8 : go to the "cpp" project folder and do git clone https://github.com/godotengine/godot-cpp.git
    # STEP 9 : verify versions
    # STEP 10 : go to cpp
    # STEP 11 : Set the SConstruct file
    # STEP 12 : Target ../bin folder and src/ folder inside SCons file
    # STEP 13 : go to cpp/src/ and copy paste register_types.cpp and .h and extension.cpp and extension.h 
    # STEP 14 : make testing class inside extension files, they already exists no need
    # STEP 15 : go to project/bin and copy paste extension.gdextension file from template
    # STEP 16 : go to cpp/SConstruct and compile with SConstruct file and set platform with user os
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



# NEEDED IMPORTS 
import string
import sys, os, subprocess, setproctitle
import shutil, re, json


# GLOBAL VARIABLES
CURRENT_PATH = "" # where the script is executed
GAME_PATH = "" # project game path

BIN_PATH = "bin" # the bin path in GAME_PATH
CPP_PATH = "cpp" # cpp dir inside working dir
SRC_PATH = "src" # src dir insisde working dir
GDCPP_PATH = "godot-cpp" # godot cpp dir where to install the repo

REG_FILES = ["register_types.cpp", "register_types.h"]
EXT_FILES = ["example_class.cpp", "example_class.h"]
SCONS = "SConstruct"
SCONS_PATH = ""

LIBNAME = "EXTENSION-NAME" # SEND TO SCONSTRUCT
PROJ_DIR = "project" # SEND TO SCONSTRUCT

GD_VER = (0,0,0) # VERSION OF GODOT
API_VER = (0,0,0) # API VERSION FOR GODOT C++

USR_OS = "" # THE OS OF THE USER

CPP_REPO = "https://github.com/godotengine/godot-cpp.git"
TEMPLATE_REPO = "https://github.com/godotengine/godot-cpp-template"

DEP_LIST = ["python", "git", "c++"]

GODOT_EXE = "" # path of the godot executable


# INIT GLOBAL VARIABLE IF USER ASKED TO MODIFY THEM
def init(current_path : string, game_path : string, libname : string, projdir : string, gd_ver : tuple, api_ver : tuple) : 
    global CURRENT_PATH, GAME_PATH, LIBNAME, PROJ_DIR, GD_VER, API_VER
    CURRENT_PATH = current_path
    GAME_PATH = game_path
    LIBNAME = libname
    PROJ_DIR = projdir
    GD_VER = gd_ver
    API_VER = api_ver
    print(f"[init] script : {CURRENT_PATH}")
    print(f"[init] projet : {GAME_PATH} | lib : {LIBNAME} | proj_dir : {PROJ_DIR}")
    return



# FUNCTIONS RELATIVE TO EVERY SECURITY CHECKS
def check_os() :
    global USR_OS
    # Checks if linux or windows
    # put OS in USR_OS
    if sys.platform.startswith("linux"):
        USR_OS = "linux"
    elif sys.platform in ("win32", "cygwin"):
        USR_OS = "windows"
    else:
        USR_OS = ""
        print(f"[check_os] OS non supporté : {sys.platform}")
        return USR_OS
    print(f"[check_os] OS détecté : {USR_OS}")
    return USR_OS

def check_dep() : 
    # check for evrery depedencies
    # check git, python, c++ compiler
    # iterates on DEP_LIST
    # if every dep are here returns true
    # else return a list of needed depedencies to install
    missing = []
    for dep in DEP_LIST:
        if dep == "python":
            found = sys.version_info >= (3, 8) and subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True).returncode == 0
        elif dep == "git":
            found = shutil.which("git") is not None
        elif dep == "c++":
            compilers = ("cl", "g++", "clang++") if USR_OS == "windows" else ("g++", "clang++")
            found = any(shutil.which(c) for c in compilers)
        else:
            found = shutil.which(dep) is not None
        print(f"[check_dep] {dep} : {'OK' if found else 'manquant'}")
        if not found:
            missing.append(dep)
    if shutil.which("scons") is None:
        print("[check_dep] scons : manquant")
        missing.append("scons")
    else:
        print("[check_dep] scons : OK")
    if not missing:
        return True
    return missing


def check_gdext() : 
    # check if there is already gdextension installed in working directory
    # checks if there is already gdextension c++ installed too
    # returns true if there are both, else returns what is missing
    bin_dir = os.path.join(GAME_PATH, BIN_PATH)
    gd_dir = os.path.join(GAME_PATH, CPP_PATH, GDCPP_PATH)
    missing = []
    if not (os.path.isdir(bin_dir) and any(f.endswith(".gdextension") for f in os.listdir(bin_dir))):
        missing.append("gdextension")
    if not (os.path.isdir(gd_dir) and len(os.listdir(gd_dir)) > 0):
        missing.append("godot-cpp")
    if not missing:
        print("[check_gdext] gdextension et godot-cpp déjà installés")
        return True
    print(f"[check_gdext] manquant : {missing}")
    return missing







# FUNCTIONS RELATIVE TO EVERY STEPS 

# STEP 0
def set_gameproj_fold() : 
    global GAME_PATH
    # checks if GAME PATH exists
    # create it if it dos not exists
    # puts this path in GAME_PATH
    GAME_PATH = os.path.abspath(os.path.expanduser(GAME_PATH))
    if not os.path.exists(GAME_PATH):
        print(f"[Step 0] {GAME_PATH} n'existe pas, création du dossier")
        os.makedirs(GAME_PATH)
    elif not os.path.isfile(os.path.join(GAME_PATH, "project.godot")):
        print("[Step 0] attention : pas de project.godot dans ce dossier")
    print(f"[Step 0] GAME_PATH = {GAME_PATH}")
    return GAME_PATH

# STEP 1
def get_gd_ver() : 
    global GODOT_EXE, GD_VER, API_VER
    # checks godot version 
    # puts it in GD_VER and returns it
    # also checks API_VER available for GDEXTENSION C++
    exe = GODOT_EXE or shutil.which("godot") or shutil.which("godot4") or ""
    while True:
        exe = os.path.expanduser(exe)
        if exe and os.path.isfile(exe):
            r = subprocess.run([exe, "--version"], capture_output=True, text=True)
            m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", r.stdout + r.stderr)
            if r.returncode == 0 and m:
                break
        print("[Step 1] exécutable Godot introuvable ou invalide")
        exe = input("Chemin de l'exécutable Godot : ").strip().strip('"')
    GODOT_EXE = exe
    GD_VER = (int(m.group(1)), int(m.group(2)), int(m.group(3) or 0))
    print(f"[Step 1] version Godot : {GD_VER[0]}.{GD_VER[1]}.{GD_VER[2]}")
    API_VER = (GD_VER[0], GD_VER[1], 0)
    if shutil.which("git"):
        r = subprocess.run(["git", "ls-remote", "--heads", CPP_REPO], capture_output=True, text=True)
        cands = sorted((int(a), int(b)) for a, b in re.findall(r"refs/heads/(\d+)\.(\d+)\s*$", r.stdout, re.M)
                       if int(a) == GD_VER[0] and (int(a), int(b)) <= GD_VER[:2])
        if cands:
            API_VER = (cands[-1][0], cands[-1][1], 0)
    else:
        print("[Step 1] git absent : API estimée depuis la version de Godot, vérifiée après le clone")
    print(f"[Step 1] API godot-cpp visée : {API_VER[0]}.{API_VER[1]}")
    return [GD_VER, API_VER]

# STEP 2
def install_dep() : 
    inst = []
    # install python git and a c++ compiler
    # puts the exacts package it tried to install in the list
    missing = check_dep()
    if missing is True:
        print("[Step 2] rien à installer")
        return inst
    if USR_OS == "linux":
        table = {
            "apt-get": {"python": ["python3", "python3-pip"], "git": ["git"], "c++": ["build-essential"], "scons": ["scons"]},
            "dnf": {"python": ["python3", "python3-pip"], "git": ["git"], "c++": ["gcc-c++", "make"], "scons": ["scons"]},
            "pacman": {"python": ["python", "python-pip"], "git": ["git"], "c++": ["gcc", "make"], "scons": ["scons"]},
            "zypper": {"python": ["python3", "python3-pip"], "git": ["git"], "c++": ["gcc-c++", "make"], "scons": ["scons"]},
        }
        pm = next((p for p in table if shutil.which(p)), None)
        if pm is None:
            print("[Step 2] gestionnaire de paquets non reconnu (apt, dnf, pacman, zypper)")
            return inst
        for dep in missing:
            inst.extend(table[pm][dep])
        inst = list(dict.fromkeys(inst))
        print(f"[Step 2] installation via {pm} : {inst}")
        if pm == "apt-get":
            subprocess.run(["sudo", "apt-get", "update"])
            r = subprocess.run(["sudo", "apt-get", "install", "-y"] + inst)
        elif pm == "dnf":
            r = subprocess.run(["sudo", "dnf", "install", "-y"] + inst)
        elif pm == "pacman":
            r = subprocess.run(["sudo", "pacman", "-S", "--noconfirm"] + inst)
        else:
            r = subprocess.run(["sudo", "zypper", "--non-interactive", "install"] + inst)
        if r.returncode != 0:
            print("[Step 2] l'installation a échoué")
    elif USR_OS == "windows":
        ids = {"python": "Python.Python.3.12", "git": "Git.Git", "c++": "BrechtSanders.WinLibs.POSIX.UCRT"}
        for dep in missing:
            if dep == "scons":
                inst.append("scons (pip)")
                r = subprocess.run([sys.executable, "-m", "pip", "install", "scons"])
            else:
                inst.append(ids[dep])
                r = subprocess.run(["winget", "install", "--id", ids[dep], "-e", "--accept-package-agreements", "--accept-source-agreements"])
            if r.returncode != 0:
                print(f"[Step 2] échec de l'installation de {dep}")
    else:
        print("[Step 2] OS non supporté")
    return inst

# STEP 3
def verif_installs(inst) : 
    # inst = install_dep()
    # veritfy if pyton git and the c++ compiler are installed
    # returns true else false
    print(f"[Step 3] paquets installés/tentés : {inst}")
    res = check_dep()
    if res is True:
        for cmd in (["git", "--version"], ["scons", "--version"]):
            r = subprocess.run(cmd, capture_output=True, text=True)
            print(f"[Step 3] {r.stdout.strip().splitlines()[0] if r.stdout.strip() else cmd[0] + ' OK'}")
        print("[Step 3] toutes les dépendances sont installées")
        return True
    print(f"[Step 3] toujours manquant : {res}")
    if USR_OS == "windows":
        print("[Step 3] sous Windows, relance le script dans un nouveau terminal (PATH mis à jour)")
    return False

# STEP 4-5
def mk_ext_folds() : 
    # Creates bin folder inside GAME_PATH using BIN_PATH
    # Creates cpp folder inside GAME_PATH using CPP_PATH
    # inside cpp folder creates scr folder and godot-cpp folder SRC_PATH and GDCPP_PATH
    os.chdir(GAME_PATH)
    bin_dir = os.path.join(GAME_PATH, BIN_PATH)
    cpp_dir = os.path.join(GAME_PATH, CPP_PATH)
    folders = [bin_dir, cpp_dir, os.path.join(cpp_dir, SRC_PATH), os.path.join(cpp_dir, GDCPP_PATH)]
    for d in folders:
        os.makedirs(d, exist_ok=True)
    ok = all(os.path.isdir(d) for d in folders)
    print(f"[Step 4-5] dossiers {'créés' if ok else 'INCOMPLETS'} : {folders}")
    return ok

# STEP 6-7
    # VERIFY IF EVERY FOLDERS ARE HERE


# STEP 8
def clone_repo() :
    global API_VER
    # go to the "cpp" project folder and do git clone https://github.com/godotengine/godot-cpp.git
    # verify versions
    cpp_dir = os.path.join(GAME_PATH, CPP_PATH)
    os.chdir(cpp_dir)
    branch = f"{API_VER[0]}.{API_VER[1]}"
    print(f"[Step 8] clone de {CPP_REPO} (branche {branch})")
    r = subprocess.run(["git", "clone", "--depth", "1", "-b", branch, CPP_REPO, GDCPP_PATH])
    if r.returncode != 0:
        print(f"[Step 8] branche {branch} indisponible, clone de la branche par défaut")
        r = subprocess.run(["git", "clone", "--depth", "1", CPP_REPO, GDCPP_PATH])
        if r.returncode != 0:
            print("[Step 8] échec du clone")
            return False
    api_file = os.path.join(cpp_dir, GDCPP_PATH, "gdextension", "extension_api.json")
    try:
        with open(api_file, encoding="utf-8") as f:
            h = json.load(f)["header"]
    except (OSError, KeyError, ValueError):
        print("[Step 9] impossible de lire extension_api.json")
        return False
    API_VER = (h["version_major"], h["version_minor"], h.get("version_patch", 0))
    print(f"[Step 9] API godot-cpp : {API_VER[0]}.{API_VER[1]}.{API_VER[2]} | Godot : {GD_VER[0]}.{GD_VER[1]}.{GD_VER[2]}")
    if API_VER[:2] > GD_VER[:2]:
        print("[Step 9] l'API de godot-cpp est plus récente que ta version de Godot")
        return False
    return True



# STEP 10-11-12
def set_scons() :
    global SCONS_PATH
    # go to cpp folder
    #  Copy paste the SConstruct file inside
    # Target ../bin folder and src/ folder inside SCons file with BIN_PATH and SRC_PATH(already done)
    # send/write libname and proj_dir to the copied SConstruct
    cpp_dir = os.path.join(GAME_PATH, CPP_PATH)
    os.chdir(cpp_dir)
    template = os.path.join(CURRENT_PATH, SCONS)
    SCONS_PATH = os.path.join(cpp_dir, SCONS)
    if not os.path.isfile(template):
        print(f"[Step 11] template introuvable : {template}")
        return False
    shutil.copy(template, SCONS_PATH)
    with open(SCONS_PATH, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r'^libname\s*=\s*".*"', lambda m: f'libname = "{LIBNAME}"', text, flags=re.M)
    text = re.sub(r'^projectdir\s*=\s*".*"', lambda m: f'projectdir = "{PROJ_DIR}"', text, flags=re.M)
    text = re.sub(r'^from methods import print_error\s*$', 'def print_error(msg): print("ERROR: " + msg)', text, flags=re.M)
    text = re.sub(r'"api_version":\s*[\d.]+', lambda m: f'"api_version": {API_VER[0]}.{API_VER[1]}', text)
    with open(SCONS_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"[Step 11-12] {SCONS_PATH} écrit (libname={LIBNAME}, projectdir={PROJ_DIR}, api={API_VER[0]}.{API_VER[1]})")
    return True

# STEP 13-14
def set_cpp() : 
    # STEP 13 : go to cpp/src/ and copy paste register_types.cpp and .h and extension.cpp and extension.h 
    # STEP 14 : testing class already exists inside these files
    # returns true or false if error
    src_dir = os.path.join(GAME_PATH, CPP_PATH, SRC_PATH)
    os.chdir(src_dir)
    ok = True
    for name in REG_FILES + EXT_FILES:
        template = os.path.join(CURRENT_PATH, name)
        if not os.path.isfile(template):
            print(f"[Step 13] template introuvable : {template}")
            ok = False
            continue
        shutil.copy(template, os.path.join(src_dir, name))
        print(f"[Step 13] copié : {name}")
    return ok

# STEP 15
def set_gdext() : 
     # STEP 15 : go to project/bin and copy paste extension.gdextension file from template
    template = os.path.join(CURRENT_PATH, "example.gdextension")
    dest = os.path.join(GAME_PATH, BIN_PATH, f"{LIBNAME}.gdextension")
    if not os.path.isfile(template):
        print(f"[Step 15] template introuvable : {template}")
        return False
    with open(template, encoding="utf-8") as f:
        text = f.read()
    text = text.replace("EXTENSION-NAME", LIBNAME)
    text = re.sub(r'^compatibility_minimum\s*=\s*".*"', lambda m: f'compatibility_minimum = "{API_VER[0]}.{API_VER[1]}"', text, flags=re.M)
    with open(dest, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"[Step 15] {dest} écrit (compatibility_minimum = {API_VER[0]}.{API_VER[1]})")
    return True



# STEP 16
def comp() :
    # STEP 16 : go to cpp/SConstruct and compile with SConstruct file and set platform with user os
    cpp_dir = os.path.join(GAME_PATH, CPP_PATH)
    os.chdir(cpp_dir)
    cmd = ["scons", f"platform={USR_OS}", "target=template_debug", "compiledb=yes", f"-j{os.cpu_count() or 2}"]
    if USR_OS == "windows" and shutil.which("cl") is None:
        cmd.append("use_mingw=yes")
    print(f"[Step 16] compilation (plusieurs minutes la première fois) : {' '.join(cmd)}")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print("[Step 16] échec de la compilation")
        return False
    out_dir = os.path.join(GAME_PATH, BIN_PATH, USR_OS)
    if not os.path.isdir(out_dir) or not os.listdir(out_dir):
        print(f"[Step 16] aucune bibliothèque trouvée dans {out_dir}")
        return False
    print(f"[Step 16] bibliothèque générée : {os.listdir(out_dir)}")

    with open(os.path.join(cpp_dir, ".clangd"), "w", encoding="utf-8") as f:
        f.write("CompileFlags:\n  Remove: [-fno-gnu-unique]\n")
    print(f"[Step 16] .clangd écrit dans {cpp_dir}")
    return True

# STEP 17
def run_godot() : 
    print("[Step 17] lancement de l'éditeur Godot")
    print("[Step 17] test : ExampleClass.new().print_type(1) dans un script GDScript")
    subprocess.Popen([GODOT_EXE, "--editor", "--path", GAME_PATH])
    return



# CALL EVERY FUNCTION IN A CORRECT FUNCTIONNING ORDER AFTER INIT()
def run() : 
    game = sys.argv[1] if len(sys.argv) > 1 else input("Chemin du projet Godot : ").strip().strip('"')
    libname = input(f"Nom de la lib [{LIBNAME}] : ").strip() or LIBNAME
    init(os.path.dirname(os.path.abspath(__file__)), game, libname, "..", GD_VER, API_VER)

    if check_os() == "":
        sys.exit(1)
    set_gameproj_fold()
    get_gd_ver()

    if check_dep() is not True:
        if input("Installer les dépendances manquantes ? [o/N] ").strip().lower() not in ("o", "oui", "y", "yes"):
            print("[run] dépendances manquantes, arrêt")
            sys.exit(1)
        inst = install_dep()
        if not verif_installs(inst):
            sys.exit(1)

    state = check_gdext()
    if state is True or len(state) == 1:
        if input("Une installation existe déjà (cpp/gdextension). L'effacer ? [o/N] ").strip().lower() not in ("o", "oui", "y", "yes"):
            print("[run] installation existante conservée, arrêt")
            sys.exit(0)
        shutil.rmtree(os.path.join(GAME_PATH, CPP_PATH), ignore_errors=True)
        bin_dir = os.path.join(GAME_PATH, BIN_PATH)
        if os.path.isdir(bin_dir):
            for f in os.listdir(bin_dir):
                if f.endswith(".gdextension"):
                    os.remove(os.path.join(bin_dir, f))
        print("[run] ancienne installation effacée")

    if not mk_ext_folds():
        sys.exit(1)
    if not clone_repo():
        sys.exit(1)
    if not set_scons():
        sys.exit(1)
    if not set_cpp():
        sys.exit(1)
    if not set_gdext():
        sys.exit(1)
    if not comp():
        sys.exit(1)



if __name__ == "__main__":
    run()
