# ─────────────────────────────────────────
# USE EXISTING API (VERY IMPORTANT)
# ─────────────────────────────────────────
data "aws_api_gateway_rest_api" "ecommerce_api" {
  name = "deepa-ecommerce-api"
}

# ─────────────────────────────────────────
# /reviews RESOURCE
# ─────────────────────────────────────────
resource "aws_api_gateway_resource" "reviews" {
  rest_api_id = data.aws_api_gateway_rest_api.ecommerce_api.id
  parent_id   = data.aws_api_gateway_rest_api.ecommerce_api.root_resource_id
  path_part   = "reviews"
}

# ─────────────────────────────────────────
# GET METHOD
# ─────────────────────────────────────────
resource "aws_api_gateway_method" "reviews_get" {
  rest_api_id   = data.aws_api_gateway_rest_api.ecommerce_api.id
  resource_id   = aws_api_gateway_resource.reviews.id
  http_method   = "GET"
  authorization = "NONE"
}

# ─────────────────────────────────────────
# POST METHOD
# ─────────────────────────────────────────
resource "aws_api_gateway_method" "reviews_post" {
  rest_api_id   = data.aws_api_gateway_rest_api.ecommerce_api.id
  resource_id   = aws_api_gateway_resource.reviews.id
  http_method   = "POST"
  authorization = "NONE"
}

# ─────────────────────────────────────────
# LAMBDA INTEGRATION (GET)
# ─────────────────────────────────────────
resource "aws_api_gateway_integration" "reviews_get" {
  rest_api_id             = data.aws_api_gateway_rest_api.ecommerce_api.id
  resource_id             = aws_api_gateway_resource.reviews.id
  http_method             = aws_api_gateway_method.reviews_get.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.review_service.invoke_arn
}

# ─────────────────────────────────────────
# LAMBDA INTEGRATION (POST)
# ─────────────────────────────────────────
resource "aws_api_gateway_integration" "reviews_post" {
  rest_api_id             = data.aws_api_gateway_rest_api.ecommerce_api.id
  resource_id             = aws_api_gateway_resource.reviews.id
  http_method             = aws_api_gateway_method.reviews_post.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.review_service.invoke_arn
}

# ─────────────────────────────────────────
# PERMISSION FOR API → LAMBDA
# ─────────────────────────────────────────
resource "aws_lambda_permission" "reviews_api" {
  statement_id  = "AllowAPIGatewayInvokeReviews"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.review_service.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${data.aws_api_gateway_rest_api.ecommerce_api.execution_arn}/*/*"
}

# ─────────────────────────────────────────
# DEPLOYMENT (FORCE UPDATE)
# ─────────────────────────────────────────
resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_integration.reviews_get,
    aws_api_gateway_integration.reviews_post
  ]

  rest_api_id = data.aws_api_gateway_rest_api.ecommerce_api.id

  triggers = {
    redeployment = timestamp()
  }
}

# ─────────────────────────────────────────
# STAGE (v1)
# ─────────────────────────────────────────
resource "aws_api_gateway_stage" "stage" {
  stage_name    = "v1"
  rest_api_id   = data.aws_api_gateway_rest_api.ecommerce_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}