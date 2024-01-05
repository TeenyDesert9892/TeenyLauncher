import subprocess
import pkg_resources

def update_libraries():
    packages = [dist.project_name for dist in pkg_resources.working_set]
    subprocess.call("pip install --upgrade " + ' '.join(packages), shell=True)

update_libraries()