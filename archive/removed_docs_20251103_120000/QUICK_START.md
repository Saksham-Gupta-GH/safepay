# SafePay Quick Start Guide

## 🚀 First Time Setup (MongoDB Atlas Cloud)

### Step 1: Get MongoDB Atlas Connection String

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create free account → Create M0 FREE cluster
3. Create database user (username + password)
4. Add IP: 0.0.0.0/0 (allow from anywhere)
5. Get connection string (looks like):
   ```
   mongodb+srv://username:password@cluster.mongodb.net/safepay?retryWrites=true&w=majority
   ```

**📖 Detailed instructions:** See `MONGODB_ATLAS_SETUP.md`

### Step 2: Install Python Dependencies

```bash
cd /Users/jawaharlal/Safepay2
pip3 install -r requirements.txt
```

### Step 3: Set Connection String & Initialize Database

```bash
# Replace with YOUR actual connection string
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/safepay?retryWrites=true&w=majority"

# Initialize database with seed data
python3 db.py
```

You should see: ✅ `MongoDB initialized and seeded!`

### Step 4: Run the Application

```bash
python3 app.py
```

### Step 5: Open in Browser

Go to: **http://127.0.0.1:5000**

---

## 🔄 Running Every Time After Setup

### Option 1: Using Helper Script (Easiest)

```bash
cd /Users/jawaharlal/Safepay2
export MONGODB_URI="your-connection-string"
./run.sh
```

### Option 2: Manual

```bash
cd /Users/jawaharlal/Safepay2
export MONGODB_URI="your-connection-string"
python3 app.py
```

### Option 3: Make It Permanent

Add to your `~/.zshrc` file (so you don't need to export every time):

```bash
echo 'export MONGODB_URI="your-connection-string"' >> ~/.zshrc
source ~/.zshrc
```

Then just run:
```bash
cd /Users/jawaharlal/Safepay2
python3 app.py
```

---

## 👤 Login Credentials

### Admin
- Username: `admin`
- Password: `admin`

### Users
- Username: `user1` | Password: `1234`
- Username: `saksham` | Password: `hello123`

---

## ⚡ Common Commands

```bash
# Initialize/reset database
python3 db.py

# Run application
python3 app.py

# Check if MongoDB URI is set
echo $MONGODB_URI

# Set MongoDB URI (temporary)
export MONGODB_URI="your-connection-string"
```

---

## 🐛 Troubleshooting

### "Connection refused" or "ServerSelectionTimeoutError"
- Check your internet connection
- Verify MongoDB URI is correct
- Make sure you set the environment variable: `export MONGODB_URI="..."`

### "Authentication failed"
- Double-check username and password in connection string
- Make sure you replaced `<password>` with actual password

### "IP not whitelisted"
- Go to MongoDB Atlas → Network Access
- Add `0.0.0.0/0` to IP whitelist
- Wait 2-3 minutes for changes to apply

### Port 5000 already in use
```bash
lsof -ti:5000 | xargs kill -9
```

---

## 📚 More Help

- **MongoDB Atlas Setup:** `MONGODB_ATLAS_SETUP.md`
- **Full Documentation:** `README.md`
- **Testing Guide:** `TESTING_GUIDE.md`
