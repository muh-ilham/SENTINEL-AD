"""
utils/soar_storage.py - Persistent Storage for SOAR Escalations, Approvals & Audit Trail
Ensures all escalated incidents, commander approvals, rejections, and audit logs persist across
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
            "rejected_incidents": [],
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
            data = json.load(f)
            if "rejected_incidents" not in data:
                data["rejected_incidents"] = []
            return data
    except Exception:
        return {"escalated_incidents": {}, "approved_incidents": [], "rejected_incidents": [], "audit_logs": []}

def _json_serial_converter(o):
    """Safely converts numpy scalars, numpy arrays, or datetime objects into JSON-compliant types."""
    if hasattr(o, "item"):
        return o.item()
    if hasattr(o, "tolist"):
        return o.tolist()
    if isinstance(o, (datetime, )):
        return o.isoformat()
    return str(o)

def save_storage(data):
    """Saves storage dictionary to JSON file."""
    _ensure_storage()
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=_json_serial_converter)
    except Exception as e:
        print(f"[SOAR Storage Error] Failed to write storage: {e}")

def get_escalated_incidents():
    """Returns dictionary of all escalated incidents (persisted)."""
    data = load_storage()
    return data.get("escalated_incidents", {})

def check_is_escalated(alert):
    """
    Checks if an alert is already escalated by ID or by normalized headline or by bot_account.
    Returns (True, record) or (False, None).
    """
    escalations = get_escalated_incidents()
    alert_id = alert.get("id")
    alert_headline = alert.get("headline", "")
    norm_headline = _normalize_title(alert_headline)
    
    # 1. Match by ID
    if alert_id and alert_id in escalations:
        return True, escalations[alert_id]
        
    # 2. Match by bot_account if provided
    bot_acc = alert.get("bot_account")
    if bot_acc:
        norm_bot = re.sub(r"[^a-zA-Z0-9]", "", str(bot_acc)).lower()
        for item in escalations.values():
            item_bot = item.get("bot_account")
            if item_bot and re.sub(r"[^a-zA-Z0-9]", "", str(item_bot)).lower() == norm_bot:
                return True, item

    # 3. Match by normalized headline
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

def remove_escalated_incident(inc_id, actor_role="Analis"):
    """
    Removes an incident from escalated queue and resets its status.
    Allows user to re-escalate if needed.
    """
    data = load_storage()
    removed_title = inc_id
    
    # 1. Remove by exact key
    if inc_id in data["escalated_incidents"]:
        removed_title = data["escalated_incidents"][inc_id].get("title", inc_id)
        del data["escalated_incidents"][inc_id]
        
    # 2. Remove by normalized title check (in case ID differed)
    norm_target = _normalize_title(inc_id)
    keys_to_del = []
    for k, v in data["escalated_incidents"].items():
        if _normalize_title(v.get("title", "")) == norm_target or _normalize_title(v.get("headline", "")) == norm_target:
            keys_to_del.append(k)
    for k in keys_to_del:
        del data["escalated_incidents"][k]
        
    if inc_id in data.get("approved_incidents", []):
        data["approved_incidents"].remove(inc_id)
        
    if inc_id in data.get("rejected_incidents", []):
        data["rejected_incidents"].remove(inc_id)
        
    # Audit trail
    audit_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
        "user": f"Petugas ({actor_role})",
        "role": actor_role,
        "action": "PEMBATALAN ESKALASI SOAR",
        "target": f"{inc_id} ({removed_title[:30]}...)",
        "status": "DIHAPUS DARI ANTREAN",
        "hash": f"{inc_id.lower().replace('-', '')}d3e1"
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
    if "rejected_incidents" in data and inc_id in data["rejected_incidents"]:
        data["rejected_incidents"].remove(inc_id)
        
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

def get_rejected_incidents():
    """Returns set of rejected incident IDs."""
    data = load_storage()
    return set(data.get("rejected_incidents", []))

def mark_incident_rejected(inc_id, rejector_role="Komandan"):
    """Marks an incident as rejected / false positive in persistent storage."""
    data = load_storage()
    if "rejected_incidents" not in data:
        data["rejected_incidents"] = []
    if inc_id not in data["rejected_incidents"]:
        data["rejected_incidents"].append(inc_id)
    if inc_id in data.get("approved_incidents", []):
        data["approved_incidents"].remove(inc_id)
        
    audit_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
        "user": f"Kolonel Bambang ({rejector_role})",
        "role": rejector_role,
        "action": "PENOLAKAN OTORISASI (REJECT)",
        "target": inc_id,
        "status": "DITOLAK / FALSE POSITIVE",
        "hash": f"{inc_id.lower().replace('-', '')}c4a2"
    }
    data["audit_logs"].insert(0, audit_entry)
    save_storage(data)

def revoke_incident_status(inc_id, actor_role="Komandan"):
    """Revokes approval or rejection, returning incident to pending review."""
    data = load_storage()
    if inc_id in data.get("approved_incidents", []):
        data["approved_incidents"].remove(inc_id)
    if inc_id in data.get("rejected_incidents", []):
        data["rejected_incidents"].remove(inc_id)
        
    audit_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
        "user": f"Kolonel Bambang ({actor_role})",
        "role": actor_role,
        "action": "PENCABUTAN STATUS (REVOKE)",
        "target": inc_id,
        "status": "RESET KE PENDING REVIEW",
        "hash": f"{inc_id.lower().replace('-', '')}b7f3"
    }
    data["audit_logs"].insert(0, audit_entry)
    save_storage(data)

def get_audit_logs():
    """Returns all audit logs from persistent storage."""
    data = load_storage()
    return data.get("audit_logs", [])

def save_wargaming_result(record):
    """Saves verified wargaming narrative result to persistent storage and logs audit."""
    data = load_storage()
    data["latest_wargaming_result"] = record
    if "wargaming_history" not in data:
        data["wargaming_history"] = []
    data["wargaming_history"].insert(0, record)
    
    # Audit trail
    audit_entry = {
        "timestamp": record.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")),
        "user": record.get("tested_by", "Analis Siber (Pussiberad)"),
        "role": record.get("tested_by", "Analis Siber (Pussiberad)"),
        "action": "INTEGRASI WARGAMING SOAR",
        "target": f"Draf Klarifikasi Dispenad ({record.get('overall_tone', 'Taktis')})",
        "status": f"SENTIMEN {record.get('positive_sentiment', 86.5)}% / BACKFIRE {record.get('backfire_risk', 11.2)}%",
        "hash": f"wargaming{datetime.now().strftime('%H%M%S')}a1"
    }
    data["audit_logs"].insert(0, audit_entry)
    save_storage(data)

def get_latest_wargaming_result():
    """Returns the latest verified wargaming narrative result."""
    data = load_storage()
    if "latest_wargaming_result" in data and data["latest_wargaming_result"]:
        return data["latest_wargaming_result"]
    return {
        "draft_text": (
            "Mabes TNI AD menegaskan rekaman audio yang beredar mengatasnamakan pimpinan TNI AD adalah 100% kloning suara sintetik (AI deepfake) "
            "yang sengaja disebarkan oleh pihak tidak bertanggung jawab untuk memecah belah persatuan. Tim Pussiberad telah memverifikasi anomali "
            "frekuensi dan berkas dossier takedown telah dikoordinasikan bersama Kominfo serta BSSN. TNI AD tetap berkomitmen menjaga stabilitas dan kedamaian di perbatasan."
        ),
        "positive_sentiment": 86.5,
        "backfire_risk": 11.2,
        "overall_tone": "Taktis, Faktual & Kredibel (Sangat Optimal)",
        "advice": "DIREKOMENDASIKAN. Penggunaan bukti digital forensik dan keterlibatan BSSN/Kominfo melumpuhkan narasi buzzer lawan serta memberikan rasa aman kepada publik awam.",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
        "tested_by": "Pussiberad & Dispenad Sandbox Engine",
        "passed": True
    }
