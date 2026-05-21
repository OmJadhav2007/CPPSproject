import requests
import streamlit as st
from typing import Optional, Dict, Any

BASE_URL = "http://localhost:8000"

def get_headers() -> Dict[str, str]:
    token = st.session_state.get("token", "")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def api_get(endpoint: str, params: Optional[Dict] = None) -> Optional[Any]:
    try:
        r = requests.get(f"{BASE_URL}{endpoint}", headers=get_headers(), params=params, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None

def api_post(endpoint: str, data: Dict) -> Optional[Any]:
    try:
        r = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=get_headers(), timeout=10)
        if r.status_code in (200, 201):
            return r.json()
        return None
    except Exception:
        return None

def api_put(endpoint: str, data: Dict) -> Optional[Any]:
    try:
        r = requests.put(f"{BASE_URL}{endpoint}", json=data, headers=get_headers(), timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None

def api_delete(endpoint: str) -> bool:
    try:
        r = requests.delete(f"{BASE_URL}{endpoint}", headers=get_headers(), timeout=10)
        return r.status_code == 200
    except Exception:
        return False

def login(email: str, password: str) -> Optional[Dict]:
    try:
        r = requests.post(
            f"{BASE_URL}/api/auth/token",
            data={"username": email, "password": password},
            timeout=10
        )
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None

def signup(email: str, username: str, password: str) -> Optional[Dict]:
    try:
        r = requests.post(
            f"{BASE_URL}/api/auth/signup",
            json={"email": email, "username": username, "password": password},
            timeout=10
        )
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None

def export_csv() -> Optional[bytes]:
    try:
        r = requests.get(f"{BASE_URL}/api/export/csv", headers=get_headers(), timeout=10)
        if r.status_code == 200:
            return r.content
        return None
    except Exception:
        return None
