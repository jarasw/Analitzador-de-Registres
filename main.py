#Analitzador de registre Joel Jara

import re # import de pytthon per treballar amb expressiones regulars (https://docs.python.org/es/3.13/library/re.html)

# Les variables globals:
FITXER_REGISTRE = 'register.log'  # Nom del fitxer de registre d'entrada
FITXER_INFORME = 'informe.txt'    # Nom del fitxer on es guardarà l'informe

def llegir_fitxer_registre(nom_fitxer):
    """
    Llegeix el fitxer de registre i retorna una llista amb les línies.
    Try/except per gestionar possibles errors (per exemple: fitxer no trobat).
    
    :param nom_fitxer: Nom del fitxer a llegir.
    :return: Llista amb les línies del fitxer o una llista buida en cas d'error.
    """
    try:
        with open(nom_fitxer, 'r', encoding='utf-8') as f:
            linies = f.readlines()
        return linies
    except FileNotFoundError:
        print(f"Error: El fitxer {nom_fitxer} no existeix.")
        return []
    except Exception as e:
        print(f"Error al llegir el fitxer: {e}")
        return []