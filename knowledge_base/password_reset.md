# Password Reset

## Problem
Users are locked out of their account, forgot their password, or need to change their password and are unsure of the correct process or its downstream effects on other tools.

## Common Symptoms
- "Incorrect password" errors despite entering the correct-seeming password
- Account locked after multiple failed attempts
- Password changed successfully but other apps (email, VPN, Teams) still reject the old password
- Password reset email/link not received

## Possible Causes
- Caps Lock or keyboard layout mismatch during entry
- Company password policy requires specific complexity not met by the new password
- Account temporarily locked due to failed attempt threshold
- Downstream systems (VPN, Wi-Fi, email client) have not yet synced the new password
- Password reset email delivered to spam/junk folder

## Troubleshooting Steps
1. Confirm Caps Lock is off and keyboard layout is correct before re-entering the password.
2. Use the self-service password reset portal on the company intranet (accessible from the login screen via "Forgot password").
3. Choose a new password meeting policy requirements: minimum 12 characters, at least one uppercase letter, one number, and one symbol.
4. Wait 10–15 minutes after resetting before trying dependent systems (VPN, email client, Wi-Fi) — these sync on a delay.
5. Update saved passwords in any local applications (Outlook, Wi-Fi profile, VPN client) to match the new password.
6. If account is locked, wait for the automatic unlock period (typically 30 minutes) or use the unlock option in the self-service portal.
7. Check spam/junk folder if the reset email has not arrived within 5 minutes.

## Resolution
Most password issues resolve by using the self-service reset portal and allowing a short sync delay before testing dependent systems.

## Warnings
- Never share your password with anyone, including IT staff, over email, chat, or phone.
- Do not reuse a previous password; the system will reject reused passwords from the last 5 changes.

## Escalation Conditions
- Escalate to IT security if the user suspects their account was accessed by someone else before the reset.
- Escalate if self-service reset repeatedly fails or the account remains locked after the standard unlock period.
- Escalate immediately if the password reset request appears to have originated from a suspicious email/link (see phishing_security.md) rather than the official portal.
