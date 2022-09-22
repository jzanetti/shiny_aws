from glob import glob
from os.path import basename
from pathlib import Path
from subprocess import Popen

# -------------------------------
# shiny_app_local: local shiny application directory
# shiny_app_s3: shiny application on S3
# -------------------------------
shiny_app_local = "../examples/hello_world"
shiny_app_s3 = "s3://mot-shiny-app/r/"

# -------------------------------
# Codes start from here
# -------------------------------
shiny_name = basename(shiny_app_local)
all_files = glob(f"{shiny_app_local}/*")

for proc_file in all_files:
    proc_file = Path(proc_file)
    if proc_file.suffix in [".R", ".sh", ".conf", ".md"]:
        proc_filename = proc_file.name
        cmd = f"aws s3 cp {proc_file} {shiny_app_s3}/{shiny_name}/{proc_filename}"
        print(cmd)
        p = Popen(cmd, shell=True)
        p.communicate()
