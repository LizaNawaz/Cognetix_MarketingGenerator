PLATFORMS = {
    "Instagram": {
        "rules": [
            "Write a scroll-stopping first line.",
            "Use concise, friendly, visual language and short paragraphs.",
            "Use a clear call to action when supplied.",
            "Add 3–5 relevant hashtags.",
            "Never invent product claims."
        ],
        "examples": [
            {
                "input": "Product: ceramic travel mug; audience: commuters; tone: friendly",
                "output": {
                    "headline": "Your coffee, ready for the commute!",
                    "content": (
                        "Meet your new everyday travel mug. "
                        "A simple way to bring your favourite drink "
                        "along for the ride."
                    ),
                    "hashtags": [
                        "#TravelMug",
                        "#DailyRoutine",
                        "#CoffeeTime"
                    ]
                }
            },
            {
                "input": "Product: desk plant; audience: home-office workers; tone: playful",
                "output": {
                    "headline": "A little green for your workspace!",
                    "content": (
                        "Give your desk a fresh little companion. "
                        "Add a touch of green to your workspace "
                        "and brighten your everyday routine."
                    ),
                    "hashtags": [
                        "#DeskSetup",
                        "#PlantLovers",
                        "#WorkFromHome"
                    ]
                }
            }
        ]
    },

    "LinkedIn": {
        "rules": [
            "Use a professional, helpful tone.",
            "Explain practical or business value without hype.",
            "Use readable paragraphs.",
            "Use no more than 3 relevant hashtags.",
            "Never invent statistics or customer results."
        ],
        "examples": [
            {
                "input": "Product: team scheduling tool; audience: small business managers",
                "output": {
                    "headline": "Make team scheduling easier to manage",
                    "content": (
                        "Coordinating a team takes time. "
                        "A clear scheduling workflow can help managers "
                        "organise shifts, availability, and updates. "
                        "Explore whether a simpler process could work "
                        "for your team."
                    ),
                    "hashtags": [
                        "#SmallBusiness",
                        "#Productivity"
                    ]
                }
            },
            {
                "input": "Product: reusable shipping boxes; audience: online retailers",
                "output": {
                    "headline": "Rethinking packaging for repeat deliveries",
                    "content": (
                        "Packaging decisions affect operations and "
                        "the customer experience. Reusable shipping "
                        "boxes may be worth evaluating for businesses "
                        "with repeat delivery routes. Review your "
                        "workflow and return process."
                    ),
                    "hashtags": [
                        "#Ecommerce",
                        "#Packaging"
                    ]
                }
            }
        ]
    },

    "Email": {
        "rules": [
            "Use a clear, concise subject line.",
            "Include a greeting, short body, and clear CTA.",
            "Avoid misleading urgency and spammy wording.",
            "Never invent contact details or signatures.",
            "Use headline as the email subject line."
        ],
        "examples": [
            {
                "input": "Product: insulated lunch bag; audience: office workers",
                "output": {
                    "headline": "A practical companion for your workday",
                    "content": (
                        "Hi there,\n\n"
                        "Looking for an easy way to bring lunch to work? "
                        "Our insulated lunch bag is designed to help you "
                        "carry your meal as part of your daily routine.\n\n"
                        "Take a look at the details to see if it fits your day.\n\n"
                        "Explore the lunch bag"
                    ),
                    "hashtags": []
                }
            },
            {
                "input": "Product: online bookkeeping service; audience: freelancers",
                "output": {
                    "headline": "Spend less time sorting receipts",
                    "content": (
                        "Hi,\n\n"
                        "Keeping track of business expenses can take time "
                        "away from client work. Our online bookkeeping "
                        "service offers freelancers a place to organise "
                        "their bookkeeping workflow.\n\n"
                        "Review the features to see whether it meets your needs.\n\n"
                        "Learn more"
                    ),
                    "hashtags": []
                }
            }
        ]
    }
}

TONES = [
    "Friendly",
    "Professional",
    "Playful",
    "Persuasive",
    "Informative",
    "Warm",
    "Direct"
]

LENGTHS = ["short", "medium", "long"]

LANGUAGES = [
    "English",
    "Hindi",
    "Assamese",
    "Bengali",
    "Spanish",
    "French"
]