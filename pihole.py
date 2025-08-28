
import requests
import os
from dotenv import load_dotenv
from PIL import ImageDraw, ImageFont

load_dotenv()

PIHOLE_URL = os.getenv("PIHOLE_URL", "http://192.168.178.99")
PIHOLE_PASSWORD = os.getenv("PIHOLE_PASSWORD", "")

_PIHOLE_SID = None
_PIHOLE_SID_EXPIRES = None
import time

def get_pihole_sid():
    global _PIHOLE_SID, _PIHOLE_SID_EXPIRES
    now = time.time()
    # Reuse SID if it exists and is not expired (assume 10 min lifetime)
    if _PIHOLE_SID and _PIHOLE_SID_EXPIRES and now < _PIHOLE_SID_EXPIRES:
        return _PIHOLE_SID
    try:
        resp = requests.post(f"{PIHOLE_URL}/api/auth", json={"password": PIHOLE_PASSWORD})
        print(f"/api/auth status: {resp.status_code}")
        print(f"/api/auth content: {resp.text}")
        resp.raise_for_status()
        data = resp.json()
        sid = data.get("session", {}).get("sid")
        if sid:
            _PIHOLE_SID = sid
            _PIHOLE_SID_EXPIRES = now + 600  # 10 minutes
        else:
            print("Failed to get Pi-hole SID: no sid in response")
        return sid
    except Exception as e:
        print(f"Error authenticating with Pi-hole: {e}")
        return None

def get_pihole_stats():
    global _PIHOLE_SID, _PIHOLE_SID_EXPIRES
    def fetch_stats(sid):
        headers = {"X-FTL-SID": sid}
        resp = requests.get(f"{PIHOLE_URL}/api/stats/summary", headers=headers)
        print(f"/api/stats/summary status: {resp.status_code}")
        print(f"/api/stats/summary content: {resp.text}")
        resp.raise_for_status()
        stats = resp.json()
        resp2 = requests.get(f"{PIHOLE_URL}/api/dns/blocking", headers=headers)
        print(f"/api/dns/blocking status: {resp2.status_code}")
        print(f"/api/dns/blocking content: {resp2.text}")
        resp2.raise_for_status()
        blocking = resp2.json()
        return stats, blocking

    sid = get_pihole_sid()
    if not sid:
        return {
            "queries_today": "-",
            "ads_blocked_today": "-",
            "ads_percentage_today": "-",
            "domains_blocked": "-",
            "status": "error"
        }
    try:
        try:
            stats, blocking = fetch_stats(sid)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code in (401, 403):
                # SID invalid, clear cache and retry once
                _PIHOLE_SID = None
                _PIHOLE_SID_EXPIRES = None
                sid = get_pihole_sid()
                if not sid:
                    raise
                stats, blocking = fetch_stats(sid)
            else:
                raise
        percent_blocked = stats.get("queries", {}).get("percent_blocked", 0.0)
        percent_blocked = f"{percent_blocked:.1f}" if isinstance(percent_blocked, (float, int)) else percent_blocked
        domains_blocked = stats.get("gravity", {}).get("domains_being_blocked")
        if not domains_blocked or domains_blocked == 0:
            domains_blocked = "-"
        blocking_status = blocking.get("blocking")
        status = "EN" if blocking_status == "enabled" else "OFF"
        return {
            "queries_today": stats.get("queries", {}).get("total", 0),
            "ads_blocked_today": stats.get("queries", {}).get("blocked", 0),
            "ads_percentage_today": percent_blocked,
            "domains_blocked": domains_blocked,
            "status": status
        }
    except Exception:
        return {
            "queries_today": "-",
            "ads_blocked_today": "-",
            "ads_percentage_today": "-",
            "domains_blocked": "-",
            "status": "error"
        }

def draw_pihole_stats(draw: ImageDraw.Draw, x, y, width, height, stats, font):
    # Draw rectangle border
    draw.rectangle([x, y, x+width, y+height], outline=0, width=2)
    # Left column: Q, Blk, %Blk
    left_labels = [
        ("Q", stats["queries_today"]),
        ("Blk", stats["ads_blocked_today"]),
        ("%Blk", stats["ads_percentage_today"])
    ]
    # Right column: Dom, Sts
    right_labels = [
        ("Dom", stats["domains_blocked"]),
        ("Sts", stats["status"])
    ]
    label_y = y + 8
    for i, (label, value) in enumerate(left_labels):
        draw.text((x+10, label_y), f"{label}: {value}", font=font, fill=0)
        label_y += font.size + 2
    # Place Dom and Sts to the right, aligned with first and second row
    right_x = x + width // 2 + 5
    right_y1 = y + 8
    right_y2 = right_y1 + font.size + 2
    draw.text((right_x, right_y1), f"Dom: {stats['domains_blocked']}", font=font, fill=0)
    draw.text((right_x, right_y2), f"Sts: {stats['status']}", font=font, fill=0)
