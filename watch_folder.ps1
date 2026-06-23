# --- CONFIGURATION ---
$WatchFolder = "C:\path\to\folder" # Folder to watch
$PythonScript = "C:\path\to\apple_to_quicken.py"       # Path to your python script
$OutputFolder = "C:\path\to\imports"  # Where to save the result

# Ensure folders exist
If (!(Test-Path $WatchFolder)) { New-Item -ItemType Directory -Force -Path $WatchFolder }
If (!(Test-Path $OutputFolder)) { New-Item -ItemType Directory -Force -Path $OutputFolder }

Write-Host "Monitoring folder: $WatchFolder" -ForegroundColor Cyan
Write-Host "Press CTRL+C to stop watching." -ForegroundColor Yellow

# Setup watcher
$Watcher = New-Object System.IO.FileSystemWatcher $WatchFolder, "*.csv"
$Watcher.IncludeSubdirectories = $false

# The polling loop
while ($true) {
    # Wait for a file to be created (checks every 1000ms)
    $Result = $Watcher.WaitForChanged([System.IO.WatcherChangeTypes]::Created, 1000)
    
    if ($Result.TimedOut -eq $false) {
        $FileName = $Result.Name
        $FilePath = Join-Path $WatchFolder $FileName
        $OutputFile = Join-Path $OutputFolder "quicken_$FileName"
        
        Write-Host "--- DETECTED: $FileName ---" -ForegroundColor Yellow
        
        # Simple loop wait to ensure the file is done writing
        while ($true) {
            try {
                $Stream = [System.IO.File]::Open($FilePath, 'Open', 'Read', 'None')
                $Stream.Close()
                break # Success, file is fully written and free!
            } catch {
                Start-Sleep -Seconds 1 # Wait 1 second before trying again
            }
        }
        
        Write-Host "Processing with Python..." -ForegroundColor Cyan
        
        # Execute python script
        python $PythonScript "$FilePath" "$OutputFile"
        
        # Verify and clean up
        if (Test-Path $OutputFile) {
            Write-Host "Success! Converted to: quicken_$FileName" -ForegroundColor Green
            Remove-Item $FilePath -Force
            Write-Host "Original cleaned up." -ForegroundColor Gray
        } else {
            Write-Host "ERROR: Output file was not created. Double check your Python script." -ForegroundColor Red
        }
        Write-Host "------------------------------------" -ForegroundColor Yellow
    }
}
