
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
    senha_criptografada = []
    #pegar letra e converter para decimal ascii

    #pegar a diferenca entre 65 - c  

    #somar 3 ao resulado acima ^

    #obter o resto da divisao do resultado acima por 26

    #somar resultado acima a 65 e converter o valor para letra somando na lista
    
    # "".join(senha_criptografada)

    for c in senha:
        if c.isalpha:
            
        senha_criptografada.append(c+3)
    return senha_criptografada

print(f"{valida_dominio_email("vitor@puc.com")}")
print(f"{possui_maiuscula("abc@1234")}")
print(f"{possui_minuscula("abc@1234")}")
print(f"{possui_numero("abc@1234")}")

print(f"{avalia_senha("Senha1@aaaa")}")