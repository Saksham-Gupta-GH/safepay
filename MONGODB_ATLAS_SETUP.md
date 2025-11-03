# MongoDB Atlas Cloud Setup Guide

Follow these steps to set up MongoDB Atlas (free cloud database) for SafePay.

## Step 1: Create MongoDB Atlas Account

1. Go to [https://www.mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register)
2. Sign up with your email or Google account
3. Complete the registration

## Step 2: Create a Free Cluster

1. After logging in, click **"Create"** or **"Build a Database"**
2. Choose **"M0 FREE"** tier (no credit card required)
3. Select a cloud provider (AWS, Google Cloud, or Azure)
4. Choose a region closest to you (e.g., Mumbai for India)
5. Give your cluster a name (e.g., "SafePayCluster")
6. Click **"Create Cluster"** (takes 3-5 minutes to deploy)

## Step 3: Create Database User

1. On the left sidebar, click **"Database Access"**
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Create a username (e.g., `safepay_user`)
5. Create a strong password (save it somewhere safe!)
6. Under "Database User Privileges", select **"Read and write to any database"**
7. Click **"Add User"**

## Step 4: Configure Network Access

1. On the left sidebar, click **"Network Access"**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (for development)
   - This adds `0.0.0.0/0` to the IP whitelist
   - For production, restrict to specific IPs
4. Click **"Confirm"**

## Step 5: Get Your Connection String

1. Go back to **"Database"** (left sidebar)
2. Click **"Connect"** on your cluster
3. Choose **"Connect your application"**
4. Select **"Python"** and version **"3.12 or later"**
5. Copy the connection string (looks like):
   ```
   mongodb+srv://safepay_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<password>` with your actual database user password
7. Add `/safepay` before the `?` to specify the database name:
   ```
   mongodb+srv://safepay_user:yourpassword@cluster0.xxxxx.mongodb.net/safepay?retryWrites=true&w=majority
   ```

## Step 6: Initialize Your Database

Run the following commands in your terminal:

```bash
cd /Users/jawaharlal/Safepay2

# Replace with your actual connection string
export MONGODB_URI="mongodb+srv://safepay_user:yourpassword@cluster0.xxxxx.mongodb.net/safepay?retryWrites=true&w=majority"

# Initialize database with seed data
python3 db.py
```

You should see: `MongoDB initialized and seeded!`

## Step 7: Run Your Application

```bash
# Set the connection string (same as above)
export MONGODB_URI="mongodb+srv://safepay_user:yourpassword@cluster0.xxxxx.mongodb.net/safepay?retryWrites=true&w=majority"

# Run the app
python3 app.py
```

## Step 8: Access Your Application

Open your browser and go to:
```
http://127.0.0.1:5000
```

## Making It Permanent (Optional)

To avoid typing the connection string every time, add it to your shell profile:

### For zsh (default on macOS):
```bash
echo 'export MONGODB_URI="mongodb+srv://safepay_user:yourpassword@cluster0.xxxxx.mongodb.net/safepay?retryWrites=true&w=majority"' >> ~/.zshrc
source ~/.zshrc
```

### For bash:
```bash
echo 'export MONGODB_URI="mongodb+srv://safepay_user:yourpassword@cluster0.xxxxx.mongodb.net/safepay?retryWrites=true&w=majority"' >> ~/.bash_profile
source ~/.bash_profile
```

After this, you can simply run:
```bash
python3 db.py
python3 app.py
```

## Troubleshooting

### Error: "Authentication failed"
- Double-check your username and password
- Make sure you replaced `<password>` with your actual password
- Password should be URL-encoded if it contains special characters

### Error: "IP not whitelisted"
- Go to Network Access in Atlas
- Make sure `0.0.0.0/0` is added
- Wait a few minutes for changes to propagate

### Error: "Connection timeout"
- Check your internet connection
- Verify the connection string is correct
- Make sure your cluster is active (not paused)

## View Your Data in Atlas

1. Go to your cluster in MongoDB Atlas
2. Click **"Browse Collections"**
3. You'll see your `safepay` database with:
   - `users` collection (with admin, user1, saksham)
   - `transactions` collection (will populate as you use the app)

## Security Best Practices

1. **Never commit your connection string to Git**
   - Add `.env` file to `.gitignore`
   - Use environment variables

2. **For production:**
   - Restrict IP whitelist to specific addresses
   - Use strong, unique passwords
   - Enable additional security features in Atlas

3. **Rotate credentials regularly**

## Free Tier Limits

MongoDB Atlas Free Tier (M0) includes:
- 512 MB storage
- Shared RAM
- Shared vCPU
- No backups (manual export only)

This is sufficient for development and small projects.
