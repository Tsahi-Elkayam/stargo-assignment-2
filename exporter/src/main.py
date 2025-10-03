"""Main application entry point."""
import time
import logging
import signal
import sys
import os
from prometheus_client import start_http_server, generate_latest, REGISTRY
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.loader import ConfigLoader
from collectors.bitcoin import BitcoinCollector


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BitcoinExporter:
    """Main Bitcoin price exporter application."""
    
    def __init__(self):
        """Initialize the exporter."""
        self.config = None
        self.collector = None
        self.running = True
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
    
    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info("Shutdown signal received, stopping exporter...")
        self.running = False
    
    def initialize(self):
        """Initialize application components."""
        try:
            # Load configuration
            config_loader = ConfigLoader()
            self.config = config_loader.load()
            
            # Configure logging
            log_level = self.config.get('logging', {}).get('level', 'INFO')
            logging.getLogger().setLevel(getattr(logging, log_level))
            
            # Initialize collector
            self.collector = BitcoinCollector(self.config)
            
            # Validate configuration
            if not self.collector.validate():
                raise ValueError("Invalid collector configuration")
            
            logger.info("Bitcoin exporter initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize exporter: {e}")
            sys.exit(1)
    
    def _start_health_server(self, port):
        """Start health check server."""
        class HealthHandler(BaseHTTPRequestHandler):
            def do_GET(handler_self):
                if handler_self.path == '/health':
                    handler_self.send_response(200)
                    handler_self.send_header('Content-type', 'application/json')
                    handler_self.end_headers()
                    status = {
                        'status': 'healthy' if self.running else 'shutting_down',
                        'collector': 'active' if self.collector else 'inactive'
                    }
                    handler_self.wfile.write(str(status).encode())
                elif handler_self.path == '/metrics':
                    handler_self.send_response(200)
                    handler_self.send_header('Content-type', 'text/plain')
                    handler_self.end_headers()
                    handler_self.wfile.write(generate_latest(REGISTRY))
                else:
                    handler_self.send_response(404)
                    handler_self.end_headers()
            
            def log_message(self, format, *args):
                # Suppress default logging
                pass
        
        server = HTTPServer(('', port), HealthHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        return server
    
    def run(self):
        """Run the exporter."""
        try:
            # Get configuration
            port = self.config.get('exporter', {}).get('port', 8000)
            interval = self.config.get('exporter', {}).get('interval', 60)
            
            # Start combined metrics and health server
            health_server = self._start_health_server(port)
            logger.info(f"Metrics server started on port {port}")
            logger.info(f"Health check available at http://localhost:{port}/health")
            
            # Initial collection
            self.collector.collect()
            
            # Main collection loop
            while self.running:
                try:
                    time.sleep(interval)
                    if self.running:
                        self.collector.collect()
                except Exception as e:
                    logger.error(f"Error during collection: {e}")
            
            logger.info("Exporter stopped")
            
        except Exception as e:
            logger.error(f"Failed to run exporter: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    exporter = BitcoinExporter()
    exporter.initialize()
    exporter.run()


if __name__ == '__main__':
    main()
