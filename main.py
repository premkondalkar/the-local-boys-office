#!/usr/bin/env python3
"""Main entry point for The Local Boys Office"""

import os
from dotenv import load_dotenv
from src.app import create_app

load_dotenv()

if __name__ == '__main__':
    app = create_app()
    
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║  🏢 The Local Boys Office - Automation Agents      ║
    ║  📊 Starting Server...                              ║
    ║  🌐 http://localhost:{port}                           ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=debug
    )