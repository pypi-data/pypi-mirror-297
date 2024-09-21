import os

from HF_QuickUtils.QuickUtils import QuickDownload, QuickLoader
from HF_QuickUtils.ModelManager import ModelManager

hf_home = ""
hf_mirror = "https://hf-mirror.com"
if not os.environ.keys().__contains__("HF_HOME"):
    print("HF_HOME environment variable is not set")
else:
    hf_home = os.environ["HF_HOME"]

if not os.environ.keys().__contains__("HF_ENDPOINT"):
    print("HF_ENDPOINT environment variable is not set")
    print("using default endpoint \"https://hf-mirror.com\"")
else:
    hf_mirror = os.environ["HF_ENDPOINT"]


def get_hf_home() -> str:
    if (hf_home == ""):
        print("HF_HOME environment variable is not set")
        print("Please set HF_HOME environment variable or call set_hf_home function to set hf_home variable")
    return hf_home


def set_hf_home(hfhome: str) -> None:
    global hf_home
    hf_home = hfhome


def set_hf_mirror(hfmirror: str) -> None:
    global hf_mirror
    hf_mirror = hfmirror
