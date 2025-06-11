# AWS ECS Infrastructure with Terraform

This Terraform configuration sets up an AWS infrastructure for a three-tier application consisting of:

1. Frontend SPA (Single Page Application) running in ECS Fargate
2. Backend API running in ECS Fargate

## 構成概要

このTerraform構成は、以下の3層アプリケーションのAWSインフラを構築します。

1. フロントエンドSPA（Single Page Application）をECS Fargate上で稼働
2. バックエンドAPIをECS Fargate上で稼働
3. PostgreSQLデータベースをRDS上で稼働

## アーキテクチャ

このインフラには以下のコンポーネントが含まれます：

- **VPC**（2つのアベイラビリティゾーンにまたがるパブリック・プライベートサブネット）
- **アプリケーションロードバランサー**（フロントエンド・バックエンド用）
- **ECSクラスター**（フロントエンド・バックエンド用Fargateサービス）
- **RDS PostgreSQL**（プライベートサブネット内）
- **セキュリティグループ**（各コンポーネント間の通信制御）
- **IAMロール**（ECSタスク実行・タスクロール用）
- **CloudWatchロググループ**（コンテナログ用）

## 前提条件

- 適切な認証情報で設定されたAWS CLI
- Terraform v1.0.0以上
- Docker（コンテナイメージのビルド・プッシュ用）

## 使い方

### 1. terraform.tfvarsファイルの更新

`terraform.tfvars`ファイルを自分の環境に合わせて編集してください：

```hcl
aws_region = "ap-northeast-1"  # 利用するリージョンに変更
environment = "dev"

# VPC設定
vpc_cidr           = "10.0.0.0/16"
availability_zones = ["ap-northeast-1a", "ap-northeast-1c"]
private_subnets    = ["10.0.1.0/24", "10.0.2.0/24"]
public_subnets     = ["10.0.101.0/24", "10.0.102.0/24"]

# コンテナイメージ
frontend_image = "your-account-id.dkr.ecr.ap-northeast-1.amazonaws.com/frontend:latest"
backend_image  = "your-account-id.dkr.ecr.ap-northeast-1.amazonaws.com/backend:latest"

# データベース設定
db_name           = "appdb"
db_username       = "dbuser"
db_password       = "your-secure-password"  # セキュアなパスワードを使用してください
db_instance_class = "db.t3.micro"
db_engine_version = "13.7"
```

### 2. Dockerイメージのビルドとプッシュ

Terraformの適用前に、DockerイメージをビルドしECRにプッシュしてください：

```bash
# ECRリポジトリがなければ作成
aws ecr create-repository --repository-name frontend
aws ecr create-repository --repository-name backend

# ECRログイン
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.ap-northeast-1.amazonaws.com

# フロントエンドイメージのビルドとプッシュ
cd ../front
docker build -t your-account-id.dkr.ecr.ap-northeast-1.amazonaws.com/frontend:latest .
docker push your-account-id.dkr.ecr.ap-northeast-1.amazonaws.com/frontend:latest

# バックエンドイメージのビルドとプッシュ
cd ../backend
docker build -t your-account-id.dkr.ecr.ap-northeast-1.amazonaws.com/backend:latest .
docker push your-account-id.dkr.ecr.ap-northeast-1.amazonaws.com/backend:latest
```

### 3. Terraformの初期化

```bash
terraform init
```

### 4. デプロイ計画の確認

```bash
terraform plan
```

### 5. 構成の適用

```bash
terraform apply
```

### 6. アプリケーションへのアクセス

デプロイ完了後、Terraformがフロントエンド・バックエンドのURLを出力します：

- フロントエンドURL: `http://<frontend-alb-dns-name>`
- バックエンドAPI URL: `http://<backend-alb-dns-name>`

## クリーンアップ

Terraformで作成したリソースを全て削除するには：

```bash
terraform destroy
```

## 注意事項

- 本番環境では、データベース認証情報などの機密情報はAWS Secrets ManagerやAWS Parameter Storeで管理してください。
- ALBにSSL証明書を追加し、HTTPSを有効化することを推奨します。
- 本番運用では、インスタンスタイプ・スケーリングポリシー・バックアップ設定などを適切に調整してください。