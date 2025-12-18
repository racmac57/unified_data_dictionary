# Release v0.2.1 — Maintenance & Cleanup

**Date:** 2025-12-18

## Summary
- **Data Cleanup**: Executed `scripts/cleanup_duplicates.ps1` on `KB_Shared\04_output` — removed ~6,000 duplicate/redundant files and retained only the newest timestamped folder per processing group.
- **Backup Verification**: Confirmed integrity of key backups (e.g., `SYNC\ssocc_desk` (70GB) and `02_ETL_Scripts`).
- **Docs Updated**: `CHANGELOG.md`, `README.md`, `SUMMARY.md` updated to document cleanup and verification.
- **Script Updates**: Bumped `scripts/Process_UDD_Chatlog.bat` to **v1.0.7** (atomic staging) and added cleanup utilities (`cleanup_duplicates.ps1`, `list_duplicate_outputs.ps1`, `cleanup_duplicate_outputs.ps1`).

## Notes
- Tag `v0.2.1` points to commit `2f3d9ba` which contains the changes referenced above.

## Actions you can take next
1. Update the GitHub Release notes body using this file (manual paste or via `gh` or the REST API).
2. Upload `release_notes.md` as a release asset (via API) if you want the file attached.
3. Ask me to call the GitHub REST API to update the release if you provide a token.

---

Maintained by: R. A. Carucci
Repository: https://github.com/racmac57/unified_data_dictionary
