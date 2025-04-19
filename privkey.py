import asyncio
import sys
import os
import time
import argparse
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base58

# Args
parser = argparse.ArgumentParser(description="Solana vanity wallet generator")
parser.add_argument("count", type=int, nargs="?", default=5, help="Number of wallets to generate") # default 5
parser.add_argument("prefix", type=str, nargs="?", default="SOL", help="Target address prefix") # default SOL
args = parser.parse_args()

# Configuration
TARGET_PREFIX = args.prefix.upper()
SAVE_FILE = f"privkey_wallet_{TARGET_PREFIX}.txt"
CONCURRENT_TASKS = 100
TRUNCATE_LEN = 12
TARGET_COUNT = args.count

# Shared state
found_count = 0
found_lock = asyncio.Lock()
start_time = time.time()

# Time Formatter
def format_duration():
    now = time.time()
    elapsed = now - start_time
    now_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))
    return f"[{now_str}]"

# Address Generator
def generate_solana_wallet():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    secret_key_64 = private_key_bytes + public_key_bytes
    address = base58.b58encode(public_key_bytes).decode()
    private_key = base58.b58encode(secret_key_64).decode()

    return address, private_key

# Async Worker
async def wallet_worker(found_event: asyncio.Event, print_lock: asyncio.Lock):
    global found_count

    while not found_event.is_set():
        address, private_key = generate_solana_wallet()

        interval = format_duration()
        async with print_lock:
            truncated = f"{address[:TRUNCATE_LEN]}...{address[-TRUNCATE_LEN:]}"
            sys.stdout.write(f"\r{interval} [Searching] {truncated}")
            sys.stdout.flush()

        if address.startswith(TARGET_PREFIX):
            async with found_lock:
                if found_count >= TARGET_COUNT:
                    found_event.set()
                    return

                found_count += 1
                index = found_count

            async with print_lock:
                print(f"\n\n[FOUND #{index}]")
                print(f"Address:     {address}")
                print(f"Private Key: {private_key}\n")
                print("="*55)
                print("")

            with open(SAVE_FILE, "a") as f:
                f.write(f"[FOUND #{index}]\n")
                f.write(f"Address:     {address}\n")
                f.write(f"Private Key: {private_key}\n\n")

            if found_count >= TARGET_COUNT:
                found_event.set()

# Main
async def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Looking for {TARGET_COUNT} Solana address starting with: {TARGET_PREFIX}\n")
    # if os.path.exists(SAVE_FILE):
        # os.remove(SAVE_FILE)

    found_event = asyncio.Event()
    print_lock = asyncio.Lock()
    tasks = [asyncio.create_task(wallet_worker(found_event, print_lock)) for _ in range(CONCURRENT_TASKS)]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nStopping search...\n")