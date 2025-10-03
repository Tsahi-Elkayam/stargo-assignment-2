@echo off
REM ========================================
REM AUTOMATED CLOUD DEPLOYMENT
REM Deploy and forget - runs in cloud!
REM ========================================

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║         AUTOMATED CLOUD DEPLOYMENT - CHOOSE YOUR OPTION         ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Your Bitcoin Exporter is ALREADY running on Railway!
echo Logs show: Bitcoin price updating every 60 seconds ✅
echo.
echo ========================================
echo SELECT DEPLOYMENT OPTION:
echo ========================================
echo.
echo [1] Complete Railway Deployment (Current - Partial)
echo     Status: Exporter deployed ✅, need Prometheus + Grafana
echo     Cost: ~$15/month after $5 credit
echo     Time: 5 minutes (manual steps)
echo.
echo [2] Deploy to Render.com (FREE Forever) ⭐
echo     Status: render.yaml created ✅
echo     Cost: FREE (services sleep when inactive)
echo     Time: 2 minutes (fully automated)
echo.
echo [3] Deploy to Fly.io (Best Automation) 🚀
echo     Status: Ready to deploy
echo     Cost: FREE (3 VMs included)
echo     Time: 1 minute (100%% CLI automated)
echo.
echo [4] Show Current Railway Status
echo.
echo [5] Exit
echo.

set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto railway
if "%choice%"=="2" goto render
if "%choice%"=="3" goto flyio
if "%choice%"=="4" goto status
if "%choice%"=="5" goto end

:railway
echo.
echo ========================================
echo COMPLETING RAILWAY DEPLOYMENT
echo ========================================
echo.
echo Your Exporter URL:
railway domain
echo.
echo To complete Railway deployment:
echo 1. Open: https://railway.app/project/788de3a1-37c8-4ab0-abeb-7afb1120be07
echo 2. Create "Prometheus" service (use Dockerfile.prometheus)
echo 3. Create "Grafana" service (use Dockerfile.grafana)
echo.
echo Opening Railway dashboard...
start https://railway.app/project/788de3a1-37c8-4ab0-abeb-7afb1120be07
echo.
echo ✅ Once deployed, you can CLOSE THIS WINDOW
echo    Services run 24/7 in Railway cloud!
echo.
pause
goto end

:render
echo.
echo ========================================
echo DEPLOYING TO RENDER.COM (FREE)
echo ========================================
echo.
python deploy-automated.py
echo.
pause
goto end

:flyio
echo.
echo ========================================
echo DEPLOYING TO FLY.IO (AUTOMATED)
echo ========================================
echo.
echo Step 1: Install Fly CLI (if not installed)
echo.
where fly >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Fly CLI...
    powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
    echo.
    echo ✅ Fly CLI installed!
    echo Please close and reopen this terminal, then run this script again.
    pause
    goto end
)

echo ✅ Fly CLI found
echo.
echo Step 2: Login to Fly.io
fly auth login
echo.
echo Step 3: Deploy Bitcoin Exporter
fly launch --name bitcoin-exporter --config fly.exporter.toml --now --yes
echo.
echo ========================================
echo ✅ DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your services are now running in Fly.io cloud!
echo You can CLOSE THIS WINDOW - services run 24/7
echo.
echo View your app: fly open
echo Check status: fly status
echo View logs: fly logs
echo.
pause
goto end

:status
echo.
echo ========================================
echo CURRENT RAILWAY STATUS
echo ========================================
echo.
railway status
echo.
echo Services:
railway ps
echo.
echo Recent logs:
railway logs --num 20
echo.
pause
goto end

:end
echo.
echo Goodbye!
