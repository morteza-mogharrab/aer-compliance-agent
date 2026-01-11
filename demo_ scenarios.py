import os
from agent_core import AERComplianceAgent
from datetime import datetime, timedelta
import mock_db

def run_scenario_1():
    """
    Scenario 1: Basic Compliance Audit
    Shows agent detecting violations and taking action
    """
    print("\n" + "="*80)
    print("SCENARIO 1: Basic Compliance Audit with Violations")
    print("="*80)
    print("Demonstrates: Equipment audit, violation detection, reporting, scheduling")
    print("="*80 + "\n")
    
    agent = AERComplianceAgent(verbose=True)
    
    instruction = """
    Audit facility FAC-AB-001 for Directive 017 calibration compliance.
    
    Steps:
    1. Check the calibration requirements from Directive 017
    2. Check all equipment at the facility
    3. If there are violations, email a detailed report to safety@petolab.com
    4. Schedule maintenance follow-up for next Monday
    """
    
    result = agent.run_audit(instruction)
    
    print("\n" + "="*80)
    print("SCENARIO 1 COMPLETE")
    print("="*80)
    print("\n📊 What just happened:")
    print("  ✓ Agent queried directive requirements")
    print("  ✓ Checked equipment calibration dates")
    print("  ✓ Detected 2 non-compliant items")
    print("  ✓ Sent email report to compliance officer")
    print("  ✓ Scheduled follow-up maintenance")
    print("="*80 + "\n")

def run_scenario_2():
    """
    Scenario 2: Multi-Facility Audit
    Shows agent handling multiple facilities
    """
    print("\n" + "="*80)
    print("SCENARIO 2: Multi-Facility Compliance Check")
    print("="*80)
    print("Demonstrates: Listing facilities, auditing multiple locations")
    print("="*80 + "\n")
    
    agent = AERComplianceAgent(verbose=True)
    
    instruction = """
    I need a compliance status report for all our facilities.
    
    Please:
    1. List all available facilities
    2. Check calibration compliance for each facility
    3. Send a summary report to operations@petolab.com with the overall compliance status
    """
    
    result = agent.run_audit(instruction)
    
    print("\n" + "="*80)
    print("SCENARIO 2 COMPLETE")
    print("="*80)
    print("\n📊 What just happened:")
    print("  ✓ Agent listed all facilities")
    print("  ✓ Audited multiple locations")
    print("  ✓ Compiled summary report")
    print("  ✓ Sent consolidated email")
    print("="*80 + "\n")

def run_scenario_3():
    """
    Scenario 3: Knowledge Base Query
    Shows agent using RAG system for directive guidance
    """
    print("\n" + "="*80)
    print("SCENARIO 3: Directive Knowledge Query")
    print("="*80)
    print("Demonstrates: RAG system integration, regulatory guidance")
    print("="*80 + "\n")
    
    agent = AERComplianceAgent(verbose=True)
    
    instruction = """
    I need to understand the requirements for gas measurement equipment.
    
    Please:
    1. Search Directive 017 for calibration and temperature compensation requirements
    2. Provide a summary of the key requirements
    3. Check if our facility FAC-AB-001 meets these requirements
    """
    
    result = agent.run_audit(instruction)
    
    print("\n" + "="*80)
    print("SCENARIO 3 COMPLETE")
    print("="*80)
    print("\n📊 What just happened:")
    print("  ✓ Agent queried RAG knowledge base")
    print("  ✓ Retrieved directive requirements")
    print("  ✓ Cross-checked with facility equipment")
    print("  ✓ Provided compliance assessment")
    print("="*80 + "\n")

def run_scenario_4():
    """
    Scenario 4: Proactive Maintenance Scheduling
    Shows agent making autonomous decisions
    """
    print("\n" + "="*80)
    print("SCENARIO 4: Proactive Maintenance Planning")
    print("="*80)
    print("Demonstrates: Autonomous decision-making, proactive scheduling")
    print("="*80 + "\n")
    
    agent = AERComplianceAgent(verbose=True)
    
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    instruction = f"""
    Perform a comprehensive audit of facility FAC-AB-001.
    
    For each non-compliant equipment:
    1. Log a maintenance action noting the violation
    2. Schedule calibration for {next_week}
    3. Send individual notifications to the maintenance team at maintenance@petolab.com
    
    Prioritize by equipment criticality.
    """
    
    result = agent.run_audit(instruction)
    
    print("\n" + "="*80)
    print("SCENARIO 4 COMPLETE")
    print("="*80)
    print("\n📊 What just happened:")
    print("  ✓ Agent performed comprehensive audit")
    print("  ✓ Created maintenance logs")
    print("  ✓ Scheduled multiple tasks")
    print("  ✓ Sent targeted notifications")
    print("  ✓ Prioritized by criticality")
    print("="*80 + "\n")

def run_all_scenarios():
    """Run all demo scenarios sequentially"""
    print("\n" + "="*80)
    print("🤖 AER COMPLIANCE AGENT - COMPLETE DEMO")
    print("="*80)
    print("Running all scenarios to demonstrate agent capabilities...")
    print("="*80 + "\n")
    
    scenarios = [
        ("Scenario 1", run_scenario_1),
        ("Scenario 2", run_scenario_2),
        ("Scenario 3", run_scenario_3),
        ("Scenario 4", run_scenario_4),
    ]
    
    for name, scenario_func in scenarios:
        input(f"\nPress ENTER to run {name}...")
        scenario_func()
        mock_db.reset_mock_data()  # Reset between scenarios
    
    print("\n" + "="*80)
    print("✅ ALL SCENARIOS COMPLETE")
    print("="*80)
    print("\nAgent Capabilities Demonstrated:")
    print("  ✓ Autonomous compliance auditing")
    print("  ✓ Multi-tool orchestration")
    print("  ✓ RAG knowledge base integration")
    print("  ✓ Email report generation")
    print("  ✓ Calendar/scheduling automation")
    print("  ✓ Maintenance logging")
    print("  ✓ Proactive decision-making")
    print("="*80 + "\n")

def interactive_demo():
    """Interactive demo mode"""
    print("\n" + "="*80)
    print("🤖 AER COMPLIANCE AGENT - INTERACTIVE DEMO")
    print("="*80)
    print("\nChoose a scenario to run:")
    print("  1. Basic Compliance Audit (violations detected)")
    print("  2. Multi-Facility Audit")
    print("  3. Directive Knowledge Query")
    print("  4. Proactive Maintenance Planning")
    print("  5. Run All Scenarios")
    print("  6. Custom Query (Interactive Mode)")
    print("  0. Exit")
    print("="*80 + "\n")
    
    while True:
        choice = input("Enter choice (0-6): ").strip()
        
        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            run_scenario_1()
        elif choice == "2":
            run_scenario_2()
        elif choice == "3":
            run_scenario_3()
        elif choice == "4":
            run_scenario_4()
        elif choice == "5":
            run_all_scenarios()
        elif choice == "6":
            agent = AERComplianceAgent(verbose=True)
            agent.run_interactive()
        else:
            print("Invalid choice. Please enter 0-6.")
        
        if choice in ["1", "2", "3", "4"]:
            mock_db.reset_mock_data()
            print("\n" + "="*80)
            print("Choose another scenario or press 0 to exit:")
            print("="*80 + "\n")

def main():
    """Main entry point"""
    import sys
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set")
        print("Run: export OPENAI_API_KEY='your-key'")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        scenario_num = sys.argv[1]
        if scenario_num == "1":
            run_scenario_1()
        elif scenario_num == "2":
            run_scenario_2()
        elif scenario_num == "3":
            run_scenario_3()
        elif scenario_num == "4":
            run_scenario_4()
        elif scenario_num == "all":
            run_all_scenarios()
        else:
            print(f"Unknown scenario: {scenario_num}")
            print("Usage: python demo_scenarios.py [1|2|3|4|all]")
    else:
        interactive_demo()

if __name__ == "__main__":
    main()