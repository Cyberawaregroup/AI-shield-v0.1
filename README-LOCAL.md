# 🚀 Running Threat Intelligence Platform Locally (No Docker)

This guide shows you how to run the Threat Intelligence Platform directly on your machine without Docker.

## 📋 Prerequisites

### **Required Software**
- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

### **System Requirements**
- **Windows 10/11** or **macOS** or **Linux**
- **4GB RAM** minimum
- **2GB free disk space**

## 🚀 Quick Start

### **Windows Users**
```batch
# Run the local startup script
start-local.bat
```

### **Linux/Mac Users**
```bash
# Make the script executable
chmod +x start-local.sh

# Run the local startup script
./start-local.sh
```

## 🔧 Manual Setup (Alternative)

If you prefer to set things up manually:

### **1. Install Python Dependencies**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

pip install -r requirements-local.txt
cd ..
```

### **2. Install Node.js Dependencies**
```bash
npm install
```

### **3. Create Environment File**
```bash
# Copy the template
cp env.example .env

# Edit .env with your API keys (optional for basic testing)
# OPENAI_API_KEY=your_key_here
# HIBP_API_KEY=your_key_here
# ABUSEIPDB_API_KEY=your_key_here
```

### **4. Start the Backend**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **5. Start the Frontend (New Terminal)**
```bash
npm run dev
```

## 🌐 Access Your Application

- **Frontend**: http://localhost:5173 (or 3000)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
vigilance-voice/
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   ├── requirements-local.txt  # Local dependencies
│   └── venv/               # Python virtual environment
├── src/                    # React frontend
├── start-local.bat         # Windows startup script
├── start-local.sh          # Linux/Mac startup script
└── .env                    # Environment variables
```

## 🔍 Troubleshooting

### **Common Issues**

#### **Port Already in Use**
```bash
# Check what's using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Kill the process or change the port
```

#### **Python Virtual Environment Issues**
```bash
# Remove and recreate virtual environment
rm -rf backend/venv          # Linux/Mac
rmdir /s backend\venv        # Windows

# Then run the startup script again
```

#### **Node.js Dependencies Issues**
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### **Database Issues**
- The app automatically uses SQLite for local development
- Database file: `backend/threat_intel.db`
- Delete this file to reset the database

### **Error Messages**

#### **"Module not found" errors**
- Make sure you're in the virtual environment
- Reinstall requirements: `pip install -r requirements-local.txt`

#### **"Port already in use"**
- Check if another service is running on ports 8000 or 5173
- Stop conflicting services or change ports in the startup scripts

#### **"Permission denied" (Linux/Mac)**
```bash
chmod +x start-local.sh
```

## 🎯 What Works Without Docker

### **✅ Fully Functional**
- FastAPI backend with SQLite database
- React frontend with hot reload
- Basic API endpoints
- Database models and tables
- Static file serving

### **⚠️ Limited Functionality**
- No Redis caching (uses in-memory fallbacks)
- No Celery background tasks
- No PostgreSQL (uses SQLite)
- External API integrations need keys

### **❌ Not Available**
- Multi-container orchestration
- Production-grade database
- Background task processing
- Advanced caching

## 🔄 Switching to Docker Later

When you're ready to use Docker:

1. **Install Docker Desktop**
2. **Run the original startup script**: `start.bat` or `start.sh`
3. **All features will be available** including Redis, PostgreSQL, and Celery

## 📚 Next Steps

1. **Test the basic functionality** - Frontend loads, backend responds
2. **Add API keys** to `.env` for external services
3. **Test threat intelligence features** - Email breach checking, etc.
4. **Develop new features** using the local setup
5. **Deploy with Docker** when ready for production

## 🆘 Getting Help

- **Check the logs** in the terminal windows
- **Verify prerequisites** are installed correctly
- **Check file permissions** (especially on Linux/Mac)
- **Review error messages** for specific issues

---

**Happy local development! 🛡️**
