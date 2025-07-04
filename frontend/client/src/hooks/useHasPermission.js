import { useAuth } from '../context/AuthContext';

/**
 * Um "custom hook" para verificar se o utilizador autenticado tem uma ou mais permissões.
 * * @param {string | string[]} requiredPermissions - O nome de uma única permissão (string) ou uma lista de nomes de permissões.
 * @returns {boolean} - Retorna `true` se o utilizador tiver a permissão (ou todas as permissões, se for uma lista), caso contrário `false`.
 */
export const useHasPermission = (requiredPermissions) => {
  const { user, permissions } = useAuth();

  // Se o utilizador for um superutilizador, ele tem todas as permissões.
  if (user?.is_superuser) {
    return true;
  }

  // Garante que temos um Set de permissões válido para trabalhar
  if (!permissions || permissions.size === 0) {
    return false;
  }

  // Se for necessário apenas uma permissão (uma string)
  if (typeof requiredPermissions === 'string') {
    return permissions.has(requiredPermissions);
  }

  // Se for necessária uma lista de permissões, verifica se o utilizador tem TODAS elas.
  if (Array.isArray(requiredPermissions)) {
    return requiredPermissions.every(p => permissions.has(p));
  }

  // Retorna false por defeito se a entrada for inválida
  return false;
};
