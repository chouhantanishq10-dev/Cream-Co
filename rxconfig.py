import reflex as rx
import os
from reflex_base.plugins.sitemap import SitemapPlugin

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

config = rx.Config(
    app_name="CreamAndCo",
    # Database connection - Supabase PostgreSQL
    db_url=os.getenv(
        "DATABASE_URL",
        "sqlite:///reflex.db"  # Fallback for development
    ),
    plugins=[
        rx.plugins.TailwindV4Plugin(),
    ],
    disable_plugins=[SitemapPlugin],
)