# ========================================
# Cognito User Pool
# ========================================

resource "aws_cognito_user_pool" "deestore_users" {
  name = "deestore-users"

  username_attributes = []

  schema {
    attribute_data_type = "String"
    name                = "email"
    required            = true
    mutable             = true
  }

  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = false
  }
}

# ========================================
# Cognito App Client
# ========================================

resource "aws_cognito_user_pool_client" "deestore_client" {
  name         = "Deepa-Ecommerce-Users"
  user_pool_id = aws_cognito_user_pool.deestore_users.id

  generate_secret = false

  callback_urls = [
    "https://dr6mr82mn4hj9.cloudfront.net"
  ]

  logout_urls = [
    "https://dr6mr82mn4hj9.cloudfront.net"
  ]

  allowed_oauth_flows = [
    "code"
  ]

  allowed_oauth_scopes = [
    "email",
    "openid",
    "phone"
  ]

  allowed_oauth_flows_user_pool_client = true

  supported_identity_providers = [
    "COGNITO"
  ]
}

# ========================================
# Cognito Hosted UI Domain
# ========================================

resource "aws_cognito_user_pool_domain" "deestore_domain" {
  domain       = "deestore-auth-deepa"
  user_pool_id = aws_cognito_user_pool.deestore_users.id
}
