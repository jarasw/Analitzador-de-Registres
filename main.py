#Analitzador de registre Joel Jara

import re # import de python per treballar amb expressiones regulars (https://docs.python.org/es/3.13/library/re.html)

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
    
def comptar_registres(log_lines):
    """
    Comptar el nombre total de registres (línies) en el fitxer de registre.
    
    :param log_lines: Llista de línies del fitxer.
    :return: Nombre total de registres.
    """
    return len(log_lines)

def comptar_tipus(log_lines):
    """
    Comptar els registres segons el seu tipus (INFO, WARNING, ERROR).
    Es recorre cada línia i s'incrementa el comptador corresponent si s'hi troba el tipus.
    
    :param log_lines: Llista de línies del fitxer.
    :return: Diccionari amb els comptadors per a cada tipus.
    """
    counts = {'INFO': 0, 'WARNING': 0, 'ERROR': 0}
    for linia in log_lines:
        # Es comprova cada tipus, si es troba, s'incrementa i es passa a la següent línia.
        for tipus in counts.keys():
            if tipus in linia:
                counts[tipus] += 1
                break  # Cada línia es considera d'un sol tipus
    return counts

def identificar_ips(log_lines):
    """
    Identifica i retorna les adreces IP úniques trobades en les línies del fitxer.
    Utilitza una expressió regular per cercar patrons d'IP.
    
    :param log_lines: Llista de línies del fitxer.
    :return: Conjunt d'adreces IP úniques.
    """
    ips = set()  # Variable local: conjunt per emmagatzemar IPs úniques
    # Expressió regular per trobar adreces IP (format: x.x.x.x, on x és de 1 a 3 dígits)
    pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    for linia in log_lines:
        matches = re.findall(pattern, linia)
        for ip in matches:
            ips.add(ip)
    return ips

def comptar_paraula_clau(log_lines, paraula):
    """
    Comptar quantes vegades apareix la paraula clau en els missatges dels registres,
    sense tenir en compte majúscules o minúscules.
    
    :param log_lines: Llista de línies del fitxer.
    :param paraula: Paraula clau a cercar.
    :return: Nombre total d'aparicions de la paraula clau.
    """
    count = 0  # Variable local per comptar aparicions
    paraula_lower = paraula.lower()  # Normalitza la paraula a minúscules
    for linia in log_lines:
        # Es converteix la línia a minúscules i es compta quantes vegades apareix la paraula
        count += linia.lower().count(paraula_lower)
    return count

def generar_informe(total, tipus_counts, ips, keyword, keyword_count):
    """
    Genera el text de l'informe amb els resultats de l'anàlisi.
    
    :param total: Nombre total de registres.
    :param tipus_counts: Diccionari amb el recompte per tipus.
    :param ips: Conjunt d'adreces IP úniques.
    :param keyword: Paraula clau cercada.
    :param keyword_count: Nombre d'aparicions de la paraula clau.
    :return: String amb l'informe complet.
    """
    informe = []
    informe.append("Informe d'Anàlisi de Fitxer de Registre")
    informe.append("---------------------------------------")
    informe.append(f"Nombre total de registres: {total}")
    informe.append("Registres per tipus:")
    for tipus, count in tipus_counts.items():
        informe.append(f"\t{tipus}: {count}")
    informe.append("Adreces IP úniques detectades:")
    if ips:
        for ip in ips:
            informe.append(f"\t{ip}")
    else:
        informe.append("\tNo s'han detectat adreces IP.")
    informe.append(f"Recurrència de la paraula clau '{keyword}': {keyword_count}")
    informe.append("---------------------------------------")
    return "\n".join(informe)

def guardar_informe(text_informe, nom_fitxer):
    """
    Guarda l'informe generat en un fitxer.
    
    :param text_informe: String amb el contingut de l'informe.
    :param nom_fitxer: Nom del fitxer on es guardarà l'informe.
    """
    try:
        with open(nom_fitxer, 'w', encoding='utf-8') as f:
            f.write(text_informe)
        print(f"Informe guardat correctament al fitxer {nom_fitxer}")
    except Exception as e:
        print(f"Error en guardar l'informe: {e}")
        
def main():
    """
    Funció principal del programa.
    Aquesta funció coordina la lectura del fitxer, l'anàlisi dels registres,
    la generació de l'informe i la seva visualització/guardat.
    """
    # Variable local: llista amb les línies del fitxer de registre
    log_lines = llegir_fitxer_registre(FITXER_REGISTRE)
    if not log_lines:
        print("No s'han pogut llegir registres. S'acaba l'execució del programa.")
        return

    # Demana a l'usuari que introdueixi la paraula clau per cercar
    paraula_clau = input("Introdueix la paraula clau per buscar: ")

    # Anàlisi del fitxer de registre
    total_registres = comptar_registres(log_lines)
    tipus_counts = comptar_tipus(log_lines)
    ips_unics = identificar_ips(log_lines)
    count_keyword = comptar_paraula_clau(log_lines, paraula_clau)

    # Generació de l'informe
    text_informe = generar_informe(total_registres, tipus_counts, ips_unics, paraula_clau, count_keyword)

    # Mostra l'informe per pantalla
    print("\n" + text_informe)

    # Opcional: guarda l'informe en un fitxer
    guardar_informe(text_informe, FITXER_INFORME)

if __name__ == "__main__":
    main()