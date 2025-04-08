import asyncio
import aiohttp
from aiohttp import ClientSession
import time
import os

yay = []

async def fetch(url, session):
    try:
        async with session.get(url) as response:
            status = response.status
            if status == 200:
                print(f"[+] Found: {url} | Status: {status}")
                yay.append(url)
            elif status == 404:
                print(f"[-] Not Found: {url} | Status: {status}")
            else:
                print(f"[?] {url} | Status: {status}")
    except Exception as e:
        print(f"[!] Error fetching {url}: {e}")

async def run(target):
    url = target.strip().replace("https://", "").replace("http://", "")
    url = "http://" + url  # atau sesuaikan kalau pakai https

    paths = []
    with open('wordlist.txt', 'r') as admin_list:
        for path in admin_list:
            paths.append(path.strip())

    tasks = []
    async with ClientSession() as session:
        for i in paths:
            full_url = f"{url}/{i}"
            task = asyncio.ensure_future(fetch(full_url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)

def main():
    start = time.time()

    with open('contoh.txt', 'r') as f:
        targets = f.readlines()

    for target in targets:
        asyncio.run(run(target.strip()))

    end = time.time()
    print(f"\n[✓] Scan completed in {end - start:.2f} seconds.\n")

    if yay:
        with open('shell.txt', 'a') as output_file:
            for y in yay:
                output_file.write(y + '\n')
        print(f"[✓] Found URLs saved to shell.txt")
    else:
        print("[-] No valid paths found.")

if __name__ == "__main__":
    main()
