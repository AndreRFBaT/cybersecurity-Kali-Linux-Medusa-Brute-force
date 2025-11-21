# Keylogger Educacional em Python

Este diretório contém um **keylogger desenvolvido para fins 100% educacionais**, como parte do **Bootcamp Santander Cibersegurança(2025)**.

O objetivo é demonstrar como softwares maliciosos capturam entradas do teclado, armazenam logs e monitoram atividades — sempre em ambiente controlado e com **finalidade de estudo**.

---

## 📄 Sobre o Script `keylogger.py`

O arquivo principal deste diretório:

---

## Como o Keylogger Funciona

O script ativa um *listener* que fica rodando em segundo plano capturando as teclas pressionadas.  
Cada tecla é interpretada, tratada e salva em `log.txt`.

## Componentes importantes

### 1. Conjunto de teclas ignoradas
Algumas teclas como *Shift, Ctrl, Alt, Caps Lock* não são registradas:

```python
IGNORAR = {
    keyboard.Key.shift,
    keyboard.Key.shift_r,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.caps_lock,
    keyboard.Key.cmd,
}
```

### 2. Teclas alfanuméricas

Se a tecla tem .char, significa que é um caractere normal (a, b, 1, !, etc.)
Ela é escrita diretamente no log.

### 3. Teclas especiais

São tratadas separadamente:
```bash
# Tecla	Registro no log
Espaço	" "
Enter	\n
Tab	\t
Backspace	" " (simulado)
ESC	[ESC]
Outras	[Key.xxx]
```

### 4. Logs de debug no terminal

O script imprime mensagens úteis no console, como:
```bash
[DEBUG] Tecla recebida no callback: 'a'
[DEBUG] Caracter detectado: a
```

Isso ajuda no entendimento do comportamento do keylogger.

#  Como Executar (Ambiente Controlado)

### 1. Instale a dependência
pip install pynput

### 2. Execute o script
python keylogger.py

### 3. Pressione algumas teclas

O terminal exibirá logs de depuração.

### 4. Verifique o arquivo log.txt

Ele conterá tudo o que foi digitado.

---

### ⚠️ Aviso Legal e Ético

Este script foi criado somente para estudo de técnicas de cibersegurança.

✔ Execute apenas no seu próprio computador

✔ Use somente em máquinas virtuais ou ambientes controlados

### Nunca utilize para espionagem, invasão de privacidade ou fins maliciosos

Uso indevido pode ser crime conforme legislação vigente.

📁 Estrutura da Pasta
```bash
keylogger/
├── keylogger.py      # Script principal
├── log.txt           # Arquivo gerado automaticamente
└── README.md         # Este arquivo
```

