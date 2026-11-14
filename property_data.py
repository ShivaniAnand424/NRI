"""
property_data.py
----------------
All property listings live here. To add a property, copy one block and edit it.
To move a property from "sale" to "sold", just change  "status".

PUBLIC fields   -> visible to everyone (name, location, summary, card_facts, highlights, amenities)
LOCKED fields   -> visible only after Client Login / Register
                   (price, private_facts, video_url, and the files in /private_files/<slug>/)

Fields marked  TODO  were not printed in the brochure - fill them in.
"""
import os

# Your WhatsApp number in international format, digits only (e.g. 919876543210).
# Better: set it as an environment variable  NRI_WHATSAPP  instead of editing here.
WHATSAPP_NUMBER = os.environ.get("NRI_WHATSAPP", "91XXXXXXXXXX")  # TODO

PARTNER_LINE = "In association with Shree Hari Realtors"

PROPERTIES = [
    # ------------------------------------------------------------------ SOLD
    {
        "slug": "keshavam-15",
        "name": "Nirmal Keshavam-15",
        "developer": "Nirmal",
        "type": "Residential Plotted Layout",
        "status": "sold",                       # "sold" or "sale"
        "location": "Nagpur, Maharashtra",      # TODO: add exact locality
        "summary": (
            "A premium gated plotted layout with a full clubhouse, swimming pool "
            "and a proposed CBSE school, planned around wide internal roads and "
            "generous open space."
        ),
        "card_facts": [
            ("Plots", "87"),
            ("Plot size", "102 – 443 sq.m"),
            ("Road width", "9 m / 12 m / 18 m D.P."),
        ],
        "highlights": [
            "87 residential plots in a gated community",
            "18 m wide D.P. road frontage",
            "2,405 sq.m dedicated open space",
            "Proposed CBSE school within the project",
        ],
        "amenities": [
            "Swimming Pool", "Gym", "Proposed CBSE School", "Pool Table",
            "Yoga Room", "Table Tennis", "Party Lawn", "Restaurant",
            "Pergola Seating", "Security Entry Gate", "Electricity",
            "Clubhouse", "Green Gym", "Kids Play Area",
        ],
        "sold_note": "Fully transacted and managed for NRI & domestic clients.",
        "image": "images/properties/keshavam-15.jpg",
        # ---- locked ----
        "price": None,          # sold price is not shown; for "sale" use e.g. "₹ 45,00,000 onwards"
        "private_facts": [
            ("Plot sizes", "102.48 – 443.35 sq.m (1,103 – 4,772 sq.ft)"),
            ("Most common plot", "105 sq.m (1,130 sq.ft)"),
            ("Open space", "2,405.46 sq.m"),
            ("Internal roads", "9 m and 12 m wide, 18 m wide D.P. road"),
        ],
        "video_url": None,      # e.g. "https://www.youtube.com/embed/XXXXXXXX"
        "layout_file": "keshavam-15/layout.jpg",     # inside /private_files
        "brochure_file": None,                       # e.g. "keshavam-15/brochure.pdf"
    },
    {
        "slug": "keshavam-city-11",
        "name": "Keshavam City-11",
        "developer": "Keshavam",
        "type": "Residential Plotted Layout",
        "status": "sold",
        "location": "Nagpur, Maharashtra",      # TODO: add exact locality
        "summary": (
            "Where living flourishes in nature's grasp - a clubhouse-led layout "
            "with pool, restaurant and landscaped open areas."
        ),
        "card_facts": [
            ("Plots", "69"),
            ("Plot size", "105 – 421 sq.m"),
            ("Road width", "9 m / 12 m / 18 m D.P."),
        ],
        "highlights": [
            "69 residential plots",
            "18 m wide proposed D.P. road",
            "Clubhouse with swimming pool and restaurant",
            "Landscaped gardens and pergola seating",
        ],
        "amenities": [
            "Swimming Pool", "Gym", "Table Tennis", "Pool Table", "Yoga Room",
            "Carrom", "Party Lawn", "Restaurant", "Pergola Seating",
            "Security Entry Gate", "Electricity", "Clubhouse", "Green Gym",
            "Kids Play Area",
        ],
        "sold_note": "Fully transacted and managed for NRI & domestic clients.",
        "image": "images/properties/keshavam-city-11.jpg",
        "price": None,
        "private_facts": [
            ("Plot sizes", "approx. 105 – 421 sq.m (1,130 – 4,537 sq.ft)"),
            ("Most common plot", "105 sq.m (1,130 sq.ft)"),
            ("Internal roads", "9 m and 12 m wide, 18 m wide proposed D.P. road"),
        ],
        "video_url": None,
        "layout_file": "keshavam-city-11/layout.jpg",
        "brochure_file": None,
    },
    {
        "slug": "saraswati-nagar-3",
        "name": "Saraswati Nagar-3",
        "developer": "Saraswati Land Developer & Builders",
        "type": "RERA Residential Layout",
        "status": "sold",
        "location": "Mouza Rui, Nagpur (Gramin), near New Outer Ring Road",
        "summary": (
            "A final-demarcated RERA-registered residential layout close to the "
            "New Outer Ring Road and the MIHAN corridor, with cement roads, "
            "water supply and fenced boundary."
        ),
        "card_facts": [
            ("Plots", "57"),
            ("Plot size", "95 – 454 sq.m"),
            ("RERA", "P50500049467"),
        ],
        "highlights": [
            "RERA registered: P50500049467",
            "KH No. 1/1 and 1/2, P.H. No. 41, Mouza Rui",
            "Near New Outer Ring Road, MIHAN and Khapri Metro",
            "Open and amenity space of over 1,700 sq.m",
        ],
        "amenities": [
            "Entry Gate", "Water Supply", "Sewage Pipe Line",
            "Road Side Tree Plantation", "Cement Road", "Green Gym",
            "Storm Water Drainage", "Layout Fencing & Demarcation",
        ],
        "sold_note": "Fully transacted and managed for NRI & domestic clients.",
        "image": "images/properties/saraswati-nagar-3.jpg",
        "price": None,
        "private_facts": [
            ("KH No. 1/1", "26 plots, 94.50 – 453.73 sq.m"),
            ("KH No. 1/2", "31 plots, 96.75 – 370.56 sq.m"),
            ("Open spaces", "587.87 sq.m and 759.92 sq.m"),
            ("Amenity space", "399.08 sq.m"),
            ("Roads", "9 m and 12 m internal, 18 m wide O.D.R. No. 160"),
        ],
        "video_url": None,
        "layout_file": "saraswati-nagar-3/layout.jpg",
        "extra_files": [("Plot-wise size chart", "saraswati-nagar-3/plot-sizes.jpg")],
        "brochure_file": None,
    },
    {
        "slug": "sai-pride-iii",
        "name": "Sai Pride-III",
        "developer": "Vision Infrastructures",
        "type": "1, 2 & 3 BHK Apartments",
        "status": "sold",
        "location": "Plot 127-128, New Aakash Nagar, Manewada, Nagpur - 440024",
        "summary": (
            "Luxurious 1, 2 and 3 BHK flats near Manewada Square with lift, "
            "CCTV, EV charging point and parking."
        ),
        "card_facts": [
            ("Configuration", "1, 2 & 3 BHK"),
            ("Super built-up", "850 – 1,300 sq.ft"),
            ("Lift", "8-passenger"),
        ],
        "highlights": [
            "RCC framed structure, modular kitchen with granite top",
            "Vitrified tiles, concealed wiring, branded fittings",
            "8-passenger lift, CCTV in parking, EV charging point",
            "Car and two-wheeler parking",
        ],
        "amenities": [
            "8 Passenger Lift", "CCTV in Parking Area", "EV Charging Point",
            "Car & 2-Wheeler Parking", "Video Door Phone", "Cable TV Connection",
        ],
        "sold_note": "Fully transacted and managed for NRI & domestic clients.",
        "image": "images/properties/sai-pride-iii.jpg",
        "price": None,
        "private_facts": [
            ("Flat 101", "1,300 sq.ft super built-up"),
            ("Flat 102", "850 sq.ft super built-up"),
            ("Typical floors 2 - 6", "1,050 sq.ft super built-up"),
            ("Marketed by", "Shree Hari Realtors"),
        ],
        "video_url": None,
        "layout_file": "sai-pride-iii/layout.jpg",
        "extra_files": [("Typical 2nd - 6th floor plan", "sai-pride-iii/typical-floor.jpg")],
        "brochure_file": None,
    },

    # ------------------------------------------------------------------ FOR SALE
    # Copy this template when you have a live listing, then set "status": "sale".
    #
    # {
    #     "slug": "my-new-listing",
    #     "name": "Project Name",
    #     "developer": "Developer",
    #     "type": "3 BHK Apartment",
    #     "status": "sale",
    #     "location": "Area, Nagpur",
    #     "summary": "Two lines about the property.",
    #     "beds": 3, "baths": 3,
    #     "card_facts": [("Area", "1,300 sq.ft"), ("Floor", "4th")],
    #     "highlights": ["...", "..."],
    #     "amenities": ["Lift", "Parking"],
    #     "image": "images/properties/my-new-listing.jpg",
    #     "price": "₹ 85,00,000",
    #     "private_facts": [("Carpet area", "1,050 sq.ft")],
    #     "video_url": "https://www.youtube.com/embed/XXXX",
    #     "layout_file": "my-new-listing/layout.jpg",
    #     "brochure_file": "my-new-listing/brochure.pdf",
    # },
]
