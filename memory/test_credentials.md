# Test Credentials

## Admin Account
- Username: admin
- Password: admin123
- Login URL: /login

## API Auth
- POST /api/auth/login with {"username": "admin", "password": "admin123"}
- Returns: {"access_token": "JWT_TOKEN", "token_type": "bearer"}

## EMERGENT_LLM_KEY
- Present in /app/backend/.env
- Used for AI optimization features
