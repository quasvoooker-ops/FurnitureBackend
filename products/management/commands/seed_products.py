from django.core.management.base import BaseCommand
from products.models import Product


PRODUCTS = [
    # Living Room
    {
        'name': 'Harlow Sofa',
        'description': 'A luxurious green velvet sofa with solid wood legs. Perfect centerpiece for any modern living room.',
        'price': 2180,
        'category': 'living',
        'rating': 4,
        'stock': 10,
        'is_available': True,
    },
    {
        'name': 'Vellum Chair',
        'description': 'Elegant accent chair with a sleek silhouette and premium fabric upholstery.',
        'price': 1599,
        'category': 'living',
        'rating': 4,
        'stock': 8,
        'is_available': True,
    },
    {
        'name': 'Velora Lounge',
        'description': 'Contemporary lounge chair with deep cushioning and a minimalist frame.',
        'price': 2990,
        'category': 'living',
        'rating': 3,
        'stock': 5,
        'is_available': True,
    },
    {
        'name': 'Ember Coffee Table',
        'description': 'Round coffee table with a warm walnut finish and slim tapered legs.',
        'price': 890,
        'category': 'living',
        'rating': 5,
        'stock': 12,
        'is_available': True,
    },
    {
        'name': 'Alcott Bookshelf',
        'description': 'Open-concept bookshelf with adjustable shelves and a natural oak finish.',
        'price': 1250,
        'category': 'living',
        'rating': 4,
        'stock': 7,
        'is_available': True,
    },
    {
        'name': 'Dune Side Table',
        'description': 'Compact side table with a stone-textured top and matte black metal base.',
        'price': 450,
        'category': 'living',
        'rating': 4,
        'stock': 15,
        'is_available': True,
    },
    # Bedroom
    {
        'name': 'Haven Bed Frame',
        'description': 'King-size bed frame with an upholstered headboard in soft linen fabric.',
        'price': 3200,
        'category': 'bedroom',
        'rating': 5,
        'stock': 6,
        'is_available': True,
    },
    {
        'name': 'Drift Dresser',
        'description': 'Six-drawer dresser with smooth glides and a Scandinavian-inspired design.',
        'price': 1800,
        'category': 'bedroom',
        'rating': 4,
        'stock': 8,
        'is_available': True,
    },
    {
        'name': 'Luna Nightstand',
        'description': 'Minimalist nightstand with a drawer and open shelf, available in white and oak.',
        'price': 520,
        'category': 'bedroom',
        'rating': 4,
        'stock': 20,
        'is_available': True,
    },
    {
        'name': 'Cozy Wardrobe',
        'description': 'Spacious two-door wardrobe with internal hanging rail and shelf storage.',
        'price': 2750,
        'category': 'bedroom',
        'rating': 3,
        'stock': 4,
        'is_available': True,
    },
    {
        'name': 'Serene Vanity',
        'description': 'Elegant vanity table with mirror and padded stool, perfect for morning routines.',
        'price': 1400,
        'category': 'bedroom',
        'rating': 5,
        'stock': 9,
        'is_available': True,
    },
    {
        'name': 'Rest Ottoman',
        'description': 'Upholstered bedroom ottoman with hidden storage inside.',
        'price': 680,
        'category': 'bedroom',
        'rating': 4,
        'stock': 11,
        'is_available': True,
    },
    # Dining
    {
        'name': 'Gather Dining Table',
        'description': 'Six-seater solid wood dining table with a natural finish and clean lines.',
        'price': 2600,
        'category': 'dining',
        'rating': 5,
        'stock': 5,
        'is_available': True,
    },
    {
        'name': 'Form Dining Chair',
        'description': 'Set of 2 upholstered dining chairs with tapered legs and cushioned seats.',
        'price': 780,
        'category': 'dining',
        'rating': 4,
        'stock': 16,
        'is_available': True,
    },
    {
        'name': 'Arch Sideboard',
        'description': 'Sleek sideboard with two doors and open shelf, ideal for dining storage.',
        'price': 1950,
        'category': 'dining',
        'rating': 4,
        'stock': 6,
        'is_available': True,
    },
    {
        'name': 'Bloom Bar Stool',
        'description': 'Counter-height bar stool with a swivel seat and footrest ring.',
        'price': 420,
        'category': 'dining',
        'rating': 3,
        'stock': 18,
        'is_available': True,
    },
    {
        'name': 'Mesa Bench',
        'description': 'Solid wood dining bench with a cushioned top, seats up to 3 people.',
        'price': 890,
        'category': 'dining',
        'rating': 4,
        'stock': 10,
        'is_available': True,
    },
    {
        'name': 'Crest China Cabinet',
        'description': 'Glass-door china cabinet with interior lighting and adjustable shelves.',
        'price': 2200,
        'category': 'dining',
        'rating': 5,
        'stock': 3,
        'is_available': True,
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with sample furniture products'

    def handle(self, *args, **kwargs):
        created_count = 0
        for data in PRODUCTS:
            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'{created_count} products created. {len(PRODUCTS) - created_count} already existed.'
        ))
