#Importando as bibliotecas:
import os
import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
#Definindo o caminho que contém a pasta com os arquivos FITS das curvas de luz que 
desejamos trabalhar:
folder_path = r'C:\Users\Documents\FITS_Folder'
#Loop por todos os arquivos FITS da pasta:
for fits_file in os.listdir(folder_path):
 if fits_file.endswith('.fits'): #O loop lê apenas os arquivos FITS da pasta
 file_path = os.path.join(folder_path, fits_file)
 lc = lk.read(file_path) #Lendo os arquivos FITS com o LightKurve
 
 #Gerando e salvando em formato JPG as curvas de luz:
 fig, ax = plt.subplots(figsize=(16, 8)) #Definindo o tamanho da figura
 #Ao plotar as curvas de luz, personalizamos o marcador, o seu tamanho, sua cor 
 e o estilo da linha:
 lc_plot = lc.plot(ax=ax, marker='.', linestyle='None', color='darkblue', 
 markersize=2)
 plt.legend(loc='best', fancybox=True, framealpha=1, shadow=True, borderpad=1)
 #O arquivo JPG será salvo na mesma pasta em que o arquivo FITS da curva de 
 luz se encontra. O nome do arquivo JPG será o nome do arquivo FITS com a 
 extensão ‘_LC’:
 lc_plot.figure.savefig(os.path.join(folder_path, f'{fits_file[:-5]}_LC.jpg'))
 plt.close(lc_plot.figure)
 
 #Gerando e salvando em formato JPG os periodogramas das curvas de luz:
 #Os periodogramas são gerados usando a função ‘.to_periodogram()’ do 
 LightKurve para o intervalo de período descrito na seção 2.3 deste relatório. 
 Os periodogramas foram normalizados
 pg = lc.normalize(unit='ppm').to_periodogram(minimum_frequency=0.02469136, 
 maximum_frequency=359.999712)
 fig, ax = plt.subplots(figsize=(16, 8)) #Definindo o tamanho da figura
 pg_plot = pg.plot(ax=ax, color='darkblue')
 plt.legend(loc='best', fancybox=True, framealpha=1, shadow=True, borderpad=1)
 plt.grid()
#O arquivo JPG do periodograma será salvo na mesma pasta em que o arquivo 
 FITS da curva de luz se encontra. O nome do arquivo JPG será o nome do 
 arquivo FITS com a extensão ‘_scargle’:
 pg_plot.figure.savefig(os.path.join(folder_path, f'{fits_file[:-
 5]}_scargle.jpg'))
 plt.close(pg_plot.figure)
 
 #Resgatando o valor do período máximo do periodograma com a função 
 ‘.period_at_max_power’ do LightKurve:
 max_period = pg.period_at_max_power.value
 
 #Salvando o valor do período máximo encontrado num arquivo TXT, cujo nome 
 será o nome do arquivo FITS com a extensão ‘_maxp’ na mesma pasta em que o 
 arquivo FITS se encontra:
 with open(os.path.join(folder_path, f'{fits_file[:-5]}_maxp.txt'), 'w') as 
 maxp_file:
 maxp_file.write(f"{max_period}")
 
 #Resgatando os valores do periodograma numa tabela com a função ‘.to_table()’
 do LightKurve:
 periodogram_table = pg.to_table()
 #Organizando a tabela em ordem crescente para a coluna ‘power’, que indica a 
 potência dos períodos encontrados:
 periodogram_table.sort('power')
 #Salvando a tabela num arquivo TXT, cujo nome será o nome do arquivo FITS com 
 a extensão ‘_table’ na mesma pasta em que o arquivo FITS se encontra:
 periodogram_table.write(os.path.join(folder_path, f'{fits_file[:-
 5]}_table.txt'), format='ascii')
#Fim
