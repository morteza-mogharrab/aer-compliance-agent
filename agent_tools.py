from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import List, Optional
import mock_db
from datetime import datetime, timedelta
from industrial_rag_system import IndustrialRAGSystem
import os

# ==============================================================================
# INPUT SCHEMAS (Type Safety)
# ==============================================================================

class FacilityInput(BaseModel):
    facility_id: str = Field(description="The ID of the facility to audit (e.g., FAC-AB-001)")

class EmailInput(BaseModel):
    recipient: str = Field(description="Email address of the compliance officer")
    subject: str = Field(description="Subject line of the email")
    report_body: str = Field(description="Full text content of the compliance report")
    cc: Optional[List[str]] = Field(default=None, description="CC recipients")

class ScheduleInput(BaseModel):
    task: str = Field(description="Task description for the scheduled item")
    date: str = Field(description="Date for follow-up in YYYY-MM-DD format")
    facility_id: Optional[str] = Field(default=None, description="Associated facility ID")

class MaintenanceLogInput(BaseModel):
    equipment_id: str = Field(description="Equipment ID")
    action: str = Field(description="Maintenance action taken")
    notes: str = Field(description="Additional notes")

class DirectiveQueryInput(BaseModel):
    query: str = Field(description="Question about AER directives")

# ==============================================================================
# RAG SYSTEM INITIALIZATION
# ==============================================================================

_rag_system = None

def get_rag_system():
    """Initialize RAG system once and reuse"""
    global _rag_system
    if _rag_system is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        _rag_system = IndustrialRAGSystem(api_key=api_key)
        try:
            _rag_system.load_index()
            print("✓ RAG system loaded successfully")
        except Exception as e:
            print(f"Warning: Could not load RAG index: {e}")
    return _rag_system

# ==============================================================================
# TOOL DEFINITIONS
# ==============================================================================

@tool
def list_facilities() -> str:
    """Get a list of all available facilities that can be audited."""
    facilities = mock_db.mock_api_get_facilities()
    if not facilities:
        return "No facilities found in the system."
    
    result = "Available Facilities:\n"
    for fac in facilities:
        result += f"- {fac['facility_id']}: {fac['name']} ({fac['location']})\n"
    return result

@tool("get_facility_equipment", args_schema=FacilityInput)
def get_facility_equipment(facility_id: str) -> str:
    """Fetch the complete list of equipment for a specific facility to check against directives."""
    data = mock_db.mock_api_fetch_equipment(facility_id)
    if not data:
        return f"No equipment found for facility ID: {facility_id}"
    
    result = f"Equipment at {facility_id}:\n"
    for item in data:
        result += f"\n- ID: {item['id']}\n"
        result += f"  Type: {item['type']}\n"
        result += f"  Directive: {item['directive_category']}\n"
        result += f"  Status: {item['status']}\n"
        if 'last_calibration' in item:
            result += f"  Last Calibration: {item['last_calibration']}\n"
        if 'criticality' in item:
            result += f"  Criticality: {item['criticality']}\n"
    
    return result

@tool("check_calibration_compliance", args_schema=FacilityInput)
def check_calibration_compliance(facility_id: str) -> str:
    """
    Checks equipment calibration dates against the 1-year requirement from Directive 017.
    Returns detailed list of non-compliant items with days overdue.
    """
    equipment_list = mock_db.mock_api_fetch_equipment(facility_id)
    if not equipment_list:
        return f"No equipment found for facility {facility_id}"
    
    non_compliant = []
    compliant = []
    current_date = datetime.now()
    
    for item in equipment_list:
        if 'last_calibration' not in item:
            continue
            
        last_cal = datetime.strptime(item['last_calibration'], "%Y-%m-%d")
        days_since = (current_date - last_cal).days
        
        if days_since > 365:
            days_overdue = days_since - 365
            non_compliant.append({
                'id': item['id'],
                'type': item['type'],
                'days_since': days_since,
                'days_overdue': days_overdue,
                'last_cal': item['last_calibration'],
                'criticality': item.get('criticality', 'Unknown')
            })
        else:
            compliant.append(f"✅ {item['type']} (ID: {item['id']}) - Compliant ({days_since} days)")
    
    result = f"Calibration Compliance Report for {facility_id}\n"
    result += f"Date: {current_date.strftime('%Y-%m-%d')}\n\n"
    
    if non_compliant:
        result += "⚠️  NON-COMPLIANT EQUIPMENT (Exceeds 365-day requirement):\n"
        for item in non_compliant:
            result += f"\n❌ {item['type']} (ID: {item['id']})\n"
            result += f"   Last Calibrated: {item['last_cal']} ({item['days_since']} days ago)\n"
            result += f"   Days Overdue: {item['days_overdue']}\n"
            result += f"   Criticality: {item['criticality']}\n"
        result += f"\nTotal Non-Compliant: {len(non_compliant)} items\n"
    else:
        result += "✅ ALL EQUIPMENT IS COMPLIANT\n"
    
    if compliant:
        result += f"\n✅ Compliant Equipment ({len(compliant)} items):\n"
        for item in compliant:
            result += f"  {item}\n"
    
    return result

@tool("search_aer_directives", args_schema=DirectiveQueryInput)
def search_aer_directives(query: str) -> str:
    """
    Searches the AER Directive knowledge base (RAG system) for specific requirements,
    procedures, or technical specifications. Use this to find authoritative guidance
    from official directives.
    """
    try:
        rag = get_rag_system()
        response = rag.generate_response(query, top_k=3)
        
        answer = response['answer']
        sources = response.get('sources', [])
        
        result = f"AER Directive Guidance:\n\n{answer}\n"
        
        if sources:
            result += "\n📚 Sources:\n"
            for i, source in enumerate(sources[:2], 1):
                doc_name = source.get('document', 'Unknown')
                result += f"  {i}. {doc_name} (Relevance: {source.get('relevance', 0):.2f})\n"
        
        return result
        
    except Exception as e:
        # Fallback if RAG system not available
        return f"AER Directive 017 requires gas metering equipment to be calibrated/proved at least once every 365 days. Temperature and pressure compensation devices must be calibrated according to manufacturer specifications. (Note: Full RAG system unavailable: {str(e)})"

@tool("send_compliance_report", args_schema=EmailInput)
def send_compliance_report(recipient: str, subject: str, report_body: str, cc: Optional[List[str]] = None) -> str:
    """
    Sends the final audit report via email to the compliance officer.
    Use this after completing an audit to notify stakeholders.
    """
    result = mock_db.mock_api_send_email(recipient, subject, report_body, cc)
    return f"✅ Report emailed successfully to {recipient}. Email ID: {result['email_id']}"

@tool("schedule_follow_up", args_schema=ScheduleInput)
def schedule_follow_up(task: str, date: str, facility_id: Optional[str] = None) -> str:
    """
    Schedule a follow-up audit, maintenance task, or inspection in the calendar system.
    Date must be in YYYY-MM-DD format.
    """
    res = mock_db.mock_api_calendar_schedule(task, date, facility_id)
    return f"✅ Follow-up scheduled: {task} on {date}. Confirmation ID: {res['confirmation_id']}"

@tool("log_maintenance_action", args_schema=MaintenanceLogInput)
def log_maintenance_action(equipment_id: str, action: str, notes: str) -> str:
    """
    Log a maintenance action for equipment. Use this to create audit trails
    for maintenance activities.
    """
    result = mock_db.mock_api_log_maintenance(equipment_id, action, notes)
    return f"✅ Maintenance logged for {equipment_id}. Log ID: {result['log_id']}"

# ==============================================================================
# EXPORT TOOLS LIST
# ==============================================================================

audit_tools = [
    list_facilities,
    get_facility_equipment,
    check_calibration_compliance,
    search_aer_directives,
    send_compliance_report,
    schedule_follow_up,
    log_maintenance_action
]