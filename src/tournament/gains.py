"""
Matrice de gains pour le dilemme du prisonnier itéré.

         j: C       j: D
i: C   (3, 3)     (0, 5)
i: D   (5, 0)     (2, 2)
"""

# Actions possibles
C = "C"  # Coopérer
D = "D"  # Défectionner

# Matrice de gains : gains[action_i][action_j] = (gain_i, gain_j)
GAINS = {
    C: {C: (3, 3), D: (0, 5)},
    D: {C: (5, 0), D: (2, 2)},
}


def gain(action_i, action_j):
    """Retourne les gains pour une paire d'actions (gain_i, gain_j)."""
    return GAINS[action_i][action_j]


def est_dilemme_prisonnier():
    """Vérifie que la matrice respecte T > R > P > S et 2R > T + S."""
    T = GAINS[D][C][0]  # 5
    R = GAINS[C][C][0]  # 3
    P = GAINS[D][D][0]  # 2
    S = GAINS[C][D][0]  # 0
    return T > R > P > S and (2 * R > T + S)


if __name__ == "__main__":
    print("Matrice de gains :")
    for a_i in (C, D):
        for a_j in (C, D):
            g_i, g_j = gain(a_i, a_j)
            print(f"  ({a_i}, {a_j}) -> ({g_i}, {g_j})")
    print(f"\nEst un dilemme du prisonnier valide : {est_dilemme_prisonnier()}")