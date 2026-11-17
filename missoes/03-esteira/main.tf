# Missão 3 · Esteira
# Laboratório local: o provider aponta para o LocalStack (S3 falso em http://localhost:4566).
# Nenhuma conta de nuvem é usada.

terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true
  endpoints {
    s3 = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "logs" {
  bucket = "modo-carreira-logs"
  tags = {
    dono  = "time-plataforma"
    custo = "laboratorio"
  }
}

# TODO da missão:
# 1. versionamento ligado no bucket
# 2. bloqueio de todo acesso público (os 4 controles)
