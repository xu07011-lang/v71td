import threading
import base64
import os
import time
import re
import requests
import socket
import sys
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
from collections import Counter, defaultdict
from urllib.parse import urlparse, parse_qs
import random
import math
import platform
import subprocess
import hashlib
import statistics
import urllib.parse
import string

# Check and install necessary libraries
try:
    from faker import Faker
    from requests import session
    from colorama import Fore, Style, init
    import pystyle
    init(autoreset=True)
except ImportError:
    os.system("pip install faker requests colorama bs4 pystyle rich")
    os.system("pip3 install requests pysocks")
    print('__Vui Lòng Chạy Lại Tool__')
    sys.exit()

# --- DO NOT CHANGE ---
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
    str_guide="""
    Hướng dẫn lấy link:
    1. Truy cập vào trang web xworld.io
    2. Đăng nhập tài khoản của bạn
    3. Tìm và nhấn vào "Chạy đua tốc độ"
    4. Nhấn "Lập tức truy cập"
    5. Copy link trang web đó và dán vào đây
"""
    prints(218, 255, 125,str_guide)
    prints(247, 255, 97,"═" * 47)
    prints(125, 255, 168,'📋 Nhập link của bạn:',end=' ')
    link=input()
    try:
        parsed_url = urllib.parse.urlparse(link)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        user_id = query_params.get('userId', [None])[0]
        user_secretkey = query_params.get('secretKey', [None])[0]

        if not user_id or not user_secretkey:
            prints(255, 0, 0, 'Link không hợp lệ, không tìm thấy userId hoặc secretKey.')
            return load_data_cdtd()

        prints(218, 255, 125,f'    User ID của bạn là: {user_id}')
        prints(218, 255, 125,f'    User Secret Key của bạn là: {user_secretkey}')
        json_data={
            'user-id':user_id,
            'user-secret-key':user_secretkey,
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
            # Dữ liệu API trả về số lần thắng của NV 1-6 trong 100 ván gần nhất.
            # athlete_2_win_times có key là '1' đến '6'
            kq.append(response['data']['athlete_2_win_times'][str(i)])
        return nv,kq
    except Exception as e:
        prints(255,0,0,f'Lỗi khi lấy top 100: {e}. Thử lại...')
        time.sleep(5)
        return top_100_cdtd(s)

def top_10_cdtd(s, headers):
    try:
        # Sử dụng headers có sẵn (có user-id, secret-key) để đảm bảo không bị lỗi nếu API yêu cầu
        response = s.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=headers, timeout=10).json()
        ki=[]
        kq=[]
        for i in response['data']['recent_10']:
            ki.append(i['issue_id'])
            # result[0] là ID của người về nhất
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
        # data_top100_cdtd[1][i] là số lần thắng của NV i+1
        prints(255,255,0,f'{NV[int(i+1)]} về nhất {data_top100_cdtd[1][int(i)]} lần')
    prints(247, 255, 97,"═" * 47)

def selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0):
    """
    Sửa lỗi logic chọn NV. Giờ sẽ tìm đúng NV ít xuất hiện nhất.
    Chọn nhân vật ít về nhất trong 10 và 100 ván gần nhất, sau đó chọn ngẫu nhiên 1 trong 2.
    """
    bet_amount = bet_amount0
    if len(htr) >= 1 and not htr[-1]['kq']:
        bet_amount = heso * htr[-1]['bet_amount']

    try:
        # --- Phân tích 10 ván gần nhất ---
        # data_top10_cdtd[1] là list kết quả (ID NV thắng)
        counts_10 = Counter(data_top10_cdtd[1])
        all_chars = list(range(1, 7))
        
        # Tìm số lần xuất hiện ít nhất (có thể là 0)
        min_count_10 = min(counts_10.get(char, 0) for char in all_chars)
        
        # Lấy danh sách các nhân vật có số lần xuất hiện ít nhất
        least_common_10 = [char for char in all_chars if counts_10.get(char, 0) == min_count_10]
        x1 = random.choice(least_common_10)

        # --- Phân tích 100 ván gần nhất ---
        # data_top100_cdtd[1] là list số lần thắng của NV 1-6 (theo thứ tự index 0->5)
        counts_100 = data_top100_cdtd[1] 
        min_count_100 = min(counts_100)
        
        # Lấy danh sách các nhân vật (index + 1) có số lần thắng ít nhất
        least_common_100 = [i + 1 for i, count in enumerate(counts_100) if count == min_count_100]
        x2 = random.choice(least_common_100)

        # Chọn ngẫu nhiên giữa kết quả 10 ván và 100 ván
        return random.choice([x1, x2]), bet_amount
    except Exception as e:
        prints(255,0,0,f'Lỗi khi chọn NV: {e}')
        # Trường hợp lỗi, chọn ngẫu nhiên
        return random.randint(1,6), bet_amount

def kiem_tra_kq_cdtd(s, headers,kq,ki):
    start_time = time.time()
    prints(0, 255, 37,f'Đang đợi kết quả của kì #{ki}')
    while True:
        try:
            data_top10_cdtd=top_10_cdtd(s, headers)
            # data_top10_cdtd[0][0] là kì mới nhất, data_top10_cdtd[1][0] là kết quả của kì đó
            if int(data_top10_cdtd[0][0])==int(ki):
                winner = int(data_top10_cdtd[1][0])
                prints(0, 255, 30,f'Kết quả kì {ki}: Người về nhất là {NV[winner]}')
                # Tool đặt cược cho NV 'kq' KHÔNG thắng (bet_group: 'not_winner').
                # Nếu winner == kq: NV mình đặt KHÔNG thắng lại thắng -> THUA cược.
                # Nếu winner != kq: NV mình đặt KHÔNG thắng lại KHÔNG thắng -> THẮNG cược.
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
        # Cần đảm bảo user_id là int
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
        json_data = { 
            'issue_id': int(ki), 
            'bet_group': 'not_winner', 
            'asset_type': Coin, 
            'athlete_id': kq, 
            'bet_amount': bet_amount 
        }
        # Cần đảm bảo user-id trong headers là string nếu API yêu cầu
        headers_bet = headers.copy()
        # API của XWorld đôi khi yêu cầu header Referer, Origin từ tên miền chính
        headers_bet['referer'] = 'https://sprintrun.win/' 
        headers_bet['origin'] = 'https://sprintrun.win'

        response = s.post('https://api.sprintrun.win/sprint/bet', headers=headers_bet, json=json_data, timeout=10).json()
        
        if response.get('code') == 0 and response.get('msg') == 'ok':
            prints(0, 255, 19,f'==> Đặt cược thành công!')
        else:
            prints(255, 0, 0, f"==> Lỗi khi đặt cược: {response.get('msg', 'Không rõ lỗi')}. Code: {response.get('code')}")
            return False
        return True
    except Exception as e:
        prints(255,0,0,f'Lỗi khi gửi yêu cầu đặt cược: {e}')
        return False

def main_cdtd():
    s=requests.Session()
    clear_screen()
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
        'user-id': data['user-id'], # Cần phải là string để dùng trong header
        'user-login': 'login_v2', 
        'user-secret-key': data['user-secret-key'], # Cần phải là string để dùng trong header
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
    Coin = ''
    while True:
        prints(125, 255, 168,'Nhập lựa chọn của bạn (1/2/3):',end=' ')
        choice = input()
        if choice in coin_map:
            Coin = coin_map[choice]
            break
        else:
            prints(247, 30, 30, 'Lựa chọn không hợp lệ, vui lòng nhập lại.', end='\r')
            time.sleep(1)

    bet_amount0 = 0
    while True:
        try:
            bet_amount0 = float(input(f'Nhập số {Coin} muốn đặt cho ván đầu tiên: '))
            if bet_amount0 > 0: break
            else: prints(255, 0, 0, "Số tiền cược phải lớn hơn 0.")
        except ValueError:
            prints(255, 0, 0, "Vui lòng nhập một con số hợp lệ.")
            
    heso = 0
    while True:
        try:
            heso = float(input('Nhập hệ số cược sau mỗi ván thua (ví dụ: 2): '))
            if heso > 1: break
            else: prints(255, 0, 0, "Hệ số phải lớn hơn 1 để có lãi.")
        except ValueError:
            prints(255, 0, 0, "Vui lòng nhập một con số hợp lệ.")

    # --- Cài đặt tùy chọn ---
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
        # --- Kiểm tra điều kiện dừng/nghỉ ---
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
            
            # Lấy kì hiện tại để tính toán thời gian nghỉ
            try:
                # Lấy kì mới nhất (index 0)
                current_issue_id = int(top_10_cdtd(s, headers)[0][0]) 
                target_issue_id = current_issue_id + pause_for
                
                while current_issue_id < target_issue_id:
                    # Kì tiếp theo sẽ là current_issue_id + 1
                    prints(255, 255, 0, f"Đang nghỉ... Ván hiện tại #{current_issue_id}. Sẽ chơi lại ở ván #{target_issue_id + 1}.", end='\r')
                    time.sleep(20)
                    current_issue_id = int(top_10_cdtd(s, headers)[0][0])
                
                prints(0, 255, 37, "\nHết thời gian nghỉ. Tiếp tục chơi!")
            except Exception as e:
                prints(255, 0, 0, f"\nLỗi trong lúc nghỉ: {e}. Chờ 30s rồi tiếp tục.")
                time.sleep(30)
        
        # --- Quy trình chính ---
        prints(247, 255, 97,"═" * 47)
        current_assets = user_asset(s, headers)
        print_wallet(current_assets)
        print_stats_cdtd(stats,s,headers,Coin)

        data_top10_cdtd=top_10_cdtd(s, headers)
        data_top100_cdtd=top_100_cdtd(s)
        
        # In dữ liệu trước khi chọn NV để người dùng theo dõi
        print_data(data_top10_cdtd, data_top100_cdtd) 
        
        kq, bet_amount = selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0)
        
        if current_assets[Coin] < bet_amount:
            prints(255,0,0, f"Không đủ tiền để cược {bet_amount:.4f} {Coin}. Dừng bot.")
            break

        # Kì tiếp theo = Kì mới nhất (index 0) + 1
        next_issue_id = int(data_top10_cdtd[0][0]) + 1 
        
        if not bet_cdtd(s, headers, next_issue_id, kq, Coin, bet_amount):
            prints(255, 0, 0, "Đặt cược thất bại, chờ 10s rồi thử lại ván tiếp theo.")
            time.sleep(10)
            continue # Bỏ qua ván này
        
        result=kiem_tra_kq_cdtd(s, headers, kq, next_issue_id)
        
        if result is True:
            stats['win']+=1
            stats['streak']+=1
            stats['max_streak']=max(stats['max_streak'],stats['streak'])
            # Thắng thì reset mức cược về ban đầu
            htr.clear() 
            htr.append({'kq':True,'bet_amount':bet_amount0}) 
        elif result is False:
            stats['streak']=0
            stats['lose']+=1
            htr.append({'kq':False,'bet_amount':bet_amount})
        
        rounds_played += 1
        prints(173, 216, 230, "Đang chờ ván tiếp theo...")
        time.sleep(10)

if __name__ == "__main__":
     main_cdtd() 
