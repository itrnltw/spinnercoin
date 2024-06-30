import requests, os
from datetime import datetime, timezone

kepala = {
    'Content-Type': 'application/json',
    'Origin':'https://spinner.timboo.pro',
    'Referer': 'https://spinner.timboo.pro/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}


def read_tgWebAppData():
    if os.path.exists('data.txt'):
        with open('data.txt', 'r') as file:
            return file.read().splitlines()
    else:
        print("File 'data.txt' tidak ditemukan.")
        return []


def percobanHitAPI(url, data):
    for percobaan in range(3):
        try:
            res = requests.post(url, headers=kepala, json=data)
            if res.status_code == 200 or 400:
                return res.status_code, res.json()
            else:
                print(f"Gagal!, percobaan {percobaan + 1}", flush=True)
        except requests.exceptions.ConnectionError as e:
            print(f"Koneksi gagal, mencoba lagi {percobaan + 1}", flush=True)
        except Exception as e:
            print(f"Error: {str(e)}", flush=True)
        except:
            print(f"Gagal!, mencoba lagi {percobaan + 1}", flush=True)
    print(f"Gagal setelah 3 percobaan.", flush=True)
    return None


def initData(tgWebData):
    data = {
        "initData": tgWebData
     }
    url = "https://back.timboo.pro/api/init-data"
    return percobanHitAPI(url, data)


def mainkan(tgWebData):
    data = {
        "initData": tgWebData,
        "data":{
            "clicks":25,
            "isClose":None
            }
     }
    url = "https://back.timboo.pro/api/upd-data"
    return percobanHitAPI(url, data)


def repair(tgWebData):
    data = {
        "initData": tgWebData,
     }
    url = "https://back.timboo.pro/api/repair-spinner"
    return percobanHitAPI(url, data)


def upgrade(tgWebData, idSpinner):
    data = {
        "initData": tgWebData,
        "spinnerId": idSpinner
     }
    url = "https://back.timboo.pro/api/upgrade-spinner"
    return percobanHitAPI(url, data)


def claimTask(tgWebData, id):
    data = {
        "initData": tgWebData,
        "requirementId": id
    }
    url = "https://api.timboo.pro/check_requirement"
    return percobanHitAPI(url, data)


for tgWebData in read_tgWebAppData():
    # username = json.loads(urllib.parse.unquote(urllib.parse.parse_qs(tgWebData)['user'][0]))['username']
    initnya = initData(tgWebData)        

    nama = initnya[1].get('initData','NO initData').get('user', 'NO user').get('name', 'NO name')
    idSpinner = initnya[1].get('initData','NO initData').get('spinners', 'NO spinners')[0].get('id', 'NO id')
    balance = initnya[1].get('initData','NO initData').get('user', 'NO user').get('balance', 'NO balance')

    print(f"=== {nama} ===")
    print(f"Balance\t\t: {balance}")
    while True:
        play = mainkan(tgWebData)
        print(f"Playing\t\t: {'Belum Waktunya' if play[0] == 400 else play[1].get('message', 'No Message')}")
        if play[0] == 400:
            break
    while True:
        up = upgrade(tgWebData, idSpinner)
        print(f"Upgrade\t\t: {'Balance Tidak cukup!' if up[0] == 400 else up[1].get('message', 'No Message')}")
        if up[0] == 400:
            break

    if initnya[1].get('initData','NO initData').get('spinners', 'NO spinners')[0].get('endRepairTime', 'NO endRepairTime') == None:
        print(f"Repair\t\t: {repair(tgWebData)[1].get('message', 'No Message')}")
        initnya = initData(tgWebData)
    timeRemaining = initnya[1].get('initData','NO initData').get('spinners', 'NO spinners')[0].get('endRepairTime', 'NO endRepairTime')
    current_time = datetime.now(timezone.utc)
    timeRemainingfix = datetime.fromisoformat(timeRemaining.replace('Z', '+00:00'))
    time_difference = timeRemainingfix - current_time

    # Ubah selisih waktu menjadi jam, menit, dan detik
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Time Remaining\t: {hours:02}:{minutes:02}:{seconds:02}")

    if input("Claim All Task? : ") == 'y':
        ids = []
        for section in initnya[1]["initData"]["sections"]:
            for task in section['tasks']:
                for requirement in task['requirements']:    
                    ids.append(requirement['id'])
        
        for id in ids:
            hasilClaim = claimTask(tgWebData, id)
            print(hasilClaim)

print("Semua akun telah di Eksekusi\nKELUAR")