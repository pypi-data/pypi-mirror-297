from rich import print
import subprocess


def run_command(args):
    ps = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ps.returncode, ps


if __name__ == '__main__':
    run_command("pip install HydrogenLib -U")

