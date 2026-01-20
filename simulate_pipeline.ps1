$companies = @("databricks.com", "snowflake.com", "confluent.io", "elastic.co", "mongodb.com")
$timestamp = "20260120T193000Z"
$rootDir = Get-Location

# Ensure directories exist
New-Item -ItemType Directory -Force -Path "$rootDir\data\metrics" | Out-Null

$allProcessedRecords = @()

foreach ($company in $companies) {
    Write-Host "Processing $company..."
    
    # 1. Simulate Raw Data
    $rawPath = "$rootDir\data\raw\$company\$timestamp"
    New-Item -ItemType Directory -Force -Path $rawPath | Out-Null
    
    $homeHtml = "<html><title>Home of $company</title><body><nav>Navbar content</nav><h1>Welcome to $company</h1><footer>Footer content</footer></body></html>"
    $homeHtml | Out-File -FilePath "$rawPath\homepage.html" -Encoding utf8
    
    # Simulate case study for some companies
    $hasCaseStudy = ($company.Length % 2 -eq 0) # Arbitrary logic
    if ($hasCaseStudy) {
        $csHtml = "<html><title>Case Study</title><body><h1>Success Story</h1><p>How Customer X used $company to win.</p></body></html>"
        $csHtml | Out-File -FilePath "$rawPath\case_study.html" -Encoding utf8
    }

    # 2. Simulate Processed Data
    $procPath = "$rootDir\data\processed\$company\$timestamp"
    New-Item -ItemType Directory -Force -Path $procPath | Out-Null
    
    $records = @(
        @{
            website = "https://www.$company"
            section = "navbar"
            content = "Navbar content"
            crawl_timestamp = $timestamp
            isActive = $true
        },
        @{
            website = "https://www.$company"
            section = "homepage"
            content = "Welcome to $company"
            crawl_timestamp = $timestamp
            isActive = $true
        },
        @{
            website = "https://www.$company"
            section = "footer"
            content = "Footer content"
            crawl_timestamp = $timestamp
            isActive = $true
        }
    )

    if ($hasCaseStudy) {
        $records += @{
            website = "https://www.$company"
            section = "case_study"
            content = "Success Story How Customer X used $company to win."
            crawl_timestamp = $timestamp
            isActive = $true
        }
    }
    
    $jsonContent = $records | ConvertTo-Json -Depth 5
    $jsonContent | Out-File -FilePath "$procPath\data.json" -Encoding utf8
    
    $allProcessedRecords += $records
}

# 3. Simulate Metrics Aggregation
Write-Host "Aggregating metrics..."
$metricsPath = "$rootDir\data\metrics\aggregation_$timestamp.json"

$websitesWithCS = ($allProcessedRecords | Where-Object { $_.section -eq 'case_study' }).website | Select-Object -Unique

$metrics = @{
    total_websites_crawled = $companies.Count
    websites_with_case_studies = $websitesWithCS.Count
    active_websites = $companies.Count
    content_length_stats = @{
        homepage = @{
            avg_length = 20 # Dummy
            count = $companies.Count
        }
        case_study = @{
            avg_length = 50 # Dummy
            count = $websitesWithCS.Count
        }
    }
}

$metrics | ConvertTo-Json -Depth 5 | Out-File -FilePath $metricsPath -Encoding utf8

Write-Host "Simulation Complete! Data generated in data/raw, data/processed, and data/metrics."
