resource "aws_dynamodb_table" "products" {
  name         = "dee-products"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "cart" {
  name         = "dee-cart"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "orders" {
  name         = "dee-orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "reviews" {
  name         = "dee-reviews"
  billing_mode = "PAY_PER_REQUEST"
  hash_key  = "product_id"
  range_key = "user_id"

  attribute {
    name = "product_id"
    type = "N"
  }

  attribute {
    name = "user_id"
    type = "S"
  }
}
