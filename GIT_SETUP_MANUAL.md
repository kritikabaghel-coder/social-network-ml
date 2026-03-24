# Manual Git Installation & GitHub Push Guide

## ⚠️ Git Not Installed Yet

The automated Git installation requires administrator privileges. Follow these manual steps:

---

## STEP 1: Download & Install Git

1. Go to: **https://git-scm.com/download/win**
2. Click **"64-bit Git for Windows Setup"** (most common)
3. **Right-click the installer** → **"Run as administrator"**
4. Click **"Yes"** when prompted
5. Follow the installation wizard:
   - Click **"Next"** through all screens
   - Keep default settings
   - Click **"Finish"** at the end

**Verify installation:**
- Open a NEW PowerShell window
- Type: `git --version`
- You should see: `git version 2.x.x.windows.1`

✅ Git is now installed!

---

## STEP 2: Configure Git (Run After Installation)

Open PowerShell and run these commands:

```powershell
git config --global user.name "Kritika Baghel"
git config --global user.email "your-email@example.com"
```

**Replace** `your-email@example.com` with your actual email.

Verify:
```powershell
git config --global user.name
git config --global user.email
```

✅ Git is configured!

---

## STEP 3: Initialize Your Project with Git

Navigate to your project folder:

```powershell
cd "c:\Users\KRITIKA\OneDrive\Desktop\project"
```

Initialize git:

```powershell
git init
```

Expected output:
```
Initialized empty Git repository in C:\Users\KRITIKA\OneDrive\Desktop\project\.git
```

✅ Git repository initialized!

---

## STEP 4: Check Project Status

```powershell
git status
```

Expected output:
```
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore
        README.md
        app.py
        ...

nothing added to commit but untracked files present (use "git add" to track)
```

✅ Git sees all your files!

---

## STEP 5: Add All Files to Git

```powershell
git add .
```

Verify:
```powershell
git status
```

Expected output:
```
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .gitignore
        new file:   README.md
        ...
```

✅ Files are staged!

---

## STEP 6: Create Your First Commit

```powershell
git commit -m "Initial commit: Social network ML project with Streamlit app"
```

Expected output:
```
[master (root-commit) abc1234] Initial commit: Social network ML project
 20 files changed, 3000 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 ...
```

✅ Commit created!

---

## STEP 7: Create GitHub Repository

1. Go to **https://github.com/new**
2. Fill in:
   - **Repository name:** `social-network-ml` (or `fake-news-detector`)
   - **Description:** "ML for fake news detection using social networks and Streamlit"
   - **Visibility:** Select **PUBLIC**
   - Leave all other options unchecked

3. Click **"Create repository"**

✅ GitHub repository created!

---

## STEP 8: Connect to GitHub & Push

GitHub will show you instructions. Run these commands:

```powershell
git remote add origin https://github.com/kritikabaghel-coder/social-network-ml.git
```

Rename branch to `main`:
```powershell
git branch -M main
```

Push your code:
```powershell
git push -u origin main
```

**You'll be prompted for authentication:**

### Option A: Use Personal Access Token (Recommended)

1. Go to: **https://github.com/settings/tokens**
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `git-push-token`
4. Select scopes: Check **`repo`** (all suboptions)
5. Scroll down → Click **"Generate token"**
6. **Copy the token** (long string of characters)
7. Go back to PowerShell when prompted for password
8. **Paste the token** (it won't show as you type - just paste and press Enter)

### Option B: Use GitHub CLI (Alternative)

If you have GitHub CLI installed:
```powershell
gh auth login
```

---

## STEP 9: Verify on GitHub

1. Visit: **https://github.com/kritikabaghel-coder/social-network-ml**
2. You should see:
   - ✅ All your files listed
   - ✅ README.md displayed
   - ✅ Code browser showing folders

✅ Your project is on GitHub!

---

## 🎉 Success!

Your project is now on GitHub and ready to share! 

**Your live project URL:** 
```
https://github.com/kritikabaghel-coder/social-network-ml
```

**Next steps:**
1. Share on LinkedIn
2. Deploy Streamlit app (follow STREAMLIT_DEPLOYMENT_GUIDE.md)
3. Add the live Streamlit URL to GitHub README

---

## 🔄 Future Updates

To push changes in the future:

```powershell
# Make changes to your files
# Then:

git status                          # See what changed
git add .                           # Stage changes
git commit -m "Add new feature"     # Commit
git push                            # Push to GitHub
```

---

## ⚠️ Troubleshooting

### Error: "fatal: 'origin' does not appear to be a 'git' repository"

**Solution:** You haven't added the remote yet. Run:
```powershell
git remote add origin https://github.com/kritikabaghel-coder/social-network-ml.git
git push -u origin main
```

### Error: "Permission denied (publickey)"

**Solution:** Use HTTPS instead of SSH. Make sure you're using:
```
https://github.com/kritikabaghel-coder/social-network-ml.git
```
(not the SSH version)

### Error: "fatal: not a git repository"

**Solution:** Reinitialize git:
```powershell
cd "c:\Users\KRITIKA\OneDrive\Desktop\project"
git init
git add .
git commit -m "Initial commit"
```

### "Authentication failed" error

**Solution:**
1. Go to: https://github.com/settings/tokens
2. Generate a new token (see Step 8, Option A)
3. Use token as password instead of GitHub password

---

## ✅ Checklist

- [ ] Downloaded and installed Git
- [ ] Opened NEW PowerShell window to verify `git --version`
- [ ] Configured Git with `git config --global`
- [ ] Ran `git init` in project folder
- [ ] Ran `git add .` to stage files
- [ ] Ran `git commit -m "..."` to commit
- [ ] Created repository on GitHub.com
- [ ] Ran `git remote add origin ...`
- [ ] Ran `git push -u origin main`
- [ ] Verified files appear on GitHub.com

---

## 📞 Need Help?

- Git documentation: https://git-scm.com/doc
- GitHub help: https://docs.github.com
- Stack Overflow: Search your error message

**You've got this! 💪**
