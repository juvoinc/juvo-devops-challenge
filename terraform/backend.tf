terraform {
  backend "s3" {
    bucket       = "tfstate-bucket-score-api"
    key          = "terraform/score-api.tfstate"
    region       = "us-east-1"
    use_lockfile = true
    encrypt      = true
  }
}