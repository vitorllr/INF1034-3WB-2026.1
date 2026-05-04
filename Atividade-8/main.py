
def valida_dominio_email(email):
    return email[-8:] == "@puc.com"

def avalia_senha(senha):
    if len(senha) != 8:
        return False

print(f"{valida_dominio_email("vitor@puc.com")}")