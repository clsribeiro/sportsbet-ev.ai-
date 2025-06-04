# Importa a classe CryptContext da biblioteca passlib
from passlib.context import CryptContext

# Cria uma instância de CryptContext, configurando os esquemas de hashing.
# Usaremos 'bcrypt' como o esquema padrão e principal.
# "deprecated="auto"" instrui o passlib a atualizar automaticamente hashes
# que possam ter sido criados com esquemas mais antigos (se aplicável no futuro).
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto puro corresponde a uma senha com hash armazenada.

    Args:
        plain_password: A senha em texto puro a ser verificada.
        hashed_password: A senha com hash armazenada no banco de dados.

    Returns:
        True se as senhas corresponderem, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha em texto puro usando o esquema bcrypt.

    Args:
        password: A senha em texto puro a ser hasheada.

    Returns:
        A string da senha com hash.
    """
    return pwd_context.hash(password)
