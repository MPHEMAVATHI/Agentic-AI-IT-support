# Phishing & Security Incidents

## Problem
A user has received a suspicious email, clicked a suspicious link, entered credentials on an unfamiliar page, or suspects their account/device has been compromised.

## Common Symptoms
- Email asking to "verify your password" or "reset your account" from an unfamiliar or slightly-off sender address
- User clicked a link and was taken to a login page requesting their corporate credentials
- User entered their username/password on a page they now suspect was not legitimate
- Unusual account activity (logins from unfamiliar locations, unexpected password reset emails)
- Unexpected pop-ups or requests for MFA approval the user did not initiate

## Possible Causes
- Targeted or mass phishing campaign impersonating IT, Microsoft, or a known vendor
- Credential-harvesting page designed to look like the company login portal
- Malware delivered via a malicious attachment or link

## Troubleshooting Steps
**This category is NOT a standard self-service troubleshooting flow.** The steps below are containment actions, not a full resolution — a security incident of this type must always go through human review.

1. Do not click any further links in the suspicious email.
2. Do not enter any further credentials anywhere until instructed by security/IT.
3. If credentials were already entered on a suspicious page, treat the account as potentially compromised immediately.
4. Note the sender address, subject line, and approximate time the email was received/link was clicked, for the security team's investigation.
5. Disconnect the device from the network (or VPN) if malware execution is suspected, to limit potential spread.

## Resolution
There is no automatic self-service resolution for phishing or credential-compromise incidents. The account should have its password reset immediately by IT/security, active sessions should be revoked, and the security team should investigate before the user resumes normal access.

## Warnings
- Never treat a phishing report as a routine password reset — the exposed account may already be compromised.
- Do not tell the user "you're fine" without security review, even if nothing appears wrong yet.
- Do not attempt to "clean up" or personally investigate the phishing email's link/attachment.

## Escalation Conditions
- **Always escalate.** Any ticket involving a suspicious email, a clicked phishing link, or credentials entered on an unfamiliar site must be routed to the security team for human review — this is never auto-resolved.
- Escalate as high severity/urgent regardless of how calm or minor the user's description sounds.
- Escalate immediately if the user reports unusual account activity in addition to the phishing exposure.
