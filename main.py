import re
import random
import string
import json
from datetime import datetime

# ==========================
# PASSWORD VALIDATION
# ==========================

def validate_password(password):
    if len(password) < 12:
        return False

    checks = [
        r"[A-Z]",
        r"[a-z]",
        r"\d",
        r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]"
    ]

    return all(re.search(pattern, password) for pattern in checks)

# ==========================
# PASSWORD STRENGTH SCORE
# ==========================

def calculate_strength(password):
    score = 0

    if len(password) >= 12:
        score += 25

    if any(c.isupper() for c in password):
        score += 20

    if any(c.islower() for c in password):
        score += 20

    if any(c.isdigit() for c in password):
        score += 15

    if any(not c.isalnum() for c in password):
        score += 20

    return min(score, 100)

# ==========================
# BLACKLIST CHECK
# ==========================

BLACKLIST = [
    "123456",
    "password",
    "qwerty",
    "admin",
    "letmein",
    "welcome"
]

def is_blacklisted(password):
    return password.lower() in BLACKLIST

# ==========================
# PASSWORD GENERATOR
# ==========================

def generate_password(length=16):
    chars = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*()"
    )

    return ''.join(
        random.choice(chars)
        for _ in range(length)
    )

# ==========================
# PASSWORD HISTORY
# ==========================

HISTORY_FILE = "passwords.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_password(password):
    history = load_history()

    if password not in history:
        history.append(password)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def password_used_before(password):
    history = load_history()
    return password in history

# ==========================
# MFA RECOMMENDATIONS
# ==========================

def mfa_advice(score):

    if score < 60:
        return [
            "Enable MFA",
            "Use Authenticator App",
            "Avoid SMS Authentication"
        ]

    return [
        "Password is Strong",
        "Still Enable MFA"
    ]

# ==========================
# SECURITY LOGGING
# ==========================

def log_event(event):

    with open("logs.txt", "a") as f:
        f.write(
            f"{datetime.now()} - {event}\n"
        )

# ==========================
# ATTACK SIMULATION
# ==========================

def simulate_attack(score):

    if score < 50:
        return "VULNERABLE"

    elif score < 80:
        return "MODERATE"

    return "STRONG"

# ==========================
# MAIN PROGRAM
# ==========================

print("=" * 50)
print("ADVANCED PASSWORD SECURITY SUITE")
print("=" * 50)

password = input("\nEnter Password: ")

valid = validate_password(password)

if not valid:
    print("\n❌ Password does not meet policy requirements")
    log_event("Weak Password Rejected")
    exit()

if is_blacklisted(password):
    print("\n⚠ Password Found in Blacklist")
    print("Risk Level: HIGH")
    log_event("Blacklist Password Attempt")
    exit()

if password_used_before(password):
    print("\n⚠ Password Reuse Detected")
    log_event("Password Reuse Attempt")
    exit()

score = calculate_strength(password)

print("\nPassword Score:", score, "/100")

if score <= 30:
    print("Rating: WEAK")
elif score <= 60:
    print("Rating: MEDIUM")
elif score <= 80:
    print("Rating: GOOD")
else:
    print("Rating: STRONG")

print("\nAttack Simulation:")
print(simulate_attack(score))

print("\nMFA Recommendations:")
for item in mfa_advice(score):
    print("-", item)

save_password(password)

log_event(
    f"Password Checked | Score={score}"
)

print("\nGenerated Secure Password:")
print(generate_password())

print("\n✅ Security Assessment Complete")
