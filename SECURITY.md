# 🔒 Security Guidelines for PulseAI

## Critical Security Rules

### ❌ NEVER Commit These Files to GitHub:
1. `.env` - Contains your API keys
2. `.streamlit/secrets.toml` - Streamlit cloud secrets
3. `data/raw/*` - May contain sensitive cached data
4. `*.key`, `*.pem` - Any private keys
5. Personal configuration files

### ✅ Safe to Commit:
- `.env.example` - Template without real keys
- All source code (`.py` files)
- `requirements.txt`
- `README.md`
- `.gitignore`
- Empty data directories with `.gitkeep`

## Setup Instructions

### For Local Development:
1. Copy `.env.example` to `.env`
2. Add your actual API key to `.env`
3. Never share or commit `.env`

### For Streamlit Cloud Deployment:
1. Don't upload `.env` file
2. Add secrets via Streamlit Cloud dashboard:
   - Go to app settings → Secrets
   - Add: `GEMINI_API_KEY = "your_key"`

## API Key Security Best Practices

### Obtaining API Keys Safely:
1. **Google Gemini API Key:**
   - Visit: https://aistudio.google.com/app/apikey
   - Sign in with Google account
   - Create new API key
   - Copy immediately (shown only once)
   - Store in `.env` file locally

### Protecting Your API Keys:
- ✅ Use environment variables (`.env`)
- ✅ Add `.env` to `.gitignore`
- ✅ Use different keys for dev/prod
- ✅ Rotate keys periodically
- ✅ Monitor API usage in Google AI Studio
- ❌ Never hardcode keys in source code
- ❌ Never share keys in screenshots
- ❌ Never commit keys to version control
- ❌ Never post keys in public forums

### If Your Key Is Compromised:
1. **Immediately:**
   - Delete the compromised key in Google AI Studio
   - Generate a new key
   - Update your `.env` file
   - Update Streamlit Cloud secrets

2. **Check for unauthorized usage:**
   - Review API usage in Google AI Studio dashboard
   - Look for suspicious request patterns
   - Monitor rate limits

## Git Safety Checklist

Before pushing to GitHub:
- [ ] Verify `.env` is in `.gitignore`
- [ ] Check no API keys in source code
- [ ] Remove any debug credentials
- [ ] Ensure `secrets.toml` is gitignored
- [ ] Review git status for sensitive files
- [ ] Use `git diff` to check staged changes

## Useful Git Commands

```bash
# Check what will be committed
git status

# See staged changes
git diff --cached

# Remove accidentally staged file
git reset HEAD <file>

# Remove file from git history (if accidentally committed)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

## Environment Variables Priority

PulseAI checks for API keys in this order:
1. Function parameter (for testing)
2. `.env` file via python-dotenv
3. `st.secrets` (Streamlit Cloud)
4. System environment variables

## Additional Security Measures

### Rate Limiting:
- Free tier: 15 requests/minute
- App has built-in rate limiting
- Monitor usage to prevent abuse

### Data Privacy:
- Cached data expires after 24 hours
- No persistent storage of user queries
- All processing happens locally or on Streamlit Cloud

### Network Security:
- All API calls use HTTPS
- Polite scraping with proper headers
- Respects robots.txt

## Reporting Security Issues

If you discover a security vulnerability:
1. **Do NOT** open a public GitHub issue
2. Email: security@yourdomain.com (replace with actual)
3. Include detailed description
4. Allow 48 hours for response

## License Note

This project is open source (MIT License), but:
- Your API keys are YOUR responsibility
- Your deployed instances are YOUR responsibility
- No warranty for security issues arising from misuse

---

**Last Updated:** November 21, 2025

**Remember:** Security is everyone's responsibility! 🔐
