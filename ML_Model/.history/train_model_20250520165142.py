from sklearn.ensemble import RandomForestClassifier
from micromlgen import port
import numpy as np

# 200 NORMAL samples: packetSize <= 10000
normal_packets = np.random.randint(400, 10000, size=200)
normal_X = normal_packets.reshape(-1, 1)
normal_y = np.zeros(200)

# 200 ANOMALY samples: packetSize > 10000
anomaly_packets = np.random.randint(11000, 17000, size=200)
anomaly_X = anomaly_packets.reshape(-1, 1)
anomaly_y = np.ones(200)

# Combine data
X = np.vstack((normal_X, anomaly_X))
y = np.concatenate((normal_y, anomaly_y))

# Train model
model = RandomForestClassifier(n_estimators=10, max_depth=4)
model.fit(X, y)

# Export to model.h
with open("model.h", "w") as f:
    f.write(port(model, classmap={0: "NORMAL", 1: "ANOMALY"}))

with open("model.h", "a") as f:
    f.write("\nEloquent::ML::Port::RandomForest clf;\n#define NORMAL 0\n#define ANOMALY 1\n")
