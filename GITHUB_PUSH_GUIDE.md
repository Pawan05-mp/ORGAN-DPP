# Push ORGAN-DPP to GitHub - Manual Instructions

Since git installation is having issues, here are manual steps to push your project to GitHub:

## Step 1: Install Git
Download from: https://git-scm.com/download/win
Run the installer and complete the installation.

## Step 2: Configure Git
After installing, open Git Bash or PowerShell and run:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@github.com"
```

## Step 3: Navigate to Project
```bash
cd "d:\New folder\organ-dpp"
```

## Step 4: Initialize Git Repository
```bash
git init
```

## Step 5: Add All Files
```bash
git add .
```

## Step 6: Create Initial Commit
```bash
git commit -m "Initial commit - ORGAN-DPP project with backend and frontend"
```

## Step 7: Add Remote Repository
Replace with your actual GitHub repository URL:
```bash
git remote add origin https://github.com/Pawan05-mp/organdpp.git
```

## Step 8: Create Main Branch
```bash
git branch -M main
```

## Step 9: Push to GitHub
```bash
git push -u origin main
```

If prompted for credentials, use your GitHub personal access token (PAT):
- Go to: https://github.com/settings/tokens
- Create a new token with 'repo' scope
- Use as password when git prompts

## Project Structure Being Pushed:
```
organ-dpp/
├── backend/
│   ├── api/
│   │   └── generate.py (with absolute imports)
│   ├── curriculum/
│   ├── database/
│   ├── dpp/
│   ├── models/
│   ├── training/
│   │   └── trainer.py (with absolute imports)
│   ├── utils/
│   ├── main.py (with CORS enabled)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── layout.tsx
│   │       ├── page.tsx (with working API integration)
│   │       └── globals.css
│   ├── tailwind.config.mjs
│   ├── postcss.config.mjs
│   ├── next.config.ts
│   ├── package.json (ES modules configured)
│   └── tsconfig.json
├── README.md
└── [other project files]
```

## .gitignore Recommendations
Create a `.gitignore` file in the root with:
```
node_modules/
.next/
.venv/
__pycache__/
*.pyc
.env
.env.local
.DS_Store
```

## Notes:
- Backend running on: http://127.0.0.1:8000
- Frontend running on: http://localhost:3000
- All relative imports converted to absolute imports
- CORS enabled for frontend-backend communication
- Tailwind CSS v3 and Next.js 16 configured
