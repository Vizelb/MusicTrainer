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

# Версии не пиним — берём те, что закреплены в рецептах p4a:
#   python3 3.14.2, kivy 2.3.1 (совпадает с десктопом), pygame 2.1.0, numpy 2.3.0
# Пин python3==3.10.0 убран: numpy собирается через meson-python,
# который требует Python >= 3.11 (см. docs/ANDROID.md).
requirements = python3,kivy,pygame,numpy

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
