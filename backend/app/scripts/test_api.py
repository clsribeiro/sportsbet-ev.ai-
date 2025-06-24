import asyncio
from app.services import football_api_service

async def main():
    print("A testar a conexão com a API-Futebol...")
    status_data = await football_api_service.get_api_status()

    if status_data:
        print("\nConexão bem-sucedida! Dados recebidos:")
        # Imprime os dados recebidos de forma legível
        import json
        print(json.dumps(status_data, indent=2))
    else:
        print("\nFalha ao conectar ou obter dados da API.")

if __name__ == "__main__":
    asyncio.run(main())
