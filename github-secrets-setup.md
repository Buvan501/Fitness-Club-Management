# GitHub Secrets Setup Guide

## Required Secrets for CI/CD Pipeline

Go to: `https://github.com/Buvan501/Fitness-Club-Management/settings/secrets/actions`

### 1. DOCKERHUB_USERNAME
- **Value**: Your Docker Hub username (e.g., `buvan501`)
- **Description**: Used to login to Docker Hub

### 2. DOCKERHUB_TOKEN
- **Value**: Docker Hub access token
- **How to get**:
  1. Go to https://hub.docker.com
  2. Login → Account Settings → Security
  3. Create New Access Token
  4. Copy the token

### 3. KUBE_CONFIG_DATA (Optional - for Kubernetes deployment)
- **Value**: Base64 encoded kubeconfig file
- **How to get**:
  ```bash
  cat ~/.kube/config | base64 -w 0
  ```
- **Note**: Only needed if you want to deploy to Kubernetes cluster

## Quick Setup Commands

### Create Docker Hub Token
1. Visit: https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Name: "GitHub-Actions-FitClub"
4. Copy the generated token

### Test Docker Login Locally
```bash
echo "YOUR_DOCKER_TOKEN" | docker login --username YOUR_USERNAME --password-stdin
```

## Verification

After adding secrets, trigger the workflow by:
1. Making a commit to main branch, or
2. Going to Actions tab and manually running the workflow

## Troubleshooting

### If Docker login still fails:
- Verify username is correct (case-sensitive)
- Ensure token has proper permissions
- Check if 2FA is enabled on Docker Hub account

### If Kubernetes deployment fails:
- Remove the deploy job if you don't have a K8s cluster
- Or add proper KUBE_CONFIG_DATA secret
