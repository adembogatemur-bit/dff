# media_control.py
# Videoyu/müziği durdurma-oynatma, sonraki/önceki parça — herhangi bir
# uygulamada (YouTube, Spotify, Netflix vb.) çalışan medyayı kontrol eder.

import keyboard


def medya_oynat_durdur() -> str:
    keyboard.send("play/pause media")
    return "Oynat/durdur."


def sonraki_parca() -> str:
    keyboard.send("next track")
    return "Sonraki parçaya geçiliyor."


def onceki_parca() -> str:
    keyboard.send("previous track")
    return "Önceki parçaya dönülüyor."
