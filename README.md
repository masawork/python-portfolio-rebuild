# Django + ML ポートフォリオ

Python/Djangoと機械学習を活用したポートフォリオサイトです。

## 技術スタック

- Python 3.11+
- Django + Django REST Framework
- OpenAPI: drf-spectacular（Swagger UI）
- DB：SQLite（開発）/ PostgreSQL（本番）
- ML：scikit-learn（推論のみ）
- Docker / docker-compose

## 起動手順

### 1. 環境変数の設定

`.env`ファイルを作成し、以下の内容を設定してください：

```env
SECRET_KEY=django-insecure-change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://portfolio_user:portfolio_pass@db:5432/portfolio_db
```

### 2. Docker Composeで起動

```bash
docker compose up -d
```

### 3. マイグレーションと初期データ投入

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py loaddata fixtures/initial_data.json
```

### 4. MLモデルの作成（オプション）

```bash
docker compose exec web python create_ml_model.py
```

### 5. スーパーユーザー作成（オプション）

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. アクセス

- フロントエンド: http://localhost:8000
- Django Admin: http://localhost:8000/admin
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/

## 環境変数（ENV）

`.env`ファイルに以下の変数を設定してください：

- `SECRET_KEY`: Djangoのシークレットキー（必須）
- `DEBUG`: デバッグモード（True/False、デフォルト: True）
- `ALLOWED_HOSTS`: 許可するホスト（カンマ区切り、デフォルト: localhost,127.0.0.1）
- `DATABASE_URL`: データベース接続URL（PostgreSQL用、Docker Compose使用時は自動設定）

## API一覧

### Projects
- `GET /api/projects/` - プロジェクト一覧
- `GET /api/projects/{id}/` - プロジェクト詳細

### Blog
- `GET /api/blog/` - ブログ一覧
- `GET /api/blog/{id}/` - ブログ詳細

### Contact
- `POST /api/contact/` - お問い合わせ送信

### ML Demo
- `POST /api/ml/predict/` - 機械学習推論API

### OpenAPI
- `GET /api/schema/swagger-ui/` - Swagger UI
- `GET /api/schema/redoc/` - ReDoc

## よくある問題

### データベース接続エラー

- Dockerコンテナが起動しているか確認: `docker compose ps`
- `.env`ファイルの`DATABASE_URL`が正しいか確認
- ポート5432が使用可能か確認

### マイグレーションエラー

- `docker compose exec web python manage.py migrate`でマイグレーションを再実行
- 必要に応じて`docker compose exec web python manage.py migrate --run-syncdb`

### MLモデルが見つからない

- `docker compose exec web python create_ml_model.py`でMLモデルを作成
- モデルがない場合でも、デモ用の計算結果が返されます

## 今後の拡張案

1. **認証機能の強化**
   - JWT認証の追加
   - OAuth2連携

2. **ML機能の拡張**
   - 複数のMLモデル対応
   - モデル選択UI
   - 推論履歴の保存

3. **パフォーマンス最適化**
   - Redisキャッシュの導入
   - 画像最適化
   - CDN連携

4. **CI/CD**
   - GitHub Actionsの設定
   - 自動テスト
   - 自動デプロイ

5. **モニタリング**
   - Sentry連携
   - ログ集約
   - パフォーマンス監視

