# Prueba opcional para una sesión funcional de Microsoft Excel en Windows.
# Abre una instancia oculta, recalcula y compara las mismas entradas del modelo.
# Si Office no responde, registra el error; no simula un recálculo exitoso.
$ErrorActionPreference = 'Stop'
$raizLaboratorio = Split-Path -Parent $PSScriptRoot
$archivoBoleta = Join-Path $raizLaboratorio 'Excel\Boleta_Pago_Semana09.xlsx'
$archivoSalida = Join-Path $raizLaboratorio 'evidencias\excel_recalculado.json'
$excelLaboratorio = $null
$libroLaboratorio = $null
try {
    $excelLaboratorio = New-Object -ComObject Excel.Application
    $excelLaboratorio.Visible = $false
    $excelLaboratorio.DisplayAlerts = $false
    $libroLaboratorio = $excelLaboratorio.Workbooks.Open($archivoBoleta)
    $excelLaboratorio.CalculateFullRebuild()
    $casosLaboratorio = $libroLaboratorio.Worksheets.Item('Casos')
    $fixturesLaboratorio = Get-Content -LiteralPath (Join-Path $raizLaboratorio 'Tests\fixtures.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    $resultadosLaboratorio = @()
    for ($filaLaboratorio = 4; $filaLaboratorio -lt 4 + $fixturesLaboratorio.Count; $filaLaboratorio++) {
        $valoresLaboratorio = @()
        for ($columnaLaboratorio = 10; $columnaLaboratorio -le 23; $columnaLaboratorio++) {
            $valorLaboratorio = $casosLaboratorio.Cells.Item($filaLaboratorio,$columnaLaboratorio).Value2
            if ($valorLaboratorio -isnot [double]) { throw "Excel devolvió un error en fila $filaLaboratorio columna $columnaLaboratorio : $valorLaboratorio" }
            $valoresLaboratorio += $valorLaboratorio.ToString('F2',[Globalization.CultureInfo]::InvariantCulture)
        }
        $resultadosLaboratorio += @{ name = $fixturesLaboratorio[$filaLaboratorio-4].name; values = $valoresLaboratorio }
    }
    $pruebasFormulario = @()
    $boletaLaboratorio = $libroLaboratorio.Worksheets.Item('Boleta')
    foreach ($fixtureLaboratorio in $fixturesLaboratorio) {
        $iLaboratorio = $fixtureLaboratorio.input
        $boletaLaboratorio.Range('B4').Value2 = [double]::Parse($iLaboratorio.sueldo,[Globalization.CultureInfo]::InvariantCulture)
        $boletaLaboratorio.Range('B5').Value2 = [double]$iLaboratorio.dias
        $boletaLaboratorio.Range('B6').Value2 = $(if ($iLaboratorio.hijos) { [string][char]0x53 + [char]0xED } else { 'No' })
        $boletaLaboratorio.Range('B7').Value2 = $iLaboratorio.sistema
        $boletaLaboratorio.Range('B8').Value2 = $iLaboratorio.afp
        $boletaLaboratorio.Range('B9').Value2 = [double]::Parse($iLaboratorio.horas25,[Globalization.CultureInfo]::InvariantCulture)
        $boletaLaboratorio.Range('B10').Value2 = [double]::Parse($iLaboratorio.horas35,[Globalization.CultureInfo]::InvariantCulture)
        $boletaLaboratorio.Range('B11').Value2 = [double]::Parse($iLaboratorio.adelantos,[Globalization.CultureInfo]::InvariantCulture)
        $excelLaboratorio.CalculateFullRebuild()
        $valoresLaboratorio = @()
        for ($filaLaboratorio=17; $filaLaboratorio -le 30; $filaLaboratorio++) {
            $valorLaboratorio = $boletaLaboratorio.Cells.Item($filaLaboratorio,2).Value2
            if ($valorLaboratorio -isnot [double]) { throw "Boleta sin resultado para $($fixtureLaboratorio.name): $valorLaboratorio" }
            $valoresLaboratorio += $valorLaboratorio.ToString('F2',[Globalization.CultureInfo]::InvariantCulture)
        }
        $pruebasFormulario += @{name=$fixtureLaboratorio.name; values=$valoresLaboratorio}
    }
    $boletaLaboratorio.Range('B5').Value2 = [double]31
    $excelLaboratorio.CalculateFullRebuild()
    if ($boletaLaboratorio.Range('B13').Value2 -eq 'OK' -or $boletaLaboratorio.Range('B28').Value2 -ne '') { throw 'La validacion de dias no bloqueo el calculo' }
    # Restaurar caso 1 para entregar el libro abierto en un estado reproducible.
    $boletaLaboratorio.Range('B4').Value2 = [double]2500
    $boletaLaboratorio.Range('B5').Value2 = [double]30
    $boletaLaboratorio.Range('B6').Value2 = 'No'
    $boletaLaboratorio.Range('B7').Value2 = 'ONP'
    $boletaLaboratorio.Range('B8').Value2 = 'Ejemplo'
    $boletaLaboratorio.Range('B9:B11').Value2 = [double]0
    $excelLaboratorio.CalculateFullRebuild()
    $libroLaboratorio.Save()
    @{engine='Microsoft Excel COM'; version=$excelLaboratorio.Version; cases=$resultadosLaboratorio; form=$pruebasFormulario; invalidDaysBlocked=$true} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $archivoSalida -Encoding UTF8
    Write-Output "Excel recalculado: $($resultadosLaboratorio.Count) casos y formulario; dias invalidos bloqueados."
} catch {
    $errorOriginalLaboratorio = $_ | Out-String
    Set-Content -LiteralPath (Join-Path $raizLaboratorio 'evidencias\excel_com_error.txt') -Value $errorOriginalLaboratorio -Encoding UTF8
    throw
} finally {
    if ($null -ne $libroLaboratorio) {
        try { $libroLaboratorio.Close($false) } catch { Write-Warning 'Excel rechazo Close; revisar la sesion de Office.' }
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($libroLaboratorio)
    }
    if ($null -ne $excelLaboratorio) {
        try { $excelLaboratorio.Quit() } catch { Write-Warning 'Excel rechazo Quit; revisar la sesion de Office.' }
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($excelLaboratorio)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
