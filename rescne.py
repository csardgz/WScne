'''
El siguiente script toma el nombre de las personas
registrads para ejercer voto en venezuela de la
pagina web del CNE (Ven) por medio de la cedula de
identidad de las personas registradas

NOTA: para los registrados que ya han fallecido, solo
se podrá obtener esa informacion (fallecido), mas no
el nombre.
'''

#----------------LIBRARIES--------------------

#Lo basico para web scraping
from bs4 import BeautifulSoup
import requests
#Para crear tabla xls
from openpyxl import Workbook

#-----------------FUNCTION--------------------

#Funcion para hacer el request
def requestcne(ci):
    #C.I:
    cis = str(ci)
    #Pagina web agregando la C.I.
    urlci = f'http://www.cne.gob.ve/web/registro_electoral/ce.php?nacionalidad=V&cedula={cis}'

    #Se hace el request
    response = requests.get(urlci)
    
    #Tomando la informacion de la peticion
    text = response.text
    soup = BeautifulSoup(text, "lxml")
    divs = soup.findAll("b")
    
    #Aqui verificamos que esté registrado
    try:

        name = divs[3]
        #Verificamos que esté vivo el votante
        if str(name) == '<b></b>':
            name = 'Fallecido'
        else:    
            name = name.string
    except IndexError:
        name = 'Persona no registrada'

    return name

#--------------------MAIN------------------------

if __name__== '__main__':
        
    #Crear un nuevo libro de trabajo
    wb = Workbook()

    #Crear una hoja de trabajo
    hoja = wb.active
    flag = 0
    #Rango de Cedulados
    ri = 19500000
    rs = 19500010

    for i in range(ri,rs):
        
        flag+=1
        #Escribir las variables en las celdas A1 y B1
        hoja['A' + str(flag)] = i               #C.I.
        hoja['B' + str(flag)] = requestcne(i)   #Nombre


    #Guardar el libro de trabajo
    wb.save(f'ListadoVotantes{str(ri)}-{str(rs)}.xlsx')