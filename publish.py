import platform
from datetime import datetime
from pathlib import Path
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory

WORKING_DIR = Path(__file__).resolve().parent

MAC, LINUX, WINDOWS = (
    True if platform.system() == "Darwin" else False,
    True if platform.system() == "Linux" else False,
    True if platform.system() == "Windows" else False,
)

DEPLOY_BRANCH: str = "gh-pages"
DEPLOY_COMMIT_MSG: str = f"Site updated at {datetime.utcnow()}"
MAIN_BRANCH: str = "src"
MAIN_COMMIT_MSG: str = "script: update (test)"
REMOTE: str = "origin"


def main():
    with TemporaryDirectory() as temp_dir:
        print(f"Creating {temp_dir}...")
        if MAC or LINUX:
            cmds = [
                f'git commit --all --message="{MAIN_COMMIT_MSG}"',
                f"git push {REMOTE} {MAIN_BRANCH} --force",
                f"mv src/_site/* {temp_dir}",
                # From git checkout docs:
                #   If -B is given, branch is created if it
                #   doesn’t exist; otherwise, branch is reset.
                f"git checkout -B {DEPLOY_BRANCH}",
                f"rm -rf src",
                f"mv {temp_dir}/* .",
                f"git add .",
                f'git commit --all --message="{DEPLOY_COMMIT_MSG}"',
                f"git push {REMOTE} {DEPLOY_BRANCH} --force",
                f"git checkout -B {MAIN_BRANCH}",  # see comment above for -B
            ]
        elif WINDOWS:
            cmds = [
                f'git commit --all --message="{MAIN_COMMIT_MSG}"',
                f"git push {REMOTE} {MAIN_BRANCH} --force",
                f"powershell.exe Move-Item src/_site/* {temp_dir}",
                # From git checkout docs:
                #   If -B is given, branch is created if it
                #   doesn’t exist; otherwise, branch is reset.
                f"git checkout -B {DEPLOY_BRANCH}",
                f"powershell.exe Remove-Item -Recurse -Force src",
                f"powershell.exe Move-Item {temp_dir}/* .",
                f"git add .",
                f'git commit --all --message="{DEPLOY_COMMIT_MSG}"',
                f"git push {REMOTE} {DEPLOY_BRANCH} --force",
                f"git checkout -B {MAIN_BRANCH}",  # see comment above for -B
            ]

        for cmd in cmds:
            print(f"CMD: {cmd}")
            args = cmd.split()  # str -> list[str] on whitespace
            process = Popen(
                args,
                shell=True,
                stderr=PIPE,
                stdout=PIPE,
                text=True,
                cwd=str(WORKING_DIR),
            )
            stdout, stderr = process.communicate()
            if stdout:
                print(f"OUT:    {stdout}")
            if stderr:
                print(f"ERR:    {stderr}")
            print()

    print("done")


if __name__ == "__main__":
    main()
