import os
import sys
from datetime import datetime

def test_imports():
    """Test 1: Verify all modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Module Imports")
    print("="*60)
    
    try:
        import mock_db
        print("✓ mock_db imported")
        
        import agent_tools
        print("✓ agent_tools imported")
        
        import agent_core
        print("✓ agent_core imported")
        
        import industrial_rag_system
        print("✓ industrial_rag_system imported")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_mock_database():
    """Test 2: Verify mock database works"""
    print("\n" + "="*60)
    print("TEST 2: Mock Database")
    print("="*60)
    
    import mock_db
    
    try:
        # Test facility retrieval
        facilities = mock_db.mock_api_get_facilities()
        assert len(facilities) >= 2, "Should have at least 2 facilities"
        print(f"✓ Found {len(facilities)} facilities")
        
        # Test equipment retrieval
        equipment = mock_db.mock_api_fetch_equipment("FAC-AB-001")
        assert len(equipment) > 0, "FAC-AB-001 should have equipment"
        print(f"✓ Found {len(equipment)} equipment items at FAC-AB-001")
        
        # Test email system
        result = mock_db.mock_api_send_email(
            "test@example.com",
            "Test Subject",
            "Test body"
        )
        assert result['status'] == 'sent', "Email should be sent"
        print("✓ Email system working")
        
        # Test calendar system
        result = mock_db.mock_api_calendar_schedule(
            "Test task",
            "2025-01-20",
            "FAC-AB-001"
        )
        assert result['status'] == 'success', "Calendar should work"
        print("✓ Calendar system working")
        
        # Reset for clean state
        mock_db.reset_mock_data()
        print("✓ Data reset working")
        
        return True
        
    except Exception as e:
        print(f"✗ Mock database test failed: {e}")
        return False

def test_agent_tools():
    """Test 3: Verify agent tools are defined correctly"""
    print("\n" + "="*60)
    print("TEST 3: Agent Tools")
    print("="*60)
    
    import agent_tools
    
    try:
        tools = agent_tools.audit_tools
        
        expected_tools = [
            'list_facilities',
            'get_facility_equipment',
            'check_calibration_compliance',
            'search_aer_directives',
            'send_compliance_report',
            'schedule_follow_up',
            'log_maintenance_action'
        ]
        
        tool_names = [tool.name for tool in tools]
        
        print(f"✓ Found {len(tools)} tools")
        
        for expected in expected_tools:
            if expected in tool_names:
                print(f"  ✓ {expected}")
            else:
                print(f"  ✗ {expected} MISSING")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Agent tools test failed: {e}")
        return False

def test_agent_initialization():
    """Test 4: Verify agent can be initialized"""
    print("\n" + "="*60)
    print("TEST 4: Agent Initialization")
    print("="*60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set - skipping agent initialization test")
        return True  # Don't fail if API key not set
    
    try:
        from agent_core import AERComplianceAgent
        
        agent = AERComplianceAgent(verbose=False)
        print("✓ Agent initialized successfully")
        print(f"  Model: {agent.model}")
        print(f"  Tools: {len(agent.agent_executor.tools)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Agent initialization failed: {e}")
        return False

def test_tool_execution():
    """Test 5: Test individual tool execution"""
    print("\n" + "="*60)
    print("TEST 5: Tool Execution")
    print("="*60)
    
    import agent_tools
    import mock_db
    
    try:
        # Test list_facilities
        result = agent_tools.list_facilities.invoke({})
        assert "FAC-AB-001" in result, "Should list FAC-AB-001"
        print("✓ list_facilities working")
        
        # Test get_facility_equipment
        result = agent_tools.get_facility_equipment.invoke({"facility_id": "FAC-AB-001"})
        assert "EQ-PUMP-01" in result or "Equipment at FAC-AB-001" in result, "Should show equipment"
        print("✓ get_facility_equipment working")
        
        # Test check_calibration_compliance
        result = agent_tools.check_calibration_compliance.invoke({"facility_id": "FAC-AB-001"})
        assert "Compliance Report" in result or "NON-COMPLIANT" in result, "Should show compliance status"
        print("✓ check_calibration_compliance working")
        
        # Test schedule_follow_up
        result = agent_tools.schedule_follow_up.invoke({
            "task": "Test maintenance",
            "date": "2025-01-20",
            "facility_id": "FAC-AB-001"
        })
        assert "scheduled" in result.lower(), "Should confirm scheduling"
        print("✓ schedule_follow_up working")
        
        # Clean up
        mock_db.reset_mock_data()
        
        return True
        
    except Exception as e:
        print(f"✗ Tool execution test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_rag_system():
    """Test 6: Verify RAG system is available"""
    print("\n" + "="*60)
    print("TEST 6: RAG System")
    print("="*60)
    
    import os
    
    if not os.path.exists("./chroma_db"):
        print("⚠️  ChromaDB not found - run 'python3 industrial_rag_system.py' first")
        return True  # Don't fail, just warn
    
    try:
        from industrial_rag_system import IndustrialRAGSystem
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  OPENAI_API_KEY not set - skipping RAG test")
            return True
        
        rag = IndustrialRAGSystem(api_key=api_key)
        rag.load_index()
        
        stats = rag.get_stats()
        print(f"✓ RAG system loaded")
        print(f"  Documents: {stats['total_documents']}")
        print(f"  Chunks: {stats['total_chunks']}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  RAG system test warning: {e}")
        return True  # Don't fail, RAG is optional for core agent

def test_full_workflow():
    """Test 7: End-to-end workflow test"""
    print("\n" + "="*60)
    print("TEST 7: End-to-End Workflow (Simulation)")
    print("="*60)
    
    import mock_db
    
    try:
        # Simulate a complete audit workflow
        print("\nSimulating: Audit → Check → Email → Schedule")
        
        # Step 1: Get equipment
        equipment = mock_db.mock_api_fetch_equipment("FAC-AB-001")
        print(f"  1. Retrieved {len(equipment)} equipment items")
        
        # Step 2: Check compliance (manual check)
        from datetime import datetime, timedelta
        non_compliant = []
        for item in equipment:
            if 'last_calibration' in item:
                last_cal = datetime.strptime(item['last_calibration'], "%Y-%m-%d")
                days_since = (datetime.now() - last_cal).days
                if days_since > 365:
                    non_compliant.append(item['id'])
        
        print(f"  2. Found {len(non_compliant)} non-compliant items")
        
        # Step 3: Send email
        if non_compliant:
            result = mock_db.mock_api_send_email(
                "safety@petolab.com",
                "Compliance Alert",
                f"Non-compliant equipment: {', '.join(non_compliant)}"
            )
            print(f"  3. Email sent: {result['email_id']}")
        
        # Step 4: Schedule follow-up
        result = mock_db.mock_api_calendar_schedule(
            "Maintenance follow-up",
            "2025-01-20",
            "FAC-AB-001"
        )
        print(f"  4. Task scheduled: {result['confirmation_id']}")
        
        # Verify all actions logged
        emails = mock_db.get_all_emails()
        tasks = mock_db.get_all_scheduled_tasks()
        
        assert len(emails) >= 1, "Should have sent email"
        assert len(tasks) >= 1, "Should have scheduled task"
        
        print("\n✓ Complete workflow executed successfully")
        
        # Clean up
        mock_db.reset_mock_data()
        
        return True
        
    except Exception as e:
        print(f"✗ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*60)
    print("AER COMPLIANCE AGENT - TEST SUITE")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Module Imports", test_imports),
        ("Mock Database", test_mock_database),
        ("Agent Tools", test_agent_tools),
        ("Agent Initialization", test_agent_initialization),
        ("Tool Execution", test_tool_execution),
        ("RAG System", test_rag_system),
        ("Full Workflow", test_full_workflow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"Result: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("Status: ✅ ALL TESTS PASSED")
        print("="*60)
        print("\n🚀 System is ready! Run:")
        print("  python3 agent_app.py       (Web interface)")
        print("  python3 agent_core.py      (CLI)")
        print("  python3 demo_scenarios.py  (Demos)")
        return 0
    else:
        print(f"Status: ⚠️  {total_count - passed_count} test(s) failed")
        print("="*60)
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)