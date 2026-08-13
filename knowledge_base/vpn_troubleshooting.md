# VPN Troubleshooting

## Problem
Users are unable to connect to the corporate VPN, or the VPN connects but then drops, especially after a recent password change.

## Common Symptoms
- VPN client shows "Authentication failed" after a password change
- VPN connects then disconnects within seconds
- VPN client hangs on "Connecting..."
- Internal resources (file shares, intranet) unreachable even though VPN shows "Connected"

## Possible Causes
- Cached old credentials are still being used by the VPN client
- Password was changed on the identity provider but not yet synced to the VPN gateway (sync delay, usually under 15 minutes)
- Local VPN client cache/config is corrupted
- Multi-factor authentication (MFA) token expired or not re-registered
- Outdated VPN client version incompatible with server policy

## Troubleshooting Steps
1. Confirm the new password works for standard company login (email, intranet) before touching the VPN.
2. Fully disconnect the existing VPN session (do not just minimize the client).
3. Clear cached VPN credentials:
   - Windows: open VPN client settings, remove the saved profile, or clear Credential Manager entries related to the VPN.
4. Restart the VPN client application (not just reconnect).
5. Reconnect using the new username and password.
6. If MFA is enabled, ensure you approve the push notification or enter a fresh code — do not reuse an old one.
7. If it still fails after 15 minutes, restart the machine to clear any locked network sessions.
8. Check VPN client version against the minimum supported version listed on the internal IT portal; update if outdated.

## Resolution
In most cases, clearing cached credentials and reconnecting with the new password resolves the issue immediately. If a sync delay is suspected, waiting 15 minutes and retrying typically resolves it without further action.

## Warnings
- Do not repeatedly attempt to log in with an old password — more than 5 failed attempts may lock the account.
- Do not disable MFA to "fix" a connection issue; this is a security control and must not be bypassed.

## Escalation Conditions
- Escalate to network/security team if VPN authentication still fails after credential refresh and a 15-minute wait.
- Escalate if the user reports the VPN client is prompting for unusual permissions or contacting an unfamiliar server (possible security concern).
- Escalate if account lockout occurs after multiple failed attempts.
