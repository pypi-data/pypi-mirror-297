import pandas as pd
from tabulate import tabulate

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

from sklearn.cluster import KMeans
import numpy as np

from scipy.spatial.distance import pdist

from scipy import stats

import plotly.graph_objects as go

from sklearn.manifold import TSNE
import plotly.express as px

import seaborn as sns


def hierarchical_clustering_analysis(df, columns, method='average', metric='sqeuclidean'):
    """
    Realiza a análise de clusters hierárquicos com base nos parâmetros fornecidos.

    Parâmetros:
    df (DataFrame): DataFrame contendo os dados a serem analisados.
    columns (list): Lista de colunas a serem usadas na análise de clusters.
    method (str): Método de aglomeração a ser utilizado. Opções comuns incluem:
        - 'single': ligação simples (mínimo)
        - 'complete': ligação completa (máximo)
        - 'average'(Default): ligação média (usado para médias) 
        - 'ward': minimiza a variância dentro dos clusters (bom para clusters esféricos)
    metric (str): Métrica de distância a ser utilizada. Opções comuns incluem:
        - 'euclidean': distância euclidiana padrão
        - 'sqeuclidean'(Default): distância euclidiana quadrada
        - 'cityblock': distância de Manhattan (ou L1)
        - 'cosine': distância baseada em cosseno
        - 'correlation': distância baseada em correlação

    Retorno:
    str: Tabela formatada com os resultados da análise de clusters.

    A tabela contém as seguintes colunas:
    - Cluster 1: Índice do primeiro cluster que está sendo unido.
    - Cluster 2: Índice do segundo cluster que está sendo unido.
    - Coefficients: A distância entre os dois clusters que estão sendo unidos.
      Este valor representa a similaridade ou diferença entre os clusters unidos.
    - Number of Points in Cluster: O número de pontos (ou observações) no cluster resultante da união.
      Isso indica quantos dados estão contidos no novo cluster formado.
    """
    
    # Selecionar as colunas relevantes para a análise de cluster
    data_for_clustering = df[columns]

    # Realizar a análise de cluster com os parâmetros fornecidos
    Z = linkage(data_for_clustering, method=method, metric=metric)

    # Criar a tabela de aglomeração
    agglomeration_schedule = pd.DataFrame(Z, columns=['Cluster 1', 'Cluster 2', 'Coefficients', 'Number of Points\n in Cluster'])

    # Exibir a tabela utilizando a biblioteca tabulate, sem a primeira coluna
    formatted_schedule = tabulate(agglomeration_schedule[['Cluster 1', 'Cluster 2', 'Coefficients', 'Number of Points\n in Cluster']], 
                    headers=['Cluster 1', 'Cluster 2', 'Distance\n (Coefficients)', 'Number of Points\n in Cluster'], 
                    tablefmt='fancy_grid')
    
    print(formatted_schedule)
    
    

def plot_dendrogram(df, columns, method='average', metric='sqeuclidean'):
    """
    Gera e exibe um dendrograma baseado na análise de clusters hierárquicos.

    Parâmetros:
    df (DataFrame): DataFrame contendo os dados a serem analisados.
    columns (list): Lista de colunas a serem usadas na análise de clusters.
    method (str): Método de aglomeração a ser utilizado. Opções comuns incluem:
        - 'single': ligação simples (mínimo)
        - 'complete': ligação completa (máximo)
        - 'average'(Default): ligação média (usado para médias)
        - 'ward': minimiza a variância dentro dos clusters (bom para clusters esféricos)
    metric (str): Métrica de distância a ser utilizada. Opções comuns incluem:
        - 'euclidean': distância euclidiana padrão
        - 'sqeuclidean'(Default): distância euclidiana quadrada
        - 'cityblock': distância de Manhattan (ou L1)
        - 'cosine': distância baseada em cosseno
        - 'correlation': distância baseada em correlação
        - 'hamming': distância de Hamming (para dados binários)

    Retorno:
    None: A função gera e exibe um dendrograma, sem retorno.

    O dendrograma mostra as seguintes informações:
    - As profissões na lista são os rótulos das folhas (leaf labels).
    - A orientação do dendrograma é horizontal, com as folhas à direita.
    - As distâncias entre clusters são representadas na escala da métrica especificada.
    """
    
    # Selecionar as colunas relevantes para a análise de cluster
    data_for_clustering = df[columns]

    # Realizar a análise de cluster com os parâmetros fornecidos
    Z = linkage(data_for_clustering, method=method, metric=metric)

    # Criar o dendrograma
    plt.figure(figsize=(10, 7))
    dendrogram(Z, labels=df['profissão'].tolist(), leaf_rotation=0, leaf_font_size=10, orientation='right')
    plt.title(f'Dendrograma da Análise de Cluster\nMétodo: {method.capitalize()}, Métrica: {metric.capitalize()}')
    plt.xlabel('Profissões')
    plt.ylabel(f'Distância ({metric.capitalize()})')
    plt.show()
    

def cluster_membership_analysis(df, columns, method='average', metric='sqeuclidean', num_clusters=[3, 4]):
    """
    Realiza uma análise de clusters hierárquicos e retorna uma tabela que identifica a qual cluster cada caso pertence 
    para diferentes soluções de cluster.

    Parâmetros:
    ----------
    df : pandas.DataFrame
        DataFrame contendo os dados a serem analisados. As linhas representam os casos (ex.: profissões) e as colunas 
        representam as variáveis (ex.: z_prestigio, z_suicídio).
        
    columns : list
        Lista de strings contendo os nomes das colunas do DataFrame que serão utilizadas na análise de clusters.
        Essas colunas devem conter os dados quantitativos padronizados que serão usados para calcular as distâncias 
        entre os casos.

    method : str, opcional, default='complete'
        Método de aglomeração a ser utilizado na análise de clusters. Os métodos comuns incluem:
        - 'single': ligação simples, que une os clusters com a menor distância mínima entre elementos.
        - 'complete': ligação completa, que une os clusters com a maior distância máxima entre elementos.
        - 'average'(Default): ligação média, que une os clusters com base na média das distâncias entre todos os pares de elementos.
        - 'ward': minimiza a variância total dentro dos clusters ao combiná-los, adequado para clusters esféricos.

    metric : str, opcional, default='euclidean'
        Métrica de distância a ser utilizada para calcular as distâncias entre os casos. Métricas comuns incluem:
        - 'euclidean': distância euclidiana padrão.
        - 'sqeuclidean'(Default): distância euclidiana ao quadrado.
        - 'cityblock': distância de Manhattan, também conhecida como L1.
        - 'cosine': distância baseada no cosseno do ângulo entre dois vetores.
        - 'correlation': distância baseada na correlação entre vetores.
        - 'hamming': distância de Hamming, utilizada para dados binários.

    num_clusters : list, opcional, default=[3, 4]
        Lista contendo os números de clusters desejados para a análise. Cada valor na lista representa uma solução 
        de cluster que será calculada e reportada na tabela final. Ex.: [3, 4] calculará soluções de cluster para 3 
        e 4 clusters.

    Retorno:
    --------
    str
        Uma string formatada representando a tabela de "Cluster Membership", onde cada caso (ex.: profissão) é associado 
        ao cluster correspondente para diferentes soluções de cluster. A tabela inclui:
        - Case: Nome ou identificação do caso analisado (ex.: nome da profissão).
        - Colunas de Clusters: Cada coluna corresponde a uma solução de cluster diferente (ex.: 3 clusters, 4 clusters),
          mostrando a qual grupo o caso pertence em cada solução.
        
    Exemplos de Uso:
    ----------------
    >>> formatted_membership = cluster_membership_analysis(df, 
                                                           columns=['z_prestigio', 'z_suicídio', 'z_rendimento', 'z_educação'], 
                                                           method='complete', 
                                                           metric='euclidean',
                                                           num_clusters=[3, 4])
    >>> print(formatted_membership)

    Esta função é útil em contextos onde é necessário identificar e comparar a alocação de casos em diferentes soluções de 
    cluster, auxiliando na identificação de grupos homogêneos dentro dos dados.
    """
    
    # Selecionar as colunas relevantes para a análise de cluster
    data_for_clustering = df[columns]

    # Realizar a análise de cluster com os parâmetros fornecidos
    Z = linkage(data_for_clustering, method=method, metric=metric)

    # Adicionar colunas para os clusters
    for n_clusters in num_clusters:
        df[f'{n_clusters} Clusters'] = fcluster(Z, n_clusters, criterion='maxclust')

    # Organizar os resultados para a tabela de "Cluster Membership"
    cluster_membership = df[['profissão'] + [f'{n_clusters} Clusters' for n_clusters in num_clusters]]

    # Formatando a tabela usando tabulate
    formatted_membership = tabulate(cluster_membership, headers=['Case'] + [f'{n_clusters} Clusters' for n_clusters in num_clusters], 
                                     showindex=True, tablefmt='fancy_grid')

    print(formatted_membership)



def kmeans_cluster_analysis(df, columns, n_clusters=3, random_state=42, max_iter=10):
    """
    Realiza a análise de clusters usando K-Means e gera as tabelas e gráficos necessários.

    Parâmetros:
    df (DataFrame): DataFrame contendo os dados a serem analisados.
    columns (list): Lista de colunas a serem usadas na análise de clusters.
    n_clusters (int): Número de clusters a ser usado no K-Means.
    random_state (int): Semente aleatória para reprodução dos resultados.
    max_iter (int): Número máximo de iterações para o K-Means.

    Retorno:
    None: A função gera tabelas e gráficos, sem retorno.
    """
    data_for_clustering = df[columns]

    # Configuração do K-Means com uma iteração inicial
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=1, max_iter=1, init='k-means++')
    
    # Executar o K-Means e capturar os centros iniciais
    kmeans.fit(data_for_clustering)
    centers_history = [kmeans.cluster_centers_]
    
    # Obtenha as contagens de cada cluster inicial
    initial_labels = kmeans.labels_
    initial_cluster_counts = np.bincount(initial_labels)
    initial_cluster_percentages = initial_cluster_counts / len(initial_labels) * 100

    for i in range(1, max_iter):
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=1, max_iter=1, init=centers_history[-1])
        kmeans.fit(data_for_clustering)
        centers_history.append(kmeans.cluster_centers_)
        if np.allclose(centers_history[-1], centers_history[-2]):
            break  # Convergência alcançada
    
    # Obtenha as contagens de cada cluster final
    final_labels = kmeans.labels_
    final_cluster_counts = np.bincount(final_labels)
    final_cluster_percentages = final_cluster_counts / len(final_labels) * 100

    # Histórico de Iterações
    centers_history_array = np.array(centers_history)
    changes_in_centers = np.abs(np.diff(centers_history_array, axis=0)).max(axis=2)
    max_change = np.max(changes_in_centers)

    print("Iteration History")
    iteration_history_table = []
    for iter_num, changes in enumerate(changes_in_centers):
        iteration_history_table.append([f"{iter_num + 1}"] + [f"{change:.3f}" for change in changes])
    print(tabulate(iteration_history_table, headers=['Iteration'] + [f'Cluster {i+1}' for i in range(n_clusters)], tablefmt='fancy_grid'))
    
    print("\na. Convergence achieved due to no or small change in cluster centers.")
    print(f"The maximum absolute coordinate change for any center is {max_change:.3f}.")
    print(f"The current iteration is {len(centers_history)}.")
    # Usando pdist para calcular todas as distâncias entre os centros iniciais
    min_initial_center_distance = np.min(pdist(centers_history[0]))
    print("The minimum distance between initial centers is {:.3f}.".format(min_initial_center_distance))

    # Centros dos Clusters Iniciais
    initial_centers = centers_history[0]
    print("\nInitial Cluster Centers")
    initial_centers_table = pd.DataFrame(initial_centers.T, index=columns, columns=[f'Cluster {i+1}' for i in range(n_clusters)])
    print(tabulate(initial_centers_table, headers='keys', tablefmt='fancy_grid'))

    # Exibindo as contagens e porcentagens dos clusters iniciais
    initial_counts_table = pd.DataFrame({
        "Cluster": [f"Cluster {i+1}" for i in range(n_clusters)],
        "n": initial_cluster_counts,
        "%": initial_cluster_percentages
    })
    print("\nInitial Cluster Counts and Percentages")
    print(tabulate(initial_counts_table, headers='keys', tablefmt='fancy_grid'))

    # Centros dos Clusters Finais
    final_centers = centers_history[-1]
    print("\nFinal Cluster Centers")
    final_centers_table = pd.DataFrame(final_centers.T, index=columns, columns=[f'Cluster {i+1}' for i in range(n_clusters)])
    print(tabulate(final_centers_table, headers='keys', tablefmt='fancy_grid'))

    # Exibindo as contagens e porcentagens dos clusters finais
    final_counts_table = pd.DataFrame({
        "Cluster": [f"Cluster {i+1}" for i in range(n_clusters)],
        "n": final_cluster_counts,
        "%": final_cluster_percentages
    })
    print("\nFinal Cluster Counts and Percentages")
    print(tabulate(final_counts_table, headers='keys', tablefmt='fancy_grid'))

    # Distâncias entre os Centros Finais dos Clusters
    distances = np.zeros((n_clusters, n_clusters))
    for i in range(n_clusters):
        for j in range(i+1, n_clusters):
            distances[i, j] = np.linalg.norm(final_centers[i] - final_centers[j])
            distances[j, i] = distances[i, j]
    
    print("\nDistances between Final Cluster Centers")
    distances_table = pd.DataFrame(distances, columns=[f'Cluster {i+1}' for i in range(n_clusters)], index=[f'Cluster {i+1}' for i in range(n_clusters)])
    formatted_table = distances_table.map(lambda x: f'{x:.3f}' if x != 0 else '')
    print(tabulate(formatted_table, headers='keys', tablefmt='fancy_grid', showindex=True))

    # Gráficos dos Centros dos Clusters Iniciais e Finais
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

    ind = np.arange(n_clusters)  # Posições no eixo x
    width = 0.15  # Largura das barras

    # Plotar os centros iniciais
    for i, column in enumerate(columns):
        axes[0].bar(ind + i*width, initial_centers[:, i], width, label=f'{column}')
    axes[0].set_title('Initial Cluster Centers')
    axes[0].set_xticks(ind + width*(len(columns)-1)/2)
    axes[0].set_xticklabels([f'Cluster {i+1}' for i in range(n_clusters)])
    axes[0].legend()

    # Plotar os centros finais
    for i, column in enumerate(columns):
        axes[1].bar(ind + i*width, final_centers[:, i], width, label=f'{column}')
    axes[1].set_title('Final Cluster Centers')
    axes[1].set_xticks(ind + width*(len(columns)-1)/2)
    axes[1].set_xticklabels([f'Cluster {i+1}' for i in range(n_clusters)])
    axes[1].legend()

    plt.show()
    
    

def perform_kmeans_anova(df, columns, n_clusters=3):
    """
    Realiza a ANOVA para cada coluna em relação aos clusters e gera a tabela com todos os parâmetros.

    Parâmetros:
    df (DataFrame): DataFrame contendo os dados e os rótulos de clusters.
    columns (list): Lista de colunas para as quais a ANOVA será realizada.

    Retorno:
    DataFrame: Resultados da ANOVA com Sum of Squares, df, Mean Square, F-value e p-value.
    """
    def perform_kmeans(df, columns, n_clusters=3, random_state=42):
        """
        Executa KMeans e adiciona a coluna de rótulos de clusters ao DataFrame.

        Parâmetros:
        df (DataFrame): DataFrame contendo os dados.
        columns (list): Lista de colunas a serem usadas no KMeans.
        n_clusters (int): Número de clusters para o KMeans.
        random_state (int): Semente aleatória para reprodução dos resultados.

        Retorno:
        df (DataFrame): DataFrame com rótulos de clusters adicionados.
        """
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
        df['Cluster'] = kmeans.fit_predict(df[columns])
        return df
    
    df = perform_kmeans(df, columns, n_clusters)
    
    anova_results = []

    for col in columns:
        # Grupos divididos por cluster
        groups = [df[df['Cluster'] == cluster][col] for cluster in df['Cluster'].unique()]

        # Realizar ANOVA unidirecional
        f_value, p_value = stats.f_oneway(*groups)

        # Calcular os parâmetros da ANOVA manualmente
        ss_between = sum(len(group) * (group.mean() - df[col].mean())**2 for group in groups)
        ss_within = sum(((group - group.mean())**2).sum() for group in groups)
        df_between = len(groups) - 1
        df_within = df.shape[0] - len(groups)
        ms_between = ss_between / df_between
        ms_within = ss_within / df_within

        # Adicionar resultados à tabela
        anova_results.append([col, ss_between, df_between, ms_between, ss_within, df_within, ms_within, f_value, p_value])

    # Converter os resultados para um DataFrame
    anova_df = pd.DataFrame(anova_results, columns=['Variable', 'Sum of Squares\n(Between)', 'df\n(Between)',
                                                    'Mean Square\n(Between)', 'Sum of Squares\n(Within)', 'df\n(Within)',
                                                    'Mean Square\n(Within)', 'F-value', 'p-value'])
    
    # Exibir os resultados da ANOVA em formato de tabela
    print("ANOVA")
    print(tabulate(anova_df, headers='keys', tablefmt='fancy_grid', floatfmt=".3f", showindex=False))



def plot_elbow_method_plotly(X, max_clusters=10):
    """Gera o gráfico do Método Elbow com WSS, AIC e BIC utilizando Plotly."""
    def calculate_aic_bic(kmeans, X):
        """Calcula AIC e BIC para o modelo KMeans."""
        m = kmeans.n_clusters  # número de clusters
        n, d = X.shape  # nº observações / nº de variáveis

        # Within-Cluster Sum of Squares (WSS)
        wss = kmeans.inertia_

        # Log-verossimilhança aproximada   
        ll = -wss / 2

        # Número de parâmetros (centroides + variância)
        k = m * d + 1

        # AIC
        aic = 2 * k - 2 * ll

        # BIC
        bic = k * np.log(n) - 2 * ll

        return aic, bic

    wss = []
    aic = []
    bic = []

    for k in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        
        # WSS (Within-Cluster Sum of Squares)
        wss.append(kmeans.inertia_)
        
        # Calcular AIC e BIC usando a função corrigida
        aic_k, bic_k = calculate_aic_bic(kmeans, X)
        aic.append(aic_k)
        bic.append(bic_k)
    
    clusters = list(range(2, max_clusters + 1))

    # Criar a figura usando Plotly
    fig = go.Figure()

    # Adicionar a curva WSS
    fig.add_trace(go.Scatter(x=clusters, y=wss, mode='lines+markers', name='WSS', line=dict(color='black')))

    # Adicionar a curva AIC
    fig.add_trace(go.Scatter(x=clusters, y=aic, mode='lines+markers', name='AIC', line=dict(dash='dash', color='red')))

    # Adicionar a curva BIC
    fig.add_trace(go.Scatter(x=clusters, y=bic, mode='lines+markers', name='BIC', line=dict(dash='dot', color='blue')))

    # Marcar o menor valor de BIC
    min_bic_index = np.argmin(bic)
    min_bic_cluster = clusters[min_bic_index]
    fig.add_trace(go.Scatter(x=[min_bic_cluster], y=[bic[min_bic_index]], mode='markers', name='Menor BIC',
                             marker=dict(color='red', size=10, symbol='x')))

    # Layout do gráfico, incluindo escala do eixo X de 1 em 1
    fig.update_layout(
        title='Método Elbow com AIC e BIC',
        xaxis_title='Número de Clusters',
        yaxis_title='Métricas',
        legend_title='Métricas',
        width=800,
        height=600,
        hovermode='x',
        xaxis=dict(
            dtick=1  # Define a escala principal de 1 em 1 no eixo X
        )
    )

    # Exibir o gráfico interativo
    fig.show()
    



def plot_tsne_clusters_interactive(X, n_clusters=3, perplexity=30, random_state=42, hover_col=None, width=800, height=600):
    """
    Gera e plota um gráfico t-SNE dos clusters interativamente usando Plotly.
    
    Parâmetros:
    - X: DataFrame ou array com os dados.
    - n_clusters: Número de clusters a serem utilizados no KMeans.
    - perplexity: Parâmetro do t-SNE.
    - random_state: Semente para reprodução.
    - hover_col: Coluna opcional para exibir ao passar o mouse (ex: df_z['profissão']).
    - width: Largura da figura (em pixels).
    - height: Altura da figura (em pixels).
    """
    
    # Verificar o número de amostras e ajustar perplexity, se necessário
    n_samples = X.shape[0]
    if perplexity >= n_samples:
        perplexity = max(5, n_samples // 2)  # Ajustar perplexity para ser menor que o número de amostras
    
    # Aplicar KMeans aos dados
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    clusters = kmeans.fit_predict(X)
    
    # Aplicar t-SNE para reduzir a dimensionalidade a 2D
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=random_state)
    X_tsne = tsne.fit_transform(X)
    
    # Criar um DataFrame com as coordenadas t-SNE e os clusters
    df_tsne = pd.DataFrame(X_tsne, columns=['Dim1', 'Dim2'])
    df_tsne['Cluster'] = clusters
    
    # Adicionar hover_col (ex: 'profissão') ao DataFrame se fornecida
    hover_data = None
    if hover_col is not None:
        df_tsne['hover_info'] = hover_col
        hover_data = ['hover_info']
    
    # Criar gráfico interativo usando Plotly
    fig = px.scatter(df_tsne, x='Dim1', y='Dim2', color=df_tsne['Cluster'].astype(str),
                     title=f't-SNE dos Clusters)',
                     labels={'color': 'Cluster'}, 
                     hover_data=hover_data)
    
    # Ajustar o tamanho da figura
    fig.update_layout(width=width, height=height)
    
    # Exibir gráfico
    fig.show()
    

def plot_pairgrid_with_clusters(df, n_clusters=3):
    """
    Gera um gráfico do tipo PairGrid com KDE e scatterplot para os dados e clusters fornecidos.
    
    Parâmetros:
    - df: DataFrame com as colunas de interesse para os clusters.
    - n_clusters: Número de clusters a serem utilizados no KMeans.
    """
    
    # Copiar o DataFrame para evitar alterações no original
    X = df.copy(deep=True)
    
    # Aplicar o algoritmo KMeans para identificar os clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    X['Cluster'] = kmeans.fit_predict(X)
    
    # Configurar o PairGrid com os clusters e cores
    g = sns.PairGrid(X, hue="Cluster", palette='tab10')
    
    # Gráficos na diagonal: KDE (Densidade)
    g.map_diag(sns.kdeplot)
    
    # Gráficos acima da diagonal: Scatterplot
    g.map_upper(sns.scatterplot)
    
    # Gráficos abaixo da diagonal: KDE
    g.map_lower(sns.kdeplot)
    
    # Adicionar legenda ao gráfico
    g.add_legend()
    
    # Mostrar o gráfico
    plt.show()