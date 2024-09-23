"""
 Copyright 2023. Aubin Ramon, Oliver Wissett and Pietro Sormanni. CC BY-NC-SA 4.0
"""

import argparse
import os,sys
import subprocess

MODELS_GIT_URL = "https://gitlab.developers.cam.ac.uk/ch/sormanni/abnativ-models.git"


# Check what OS we are on
def get_platform():
    return os.uname().sysname

model_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "pretrained_models")
if os.path.exists(model_path):
    sys.path.append(model_path)
    PRETRAINED_MODELS_DIR = model_path
elif get_platform() == "Linux" or get_platform() == "Darwin":
    # NOTE: Maybe use /usr/local/share/abnativ/models instead?
    PRETRAINED_MODELS_DIR = os.path.expanduser("~/.abnativ/models/pretrained_models")
elif get_platform() == "Windows":
    PRETRAINED_MODELS_DIR = os.path.expanduser(
        "~\\AppData\\Local\\abnativ\\models\\pretrained_models"
    )
else:
    raise Exception("Unsupported OS")


def clone_models(tag):
    cmd = [
        "git",
        "clone",
        MODELS_GIT_URL,
        PRETRAINED_MODELS_DIR,
        "--depth=1",  # Only clone the latest commit (these are large repos!)
        "--single-branch",  # Only clone the main branch
    ]

    if tag:
        cmd.append("--branch")
        cmd.append(tag)

    # Clone the models repo
    subprocess.run(cmd)


def pull_models():
    # Pull the models repo
    subprocess.run(["git", "pull"], cwd=PRETRAINED_MODELS_DIR)


def checkout_tag(tag: str):
    # Checkout a specific tag
    subprocess.run(["git", "checkout", tag], cwd=PRETRAINED_MODELS_DIR)


def init(args: argparse.Namespace):

    # Create the models directory
    if not os.path.exists(PRETRAINED_MODELS_DIR):
        print("Models not found in %s, downloading..." % PRETRAINED_MODELS_DIR)
        os.makedirs(PRETRAINED_MODELS_DIR)
        # Download the models
        clone_models(args.tag)
        print("Models downloaded in %s" % PRETRAINED_MODELS_DIR)
    elif len(os.listdir(PRETRAINED_MODELS_DIR)) == 0:
        print("Models not found in %s, downloading..." % PRETRAINED_MODELS_DIR)
        # Download the models
        clone_models(args.tag)
        print("Models downloaded in %s" % PRETRAINED_MODELS_DIR)
    else:
        print("Models found in %s, checking for updates..." % PRETRAINED_MODELS_DIR)
        if args.tag:
            # Checkout the tag
            checkout_tag(args.tag)
        else:
            # Update the models
            pull_models()

if __name__ == "__main__":
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    args = Namespace(tag=None)
    init(args)