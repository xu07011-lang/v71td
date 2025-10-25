import base64
import hashlib
import json
import os
import platform
import random
import re
import string
import subprocess
import sys
import time
import urllib.parse
import uuid
from datetime import datetime, timedelta, timezone
from time import sleep

# Check and install necessary libraries
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    import pytz
    import requests
    from collections import Counter
    import statistics
except ImportError:
    print('__Đang cài đặt các thư viện cần thiết, vui lòng chờ...__')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "colorama", "pytz", "statistics"])
    print('__Cài đặt hoàn tất, vui lòng chạy lại Tool__')
    sys.exit()

# CONFIGURATION
FREE_CACHE_FILE = 'free_key_cache.json'
VIP_CACHE_FILE = 'vip_cache.json'
HANOI_TZ = pytz.timezone('Asia/Ho_Chi_Minh')
VIP_KEY_URL = "https://raw.githubusercontent.com/DUONGKP2401/keyxworkdf/main/keyxworkdf.txt"

# Encrypt and decrypt data using base64
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

# Colors for display
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
end = '\033[0m'

# Authentication banner
def authentication_banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner_text = f"""
████████╗██████╗░██╗░░██╗
╚══██╔══╝██╔══██╗██║░██╔╝
░░░██║░░░██║░░██║█████═╝░
░░░██║░░░██║░░██║██╔═██╗░
░░░██║░░░██████╔╝██║░╚██╗
░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝
══════════════════════════
Admin: DUONG phung
Tool xworld VTD
TIKTOK: @tdktool
══════════════════════════
"""
    for char in banner_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.0001)

# DEVICE ID AND IP ADDRESS FUNCTIONS
def get_device_id():
    """Generates a stable device ID based on CPU information."""
    system = platform.system()
    try:
        if system == "Windows":
            cpu_info = subprocess.check_output('wmic cpu get ProcessorId', shell=True, text=True, stderr=subprocess.DEVNULL)
            cpu_info = ''.join(line.strip() for line in cpu_info.splitlines() if line.strip() and "ProcessorId" not in line)
        else:
            try:
                cpu_info = subprocess.check_output("cat /proc/cpuinfo", shell=True, text=True)
            except:
                cpu_info = platform.processor()
        if not cpu_info:
            cpu_info = platform.processor()
    except Exception:
        cpu_info = "Unknown"

    hash_hex = hashlib.sha256(cpu_info.encode()).hexdigest()
    only_digits = re.sub(r'\D', '', hash_hex)
    if len(only_digits) < 16:
        only_digits = (only_digits * 3)[:16]

    return f"DEVICE-{only_digits[:16]}"

def get_ip_address():
    """Gets the user's public IP address."""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip_data = response.json()
        return ip_data.get('ip')
    except Exception as e:
        print(f"{do}Lỗi khi lấy địa chỉ IP: {e}{trang}")
        return None

def display_machine_info(ip_address, device_id):
    """Displays the banner, IP address, and Device ID."""
    authentication_banner()
    if ip_address:
        print(f"{trang}[{do}<>{trang}] {do}Địa chỉ IP: {vang}{ip_address}{trang}")
    else:
        print(f"{do}Không thể lấy địa chỉ IP của thiết bị.{trang}")

    if device_id:
        print(f"{trang}[{do}<>{trang}] {do}Mã Máy: {vang}{device_id}{trang}")
    else:
        print(f"{do}Không thể lấy Mã Máy của thiết bị.{trang}")

def save_vip_key_info(device_id, key, expiration_date_str):
    """Saves VIP key information to a local cache file."""
    data = {'device_id': device_id, 'key': key, 'expiration_date': expiration_date_str}
    encrypted_data = encrypt_data(json.dumps(data))
    with open(VIP_CACHE_FILE, 'w') as file:
        file.write(encrypted_data)
    print(f"{luc}Đã lưu thông tin Key VIP cho lần đăng nhập sau.{trang}")

def load_vip_key_info():
    """Loads VIP key information from the local cache file."""
    try:
        with open(VIP_CACHE_FILE, 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        return None

def display_remaining_time(expiry_date_str):
    """Calculates and displays the remaining time for a VIP key."""
    try:
        expiry_date = datetime.strptime(expiry_date_str, '%d/%m/%Y').replace(hour=23, minute=59, second=59)
        now = datetime.now()

        if expiry_date > now:
            delta = expiry_date - now
            days = delta.days
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"{xnhac}Key VIP của bạn còn lại: {luc}{days} ngày, {hours} giờ, {minutes} phút.{trang}")
        else:
            print(f"{do}Key VIP của bạn đã hết hạn.{trang}")
    except ValueError:
        print(f"{vang}Không thể xác định ngày hết hạn của key.{trang}")

def check_vip_key(machine_id, user_key):
    """Checks the VIP key from the URL on GitHub."""
    print(f"{vang}Đang kiểm tra Key VIP...{trang}")
    try:
        response = requests.get(VIP_KEY_URL, timeout=10)
        if response.status_code != 200:
            print(f"{do}Lỗi: Không thể tải danh sách key (Status code: {response.status_code}).{trang}")
            return 'error', None

        key_list = response.text.strip().split('\n')
        for line in key_list:
            parts = line.strip().split('|')
            if len(parts) >= 4:
                key_ma_may, key_value, _, key_ngay_het_han = parts

                if key_ma_may == machine_id and key_value == user_key:
                    try:
                        expiry_date = datetime.strptime(key_ngay_het_han, '%d/%m/%Y')
                        if expiry_date.date() >= datetime.now().date():
                            return 'valid', key_ngay_het_han
                        else:
                            return 'expired', None
                    except ValueError:
                        continue
        return 'not_found', None
    except requests.exceptions.RequestException as e:
        print(f"{do}Lỗi kết nối đến server key: {e}{trang}")
        return 'error', None
        
def seeded_shuffle_js_equivalent(array, seed):
    seed_value = 0
    for i, char in enumerate(seed):
        seed_value = (seed_value + ord(char) * (i + 1)) % 1_000_000_000
    def custom_random():
        nonlocal seed_value
        seed_value = (seed_value * 9301 + 49297) % 233280
        return seed_value / 233280.0
    shuffled_array = array[:]
    current_index = len(shuffled_array)
    while current_index != 0:
        random_index = int(custom_random() * current_index)
        current_index -= 1
        shuffled_array[current_index], shuffled_array[random_index] = shuffled_array[random_index], shuffled_array[current_index]
    return shuffled_array

def save_free_key_info(device_id, key, expiration_date):
    """Saves free key information to a json file based on device_id."""
    data = {device_id: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))
    with open(FREE_CACHE_FILE, 'w') as file:
        file.write(encrypted_data)

def load_free_key_info():
    """Loads free key information from the json file."""
    try:
        with open(FREE_CACHE_FILE, 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def check_saved_free_key(device_id):
    """Checks for a saved free key for the current device_id."""
    data = load_free_key_info()
    if data and device_id in data:
        try:
            expiration_date = datetime.fromisoformat(data[device_id]['expiration_date'])
            if expiration_date > datetime.now(HANOI_TZ):
                return data[device_id]['key']
        except (ValueError, KeyError):
            return None
    return None

def generate_free_key_and_url(device_id):
    """Creates a free key based on device_id and a URL to bypass the link."""
    today_str = datetime.now(HANOI_TZ).strftime('%Y-%m-%d')
    seed_str = f"TDK_FREE_KEY_{device_id}_{today_str}"
    hashed_seed = hashlib.sha256(seed_str.encode()).hexdigest()
    digits = [d for d in hashed_seed if d.isdigit()][:10]
    letters = [l for l in hashed_seed if 'a' <= l <= 'f'][:5]
    while len(digits) < 10:
        digits.extend(random.choices(string.digits))
    while len(letters) < 5:
        letters.extend(random.choices(string.ascii_lowercase))
    key_list = digits + letters
    shuffled_list = seeded_shuffle_js_equivalent(key_list, hashed_seed)
    key = "".join(shuffled_list)
    now_hanoi = datetime.now(HANOI_TZ)
    expiration_date = now_hanoi.replace(hour=21, minute=0, second=0, microsecond=0)
    url = f'https://tdkbumxkey.blogspot.com/2025/10/lay-link.html?m={key}'
    return url, key, expiration_date

def get_shortened_link_phu(url):
    """Shortens the link to get the free key."""
    try:
        token = "6725c7b50c661e3428736919"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={urllib.parse.quote(url)}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": f"Lỗi {response.status_code}: Không thể kết nối đến dịch vụ rút gọn URL."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi rút gọn URL: {e}"}

def process_free_key(device_id):
    """Handles the entire process of obtaining a free key based on device_id."""
    if datetime.now(HANOI_TZ).hour >= 21:
        print(f"{do}Đã qua 21:00 giờ Việt Nam, key miễn phí cho hôm nay đã hết hạn.{trang}")
        print(f"{vang}Vui lòng quay lại vào ngày mai để nhận key mới.{trang}")
        time.sleep(3)
        return False

    url, key, expiration_date = generate_free_key_and_url(device_id)
    shortened_data = get_shortened_link_phu(url)

    if shortened_data and shortened_data.get('status') == "error":
        print(f"{do}{shortened_data.get('message')}{trang}")
        return False

    link_key_shortened = shortened_data.get('shortenedUrl')
    if not link_key_shortened:
        print(f"{do}Không thể tạo link rút gọn. Vui lòng thử lại.{trang}")
        return False

    print(f'{trang}[{do}<>{trang}] {hong}Vui Lòng Vượt Link Để Lấy Key Free (Hết hạn 21:00 hàng ngày).{trang}')
    print(f'{trang}[{do}<>{trang}] {hong}Link Để Vượt Key Là {xnhac}: {link_key_shortened}{trang}')

    while True:
        keynhap = input(f'{trang}[{do}<>{trang}] {vang}Key Đã Vượt Là: {luc}')
        if keynhap == key:
            print(f'{luc}Key Đúng! Mời Bạn Dùng Tool{trang}')
            if datetime.now(HANOI_TZ) >= expiration_date:
                print(f"{do}Rất tiếc, key này đã hết hạn vào lúc 21:00. Vui lòng quay lại vào ngày mai.{trang}")
                return False
            time.sleep(2)
            save_free_key_info(device_id, keynhap, expiration_date)
            return True
        else:
            print(f'{trang}[{do}<>{trang}] {hong}Key Sai! Vui Lòng Vượt Lại Link {xnhac}: {link_key_shortened}{trang}')

def main_authentication():
    ip_address = get_ip_address()
    device_id = get_device_id()
    display_machine_info(ip_address, device_id)

    if not device_id:
        print(f"{do}Không thể lấy thông tin Mã Máy. Vui lòng kiểm tra lại thiết bị.{trang}")
        return False

    # 1. Prioritize checking for a saved VIP key
    cached_vip_info = load_vip_key_info()
    if cached_vip_info and cached_vip_info.get('device_id') == device_id:
        try:
            expiry_date = datetime.strptime(cached_vip_info['expiration_date'], '%d/%m/%Y')
            if expiry_date.date() >= datetime.now().date():
                print(f"{luc}Đã tìm thấy Key VIP hợp lệ, tự động đăng nhập...{trang}")
                display_remaining_time(cached_vip_info['expiration_date'])
                sleep(3)
                return True
            else:
                print(f"{vang}Key VIP đã lưu đã hết hạn. Vui lòng lấy hoặc nhập key mới.{trang}")
        except (ValueError, KeyError):
            print(f"{do}Lỗi file lưu key VIP. Vui lòng nhập lại key.{trang}")

    # 2. If no VIP key, check for a saved free key for the day
    if check_saved_free_key(device_id):
        expiry_str = f"21:00 ngày {datetime.now(HANOI_TZ).strftime('%d/%m/%Y')}"
        print(f"{trang}[{do}<>{trang}] {hong}Key free hôm nay vẫn còn hạn (Hết hạn lúc {expiry_str}). Mời bạn dùng tool...{trang}")
        time.sleep(2)
        return True

    # 3. If no key is saved, display the selection menu
    while True:
        print(f"{trang}========== {vang}MENU LỰA CHỌN{trang} ==========")
        print(f"{trang}[{luc}1{trang}] {xduong}Nhập Key VIP{trang}")
        print(f"{trang}[{luc}2{trang}] {xduong}Lấy Key Free (Hết hạn 21:00 hàng ngày){trang}")
        print(f"{trang}======================================")

        try:
            choice = input(f"{trang}[{do}<>{trang}] {xduong}Nhập lựa chọn của bạn: {trang}")
            print(f"{trang}═══════════════════════════════════")

            if choice == '1':
                vip_key_input = input(f'{trang}[{do}<>{trang}] {vang}Vui lòng nhập Key VIP: {luc}')
                status, expiry_date_str = check_vip_key(device_id, vip_key_input)

                if status == 'valid':
                    print(f"{luc}Xác thực Key VIP thành công!{trang}")
                    save_vip_key_info(device_id, vip_key_input, expiry_date_str)
                    display_remaining_time(expiry_date_str)
                    sleep(3)
                    return True
                elif status == 'expired':
                    print(f"{do}Key VIP của bạn đã hết hạn. Vui lòng liên hệ admin.{trang}")
                elif status == 'not_found':
                    print(f"{do}Key VIP không hợp lệ hoặc không tồn tại cho mã máy này.{trang}")
                else: 
                    print(f"{do}Đã xảy ra lỗi trong quá trình xác thực. Vui lòng thử lại.{trang}")
                sleep(2)

            elif choice == '2':
                return process_free_key(device_id)

            else:
                print(f"{vang}Lựa chọn không hợp lệ, vui lòng nhập 1 hoặc 2.{trang}")

        except KeyboardInterrupt:
            print(f"\n{trang}[{do}<>{trang}] {do}Cảm ơn bạn đã dùng Tool !!!{trang}")
            sys.exit()

NV={
    1:'Bậc thầy tấn công',
    2:'Quyền sắt',
    3:'Thợ lặn sâu',
    4:'Cơn lốc sân cỏ',
    5:'Hiếp sĩ phi nhanh',
    6:'Vua home run'
}

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def prints(r, g, b, text="text", end="\n"):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=end)

def banner(game):
    banner="""
████████╗██████╗░██╗░░██╗
╚══██╔══╝██╔══██╗██║░██╔╝
░░░██║░░░██║░░██║█████═╝░
░░░██║░░░██║░░██║██╔═██╗░
░░░██║░░░██████╔╝██║░╚██╗
░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝
    """
    for i in banner.split('\n'):
        x,y,z=200,255,255
        for j in range(len(i)):
            prints(x,y,z,i[j],end='')
            x-=4
            time.sleep(0.001)
        print()
    prints(247, 255, 97,"✨" + "═" * 45 + "✨")
    prints(32, 230, 151,f"🌟 XWORLD - {game} V7.PRO (FIXED & UPGRADED) 🌟".center(45))
    prints(247, 255, 97,"═" * 47)
    prints(7, 205, 240,"Telegram: @tankelo12")
    prints(7, 205, 240,"Nhóm Zalo: https://zalo.me/g/ddxsyp497")
    prints(7, 205, 240,"Admin: DUONG PHUNG")
    prints(247, 255, 97,"═" * 47)

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        prints(0, 255, 243,'Bạn có muốn sử dụng thông tin đã lưu hay không? (y/n): ',end='')
        x=input()
        if x.lower()=='y':
            with open('data-xw-cdtd.txt','r',encoding='utf-8') as f:
                return json.load(f)
        prints(247, 255, 97,"═" * 47)
    str="""
    Hướng dẫn lấy link:
    1. Truy cập vào trang web xworld.io
    2. Đăng nhập tài khoản của bạn
    3. Tìm và nhấn vào "Chạy đua tốc độ"
    4. Nhấn "Lập tức truy cập"
    5. Copy link trang web đó và dán vào đây
"""
    prints(218, 255, 125,str)
    prints(247, 255, 97,"═" * 47)
    prints(125, 255, 168,'📋 Nhập link của bạn:',end=' ')
    link=input()
    try:
        parsed_url = urllib.parse.urlparse(link)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        user_id = query_params.get('userId', [None])[0]
        user_secret_key = query_params.get('secretKey', [None])[0]

        if not user_id or not user_secret_key:
            prints(255, 0, 0, 'Link không hợp lệ, không tìm thấy userId hoặc secretKey.')
            return load_data_cdtd()

        prints(218, 255, 125,f'    User ID của bạn là: {user_id}')
        prints(218, 255, 125,f'    User Secret Key của bạn là: {user_secret_key}')
        json_data={
            'user-id':user_id,
            'user-secret-key':user_secret_key,
        }
        with open('data-xw-cdtd.txt','w+',encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        return json_data
    except Exception as e:
        prints(255, 0, 0, f"Lỗi xử lý link: {e}. Vui lòng thử lại.")
        return load_data_cdtd()

def top_100_cdtd(s):
    headers = {
        'accept': '*/*', 'accept-language': 'vi,en;q=0.9', 'origin': 'https://sprintrun.win',
        'priority': 'u=1, i', 'referer': 'https://sprintrun.win/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"', 'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
    }
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_100_issues', headers=headers, timeout=10).json()
        nv=[1,2,3,4,5,6]
        kq=[]
        for i in range(1,7):
            kq.append(response['data']['athlete_2_win_times'][str(i)])
        return nv,kq
    except Exception as e:
        prints(255,0,0,f'Lỗi khi lấy top 100: {e}. Thử lại...')
        time.sleep(5)
        return top_100_cdtd(s)

def top_10_cdtd(s, headers):
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=headers, timeout=10).json()
        ki=[]
        kq=[]
        for i in response['data']['recent_10']:
            ki.append(i['issue_id'])
            kq.append(i['result'][0])
        return ki,kq
    except Exception as e:
        prints(255,0,0,f'Lỗi khi lấy top 10: {e}. Thử lại...')
        time.sleep(5)
        return top_10_cdtd(s, headers)

def print_data(data_top10_cdtd,data_top100_cdtd):
    prints(247, 255, 97,"═" * 47)
    prints(0, 255, 250,"DỮ LIỆU 10 VÁN GẦN NHẤT:".center(50))
    for i in range(len(data_top10_cdtd[0])):
        prints(255,255,0,f'Kì {data_top10_cdtd[0][i]}: Người về nhất : {NV[int(data_top10_cdtd[1][i])]}')
    prints(247, 255, 97,"═" * 47)
    prints(0, 255, 250,"DỮ LIỆU 100 VÁN GẦN NHẤT:".center(50))
    for i in range(6):
        prints(255,255,0,f'{NV[int(i+1)]} về nhất {data_top100_cdtd[1][int(i)]} lần')
    prints(247, 255, 97,"═" * 47)

def selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0):
    """
    FIXED: Sửa lỗi logic chọn NV. Giờ sẽ tìm đúng NV ít xuất hiện nhất.
    """
    bet_amount = bet_amount0
    if len(htr) >= 1 and not htr[-1]['kq']:
        bet_amount = heso * htr[-1]['bet_amount']

    try:
        counts_10 = Counter(data_top10_cdtd[1])
        all_chars = list(range(1, 7))
        
        min_count_10 = min(counts_10.get(char, 0) for char in all_chars)
        
        least_common_10 = [char for char in all_chars if counts_10.get(char, 0) == min_count_10]
        x1 = random.choice(least_common_10)

        counts_100 = [int(x) for x in data_top100_cdtd[1]] 
        min_count_100 = min(counts_100)
        
        least_common_100 = [i + 1 for i, count in enumerate(counts_100) if count == min_count_100]
        x2 = random.choice(least_common_100)

        return random.choice([x1, x2]), bet_amount
    except Exception as e:
        prints(255,0,0,f'Lỗi khi chọn NV: {e}')
        return random.randint(1,6), bet_amount

def kiem_tra_kq_cdtd(s, headers,kq,ki):
    start_time = time.time()
    prints(0, 255, 37,f'Đang đợi kết quả của kì #{ki}')
    while True:
        try:
            data_top10_cdtd=top_10_cdtd(s, headers)
            if int(data_top10_cdtd[0][0])==int(ki):
                winner = int(data_top10_cdtd[1][0])
                prints(0, 255, 30,f'Kết quả kì {ki}: Người về nhất là {NV[winner]}')
                if winner == kq:
                    prints(255, 0, 0,'Bạn đã thua. Chúc bạn may mắn lần sau!')
                    return False
                else:
                    prints(0, 255, 37,'Xin chúc mừng. Bạn đã thắng!')
                    return True
            elapsed_time = time.time() - start_time
            prints(0, 255, 197,f'Đang đợi kết quả {elapsed_time:.0f}s...',end='\r')
            time.sleep(5)
        except Exception:
            prints(255, 0, 0, 'Lỗi mạng khi kiểm tra kết quả, thử lại sau 5s...', end='\r')
            time.sleep(5)

def user_asset(s, headers):
    try:
        json_data = {'user_id': int(headers['user-id']),'source': 'home'}
        response = s.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json=json_data, timeout=10).json()
        asset={'USDT':response['data']['user_asset']['USDT'],'WORLD':response['data']['user_asset']['WORLD'],'BUILD':response['data']['user_asset']['BUILD']}
        return asset
    except Exception as e:
        prints(255,0,0,f'Lỗi khi lấy số dư: {e}. Thử lại...')
        time.sleep(5)
        return user_asset(s, headers)

def print_stats_cdtd(stats, s, headers, Coin):
    try:
        current_assets = user_asset(s, headers)
        profit = current_assets[Coin] - stats['asset_0']
        
        prints(70, 240, 234,'Thống kê phiên:')
        prints(50, 237, 65,f"Số ván đã chơi: {stats['win'] + stats['lose']}")
        prints(50, 237, 65,f"Thắng/Thua: {stats['win']}/{stats['lose']}")
        prints(50, 237, 65,f"Chuỗi thắng hiện tại: {stats['streak']} (Cao nhất: {stats['max_streak']})")
        
        profit_color_r, profit_color_g, profit_color_b = (0, 255, 20) if profit >= 0 else (255, 0, 0)
        prints(profit_color_r, profit_color_g, profit_color_b, f"Lời/Lỗ: {profit:.4f} {Coin}")

    except Exception as e:
        prints(255,0,0,f'Lỗi khi in thống kê: {e}')

def print_wallet(asset):
    prints(23, 232, 159,f"Số dư:  USDT: {asset['USDT']:.2f} | WORLD: {asset['WORLD']:.2f} | BUILD: {asset['BUILD']:.2f}")

def bet_cdtd(s, headers,ki,kq,Coin,bet_amount):
    prints(255,255,0,f'Kì #{ki}: Đang đặt cược {bet_amount:.4f} {Coin} vào "{NV[kq]}" KHÔNG thắng.')
    try:
        json_data = { 'issue_id': int(ki), 'bet_group': 'not_winner', 'asset_type': Coin, 'athlete_id': kq, 'bet_amount': bet_amount }
        response = s.post('https://api.sprintrun.win/sprint/bet', headers=headers, json=json_data, timeout=10).json()
        
        if response.get('code') == 0 and response.get('msg') == 'ok':
            prints(0, 255, 19,f'==> Đặt cược thành công!')
        else:
            prints(255, 0, 0, f"==> Lỗi khi đặt cược: {response.get('msg', 'Không rõ lỗi')}")
            return False
        return True
    except Exception as e:
        prints(255,0,0,f'Lỗi khi gửi yêu cầu đặt cược: {e}')
        return False

def main_cdtd():
    s=requests.Session()
    banner("CHẠY ĐUA TỐC ĐỘ")
    data=load_data_cdtd()
    headers = {
        'accept': '*/*', 'accept-language': 'vi,en;q=0.9', 'cache-control': 'no-cache',
        'country-code': 'vn', 'origin': 'https://xworld.info', 'pragma': 'no-cache',
        'priority': 'u=1, i', 'referer': 'https://xworld.info/',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"', 'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'user-id': data['user-id'], 'user-login': 'login_v2', 'user-secret-key': data['user-secret-key'],
        'xb-language': 'vi-VN',
    }
    
    initial_asset = user_asset(s, headers)
    print_wallet(initial_asset)
    
    str_coin="""
    Chọn loại tiền bạn muốn chơi:
        1. USDT
        2. BUILD
        3. WORLD
    """
    prints(219, 237, 138,str_coin)
    coin_map = {'1': 'USDT', '2': 'BUILD', '3': 'WORLD'}
    while True:
        prints(125, 255, 168,'Nhập lựa chọn của bạn (1/2/3):',end=' ')
        choice = input()
        if choice in coin_map:
            Coin = coin_map[choice]
            break
        else:
            prints(247, 30, 30, 'Lựa chọn không hợp lệ, vui lòng nhập lại.', end='\r')
            time.sleep(1)

    while True:
        try:
            bet_amount0 = float(input(f'Nhập số {Coin} muốn đặt cho ván đầu tiên: '))
            if bet_amount0 > 0: break
            else: prints(255, 0, 0, "Số tiền cược phải lớn hơn 0.")
        except ValueError:
            prints(255, 0, 0, "Vui lòng nhập một con số hợp lệ.")
            
    while True:
        try:
            heso = float(input('Nhập hệ số cược sau mỗi ván thua (ví dụ: 2): '))
            if heso > 1: break
            else: prints(255, 0, 0, "Hệ số phải lớn hơn 1 để có lãi.")
        except ValueError:
            prints(255, 0, 0, "Vui lòng nhập một con số hợp lệ.")

    
    prints(32, 230, 151, "\n--- CÀI ĐẶT TÙY CHỌN (nhấn Enter để bỏ qua) ---")
    try:
        max_rounds = int(input('Sau bao nhiêu ván thì dừng hẳn?: ') or 0)
    except ValueError: max_rounds = 0
    
    try:
        take_profit = float(input(f'Chốt lời khi lãi bao nhiêu {Coin}?: ') or 0)
    except ValueError: take_profit = 0

    try:
        stop_loss = float(input(f'Cắt lỗ khi lỗ bao nhiêu {Coin}?: ') or 0)
    except ValueError: stop_loss = 0

    try:
        pause_after = int(input('Chơi bao nhiêu ván thì tạm nghỉ?: ') or 0)
    except ValueError: pause_after = 0

    pause_for = 0
    if pause_after > 0:
        try:
            pause_for = int(input('Nghỉ bao nhiêu ván rồi chơi tiếp?: ') or 1)
        except ValueError: pause_for = 1

    stats={'win':0, 'lose':0, 'streak':0, 'max_streak':0, 'asset_0': initial_asset[Coin]}
    htr=[]
    rounds_played = 0

    clear_screen()
    banner('CHẠY ĐUA TỐC ĐỘ')
    prints(247, 255, 97, "--- CÀI ĐẶT CỦA BẠN ---")
    prints(255, 255, 255, f"Loại tiền: {Coin}")
    prints(255, 255, 255, f"Mức cược ban đầu: {bet_amount0} {Coin}")
    prints(255, 255, 255, f"Hệ số thua: x{heso}")
    prints(255, 255, 255, f"Dừng sau: {'Vô hạn' if max_rounds == 0 else f'{max_rounds} ván'}")
    prints(255, 255, 255, f"Chốt lời: {'Không đặt' if take_profit == 0 else f'{take_profit} {Coin}'}")
    prints(255, 255, 255, f"Cắt lỗ: {'Không đặt' if stop_loss == 0 else f'{stop_loss} {Coin}'}")
    if pause_after > 0:
        prints(255, 255, 255, f"Nghỉ {pause_for} ván sau mỗi {pause_after} ván chơi")
    prints(247, 255, 97, "----------------------")
    prints(0, 255, 0, "Bot bắt đầu sau 5 giây...")
    time.sleep(5)

    while True:
        
        current_assets_check = user_asset(s, headers)
        current_profit = current_assets_check[Coin] - stats['asset_0']

        if max_rounds > 0 and rounds_played >= max_rounds:
            prints(0, 255, 37, f"Đã hoàn thành mục tiêu {max_rounds} ván. Dừng bot.")
            break
        if take_profit > 0 and current_profit >= take_profit:
            prints(0, 255, 37, f"Đã đạt mục tiêu chốt lời! Lãi: {current_profit:.4f} {Coin}. Dừng bot.")
            break
        if stop_loss > 0 and current_profit <= -stop_loss:
            prints(255, 0, 0, f"Đã chạm mốc cắt lỗ! Lỗ: {current_profit:.4f} {Coin}. Dừng bot.")
            break
        
        if pause_after > 0 and rounds_played > 0 and rounds_played % pause_after == 0:
            prints(255, 255, 0, f"Đã chơi {rounds_played} ván, tạm nghỉ {pause_for} ván theo cài đặt.")
            
            try:
                current_issue_id = top_10_cdtd(s, headers)[0][0]
                target_issue_id = current_issue_id + pause_for
                
                while current_issue_id < target_issue_id:
                    prints(255, 255, 0, f"Đang nghỉ... Ván hiện tại #{current_issue_id + 1}. Sẽ chơi lại ở ván #{target_issue_id + 1}.", end='\r')
                    time.sleep(20)
                    current_issue_id = top_10_cdtd(s, headers)[0][0]
                
                prints(0, 255, 37, "\nHết thời gian nghỉ. Tiếp tục chơi!")
            except Exception as e:
                prints(255, 0, 0, f"\nLỗi trong lúc nghỉ: {e}. Chờ 30s rồi tiếp tục.")
                time.sleep(30)
        
        prints(247, 255, 97,"═" * 47)
        current_assets = user_asset(s, headers)
        print_wallet(current_assets)
        print_stats_cdtd(stats,s,headers,Coin)

        data_top10_cdtd=top_10_cdtd(s, headers)
        data_top100_cdtd=top_100_cdtd(s)
        
        kq, bet_amount = selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0)
        
        if current_assets[Coin] < bet_amount:
            prints(255,0,0, f"Không đủ tiền để cược {bet_amount:.4f} {Coin}. Dừng bot.")
            break

        next_issue_id = data_top10_cdtd[0][0] + 1
        if not bet_cdtd(s, headers, next_issue_id, kq, Coin, bet_amount):
            prints(255, 0, 0, "Đặt cược thất bại, chờ 10s rồi thử lại ván tiếp theo.")
            time.sleep(10)
            continue
        
        result=kiem_tra_kq_cdtd(s, headers, kq, next_issue_id)
        
        if result is True:
            stats['win']+=1
            stats['streak']+=1
            stats['max_streak']=max(stats['max_streak'],stats['streak'])
            htr.append({'kq':True,'bet_amount':bet_amount0})
        elif result is False:
            stats['streak']=0
            stats['lose']+=1
            htr.append({'kq':False,'bet_amount':bet_amount})
        
        rounds_played += 1
        prints(173, 216, 230, "Đang chờ ván tiếp theo...")
        time.sleep(10)


if __name__ == "__main__":
    is_authenticated = main_authentication()

    if is_authenticated:
        print(f"\n{luc}>>>>> Xác thực thành công! Bắt đầu chạy tool... <<<<< {trang}")
        print(f"{trang}======================================================{trang}\n")
        time.sleep(2)
        try:
            main_cdtd()
        except KeyboardInterrupt:
            prints(255, 255, 0, "\nĐã dừng bot theo yêu cầu của người dùng.")
        except Exception as e:
            prints(255, 0, 0, f"\nMột lỗi không xác định đã xảy ra: {e}")
            
    else:
        print(f"\n{do}>>>>> Xác thực không thành công. Tool sẽ không được chạy. <<<<< {trang}")
        sys.exit()
