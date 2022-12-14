from os import system
from os.path import basename, exists, join
from shutil import rmtree

from yaml import safe_load
from json import load as json_load

from infras import PRIVATE_PKHS

def read_cfg(cfg_path: str):
    """Read configuration file

    Args:
        cfg_path (str): configuration file path
    """
    with open(cfg_path, "r") as fid:
        cfg = safe_load(fid)

    return cfg

def obtain_cfg_name(cfg_path: str) -> str:
    """Get the configuration name from its path

    Args:
        cfg_path (str): configuration path

    Returns:
        str: configuration name
    """
    return basename(cfg_path).replace(".yml", "")



def create_git_url(shiny_cfg: dict) -> str:
    """Obtain git repository URL to be used, e.g.,
        for gitlab we have:
            https://user-xxx:glpat-12345@gitlab.com/my-repos/my_shiny_dev.git
        where
            user-xxx: the user name
            glpat-12345: private token
            itlab.com/my-repos/my_shiny_dev.git: the private repository
    Args:
        shiny_cfg (dict): shiny configurtion

    Returns:
        str: the processed URL
    """
    if (shiny_cfg["cred"] is None):
        url_to_use = shiny_cfg["url"]
    else:
        base_url = shiny_cfg["url"].replace("https://", "")
        url_to_use = f"https://{shiny_cfg['cred']['user']}:{shiny_cfg['cred']['token']}@{base_url}"

    return url_to_use


def download_base_repository(workdir: str, url: str, branch: str) -> str:
    """Download the latest base repository

    Args:
        workdir (str): working directory
        url (str): url to be used
    
    Returns:
        str: the local downloaded repository
    """
    repository_name = basename(url).replace(".git", "")
    local_repository_dir = join(workdir, repository_name)

    if exists(local_repository_dir):
        rmtree(local_repository_dir)

    git_name = basename(url).replace(".git", "")
    cmd = f"cd {workdir}; git clone {url}; cd {git_name}; git checkout {branch}"
    system(cmd)

    return local_repository_dir


def get_app_dependant_cloud_init(repos_dir: str, app_names: list) -> dict:
    """application dependant cloud init information

    Args:
        repos_dir (str): repository directory
        app_names (list): application names in a list

    Returns:
        dict: cloud init for different applications
    """
    app_cloud_init = {}
    for app_name in app_names:
        proc_cloud_init = join(repos_dir, app_name, "cloud-init.sh")

        if not exists(proc_cloud_init):
            raise Exception(f"cloud-init cannot be found for {app_name}")

        app_cloud_init[app_name] = [f"# {app_name} dependancies:\n"]
        with open(proc_cloud_init) as fid:
            for line in fid:
                if not (line.startswith("#") or line == "\n"):
                    app_cloud_init[app_name].append(line)
    
    return app_cloud_init


def obtain_private_packages(renv_lock_file: str) -> list or None:
    """Obtain private package that to be installed via renv.lock
        Due to some unknown reasons (Oct 2022), we are not able to
        install private packages (e.g., motplotr) through renv.restore(),
        therefore we skip it in renv, and install it seperately ... 

    Args:
        renv_lock_file (str): renv.lock file path

    Returns:
        list or None: a list of existing private packages
    """
    existing_pkgs = []

    with open(renv_lock_file) as fid:
        pkgs = json_load(fid)["Packages"]

    for private_pkg in PRIVATE_PKHS:

        if private_pkg in pkgs:

            existing_pkgs.append("'" + private_pkg + "'")

    if len(existing_pkgs) == 0:
        return None

    return "c(" + ', '.join(existing_pkgs) + ")"




    


    
