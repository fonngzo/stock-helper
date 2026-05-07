import requests
from datetime import datetime, timedelta
TOKEN = "ff2ccc04b6264bc894d11cc2bd478a00"
URL = f"https://www.pushplus.plus/send?token={TOKEN}"
def get():
    try:
        h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com'}
        r = requests.get('https://qt.gtimg.cn/q=sh000001,sz399001,sz399006', headers=h, timeout=10)
        d = {}
        for l in r.text.strip().split('\n'):
            if '~' in l:
                p = l.split('~')
                if len(p) > 35:
                    c, v = p[2], float(p[3]) if p[3] else 0
                    ch = float(p[32]) if p[32] else 0
                    if '000001' in c: d['sh'] = {'v': v, 'c': ch}
                    elif '399001' in c: d['sz'] = {'v': v, 'c': ch}
                    elif '399006' in c: d['cy'] = {'v': v, 'c': ch}
        return d
    except: return {}
def b():
    i = get()
    sh = i.get('sh', {}).get('c', 0)
    y = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    m = f"{y}\n上证 {i.get('sh',{}).get('v',0):.2f} ({i.get('sh',{}).get('c',0):+.2f}%)\n深证 {i.get('sz',{}).get('v',0):.2f} ({i.get('sz',{}).get('c',0):+.2f}%)\n创业板 {i.get('cy',{}).get('v',0):.2f} ({i.get('cy',{}).get('c',0):+.2f}%)"
    try:
        r = requests.post(URL, json={"msg": m}, timeout=10)
        print("OK" if r.json().get('code') == 0 else "FAIL")
    except Exception as e: print(f"ERR: {e}")
if __name__ == "__main__": b()
