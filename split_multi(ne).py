# split-multi.py
# open source, MIT license

import json
filename = 'data/RUS_simple'
target_len = 15

target_region = ['AUS','BRA','CAN','CHL','CHN','COL','DEU','ESP','GBR','IND','ITA','JPN','KOR','MEX','NGA','NLD','PAK','PER','RUS','SWE','UKR','USA']
# target_region = ['ITA','UKR','RUS']

output_region = [{"type":"FeatureCollection","features":[]} for region in target_region]
# print(output_region)

def parse_cases(filename):
    file = open(filename+'.json','r').read()
    file = file.replace('ADM0_A3','adm0_a3').replace('NAME','name').replace('ADMIN','admin').replace('CONTINENT','region')
    open(filename+'.json','w').write(file)

def process_geojson(filename):
    js = open(filename+'.json', 'r').read()
    gj = json.loads(js)
    output = {"type":"FeatureCollection","features":[]}
    if filename.find('states') != -1:
        mode = 's'
    else:
        mode = 'c'

    for feature in gj['features']:
        if feature['geometry'] is not None:
            if feature['geometry']['type'] == 'MultiPolygon':
                len_list = sorted([[idx, len(elem[0])] for idx, elem in enumerate(feature['geometry']['coordinates'])],key=lambda x: x[1],reverse=True)[:target_len]
                reg_len = [i[0] for i in len_list]

                for idx, poly in enumerate(feature['geometry']['coordinates']):
                    # print(idx)
                    # print(poly)"properties":{},
                        # print(len(feature['geometry']['coordinates']))
                        # print(len(feature['geometry']['coordinates']))
                        # print(len(poly[0]))
                        # print(poly)

                    # if len(feature['geometry']['coordinates'])<target_len or idx in reg_len:  # to be added!
                    if (feature["properties"]["adm0_a3"] in target_region or mode=='c') and (len(feature['geometry']['coordinates'])<target_len or idx in reg_len):
                        xfeature = {"type":"Feature", "properties":{"name":feature["properties"]["name"],"adm0_a3":feature["properties"]["adm0_a3"],"region":feature["properties"]["region"],"admin":feature["properties"]["admin"]}, "geometry":{"type":"Polygon"}}
                        xfeature['geometry']['coordinates'] = poly
                        output['features'].append(xfeature)
                        if mode=='s' and feature["properties"]["adm0_a3"] in target_region:
                            output_region[target_region.index(feature["properties"]["adm0_a3"])]['features'].append(xfeature)

                    # else:
                    #     continue
            else:
                for idx, poly in enumerate(feature['geometry']['coordinates']):
                    # print(idx)
                    # print(poly)
                    # if idx == 0:
                    if feature["properties"]["adm0_a3"] in target_region or mode=='c':
                        xfeature = {"type":"Feature", "properties":{"name":feature["properties"]["name"],"adm0_a3":feature["properties"]["adm0_a3"],"region":feature["properties"]["region"],"admin":feature["properties"]["admin"]}, "geometry":feature["geometry"]}
                        output['features'].append(xfeature)
                        if mode=='s' and feature["properties"]["adm0_a3"] in target_region:
                            output_region[target_region.index(feature["properties"]["adm0_a3"])]['features'].append(xfeature)
                    # else:
                    #     continue
            # if feature["properties"]["adm0_a3"] in target_region:
            #     output_region[target_region.index(feature["properties"]["adm0_a3"])]['features'].append(xfeature)

    if mode == 's':
        for reg_idx in range(len(target_region)):
            # output = output_region[reg_idx]
            open(filename+'_'+target_region[reg_idx]+'.geojson', 'w').write(json.dumps(output_region[reg_idx],separators=(',',':'),ensure_ascii=False).replace('}},','}},\n'))
    open(filename+'.geojson', 'w').write(json.dumps(output,separators=(',',':'),ensure_ascii=False).replace('}},','}},\n'))

if __name__ == '__main__':
    parse_cases(filename)
    process_geojson(filename)
