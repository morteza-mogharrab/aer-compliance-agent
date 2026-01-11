import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
import agent_tools
from datetime import datetime

class AERComplianceAgent:
    """
    Autonomous AI agent for industrial compliance auditing.
    Orchestrates multiple tools to perform complete audit workflows.
    """
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o", verbose: bool = True):
        """
        Initialize the compliance agent
        
        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4o, gpt-4-turbo, etc.)
            verbose: Whether to print detailed execution logs
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.model = model
        self.verbose = verbose
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0,  # Deterministic for compliance work
            api_key=self.api_key
        )
        
        # Create custom prompt for industrial compliance
        self.prompt = self._create_prompt()
        
        # Create agent
        self.agent = create_tool_calling_agent(

            self.llm,
            agent_tools.audit_tools,
            self.prompt
        )
        
        # Create executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=agent_tools.audit_tools,
            verbose=self.verbose,
            max_iterations=15,  # Prevent infinite loops
            handle_parsing_errors=True
        )
        
        print(f"✓ AER Compliance Agent initialized")
        print(f"  Model: {self.model}")
        print(f"  Tools: {len(agent_tools.audit_tools)} available")
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Create specialized prompt for compliance auditing"""
        system_message = """You are an expert AI agent for Alberta Energy Regulator (AER) compliance auditing.

Your Role:
- Perform autonomous compliance audits on industrial facilities
- Check equipment against AER directive requirements
- Take concrete actions: schedule maintenance, send reports, log findings
- Provide professional, detailed compliance reports

Your Tools:
- list_facilities: See all available facilities
- get_facility_equipment: Get equipment details for a facility
- check_calibration_compliance: Check if equipment meets calibration requirements
- search_aer_directives: Query the AER directive knowledge base for requirements
- send_compliance_report: Email audit reports to compliance officers
- schedule_follow_up: Schedule follow-up tasks in the calendar
- log_maintenance_action: Create maintenance logs

Workflow Best Practices:
1. When asked to audit a facility:
   - First, get the equipment list
   - Check compliance against relevant directives
   - If violations found: prepare detailed report, email it, and schedule follow-up
   - If compliant: send confirmation report

2. Always include in reports:
   - Facility ID and name
   - Date of audit
   - List of non-compliant items with specific details
   - Recommended actions
   - Follow-up dates

3. Be proactive:
   - Suggest follow-up dates (typically 1-2 weeks for critical issues)
   - Include directive citations
   - Categorize by severity (Critical, High, Medium)

4. Professional tone:
   - Use clear, technical language
   - Include specific equipment IDs and dates
   - Cite directive requirements

Current date: {current_date}
"""
        
        return ChatPromptTemplate.from_messages([
            ("system", system_message.format(current_date=datetime.now().strftime("%Y-%m-%d"))),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
    
    def run_audit(self, instruction: str) -> dict:
        """
        Execute an audit based on natural language instruction
        
        Args:
            instruction: What the agent should do (e.g., "Audit facility FAC-AB-001")
        
        Returns:
            dict with 'output' key containing the agent's response
        """
        print("\n" + "="*60)
        print("🤖 AER COMPLIANCE AGENT STARTING AUDIT")
        print("="*60)
        print(f"Instruction: {instruction}")
        print("="*60 + "\n")
        
        try:
            result = self.agent_executor.invoke({"input": instruction})
            
            print("\n" + "="*60)
            print("✅ AUDIT COMPLETE")
            print("="*60)
            
            return result
            
        except Exception as e:
            print(f"\n❌ Error during audit: {e}")
            return {
                "output": f"Audit failed with error: {str(e)}",
                "error": str(e)
            }
    
    def run_interactive(self):
        """Run the agent in interactive mode"""
        print("\n" + "="*60)
        print("🤖 AER COMPLIANCE AGENT - INTERACTIVE MODE")
        print("="*60)
        print("Type 'quit' or 'exit' to stop")
        print("Type 'help' for example commands")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self._print_help()
                    continue
                
                result = self.run_audit(user_input)
                print(f"\nAgent: {result['output']}\n")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")
    
    def _print_help(self):
        """Print example commands"""
        print("\n📋 Example Commands:")
        print("  - 'List all facilities'")
        print("  - 'Audit facility FAC-AB-001 for Directive 017 compliance'")
        print("  - 'Check calibration compliance at FAC-AB-001 and email results to safety@petolab.com'")
        print("  - 'What are the calibration requirements in Directive 017?'")
        print("  - 'Perform full audit of FAC-AB-002 and schedule maintenance if needed'")
        print()

def main():
    """Command-line interface for the agent"""
    import sys
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set")
        print("Run: export OPENAI_API_KEY='your-key'")
        sys.exit(1)
    
    # Initialize agent
    try:
        agent = AERComplianceAgent(verbose=True)
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        sys.exit(1)
    
    # Run predefined audit or interactive mode
    if len(sys.argv) > 1:
        # Command provided as argument
        instruction = " ".join(sys.argv[1:])
        result = agent.run_audit(instruction)
        print("\n🤖 FINAL RESPONSE:")
        print(result['output'])
    else:
        # Interactive mode
        agent.run_interactive()

if __name__ == "__main__":
    main()