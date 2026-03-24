#!/bin/bash

echo "🚀 Databricks Hackathon 2026 - GitHub Deployment Script"
echo "========================================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

echo "✅ Git found"
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the Databricks-Hack26 directory"
    exit 1
fi

echo "📁 Current directory: $(pwd)"
echo ""

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    git branch -M main
    echo "✅ Git initialized"
else
    echo "✅ Git repository already exists"
fi
echo ""

# Configure git
echo "🔧 Configuring Git..."
git config user.name "nikethanp17"
git config user.email "nikethanp17@gmail.com"
echo "✅ Git configured"
echo ""

# Add all files
echo "📦 Adding files to Git..."
git add .
echo "✅ Files added"
echo ""

# Create commit
echo "💾 Creating commit..."
git commit -m "Initial commit: Hyper-Local Supply Chain Optimizer for Kirana Stores

Features:
- ML model with 89.7% accuracy (Random Forest)
- Delta Lake integration for data storage
- FastAPI backend with /predict endpoint  
- Modern web frontend (login, landing, dashboard)
- Full documentation and setup instructions
- Production-ready code structure

Built for Databricks Hackathon 2026" || echo "No changes to commit or commit already exists"
echo ""

# Add remote (remove existing if present)
echo "🔗 Setting up remote repository..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/nikethanp17/Databricks-Hack26.git
echo "✅ Remote added"
echo ""

# Push to GitHub
echo "🚀 Pushing to GitHub..."
echo ""
echo "⚠️  You may be prompted for your GitHub credentials."
echo "    If you have 2FA enabled, use a Personal Access Token instead of your password."
echo ""
git push -u origin main --force

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "🎉 SUCCESS! Your project is now on GitHub!"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "📍 Repository URL:"
    echo "   https://github.com/nikethanp17/Databricks-Hack26"
    echo ""
    echo "🌐 Next Steps:"
    echo "   1. Visit your repository on GitHub"
    echo "   2. Enable GitHub Pages (Settings → Pages → Source: main branch)"
    echo "   3. Your frontend will be live at:"
    echo "      https://nikethanp17.github.io/Databricks-Hack26/frontend/login.html"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
else
    echo ""
    echo "❌ Push failed. Please check your credentials and try again."
    echo ""
    echo "💡 Tips:"
    echo "   - Make sure you have access to the repository"
    echo "   - Use a Personal Access Token if you have 2FA enabled"
    echo "   - Check your internet connection"
fi
