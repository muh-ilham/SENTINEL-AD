"""
utils/soar_storage.py - Persistent Storage for SOAR Escalations, Approvals & Audit Trail
Ensures all escalated incidents, commander approvals, and audit logs persist across
browser refreshes (F5), new sessions, and dynamic live feed re-fetches.
"""

import json
import os
import re
from datetime import datetime

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
STORAGE_FILE = os.path.join(STORAGE_DIR, "soar_history.json")

def _normalize_title(text: str) -> str:
    """Normalizes headline text to allow fuzzy title matching across re-scraped feeds."""
    if not text:
        return ""
    return re.sub(r"[^a-zA-Z0-9]", "", text).lower()

def _ensure_storage():
    """Creates data directory and initial JSON file if not exists."""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    if not os.path.exists(STORAGE_FILE):
        initial_data = {
            "escalated_incidents": {},
            "approved_incidents": [],
            "audit_logs": [
                {
                    "timestamp": "2026-10-20 14:10:22 WIB",
                    "user": "Mayor Arh. Dedi (Pussiberad)",
                    "role": "Analis Siber (Pussiberad)",
                    "action": "DETEKSI INSIDEN",
                    "target": "THREAT-2026-ALPHA (Voice Clone Panglima)",
                    "status": "DRAFT DISUSUN",
                    "hash": "8f4a9b7c...21d0"
                },
                {
                    "timestamp": "2026-10-20 14:25:08 WIB",
                    "user": "Kapten Inf. Sarah (Dispenad)",
                    "role": "Komunikasi Publik / Penerangan (Dispenad)",
                    "action": "REVIEW NARASI KLARIFIKASI",
                    "target": "Infografis Side-by-Side Debunk",
                    "status": "TERVERIFIKASI DISPENAD",
                    "hash": "3d1b8e62...45a1"
                }
            ]
        }
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, indent=2, ensure_ascii=False)

def load_storage():
    """Loads complete storage dictionary from JSON file."""
    _ensure_storage()
    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"escalated_incidents": {}, "approved_incidents": [], "audit_logs": []}

def save_storage(data):
    """Saves storage dictionary to JSON file."""
    _ensure_storage()
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def get_escalated_incidents():
    """Returns dictionary of all escalated incidents (persisted)."""
    data = load_storage()
    return data.get("escalated_incidents", {})

def check_is_escalated(alert):
    """
    Checks if an alert is already escalated by ID or by normalized headline.
    Returns (True, record) or (False, None).
    """
    escalations = get_escalated_incidents()
    alert_id = alert.get("id")
    alert_headline = alert.get("headline", "")
    norm_headline = _normalize_title(alert_headline)
    
    # 1. Match by ID
    if alert_id and alert_id in escalations:
        return True, escalations[alert_id]
        
    # 2. Match by normalized headline
    if norm_headline:
        for item in escalations.values():
            item_title = item.get("headline", item.get("title", ""))
            if _normalize_title(item_title) == norm_headline:
                return True, item
                
    return False, None

def add_escalated_incident(soar_record):
    """Adds an incident to persistent storage and logs to audit trail."""
    data = load_storage()
    inc_id = soar_record["id"]
    data["escalated_incidents"][inc_id] = soar_record
    
    # Add audit log
    audit_entry = {
        "timestamp": soar_record.get("escalated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")),
        "user": soar_record.get("escalated_by", "Analis"),
        "role": soar_record.get("escalated_by", "Analis"),
        "action": "ESKALASI KE SOAR",
        "target": f"{inc_id} - {soar_record.get('headline', '')[:35]}...",
        "status": "MENUNGGU OTORISASI KOMANDAN",
        "hash": f"{inc_id.lower().replace('-', '')}e8a1"
    }
    data["audit_logs"].insert(0, audit_entry)
    save_storage(data)

def get_approved_incidents():
    """Returns set of approved incident IDs."""
    data = load_storage()
    return set(data.get("approved_incidents", []))

def mark_incident_approved(inc_id, approver_role="Komandan"):
    """Marks an incident as approved in persistent storage."""
    data = load_storage()
    if inc_id not in data["approved_incidents"]:
        data["approved_incidents"].append(inc_id)
        
    audit_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
        "user": f"Kolonel Bambang ({approver_role})",
        "role": approver_role,
        "action": "DIGITAL SIGNATURE APPROVAL",
        "target": inc_id,
        "status": "APPROVED & ENCRYPTED",
        "hash": f"{inc_id.lower().replace('-', '')}99f0"
    }
    data["audit_logs"].insert(0, audit_entry)
    save_storage(data)

def get_audit_logs():
    """Returns all audit logs from persistent storage."""
    data = load_storage()
    return data.get("audit_logs", [])
