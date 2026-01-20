# Testing instructions

## Run the attack script 
The "Denial of Wallet" Test (Testing Rate Limits)
k6 run -e TARGET_URL=https://example.com attack.js

## The "Spam" Test (Testing Form Protections)
for i in {1..20}; do 
  curl -X POST -d "email=spam$i@evil.com&message=spam" https://formspree.io/f/YOUR_FORM_ID
done

## Security Headers
Mozilla Observatory	Scan URL for CSP/HSTS

## Vulnerable Code
npm audit	Run in CLI

## Bank Account
AWS Budgets	Set hard alarm at $10
