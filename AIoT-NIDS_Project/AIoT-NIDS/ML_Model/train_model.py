# Python: ML model training script
from sklearn.ensemble import RandomForestClassifier
from micromlgen import port
import numpy as np

# Örnek veri: [packet_size, rssi, device_count]
X = np.array([
    [200, -60, 3], [180, -65, 2], [190, -58, 2],   # Normal trafik
    [400, -30, 10], [420, -28, 11], [410, -25, 12]  # Anormal trafik
])

# Etiketler: 0 = NORMAL, 1 = ANOMALY
y = np.array([0, 0, 0, 1, 1, 1])

# Model oluştur
model = RandomForestClassifier(n_estimators=10, max_depth=5)
model.fit(X, y)

# Modeli Arduino için .h dosyasına çevir
with open("model.h", "w") as f:
    f.write(port(model, classmap={0: "NORMAL", 1: "ANOMALY"}))

# Model export bitti, şimdi elle gerekli eklemeleri yapıyoruz
with open("model.h", "a") as f:
    f.write("\n\n// MODEL NESNESİ\n")
    f.write("Eloquent::ML::Port::RandomForest clf;\n")
    f.write("\n// SINIF ETİKETLERİ\n")
    f.write("#define NORMAL 0\n")
    f.write("#define ANOMALY 1\n")

