# Apple Card CSV export to Quicken import

## Problem

Apple Card transaction export to CSV doesn't match required format for Quicken import CSV. 

### Manual usage

1. **`apple_to_quicken.py`**: Converts CSV output from Apple Card export to Quicken required CSV import format. Clears out default categories to let Quicken handle assignments locally.

`python apple_to_quicken.py transaction-export quicken-import`

### Automated usage

2. **`watch_folder.ps1`**: The monitoring agent running a synchronous polling loop. It uses .NET file streams to ensure incoming downloads are completely written and unlocked by Windows before calling the Python processor.
3. **Windows Task Scheduler**: The persistence layer that automatically initializes the script invisibly behind the scenes whenever the machine boots up and logs in.

---

## Setting up automation

### 1. Script Configuration
* Place `apple_to_quicken.py` and `watch_folder.ps1` into your preferred environment directories.
* Update the configuration paths at the top of `watch_folder.ps1` to reflect your specific download watcher and Quicken storage paths.

### 2. Task Scheduler Registry
To install the background agent without dealing with the Windows Task Scheduler GUI sorting or validation anomalies, open an **Administrator PowerShell** session and execute the registration block provided in the deployment codebase.

This establishes a task named **"Apple Card Watcher Loop"** configured with:
* **Trigger**: Launch automatically at user logon.
* **Execution Options**: Run with highest privileges to avoid OS blocks.
* **Visibility**: Uses the `-WindowStyle Hidden` argument to run silently as a background process.
* **VM Compatibility**: Overrides the default Windows AC power requirements so it never falls asleep or fails to initialize on a virtual machine.

### 3. Verification & Maintenance
* **Status Checks**: Run `Get-ScheduledTask -TaskName "Apple Card Watcher Loop"` to check status. When active, it will report as `Running`.
* **Process Tracking**: The loop runs under a silent instance of `Windows PowerShell` viewable inside Windows Task Manager's *Background processes* view.
* **Manual Cycling**: The engine can be restarted at any point via PowerShell using `Stop-ScheduledTask` followed by `Start-ScheduledTask`.
