import pandas as pd
import numpy as np


data = pd.read_csv('clustering.csv')

riders = ['jon-aberasturi', 'phil-bauhaus', 'mark-cavendish',
          'ion-izagirre', 'sonny-colbrelli', 'michael-matthews',
          'greg-van-avermaet', 'tiesj-benoot', 'alejandro-valverde',
          'diego-ulissi', 'dylan-teuns', 'jakob-fuglsang',
          'patrick-konrad', 'guillaume-martin', 'wilco-kelderman',
          'dan-martin', 'danny-van-poppel', 'mathieu-van-der-poel',
          'julian-alaphilippe', 'romain-bardet', 'matteo-trentin',
          'bauke-mollema', 'wout-van-aert', 'michael-woods',
          'tadej-pogacar', 'peter-sagan', 'john-degenkolb',
          'luka-mezgec', 'tim-merlier', 'sam-bennett',
          'dylan-groenewegen', 'jasper-philipsen', 'arnaud-demare',
          'pascal-ackermann', 'fernando-gaviria', 'jasper-stuyven',
          'elia-viviani', 'caleb-ewan', 'giacomo-nizzolo',
          'sergio-higuita', 'david-gaudu', 'miguel-angel-lopez',
          'pello-bilbao', 'adam-yates', 'vincenzo-nibali',
          'nairo-quintana', 'thibaut-pinot', 'andre-greipel',
          'egan-bernal', 'primoz-roglic', 'rigoberto-uran',
          'mikel-landa', 'enric-mas', 'alexander-kristoff',
          'rafal-majka', 'simon-yates', 'aleksandr-vlasov']

dims = 1
old_coordinates = np.zeros((len(riders), dims))
coordinates = np.zeros((len(riders), dims))
loss = 9999999999999
start_moving_loc = 1000
decay = -0.0004
init_scale = 1.25
for n in range(10000):
    # new_coordinates = np.tril(np.random.normal(loc=0.0, scale=data['scaled'].std(), size=(len(riders), len(riders))))
    if n < start_moving_loc:
        loc = 0
    else:
        loc = (old_coordinates+coordinates)/2
    scale = init_scale*np.exp(decay*n)
    new_coordinates = np.random.normal(loc=loc, scale=scale, size=(len(riders), dims))
    new_loss = 0
    k = 0
    for i in range(len(riders)):
        for j in range(i, len(riders)):
            new_loss += np.square(data.loc[k, 'scaled'] - np.sqrt(np.sum(np.square(new_coordinates[i, :]
                                                                         - new_coordinates[j, :]))))
            k += 1

    if new_loss < loss:
        old_coordinates = coordinates
        coordinates = new_coordinates
        loss = new_loss
    print(f'iter: {n+1}, loss: {loss}')

data = pd.DataFrame({'rider': riders})
for i in range(dims):
    data['k'+str(i)] = coordinates[:, i]

data.to_csv('coordinates.csv', index=False)
