def valida_dominio_email(email):
    return email[-8:] == "@puc.com"


def possui_maiuscula(palavra):
    for c in palavra:
        if c.isupper():
            return True
    return False


def possui_minuscula(palavra):
    for c in palavra:
        if c.islower():
            return True
    return False


def possui_numero(palavra):
    for c in palavra:
        if c.isdigit():
            return True
    return False


def avalia_senha(senha):
    check_tamanho = len(senha) >= 8
    check_maiuscula = possui_maiuscula(senha)
    check_minuscula = possui_minuscula(senha)
    check_numero = possui_numero(senha)

    return check_tamanho and check_maiuscula and check_minuscula and check_numero


def criptografa_a_senha(senha):
    senha_criptografada = ""
    # pegar letra e converter para decimal ascii
    if avalia_senha(senha):
        for char in senha:
            if char.isdigit():
                ref = ord("0")  # 65
                ascii_char = ord(char)
                pos_alfabeto = ascii_char - ref
                pos_cesar = pos_alfabeto + 3
                pos_cesar = pos_cesar % 10
                letra_cifrada = chr(ref + pos_cesar)
                senha_criptografada += letra_cifrada
            elif "A" <= char <= "Z":
                ref = ord("A")  # 65
                ascii_char = ord(char)
                pos_alfabeto = ascii_char - ref
                pos_cesar = pos_alfabeto + 3
                pos_cesar = pos_cesar % 26
                letra_cifrada = chr(ref + pos_cesar)
                senha_criptografada += letra_cifrada
            elif "a" <= char <= "z":
                ref = ord("a")  # 65
                ascii_char = ord(char)
                pos_alfabeto = ascii_char - ref
                pos_cesar = pos_alfabeto + 3
                pos_cesar = pos_cesar % 26
                letra_cifrada = chr(ref + pos_cesar)
                senha_criptografada += letra_cifrada 
            else:
                senha_criptografada += char
        return senha_criptografada


# pegar a diferenca entre 65 - c

# somar 3 ao resulado acima ^

# obter o resto da divisao do resultado acima por 26

# somar resultado acima a 65 e converter o valor para letra somando na lista

# "".join(senha_criptografada)


print(f"{valida_dominio_email('vitor@puc.com')}")
print(f"{possui_maiuscula('abc@1234')}")
print(f"{possui_minuscula('abc@1234')}")
print(f"{possui_numero('abc@1234')}")

print(f"{avalia_senha('Senha1@aaaa')}")
print(f"{criptografa_a_senha("Senha123@")}")