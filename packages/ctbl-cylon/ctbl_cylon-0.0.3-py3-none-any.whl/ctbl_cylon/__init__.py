__all__ = ["cprint", "get_remote_folders"]

import re
import os.path
from colorama import Fore, Style
from ctbl_tools.process import process

#> -----------------------------------------------------------------------------------
def cprint(arg:str, return_it:bool = False):
    """Prints colored output.
    
    This method prints colored output. The argument has to specify which substrings
    should be colored through the following format:
    
    "... bla bla bla [r|this text will be in red] and [b|this one will go in blue]..."

    Allowed colors are r (red), g (green), b (blue) and y (yellow)."""

    arg = re.sub(r"\[r\|([^]]+?)\]", Fore.RED + Style.BRIGHT + r"\1" + Style.RESET_ALL, arg)
    arg = re.sub(r"\[g\|([^]]+?)\]", Fore.GREEN + Style.BRIGHT + r"\1" + Style.RESET_ALL, arg)
    arg = re.sub(r"\[b\|([^]]+?)\]", Fore.BLUE + Style.BRIGHT + r"\1" + Style.RESET_ALL, arg)
    arg = re.sub(r"\[y\|([^]]+?)\]", Fore.YELLOW + Style.BRIGHT + r"\1" + Style.RESET_ALL, arg)

    if return_it:
        return arg
    else:
        print(arg)
        return None

#> -----------------------------------------------------------------------------------
def get_remote_folders(rmt_server:str, rmt_path:str, get_description:bool = False):
    """It gets all remote folders as a list, using the cylon convention.
    
    If rmt_server or rmt_path are empty, it return None."""

    if not rmt_server or not rmt_path:
        return None

    tst = process()
    tst.run(f"rsh {rmt_server} ls -1 {rmt_path}")
    if not tst.is_ok():
        return tst.stderr

    items = tst.stdout
    tst.reset()
    if get_description:
        desc = {}
        for item in items:
            if item.endswith('/'):
                fld = item.rstrip('/')
                if not fld in desc:
                    desc[fld] = ''

            elif item.endswith('.txt'):
                file = os.path.join(rmt_path, item)
                fld = item.removesuffix('.txt') + '.git'
                tst.run(f"rsh {rmt_server} cat {file}")
                if tst.is_ok():
                    desc[fld] = "\n".join(tst.stdout)
                else:
                    desc[fld] = "No description"
        return desc
    else:
        folders = filter(lambda name: name.endswith('/'), items)
        lst = []
        for fld in folders:
            lst.append(fld.rstrip("/"))
        return lst
