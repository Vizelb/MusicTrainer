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

# ВОЗВРАЩАЕМСЯ К KIVY 2.1.0 И PYTHON 3.10
requirements = python3==3.10.0,kivy==2.1.0,pygame==2.6.1,numpy

hostpython3 = /usr/local/bin/python3.10  # <-- ИЗМЕНЕНО

p4a.local_recipes = ./p4a-recipes

orientation = portrait

android.permissions = INTERNET, VIBRATE, RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, BLUETOOTH, BLUETOOTH_CONNECT, BLUETOOTH_SCAN

android.api = 31
android.minapi = 24
android.ndk_api = 24
android.sdk = 33
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
