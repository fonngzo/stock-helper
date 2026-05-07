import requests
from datetime import datetime, timedelta

TOKEN = "ff2ccc04b6264bc894d11cc2bd478a00"
URL = f"https://www.pushplus.plus/send?token={TOKEN}"


def get_idx():
    try:
        h = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://finance.qq.com'
        }
        r = requests.get(
            'https://qt.gtimg.cn/q=sh000001,sz399001,sz399006',
            headers=h, timeout=10
        )
        d = {}
        for l in r.text.strip().split('\n'):
            if '~' in l:
                p = l.split('~')
                if len(p) > 35:
                    c = p[2]
                    v = float(p[3]) if p[3] else 0
                    ch = float(p[32]) if p[32] else 0
                    if '000001' in c:
                        d['sh'] = {'v': v, 'c': ch}
                    elif '399001' in c:
                        d['sz'] = {'v': v, 'c': ch}
                    elif '399006' in c:
                        d['cy'] = {'v': v, 'c': ch}
        return d
    except:
        return {}


def brief():
    idx = get_idx()
    sh = idx.get('sh', {}).get('c', 0)
    t = max(0, min(100, int(30 + sh * 10)))
    pred = "强势" if sh > 1.5 else "偏强" if sh > 0.5 else \
        "震荡" if sh > -0.5 else "偏弱"
    pos = "7-9成" if sh > 1.5 else "6-7成" if sh > 0.5 else \
        "5-6成" if sh > -0.5 else "3-5成"
    y = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    msg = f"【{y}简报】\n\n【大盘】\n"
    msg += f"上证 {idx.get('sh',{}).get('v',0):.2f} "
    msg += f"({idx.get('sh',{}).get('c',0):+.2f}%)\n"
    msg += f"深证 {idx.get('sz',{}).get('v',0):.2f} "
    msg += f"({idx.get('sz',{}).get('c',0):+.2f}%)\n"
    msg += f"创业板 {idx.get('cy',{}).get('v',0):.2f} "
    msg += f"({idx.get('cy',{}).get('c',0):+.2f}%)\n"
    msg += f"温度 {t} | {pred}\n仓位 {pos}\n\n"
    msg += "【热点板块】\n"
    msg += "1 半导体 2 AI算力 3 新能源 4 军工 5 消费\n\n"
    msg += "仅供参考"
    try:
        r = requests.post(URL, json={"msg": msg}, timeout=10)
        print("OK" if r.json().get('code') == 0 else "FAIL")
    except Exception as e:
        print(f"ERR: {e}")


if __name__ == "__main__":
    brief()
