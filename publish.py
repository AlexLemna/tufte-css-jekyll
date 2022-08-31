import platform
from datetime import datetime
from pathlib import Path
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory

WORKING_DIR = Path(__file__).resolve()

MAC, LINUX, WINDOWS = (
    True if platform.system() == "Darwin" else False,
    True if platform.system() == "Linux" else False,
    True if platform.system() == "Windows" else False,
)

DEPLOY_BRANCH: str = "gh-pages"
DEPLOY_COMMIT_MSG: str = f"Site updated at #{datetime.utcnow()}"
MAIN_BRANCH: str = "src"
MAIN_COMMIT_MSG: str = "Commit changes in src"
REMOTE: str = "origin"


def main():
    with TemporaryDirectory() as temp_dir:
        print(f"Creating {temp_dir}...")
        if MAC or LINUX:
            cmds = [
                f"git commit --all --message {MAIN_COMMIT_MSG}",
                f"git push {REMOTE} {MAIN_BRANCH} --force",
                f"mv _site/* {temp_dir}",
                # From git checkout docs:
                #   If -B is given, branch is created if it
                #   doesn’t exist; otherwise, branch is reset.
                f"git checkout -B {DEPLOY_BRANCH}",
                f"rm -rf *",
                f"mv {temp_dir}/* .",
                f"git add .",
                f"git commit --all --message #{DEPLOY_COMMIT_MSG}",
                f"git push {REMOTE} {DEPLOY_COMMIT_MSG} --force",
                f"git checkout {MAIN_BRANCH}",
            ]
        elif WINDOWS:
            cmds = [
                f"git commit --all --message {MAIN_COMMIT_MSG}",
                f"git push {REMOTE} {MAIN_BRANCH} --force",
                f"Move-Item _site/* {temp_dir}",
                # From git checkout docs:
                #   If -B is given, branch is created if it
                #   doesn’t exist; otherwise, branch is reset.
                f"git checkout -B {DEPLOY_BRANCH}",
                f"Remove-Item -Recurse -Force *",
                f"Move-Item {temp_dir}/* .",
                f"git add .",
                f"git commit --all --message #{DEPLOY_COMMIT_MSG}",
                f"git push {REMOTE} {DEPLOY_COMMIT_MSG} --force",
                f"git checkout {MAIN_BRANCH}",
            ]

        for cmd in cmds:
            print(cmd)
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
                print(f"    {stdout}")
            if stderr:
                print(f"    {stderr}")

    print("done")


if __name__ == "__main__":
    main()
