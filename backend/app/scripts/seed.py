import asyncio
from datetime import datetime, timedelta, timezone

from app.db.session import AsyncSessionLocal
from app.crud import crud_team, crud_game, crud_role, crud_permission
from app.schemas import TeamCreate, GameCreate, GameUpdate, RoleCreate, PermissionCreate

# --- LISTA DE PERMISSÕES DA PLATAFORMA ---
# Usar um formato (nome técnico, descrição, grupo) facilita a gestão
PLATFORM_PERMISSIONS = [
    # Funcionalidades Básicas
    ("feature:view_game_schedule", "Visualizar a lista de jogos agendados.", "Jogos"),
    ("feature:view_game_details", "Visualizar os detalhes básicos de um jogo.", "Jogos"),

    # Análises Avançadas
    ("feature:access_advanced_analysis", "Aceder à análise avançada de jogos e dicas de valor.", "Análises"),
    ("feature:access_player_stats", "Aceder a estatísticas detalhadas de jogadores.", "Análises"),
    ("feature:access_historical_data", "Aceder e pesquisar dados históricos.", "Análises"),

    # Notificações
    ("notifications:browser_live_bets", "Receber notificações de apostas de valor no navegador.", "Notificações"),
    ("notifications:telegram_live_bets", "Receber notificações de apostas de valor via Telegram.", "Notificações"),

    # Ferramentas
    ("tool:bet_tracker", "Utilizar a ferramenta de acompanhamento de apostas (Bet Tracker).", "Ferramentas"),
    ("tool:bankroll_management", "Utilizar as ferramentas de gestão de banca.", "Ferramentas"),
    ("tool:odds_comparison", "Utilizar o comparador de odds.", "Ferramentas"),

    # Gestão de Conteúdo (Admin)
    ("admin:manage_games", "Criar, editar e apagar jogos.", "Admin"),
    ("admin:manage_teams", "Criar, editar e apagar equipas.", "Admin"),
    ("admin:manage_users", "Gerir utilizadores (ativar, desativar).", "Admin"),
    ("admin:manage_roles_permissions", "Gerir planos (roles) e as suas permissões.", "Admin"),
]


async def seed_data():
    """
    Popula a base de dados com dados iniciais, incluindo permissões e o role de admin.
    """
    print("A iniciar o processo de seeding...")
    db = AsyncSessionLocal()

    try:
        # --- 1. Criar todas as Permissões da Plataforma ---
        print("A criar/verificar permissões...")
        all_permissions = []
        for name, description, group in PLATFORM_PERMISSIONS:
            permission_in = PermissionCreate(name=name, description=description, module_group=group)
            permission = await crud_permission.create_permission(db=db, permission_in=permission_in)
            all_permissions.append(permission)
        await db.commit() # Commit das permissões
        print(f"{len(all_permissions)} permissões processadas.")


        # --- 2. Criar o Role (Plano) de Administrador e associar todas as permissões ---
        print("A criar/verificar o role de Administrador...")
        admin_role_in = RoleCreate(name="admin_full", display_name="Administrador Full", description="Acesso total a todas as funcionalidades e áreas de gestão.")
        admin_role = await crud_role.create_role(db=db, role_in=admin_role_in)

        # Limpa permissões antigas e adiciona as novas para garantir consistência
        admin_role.permissions.clear()
        for perm in all_permissions:
            admin_role.permissions.append(perm)

        db.add(admin_role)
        await db.commit() # Commit do role e das suas associações de permissão
        print("Role de Administrador configurado com todas as permissões.")


        # --- 3. Criar Equipas ---
        print("A criar/verificar equipas...")
        flamengo = await crud_team.create_team(db, team_in=TeamCreate(name="Flamengo", sport="futebol", league="Brasileirão Série A"))
        palmeiras = await crud_team.create_team(db, team_in=TeamCreate(name="Palmeiras", sport="futebol", league="Brasileirão Série A"))
        lakers = await crud_team.create_team(db, team_in=TeamCreate(name="Los Angeles Lakers", sport="nba", league="NBA"))
        warriors = await crud_team.create_team(db, team_in=TeamCreate(name="Golden State Warriors", sport="nba", league="NBA"))
        await db.commit() # Commit das equipas


        # --- 4. Criar Jogos de Exemplo ---
        print("A criar/verificar jogos de exemplo...")
        game1 = await crud_game.get_game_by_id(db, game_id=1)
        if not game1:
            now = datetime.now(timezone.utc)
            game1_in = GameCreate(home_team_id=flamengo.id, away_team_id=palmeiras.id, game_time=now + timedelta(days=1, hours=2))
            await crud_game.create_game(db, game_in=game1_in)

        # --- 5. Adicionar Análise ao Jogo 1 ---
        print("A adicionar/atualizar análise do jogo 1...")
        game_to_update = await crud_game.get_game_by_id(db, game_id=1)
        if game_to_update:
            analysis_update_data = GameUpdate(
                analysis="Clássico de grande rivalidade. Espera-se um jogo equilibrado com poucos golos.",
                value_bet_tip="Menos de 2.5 golos (Under 2.5) é a aposta de maior valor."
            )
            await crud_game.update_game(db, db_game=game_to_update, game_in=analysis_update_data)


        print("\nSeeding concluído com sucesso!")

    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
