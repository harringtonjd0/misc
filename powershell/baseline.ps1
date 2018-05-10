param (
    [string]$outfile = "None"
)

if ( $outfile -eq "None" ) {
    

    

    if ( Test-Path "$HOME\Desktop\Baseline_Out\baseline_out1.txt") {
        
        
        write "`r`n[!] No output file specified, writing to $($HOME)\Desktop\Baseline_Out\baseline_out2.txt." 
        write "    To specify an output file, include '-outfile'.`r`n"
        $outfile = "$HOME\Desktop\Baseline_Out\baseline_out2.txt"
        sleep(4)
    }
    else {
        write "`r`n[!] No output file/directory specified."
        new-item -path "$HOME\Desktop\Baseline_Out\" -itemtype directory -erroraction SilentlyContinue | out-null
        write "[!] Created Directory $($HOME)\Desktop\Baseline_Out`r`n"
        sleep(1)
        
        write "`r`n[!] Writing to $($HOME)\Desktop\Baseline_Out\baseline_out1.txt. "
        write "    To specify an output file, include '-outfile'.`r`n"
        $outfile = "$HOME\Desktop\Baseline_Out\baseline_out1.txt"
        sleep(4)

    }

}

write "`nBaselining system..."
sleep(1)
write `r`n============================================================================================= | tee $outfile 
Get-Date | tee -append $outfile
write `r`n============================================================================================= | tee -append $outfile
write "`r`nHostname:  $($env:computername)" | tee -append $outfile

write "`r`nAll Users:`r`n---------------------------------------------------------------------------------------------" | tee -append $outfile
get-localuser | % { write "User: $($_.Name)" } | tee -append $outfile

write "`r`nAll Groups: `r`n --------------------------------------------------------------------------------------------" | tee -append $outfile
get-localgroup | % { write "Group: $($_.Name)" } | tee -append $outfile

write "`r`nLogged On Users:`r`n-------------------------------------------------------------------------------------------" | tee -append $outfile
(get-process -IncludeUserName "*" | where { $_.Processname -eq "explorer" }).UserName | tee -append $outfile

write "`r`nRunning Processes:`r`n-------------------------------------------------------------------------------------------"| tee -append $outfile
get-process | sort | format-table ProcessName, SI, ID | tee -append $outfile

write "`r`nServices:`r`n-------------------------------------------------------------------------------------------"  | tee -append $outfile
get-service | sort status -descending | format-table DisplayName, Name, Status  | tee -append $outfile

write "`r`nNetwork Information:`r`n-------------------------------------------------------------------------------------------"  | tee -append $outfile
gwmi win32_networkadapterconfiguration | where { $_.IPAddress -ne $null} | format-table IPAddress, DefaultIPGateway, IpSubnet,MACAddress  | tee -append $outfile
gwmi win32_networkadapterconfiguration | where { $_.IPAddress -ne $null} | format-table Description,DNSDomain  | tee -append $outfile

write "`r`nEstablished Connections:`r`n-------------------------------------------------------------------------------------------"  | tee -append $outfile
get-nettcpconnection | where { $_.State -ne "Listen" -and $_.RemotePort -ne 0} | format-table OwningProcess, LocalAddress, LocalPort, RemoteAddress, RemotePort, State  | tee -append $outfile

write "`r`n`r`nListening Network Sockets:`r`n-------------------------------------------------------------------------------------------" | tee -append $outfile
get-nettcpconnection -state Listen | format-table OwningProcess, LocalAddress, LocalPort, RemoteAddress, RemotePort, State | tee -append $outfile


write "`r`n`r`nSystem Information:`r`n-------------------------------------------------------------------------------------------" | tee -append $outfile
get-ciminstance win32_operatingsystem | select Caption, Version, InstallDate, ServicePackMajorVersion, OSArchitecture, BootDevice,  BuildNumber, CSName | FL | tee -append $outfile
 

$cpu = (get-ciminstance CIM_Processor).Name
"CPU  :  " + $cpu | tee -append $outfile

$computerHDD = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID = 'C:'" 

$hddcapacity = "{0:N2}" -f ($computerHDD.Size/1GB) + "GB"
"HDD Capacity  :  "  + $hddcapacity | tee -append $outfile

$hddspace = "{0:P2}" -f ($computerHDD.FreeSpace/$computerHDD.Size) + " Free (" + "{0:N2}" -f ($computerHDD.FreeSpace/1GB) + "GB)"
"HDD Space  :  " + $hddspace | tee -append $outfile
 
$ram = "{0:N2}" -f ((gwmi win32_computersystem).TotalPhysicalMemory/1GB) + "GB"
"RAM  :  " + $ram | tee -append $outfile
 
write "`r`n`r`nMapped Network Drives:`r`n-------------------------------------------------------------------------------------------" | tee -append $outfile
#gwmi win32_mappedlogicaldisk | select Name, ProviderName
Get-PSDrive -PSProvider filesystem| Select-Object Name, Root | tee -append $outfile

write "`r`n`r`nPlug and Play Devices:`r`n-------------------------------------------------------------------------------------------" | tee -append $outfile
get-pnpdevice | where { $_.Status -ne "Unknown" }  | format-table FriendlyName, Class, Status | tee -append $outfile

write "`r`n`r`nShares:`r`n-------------------------------------------------------------------------------------------" | tee -append $outfile
gwmi win32_share | tee -append $outfile

write "`r`n`r`nScheduled Tasks:`r`n-------------------------------------------------------------------------------------------" | tee -append $outfile
get-scheduledtask | sort State -Descending | format-table TaskName, State  | tee -append $outfile

write "`r`nOutput written to $($outfile)."
