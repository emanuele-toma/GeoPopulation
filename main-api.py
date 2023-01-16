from PIL import Image
from flask import Flask, request, jsonify
from waitress import serve
import hashlib
import os
import threading
import random
import base64
import geopandas as gpd
from matplotlib.colors import ListedColormap  
import matplotlib.patheffects as pe
import io
import shutil
import time

app = Flask(__name__)

@app.route('/api/v1/generate_map/<int:QUADRANTE>/<int:THRESHOLD>', methods=['GET'])
def generate_map(QUADRANTE, THRESHOLD):
    if QUADRANTE < 1 or QUADRANTE > 8:
        return jsonify({'error': 'Quadrante deve essere compreso tra 1 e 8'}), 400
    
    if THRESHOLD < 0:
        return jsonify({'error': 'Threshold deve essere maggiore o uguale a 0'}), 400

    HASH = hashlib.md5(str(QUADRANTE).encode('utf-8') + str(THRESHOLD).encode('utf-8')).hexdigest()
    DIRECTORY_PATH = 'jobs/' + HASH

    if os.path.exists(DIRECTORY_PATH):
        if os.path.exists(DIRECTORY_PATH + '/status.txt'):
            with open(DIRECTORY_PATH + '/status.txt', 'r') as file:
                status = file.read()
                return jsonify({'status': status, 'hash': HASH}), 200

        if not os.path.exists(DIRECTORY_PATH + '/status.txt'):
            os.rmdir(DIRECTORY_PATH)

    thread = threading.Thread(target=thread_generate_map, args=(DIRECTORY_PATH, QUADRANTE, THRESHOLD))
    thread.start()

    return jsonify({'status': '0', 'hash': HASH}), 200

@app.route('/api/v1/get_random_map/<HASH>', methods=['GET'])
def get_random_map(HASH):
    DIRECTORY_PATH = 'jobs/' + HASH

    if not os.path.exists(DIRECTORY_PATH):
        return jsonify({'error': 'Hash non trovato'}), 404

    if not os.path.exists(DIRECTORY_PATH + '/status.txt'):
        return jsonify({'error': 'Hash non trovato'}), 404

    with open(DIRECTORY_PATH + '/status.txt', 'r') as file:
        status = file.read()

    if status < '100':
        return jsonify({'error': 'Job in corso'}), 400

    if status == '100':
        with open(DIRECTORY_PATH + '/output.txt', 'r') as file:
            line = random_line(file)
            line = line.replace('\n', '').split(', ')

            marked_map = get_map_image(line[0], line[1])

            return jsonify({
                'hash': HASH,
                'latitudine': line[0],
                'longitudine': line[1],
                'coordinates': line[0] + ', ' + line[1],
                'gmaps': 'https://maps.google.com/?q=' + line[0] + ',' + line[1],
                'map': marked_map
                }), 200

@app.route('/api/v1/get_map/<HASH>', methods=['GET'])
def get_map(HASH):
    DIRECTORY_PATH = 'jobs/' + HASH

    if not os.path.exists(DIRECTORY_PATH):
        return jsonify({'error': 'Hash non trovato'}), 404

    if not os.path.exists(DIRECTORY_PATH + '/status.txt'):
        return jsonify({'error': 'Hash non trovato'}), 404

    with open(DIRECTORY_PATH + '/status.txt', 'r') as file:
        status = file.read()

    if status < '100':
        return jsonify({'error': 'Job in corso'}), 400

    if status == '100':
        with open(DIRECTORY_PATH + '/map.png', 'rb') as file:
            map = base64.b64encode(file.read()).decode('utf-8')

        return jsonify({
            'hash': HASH,
            'map': map
            }), 200

def thread_generate_map(DIRECTORY_PATH, QUADRANTE, THRESHOLD):
    print('Nuova operazione: ' + DIRECTORY_PATH + ' - Quadrante: ' + str(QUADRANTE) + ' - Threshold: ' + str(THRESHOLD))
    os.mkdir(DIRECTORY_PATH)

    with open(DIRECTORY_PATH + '/status.txt', 'w') as file:
        file.write('0')

    NO_DATA_VALUE = -9999
    GRIDSIZE = 10800
    HEADERLINES = 6
    CELLSIZE = 0.008333333333333333

    START_QUADRANTE_X = 0
    START_QUADRANTE_Y = 0

    if QUADRANTE >= 1 and QUADRANTE <= 4:
        START_QUADRANTE_Y = 90

    if QUADRANTE >= 5 and QUADRANTE <= 8:
        START_QUADRANTE_Y = 0

    if QUADRANTE == 1 or QUADRANTE == 5:
        START_QUADRANTE_X = -180

    if QUADRANTE == 2 or QUADRANTE == 6:
        START_QUADRANTE_X = -90

    if QUADRANTE == 3 or QUADRANTE == 7:
        START_QUADRANTE_X = 0

    if QUADRANTE == 4 or QUADRANTE == 8:
        START_QUADRANTE_X = 90

    FILE = './popolazione/gpw_v4_population_density_rev11_2020_30_sec_' + str(QUADRANTE) + '.asc'

    img = Image.new('RGB', (GRIDSIZE, GRIDSIZE), (180, 210, 250))
    output = open(DIRECTORY_PATH + '/output.txt', mode='a')

    with open(FILE, 'r') as fileobj:
        line_number = -HEADERLINES
        for line in fileobj:

            if line_number < 0:
                line_number += 1
                continue

            line = line.split()
            if line:
                for i in range(len(line)):
                    if line[i] == str(NO_DATA_VALUE):
                        continue

                    r = int(float(line[i]))
                    
                    if r >= THRESHOLD:
                        r = 255
                        output.write(
                            str(
                                format(
                                    START_QUADRANTE_Y - line_number*CELLSIZE
                                , '.6f')) + ", " + 
                            str(
                                format(
                                    START_QUADRANTE_X + i*CELLSIZE
                                , '.6f')) + "\n")
                    else:
                        r = 0

                    g = 255 - r
                    b = 255 - r
                
                    img.putpixel((i, line_number), (255, g, b))

            line_number += 1
            if line_number % 100 == 0:
                with open(DIRECTORY_PATH + '/status.txt', 'w') as file:
                    file.write(str(int(line_number / GRIDSIZE * 100)))
            
    img.save(DIRECTORY_PATH + '/map.png')
    output.close()

    with open(DIRECTORY_PATH + '/status.txt', 'w') as file:
        file.write('100')

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
    return line

def get_map_image(lat, lon):
    
    gdf = gpd.GeoDataFrame(
        {
            'geometry': gpd.points_from_xy([lon], [lat])
        }, crs="EPSG:4326")
    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    mycolor = ListedColormap(['#6ea133'])

    ax = world.plot(color='white', edgecolor='black', cmap=mycolor)
    
    ax.set_xlim([float(lon) - 30, float(lon) + 30])
    ax.set_ylim([float(lat) - 30, float(lat) + 30])

    gdf.plot(ax=ax, color='red', markersize=1)
    
    for x, y, label in zip(world.geometry.centroid.x, world.geometry.centroid.y, world.name):
        ax.annotate(label, xy=(x, y), ha='center', fontsize=4, color='black', path_effects=[pe.withStroke(linewidth=1, foreground='#6ea133')])

    buf = io.BytesIO()
    
    fig = ax.get_figure()
    fig.savefig(buf, format='png', dpi=600)
    
    data = base64.b64encode(buf.getbuffer()).decode("utf8")
    buf.close()
    return data

def delete_old_folders(max_time=3*60*60, size=2 * 1024 * 1024 * 1024):
    print('Spazzino attivo')
    while True:
        total_size = 0
        for path, dirs, files in os.walk('./jobs'):
            for f in files:
                fp = os.path.join(path, f)
                total_size += os.path.getsize(fp)
        if total_size > size:
            oldest_folder = min(os.listdir('./jobs'), key=lambda f: os.stat(os.path.join('./jobs', f)).st_mtime)
            print('Eliminazione cartella: ' + oldest_folder)
            shutil.rmtree('./jobs/' + oldest_folder)
        else:
            for folder in os.listdir('./jobs'):
                if max_time < time.time() - os.path.getmtime('./jobs/' + folder):
                    print('Eliminazione cartella: ' + folder)
                    shutil.rmtree('./jobs/' + folder)
        time.sleep(2)

if __name__ == '__main__':
    print('API in ascolto su http://localhost:8181/api/v1/')
    thread = threading.Thread(target=delete_old_folders, daemon=True)
    thread.start()
    serve(app, host='0.0.0.0', port=8181)