# SafePay - Secure Payment System

A Flask-based secure payment system with fraud detection, encryption, and digital signatures.

## Production Deployment

### Deploying to Render

1. Fork this repository to your GitHub account at https://github.com/Saksham-Gupta-GH

2. Create a new Web Service on Render:
   - Go to https://dashboard.render.com
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Choose a name for your service
   - Set the following:
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Add the following environment variables:
     - `MONGODB_URI`: Your MongoDB Atlas connection string
     - `SECRET_KEY`: A secure random string for Flask sessions

3. Click "Create Web Service"

The application will be automatically deployed. Any future pushes to the main branch will trigger automatic deployments.

### Deploying to Railway (GitHub → Railway) — recommended

Railway integrates directly with GitHub and can build your repository (including using the `Dockerfile`) and deploy automatically on pushes to `main`.

Steps:

1. Sign in to https://railway.app using your GitHub account.
2. Click "New Project" → "Deploy from GitHub" and select the `safepay` repository and `main` branch.
3. Railway should detect the `Dockerfile` in the repository. If prompted, choose the Dockerfile build option.
4. In the Railway project settings, add the required environment variables:
  - `MONGODB_URI` — Your MongoDB Atlas connection string
  - `SECRET_KEY` — A long random string (generate locally with `python3 -c "import secrets; print(secrets.token_urlsafe(48))"`)
5. Click "Deploy". Railway will build and run the app and provide a public URL.

Notes:
- If your repository contains large files (CSV datasets > 50MB), Railway can still build the repo but build times may be slower. Consider using Git LFS or hosting large artifacts externally.
- Railway will automatically redeploy on pushes to `main` if the repo is linked.

## Prerequisites

- Python 3.8 or higher
- MongoDB Atlas (cloud) OR MongoDB (local installation)

## Installation & Setup

### 1. Choose Your Database Option

#### Option A: MongoDB Atlas (Cloud - Recommended) ☁️

**No local installation required!** Follow the detailed guide:
📖 **[MONGODB_ATLAS_SETUP.md](MONGODB_ATLAS_SETUP.md)** - Complete step-by-step instructions

Quick summary:
1. Create free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Create a free M0 cluster
3. Get your connection string
4. Set environment variable and run

#### Option B: Local MongoDB Installation

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

**Windows:**
Download and install from [MongoDB Download Center](https://www.mongodb.com/try/download/community)

### 2. Install Python Dependencies

```bash
cd /Users/jawaharlal/Safepay2
pip install -r requirements.txt
```

Or install with pip3:
```bash
pip3 install -r requirements.txt
```

### 3. Set Up MongoDB Connection (Optional)

By default, the app connects to `mongodb://localhost:27017/safepay`.

To use a different MongoDB instance, set the environment variable:
```bash
export MONGODB_URI="mongodb://your-mongodb-uri/safepay"
```

## Running the Application

### Quick Start (MongoDB Atlas)

**Using the helper script (easiest):**
```bash
cd /Users/jawaharlal/Safepay2

# Set your MongoDB Atlas connection string
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/safepay?retryWrites=true&w=majority"

# Run the helper script (initializes DB and starts app)
./run.sh
```

**Manual method:**
```bash
cd /Users/jawaharlal/Safepay2

# Set your connection string
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/safepay?retryWrites=true&w=majority"

# Initialize database
python3 db.py

# Run the app
python3 app.py
```

### Quick Start (Local MongoDB)

```bash
cd /Users/jawaharlal/Safepay2
python3 db.py  # Initialize database
python3 app.py  # Run the app
```

The application will start on **http://127.0.0.1:5000**

### Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Default Accounts

After running `python3 db.py`, these accounts are created:

### Admin Account
- **Username:** admin
- **Password:** admin
- **Role:** admin
- **Balance:** ₹50,000

### Test User Accounts
- **Username:** user1
- **Password:** 1234
- **Role:** user
- **Balance:** ₹50,000

- **Username:** saksham
- **Password:** hello123
- **Role:** user
- **Balance:** ₹50,000

*Note: You can create new user accounts via the signup page*

## Project Structure

```
Safepay2/
├── app.py                  # Main Flask application
├── db.py                   # Database utilities
├── encryption.py           # Data encryption functions
├── hashing.py             # Password hashing utilities
├── digital_signature.py   # Digital signature functions
├── model_predict.py       # Fraud detection model
├── model_train_augmented.py # Enhanced model training script with additional features
├── requirements.txt       # Python dependencies
├── fraud_model.pkl        # Pre-trained fraud detection model
├── database.db            # SQLite database (if used)
├── aes_key.bin           # Encryption key
├── templates/            # HTML templates
└── static/              # CSS, JS, images

```

## Features

- **User Authentication:** Secure login/signup with password hashing
- **Role-Based Access:** Admin and user roles with different dashboards
- **Secure Transactions:** Encrypted transaction data with digital signatures
- **Fraud Detection:** ML-based fraud detection for transactions
- **Balance Management:** Real-time balance updates with concurrency control
- **Transaction History:** View all past transactions

## Troubleshooting

### MongoDB Connection Error
```
Error: Connection refused to MongoDB
```
**Solution:** Make sure MongoDB is running:
```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongodb
```

### Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution:** Kill the process using port 5000 or run on a different port:
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or run on different port
flask run --port 5001
```

## Development Mode

The app runs in debug mode by default (see `app.py` line 190). For production:

1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Security Notes

- Change the `app.secret_key` in production (currently set to "safepay_secret")
- Store sensitive keys in environment variables
- Use HTTPS in production
- Regularly update dependencies for security patches

## Additional Documentation

- **`MONGODB_ATLAS_SETUP.md`** - Complete MongoDB Atlas cloud setup guide
- `DESIGN_SYSTEM.md` - UI/UX design guidelines
- `TESTING_GUIDE.md` - Testing procedures
- `CHANGES_SUMMARY.md` - Recent changes and updates
- `VISUAL_SHOWCASE.md` - Visual documentation
