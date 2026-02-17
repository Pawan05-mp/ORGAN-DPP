#!/usr/bin/env python3
import os
import sys
from git import Repo
from pathlib import Path

# Project directory
project_dir = r"d:\New folder\organ-dpp"
repo_url = "https://github.com/Pawan05-mp/organdpp"

os.chdir(project_dir)

try:
    # Initialize repo if not already initialized
    if not os.path.exists(os.path.join(project_dir, '.git')):
        print("Initializing git repository...")
        repo = Repo.init(project_dir)
    else:
        repo = Repo(project_dir)
    
    # Configure git user (use GitHub credentials)
    config_writer = repo.config_writer()
    config_writer.set_value("user", "name", "GitHub User").release()
    config_writer = repo.config_writer()
    config_writer.set_value("user", "email", "user@github.com").release()
    
    # Add all files
    print("Adding files to git...")
    repo.index.add(['*'])
    
    # Create initial commit
    print("Creating commit...")
    repo.index.commit("Initial commit - ORGAN-DPP project with backend and frontend")
    
    # Add remote
    print(f"Adding remote: {repo_url}")
    if 'origin' in [remote.name for remote in repo.remotes]:
        repo.delete_remote('origin')
    repo.create_remote('origin', repo_url)
    
    # Push to GitHub
    print("Pushing to GitHub...")
    origin = repo.remote('origin')
    origin.push(refspec='master:main')
    
    print("✅ Successfully pushed to GitHub!")
    print(f"Repository: {repo_url}")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
