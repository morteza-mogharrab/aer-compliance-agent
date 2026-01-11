import os
import gradio as gr
from agent_core import AERComplianceAgent
from datetime import datetime
import mock_db
import json

class AgentWebInterface:
    """Web interface for the compliance agent"""
    
    def __init__(self):
        self.agent = None
        self.conversation_history = []
        self.initialize_agent()
    
    def initialize_agent(self):
        """Initialize the AI agent"""
        print("Initializing AER Compliance Agent...")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        try:
            self.agent = AERComplianceAgent(api_key=api_key, verbose=False)
            print("✓ Agent ready")
        except Exception as e:
            print(f"ERROR: {e}")
            raise
    
    def chat(self, message, history):
        """Process agent instruction"""
        if not message or not message.strip():
            return history
        
        # Append user message
        history.append({"role": "user", "content": message})
        
        # Append placeholder
        history.append({"role": "assistant", "content": "🤖 Agent working..."})
        yield history
        
        try:
            # Run agent
            result = self.agent.run_audit(message)
            
            # Store conversation
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'query': message,
                'response': result['output']
            })
            
            # Update with real response
            history[-1]['content'] = result['output']
            yield history
            
        except Exception as e:
            error_msg = f"❌ Agent error: {str(e)}\n\nPlease try rephrasing your instruction."
            history[-1]['content'] = error_msg
            yield history
    
    def clear_chat(self):
        """Clear conversation"""
        self.conversation_history = []
        mock_db.reset_mock_data()
        return []
    
    def get_system_status(self):
        """Get current system status"""
        facilities = mock_db.mock_api_get_facilities()
        tasks = mock_db.get_all_scheduled_tasks()
        emails = mock_db.get_all_emails()
        logs = mock_db.get_maintenance_logs()
        
        status = f"""
### 📊 System Status
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Active Facilities:** {len(facilities)}  
**Scheduled Tasks:** {len(tasks)}  
**Emails Sent:** {len(emails)}  
**Maintenance Logs:** {len(logs)}
"""
        return status

def create_interface():
    """Create production-ready Gradio interface"""
    interface = AgentWebInterface()
    
    # Modern, accessible CSS
    custom_css = """
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .gradio-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    /* Header - Always white text on dark background */
    .app-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #3b82f6 100%);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .app-header h1 {
        color: #ffffff !important;
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        line-height: 1.2;
    }
    
    .app-header p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.1rem;
        margin: 0 0 1rem 0;
        line-height: 1.5;
    }
    
    .app-header .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.2);
        color: #ffffff !important;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }
    
    /* Info cards */
    .info-section {
        margin-bottom: 2rem;
    }
    
    .info-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .info-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transform: translateY(-2px);
    }
    
    .info-card h3 {
        color: #111827;
        font-size: 1.125rem;
        font-weight: 600;
        margin: 0 0 0.75rem 0;
    }
    
    .info-card p {
        color: #6b7280;
        font-size: 0.938rem;
        line-height: 1.6;
        margin: 0;
    }
    
    .info-card ul {
        margin: 0;
        padding-left: 1.25rem;
        color: #6b7280;
    }
    
    .info-card li {
        margin-bottom: 0.5rem;
        line-height: 1.5;
    }
    
    /* Chat interface */
    .chat-container {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .chat-header-bar {
        background: linear-gradient(to right, #f9fafb, #ffffff);
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .chat-header-bar h2 {
        color: #111827;
        font-size: 1.125rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Chatbot styling */
    #chatbot {
        height: 500px !important;
        border: none !important;
    }
    
    /* User messages - dark blue background with white text */
    #chatbot .message.user {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border-radius: 12px 12px 4px 12px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
    }
    
    #chatbot .message.user p,
    #chatbot .message.user span,
    #chatbot .message.user div {
        color: #ffffff !important;
    }
    
    /* Bot messages - light background with dark text */
    #chatbot .message.bot {
        background: #f9fafb !important;
        color: #111827 !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px 12px 12px 4px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
    }
    
    #chatbot .message.bot p,
    #chatbot .message.bot span,
    #chatbot .message.bot div {
        color: #111827 !important;
    }
    
    /* Input area */
    .input-section {
        padding: 1.5rem;
        background: white;
        border-top: 1px solid #e5e7eb;
    }
    
    .input-section textarea {
        border: 2px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.938rem !important;
        transition: all 0.2s ease !important;
        background: #ffffff !important;
        color: #111827 !important;
    }
    
    .input-section textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
    }
    
    .input-section textarea::placeholder {
        color: #9ca3af !important;
    }
    
    /* Buttons */
    button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .primary-btn {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
    }
    
    .primary-btn:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.4) !important;
    }
    
    .secondary-btn {
        background: white !important;
        color: #374151 !important;
        border: 1px solid #e5e7eb !important;
    }
    
    .secondary-btn:hover {
        background: #f9fafb !important;
        border-color: #d1d5db !important;
    }
    
    /* Sidebar */
    .sidebar-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-card h3 {
        color: #111827;
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
    }
    
    /* Status display */
    .status-box {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .status-box h3 {
        color: #111827 !important;
        font-size: 0.938rem !important;
        font-weight: 600 !important;
    }
    
    .status-box p,
    .status-box strong {
        color: #374151 !important;
    }
    
    /* Quick action buttons */
    .quick-action-btn {
        width: 100%;
        text-align: left !important;
        background: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        color: #374151 !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.5rem !important;
        font-size: 0.875rem !important;
    }
    
    .quick-action-btn:hover {
        background: #ffffff !important;
        border-color: #3b82f6 !important;
        color: #1e40af !important;
    }
    
    /* Examples */
    .examples-container button {
        background: #f9fafb !important;
        border: 1px solid #e5e7eb !important;
        color: #374151 !important;
        padding: 0.875rem 1rem !important;
        text-align: left !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    
    .examples-container button:hover {
        background: #ffffff !important;
        border-color: #3b82f6 !important;
        transform: translateX(4px);
    }
    
    /* Footer */
    .app-footer {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-top: 2rem;
        text-align: center;
    }
    
    .app-footer h4 {
        color: #ffffff !important;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }
    
    .app-footer p {
        color: rgba(255, 255, 255, 0.9) !important;
        margin: 0.5rem 0;
    }
    
    .app-footer .tech-stack {
        display: flex;
        gap: 0.75rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    
    .app-footer .tech-badge {
        background: rgba(255, 255, 255, 0.2);
        color: #ffffff !important;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .app-header h1 {
            font-size: 1.5rem;
        }
        
        .app-header p {
            font-size: 1rem;
        }
        
        #chatbot {
            height: 400px !important;
        }
    }
    """
    
    with gr.Blocks(title="AER Compliance Agent", theme=gr.themes.Soft()) as demo:
        
        # Header
        gr.HTML("""
        <div class="app-header">
            <h1>🤖 AER Compliance Agent</h1>
            <p>Autonomous AI Agent for Industrial Compliance Auditing</p>
            <div class="badge">⚡ Agentic AI • Multi-Tool Orchestration • RAG-Powered</div>
        </div>
        """)
        
        # Info Cards
        with gr.Row(elem_classes=["info-section"]):
            with gr.Column(scale=1):
                gr.HTML("""
                <div class="info-card">
                    <h3>🎯 Agent Capabilities</h3>
                    <ul>
                        <li><strong>Autonomous Auditing:</strong> Performs complete compliance checks</li>
                        <li><strong>Multi-Tool Orchestration:</strong> Uses 7+ tools to complete tasks</li>
                        <li><strong>RAG Integration:</strong> Queries AER directive knowledge base</li>
                        <li><strong>Action Execution:</strong> Sends emails, schedules tasks, logs actions</li>
                    </ul>
                </div>
                """)
            
            with gr.Column(scale=1):
                gr.HTML("""
                <div class="info-card">
                    <h3>🔧 Available Tools</h3>
                    <ul>
                        <li><code>list_facilities</code> - View all facilities</li>
                        <li><code>get_facility_equipment</code> - Fetch equipment data</li>
                        <li><code>check_calibration_compliance</code> - Audit compliance</li>
                        <li><code>search_aer_directives</code> - Query regulations</li>
                        <li><code>send_compliance_report</code> - Email reports</li>
                        <li><code>schedule_follow_up</code> - Calendar scheduling</li>
                        <li><code>log_maintenance_action</code> - Create logs</li>
                    </ul>
                </div>
                """)
        
        # Main Content
        with gr.Row():
            # Chat Section
            with gr.Column(scale=3):
                with gr.Group(elem_classes=["chat-container"]):
                    gr.HTML("""
                    <div class="chat-header-bar">
                        <h2>💬 Agent Execution Log</h2>
                    </div>
                    """)
                    
                    chatbot = gr.Chatbot(
                        [],
                        elem_id="chatbot",
                        show_label=False,
                        height=500
                    )
                    
                    with gr.Group(elem_classes=["input-section"]):
                        with gr.Row():
                            msg = gr.Textbox(
                                placeholder="Give the agent an instruction (e.g., 'Audit facility FAC-AB-001 and email results to safety@petolab.com')",
                                show_label=False,
                                scale=4,
                                container=False,
                                lines=2
                            )
                            submit_btn = gr.Button(
                                "▶️ Execute", 
                                variant="primary",
                                scale=1,
                                elem_classes=["primary-btn"]
                            )
                        
                        clear_btn = gr.Button(
                            "🗑️ Clear & Reset",
                            elem_classes=["secondary-btn"],
                            size="sm"
                        )
            
            # Sidebar
            with gr.Column(scale=1):
                with gr.Group(elem_classes=["sidebar-card"]):
                    gr.Markdown("### 📊 System Status")
                    status_display = gr.Markdown(
                        interface.get_system_status(),
                        elem_classes=["status-box"]
                    )
                    refresh_btn = gr.Button(
                        "🔄 Refresh Status",
                        elem_classes=["secondary-btn"],
                        size="sm"
                    )
                
                with gr.Group(elem_classes=["sidebar-card"]):
                    gr.Markdown("### 📁 Quick Actions")
                    
                    audit_btn = gr.Button(
                        "🔍 Audit FAC-AB-001",
                        elem_classes=["quick-action-btn"]
                    )
                    list_btn = gr.Button(
                        "📋 List Facilities",
                        elem_classes=["quick-action-btn"]
                    )
                    check_all_btn = gr.Button(
                        "✅ Check All Compliance",
                        elem_classes=["quick-action-btn"]
                    )
                    query_btn = gr.Button(
                        "📖 Query Directive",
                        elem_classes=["quick-action-btn"]
                    )
        
        # Examples Section
        gr.Markdown("### 💡 Example Instructions")
        
        with gr.Group(elem_classes=["examples-container"]):
            examples = gr.Examples(
                examples=[
                    "Audit facility FAC-AB-001 for Directive 017 calibration compliance. If violations found, email safety@petolab.com and schedule follow-up.",
                    "Check all equipment at FAC-AB-002 and create a compliance report",
                    "What are the temperature compensation requirements in Directive 017?",
                    "List all facilities and check which ones have non-compliant equipment",
                    "For each non-compliant item at FAC-AB-001, log a maintenance action and schedule calibration",
                    "Perform a comprehensive audit of all facilities and send executive summary to management@petolab.com"
                ],
                inputs=msg,
                label=None
            )
        
        # Footer
        gr.HTML("""
        <div class="app-footer">
            <h4>Alberta Energy Regulator Compliance Agent</h4>
            <p>Autonomous AI agent combining RAG knowledge retrieval with agentic tool execution</p>
            <div class="tech-stack">
                <span class="tech-badge">GPT-4o</span>
                <span class="tech-badge">LangChain</span>
                <span class="tech-badge">ChromaDB</span>
                <span class="tech-badge">Multi-Tool Orchestration</span>
            </div>
        </div>
        """)
        
        # Event Handlers
        def submit_and_clear(message, history):
            for response in interface.chat(message, history):
                yield response, ""
        
        # Quick action button handlers
        audit_btn.click(
            lambda: "Audit facility FAC-AB-001 for Directive 017 compliance and email results to safety@petolab.com",
            outputs=msg
        )
        
        list_btn.click(
            lambda: "List all available facilities",
            outputs=msg
        )
        
        check_all_btn.click(
            lambda: "Check calibration compliance for all facilities and send summary to operations@petolab.com",
            outputs=msg
        )
        
        query_btn.click(
            lambda: "What are the calibration requirements in Directive 017?",
            outputs=msg
        )
        
        # Main handlers
        msg.submit(
            submit_and_clear,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )
        
        submit_btn.click(
            submit_and_clear,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )
        
        clear_btn.click(
            interface.clear_chat,
            outputs=[chatbot]
        )
        
        refresh_btn.click(
            interface.get_system_status,
            outputs=[status_display]
        )
    
    return demo, custom_css

def main():
    """Launch the application"""
    print("="*60)
    print("AER Compliance Agent - Web Interface")
    print("Autonomous AI Agent for Industrial Compliance")
    print("="*60)
    
    try:
        demo, custom_css = create_interface()
        print("\n✓ Starting web server...")
        print("\nAccess the application at: http://localhost:7860")
        print("Press Ctrl+C to stop\n")
        
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure OPENAI_API_KEY is set")
        print("2. Run setup_agent.sh first")
        raise

if __name__ == "__main__":
    main()