import asyncio
import sys
import os
import time
import argparse
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicGenerator, Bip39WordsNum

# Args
parser = argparse.ArgumentParser(description="Solana vanity wallet generator")
parser.add_argument("count", type=int, nargs="?", default=5, help="Number of wallets to generate") # default 5
parser.add_argument("prefix", type=str, nargs="?", default="SOL", help="Target address prefix") # default SOL
args = parser.parse_args()

# Configuration
TARGET_PREFIX = args.prefix.upper()
SAVE_FILE = f"mnemonic_wallet_{TARGET_PREFIX}.txt"
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
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
    bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
    address = bip44_acc.PublicKey().ToAddress()
    
    return mnemonic, address

# Async Worker
async def wallet_worker(found_event: asyncio.Event, print_lock: asyncio.Lock):
    global found_count

    while not found_event.is_set():
        mnemonic, address = generate_solana_wallet()

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
                print(f"Mnemonic:    {mnemonic}\n")
                print("="*55)
                print("")

            with open(SAVE_FILE, "a") as f:
                f.write(f"[FOUND #{index}]\n")
                f.write(f"Address:     {address}\n")
                f.write(f"Mnemonic:    {mnemonic}\n\n")

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