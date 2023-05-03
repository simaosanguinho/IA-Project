
## Inteligência Artificial 2022/2023

# Projeto: Bimaru

## 1 Introdução
<p align="justify">
O projeto da unidade curricular de Inteligência Artificial (IA) tem como objetivo desenvolver
um programa em Python que resolva o problema Bimaru utilizando técnicas de IA.
O problema Bimaru, também denominado Puzzle Batalha Naval, Yubotu ou Batalha Naval
Solitário, é um puzzle inspirado no conhecido jogo de Batalha Naval entre dois jogadores.
O jogo foi criado na Argentina por Jaime Poniachik e apareceu pela primeira vez em 1982 na
revista argentinaHumor & Juegos. O jogo ficou conhecido internacionalmente ao ser integrado
pela primeira vez noWorld Puzzle Championshipem 1992.
</p>

## 2 Descrição do problema
<p align="justify"> 
De acordo com a descrição que consta na CSPlib^1 , o jogo Bimaru decorre numa grelha quadrada, representando uma área do oceano. Os jogos publicados geralmente usam uma grelha
de 10×10, pelo que assumiremos essa dimensão no contexto do projeto.
A área de oceano contém uma frota escondida que o jogador deve encontrar. Esta frota
consiste num couraçado (quatro quadrados de comprimento), dois cruzadores (cada um com
três quadrados de comprimento), três contratorpedeiros (cada um com dois quadrados de comprimento) e quatro submarinos (um quadrado cada).
</p>

<p align="justify"> 
Os navios podem ser orientados horizontal ou verticalmente, e dois navios não ocupam
quadrados da grelha adjacentes, nem mesmo na diagonal. O jogador também recebe as contagens de linha e coluna, ou seja, o número de quadrados ocupados em cada linha e coluna,
e várias dicas. Cada dica especifica o estado de um quadrado individual na grelha: água (o
quadrado está vazio); círculo (o quadrado é ocupado por um submarino); meio (este é um
quadrado no meio de um couraçado ou cruzador); superior, inferior, esquerda ou direita (este
quadrado é a extremidade de um navio que ocupa pelo menos dois quadrados).
A Figura 1 mostra um exemplo da disposição inicial de uma grelha. A Figura 2 mostra
uma solução para essa mesma grelha. Podemos assumir que uma instância de Bimaru tem
uma solução única.
</p>

## 3 Objetivo
<p align="justify"> 
O objetivo deste projeto é o desenvolvimento de um programa em Python 3.8 que, dada uma
instância de Bimaru, retorna uma solução, i.e., uma grelha totalmente preenchida.
O programa deve ser desenvolvido num ficheirobimaru.py, que lê uma instância de Bimaru a partir do standard input. O programa deve resolver
o problema utilizando uma técnica à escolha e imprimir a solução para o standard output.
</p>

## Entrega 
<p align="justify"> 
Entrega do projeto (.py) no Mooshak e relatório: 5 de Junho, até às 17.
</p>