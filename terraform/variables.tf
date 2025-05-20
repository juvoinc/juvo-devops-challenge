variable "lambda_zip_path" {
  type = string
}

resource "aws_lambda_function" "score_api" {
  function_name = "score-api"
  filename      = var.lambda_zip_path
  ...
  architectures = ["arm64"]
  ...
}
