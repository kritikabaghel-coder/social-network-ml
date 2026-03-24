# ⚠️ BEFORE PUSHING - CREATE GitHub Repository

## IMPORTANT: Create the Repository on GitHub FIRST

Follow these steps **before pushing**:

### Step 1: Create Repository on GitHub.com

1. Go to: **https://github.com/new**

2. Fill in these details:
   - **Repository name:** `social-network-ml`
   - **Description:** `ML for fake news detection using social networks and Streamlit app`
   - **Visibility:** Select **PUBLIC** ✅
   - **Leave all checkboxes UNCHECKED** (Initialize with README, .gitignore, etc should all be unchecked)

3. Click **"Create repository"** button

### Step 2: You're Ready to Push!

Once the repository is created on GitHub, your project is ready to push.

---

## Next: Push to GitHub

Once you've created the repository above, run:

```powershell
cd "c:\Users\KRITIKA\OneDrive\Desktop\project"
& "C:\Program Files\Git\bin\git.exe" push -u origin main
```

GitHub will prompt you for authentication. You have two options:

### Option A: Use Personal Access Token (Recommended)

1. Go to: **https://github.com/settings/tokens**
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Fill in:
   - **Token name:** `git-push-token`
   - **Expiration:** 30 days (or longer if you prefer)
   - **Select scopes:** Check the box next to `repo` (all suboptions will be selected)
4. Scroll to bottom → Click **"Generate token"**
5. **COPY THE TOKEN** (it starts with `ghp_`)
6. Go back to PowerShell

When PowerShell asks for a password, **paste the token** you just copied.

### Option B: Use GitHub CLI

If you install GitHub CLI:
```powershell
gh auth login
```

---

## 📋 Checklist

- [ ] Visited https://github.com/new
- [ ] Entered repository name: `social-network-ml`
- [ ] Selected PUBLIC visibility
- [ ] Left all checkboxes unchecked
- [ ] Clicked "Create repository"
- [ ] Ready to push to GitHub

Once done, **Run the push command above!**

---

**Your code is ready to push. Just create the GitHub repo first!** 🚀
