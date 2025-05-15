from sklearn.ensemble import RandomForestClassifier
from micromlgen import port
import numpy as np

# [packetSize, rssi, deviceCount]
X = np.array([
    # NORMAL örnekler (1–2 cihaz bağlı, paket boyutu küçük, zayıf sinyal)
    [500, -65, 1],
    [680, -70, 2],
    [420, -68, 1],
    [540, -62, 2],
    [660, -60, 2],
    [800, -60, 2],
    [980, -60, 2],
    
    # ANOMALY örnekler (3+ cihaz bağlı, ya da büyük paket ya da güçlü sinyal)
    [10000, -15, 3],  # sadece cihaz sayısı fazla
    [15000, -35, 3],  # büyük paket + yüksek cihaz
    [14000, -25, 5],  # hepsi yüksek
    [11000, -30, 4],
    [11500, -45, 4],  # düşük packet ama sinyal çok güçlü ve cihaz fazla
])

y = np.array([
    0, 0, 0, 0, 0, 0, 0,   # NORMAL
    1, 1, 1, 1, 1    # ANOMALY
])

model = RandomForestClassifier(n_estimators=10, max_depth=5)
model.fit(X, y)

with open("model.h", "w") as f:
    f.write(port(model, classmap={0: "NORMAL", 1: "ANOMALY"}))

with open("model.h", "a") as f:
    f.write("\nEloquent::ML::Port::RandomForest clf;\n#define NORMAL 0\n#define ANOMALY 1\n")
