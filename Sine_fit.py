#Importando as bibliotecas:
import os
import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
#Definindo o caminho que contém a pasta com os arquivos FITS das curvas de luz que 
desejamos trabalhar:
folder_path = r'C:\Users\Documents\FITS_Folder'
#Definindo a função responsável para calcular a função senoidal modelo que se ajustará 
às curvas dobradas em fase
def sine_function(x, amplitude, frequency, phase, offset):
return amplitude * np.sin(2 * np.pi * frequency * x + phase) + offset
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
 
 #Gerando os diagramas de fase:
 plt.figure(figsize=(16, 8)) #Definindo o tamanho da figura
 #Ao plotar os diagramas, personalizamos os marcadores, seus tamanhos e cor:
 plt.plot(extended_phase, extended_flux, '.', color='crimson', markersize=1, 
 label=label)
 #Determinando os parâmetros iniciais para o ajuste da função senoidal:
 amplitude = (np.nanmax(lc.flux) - np.nanmin(lc.flux)) / 2
 initial_amplitude = amplitude.value
 initial_frequency = 1
 initial_phase = 0
 initial_offset = np.mean(extended_flux_valid)
 initial_guesses = [initial_amplitude, initial_frequency, initial_phase, 
 initial_offset]
 #Ajustando os parâmetros iniciais da função senoidal com a função 
 ‘curve_fit()’:
 popt, pcov = curve_fit(
 sine_function, 
 extended_phase_valid, 
 extended_flux_valid, 
 p0=initial_guesses,
 bounds=([0, initial_frequency * 0.9, -np.pi,np.min(extended_flux_valid)], 
 [np.max(extended_flux_valid) * 1.1, initial_frequency * 1.1, 
 np.pi, np.max(extended_flux_valid)])
 )
 #Extraindo os parâmetros otimizados para gerar a função senoidal:
 amplitude_fit, frequency_fit, phase_fit, offset_fit = popt
#Recuperando a amplitude otimizada:
ampep = amplitude_fit

#Gerando a função senoidal. Chamando a função ‘sine_function()’ definida no 
 cabeçalho para os parâmetros otimizados:
 sine_fit = sine_function(extended_phase_valid, amplitude_fit, frequency_fit, 
 phase_fit, offset_fit)
#Calculando os resíduos entre a função senoidal ajustada e os dados reais:
residuals = extended_flux_valid - sine_fit
mean_residuals = np.nanmean(np.abs(residuals))
#Criando legenda para que os resíduos calculados apareçam no plot também:
label2 = f'<r> = {mean_residuals:.6f}' #Resíduo com 6 casas decimais
 #Plotando a função senoidal ajustada junto com o diagrama de fase:
plt.plot(extended_phase_valid, sine_fit, label=label2, color='blue')
 plt.xlabel('Phase [Cycles]')
 plt.ylabel('Flux [$\\mathrm{e^{-}\\,s^{-1}}$]')
 plt.legend(loc='best', fancybox=True, framealpha=1, shadow=True, borderpad=1)
 plt.grid()
 plt.tight_layout()
#O arquivo JPG do diagrama de fase com a função senoidal ajustada será salvo 
 na mesma pasta em que o arquivo FITS da curva de luz se encontra. O nome do 
 arquivo JPG será o nome do arquivo FITS com a extensão ‘_phase_sin’:
 jpg_file_path = os.path.join(folder_path, f'{fits_file[:-5]}_phase_sin_.jpg')
 plt.savefig(jpg_file_path)
 plt.close()
#E os valores calculados para os resíduos e recuperados para as amplitudes 
serão salvos num arquivo TXT na mesma pasta em que o arquivo FITS se 
encontra:
f.write(f"{fits_file}; {ampep}; {mean_residuals}\n")
#Fim
