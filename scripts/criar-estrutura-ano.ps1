# Solicita o ano ao usuário
$ano = Read-Host "Informe o ano (ex: 2026)"

# Diretório base (onde o script está sendo executado)
$basePath = Read-Host "Informe o caminho base (ex: G:\Meu Drive\cjmc\02.00. administrativo\02.03. rh\folha de pagamento)"
$anoPath = Join-Path $basePath $ano

# Lista de pastas do primeiro nível
$pastas = @(
    "01-jan",
    "02-fev",
    "03-mar",
    "04-abr",
    "05-mai",
    "06-jun",
    "07-jul",
    "08-ago",
    "09-set",
    "10-out",
    "11-nov",
    "12-dez",
    "13o",
    "ferias",
    "rescisao"
)

# Cria a pasta do ano se não existir
if (-not (Test-Path $anoPath)) {
    New-Item -Path $anoPath -ItemType Directory | Out-Null
    Write-Host "Pasta do ano criada: $ano"
} else {
    Write-Host "Pasta do ano já existe: $ano"
}

# Cria as pastas internas (somente primeiro nível)
foreach ($pasta in $pastas) {
    $pastaPath = Join-Path $anoPath $pasta

    if (-not (Test-Path $pastaPath)) {
        New-Item -Path $pastaPath -ItemType Directory | Out-Null
        Write-Host "Criada: $pasta"
    } else {
        Write-Host "Já existe (não recriada): $pasta"
    }
}

Write-Host "Estrutura verificada com sucesso."
