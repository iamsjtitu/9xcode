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
- Works only within Emergent platform (preview environment)

## OPENAI_API_KEY
- Present in /app/backend/.env
- Used on VPS for AI optimization (direct OpenAI GPT-4o-mini)
- Also needs to be in VPS .env: /var/www/9xcodes/backend/.env
