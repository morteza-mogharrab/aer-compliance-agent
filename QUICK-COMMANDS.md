# Quick Commands Reference

## 🚀 Setup & Installation

```bash
# Clone and setup
git clone https://github.com/morteza-mogharrab/aer-compliance-agent.git
cd aer-compliance-agent
python3 -m venv venv
source venv/bin/activate

# Set API key
export OPENAI_API_KEY='your-key-here'

# Run setup
chmod +x setup_agent.sh
./setup_agent.sh
```

## 🎮 Running the Agent

```bash
# Web interface (recommended)
python3 agent_app.py

# Command line
python3 agent_core.py

# Interactive CLI
python3 agent_core.py
# Then type commands like: "List all facilities"

# Single command
python3 agent_core.py "Audit facility FAC-AB-001"

# Demo scenarios
python3 demo_scenarios.py
```

## 🧪 Testing

```bash
# Run all tests
python3 test_agent.py

# Test specific component
python3 -c "from mock_db import mock_api_get_facilities; print(mock_api_get_facilities())"

# Rebuild RAG index
python3 industrial_rag_system.py
```

## 📝 Common Tasks

### Check What the Agent Sees
```bash
python3 -c "from agent_tools import audit_tools; print(f'{len(audit_tools)} tools'); [print(f'- {t.name}') for t in audit_tools]"
```

### View Mock Data
```bash
python3 -c "from mock_db import MOCK_FACILITIES; import json; print(json.dumps(MOCK_FACILITIES, indent=2))"
```

### Clear Mock Data
```bash
python3 -c "from mock_db import reset_mock_data; reset_mock_data(); print('Reset complete')"
```

## 🔧 Debugging

### Enable Verbose Mode
In `agent_core.py`, line ~55:
```python
self.agent_executor = AgentExecutor(
    agent=self.agent,
    tools=audit_tools,
    verbose=True,  # ← Make sure this is True
    max_iterations=15
)
```

### Check API Key
```bash
echo $OPENAI_API_KEY
# Should show: sk-proj-...
```

### Verify Dependencies
```bash
pip list | grep -E "langchain|openai|chromadb|gradio"
```

## 📊 Useful Python Snippets

### Test Single Tool
```python
from agent_tools import list_facilities
result = list_facilities.invoke({})
print(result)
```

### Query RAG Directly
```python
from industrial_rag_system import IndustrialRAGSystem
import os

rag = IndustrialRAGSystem(api_key=os.getenv("OPENAI_API_KEY"))
rag.load_index()
result = rag.generate_response("What are calibration requirements?")
print(result['answer'])
```

### Send Mock Email
```python
from mock_db import mock_api_send_email
result = mock_api_send_email(
    to="test@example.com",
    subject="Test",
    body="Test email"
)
print(result)
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
lsof -ti:7860 | xargs kill -9
```

### Module Not Found
```bash
pip install -r requirements_agent.txt --force-reinstall
```

### ChromaDB Issues
```bash
rm -rf chroma_db/
python3 industrial_rag_system.py
```

## 📦 Git Commands

### Initial Setup
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/aer-compliance-agent.git
git push -u origin main
```

### Updates
```bash
git add .
git commit -m "Update: Description of changes"
git push
```

### Check Status
```bash
git status
git log --oneline
```

## 🎯 Example Agent Commands

Try these in the web interface or CLI:

```
"List all facilities"

"Audit facility FAC-AB-001"

"What are the calibration requirements in Directive 017?"

"Check compliance for all facilities and send summary to ops@petolab.com"

"For each non-compliant item at FAC-AB-001, log maintenance and schedule calibration"
```

## 📚 View Documentation

```bash
# View README
cat README.md | less

# View all available tools
python3 -c "from agent_tools import audit_tools; [print(f'{t.name}: {t.description}') for t in audit_tools]"

# View mock facilities
python3 -c "from mock_db import mock_api_get_facilities; import json; print(json.dumps(mock_api_get_facilities(), indent=2))"
```

## 🔄 Reset Everything

```bash
# Remove all generated files
rm -rf venv/ __pycache__/ chroma_db/ *.pyc

# Start fresh
python3 -m venv venv
source venv/bin/activate
./setup_agent.sh
```

## 💾 Backup

```bash
# Create backup
tar -czf aer-agent-backup-$(date +%Y%m%d).tar.gz \
  --exclude='venv' \
  --exclude='__pycache__' \
  --exclude='chroma_db' \
  .

# Restore backup
tar -xzf aer-agent-backup-YYYYMMDD.tar.gz
```