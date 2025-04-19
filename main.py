import os
import time

default_count = 5
default_prefix = "SOL"
banner = ("\n    :: Solana Vanity Wallet Generator\n")

def countdown(seconds):
    while seconds > 0:
        print(f"start in {seconds}", end='\r')
        time.sleep(1)
        seconds -= 1

def main():
    print(banner)
    print("1. Generate using mnemonic")
    print("2. Generate using private key")
    while True:
        choose = input("Choose (1/2): ")

        if choose == "1":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("You're using mnemonic")
                mnemonic = input("Would you want generate with default count and prefix or not? (y/n): ")
                if mnemonic == "y":
                    print(f"Default count is {default_count}, and default prefix is {default_prefix}\n")
                    countdown(5)
                    os.system('python mnemonic.py')
                    break
                elif mnemonic == "n":
                    print("\n:: Please input target count and prefix")
                    while True:
                        count = input("Target count: ")
                        if count.isdigit():
                            count = int(count)
                            break
                        else:
                            print("Please enter a valid number.")
                    prefix = input("Prefix: ")
                    print("")
                    countdown(5)
                    os.system(f'python mnemonic.py {count} {prefix}')
                    break
                else:
                    print("Invalid input")
        elif choose == "2":
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("You're using private key")
                mnemonic = input("Would you want generate with default count and prefix or not? (y/n): ")
                if mnemonic == "y":
                    print(f"Default count is {default_count}, and default prefix is {default_prefix}\n")
                    countdown(5)
                    os.system('python privkey.py')
                    break
                elif mnemonic == "n":
                    print("\n:: Please input target count and prefix")
                    while True:
                        count = input("Target count: ")
                        if count.isdigit():
                            count = int(count)
                            break
                        else:
                            print("Please enter a valid number.")
                    prefix = input("Prefix: ")
                    print("")
                    countdown(5)
                    os.system(f'python privkey.py {count} {prefix}')
                    break
                else:
                    print("Invalid input")
        else:
            print("Invalid input")
        break
        

if __name__ == "__main__":
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    except KeyboardInterrupt:
        print("\n\nClose program..\n")
