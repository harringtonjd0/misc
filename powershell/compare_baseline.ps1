param (
       [string]$first = "$HOME\Desktop\Baseline_Out\baseline_out1.txt",
       [string]$second = "$HOME\Desktop\Baseline_Out\baseline_out2.txt",
       [string]$outfile = "$HOME\Desktop\Baseline_Out\baseline_comparison.txt"
)


   new-item $outfile -ErrorAction SilentlyContinue | out-null
 
if (! (test-path $outfile)) {
 
    write "`r`n[!]  Error opening output file $($outfile). "
    write "[!]  Please specify the output file with ' -outfile' or run baseline.ps1 to create output files."
    break
 } 
 if ($first -eq "$HOME\Desktop\Baseline_Out\baseline_out1.txt" -and $second -eq "$HOME\Desktop\Baseline_Out\baseline_out2.txt") {
      write "`r`n`r`n[!] No comparison files specified, attempting to compare files `n   - $($first) and`n   - $($second).`r`n" 
      write "To specify baseline files, use '-first' and ' -second '.`r`n" 
      sleep(3)
    }

write "Comparing baselines...`r`n" 
sleep(1)
Try {
    $first_content = cat $first 
    $second_content = cat $second
 }
Catch {
    write "[!] Error opening  $($_.Exception.ItemName):`r`n"
    write "      -----> $($_.Exception.Message)`r`n"
    write "[!] Terminating comparison, please specify baseline files or run baseline script to create them.`r`n"
    break
}
$compare = compare-object $($first_content) $($second_content)
write "`r`n`r`nIn $($first):`r`n-------------------------------------------------------------------------------------------`r`n"  | tee $outfile
$compare | % { if ( $_.SideIndicator -eq "<=" ) { $_.InputObject } }  | tee -append $outfile

write "`r`n`r`nIn $($second):`r`n-------------------------------------------------------------------------------------------`r`n"  | tee -append $outfile
$compare | % { if ( $_.SideIndicator -eq "=>" ) { $_.InputObject } }  | tee -append $outfile

write "`r`nComparison output written to $($outfile)."