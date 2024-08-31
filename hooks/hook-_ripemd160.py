from PyInstaller.utils.hooks import collect_dynamic_libs

# ripemdモジュールのネイティブライブラリを収集する
binaries = collect_dynamic_libs('ripemd')