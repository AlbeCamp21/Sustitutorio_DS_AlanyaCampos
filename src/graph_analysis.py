import subprocess
from pathlib import Path

ruta_head = 'refs/heads'
ruta_remoto = 'refs/remotes'
ruta_tag = 'refs/tags'


def comando_git(ruta, comando):
    ruta_path = Path(ruta) if isinstance(ruta, str) else ruta
    if not (ruta_path / '.git').is_dir():
        print("No es un repositorio")
        return []
    comando_bash = 'git -C ' + str(ruta_path) + ' ' + comando
    try:
        output = subprocess.run(comando_bash.split(), stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print('No es comando de git')
        return []
    else:
        resultado = output.stdout.decode('utf-8').splitlines()
        return resultado


# Usando comando para obtener todos los commits con sus padres, devuelve una matriz
# Conteniendo los commits, los padres, etc
def obtener_commits_con_padres(ruta):
    lineas = comando_git(ruta, 'rev-list --all --parents')
    commits_padres = []
    for linea in lineas:
        elementos = linea.split()
        if elementos:
            commits_padres.append(elementos)
    return commits_padres


# Para construir el DAG, devuevlve diccionario con los commits de nodos
def construir_dag(ruta):
    commits_padres = obtener_commits_con_padres(ruta)
    dag = {}
    for elementos in commits_padres:
        if len(elementos) >= 1:
            commit = elementos[0]
            padres = elementos[1:] if len(elementos) > 1 else []
            dag[commit] = padres
    return dag


# Calcular nive de los commits en el DAG, comienza desde el 0
def calcular_niveles_dag(dag):
    niveles = {}
    # Encontrar commits raiz (sin padres)
    commits_raiz = [commit for commit, padres in dag.items() if not padres]
    # da nivel 0 a commits raiz
    for commit in commits_raiz:
        niveles[commit] = 0
    # iterando para calcular niveles
    cambios = True
    while cambios:
        cambios = False
        for commit, padres in dag.items():
            if commit not in niveles and padres:
                if all(padre in niveles for padre in padres):
                    nivel_max_padre = max(niveles[padre] for padre in padres)
                    niveles[commit] = nivel_max_padre + 1
                    cambios = True
    return niveles


# Calcular la densidad
def calcular_densidad_ramas(ruta):
    dag = construir_dag(ruta)
    if not dag:
        return 0.0
    niveles = calcular_niveles_dag(dag)
    if not niveles:
        return 0.0
    num_nodos = len(dag)
    nivel_maximo = max(niveles.values()) + 1  # se suma porque los niveles empiezan en 0
    densidad = num_nodos / nivel_maximo
    return densidad


# Para obtener estadisticas del repositorio
def obtener_estadisticas_repositorio(ruta):
    dag = construir_dag(ruta)
    niveles = calcular_niveles_dag(dag)
    densidad = calcular_densidad_ramas(ruta)
    estadisticas = {
        'total_commits': len(dag),
        'niveles_maximos': max(niveles.values()) + 1 if niveles else 0,
        'densidad_ramas': densidad,
        'commits_raiz': len([c for c, p in dag.items() if not p]),
        'commits_merge': len([c for c, p in dag.items() if len(p) > 1])
    }
    return estadisticas


def main():
    ruta_repo = Path('.')
    print(f"Ruta: {ruta_repo.absolute()}")
    # commits con sus padres
    commits_padres = obtener_commits_con_padres(ruta_repo)
    print(f"\nTotal de commits encontrados: {len(commits_padres)}")
    # construccion del DAG
    dag = construir_dag(ruta_repo)
    print(f"Nodos en el DAG: {len(dag)}")
    # Mostrar algunos commits y sus padres para ver que saio bien
    print("\ncommits y sus padres:")
    for i, (commit, padres) in enumerate(list(dag.items())[:]):
        print(f"  {commit[:7]} ---- padres: {[p[:7] for p in padres]}")
    # estadisticas
    stats = obtener_estadisticas_repositorio(ruta_repo)
    print("\nEstadisticas del repo:")
    print(f"  Total de commits: {stats['total_commits']}")
    print(f"  Niveles maximos: {stats['niveles_maximos']}")
    print(f"  Densidad de ramas: {stats['densidad_ramas']:.2f}")
    print(f"  Commits raiz: {stats['commits_raiz']}")
    print(f"  Commits de merge: {stats['commits_merge']}")


if __name__ == "__main__":
    main()
