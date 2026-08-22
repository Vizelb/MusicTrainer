FROM python:3.12-slim

# Python 3.12, а не 3.10: numpy собирается через meson-python, который
# требует Python >= 3.11. На 3.10 сборка падала с
# "meson-python: error: The package requires Python version >=3.11".

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ANDROID_HOME=/home/builder/.buildozer/android/platform/android-sdk \
    ANDROID_SDK_ROOT=/home/builder/.buildozer/android/platform/android-sdk

RUN apt-get update && apt-get install -y \
    git zip unzip wget curl make \
    default-jdk \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    cmake libffi-dev libssl-dev \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libgl1-mesa-dev \
    portaudio19-dev \
    libblas-dev liblapack-dev gfortran \
    patchelf \
    ninja-build \
    sudo \
    && rm -rf /var/lib/apt/lists/* && apt-get clean

RUN git config --global http.postBuffer 524288000 && \
    git config --global http.lowSpeedLimit 0 && \
    git config --global http.lowSpeedTime 999999

# python-for-android сюда намеренно не ставится: buildozer игнорирует
# установленный пакет и клонирует p4a сам (см. p4a.branch в buildozer.spec).
# Cython <= 3.0.12 — верхняя граница, которую требует рецепт kivy 2.3.1.
RUN pip install --no-cache-dir \
    buildozer==1.6.0 \
    setuptools \
    wheel \
    cython==0.29.37

RUN useradd -m -u 1000 builder \
    && mkdir -p /home/builder/.buildozer \
    && mkdir -p /home/builder/.android \
    && touch /home/builder/.buildozer/default.spec \
    && echo "### User Sources for Android SDK Manager" > /home/builder/.android/repositories.cfg \
    && chown -R builder:builder /home/builder \
    && chmod -R 755 /home/builder \
    && echo "builder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER builder
WORKDIR /app

RUN git config --global --add safe.directory '*' \
    && git config --global user.email "builder@local" \
    && git config --global user.name "Builder" \
    && git config --global http.postBuffer 524288000

ENV TERM=xterm-256color
