# GitHub Push Guide: Step-by-Step

## 📋 Prerequisites

Before starting, you need:
1. A GitHub account (free at github.com)
2. Git installed on your computer
3. Your project folder organized (✓ Already done!)

**Check if Git is installed:**
```powershell
git --version
```

If not installed, download from: https://git-scm.com/

---

## 🚀 Step-by-Step Instructions

### STEP 1: Verify Your Project Structure ✓

Navigate to your project folder:
```powershell
cd c:\Users\KRITIKA\OneDrive\Desktop\project
```

Check what's there:
```powershell
dir
```

You should see:
```
.gitignore
README.md
requirements.txt
DATASET.md
data/
scripts/
results/
notebooks/
```

✅ **Status**: Project is ready

---

### STEP 2: Initialize Git Repository (First Time Only)

If you haven't already, initialize git:
```powershell
git init
```

**Output:**
```
Initialized empty Git repository in C:\Users\KRITIKA\OneDrive\Desktop\project\.git
```

**What it does**: Creates `.git` folder to track changes

✅ **Status**: Git repository initialized

---

### STEP 3: Check Git Status

See what files will be committed:
```powershell
git status
```

**Expected output:**
```
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore
        README.md
        requirements.txt
        DATASET.md
        data/
        scripts/
        results/
        notebooks/

nothing added to commit but untracked files
```

✅ **Status**: Git sees all your files

---

### STEP 4: Add All Files to Staging Area

```powershell
git add .
```

**What it does**: Stages all files (except those in `.gitignore`)

**Verify with:**
```powershell
git status
```

**Expected output:**
```
On branch master
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .gitignore
        new file:   README.md
        new file:   requirements.txt
        ...
```

✅ **Status**: Files are staged and ready

---

### STEP 5: Configure Git (First Time Only)

Set your identity:
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Example:**
```powershell
git config --global user.name "Kritika Singh"
git config --global user.email "kritika.singh@example.com"
```

Verify:
```powershell
git config --global user.name
git config --global user.email
```

✅ **Status**: Git is configured

---

### STEP 6: Create First Commit

Commit all staged files:
```powershell
git commit -m "Initial commit: Social network ML project for fake news detection"
```

**Good commit messages:**
- ✅ `Initial commit: Social network analysis ML project`
- ✅ `Add data exploration and network analysis scripts`
- ❌ `first commit`
- ❌ `fix`

**Expected output:**
```
[master (root-commit) a1b2c3d] Initial commit: Social network ML project
 15 files changed, 1500 insertions(+)
 create mode 100644 README.md
 create mode 100644 requirements.txt
 ...
```

✅ **Status**: Changes committed locally

---

### STEP 7: Create GitHub Repository

1. Go to **https://github.com/new**
2. Fill in:
   - **Repository name**: `social-network-ml` (or similar)
   - **Description**: "ML for fake news detection using social networks"
   - **Visibility**: Select **PUBLIC** (good for portfolios)
   - **Initialize with**: Leave UNCHECKED (you already have files)

3. Click **"Create repository"**

**Expected result:** GitHub shows instructions like:
```
…or push an existing repository from the command line

git remote add origin https://github.com/YOUR-USERNAME/social-network-ml.git
git branch -M main
git push -u origin main
```

✅ **Status**: GitHub repository created

---

### STEP 8: Add Remote Repository URL

Connect your local git to GitHub:
```powershell
git remote add origin https://github.com/YOUR-USERNAME/social-network-ml.git
```

**Replace:**
- `YOUR-USERNAME` with your GitHub username
- `social-network-ml` with your repository name

**Example:**
```powershell
git remote add origin https://github.com/kritika-singh/social-network-ml.git
```

**Verify:**
```powershell
git remote -v
```

**Expected output:**
```
origin  https://github.com/YOUR-USERNAME/social-network-ml.git (fetch)
origin  https://github.com/YOUR-USERNAME/social-network-ml.git (push)
```

✅ **Status**: Remote configured

---

### STEP 9: Rename Branch to 'main' (Optional but Modern)

```powershell
git branch -M main
```

This renames `master` → `main` (GitHub's new standard)

Verify:
```powershell
git branch
```

**Output:**
```
* main
```

✅ **Status**: Branch renamed

---

### STEP 10: Push to GitHub

Push your code:
```powershell
git push -u origin main
```

**What it does**: 
- `-u`: Sets `origin/main` as default upstream
- `origin`: Remote name (GitHub)
- `main`: Branch name

**You may be prompted for credentials:**
- **Use GitHub token** (not password):
  1. Go to: https://github.com/settings/tokens
  2. Click "Generate new token (classic)"
  3. Give it permissions (select `repo` for full access)
  4. Copy the token
  5. Paste into the terminal when prompted

**Expected output:**
```
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 8 threads
Compressing objects: 100% (12/12), done.
Writing objects: 100% (15/15), 2.50 KiB | 2.50 MiB/s, done.
Total 15 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR-USERNAME/social-network-ml.git
 * [new branch]      main -> main
Branch 'main' is set to track remote branch 'main' from 'origin'.
```

✅ **Status**: Code is on GitHub!

---

### STEP 11: Verify on GitHub

1. Go to: **https://github.com/YOUR-USERNAME/social-network-ml**
2. You should see:
   - ✅ All your files listed
   - ✅ README.md displayed nicely
   - ✅ Green code badge
   - ✅ File count in top bar

3. Click on files to verify they're there:
   - README.md
   - requirements.txt
   - scripts/ folder
   - data/ folder

✅ **Status**: Project is live on GitHub!

---

## 🔄 Future Workflow (For Future Updates)

Every time you make changes:

```powershell
# 1. See what changed
git status

# 2. Stage changes
git add .

# 3. Commit with message
git commit -m "Add cross-validation to model evaluation"

# 4. Push to GitHub
git push
```

---

## ⚠️ Troubleshooting

### Problem: "fatal: not a git repository"
**Solution:**
```powershell
git init
```

### Problem: "fatal: 'origin' does not appear to be a 'git' repository"
**Solution:**
```powershell
git remote add origin https://github.com/YOUR-USERNAME/your-repo.git
```

### Problem: "permission denied (publickey)"
**Solution:** Use HTTPS token instead of SSH:
```powershell
git remote set-url origin https://github.com/YOUR-USERNAME/your-repo.git
```

### Problem: "Authentication failed"
**Solution:** 
1. Go to: https://github.com/settings/tokens
2. Generate new personal access token (classic)
3. Use token as password when prompted

### Problem: "refusing to merge unrelated histories"
**Solution:**
```powershell
git pull origin main --allow-unrelated-histories
git push origin main
```

---

## ✅ Complete Checklist

Use this to verify everything worked:

- [ ] Project folder organized with README, scripts, data, results
- [ ] Git repository initialized (`git init`)
- [ ] GitHub account created
- [ ] GitHub repository created (PUBLIC)
- [ ] Remote added (`git remote add origin ...`)
- [ ] Files staged (`git add .`)
- [ ] Initial commit created (`git commit -m ...`)
- [ ] Branch renamed to main (`git branch -M main`)
- [ ] Code pushed to GitHub (`git push -u origin main`)
- [ ] Files visible on GitHub.com
- [ ] README.md displays correctly
- [ ] All scripts are visible

---

## 🎉 Success Indicators

Visit your GitHub repository URL and you should see:

✅ Project name and description  
✅ Green "Code" button with file count  
✅ README.md displayed as formatted markdown  
✅ File browser showing all folders  
✅ Your commits listed in "Commits" section  
✅ Branch showing "main"  

**Example URL:** `https://github.com/kritika-singh/social-network-ml`

---

## 📚 Next Steps After Pushing

1. **Add GitHub link to resume/portfolio**
   "See my ML project: github.com/username/social-network-ml"

2. **Share on LinkedIn**
   "Just published my social network ML project on GitHub!"

3. **Add more features** (using the git workflow)
   - Implement improvements from INTERNSHIP_IMPROVEMENTS.md
   - Commit: `git commit -m "Add cross-validation to model"`
   - Push: `git push`

4. **Create branches for experiments**
   ```powershell
   git checkout -b feature/add-neural-network
   # Make changes
   git push origin feature/add-neural-network
   ```

5. **Monitor GitHub activity**
   - Watch for stars ⭐
   - Check if anyone forks it
   - Respond to issues

---

## 💡 Tips for Maximum Impact

### Enhance Your Repository:

1. **Add Topics** (on GitHub repo page)
   - Click ⚙️ settings → Topics
   - Add: machine-learning, fake-news, network-analysis, python

2. **Write a Compelling Description**
   - Go to ⚙️ settings → General
   - Update "About" section with 1-2 sentences

3. **Add Badges to README**
   ```markdown
   ![Python](https://img.shields.io/badge/Python-3.13-blue)
   ![Last Commit](https://img.shields.io/github/last-commit/username/repo)
   ```

4. **Pin the Repository**
   - Go to your GitHub profile
   - Click ⭐ Pin this repository
   - Shows on your profile when people visit

5. **Add a License**
   - GitHub page → Add file → LICENSE
   - Choose MIT (most popular for ML projects)

---

## 📖 Quick Reference Commands

```powershell
# Initial setup (first time only)
git init
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Add and commit
git add .
git commit -m "Your message"

# Connect to GitHub (first time)
git remote add origin URL
git branch -M main

# Push
git push -u origin main          # First time
git push                          # Future pushes

# Check status
git status                       # See what changed
git log                          # See commit history
git remote -v                    # See remote URL
```

---

## 🚀 You're Done!

Your project is now on GitHub and visible to:
- ✅ Hiring managers
- ✅ Internship recruiters  
- ✅ Collaborators
- ✅ The internet!

**Next:** Add improvements from INTERNSHIP_IMPROVEMENTS.md and watch your project grow! 📈

---

## 📞 Still Need Help?

GitHub Help: https://docs.github.com/en/github/getting-started-with-github  
Common Issues: https://docs.github.com/en/github/contact-us  
Stack Overflow: Search "git push" or "GitHub"  

**You've got this!** 💪
