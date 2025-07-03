import asyncio
import sys
# Adiciona o diretório atual ao path do Python para que ele possa encontrar o módulo 'app'
sys.path.append('.')

from app.db.session import AsyncSessionLocal
from app.crud import crud_user
from app.core.security import verify_password

async def debug_password_verification():
    """
    Busca um utilizador específico e tenta verificar a sua senha para depuração.
    """
    db = AsyncSessionLocal()
    try:
        email_to_check = "administrador@exemplo.com"
        password_to_check = "novasenha123"

        print(f"\n--- A depurar a verificação de senha para: {email_to_check} ---")

        # 1. Buscar o utilizador no banco de dados
        print(f"A procurar utilizador com email: {email_to_check}")
        user = await crud_user.get_user_by_email(db, email=email_to_check)

        if not user:
            print(f"\nERRO: Utilizador '{email_to_check}' não foi encontrado na base de dados.")
            return

        print("Utilizador encontrado!")
        print(f"Hash armazenada no banco: {user.hashed_password}")

        # 2. Verificar a senha
        print(f"A tentar verificar a senha: '{password_to_check}'")
        is_password_correct = verify_password(password_to_check, user.hashed_password)

        print("\n--- RESULTADO DA VERIFICAÇÃO ---")
        if is_password_correct:
            print("✅ SUCESSO! A senha corresponde à hash armazenada.")
        else:
            print("❌ FALHA! A senha NÃO corresponde à hash armazenada.")
        print("--------------------------------\n")

    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(debug_password_verification())
