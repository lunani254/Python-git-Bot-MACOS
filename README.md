# Vikings Git Auto-Pusher 🪓

   ᚢᛁᚴᛁᚾᚴᛋ  (Runes for "Vikings")
   Wielding the Axe of Automation! 🪓

---

## 🔥 Features

- **Automatic Git Operations**  
  Detects changes, commits, and pushes with Viking precision
- **Secure macOS Integration**  
  🔐 Keychain credential storage • 💬 Native notifications
- **Flexible Monitoring Modes**  
  ⚔️ Single-run raids • 🛡️ Continuous watch mode
- **Intelligent Configuration**  
  📝 Recent repo tracking • 🛠️ Error resilience

---

## ⚡ Why Vikings Git Auto-Pusher?

> "Forgetting to push code is like leaving your axe before battle!"

- **Never lose work** - Automatic protection against unpushed commits
- **Mac-native experience** - Keychain security and Notification Center alerts
- **Focus on creation** - Let the tool handle Git chores while you code
- **Viking reliability** - Battle-tested error handling for common Git issues

---

## 🛠 Requirements

| Component       | Requirement                          |
|-----------------|--------------------------------------|
| **macOS**       | 10.8+ (Ventura+ recommended)         |
| **Python**      | 3.8+ (Tested with 3.13)              |
| **Git**         | 2.30+ (`brew install git`)           |
| **Credentials** | GitHub PAT with `repo` scope         |

---

## 🚀 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/lunani254/git-auto-pusher.git
cd git-auto-pusher

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install GitPython pyobjc keyring

# Configure credentials (stored in Keychain)
python main.py --setup-credentials
