import requests

BASE_URL = "http://127.0.0.1:5000"

def register_user(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"
    assert response.json() == {"email": email, "message": "user created"}, f"Unexpected response {response.json()}"

def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401, f"Unexpected status code {response.status_code}"

def log_in(email: str, password: str) -> str:
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"
    assert "session_id" in response.cookies, "Session ID not in cookies"
    return response.cookies["session_id"]

def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Unexpected status code {response.status_code}"

def profile_logged(session_id: str) -> None:
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"
    assert "email" in response.json(), "Email not in response"

def log_out(session_id: str) -> None:
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"

def reset_password_token(email: str) -> str:
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"
    assert "reset_token" in response.json(), "Reset token not in response"
    return response.json()["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    response = requests.put(f"{BASE_URL}/reset_password", data={"email": email, "reset_token": reset_token, "new_password": new_password})
    assert response.status_code == 200, f"Unexpected status code {response.status_code}"
    assert response.json() == {"email": email, "message": "Password updated"}, f"Unexpected response {response.json()}"

# Predefined constants for testing
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

