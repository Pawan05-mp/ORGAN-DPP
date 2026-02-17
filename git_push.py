#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

project_dir = r"d:\New folder\organ-dpp"
repo_url = "https://github.com/Pawan05-mp/organdpp"

os.chdir(project_dir)

def run_git(cmd):
    """Run git command"""
    try:
        result = subprocess.run(f'git {cmd}', shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

print("ORGAN-DPP GitHub Push Script")
print("=" * 50)

commands = [
    'config --global user.name "GitHub User"',
    'config --global user.email "user@github.com"',
    'init',
    'add .',
    'commit -m "Initial commit - ORGAN-DPP with backend and frontend"',
    f'remote add origin {repo_url}',
    'branch -M main',
    f'push -u origin main'
]

for i, cmd in enumerate(commands, 1):
    print(f"\n[{i}/{len(commands)}] Running: git {cmd}")
    if not run_git(cmd):
        print(f"Failed at step {i}")
        sys.exit(1)

print("\n✅ Successfully pushed to GitHub!")
print(f"Repository: {repo_url}")
