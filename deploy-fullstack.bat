@echo off
cls
echo ========================================================
echo    RAILWAY FULL STACK DEPLOYMENT
echo    Bitcoin Exporter + Prometheus + Grafana
echo ========================================================
echo.

echo Current Status:
echo [OK] Bitcoin Exporter - Already deployed
echo [ ] Prometheus - Ready to deploy
echo [ ] Grafana - Ready to deploy
echo.

echo --------------------------------------------------------
echo STEP 1: Open Railway Dashboard
echo --------------------------------------------------------
echo.
echo Opening your Railway project in browser...
start https://railway.app/project/788de3a1-37c8-4ab0-abeb-7afb1120be07
echo.
echo In the Railway Dashboard:
echo 1. Click "+ New" button
echo 2. Select "Empty Service"
echo 3. Name it: prometheus
echo.
pause

echo.
echo --------------------------------------------------------
echo STEP 2: Deploy Prometheus
echo --------------------------------------------------------
echo.
echo Switching to prometheus service...
railway link
echo.
echo Select "prometheus" from the list above
pause

echo.
echo Setting Prometheus Dockerfile path...
railway variables --set RAILWAY_DOCKERFILE_PATH=Dockerfile.prometheus
echo.
echo Deploying Prometheus...
railway up
echo.
timeout /t 10

echo.
echo Generating Prometheus domain...
railway domain
echo.
pause

echo.
echo --------------------------------------------------------
echo STEP 3: Add Grafana Service
echo --------------------------------------------------------
echo.
echo Go back to Railway Dashboard and:
echo 1. Click "+ New" button
echo 2. Select "Empty Service"
echo 3. Name it: grafana
echo.
start https://railway.app/project/788de3a1-37c8-4ab0-abeb-7afb1120be07
pause

echo.
echo --------------------------------------------------------
echo STEP 4: Deploy Grafana
echo --------------------------------------------------------
echo.
echo Switching to grafana service...
railway link
echo.
echo Select "grafana" from the list above
pause

echo.
echo Setting Grafana variables...
railway variables --set RAILWAY_DOCKERFILE_PATH=Dockerfile.grafana
railway variables --set GF_AUTH_ANONYMOUS_ENABLED=true
railway variables --set GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
railway variables --set GF_AUTH_DISABLE_LOGIN_FORM=true
echo.
echo Deploying Grafana...
railway up
echo.
timeout /t 10

echo.
echo Generating Grafana domain...
railway domain
echo.
pause

echo.
echo ========================================================
echo    DEPLOYMENT COMPLETE!
echo ========================================================
echo.
echo Your services should now be running:
echo.
echo 1. Bitcoin Exporter (already running)
echo 2. Prometheus (just deployed)
echo 3. Grafana (just deployed)
echo.
echo Access Grafana dashboard at the URL above!
echo.
echo ========================================================
pause
