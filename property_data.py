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

    {
        "slug": "mukunda-keshavam-9",
        "name": "Mukunda Keshavam-9",
        "developer": "Keshavam Infra",
        "type": "Residential Plotted Layout",
        "status": "sold",
        "location": "Kh. No. 67, Mouza Wagdara, Tah. Hingna, Nagpur",
        "summary": (
            "A residential plotted layout in Hingna with a clubhouse, open and "
            "amenity spaces, and frontage on a proposed 24 m wide road, close to "
            "the upcoming metro stations and Hingna-Wanadongri Road."
        ),
        "card_facts": [
            ("Plots", "28"),
            ("Plot size", "204 – 2,257 sq.m"),
            ("Road width", "9 m / 24 m"),
        ],
        "highlights": [
            "28 residential plots",
            "Proposed 24 m wide road and 9 m internal roads",
            "Clubhouse, open space and amenity space",
            "Near upcoming metro stations, D-Mart and Hingna Tehsil",
        ],
        "amenities": [
            "Green Gym", "Kids Play Area", "Landscape Garden",
            "Security Entry Gate", "Jogging Track", "Senior Sit Out",
            "Cement Road", "Storm Water Drain", "Rain Water Harvesting",
            "Electricity", "Clubhouse",
        ],
        "sold_note": "Fully transacted and managed for NRI & domestic clients.",
        "image": "images/properties/mukunda-keshavam-9.jpg",
        "price": None,
        "private_facts": [
            ("Survey details", "Kh. No. 67, Mouza Wagdara, Tah. Hingna, Dist. Nagpur"),
            ("Plot sizes", "203.94 – 2,257.24 sq.m (2,195 – 24,297 sq.ft)"),
            ("Most common plot", "266.46 sq.m (2,868 sq.ft), plots 4 to 6"),
            ("Roads", "9 m internal, proposed 24 m wide road"),
            ("Nearby", "Upcoming metro stations, D-Mart, Hingna Tehsil Office, "
                       "Sant Gadge Maharaj College, G.H. Raisoni Public School, "
                       "Cummins College of Engineering"),
        ],
        "video_url": None,
        "layout_file": "mukunda-keshavam-9/layout.jpg",
        "brochure_file": None,
    },
    {
        "slug": "oshian-super-city-3",
        "name": "Oshian Super City-3",
        "developer": "Oshian Realtors India Pvt. Ltd.",
        "type": "Residential & Commercial Plots",
        "status": "sold",
        "location": "Kh. No. 151, opposite Atharva Nagri-6, Besa-Pipla Road, Nagpur - 440034",
        "summary": (
            "An NMRDA-approved layout of 51 plots across 4.99 acres, with wide "
            "roads on all sides, a children's park, STP and underground "
            "electrification, on the Besa-Pipla Road corridor."
        ),
        "card_facts": [
            ("Plots", "51"),
            ("Land area", "4.99 acres"),
            ("RERA", "P50500034657"),
        ],
        "highlights": [
            "RERA registered: P50500034657",
            "NMRDA approved",
            "51 plots on 4.99 acres, commercial and residential",
            "Wide roads on all sides (9 m, 12 m and 12 m D.P. road)",
        ],
        "amenities": [
            "Cement Road", "Drainage Line", "Drinking Water Line",
            "Tree Plantation", "STP", "Sewer Line", "Garden Fencing",
            "Underground Electrification", "Children Park",
            "Storm Water Drainage Network",
        ],
        "sold_note": "Fully transacted and managed for NRI & domestic clients.",
        "image": "images/properties/oshian-super-city-3.jpg",
        "price": None,
        "private_facts": [
            ("RERA No.", "P50500034657"),
            ("Survey details", "Kh. No. 151, opposite Atharva Nagri-6, Besa-Pipla Road"),
            ("Total plots", "51"),
            ("Land area", "4.99 acres"),
            ("Open space", "1,121.98 sq.m (12,077 sq.ft)"),
            ("Roads", "9 m and 12 m wide, 12 m proposed D.P. road"),
        ],
        "video_url": None,
        "layout_file": "oshian-super-city-3/layout.jpg",
        "brochure_file": None,
    },
    {
        "slug": "kasturi-hills",
        "name": "Kasturi Hills",
        "developer": "Ozen Realtors India Pvt. Ltd.",
        "type": "RERA Residential Plotted Layout",
        "status": "sold",
        "location": "Beside Paradise Hills, Mouza Waghdara, Tah. Hingna, Nagpur - 441110",
        "summary": (
            "An NMRDA-sanctioned, RERA-registered plotted layout touching an 80 ft "
            "road, next to Paradise Hills and Greenfield Township, within a short "
            "drive of MIHAN, AIIMS and Hingna Road."
        ),
        "card_facts": [
            ("Plots", "79"),
            ("Plot size", "approx. 75 – 273 sq.m"),   # TODO: verify min/max from the area table
            ("RERA", "P50500031145"),
        ],
        "highlights": [
            "RERA registered: P50500031145",
            "NMRDA sanctioned",
            "80 ft road touch, adjacent to Paradise Hills",
            "MIHAN 2 km, AIIMS 7 minutes, D-Mart 1.5 km",
        ],
        "amenities": [
            "9 m and 12 m Internal Roads", "Open Space", "Amenity Space",
            "Layout Fencing",
        ],
        "sold_note": "Fully transacted and managed for NRI & domestic clients.",
        "image": "images/properties/kasturi-hills.jpg",
        "price": None,
        "private_facts": [
            ("RERA No.", "P50500031145"),
            ("Survey details", "Kh. No. 75/B/2, P.H. No. 46, Mouza Waghdara, Tah. Hingna"),
            ("Total plots", "79"),
            ("Amenity space", "1,616.27 sq.m"),
            ("Roads", "9 m and 12 m internal; 24 m wide road; 80 ft road touch"),
            ("Nearby", "Greenfield Township 500 m, Hingna Road 1.5 km, D-Mart 1.5 km, "
                       "Raisoni College 2.5 km, YCCE 2.5 km, Lata Mangeshkar Hospital 3 km, "
                       "MIHAN 2 km, AIIMS 7 min"),
        ],
        "video_url": None,
        "layout_file": "kasturi-hills/layout.jpg",
        "extra_files": [("Plot-wise area chart", "kasturi-hills/plot-sizes.jpg")],
        "brochure_file": None,
    },
    {
        "slug": "saraswati-nagar-5",
        "name": "Saraswati Nagar-5",
        "developer": "Saraswati Land Developer & Builders",
        "type": "Residential Layout",
        "status": "sold",
        "location": "Kh. No. 10, P.H. No. 41, Mouza Rui, Tah. Nagpur (Gramin)",
        "summary": (
            "A final-demarcated residential layout of 61 plots at Mouza Rui, with "
            "cement roads, water supply, fencing and two landscaped open spaces."
        ),
        "card_facts": [
            ("Plots", "61"),
            ("Plot size", "105 – 372 sq.m"),
            ("Road width", "9 m / 12 m / 15 m"),
        ],
        "highlights": [
            "61 plots in a final-demarcated layout",
            "15 m wide road frontage",
            "Open spaces of 585 sq.m and 755 sq.m",
            "Entry gate, cement roads and green gym",
        ],
        "amenities": [
            "Entry Gate", "Water Supply", "Sewage Pipe Line",
            "Road Side Tree Plantation", "Cement Road", "Green Gym",
            "Storm Water Drainage", "Layout Fencing & Demarcation",
        ],
        "sold_note": "Fully transacted and managed for NRI & domestic clients.",
        "image": "images/properties/saraswati-nagar-5.jpg",
        "price": None,
        "private_facts": [
            ("Survey details", "Kh. No. 10, P.H. No. 41, Mouza Rui, Tah. Nagpur (Gramin)"),
            ("Plot sizes", "105.00 – 372.22 sq.m (1,130 – 4,007 sq.ft)"),
            ("Most common plot", "105 sq.m (1,130 sq.ft)"),
            ("Open space A", "585.25 sq.m"),
            ("Open space B", "755.38 sq.m"),
            ("Roads", "9 m, 12 m and 15 m wide"),
        ],
        "video_url": None,
        "layout_file": "saraswati-nagar-5/layout.jpg",
        "extra_files": [("Plot-wise size chart", "saraswati-nagar-5/plot-sizes.jpg")],
        "brochure_file": None,
    },
    {
        "slug": "ozen-city",
        "name": "Ozen City",
        "developer": "Ozen Realtors India Pvt. Ltd.",
        "type": "Plotted Smart City (Phase I & II)",
        "status": "sold",
        "location": "Off Wardha Road, Nagpur",      # TODO: add exact locality
        "summary": (
            "A 32-acre, well-planned smart-city layout in two phases, organised "
            "around a 200 ft D.P. road, with landscaped avenues and dedicated "
            "open and amenity spaces."
        ),
        "card_facts": [
            ("Land area", "32 acres"),
            ("Phases", "2"),
            ("Main road", "200 ft D.P. road"),
        ],
        "highlights": [
            "32-acre integrated layout",
            "200 ft wide D.P. road through the project",
            "Phase I and Phase II plotted development",
            "Close to Wardha Road",
        ],
        "amenities": [
            "200 ft D.P. Road", "Landscaped Avenues", "Open Spaces",
            "Amenity Spaces", "Internal Roads",
        ],
        "sold_note": "Fully transacted and managed for NRI & domestic clients.",
        "image": "images/properties/ozen-city.jpg",
        "price": None,
        "private_facts": [
            ("Phase I plottable area", "580,601.55 sq.ft"),
            ("Phase I open space", "85,395.33 sq.ft"),
            ("Phase I amenity space", "45,000.63 sq.ft"),
            ("Phase II plottable area", "109,530.80 sq.ft"),
            ("Phase II open space", "21,965.87 sq.ft"),
            ("Phase II amenity space", "11,061.19 sq.ft"),
        ],  # TODO: confirm the units (sq.ft vs sq.m) on the brochure's totals table
        "video_url": None,
        "layout_file": "ozen-city/layout.jpg",
        "extra_files": [
            ("Phase I plot chart", "ozen-city/phase-1.jpg"),
            ("Phase II plot chart", "ozen-city/phase-2.jpg"),
        ],
        "brochure_file": None,
    },

    {
        "slug": "highway-prime-mouza-panjari",
        "name": "Highway Prime - Mouza Panjari",
        "developer": "Shree Hari Realtors",
        "type": "Residential Plotted Layout",
        "status": "sale",
        "location": "Mouza Panjari, Nagpur, Maharashtra",
        "summary": (
            "A premium residential plotted layout close to the Outer Ring Road, "
            "with strong everyday connectivity, nearby schools, metro access and "
            "a future-ready lifestyle environment for families."
        ),
        "card_facts": [
            ("Plots", "48"),
            ("Plot size", "95 – 454 sq.m"),
            ("Road width", "9 m / 12 m / 18 m"),
            ("Location", "Outer Ring Road touch"),
        ],
        "highlights": [
            "48 residential plots in a premium gated layout",
            "Near Mouza Panjari and the Outer Ring Road corridor",
            "Excellent access to schools, hospitals, metro, and city landmarks",
            "Open spaces, entry gate, and long-term appreciation potential",
        ],
        "amenities": [
            "Entry Gate", "Water Supply", "Cement Road", "Sewage Pipeline",
            "Roadside Tree Plantation", "Green Gym", "Storm Water Drainage",
            "Layout Fencing & Demarcation",
        ],
        "image": "images/properties/highway-prime-mouza-panjari.jpg",
        "price": "₹ On request",
        "private_facts": [
            ("Connectivity", "Near Outer Ring Road, MIHAN and Khapri Metro"),
            ("Nearby landmarks", "Orange Grove School, NCI, Mihan, Samruddhi Circle"),
            ("Project type", "Gated plotted residential development"),
            ("Marketed by", "Shree Hari Realtors"),
        ],
        "video_url": None,
        "layout_file": "highway-prime-mouza-panjari/layout.jpg",
        "brochure_file": None,
    },
    {
        "slug": "avinya-enclave",
        "name": "Avinya Enclave",
        "developer": "Agarkar Builders",
        "type": "Premium 3 BHK apartments",
        "status": "ongoing",
        "location": "Narendra Nagar, Nagpur",
        "summary": (
            "A boutique building with only six 3 BHK homes across G+6 floors and one "
            "residence per floor, for complete privacy. It stands just behind Narendra "
            "Nagar Post Office, in a well-connected and established neighbourhood."
        ),
        "card_facts": [
            ("Units", "6 flats"),
            ("Size", "1,250 sq.ft carpet / 1,450 sq.ft super built-up"),
            ("Floors", "G+6"),
        ],
        "highlights": [
            "Only 6 flats",
            "1 floor = 1 residence",
            "Modular kitchen",
            "CCTV and secure entry",
        ],
        "amenities": [
            "Spacious 3 BHK flats",
            "Only 6 exclusive flats in the building",
            "One residence per floor",
            "Secure entry system",
            "Lift access",
            "Parking space",
            "Modular kitchen",
            "CCTV surveillance",
            "Well-lit common passages",
        ],
        "nearby": [
            ("Narendra Nagar Square", "650 m, about 2 min"),
            ("Chhatrapati Metro Station", "2 km, about 5 min"),
            ("Jaiprakash Nagar Metro Station", "2 km, about 5 min"),
            ("Shri Durga Devi Mandir and Indian Oil petrol pump", "450 m, about 2 min"),
            ("Success Point School", "600 m, about 3 min"),
            ("Suyog Hospital", "600 m, about 3 min"),
        ],
        "image": "images/properties/avinya-enclave.jpg",
        "price": "₹80 lakh",
        "price_note": "Selling rate for a 3 BHK flat. Our team will confirm what is included.",
        "private_facts": [
            ("Location", "Behind Narendra Nagar Post Office, Shri Hari Society, Narendra Nagar, Nagpur"),
            ("Developer", "Agarkar Builders"),
            ("Marketed by", "Shree Hari Realtors"),
            ("Configuration", "All 3 BHK, one residence per floor"),
            ("Total flats", "6"),
            ("Floors", "G+6"),
            ("Land area", "2,400 sq.ft"),
            ("Carpet area", "1,250 sq.ft"),
            ("Super built-up area", "1,450 sq.ft"),
            ("More places nearby", "Swasthyam Superspeciality Hospital 7 min, Shri Krishna Super Bazar 5 min, Suyog Nagar Garden 3 min, NIT Garden 10 min, Kidzee Preschool 10 min, Haldiram's 15 min"),
        ],
        "video_url": None,
        "layout_file": "avinya-enclave/layout.jpg",
        "brochure_file": "avinya-enclave.pdf",
        "map_url": "https://maps.app.goo.gl/QzDxmRKiCWgj7pFf9",
        "details": [
            ("Location", "Behind Narendra Nagar Post Office, Shri Hari Society, Narendra Nagar, Nagpur"),
            ("Developer", "Agarkar Builders"),
            ("Marketed by", "Shree Hari Realtors"),
            ("Configuration", "All 3 BHK, one residence per floor"),
            ("Total flats", "6"),
            ("Floors", "G+6"),
            ("Land area", "2,400 sq.ft"),
            ("Carpet area", "1,250 sq.ft"),
            ("Super built-up area", "1,450 sq.ft"),
            ("More places nearby", "Swasthyam Superspeciality Hospital 7 min, Shri Krishna Super Bazar 5 min, Suyog Nagar Garden 3 min, NIT Garden 10 min, Kidzee Preschool 10 min, Haldiram's 15 min"),
        ],
        "specs": [
            ("Structure", ["Earthquake-resistant RCC-framed structure"]),
            ("Walls", ["Internal: 115 mm thick brick masonry", "External: 150 mm thick brick masonry"]),
            ("Painting", ["Internal: putty finish with acrylic emulsion paint", "External: waterproof acrylic paint", "POP in hall and master bedroom"]),
            ("Doors and windows", ["Entrance door: teakwood veneer", "Internal doors: laminated flush doors", "Toilet doors: laminated doors", "Windows: powder-coated aluminium sliding windows with MS safety grills"]),
            ("Kitchen", ["Modular kitchen in each flat", "Granite countertop with stainless steel sink", "Glazed ceramic tiles up to lintel level", "Power points for fridge, oven, chimney and water purifier", "Tap fittings for sink"]),
            ("Bathrooms", ["Waterproofing with coba treatment", "Concealed plumbing with PVC pipes", "Coloured ceramic dado tiles up to lintel level", "Sanitary ware and bath fittings", "Provision for geyser and exhaust fan"]),
            ("Flooring", ["Drawing, dining, bedrooms, kitchen and lobby: double-charged digital vitrified tiles", "Toilets: anti-skid tiles", "Staircase: granite or full-body vitrified tiles", "Granite frames for lift door"]),
            ("Electrical", ["Concealed wiring with adequate electrical points", "ISI-standard modular switches or equivalent", "Provision for inverter wiring", "AC points in hall and master bedroom", "TV points in hall and master bedroom"]),
            ("Water supply", ["Overhead water tank", "Underground water storage", "Separate pipeline for corporation water and borewell water", "Borewell available"]),
        ],
        "card": "avinya-enclave-card.jpg",
        "hero": "avinya-enclave-hero.jpg",
        "gallery": [
            ("avinya-enclave-site-1.jpg", "Site progress: foundation work"),
            ("avinya-enclave-site-2.jpg", "Site progress: excavation"),
        ],
        "plans": [
            ("3 BHK floor plan and 3D view", "avinya-enclave-floor-plan.jpg"),
            ("Location map and key distances", "avinya-enclave-location.jpg"),
            ("Premium materials used", "avinya-enclave-materials.jpg"),
        ],
    },

        {
        "slug": "nagpur-marina",
        "name": "Nagpur Marina",
        "developer": "The House of Abhinandan Lodha",
        "type": "Luxury Villa Land",
        "status": "ongoing",
        "location": "Near Samruddhi Circle, Nagpur",   # TODO: add exact locality
        "summary": (
            "A master-planned 78-acre luxury land development with a 3-acre "
            "man-made beach and 40+ amenities, close to Samruddhi Circle, "
            "MIHAN-SEZ and the proposed IBFC."
        ),
        "card_facts": [
            ("Land area", "78 acres"),
            ("Signature feature", "3-acre man-made beach"),
            ("RERA", "PP1190002502095"),      # TODO: verify against the brochure
        ],
        "highlights": [
            "78 acres of integrated, low-density planning",
            "3-acre man-made beach as the central feature",
            "40+ world-class amenities",
            "Samruddhi Circle 5 min, MIHAN-SEZ 10 min",
        ],
        "amenities": [
            "3-Acre Man-Made Beach", "40+ Amenities", "Integrated Lifestyle Ecosystem",
            "Low-Density Planning", "Experience-Led Planning",
        ],
        "nearby": [
            ("Samruddhi Circle", "5 min"),
            ("MIHAN - SEZ", "10 min"),
            ("IBFC", "10 min"),
            ("Butibori MIDC", "20 min"),
            ("Hingna MIDC", "20 min"),
            ("International Airport", "25 min"),
        ],
        "image": "images/properties/nagpur-marina.jpg",
        "price": "₹ On request",
        "price_note": "Our team will share current pricing and availability.",
        "private_facts": [
            ("RERA No.", "PP1190002502095"),
            ("Developer", "The House of Abhinandan Lodha"),
            ("Marketed by", "Shree Hari Realtors"),
            ("Project type", "Branded villa land in a master-planned ecosystem"),
            ("Total area", "78 acres"),
            ("Key feature", "3-acre man-made beach"),
            ("Amenities", "40+"),
        ],
        "video_url": None,
        "layout_file": "nagpur-marina/layout.jpg",
        "brochure_file": None,
        "map_url": "",
        "details": [
            ("RERA No.", "PP1190002502095"),
            ("Developer", "The House of Abhinandan Lodha"),
            ("Marketed by", "Shree Hari Realtors"),
            ("Project type", "Branded villa land in a master-planned ecosystem"),
            ("Total area", "78 acres"),
            ("Key feature", "3-acre man-made beach"),
            ("Amenities", "40+"),
        ],
        "specs": [],
        "card": "nagpur-marina-card.jpg",
        "hero": "nagpur-marina-hero.jpg",
        "gallery": [],
        "plans": [],
    },
    {
        "slug": "kalpataru-launch-code-nagpur",
        "name": "Kalpataru Launch Code Nagpur",
        "developer": "Kalpataru",
        "type": "Premium Plotted Development",
        "status": "ongoing",
        "location": "Khadka, Hingna Road, Near Samruddhi Circle, Nagpur - 441122",
        "summary": (
            "A 37-acre gated plotted community near Samruddhi Circle, with "
            "30+ themed amenities, 1.54 lakh sq.ft of recreational space and "
            "customizable villa plans."
        ),
        "card_facts": [
            ("Land area", "37 acres"),
            ("Plot size", "1,320 – 2,400 sq.ft"),
            ("RERA", "P50500077372"),
        ],
        "highlights": [
            "RERA registered: P50500077372",
            "37 acres of plotted development in a gated community",
            "30+ themed amenities",
            "1.54 lakh sq.ft of recreational space",
        ],
        "amenities": [
            "Premium Gated Community", "30+ Themed Amenities",
            "Recreational Space", "Clubhouse", "Landscaped Greens",
            "Customizable Villa Plans",
        ],
        "image": "images/properties/kalpataru-launch-code-nagpur.jpg",
        "price": "₹ On request",
        "price_note": "Our team will share current pricing and availability.",
        "private_facts": [
            ("RERA No.", "P50500077372"),
            ("Developer", "Kalpataru"),
            ("Marketed by", "Shree Hari Realtors"),
            ("Site address", "Khadka, Hingna Road, Near Samruddhi Circle, Nagpur - 441122"),
            ("Total area", "37 acres"),
            ("Plot sizes", "1,320 sq.ft to 2,400 sq.ft"),
            ("Recreational space", "1.54 lakh sq.ft"),
        ],
        "video_url": None,
        "layout_file": "kalpataru-launch-code-nagpur/layout.jpg",
        "brochure_file": None,
        "map_url": "",
        "details": [
            ("RERA No.", "P50500077372"),
            ("Developer", "Kalpataru"),
            ("Marketed by", "Shree Hari Realtors"),
            ("Site address", "Khadka, Hingna Road, Near Samruddhi Circle, Nagpur - 441122"),
            ("Total area", "37 acres"),
            ("Plot sizes", "1,320 sq.ft to 2,400 sq.ft"),
            ("Recreational space", "1.54 lakh sq.ft"),
        ],
        "specs": [],
        "card": "kalpataru-launch-code-nagpur-card.jpg",
        "hero": "kalpataru-launch-code-nagpur-hero.jpg",
        "gallery": [],
        "plans": [],
    },
    {
        "slug": "infinia-city",
        "name": "Infinia City",
        "developer": "Infinia",      # TODO: add the developer's full name
        "type": "Villa Plots & 3 BHK Villas",
        "status": "ongoing",
        "location": "Mohgaon, Wardha Road, Nagpur",
        "summary": (
            "A secured gated villa-plot community spread over 120+ acres, "
            "500 m from a proposed metro station, with four exclusive zones "
            "for sports, entertainment and relaxation."
        ),
        "card_facts": [
            ("Land area", "120+ acres"),
            ("Plot size", "1,000 – 5,000 sq.ft"),
            ("Villas", "3 BHK, 1,050 & 1,250 sq.ft"),
        ],
        "highlights": [
            "120+ acres of villa plots in a secured gated community",
            "500 m from the proposed metro station",
            "4 exclusive zones for sports, entertainment and relaxation",
            "3 BHK villa options of 1,050 and 1,250 sq.ft",
        ],
        "amenities": [
            "1.5 Lakh sq.ft Infinia Park",
            "60,000 sq.ft Infinia Forest Garden",
            "44,000 sq.ft Infinia Sports Centre",
            "65,000 sq.ft Club Infinia",
            "Secured Gated Community",
        ],
        "image": "images/properties/infinia-city.jpg",
        "price": "₹ On request",
        "price_note": "Our team will share current pricing and availability.",
        "private_facts": [
            ("Developer", "Infinia"),      # TODO
            ("Marketed by", "Shree Hari Realtors"),
            ("Location", "Mohgaon, Wardha Road, Nagpur"),
            ("Total area", "120+ acres"),
            ("Plot sizes", "1,000 to 5,000 sq.ft"),
            ("Villa options", "3 BHK villa, 1,050 sq.ft and 1,250 sq.ft"),
            ("Internal roads", "9 m, 12 m and 15 m wide; 18 m wide road; proposed 60 m wide road nearby"),
        ],
        "video_url": None,
        "layout_file": "infinia-city/layout.jpg",
        "extra_files": [
            ("3 BHK villa plan - 1,050 sq.ft", "infinia-city/villa-1050.jpg"),
            ("3 BHK villa plan - 1,250 sq.ft", "infinia-city/villa-1250.jpg"),
        ],
        "brochure_file": None,
        "map_url": "",
        "details": [
            ("Developer", "Infinia"),      # TODO
            ("Marketed by", "Shree Hari Realtors"),
            ("Location", "Mohgaon, Wardha Road, Nagpur"),
            ("Total area", "120+ acres"),
            ("Plot sizes", "1,000 to 5,000 sq.ft"),
            ("Villa options", "3 BHK villa, 1,050 sq.ft and 1,250 sq.ft"),
        ],
        "specs": [],
        "card": "infinia-city-card.jpg",
        "hero": "infinia-city-hero.jpg",
        "gallery": [],
        "plans": [],
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
