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
 
 #Gerando os periodogramas, assim como no Apêndice I, para recuperarmos os 
 períodos máximos:
 pg = lc.normalize(unit='ppm').to_periodogram(minimum_frequency=0.02469136, 
 maximum_frequency=359.999712)
 period_value = pg.period_at_max_power.value
 
 #Dobrando a curva de luz em fase para o período máximo (period_value):
 folded_lc = lc.fold(period=period_value)
 phase = folded_lc.phase.value
 flux = folded_lc.flux.value
 
 #Normalizando e estendendo a curva dobrada em fase para melhor visualização 
 do plot:
 normalized_phase = phase / period_value
 normalized_phase = (normalized_phase + 0.5) % 1
 extended_phase = np.concatenate([normalized_phase, normalized_phase + 1])
 extended_flux = np.concatenate([flux, flux])
 
 #Filtrando e retirando os valores NaN para evitar possíveis mensagens de erro 
 no código:
 extended_flux = np.where(np.isfinite(extended_flux), extended_flux, np.nan)
 
 #Extraindo apenas o número TIC dos arquivos FITS (por exemplo, se o arquivo
 FITS se chamar '0000000004161582_s0044.fits', queremos extrair a informação 
 'TIC 4161582') para deixar uma legenda com o TIC da estrela junto ao diagrama 
 salvo no formato JPG:
 tic_number = fits_file.split('_')[0].lstrip('0')
label = f'TIC {tic_number}'
 
 #Gerando e salvando em formato JPG os diagramas de fase:
 plt.figure(figsize=(16, 8)) #Definindo o tamanho da figura
 #Ao plotar os diagramas, personalizamos os marcadores, seus tamanhos e cor:
 plt.plot(extended_phase, extended_flux, '.', color='crimson', markersize=1, 
 label=label)
 plt.xlabel('Phase [Cycles]')
 plt.ylabel('Flux [$\\mathrm{e^{-}\\,s^{-1}}$]')
 plt.legend(loc='best', fancybox=True, framealpha=1, shadow=True, borderpad=1)
 plt.grid()
 plt.tight_layout()
 
 #O arquivo JPG será salvo na mesma pasta em que o arquivo FITS da curva de 
 luz se encontra. O nome do arquivo JPG será o nome do arquivo FITS com a 
 extensão ‘_phase’:
 jpg_file_path = os.path.join(folder_path, f'{fits_file[:-5]}_phase.jpg')
 plt.savefig(jpg_file_path)
 plt.close()
#Fim
