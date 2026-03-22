#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# 初期データがあれば投入（既にデータがある場合は無視）
python manage.py loaddata fixtures/initial_data.json || true

# MLモデルの作成（オプション）
python create_ml_model.py || true
