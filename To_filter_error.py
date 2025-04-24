#Importando as bibliotecas:
import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
#Definindo o caminho que contém o arquivo FITS da curva de luz que desejamos reparar:
file_path = r'C:\Users\Documents\FITS_File'
#Lendo o arquivo usando o LightKurve:
lc = lk.read(file_path)
#Definindo os filtros de fluxo:
flux_min = 175 #Os valores aqui são arbitrários e cada LC que foi reparada teve
flux_max = 222 #um valor de filtro de fluxo diferente.
#Aplicando o filtro de fluxo:
mask = (lc.flux.value >= flux_min) & (lc.flux.value <= flux_max)
lc_filtered = lc[mask]
#Salvando a LC filtrada como um novo arquivo FITS:
lc_filtered.to_fits('New_FITS_File_Name.fits', overwrite=True)
output_path = r'C:\Users\Documents\New_FITS_File_Name.fits'
lc_filtered.to_fits(output_path, overwrite=True)
#Fim
