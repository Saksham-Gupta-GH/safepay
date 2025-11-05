# MongoDB Atlas Troubleshooting Guide

## 🔍 Quick Diagnosis

Run this test script to diagnose your connection issue:

```bash
cd /Users/jawaharlal/Safepay2
python3 test_connection.py
```

This will tell you exactly what's wrong and how to fix it.

---

## ❌ Error: "bad auth : authentication failed"

### What it means:
Your username or password is incorrect.

### Solutions:

#### 1. Verify Your Database User Credentials

Go to MongoDB Atlas:
1. Click **"Database Access"** (left sidebar)
2. Check your username
3. If unsure about password, click **"Edit"** → **"Edit Password"** → Set a new simple password

**Use a simple password:** Only letters and numbers (e.g., `mypassword123`)

#### 2. Get a Fresh Connection String

1. Go to **"Database"** (left sidebar)
2. Click **"Connect"** on your cluster
3. Choose **"Connect your application"**
4. Copy the connection string
5. Replace `<password>` with your actual password
6. Add `/safepay` before the `?` to specify database name

**Example:**
```
mongodb+srv://myusername:mypassword123@cluster0.abc123.mongodb.net/safepay?retryWrites=true&w=majority
```

#### 3. Special Characters in Password?

If your password has special characters like `@`, `:`, `/`, `?`, `#`, you need to URL-encode them:

| Character | Encoded |
|-----------|---------|
| @         | %40     |
| :         | %3A     |
| /         | %2F     |
| ?         | %3F     |
| #         | %23     |
| %         | %25     |

**Example:**
- Password: `my@pass:word`
- Encoded: `my%40pass%3Aword`
- Connection string: `mongodb+srv://user:my%40pass%3Aword@cluster.mongodb.net/safepay`

**OR** just create a new user with a simple password!

#### 4. Test Your Connection

```bash
export MONGODB_URI="your-connection-string-here"
python3 test_connection.py
```

---

## ❌ Error: "IP not whitelisted" or "Connection timeout"

### What it means:
Your IP address is not allowed to connect to MongoDB Atlas.

### Solution:

1. Go to MongoDB Atlas
2. Click **"Network Access"** (left sidebar)
3. Click **"Add IP Address"**
4. Click **"Allow Access from Anywhere"**
   - This adds `0.0.0.0/0`
5. Click **"Confirm"**
6. **Wait 2-3 minutes** for changes to take effect

---

## ❌ Error: "MONGODB_URI environment variable is not set"

### What it means:
You didn't set the connection string in your terminal.

### Solution:

```bash
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/safepay?retryWrites=true&w=majority"
```

**Make it permanent** (add to ~/.zshrc):
```bash
echo 'export MONGODB_URI="your-connection-string"' >> ~/.zshrc
source ~/.zshrc
```

---

## 🔄 Step-by-Step: Start Fresh

If you're stuck, follow these steps exactly:

### 1. Create New Database User (Simple Password)

In MongoDB Atlas:
1. **Database Access** → **Add New Database User**
2. Username: `safepay_admin`
3. Password: `safepay123` (simple, no special chars)
4. Database User Privileges: **Read and write to any database**
5. Click **Add User**

### 2. Whitelist All IPs

1. **Network Access** → **Add IP Address**
2. **Allow Access from Anywhere** (0.0.0.0/0)
3. Click **Confirm**
4. Wait 2-3 minutes

### 3. Get Connection String

1. **Database** → **Connect** (on your cluster)
2. **Connect your application**
3. Copy the string, it looks like:
   ```
   mongodb+srv://safepay_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### 4. Build Your Final Connection String

Replace `<password>` with `safepay123` and add `/safepay`:

```
mongodb+srv://safepay_admin:safepay123@cluster0.xxxxx.mongodb.net/safepay?retryWrites=true&w=majority
```

**Important:** Replace `cluster0.xxxxx.mongodb.net` with YOUR actual cluster hostname!

### 5. Test It

```bash
cd /Users/jawaharlal/Safepay2

# Set the connection string
export MONGODB_URI="mongodb+srv://safepay_admin:safepay123@cluster0.xxxxx.mongodb.net/safepay?retryWrites=true&w=majority"

# Test connection
python3 test_connection.py
```

If you see ✅ **ALL TESTS PASSED**, continue:

```bash
# Initialize database
python3 db.py

# Run app
python3 app.py
```

---

## 📋 Checklist

Before running your app, verify:

- [ ] MongoDB Atlas cluster is created and active (green status)
- [ ] Database user is created with username and password
- [ ] IP whitelist includes `0.0.0.0/0`
- [ ] Connection string has actual password (not `<password>`)
- [ ] Connection string includes `/safepay` before the `?`
- [ ] MONGODB_URI environment variable is set
- [ ] `python3 test_connection.py` passes

---

## 🆘 Still Having Issues?

### Check Cluster Status

1. Go to MongoDB Atlas
2. Click **"Database"**
3. Make sure your cluster shows **green status** (not paused or creating)

### View Logs

In MongoDB Atlas:
1. Click on your cluster
2. Go to **"Metrics"** or **"Logs"**
3. Look for authentication failures or connection attempts

### Create New Cluster

If all else fails:
1. Delete the old cluster
2. Create a new M0 FREE cluster
3. Follow the setup steps again from scratch

---

## 💡 Pro Tips

1. **Use simple passwords** during development (letters + numbers only)
2. **Wait 2-3 minutes** after making changes in Atlas
3. **Test connection** before running the app
4. **Save your connection string** somewhere safe
5. **Don't commit** connection strings to Git

---

## 🔗 Useful Links

- [MongoDB Atlas Login](https://cloud.mongodb.com/)
- [Connection String Format](https://www.mongodb.com/docs/manual/reference/connection-string/)
- [URL Encoding Reference](https://www.w3schools.com/tags/ref_urlencode.asp)
