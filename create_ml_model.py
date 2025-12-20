#!/usr/bin/env python
"""
MLモデルを作成するスクリプト
Dockerコンテナ内で実行: docker compose exec web python create_ml_model.py
"""
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from pathlib import Path

# モデル保存先
MODEL_DIR = Path(__file__).parent / 'ml' / 'models'
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / 'sample_model.pkl'

# サンプルデータで学習
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
y = np.array([2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0])

# モデルの学習
model = LinearRegression()
model.fit(X, y)

# モデルの保存
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model, f)

print(f'MLモデルを作成しました: {MODEL_PATH}')
print(f'テスト予測: 入力=5 -> 予測={model.predict([[5]])[0]}')


