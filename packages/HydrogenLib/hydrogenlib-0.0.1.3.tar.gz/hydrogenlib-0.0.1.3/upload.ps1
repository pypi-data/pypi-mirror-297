function Run-Command {
    param(
        [string]$command
    )
    try {
        & powershell.exe -Command $command
    }
    catch {
        Write-Host "Error running command: $command"
        Write-Host $_.Exception.Message
        return $false
    }
    return $true
}

# 执行构建命令
if ($args.Length -eq 1) {
    Run-Command "rm .\dist\*"
    Write-Host "Remove old files"
}

if (-not (Run-Command "hatch build")) {
    Write-Host "Build failed. Stopping."
}
elseif (-not (Run-Command "twine check dist/*")) {
    Write-Host "Check failed. Not uploading."
}
else {
    # 上传文件
    Run-Command "twine upload dist/*"
}
