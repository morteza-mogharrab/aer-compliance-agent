import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# ==============================================================================
# MOCK FACILITY DATABASE
# ==============================================================================

MOCK_FACILITIES = {
    "FAC-AB-001": {
        "facility_id": "FAC-AB-001",
        "name": "Edmonton South Terminal",
        "location": "Edmonton, AB",
        "operator": "PetroLab Energy",
        "equipment": [
            {
                "id": "EQ-PUMP-01",
                "type": "Glycol Pump",
                "directive_category": "Directive 017",
                "last_calibration": (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d"),
                "status": "Active",
                "criticality": "High"
            },
            {
                "id": "EQ-METER-04",
                "type": "Gas Flow Meter",
                "directive_category": "Directive 017",
                "last_calibration": (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d"),
                "status": "Active",
                "criticality": "Critical"
            },
            {
                "id": "EQ-FLARE-02",
                "type": "Flare Stack",
                "directive_category": "Directive 060",
                "last_inspection": (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"),
                "status": "Active",
                "criticality": "High"
            },
            {
                "id": "EQ-METER-05",
                "type": "Differential Pressure Meter",
                "directive_category": "Directive 017",
                "last_calibration": (datetime.now() - timedelta(days=380)).strftime("%Y-%m-%d"),
                "status": "Active",
                "criticality": "High"
            }
        ]
    },
    "FAC-AB-002": {
        "facility_id": "FAC-AB-002",
        "name": "Calgary Processing Plant",
        "location": "Calgary, AB",
        "operator": "PetroLab Energy",
        "equipment": [
            {
                "id": "EQ-METER-10",
                "type": "Turbine Meter",
                "directive_category": "Directive 017",
                "last_calibration": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                "status": "Active",
                "criticality": "Critical"
            }
        ]
    }
}

MAINTENANCE_LOG = []
EMAIL_OUTBOX = []
SCHEDULED_TASKS = []

def mock_api_get_facilities() -> List[Dict]:
    """Get all facilities"""
    return [
        {
            "facility_id": fac["facility_id"],
            "name": fac["name"],
            "location": fac["location"],
            "operator": fac["operator"]
        }
        for fac in MOCK_FACILITIES.values()
    ]

def mock_api_fetch_equipment(facility_id: str) -> List[Dict]:
    """Simulates GET /api/facilities/{id}/equipment"""
    facility = MOCK_FACILITIES.get(facility_id)
    if facility:
        return facility["equipment"]
    return []

def mock_api_get_facility_info(facility_id: str) -> Optional[Dict]:
    """Get basic facility information"""
    facility = MOCK_FACILITIES.get(facility_id)
    if facility:
        return {
            "facility_id": facility["facility_id"],
            "name": facility["name"],
            "location": facility["location"],
            "operator": facility["operator"],
            "equipment_count": len(facility["equipment"])
        }
    return None

def mock_api_calendar_schedule(task: str, date: str, facility_id: str = None) -> Dict:
    """Simulates POST /api/calendar/schedule"""
    task_entry = {
        "confirmation_id": f"CAL-{len(SCHEDULED_TASKS) + 1000}",
        "task": task,
        "scheduled_date": date,
        "facility_id": facility_id,
        "created_at": datetime.now().isoformat(),
        "status": "scheduled"
    }
    SCHEDULED_TASKS.append(task_entry)
    return {
        "status": "success",
        "confirmation_id": task_entry["confirmation_id"],
        "scheduled_date": date,
        "task": task
    }

def mock_api_send_email(to: str, subject: str, body: str, cc: List[str] = None) -> Dict:
    """Simulates POST /api/email/send"""
    email_entry = {
        "id": f"EMAIL-{len(EMAIL_OUTBOX) + 1000}",
        "to": to,
        "cc": cc or [],
        "subject": subject,
        "body": body,
        "sent_at": datetime.now().isoformat(),
        "status": "sent"
    }
    EMAIL_OUTBOX.append(email_entry)
    
    print("\n" + "="*60)
    print("📨 [MOCK EMAIL SENT]")
    print("="*60)
    print(f"To: {to}")
    if cc:
        print(f"CC: {', '.join(cc)}")
    print(f"Subject: {subject}")
    print(f"Body Preview:\n{body[:200]}...")
    print("="*60 + "\n")
    
    return {
        "status": "sent",
        "email_id": email_entry["id"],
        "timestamp": email_entry["sent_at"]
    }

def mock_api_log_maintenance(equipment_id: str, action: str, notes: str) -> Dict:
    """Simulates POST /api/maintenance/log"""
    log_entry = {
        "log_id": f"MAINT-{len(MAINTENANCE_LOG) + 1000}",
        "equipment_id": equipment_id,
        "action": action,
        "notes": notes,
        "logged_at": datetime.now().isoformat(),
        "logged_by": "AI Agent"
    }
    MAINTENANCE_LOG.append(log_entry)
    return {
        "status": "logged",
        "log_id": log_entry["log_id"]
    }

def mock_api_update_equipment_status(equipment_id: str, status: str) -> Dict:
    """Simulates PATCH /api/equipment/{id}/status"""
    for facility in MOCK_FACILITIES.values():
        for equipment in facility["equipment"]:
            if equipment["id"] == equipment_id:
                equipment["status"] = status
                return {
                    "status": "success",
                    "equipment_id": equipment_id,
                    "new_status": status
                }
    return {"status": "error", "message": "Equipment not found"}

def get_all_scheduled_tasks() -> List[Dict]:
    """Get all scheduled tasks"""
    return SCHEDULED_TASKS

def get_all_emails() -> List[Dict]:
    """Get all sent emails"""
    return EMAIL_OUTBOX

def get_maintenance_logs() -> List[Dict]:
    """Get all maintenance logs"""
    return MAINTENANCE_LOG

def reset_mock_data():
    """Reset all mock data to initial state"""
    global SCHEDULED_TASKS, EMAIL_OUTBOX, MAINTENANCE_LOG
    SCHEDULED_TASKS = []
    EMAIL_OUTBOX = []
    MAINTENANCE_LOG = []
