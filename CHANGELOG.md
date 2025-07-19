## Version 1.0.4 - 2025-07-19

### Fixed
- Resolved issue where `python3.11-venv` was not being installed, causing virtual environment creation to fail.




- Fixed `ERR_PNPM_NO_PKG_MANIFEST` error by ensuring correct copying of frontend and backend files.



- Fixed `ModuleNotFoundError: No module named 'src'` by setting `PYTHONPATH` in the installation script and systemd service.



- Fixed `ERR_PNPM_NO_PKG_MANIFEST` error by ensuring the frontend directory is created before copying files.



- Fixed `ERR_PNPM_NO_PKG_MANIFEST` error by moving the entire `ets2-panel-frontend` directory instead of copying its contents.

