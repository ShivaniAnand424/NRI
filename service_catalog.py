# Shared questions appear on every service enquiry page.
# Contact name and email come from the signed-in user's account.

def field(name, label, field_type="text", required=False, options=None, help_text=None):
    item = {
        "name": name,
        "label": label,
        "type": field_type,
        "required": required,
    }

    if options:
        item["options"] = options

    if help_text:
        item["help_text"] = help_text

    return item


COMMON_FIELDS = [
    field(
        "property_area",
        "Nagpur locality or area",
        required=True,
        help_text="A locality or area is enough to start. Do not enter the full address here.",
    ),
    field(
        "property_type",
        "Property type",
        field_type="select",
        required=True,
        options=[
            "Apartment or flat",
            "Independent house or villa",
            "Plot or land",
            "Commercial property",
            "Not sure",
        ],
    ),
    field(
        "preferred_contact",
        "Preferred contact method",
        field_type="select",
        required=True,
        options=[
            "Email",
            "Phone call",
            "WhatsApp",
        ],
    ),
]


SERVICE_PAGES = {
    "property-management": {
        "number": "01",
        "title": "Property management",
        "summary": "Discuss local coordination and ongoing property needs with our team.",
        "intro": "Tell us about the property and the kind of ongoing support you want to discuss.",
        "fields": [
            field(
                "occupancy_status",
                "Current occupancy",
                field_type="select",
                required=True,
                options=[
                    "Occupied by the owner",
                    "Occupied by a tenant",
                    "Currently vacant",
                    "Not sure",
                ],
            ),
            field(
                "management_needs",
                "What support would you like to discuss?",
                field_type="checkboxes",
                required=True,
                options=[
                    "Routine property coordination",
                    "Maintenance follow-up",
                    "Tenant communication",
                    "Property visits",
                    "Other",
                ],
            ),
            field(
                "support_start",
                "When would you like to start?",
                field_type="select",
                required=True,
                options=[
                    "As soon as possible",
                    "Within one month",
                    "Later",
                    "Just exploring options",
                ],
            ),
            field(
                "management_notes",
                "Anything else we should know?",
                field_type="textarea",
            ),
        ],
    },

    "buy-sell-assistance": {
        "number": "02",
        "title": "Buy & sell assistance",
        "summary": "Explore support for the practical steps involved in a property decision.",
        "intro": "Share whether you are buying or selling and what kind of local assistance you are looking for.",
        "fields": [
            field(
                "transaction_type",
                "Are you buying or selling?",
                field_type="select",
                required=True,
                options=[
                    "Buying a property",
                    "Selling a property",
                    "Considering both",
                    "Not sure yet",
                ],
            ),
            field(
                "property_area_preference",
                "Preferred Nagpur locality or area",
                help_text="A general area is enough for your first enquiry.",
            ),
            field(
                "price_expectation",
                "Approximate budget or expected price",
                help_text="Optional. A broad estimate is enough; do not include financial account details.",
            ),
            field(
                "decision_timeline",
                "When are you hoping to proceed?",
                field_type="select",
                required=True,
                options=[
                    "Within one month",
                    "Within three months",
                    "Later",
                    "Just exploring",
                ],
            ),
            field(
                "buy_sell_notes",
                "What would you like help with?",
                field_type="textarea",
                required=True,
            ),
        ],
    },

    "rental-coordination": {
        "number": "03",
        "title": "Rental coordination",
        "summary": "Ask about rental-related coordination and owner requirements.",
        "intro": "Tell us your role and what rental coordination you want to discuss.",
        "fields": [
            field(
                "rental_role",
                "Your role",
                field_type="select",
                required=True,
                options=[
                    "Property owner",
                    "Tenant",
                    "Authorized representative",
                    "Other",
                ],
            ),
            field(
                "rental_status",
                "Current rental status",
                field_type="select",
                required=True,
                options=[
                    "Currently rented",
                    "Vacant",
                    "Looking for a tenant",
                    "Not sure",
                ],
            ),
            field(
                "rental_needs",
                "What rental support do you need?",
                field_type="checkboxes",
                required=True,
                options=[
                    "Tenant coordination",
                    "Move-in or move-out coordination",
                    "Rent-related follow-up",
                    "Rental communication",
                    "Other",
                ],
            ),
            field(
                "rental_date",
                "Relevant date, if any",
                field_type="date",
            ),
            field(
                "rental_notes",
                "Additional details",
                field_type="textarea",
            ),
        ],
    },

    "documentation-guidance": {
        "number": "04",
        "title": "Documentation guidance",
        "summary": "Understand which paperwork or local professional support may be relevant.",
        "intro": "Tell us what kind of property paperwork you have questions about. Please do not upload documents on this first enquiry.",
        "fields": [
            field(
                "requester_role",
                "Your role in this matter",
                field_type="select",
                required=True,
                options=[
                    "Property owner",
                    "Buyer or seller",
                    "Tenant or landlord",
                    "Authorized representative",
                    "Other",
                ],
            ),
            field(
                "paperwork_topic",
                "What paperwork is this about?",
                field_type="select",
                required=True,
                options=[
                    "Ownership or property records",
                    "Property tax or municipal records",
                    "Buying or selling paperwork",
                    "Rental paperwork",
                    "NRI or representative coordination",
                    "Not sure",
                    "Other",
                ],
            ),
            field(
                "paperwork_stage",
                "Where are you in the process?",
                field_type="select",
                required=True,
                options=[
                    "I am gathering information",
                    "I have started the process",
                    "I need help understanding a next step",
                    "There is a time-sensitive matter",
                ],
            ),
            field(
                "paperwork_notes",
                "What would you like clarified?",
                field_type="textarea",
                required=True,
            ),
        ],
    },

    "property-visits": {
        "number": "05",
        "title": "Property visits",
        "summary": "Discuss visit coordination and what can be arranged for your situation.",
        "intro": "Share the reason for a visit and any timing or access details that may help with coordination.",
        "fields": [
            field(
                "visit_purpose",
                "Purpose of the visit",
                field_type="select",
                required=True,
                options=[
                    "View a property",
                    "Visit a property I own",
                    "Discuss a potential purchase",
                    "Coordinate a local meeting",
                    "Other",
                ],
            ),
            field(
                "preferred_visit_date",
                "Preferred date, if known",
                field_type="date",
            ),
            field(
                "visit_access",
                "How might access be arranged?",
                field_type="select",
                required=True,
                options=[
                    "I can arrange access",
                    "Another person may need to coordinate access",
                    "I am not sure yet",
                ],
            ),
            field(
                "visit_notes",
                "What should we know about the visit?",
                field_type="textarea",
            ),
        ],
    },

    "tenant-coordination": {
        "number": "06",
        "title": "Tenant coordination",
        "summary": "Talk through tenant-related communication and local follow-up needs.",
        "intro": "Tell us your role and the tenant-related matter you want to discuss.",
        "fields": [
            field(
                "tenant_role",
                "Your role",
                field_type="select",
                required=True,
                options=[
                    "Property owner or landlord",
                    "Tenant",
                    "Authorized representative",
                    "Other",
                ],
            ),
            field(
                "coordination_topic",
                "What needs coordination?",
                field_type="select",
                required=True,
                options=[
                    "Tenant communication",
                    "Maintenance follow-up",
                    "Move-in or move-out",
                    "Rent-related follow-up",
                    "Other",
                ],
            ),
            field(
                "coordination_urgency",
                "How soon is a response needed?",
                field_type="select",
                required=True,
                options=[
                    "Routine",
                    "Within a few days",
                    "Time-sensitive",
                ],
            ),
            field(
                "coordination_notes",
                "Briefly describe the situation",
                field_type="textarea",
                required=True,
            ),
        ],
    },

    "site-condition-checks": {
        "number": "07",
        "title": "Site & condition checks",
        "summary": "Ask whether an in-person property check fits your requirement.",
        "intro": "Describe what you would like someone to check. Any initial check is a general visual visit, not a certified engineering inspection.",
        "fields": [
            field(
                "check_areas",
                "What would you like checked?",
                field_type="checkboxes",
                required=True,
                options=[
                    "Exterior or visible surroundings",
                    "Interior condition",
                    "Visible maintenance concerns",
                    "Occupancy or access status",
                    "Other",
                ],
            ),
            field(
                "site_access",
                "Can access to the property be arranged?",
                field_type="select",
                required=True,
                options=[
                    "Yes",
                    "Access will need coordination",
                    "Not sure",
                ],
            ),
            field(
                "preferred_check_date",
                "Preferred date, if known",
                field_type="date",
            ),
            field(
                "condition_notes",
                "What prompted the check?",
                field_type="textarea",
                required=True,
            ),
        ],
    },

    "local-assistance": {
        "number": "08",
        "title": "Local assistance",
        "summary": "Share your Nagpur property question and confirm the appropriate next step.",
        "intro": "Use this option if your question does not fit one of the other service areas.",
        "fields": [
            field(
                "assistance_topic",
                "What is your question about?",
                field_type="select",
                required=True,
                options=[
                    "Property management",
                    "Buying or selling",
                    "Rental coordination",
                    "Documentation",
                    "Property visit or check",
                    "Something else",
                ],
            ),
            field(
                "assistance_timeline",
                "When do you need help?",
                field_type="select",
                required=True,
                options=[
                    "As soon as possible",
                    "Within one month",
                    "Later",
                    "Just looking for information",
                ],
            ),
            field(
                "assistance_notes",
                "Describe your Nagpur property question",
                field_type="textarea",
                required=True,
            ),
        ],
    },
}


def get_service_page(slug):
    """Return one service-page definition, or None when the slug is unknown."""
    return SERVICE_PAGES.get(slug)