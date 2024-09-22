from colorama import init, Fore, Style

# 初始化 colorama
init(autoreset=True)

print(Fore.RED + 'This is red text')
print(Fore.GREEN + 'This is green text')
print(Fore.BLUE + 'This is blue text')
print(Fore.YELLOW + 'This is yellow text')

print(Style.BRIGHT + 'This is bright text')
print(Style.DIM + 'This is dim text')
print(Style.NORMAL + 'This is normal text')
