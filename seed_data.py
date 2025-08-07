from app import create_app, db
from app.models import Product, User

app = create_app()
app.app_context().push()

# Clear all existing products
Product.query.delete()
db.session.commit()

# New smartphone entries (sample of 30+)
products = [
    Product(name="iPhone 12", brand="Apple", price=59999, stock=10,
            description="6.1-inch OLED Super Retina XDR display | A14 Bionic chip delivers fast performance and efficiency | Dual 12MP cameras with Night mode | Ceramic Shield front for better drop performance | 5G connectivity for blazing-fast internet.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-12-pro--.jpg"),

    Product(name="iPhone 13", brand="Apple", price=69999, stock=12,
            description="A15 Bionic chip for improved speed and power efficiency | Super Retina XDR display offers vibrant colors and clarity | Cinematic mode for professional-style video shooting | Dual 12MP rear cameras with sensor-shift stabilization | 5G enabled for ultra-fast wireless performance.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-13.jpg"),

    Product(name="iPhone 13 Pro", brand="Apple", price=99999, stock=8,
            description="6.1-inch ProMotion display with 120Hz refresh rate | Triple 12MP camera system including ultra-wide and telephoto | A15 Bionic chip with 5-core GPU for gaming and creativity | ProRAW and ProRes for high-end photo and video editing | LiDAR scanner for advanced AR experiences and night portraits.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-13-pro.jpg"),

    Product(name="iPhone 14", brand="Apple", price=79999, stock=10,
            description="Same A15 chip with enhanced GPU | Crash detection and satellite SOS for emergencies | New Photonic Engine for improved low-light photography | Improved thermal performance for longer gaming | Long battery life with 5G support and iOS 16 features.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-14.jpg"),

    Product(name="iPhone 14 Pro", brand="Apple", price=129999, stock=7,
            description="6.1-inch Super Retina XDR with Always-On and ProMotion | Dynamic Island changes how you receive alerts and activities | A16 Bionic chip for ultimate performance | 48MP main camera for pro-level photography | All-day battery life and crash detection included.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-14-pro.jpg"),

    Product(name="iPhone 15", brand="Apple", price=89999, stock=6,
            description="Aluminum body with contoured edges for comfortable grip | A16 Bionic chip for performance and efficiency | Dynamic Island brings interactive notifications | USB-C support for universal charging | Advanced camera system with Photonic Engine.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15.jpg"),

    Product(name="iPhone 15 Pro", brand="Apple", price=139999, stock=5,
            description="Titanium design makes it strong and light | A17 Pro chip delivers desktop-level gaming | New Action button replaces mute switch for customization | Best-in-class camera system with new telephoto lens | Ray tracing for next-gen mobile gaming performance.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro.jpg"),

    Product(name="Google Pixel 6", brand="Google", price=49999, stock=10,
            description="6.4-inch AMOLED display with HDR support | First phone with Google Tensor chip for smart AI processing | Dual rear cameras with Magic Eraser and Real Tone | Built-in Titan M2 security chip for protection | Runs clean Android with long-term updates.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/google-pixel-6.jpg"),

    Product(name="Google Pixel 6 Pro", brand="Google", price=74999, stock=8,
            description="6.7-inch curved LTPO OLED display with 120Hz | Triple camera setup with 4x optical zoom | Google Tensor chip with ML features like Live Translate | 5000mAh battery with fast charging | High-end design with IP68 and Gorilla Glass Victus.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/google-pixel-6-pro.jpg"),

    Product(name="Google Pixel 7", brand="Google", price=59999, stock=10,
            description="Refined design with matte aluminum finish | 6.3-inch OLED display and Tensor G2 chip | Excellent camera with Real Tone and Guided Frame | Great low-light performance with Night Sight | Secure with Titan M2 chip and Face Unlock.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/google-pixel7-new.jpg"),

    Product(name="Google Pixel 7 Pro", brand="Google", price=84999, stock=6,
            description="Flagship device with 6.7-inch OLED display | 5x telephoto and macro focus camera features | Tensor G2 chip with VPN and voice typing enhancements | All-day battery life with intelligent adaptive features | Pure Android experience with Pixel-exclusive features.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/google-pixel7-pro-new.jpg"),

    Product(name="Google Pixel 8", brand="Google", price=69999, stock=10,
            description="Tensor G3 brings new AI experiences | Magic Editor for creative photo editing | 7 years of updates for long-term use | Enhanced OLED display with 120Hz refresh | Improved camera and better battery optimization.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8.jpg"),

    Product(name="Google Pixel 8 Pro", brand="Google", price=84999, stock=7,
            description="6.7-inch Super Actua display with 2400 nits peak | Best AI camera with Pro controls | Tensor G3 powers smart tools like Audio Magic Eraser | Temperature sensor for health and daily use | IP68 and Gorilla Glass Victus 2 for durability.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8-pro.jpg"),

    Product(name="Samsung Galaxy S21", brand="Samsung", price=69999, stock=9,
            description="Compact 6.2-inch Dynamic AMOLED 2X display | 120Hz refresh and HDR10+ support | Exynos 2100 for blazing fast performance | Triple rear cameras with 64MP zoom sensor | Glass front and back with Gorilla Glass Victus.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s21-ultra-5g-.jpg"),

    Product(name="Samsung Galaxy S22", brand="Samsung", price=74999, stock=8,
            description="Premium compact flagship with 6.1-inch AMOLED | Nightography features improve low-light shots | Snapdragon 8 Gen 1 for smooth multitasking | IP68 water resistance and stereo speakers | Aluminum Armor frame for solid build quality.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s22-5g.jpg"),

    Product(name="Samsung Galaxy S23", brand="Samsung", price=79999, stock=7,
            description="Refined design with flat edges and Gorilla Glass Victus 2 | 6.1-inch AMOLED with 120Hz refresh rate | Snapdragon 8 Gen 2 made for Galaxy | Upgraded camera processing with Nightography | Long-lasting battery with 25W fast charging.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s23-5g.jpg"),

    Product(name="Samsung Galaxy S23 Ultra", brand="Samsung", price=124999, stock=6,
            description="Ultimate flagship with 200MP main sensor | Integrated S-Pen for note taking and sketching | 6.8-inch WQHD+ AMOLED display | 5000mAh battery with 45W charging | Powerful zoom and RAW shooting capabilities.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s23-ultra-5g.jpg"),

    Product(name="Samsung Galaxy S24", brand="Samsung", price=84999, stock=10,
            description="6.2-inch AMOLED display with slimmer bezels | AI-powered features for enhanced productivity | Exynos 2400 or Snapdragon 8 Gen 3 (region specific) | Durable Armor Aluminum frame | All-day battery life and One UI 6.1 with Galaxy AI.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-5g-sm-s921.jpg"),

    Product(name="Samsung Galaxy S25 Ultra", brand="Samsung", price=134999, stock=4,
            description="Expected flagship with 200MP upgraded sensor | Galaxy AI 2.0 with enhanced on-device intelligence | S-Pen support with improved latency | Bigger and brighter AMOLED panel | Likely to ship with Snapdragon 8 Gen 4 chip.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s25-ultra-sm-s938.jpg"),

    Product(name="OnePlus 12", brand="OnePlus", price=69999, stock=10,
            description="6.82-inch QHD+ AMOLED with 120Hz refresh | Snapdragon 8 Gen 3 for extreme performance | Hasselblad-tuned cameras with RAW support | 100W SUPERVOOC fast charging and 50W wireless | Big 5400mAh battery for extended use.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/oneplus-12.jpg"),

    Product(name="Nothing Phone 1", brand="Nothing", price=29999, stock=15,
            description="Transparent back with Glyph interface | Snapdragon 778G+ optimized for smooth performance | 6.55-inch OLED with 120Hz refresh rate | Dual 50MP camera with OIS and EIS | Unique minimalist design and Nothing OS.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/nothing-cmf-phone-1-ofic.jpg"),

    Product(name="Nothing Phone 2", brand="Nothing", price=44999, stock=10,
            description="Premium upgrade with Snapdragon 8+ Gen 1 | Glyph interface enhanced for interactivity | 6.7-inch LTPO OLED with 1-120Hz adaptive refresh | 4700mAh battery with wireless and reverse charging | Clean and bloat-free Nothing OS experience.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/nothing-cmf-phone-2-pro.jpg"),

    Product(name="Samsung Galaxy M14", brand="Samsung", price=13999, stock=18,
            description="6.6-inch PLS LCD display with FHD+ resolution | 6000mAh massive battery for two-day use | Exynos 1330 with 5G support | Triple camera setup with 50MP main sensor | Budget-friendly option with Android 13 out of the box.",
            image_url="https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-m14-5g-sm-m146.jpg"),
]


# Insert and commit
db.session.bulk_save_objects(products)
db.session.commit()
print("📦 Database seeded with 30+ phones.")
