from colorama import Fore



_banner = '''
 _____ _   _ _____ _____ ___________ _____ 
|  _  | | | |_   _/  ___|_   _|  _  \  ___|
| | | | | | | | | \ `--.  | | | | | | |__  
| | | | | | | | |  `--. \ | | | | | |  __| 
\ \_/ / |_| | | | /\__/ /_| |_| |/ /| |___ 
 \___/ \___/  \_/ \____/ \___/|___/ \____/                         
'''



def banner(host, port):
    '''Вывод баннера с ссылкой'''

    print(Fore.GREEN + _banner)
    print(f'Перейдите по http://{host}:{port}')