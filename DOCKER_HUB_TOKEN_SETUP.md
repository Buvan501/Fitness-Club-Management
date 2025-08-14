# Docker Hub Token Setup - Step by Step

## Creating a Docker Hub Access Token

### Step 1: Login to Docker Hub
1. Go to https://hub.docker.com
2. Sign in with your credentials

### Step 2: Navigate to Security Settings
1. Click on your username (top right)
2. Select "Account Settings"
3. Click on "Security" tab in the left sidebar

### Step 3: Generate Access Token
1. Scroll down to "Access Tokens" section
2. Click "New Access Token"
3. Fill in the details:
   - **Token description**: `GitHub-Actions-FitClub`
   - **Access permissions**: Select "Read, Write, Delete" or "Read, Write"
4. Click "Generate"

### Step 4: Copy the Token
⚠️ **IMPORTANT**: Copy the token immediately - you won't see it again!

### Step 5: Add to GitHub Secrets
1. Go to: https://github.com/Buvan501/Fitness-Club-Management/settings/secrets/actions
2. Click "New repository secret"
3. Name: `DOCKERHUB_TOKEN`
4. Value: Paste the token you copied
5. Click "Add secret"

## Alternative: Use Docker Hub Password
If you don't want to create a token, you can use your Docker Hub password:
- Secret name: `DOCKERHUB_TOKEN`
- Secret value: Your Docker Hub password

## Verification
After adding both secrets, go to Actions tab and re-run the failed workflow.
