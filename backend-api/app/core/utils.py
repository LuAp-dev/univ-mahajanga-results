# app/core/utils.py

def calculate_overall_status(results: list) -> str:
    if not results:
        return "Aucun résultat"

    # Filtrer les résultats valides
    valid_notes = [r.note for r in results if r.note is not None]

    if not valid_notes:
        return "Notes manquantes"

    all_passed = all(note >= 10 for note in valid_notes)
    return "Réussi" if all_passed else "Échec"

