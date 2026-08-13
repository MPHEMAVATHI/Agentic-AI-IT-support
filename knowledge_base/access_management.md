# Access Management (Shared Folders & Permissions)

## Problem
Users are unable to access a shared folder, drive, SharePoint site, or application they need for their work — either they never had access, lost access, or access was revoked.

## Common Symptoms
- "Access Denied" error when opening a shared folder or SharePoint site
- Folder/drive is visible but contents fail to load
- Access worked previously but stopped after a team/role change
- New employee has no access to team resources on day one

## Possible Causes
- User was never added to the required security group
- User's role/department changed and old group membership was removed without new access being granted
- Folder/site permissions were recently restructured
- Access request was submitted but not yet approved by the resource owner
- User is trying to access the resource from an unapproved device or network

## Troubleshooting Steps
1. Confirm the exact resource name and path the user is trying to access (e.g. "Finance shared folder" — get the precise folder name).
2. Check whether the user has an approved access request on file via the internal access management portal.
3. If no request exists, the user should submit an access request specifying the resource and business justification; this typically requires manager or resource-owner approval.
4. If access was previously granted but recently stopped working, check whether the user's team/role changed recently — this may have triggered automatic group membership changes.
5. Confirm the user is connected via an approved network (VPN or office network) if the resource is restricted to internal access only.
6. Once approval is granted, allow up to 30 minutes for permission changes to propagate before retrying.

## Resolution
Access issues are resolved through the formal access request and approval process — IT support cannot directly grant access to sensitive shared resources (like Finance folders) without owner/manager approval, even for troubleshooting purposes.

## Warnings
- IT support must never bypass or directly modify permissions on sensitive folders (Finance, HR, Legal) without going through the formal approval workflow.
- Do not share personal credentials or access with another user to work around a permissions issue.

## Escalation Conditions
- Always escalate access requests for sensitive folders (Finance, HR, Legal, Payroll) to the resource owner for manual approval — this cannot be automatically resolved.
- Escalate if a user reports losing access unexpectedly with no known role change (possible account or security issue).
- Escalate if multiple users report the same access problem simultaneously (possible broader permissions misconfiguration).
