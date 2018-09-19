import geopandas as gpd
import random
import os

d = {}

savefile = open('Report.txt', 'w')
savefile = open('Report.txt', 'a')

for file in os.listdir():

    if file.endswith('.shp'):
        file_name = file[:-4]
        d["{0}".format(file_name)] = gpd.read_file(file)
        # Count
        d["c_{0}".format(file_name)] = d["{0}".format(file_name)].count()[0]

        # Training samples
        d["t_{0}".format(file_name)] = d["c_{0}".format(file_name)]/3

        # Validation
        c = 0
        d["v_{0}".format(file_name)] = []
        while c < d["t_{0}".format(file_name)]:
            r = random.randint(0, d["c_{0}".format(file_name)]-1)
            if r in d["v_{0}".format(file_name)]:
                pass
            else:
                d["v_{0}".format(file_name)].append(r)
                c += 1

        # Entrainement
        d["e_{0}".format(file_name)] = []
        for i in range(d["c_{0}".format(file_name)]):
            if i in d["v_{0}".format(file_name)]:
                pass
            else:
                d["e_{0}".format(file_name)].append(i)
        savefile.write('{0}\n'.format(file_name.upper())+str(len(d["v_{0}".format(file_name)])) + ' sur ' + str(d["c_{0}".format(file_name)]) + ' pour valider:')
        savefile.write('\nValidation ')
        savefile.write(str(sorted(d["v_{0}".format(file_name)])))
        savefile.write('\nEntrainement ')
        savefile.write(str(sorted(d["e_{0}".format(file_name)])))
        savefile.write('\n')
        savefile.write('-'*120)
        savefile.write('\n')

        # Training GeoDataFrame
        d["Ent_{0}".format(file_name)] = d["{0}".format(file_name)].drop(d["{0}".format(file_name)].index[d["v_{0}".format(file_name)]])    

        # Validation GeoDataFrame
        d["Val_{0}".format(file_name)] = d["{0}".format(file_name)].drop(d["{0}".format(file_name)].index[d["e_{0}".format(file_name)]])

        # Export results
        if not os.path.exists('ENTRAINEMENT'):
            os.makedirs('ENTRAINEMENT')

        if not os.path.exists('VALIDATION'):
            os.makedirs('VALIDATION')

        if not os.path.exists("Ent_{0}".format(file)):
            d["Ent_{0}".format(file_name)].to_file(r"ENTRAINEMENT\Ent_{0}".format(file))
        else:
            print('Ent_{0} already exists'.format(file))

        if not os.path.exists("Val_{0}".format(file)):
            d["Val_{0}".format(file_name)].to_file(r"VALIDATION\Val_{0}".format(file))
        else:
            print('Val_{0} already exists'.format(file))
savefile.close()

print('Done')
input('Click "Enter" to exit')
