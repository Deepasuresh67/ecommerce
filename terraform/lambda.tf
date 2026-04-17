resource "aws_lambda_function" "product_service" {
  function_name = "Deepa-product-service"
  role          = "arn:aws:iam::726101441380:role/Deepa-product-service-role-qlj5sf8y"

  handler = "lambda_function.lambda_handler"
  runtime = "python3.10"

  filename         = "dummy.zip"
  source_code_hash = filebase64sha256("dummy.zip")

  lifecycle {
    ignore_changes = all
  }
}

resource "aws_lambda_function" "cart_service" {
  function_name = "Deepa-cart-service"
  role          = "arn:aws:iam::726101441380:role/Deepa-cart-service-role-yjztcl4l"

  handler = "lambda_function.lambda_handler"
  runtime = "python3.10"

  filename         = "dummy.zip"
  source_code_hash = filebase64sha256("dummy.zip")

  lifecycle {
    ignore_changes = all
  }
}

resource "aws_lambda_function" "order_service" {
  function_name = "Deepa-order-service"
  role          = "arn:aws:iam::726101441380:role/Deepa-order-service-role-pd7dncrv"

  handler = "lambda_function.lambda_handler"
  runtime = "python3.10"

  filename         = "dummy.zip"
  source_code_hash = filebase64sha256("dummy.zip")

  lifecycle {
    ignore_changes = all
  }
}