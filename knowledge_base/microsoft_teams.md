# Microsoft Teams Issues

## Problem
Microsoft Teams fails to open, crashes on launch, gets stuck loading, or has audio/video/call issues, often after a Windows update.

## Common Symptoms
- Teams shows a blank/white screen and never loads
- Teams crashes immediately on launch
- "We couldn't sign you in" error
- Camera or microphone not detected during calls
- Teams is extremely slow or unresponsive after a recent Windows update

## Possible Causes
- Corrupted local Teams cache after an update
- Outdated Teams client version incompatible with the new Windows update
- Conflicting background processes holding the microphone/camera
- Sign-in token expired or corrupted
- Insufficient system resources (see laptop_performance.md if the whole machine is slow, not just Teams)

## Troubleshooting Steps
1. Fully close Teams, including background processes (check Task Manager for any lingering `Teams.exe` or `ms-teams.exe` process and end it).
2. Clear the Teams cache:
   - Navigate to `%appdata%\Microsoft\Teams` and delete the contents of the `Cache`, `blob_storage`, and `GPUCache` folders (do not delete the whole Teams folder).
3. Restart the machine (this releases any locked camera/microphone handles).
4. Reopen Teams and sign in again.
5. Check for Teams updates: Profile picture → Check for updates.
6. If camera/mic issues persist, confirm no other app (Zoom, browser tab) is currently using the camera/microphone.
7. If the issue started right after a Windows update, check the internal IT portal for known compatibility issues with that specific update.

## Resolution
Clearing the Teams cache and restarting the machine resolves the majority of post-update Teams issues. Sign-in errors typically resolve after a fresh cache and re-authentication.

## Warnings
- Do not delete the entire `Microsoft\Teams` folder — this removes local settings and may require full reinstallation.
- Do not uninstall Teams without checking with IT first if it is centrally managed/deployed.

## Escalation Conditions
- Escalate if the issue affects multiple users after the same Windows update (likely a broader compatibility issue, not a single-machine fix).
- Escalate if sign-in fails with an authentication error unrelated to password (may indicate an identity/licensing issue).
- Escalate if camera/microphone issues persist across a full restart and no conflicting app is found (possible hardware/driver issue).
