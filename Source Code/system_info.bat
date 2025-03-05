::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAnk
::fBw5plQjdCyDJGyX8VAjFDpQQQ2MNXiuFLQI5/rHy+WQrEESVeYsRIvUzbqCL+EXqg23PNgk1XU6
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdFy5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFDpQQQ2MNXiuFLQI5/rHy+WQrEESVeYsRK7X1vS9OfMH70ikXJgr2WhXmd8FAxUYL1yudgpU
::YB416Ek+ZW8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
:: Define output file
set OUTPUT_FILE=C:\system_info.txt

:: Clear previous file if exists
if exist %OUTPUT_FILE% del %OUTPUT_FILE%

:: Function to append command output
(
    echo ===============================
    echo System Information
    echo ===============================
    systeminfo

    echo ===============================
    echo Hostname
    echo ===============================
    hostname

    echo ===============================
    echo OS Version
    echo ===============================
    wmic os get caption

    echo ===============================
    echo CPU Info
    echo ===============================
    wmic cpu get name,NumberOfCores,NumberOfLogicalProcessors

    echo ===============================
    echo Memory Info
    echo ===============================
    wmic OS get FreePhysicalMemory,TotalVisibleMemorySize

    echo ===============================
    echo Disk Usage
    echo ===============================
    wmic logicaldisk get size,freespace,caption

    echo ===============================
    echo Network Configuration
    echo ===============================
    ipconfig /all

    echo ===============================
    echo Active Connections
    echo ===============================
    netstat -ano

    echo ===============================
    echo Routing Table
    echo ===============================
    route print

    echo ===============================
    echo DNS Lookup
    echo ===============================
    nslookup google.com

    echo ===============================
    echo Running Processes
    echo ===============================
    tasklist

    echo ===============================
    echo Installed Services
    echo ===============================
    sc query

    echo ===============================
    echo Firewall Rules
    echo ===============================
    netsh advfirewall firewall show rule name=all

    echo ===============================
    echo Last 10 System Logs
    echo ===============================
    wevtutil qe System /c:10 /f:text
) >> %OUTPUT_FILE%

:: Notify user
echo Report saved at %OUTPUT_FILE%
pause
