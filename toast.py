# toast.py
# Windows bildirim balonu (sağ alttaki küçük pop-up). plyer kurulu değilse
# ya da başarısız olursa sessizce atlanır — program hiçbir zaman bu yüzden
# çökmez.

def bildirim_goster(baslik: str, mesaj: str):
    try:
        from plyer import notification
        notification.notify(title=baslik, message=mesaj, app_name="Friday", timeout=6)
    except Exception:
        pass
