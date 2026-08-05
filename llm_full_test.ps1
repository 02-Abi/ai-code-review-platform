# llm_review_test.ps1
$username = "oviya"
$password = "admin123"
$baseUrl = "http://127.0.0.1:8000/api"

# REPLACE THIS WITH YOUR SUBMISSION ID FROM ADMIN PANEL
$submissionId = 1  # Change this to the ID you got from admin

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LLM REVIEW TEST" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

# 1. Login
Write-Host "`nLogging in..." -ForegroundColor Green
$body = @{ username = $username; password = $password } | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/token/" -Method Post -Body $body -ContentType "application/json" -ErrorAction Stop
    $token = $response.access
    $headers = @{ Authorization = "Bearer $token" }
    Write-Host "✅ Logged in!" -ForegroundColor Green
} catch {
    Write-Host "❌ Login failed: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# 2. Check submission exists
Write-Host "`nChecking submission..." -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/code-review/submissions/$submissionId/" -Method Get -Headers $headers -ErrorAction Stop
    Write-Host "✅ Submission found!" -ForegroundColor Green
    Write-Host "  ID: $($response.id)" -ForegroundColor Cyan
    Write-Host "  Language: $($response.language)" -ForegroundColor Cyan
    Write-Host "  Status: $($response.status)" -ForegroundColor Cyan
    Write-Host "  Code length: $($response.code.Length) characters" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Submission not found! Check the ID: $submissionId" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# 3. Start LLM review
Write-Host "`nStarting LLM review (10-15 seconds)..." -ForegroundColor Yellow

$body = @{
    submission_id = $submissionId
    use_llm = $true
    full_analysis = $true
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "$baseUrl/code-review/initiate-review/" -Method Post -Body $body -ContentType "application/json" -Headers $headers -ErrorAction Stop
    
    # 4. Show results
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "📊 LLM ANALYSIS RESULTS" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    
    Write-Host "`nQUALITY SCORE: $($response.quality_score)/100" -ForegroundColor $(if ($response.quality_score -ge 70) { "Green" } else { "Red" })
    
    Write-Host "`nSTATISTICS:" -ForegroundColor Cyan
    Write-Host "  Bugs Found: $($response.bugs_found)" -ForegroundColor Red
    Write-Host "  Issues Found: $($response.issues_found)" -ForegroundColor Yellow
    Write-Host "  Suggestions: $($response.suggestions)" -ForegroundColor Cyan
    Write-Host "  Syntax Errors: $($response.syntax_errors.count)" -ForegroundColor Magenta
    Write-Host "  LLM Used: $($response.analysis_metadata.llm_used)" -ForegroundColor Magenta
    Write-Host "  LLM Bugs Contribution: $($response.analysis_metadata.llm_bugs_contribution)" -ForegroundColor Magenta
    
    # Show bugs
    if ($response.bugs) {
        Write-Host "`n🐛 CRITICAL BUGS FOUND:" -ForegroundColor Red
        $response.bugs | ForEach-Object {
            Write-Host "  ─────────────────────────" -ForegroundColor Gray
            Write-Host "  Line: $($_.line)" -ForegroundColor White
            Write-Host "  Severity: $($_.severity)" -ForegroundColor Red
            Write-Host "  Source: $($_.source)" -ForegroundColor Gray
            Write-Host "  Description: $($_.description)" -ForegroundColor White
            Write-Host "  💡 Suggestion: $($_.suggestion)" -ForegroundColor Yellow
            Write-Host ""
        }
    }
    
    # Show issues
    if ($response.issues) {
        Write-Host "`n⚠️ ISSUES FOUND:" -ForegroundColor Yellow
        $response.issues | Select-Object -First 3 | ForEach-Object {
            Write-Host "  $($_.description)" -ForegroundColor White
            Write-Host "  💡 $($_.suggestion)" -ForegroundColor Cyan
            Write-Host ""
        }
        if ($response.issues.Count -gt 3) {
            Write-Host "  ... and $($response.issues.Count - 3) more issues" -ForegroundColor Gray
        }
    }
    
    # Show suggestions
    if ($response.suggestions) {
        Write-Host "`n💡 SUGGESTIONS:" -ForegroundColor Cyan
        $response.suggestions | Select-Object -First 3 | ForEach-Object {
            Write-Host "  $($_.description)" -ForegroundColor White
            Write-Host "  💡 $($_.suggestion)" -ForegroundColor Gray
            Write-Host ""
        }
        if ($response.suggestions.Count -gt 3) {
            Write-Host "  ... and $($response.suggestions.Count - 3) more suggestions" -ForegroundColor Gray
        }
    }
    
    # Show explanation
    if ($response.explanation) {
        Write-Host "`n📝 LLM SUMMARY:" -ForegroundColor Yellow
        Write-Host "────────────────────────────────────────────" -ForegroundColor Gray
        $explanation = $response.explanation
        if ($explanation.Length -gt 600) {
            Write-Host $explanation.Substring(0, 600) -ForegroundColor White
            Write-Host "... (full explanation in review)" -ForegroundColor Gray
        } else {
            Write-Host $explanation -ForegroundColor White
        }
    }
    
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "✅ LLM REVIEW COMPLETE!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ Review failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    # Try to get detailed error
    if ($_.Exception.Response) {
        try {
            $stream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($stream)
            $responseBody = $reader.ReadToEnd()
            Write-Host "`nError details:" -ForegroundColor Yellow
            Write-Host $responseBody -ForegroundColor Red
        } catch {
            Write-Host "Could not read error details" -ForegroundColor Gray
        }
    }
}