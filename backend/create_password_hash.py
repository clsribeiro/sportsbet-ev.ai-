import sys
# Adiciona o diretório atual ao path do Python para encontrar o módulo 'app'
sys.path.append('.')

from app.core.security import get_password_hash

def generate_hash():
    """
    Gera uma hash bcrypt para a senha fornecida como argumento na linha de comando.
    """
    if len(sys.argv) < 2:
        print("Uso: python create_password_hash.py 'sua_senha_aqui'")
        sys.exit(1)

    plain_password = sys.argv[1]
    hashed_password = get_password_hash(plain_password)

    print("\n--- HASH GERADA ---")
    print(hashed_password)
    print("-------------------\n")
    print("Copie a hash acima para usar no seu comando SQL.")

if __name__ == "__main__":
    generate_hash()
