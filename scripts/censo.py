import os
import shutil
import zipfile

# Descargar el archivo zip, si hay otro archivo con el mismo nombre lo sobreescribe
os.system("curl -# -f -O http://www.ine.es/censos2011_datos/cartografia_censo2011_nacional.zip")

# Comprobamos que el archivo se ha descargado
if os.path.isfile('cartografia_censo2011_nacional.zip'):
    # Se crea el directorio cartografia_censo2011_nacional si no existe y si exixte lo vaciamos, ogr2ogr no sobreescribe.
    if not os.path.exists('cartografia_censo2011_nacional'):
        os.makedirs('cartografia_censo2011_nacional')
    else:
        shutil.rmtree('cartografia_censo2011_nacional')
        os.makedirs('cartografia_censo2011_nacional')
    # Se descomprime el archivo
    with zipfile.ZipFile('cartografia_censo2011_nacional.zip', 'r') as z:
        z.extractall('cartografia_censo2011_nacional')
    z.close()
    # Se buscan los archivos shapefile y se convierten a GeoJSON
    for root, dirs, files in os.walk('cartografia_censo2011_nacional'):
        for file in files:
            if file.endswith(".shp"):
                file = file[:-4]
                path = os.path.join(root, file)
                cmd = 'ogr2ogr -f GeoJSON -t_srs crs:84 ' + path + '.geojson ' + path + '.shp'
                os.system(cmd)
                end = "Archivo: " + file + " convertido a GeoJSON!"
                print(end)
else:
    print("El Archivo no se ha descargado correctamente.")
