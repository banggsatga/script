# 🚀 Perintah Curl untuk Install di VPS

## 📥 Option 1: Install dengan Script Installer (Recommended)

### Cara paling mudah - One liner:

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/install_bpjs_login.sh | bash
```

Atau dengan wget:
```bash
wget -qO- https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/install_bpjs_login.sh | bash
```

**Script ini akan:**
- ✅ Check Python & pip
- ✅ Create folder `~/bpjs-login`
- ✅ Download semua file yang diperlukan
- ✅ Install dependencies otomatis
- ✅ Set executable permissions

---

## 📥 Option 2: Manual Download File-by-File

### 1. Create Directory
```bash
mkdir -p ~/bpjs-login
cd ~/bpjs-login
```

### 2. Download requirements.txt
```bash
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/requirements.txt
```

Atau buat manual:
```bash
cat > requirements.txt << 'EOF'
requests>=2.31.0
pyjwt>=2.10.1
EOF
```

### 3. Download bpjs_login.py (Advanced)
```bash
curl -o bpjs_login.py https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/bpjs_login.py
chmod +x bpjs_login.py
```

### 4. Download simple_login.py
```bash
curl -o simple_login.py https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/simple_login.py
chmod +x simple_login.py
```

### 5. Install Dependencies
```bash
pip3 install -r requirements.txt --user
```

---

## 📥 Option 3: Create Files Directly (Tanpa GitHub)

### Step 1: Create requirements.txt
```bash
mkdir -p ~/bpjs-login
cd ~/bpjs-login

cat > requirements.txt << 'EOF'
requests>=2.31.0
pyjwt>=2.10.1
EOF
```

### Step 2: Install Dependencies
```bash
pip3 install -r requirements.txt --user
```

### Step 3: Create bpjs_login.py
```bash
curl https://pastebin.com/raw/YOUR_PASTE_ID -o bpjs_login.py
chmod +x bpjs_login.py
```

Atau buat dengan heredoc:
```bash
cat > bpjs_login.py << 'EOFPYTHON'
#!/usr/bin/env python3
# [paste full content here]
EOFPYTHON

chmod +x bpjs_login.py
```

---

## 🎯 Quick Install (Copy-Paste Friendly)

### All-in-One Command:

```bash
# Create directory
mkdir -p ~/bpjs-login && cd ~/bpjs-login

# Create requirements.txt
cat > requirements.txt << 'EOF'
requests>=2.31.0
pyjwt>=2.10.1
EOF

# Install dependencies
pip3 install -r requirements.txt --user

# Download script (ganti URL dengan lokasi file Anda)
curl -o bpjs_login.py https://your-server.com/bpjs_login.py
chmod +x bpjs_login.py

# Test
python3 bpjs_login.py
```

---

## 📦 Alternative: Download from Pastebin/Gist

### Upload ke Pastebin:
1. Copy isi `bpjs_login.py`
2. Upload ke https://pastebin.com
3. Get raw URL

### Download dari Pastebin:
```bash
cd ~/bpjs-login
curl https://pastebin.com/raw/PASTE_ID -o bpjs_login.py
chmod +x bpjs_login.py
```

### Upload ke GitHub Gist:
1. Go to https://gist.github.com
2. Create new gist dengan file `bpjs_login.py`
3. Get raw URL

### Download dari Gist:
```bash
curl https://gist.githubusercontent.com/USERNAME/GIST_ID/raw/bpjs_login.py -o bpjs_login.py
chmod +x bpjs_login.py
```

---

## 🔧 Setup VPS dari Scratch

### Complete Setup Command:

```bash
# Update system
sudo apt update

# Install Python & pip (jika belum ada)
sudo apt install -y python3 python3-pip

# Create directory
mkdir -p ~/bpjs-login && cd ~/bpjs-login

# Create requirements.txt
cat > requirements.txt << 'EOF'
requests>=2.31.0
pyjwt>=2.10.1
EOF

# Install dependencies
pip3 install -r requirements.txt --user

# Add pip to PATH (jika belum)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Download atau create script
# (pilih salah satu method di atas)

# Test installation
python3 --version
pip3 --version
python3 -c "import requests; print('✓ requests OK')"
```

---

## 📁 File Structure Setelah Install:

```
~/bpjs-login/
├── requirements.txt          # Dependencies
├── bpjs_login.py            # Advanced script
├── simple_login.py          # Simple script (optional)
├── README.md                # Documentation (optional)
├── .bpjs_device_id          # Auto-generated
└── .bpjs_tokens.json        # Auto-generated setelah login
```

---

## ✅ Verify Installation:

```bash
cd ~/bpjs-login

# Check Python
python3 --version

# Check pip
pip3 --version

# Check requests library
python3 -c "import requests; print('✓ requests installed')"

# Check script
python3 -c "from bpjs_login import BPJSLoginClient; print('✓ script OK')"

# Run script
python3 bpjs_login.py
```

---

## 🚀 Quick Test:

```bash
cd ~/bpjs-login
python3 bpjs_login.py
```

Atau direct:
```bash
python3 ~/bpjs-login/bpjs_login.py
```

---

## 🌐 Host Files on Your Own Server

### Option A: Using Python HTTP Server

Di komputer lokal Anda:
```bash
cd /app/backend
python3 -m http.server 8000
```

Di VPS:
```bash
curl http://YOUR_IP:8000/bpjs_login.py -o bpjs_login.py
curl http://YOUR_IP:8000/requirements.txt -o requirements.txt
```

### Option B: Using SCP

```bash
# From local machine to VPS
scp /app/backend/bpjs_login.py user@your-vps:/home/user/bpjs-login/
scp /app/backend/requirements.txt user@your-vps:/home/user/bpjs-login/
```

### Option C: Using rsync

```bash
# Sync entire directory
rsync -avz /app/backend/*.py user@your-vps:~/bpjs-login/
```

---

## 🔐 Secure Transfer dengan Password Protection

### Create encrypted archive:
```bash
# On local
cd /app/backend
tar czf - bpjs_login.py requirements.txt | openssl enc -aes-256-cbc -out bpjs.tar.gz.enc

# Upload to server
scp bpjs.tar.gz.enc user@vps:~/

# On VPS
openssl enc -d -aes-256-cbc -in bpjs.tar.gz.enc | tar xzf -
```

---

## 💡 Tips:

1. **Pakai screen/tmux** untuk running script:
   ```bash
   screen -S bpjs
   python3 bpjs_login.py
   # Ctrl+A, D untuk detach
   ```

2. **Create alias** untuk mudah:
   ```bash
   echo 'alias bpjs="python3 ~/bpjs-login/bpjs_login.py"' >> ~/.bashrc
   source ~/.bashrc
   
   # Now just run:
   bpjs
   ```

3. **Auto-run on boot** (systemd):
   ```bash
   sudo nano /etc/systemd/system/bpjs-login.service
   ```

---

## 🎬 Complete Example - Fresh VPS to Running:

```bash
# SSH ke VPS
ssh user@your-vps-ip

# Update & Install Python
sudo apt update && sudo apt install -y python3 python3-pip

# Create directory
mkdir -p ~/bpjs-login && cd ~/bpjs-login

# Create requirements
cat > requirements.txt << 'EOF'
requests>=2.31.0
pyjwt>=2.10.1
EOF

# Install
pip3 install -r requirements.txt --user

# Download script (ganti dengan URL Anda)
curl -o bpjs_login.py https://your-url/bpjs_login.py
chmod +x bpjs_login.py

# Run
python3 bpjs_login.py
```

**Done!** 🎉
