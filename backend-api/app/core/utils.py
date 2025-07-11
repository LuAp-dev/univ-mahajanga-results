# app/core/utils.py

def calculate_overall_status(results: list) -> str:
    if not results:
        return "Aucun résultat"

    # Exemple simple : succès si toutes les notes >= 10
    all_passed = all(r.note >= 10 for r in results)
    return "Réussi" if all_passed else "Échec"
