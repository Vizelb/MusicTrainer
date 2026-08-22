[app]

title = MusicTrainer
package.name = musictrainer
package.domain = org.niknitro
version = 17.5

source.dir = src
source.include_exts = py,png,jpg,kv,atlas,json,md
source.exclude_exts = spec,db,pyc,pyo
source.exclude_dirs = tests, __pycache__, .git, .buildozer, to_delete_backup
source.include_patterns = exercises/*, screens/*, core/*, ui/*

# Два пина обязательны, остальное берётся из рецептов p4a (kivy 2.3.1, numpy 2.3.0).
#
# python3==3.12.11 — по умолчанию p4a собирает 3.14.2, но pygame под 3.14
#   не собирается вообще. Верхняя граница pygame — 3.12/3.13.
#   Нижняя граница — 3.11: numpy собирается через meson-python, который
#   требует Python >= 3.11. Остаётся окно 3.11-3.13, берём 3.12.
#
# pygame==2.6.1 — рецепт p4a пинует 2.1.0 (2021), а он падает на
#   'longintrepr.h' file not found: этот заголовок убрали из публичного
#   API CPython в 3.11. 2.6.1 совпадает с версией на десктопе.
#
# hostpython3 обязан совпадать по версии с python3, иначе p4a прерывает сборку:
#   "python3 should have same version as hostpython3, 3.12.11 != 3.14.2"
#
# Подробности всех трёх ошибок — в docs/ANDROID.md.
requirements = hostpython3==3.12.11,python3==3.12.11,kivy,pygame==2.6.1,numpy

# Кастомные рецепты p4a-recipes/ удалены: рецепт kivy 2.3.1 сам настраивает
# SDL2 и графику под Android, а hostpython3 больше не нужно подменять.

orientation = portrait

android.permissions = INTERNET, VIBRATE, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, BLUETOOTH, BLUETOOTH_CONNECT, BLUETOOTH_SCAN

android.api = 31
android.minapi = 24
android.ndk_api = 24
# android.sdk — устаревший ключ, buildozer его игнорирует, используется android.api
android.ndk = 28c
android.build_tools = 33.0.2
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True
android.auto_sign = True
android.accept_sdk_license = True

android.graphics = gles2
android.gles_version = 2

[buildozer]

log_level = 2
build_dir = ./.buildozer
bin_dir = ./bin
