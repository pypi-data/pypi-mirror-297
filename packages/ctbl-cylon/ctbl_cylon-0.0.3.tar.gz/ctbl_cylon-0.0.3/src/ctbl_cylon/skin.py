"""It implements a copy of a cylon: a git package, retrieved from a source.

A skin is a simply a set of folders and files to be put at the root of a user account in a server, with a set
of instructions about what to do to deploy. For example, I would like to copy most files, and then create symbolic
links to these files. Sometimes I would like to create certain files out of some content. All of these instructions
are contained within a config file, that is implemented through cbl_tools/config.

This class has no CLI interaction with the user.
"""

import os.path
from datetime import datetime
from ctbl_tools.config import config
from ctbl_tools.process import process
from ctbl_tools.git import git
from ctbl_tools import norm_path

class skin(config):

    _gitobj = None

    def __init__(self, path:str) -> None:
        """It loads a skin located in path. Path should be the root of the cylon folder,
        not the files/ folder which contains the ini file.

        Loading a skin means to load a local folder, already downloaded from a source, and
        reading the config file in order to check whether this copy is in good condition.
        """
        super().__init__(initpath=os.path.join(path, 'files/cylon.ini'), create_folder=False)

        # Valores importantes
        self.set('local', 'home', os.getenv('HOME'))
        self.set('local', 'sh', os.getenv('SHELL'))
        self._set_value('uname -o', 'os')
        self._set_value('uname -n', 'node')
        self._set_value('uname -p', 'arch')
        self.register(self._set_postvalue)

        self._gitobj = git(self.get_dirname())
        self.set('local', 'path', self._gitobj.local_path)

    def _set_value(self, com:str, label:str) -> None:
        p = process()
        p.run(com)
        if not p.is_ok() or not p.is_there_stdout():
            raise OSError(f"Cannot run {com}")
        self.set('local', label, p.stdout[0])

    def _set_postvalue(self) -> None:
        self.set('local', 'last_modified', datetime.now().strftime('%Y%m%d%H%M%S'))

    def check_n_fix_links(self):
        "Checks whether 'link' is a symbolic link to 'target'."

        home = self.get("local", "home")
        results = []
        for key in self.options("symlinks"):
            link = os.path.join(home, key)
            target = norm_path(self.get('local', 'path'), self.get("symlinks", key))

            if not os.path.exists(target):
                results.append(f"[r|Target {target} in config file does not exist]. Please check.\n")
                continue

            if os.path.exists(link) and not os.path.islink(link):
                results.append(f"[r|Link {link} mentioned in config file exists, and is not a link]. Please check.\n")
                continue

            if os.path.lexists(link) and os.path.realpath(link) != target:
                results.append(f"[r|{link} points to {os.path.realpath(link)} instead of {target}], so fixing it...\n")
                os.remove(link)
                continue

            if not os.path.exists(link):
                results.append(f"[y|Creating {link} -> {target}]\n")
                os.symlink(target, link)
                continue
        return "".join(results)
