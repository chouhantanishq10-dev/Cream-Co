"""
Cream & Co. — Product State
==============================
Manages product catalog, categories, searching, and filtering.
"""

import reflex as rx
from sqlmodel import select, col
from typing import Optional, Any

from ..models.product import Product, Category
from ..services.seed_data import get_seed_categories, get_seed_products


class ProductState(rx.State):
    """State for browsing the product catalog."""

    # ── Data ──────────────────────────────────────────────────────────────
    products: list[dict[str, Any]] = []
    categories: list[dict[str, Any]] = []
    filtered_products: list[dict[str, Any]] = []
    bestsellers: list[dict[str, Any]] = []
    selected_product: dict[str, Any] = {}

    # ── Filters ───────────────────────────────────────────────────────────
    selected_category: str = "all"
    search_query: str = ""
    is_loading: bool = False
    is_seeded: bool = False

    # ─────────────────────────────────────────────────────────────────────
    # Data Loading
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def load_products(self):
        """Load all products and categories from the database."""
        self.is_loading = True
        try:
            with rx.session() as session:
                # Check if data exists, if not seed it
                cat_count = len(session.exec(select(Category)).all())
                if cat_count == 0:
                    self._seed_database(session)

                # Load categories
                cats = session.exec(
                    select(Category)
                    .where(Category.is_active == True)
                    .order_by(col(Category.display_order))
                ).all()
                self.categories = [
                    {
                        "id": c.id,
                        "name": c.name,
                        "slug": c.slug,
                        "description": c.description,
                        "image_url": c.image_url,
                    }
                    for c in cats
                ]

                # Load all products
                prods = session.exec(
                    select(Product).where(Product.is_available == True)
                ).all()
                self.products = [self._product_to_dict(p) for p in prods]
                self.filtered_products = self.products.copy()

                # Load bestsellers
                self.bestsellers = [
                    p for p in self.products if p.get("is_bestseller")
                ]

        except Exception as e:
            print(f"Error loading products: {e}")
        finally:
            self.is_loading = False

    def _seed_database(self, session):
        """Seed the database with initial catalog data."""
        # Insert categories
        cat_map = {}
        for cat_data in get_seed_categories():
            cat = Category(**cat_data)
            session.add(cat)
            session.flush()
            cat_map[cat.slug] = cat.id

        # Insert products
        for prod_data in get_seed_products():
            category_slug = prod_data.pop("category_slug")
            category_id = cat_map.get(category_slug, 1)
            product = Product(category_id=category_id, **prod_data)
            session.add(product)

        session.commit()
        print("✅ Database seeded with Cream & Co. catalog!")

    def _product_to_dict(self, p: Product) -> dict:
        """Convert a Product model instance to a serializable dict."""
        return {
            "id": p.id,
            "name": p.name,
            "slug": p.slug,
            "description": p.description,
            "price": p.price,
            "discount_price": p.discount_price,
            "image_url": p.image_url or "",
            "category_id": p.category_id,
            "is_veg": p.is_veg,
            "is_bestseller": p.is_bestseller,
            "is_available": p.is_available,
            "weight_info": p.weight_info,
            "stock_quantity": p.stock_quantity,
            "is_low_stock": 0 < p.stock_quantity <= 5,
        }

    # ─────────────────────────────────────────────────────────────────────
    # Filtering & Search
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def filter_by_category(self, category_slug: str):
        """Filter products by category slug."""
        self.selected_category = category_slug
        self._apply_filters()

    @rx.event
    def handle_search(self, query: str):
        """Update search query and filter products."""
        self.search_query = query
        self._apply_filters()

    def _apply_filters(self):
        """Apply category and search filters to product list."""
        filtered = self.products.copy()

        # Category filter
        if self.selected_category != "all":
            # Find category id by slug
            cat_id = None
            for c in self.categories:
                if c["slug"] == self.selected_category:
                    cat_id = c["id"]
                    break
            if cat_id is not None:
                filtered = [
                    p for p in filtered if p.get("category_id") == cat_id
                ]

        # Search filter
        if self.search_query.strip():
            query_lower = self.search_query.strip().lower()
            filtered = [
                p
                for p in filtered
                if query_lower in p.get("name", "").lower()
                or query_lower in p.get("description", "").lower()
            ]

        self.filtered_products = filtered

    # ─────────────────────────────────────────────────────────────────────
    # Single Product
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def load_product_by_slug(self):
        """Load a single product by its slug from URL params."""
        self.is_loading = True
        slug = self.router.page.params.get("slug", "")

        try:
            with rx.session() as session:
                product = session.exec(
                    select(Product).where(Product.slug == slug)
                ).first()

                if product:
                    self.selected_product = self._product_to_dict(product)
                else:
                    self.selected_product = {}
        except Exception as e:
            print(f"Error loading product: {e}")
            self.selected_product = {}
        finally:
            self.is_loading = False
