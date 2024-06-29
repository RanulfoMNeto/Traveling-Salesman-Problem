# Avaliação de Métodos de Clusterização Aplicado ao Problema do Caixeiro Viajante Simétrico

O Problema do Caixeiro Viajante (PCV) é um dos mais clássicos e conhecidos problemas da otimização combinatória com ampla aplicabilidade para a modelagem de muitas situações importantes do mundo real, associado à determinação do ciclo hamiltoniano de custo mínimo, pertencente à classe dos problemas *NP*-difícil, isto é, não pode ser resolvido em tempo polinomial com uma razão de aproximação constante a menos que *P = NP*.

Uma abordagem de resolução para o problema utiliza técnicas de enumeração, em que todo o espaço de combinações é examinado, realizando uma busca exaustiva pela permutação, isto é, uma bijeção $\pi \colon \{1,\dots,n\} \to \{1,\dots,n\}$ tal que minimize a função objetivo, usualmente consumindo uma inviável quantidade de tempo computacional. Dado esse aspecto combinatório, é necessário considerar algoritmos de aproximação que não possuem garantias da otimalidade da resposta em compensação de eficiência.

Embora a abordagem clássica apresente resultados satisfatórios, avaliaremos a aplicabilidade de métodos de aprendizado de máquina, capazes de automaticamente detectar padrões nos dados e, em seguida, realizar previsões ou tomar decisões. Os pontos $i, j, \dots, k$ definidos em instâncias do problema correspondem a pontos no plano e satisfazem a desigualdade triangular, $c_{ij} + c_{jk} \geq c_{ik}$, onde $c_{ij}$ é a distância estabelecida usando a norma $\ell_2$, tornando possível particionar a instância em problemas independentes utilizando técnicas de agrupamento e, posteriormente, tentar resolvê-las separadamente.

O uso de técnicas de agrupamento é respaldado por trabalhos recentes que demonstram que tais técnicas possuem grande potencial para auxiliar a resolução do PCV.

Além disso, a programação dinâmica destaca-se como uma abordagem sólida e confiável para solucionar o problema em instâncias menores, garantindo a obtenção de soluções ótimas para subproblemas de maneira eficiente, utilizando o princípio da otimalidade para evitar repetições desnecessárias e alcançar resultados precisos ao decompor o problema em subestruturas mais simples.
