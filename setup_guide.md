# 🧁 Cream & Co. — Full Setup Guide

The app is running but currently using **SQLite** with no email or real auth. Here's everything needed to make it **production-ready**, step by step.

---

## Overview — What Needs Setup

| # | What | Why | Required? |
|---|------|-----|-----------|
| 1 | **Supabase Database** | Store users, products, orders persistently | ✅ Yes |
| 2 | **Database Migration** | Create tables in Supabase | ✅ Yes |
| 3 | **JWT Secret** | Secure authentication tokens | ✅ Yes |
| 4 | **Email (SMTP)** | Verification emails, password reset, order confirmations | ⚠️ Optional for testing |
| 5 | **Admin User** | Access the admin dashboard | ✅ Yes |

> [!NOTE]
> You can test locally with just **SQLite** (current setup) — products auto-seed, auth works, but emails won't send. Steps 1-2 are needed for real data persistence.

---

## Step 1: Supabase Database Setup

### 1.1 Create a Supabase Project
1. Go to [supabase.com](https://supabase.com) → **Sign in** (or create account)
2. Click **"New project"**
3. Fill in:
   - **Name**: `cream-and-co`
   - **Database Password**: Generate a strong password → **save this!**
   - **Region**: Choose closest to Dewas (e.g., `Mumbai` or `Singapore`)
4. Click **"Create new project"** (takes ~2 minutes)

### 1.2 Get Your Connection String
1. In your Supabase dashboard → **Settings** (gear icon) → **Database**
2. Scroll to **"Connection string"** → Click **URI** tab
3. Copy the connection string, it looks like:
   ```
   postgresql://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
   ```
4. **Replace `[YOUR-PASSWORD]`** with the password you set in step 1.1

### 1.3 Update `.env` File
Open [.env](file:///e:/TanishqCode/CreamAndCo/.env) and update:

```diff
- DATABASE_URL=sqlite:///reflex.db
+ DATABASE_URL=postgresql://postgres.[your-ref]:[your-password]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

> [!IMPORTANT]
> Make sure the password has no special URL characters unescaped. If your password has `@`, `#`, etc., URL-encode them.

---

## Step 2: Database Migration

After updating `DATABASE_URL`, run these commands to create all tables:

```powershell
# Stop the running app first (Ctrl+C in the terminal)

# Initialize/migrate the database
reflex db migrate

# Start the app again
reflex run
```

The first time you visit `/menu`, the app auto-seeds **27 products** and **4 categories** from the Cream & Co. catalog.

> [!TIP]
> If migration fails, try `reflex db makemigrations` first, then `reflex db migrate`.

---

## Step 3: JWT Secret (Authentication Security)

The current dev secret works for testing. For production, generate a real secret:

### Generate a Secure Secret
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### Update `.env`
```diff
- JWT_SECRET=cream-and-co-dev-secret-key-change-in-production-2024
+ JWT_SECRET=<paste-your-64-char-hex-string-here>
```

> [!WARNING]
> Changing the JWT secret will invalidate all existing login sessions. Do this before real users sign up.

---

## Step 4: Email Setup (SMTP)

This enables: email verification, password reset, and order confirmation emails.

### Option A: Gmail App Password (Easiest)
1. Go to [myaccount.google.com](https://myaccount.google.com) → **Security**
2. Enable **2-Step Verification** (if not already)
3. Go to **Security** → **2-Step Verification** → scroll down → **App passwords**
4. Create app password:
   - **App**: Select "Mail"
   - **Device**: Select "Windows Computer"
5. Copy the 16-character password Google gives you

### Update `.env`
```diff
- SMTP_USER=creamandco@gmail.com
+ SMTP_USER=your-actual-gmail@gmail.com
- SMTP_PASSWORD=app-specific-password
+ SMTP_PASSWORD=xxxx xxxx xxxx xxxx
```

### Option B: Skip Email (Dev Mode)
If you don't setup SMTP, the app will:
- Print verification links to the **terminal console** instead of emailing
- Users can still register, but verification emails won't send
- No order confirmation emails

This is fine for testing!

---

## Step 5: Create Admin User

After the database is set up and app is running:

### 5.1 Register Normally
1. Go to `http://localhost:3000/register`
2. Create an account with your email
3. If email isn't configured, check the **terminal** for the verification link

### 5.2 Promote to Admin
Run this in PowerShell (while the app is running):

```powershell
python -c "
import os
os.environ['DATABASE_URL'] = 'sqlite:///reflex.db'  # or your Supabase URL
from sqlmodel import create_engine, Session, select
from CreamAndCo.models.user import User

engine = create_engine(os.environ['DATABASE_URL'])
with Session(engine) as session:
    user = session.exec(select(User).where(User.email == 'YOUR_EMAIL_HERE')).first()
    if user:
        user.is_admin = True
        user.is_verified = True
        session.add(user)
        session.commit()
        print(f'✅ {user.full_name} is now an admin!')
    else:
        print('❌ User not found')
"
```

Replace `YOUR_EMAIL_HERE` with the email you registered with.

### 5.3 Access Admin Panel
Go to `http://localhost:3000/admin` — you'll see:
- **Dashboard** with stats
- **Product management** (edit prices, add/remove items)  
- **Order management** (update statuses)
- **User management** (promote/demote admins)

---

## Final `.env` Checklist

Here's what your completed `.env` should look like:

```env
# ✅ Database — Supabase PostgreSQL
DATABASE_URL=postgresql://postgres.xxxxx:YourPassword@aws-0-ap-south-1.pooler.supabase.com:6543/postgres

# ✅ Auth — Secure JWT
JWT_SECRET=<your-64-char-hex-secret>
JWT_ALGORITHM=HS256
JWT_EXPIRY_DAYS=7

# ✅ Email — Gmail SMTP  
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_NAME=Cream & Co.

# ✅ App Config
APP_BASE_URL=http://localhost:3000
APP_ENV=development
```

---

## Quick Start Order

> [!TIP]
> **Minimum viable setup** (just to see products & test login):
> 1. Leave `DATABASE_URL` as SQLite ✅ (already done)
> 2. Skip email setup ✅ 
> 3. Run `reflex db migrate` → `reflex run`
> 4. Visit `/menu` — products auto-seed
> 5. Register → check terminal for verification link → login
>
> **Full production setup**: Do all 5 steps above.

---

## What Each Step Unlocks

```mermaid
graph LR
    A[SQLite Default] -->|Step 1-2| B[Supabase DB]
    A -->|Already works| C[Products Auto-seed]
    A -->|Already works| D[Auth Login/Register]
    B --> E[Persistent Data]
    B --> F[Multiple Users]
    G[Step 3: JWT] --> H[Secure Sessions]
    I[Step 4: SMTP] --> J[Email Verification]
    I --> K[Password Reset]
    I --> L[Order Confirmations]
    M[Step 5: Admin] --> N[Admin Dashboard]
    M --> O[Manage Products]
    M --> P[Manage Orders]
```

**Tell me which step you want to do first and I'll walk you through it!**
