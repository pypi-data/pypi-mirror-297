import subprocess
from typing import List

import typer
from yaspin import yaspin
from yaspin.spinners import Spinners

app = typer.Typer()

@app.command()
def list():
    for l in get_running_vms():
        print(l)

def get_running_vms():
    with yaspin(Spinners.aesthetic, text="Grabbing vms...", color="yellow") as spinner:
        res = subprocess.run(['gcloud', 'compute', 'instances', 'list', '--project', 'fde-playground', '--filter=status=RUNNING', '--format=table(name, zone, machineType, networkInterfaces.networkIP, status)', '--sort-by=name'], check=True,
                             capture_output=True, encoding='utf-8')
        lines = res.stdout.split('\n')
        spinner.ok("✅ ")
        return lines

@app.command()
def stop(names: List[str]):
    for name in names:
        try:
            uri = get_vm_uri(name)
            stop_vm(uri)
        except (ValueError, subprocess.CalledProcessError):
            pass


def stop_vm(uri):
    with yaspin(Spinners.aesthetic, text=f"Stopping vm ({uri})...", color="yellow") as spinner:
        try:
            subprocess.run(['gcloud', 'compute', 'instances', 'stop', uri],
                       check=True,
                       capture_output=True, encoding='utf-8')
            spinner.ok("✅ ")
        except subprocess.CalledProcessError as e:
            spinner.fail("💥 ")
            raise e


def get_vm_uri(name):
    with yaspin(Spinners.aesthetic, text=f"Getting URI for vm ({name})...", color="yellow") as spinner:
        try:
            res = subprocess.run(
                ['gcloud', 'compute', 'instances', 'list', f'--filter=name:{name}', '--uri', '--project', 'fde-playground'],
                check=True,
                capture_output=True, encoding='utf-8')
            uri = res.stdout.split('\n')[0]
            if uri:
                spinner.ok("✅ ")
                return uri
            else:
                raise ValueError(f"Couldn't get URI for vm {name}")
        except (ValueError, subprocess.CalledProcessError) as e:
            spinner.fail("💥 ")
            raise e



if __name__ == '__main__':
    app()

