$ErrorActionPreference = 'Stop'
$revisionRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $revisionRoot
$documentPath = Join-Path $projectRoot 'IA trabalho 11.docx'
$pdfPath = Join-Path $revisionRoot 'IA trabalho 11 - completado.pdf'
$wordApp = $null
$wordDocument = $null
try {
    Write-Output 'A iniciar uma instancia isolada do Word.'
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $wordApp.AutomationSecurity = 3
    $wordDocument = $wordApp.Documents.Open($documentPath, $false, $false)
    Write-Output 'Documento aberto. A actualizar o indice.'
    if ($wordDocument.ReadOnly) {
        throw 'O Word abriu o documento em modo de leitura. A revisão não foi guardada.'
    }
    $tocCount = $wordDocument.TablesOfContents.Count
    for ($tocIndex = 1; $tocIndex -le $tocCount; $tocIndex++) {
        $wordDocument.TablesOfContents.Item($tocIndex).Update()
    }
    $wordDocument.Repaginate()
    for ($tocIndex = 1; $tocIndex -le $tocCount; $tocIndex++) {
        $wordDocument.TablesOfContents.Item($tocIndex).UpdatePageNumbers()
    }
    $wordDocument.Save()
    Write-Output 'Documento Word guardado. A gerar PDF com SaveAs2.'
    $pageCount = $wordDocument.ComputeStatistics(2)
    $wordDocument.SaveAs2($pdfPath, 17)
    Write-Output 'PDF guardado.'
    [pscustomobject]@{
        paginas = $pageCount
        indices_actualizados = $tocCount
        figuras = $wordDocument.InlineShapes.Count
        tabelas = $wordDocument.Tables.Count
        versao_word = $wordApp.Version
        documento = $documentPath
        pdf = $pdfPath
    } | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $revisionRoot 'paginacao_word.json')
    Write-Output "Documento paginado: $pageCount paginas; $tocCount indice(s) actualizado(s)."
    Write-Output $pdfPath
}
finally {
    if ($null -ne $wordDocument) {
        $wordDocument.Close(0)
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordDocument)
    }
    if ($null -ne $wordApp) {
        $wordApp.Quit()
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($wordApp)
    }
}
