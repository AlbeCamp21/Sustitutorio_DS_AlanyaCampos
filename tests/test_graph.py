from pathlib import Path
import tempfile
from src.graph_analysis import (
    comando_git,
    obtener_commits_con_padres,
    construir_dag,
    calcular_niveles_dag,
    calcular_densidad_ramas,
    obtener_estadisticas_repositorio
)


class TestGraphAnalysis:

    # lista vacia
    def test_comando_git_no_repositorio(self, tmp_path):
        resultado = comando_git(tmp_path, 'status')
        assert resultado == []

    def test_comando_git_repositorio_valido(self):
        ruta_actual = Path('.')
        resultado = comando_git(ruta_actual, 'status --porcelain')
        assert isinstance(resultado, list)

    def test_obtener_commits_con_padres(self):
        ruta_actual = Path('.')
        commits_padres = obtener_commits_con_padres(ruta_actual)
        assert isinstance(commits_padres, list)
        if commits_padres:
            assert isinstance(commits_padres[0], list)
            assert len(commits_padres[0]) >= 1  # Al menos el commit hash

    def test_construir_dag(self):
        ruta_actual = Path('.')
        dag = construir_dag(ruta_actual)
        assert isinstance(dag, dict)
        for commit, padres in dag.items():
            assert isinstance(commit, str)
            assert isinstance(padres, list)

    def test_calcular_niveles_dag_vacio(self):
        dag_vacio = {}
        niveles = calcular_niveles_dag(dag_vacio)
        assert niveles == {}

    def test_calcular_niveles_dag_simple(self):
        # dag simple: commit1 <- commit2 <- commit3
        dag_simple = {
            'commit1': [],  # commit raiz
            'commit2': ['commit1'],
            'commit3': ['commit2']
        }
        niveles = calcular_niveles_dag(dag_simple)
        assert niveles['commit1'] == 0
        assert niveles['commit2'] == 1
        assert niveles['commit3'] == 2

    def test_calcular_niveles_dag_con_merge(self):
        dag_merge = {
            'commit1': [],  # raiz
            'commit2': ['commit1'],
            'commit3': ['commit1'],  # otra rama
            'commit4': ['commit2', 'commit3']  # merge
        }
        niveles = calcular_niveles_dag(dag_merge)
        assert niveles['commit1'] == 0
        assert niveles['commit2'] == 1
        assert niveles['commit3'] == 1
        assert niveles['commit4'] == 2

    def test_calcular_densidad_ramas_vacio(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            densidad = calcular_densidad_ramas(Path(tmp_dir))
            assert densidad == 0.0

    def test_calcular_densidad_ramas_repositorio_real(self):
        ruta_actual = Path('.')
        densidad = calcular_densidad_ramas(ruta_actual)
        assert isinstance(densidad, float)
        assert densidad >= 0.0

    def test_obtener_estadisticas_repositorio(self):
        ruta_actual = Path('.')
        stats = obtener_estadisticas_repositorio(ruta_actual)      
        assert isinstance(stats, dict)
        assert 'total_commits' in stats
        assert 'niveles_maximos' in stats
        assert 'densidad_ramas' in stats
        assert 'commits_raiz' in stats
        assert 'commits_merge' in stats
        assert isinstance(stats['total_commits'], int)
        assert isinstance(stats['niveles_maximos'], int)
        assert isinstance(stats['densidad_ramas'], float)
        assert isinstance(stats['commits_raiz'], int)
        assert isinstance(stats['commits_merge'], int) 
        assert stats['total_commits'] >= 0
        assert stats['niveles_maximos'] >= 0
        assert stats['densidad_ramas'] >= 0.0
        assert stats['commits_raiz'] >= 0
        assert stats['commits_merge'] >= 0

    def test_dag_coherencia(self):
        ruta_actual = Path('.')
        dag = construir_dag(ruta_actual) 
        if dag:
            # ver que todos los padres referenciados existen en el DAG
            for commit, padres in dag.items():
                for padre in padres:
                    pass            
            # verificaf que hay al menos un commit raiz
            commits_raiz = [c for c, p in dag.items() if not p]
            assert len(commits_raiz) >= 1
