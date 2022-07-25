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
riders.reverse()

coordinates = np.ones((len(riders), len(riders)))

for i in range(1, len(riders)):
    loss = 999999999
    best = np.zeros((1, len(riders)))
    for n in range(100*i):
        coordinates[i, :i] = np.random.normal(loc=0, scale=1, size=(1, i))
        new_loss = 0
        for j in range(i):
            new_loss += np.square(data.loc[((data['rider_1'] == riders[i])
                                            & (data['rider_2'] == riders[j]))
                                           | ((data['rider_1'] == riders[j])
                                              & (data['rider_2'] == riders[i]))
                                           , 'scaled'].values[0] - np.sqrt(np.sum(np.square(coordinates[i, :]
                                                                                  - coordinates[j, :]))))
        if new_loss < loss:
            loss = new_loss
            best = coordinates[i, :]
    print(loss)
    coordinates[i, :] = best
