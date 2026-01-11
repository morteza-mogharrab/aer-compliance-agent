#!/bin/bash

set -e  # Exit on error

echo "============================================================"
echo "AER Compliance Agent - Setup Script"
echo "Upgrading RAG to Autonomous Agent System"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo ""
    echo "Please activate your virtual environment first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    exit 1
fi

# Check for API key
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo -e "${YELLOW}⚠️  OPENAI_API_KEY not set${NC}"
    echo ""
    echo "Please set your OpenAI API key:"
    echo "  export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "Or create a .env file with:"
    echo "  OPENAI_API_KEY=your-api-key-here"
    exit 1
fi

echo -e "${GREEN}✓${NC} Virtual environment: activated"
echo -e "${GREEN}✓${NC} API key: configured"
echo ""

# Step 1: Install agent dependencies
echo "Step 1: Installing Agent Dependencies..."
pip install -r requirements_agent.txt -q
echo -e "${GREEN}✓${NC} Agent dependencies installed"
echo ""

# Step 2: Verify RAG system (should already be set up)
echo "Step 2: Verifying RAG System..."
if [ -d "./chroma_db" ]; then
    echo -e "${GREEN}✓${NC} ChromaDB vector database found"
else
    echo -e "${YELLOW}⚠️  ChromaDB not found. Running RAG setup...${NC}"
    
    # Download PDFs if needed
    if [ ! -f "directive_001.pdf" ]; then
        echo "  Downloading Directive 001..."
        curl -# -o directive_001.pdf "https://static.aer.ca/prd/documents/directives/Directive001.pdf"
    fi
    
    if [ ! -f "directive_017.pdf" ]; then
        echo "  Downloading Directive 017..."
        curl -# -o directive_017.pdf "https://static.aer.ca/prd/documents/directives/Directive017.pdf"
    fi
    
    # Build index
    python3 industrial_rag_system.py
    echo -e "${GREEN}✓${NC} RAG system initialized"
fi
echo ""

# Step 3: Test agent system
echo "Step 3: Testing Agent System..."
python3 -c "
import os
from agent_core import AERComplianceAgent
from mock_db import mock_api_get_facilities

# Test agent initialization
try:
    agent = AERComplianceAgent(verbose=False)
    print('✓ Agent initialized successfully')
except Exception as e:
    print(f'✗ Agent initialization failed: {e}')
    exit(1)

# Test mock database
facilities = mock_api_get_facilities()
print(f'✓ Mock database working ({len(facilities)} facilities)')

# Test tools
from agent_tools import audit_tools
print(f'✓ {len(audit_tools)} agent tools loaded')
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Agent system tests passed"
else
    echo -e "${RED}✗${NC} Agent system tests failed"
    exit 1
fi
echo ""

# Step 4: Completion
echo "============================================================"
echo -e "${GREEN}✅ AGENT SYSTEM READY!${NC}"
echo "============================================================"
echo ""
echo "Your AER Compliance Agent is ready to use."
echo ""
echo "🚀 Quick Start Options:"
echo ""
echo "1. Web Interface (Recommended):"
echo "   python3 agent_app.py"
echo "   Then open: http://localhost:7860"
echo ""
echo "2. Command Line:"
echo "   python3 agent_core.py"
echo "   (Interactive mode)"
echo ""
echo "3. Demo Scenarios:"
echo "   python3 demo_scenarios.py"
echo "   (Pre-configured audit scenarios)"
echo ""
echo "4. Single Command:"
echo "   python3 agent_core.py \"Audit facility FAC-AB-001\""
echo ""
echo "============================================================"
echo ""
echo "📚 What's New:"
echo "  ✓ Autonomous agent with 7 tools"
echo "  ✓ Multi-tool orchestration (LangChain)"
echo "  ✓ RAG integration for directive queries"
echo "  ✓ Email automation (mock)"
echo "  ✓ Calendar scheduling (mock)"
echo "  ✓ Maintenance logging (mock)"
echo "  ✓ Agentic workflow execution"
echo ""
echo "============================================================"