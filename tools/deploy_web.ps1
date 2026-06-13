# 『雨の終わりに』Ren'Py版を Web書き出しして GitHub Pages(gh-pagesブランチ) に公開する。
# 使い方: powershell -ExecutionPolicy Bypass -File deploy_web.ps1
# 前提: renpy-sdk に web サポート導入済み(renpy-sdk\web)。未導入なら
#   https://www.renpy.org/dl/<version>/renpy-<version>-web.zip を展開して renpy-sdk\web に置く。

$ErrorActionPreference = 'Stop'
$sdk  = 'C:\Users\user\Downloads\renpy-sdk'
$py   = "$sdk\lib\py3-windows-x86_64\python.exe"
$proj = 'C:\Users\user\Downloads\ame-no-owarini\renpy\AmeNoOwariNi'
$web  = 'C:\Users\user\Downloads\ame-web'        # Web書き出し先
$dep  = "$env:TEMP\ame_ghpages_deploy"           # gh-pages 用作業ディレクトリ
$repo = 'https://github.com/sakurasaku1213/ame-no-owarini.git'

Write-Host '== Web書き出し ==' -ForegroundColor Cyan
if (Test-Path $web) { Remove-Item $web -Recurse -Force }
& $py "$sdk\renpy.py" "$sdk\launcher" web_build $proj --destination $web
if (-not (Test-Path "$web\index.html")) { throw 'web_build に失敗(index.html なし)' }

Write-Host '== gh-pages へ配置 ==' -ForegroundColor Cyan
if (Test-Path $dep) { Remove-Item $dep -Recurse -Force }
New-Item -ItemType Directory -Force $dep | Out-Null
Copy-Item "$web\*" $dep -Recurse -Force
New-Item -ItemType File -Path "$dep\.nojekyll" -Force | Out-Null

Set-Location $dep
git init -b gh-pages -q
git config user.name  'sakurasaku1213'
git config user.email '208340787+sakurasaku1213@users.noreply.github.com'
git add -A
git commit -q -m ("Ren'Py Web版を更新 " + (Get-Date -Format 'yyyy-MM-dd'))
git remote add origin $repo
git push -f -u origin gh-pages

Write-Host '== 完了: https://sakurasaku1213.github.io/ame-no-owarini/ ==' -ForegroundColor Green
