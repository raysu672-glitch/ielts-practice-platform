// 模块配置、词表数据与模块相关工具
// 单词列表
var allWords = ["ancestor", "barrier", "calendar", "dynasty", "engine", "festival", "gallery", "harbour", "income", "journal", "kingdom", "labour", "melody", "nursery", "occasion", "palace", "queue", "railway", "scenery", "territory", "umbrella", "vacancy", "welfare", "youth", "zone", "academy", "banquet", "capital", "disaster", "economy", "fashion", "grocery", "horizon", "identity", "journey", "landscape", "monument", "obstacle", "origin", "portrait", "quantity", "recreation", "tradition", "universe", "volunteer", "wealth", "boundary", "charity", "destiny", "empire", "faculty", "guarantee", "illusion", "liberty", "mission", "novel", "outcome", "priority", "realm", "strategy", "tension", "version", "wisdom", "avenue", "branch", "colony", "departure", "essence", "frontier", "gravity", "harvest", "impression", "leisure", "mystery", "opponent", "perspective", "radius", "schedule", "tendency", "utility", "victory", "anniversary", "blossom", "ceremony", "dilemma", "fortune", "generation", "harmony", "impact", "inflation", "luxury", "narrative", "privilege", "rhythm", "talent", "trend", "virtue", "abandon", "biography", "catastrophe", "diploma", "elegance", "hospitality", "incident", "legend", "monopoly", "oath", "phenomenon", "pursuit", "routine", "symptom", "tragedy", "alliance", "burden", "climax", "epidemic", "friction", "galaxy", "impulse", "motive", "orbit", "remedy", "skeleton", "technique", "urban", "vocation", "behaviour", "campaign", "heritage", "initiative", "legacy", "network", "paradise", "quest", "reservoir", "warfare", "autumn", "consequence", "dignity", "evolution", "function", "gratitude", "humidity", "innovation", "latitude", "norm", "reunion", "shortage", "altitude", "blueprint", "budget", "coincidence", "doctrine", "enterprise", "framework", "guideline", "ingredient", "layout", "module", "nutrition", "oxygen", "premium", "revenue", "subsidy", "tariff", "vintage", "assembly", "archive", "brochure", "catalogue", "dossier", "estate", "index", "manual", "overview", "portfolio", "register", "statute", "treaty", "basement", "cottage", "dwelling", "inn", "lodge", "mansion", "residence", "terrace", "artery", "boulevard", "corridor", "pathway", "route", "beverage", "cuisine", "feast", "pastry", "recipe", "spice", "refreshment", "alphabet", "document", "essay", "fiction", "manuscript", "poetry", "prose", "volume", "album", "artifact", "carving", "exhibit", "masterpiece", "mural", "sculpture", "statue", "amateur", "athlete", "competitor", "tournament", "author", "candidate", "civilian", "employer", "guest", "pedestrian", "astronomy", "chemistry", "geography", "geometry", "geology", "physics", "statistics", "algebra", "calculus", "formula", "fraction", "matrix", "numeral", "proportion", "aroma", "breeze", "echo", "fragrance", "lightning", "rainbow", "sunrise", "sunset", "thunder", "whisper", "adventure", "carnival", "parade", "ritual", "moderate", "park", "pool", "museum", "flowers", "cafe", "bridge", "map", "qualification", "government", "boys", "meeting", "business", "university", "reading", "age", "relationships", "neighbour", "noise", "screen", "size", "colour", "commercial", "animals", "lines", "photograph", "communication", "invention", "printing", "radio", "television", "internet", "instructor", "certificate", "shoes", "waterproof", "jeans", "snack", "doctor", "photographs", "farm", "harvest", "field", "tractor", "seed", "fertilizer", "soil", "Sunday", "lifting", "watering", "maths", "passport", "fish", "clothing", "training", "paper", "rivers", "allergy", "minerals", "organic", "jewellery", "shells", "Mexico", "shiny", "corn", "money", "weight", "fertility", "wedding", "power", "rulers", "rich", "women", "China", "material", "decoration", "trade", "symbol", "foundation", "sand", "clay", "cheap", "convenient", "labour", "roof", "plaster", "birthday", "children", "Italian", "cake", "guitar", "Wednesday", "review", "cities", "acid", "stone", "bank", "rainfall", "glass", "wood", "movement", "guidelines", "airport", "clothes", "Chinese", "coffee", "school", "swimming", "film", "smooth", "protection", "half", "salt", "mud", "smell", "pump", "pest", "antibiotic", "boat", "leather", "purple", "medium", "magazine", "regular", "attitude", "education", "development", "horse", "canoe", "caves", "helmet", "past", "village", "basketball", "butter", "grants", "buffet", "stove", "microwave", "dishwasher", "garden", "hunt", "flute", "swan", "stones", "Europe", "variety", "simple", "wind", "painting", "poetry", "summer", "lake", "nutrition", "soccer", "safety", "fire", "speaker", "coins", "status", "belt", "marriage", "skirts", "sweet", "gifts", "fabrics", "feminism", "sports", "whistle", "tool", "signal", "design", "Rafael", "babies", "nuts", "combination", "outdoor", "advertisement", "storage", "gift", "hunting", "face", "storms", "ancestors", "island", "view", "pie", "movie", "market", "online", "student", "changing", "areas", "refreshment", "stalls", "picnic", "medical", "aid", "lost", "found", "fragile", "claws", "mushrooms", "critical", "dogs", "dry", "relocation", "elephant", "wildlife", "habitat", "endangered", "reserve", "conservation", "noisy", "disease", "shelter", "adapt", "survive", "conference", "room", "mixed", "table", "chicken", "volcano", "smoke", "flower", "grass", "bacteria", "carpet", "fossils", "centuries", "tunnel", "hacking", "names", "group", "reputation", "articles", "supermarket", "materials", "Patterson", "faces", "pencils", "cartoon", "competition", "sheep", "dust", "hearing", "gender", "wolf", "distribution", "stress", "parking", "September", "orientation", "judo", "yoga", "intermediate", "train", "sharks", "Africa", "member", "birds", "hospital", "professional", "learning", "team", "presenting", "results", "behaviour", "diary", "video", "recording", "simulation", "interviews", "silk", "fabric", "bowls", "head", "danger", "metal", "pottery", "year", "history", "poster", "junior", "adventure", "honey", "desk", "weak", "brain", "tongue", "cold", "sleep", "breakfast", "counting", "shoulder", "success", "social", "plans", "influence", "skills", "reason", "emotional", "environment", "analysis", "restaurant", "hotel", "hostel", "apartment", "flat", "house", "kitchen", "bathroom", "living room", "garage", "attic", "street", "road", "avenue", "lane", "path", "highway", "motorway", "railway", "station", "port", "bus", "plane", "ship", "bicycle", "car", "taxi", "truck", "van", "ticket", "fare", "journey", "trip", "travel", "tour", "guide", "compass", "camera", "luggage", "suitcase", "bag", "backpack", "wallet", "purse", "key", "phone", "charger", "book", "pen", "pencil", "paper", "notebook", "dictionary", "encyclopedia", "newspaper", "cash", "credit", "debit", "account", "cheque", "coin", "note", "present", "card", "letter", "email", "message", "parcel", "package", "delivery", "service", "product", "goods", "food", "drink", "water", "tea", "milk", "juice", "soda", "bread", "rice", "noodle", "meat", "beef", "pork", "lamb", "vegetable", "fruit", "salad", "soup", "meal", "lunch", "dinner", "dessert", "chocolate", "sugar", "pepper", "oil", "butter", "cheese", "egg", "diet", "health", "sport", "exercise", "gym", "running", "cycling", "football", "golf", "match", "game", "player", "coach", "referee", "score", "goal", "win", "loss", "draw", "ecosystem", "species", "climate", "weather", "atmosphere", "temperature", "pollution", "contamination", "emission", "waste", "sewage", "resource", "energy", "fuel", "fossil", "solar", "renewable", "preservation", "sustainability", "deforestation", "desertification", "erosion", "degradation", "glacier", "iceberg", "earthquake", "tsunami", "flood", "drought", "hurricane", "tornado", "forest", "jungle", "desert", "mountain", "ocean", "sea", "beach", "coast", "plain", "valley", "canyon", "plateau", "rock", "mineral", "chemical", "substance", "fibre", "plastic", "technology", "device", "equipment", "machine", "instrument", "appliance", "gadget", "software", "hardware", "network", "system", "program", "application", "database", "website", "robot", "artificial", "intelligence", "computer", "sensor", "battery", "screen", "keyboard", "mouse", "data", "information", "code", "virus", "bug", "error", "mammal", "reptile", "insect", "bird", "amphibian", "predator", "prey", "creature", "organism", "colony", "herd", "flock", "swarm", "pack", "evolution", "extinction", "migration", "reproduction", "wing", "feather", "fur", "scale", "tail", "claw", "whale", "dolphin", "octopus", "tiger", "lion", "bear", "fox", "deer", "rabbit", "mouse", "rat", "eagle", "hawk", "owl", "parrot", "pigeon", "butterfly", "bee", "ant", "fly", "mosquito", "zoo", "sanctuary", "diploma", "biology", "operation", "reputation", "approach", "dismissal", "manipulation", "licence", "pasture", "woodland", "microscope", "contract", "contact", "definition", "peers", "professionals", "vision", "security", "community", "validity", "interview", "seminar", "workshop", "lecture", "tutorial", "deadline", "budget", "schedule", "agenda", "document", "file", "journal", "booklet", "brochure", "leaflet", "diagram", "graph", "chart", "table", "sample", "statistic", "evidence", "proof", "theory", "hypothesis", "concept", "idea", "method", "technique", "process", "procedure", "rule", "regulation", "policy", "law", "standard", "principle", "ethics", "culture", "tradition", "custom", "belief", "value", "opinion", "view", "emotion", "feeling", "mood", "habit", "lifestyle", "illness", "injury", "pain", "fatigue", "energy", "strength", "weakness", "ability", "skill", "talent", "knowledge", "experience", "career", "job", "occupation", "profession", "employment", "unemployment", "salary", "wage", "income", "expense", "cost", "price", "fee", "charge", "discount", "bonus", "profit", "loss", "investment", "fund", "finance", "economy", "market", "company", "corporation", "enterprise", "organization", "institution", "authority", "council", "department", "agency", "office", "staff", "employee", "employer", "colleague", "manager", "director", "leader", "group", "partner", "client", "customer", "consumer", "user", "patient", "teacher", "professor", "tutor", "lecturer", "researcher", "scientist", "expert", "specialist", "consultant", "volunteer", "citizen", "resident", "friend", "family", "relative", "parent", "adult", "teenager", "youth", "elder", "male", "female", "man", "woman", "girl", "boy", "victory", "sacrifice", "patience", "wisdom", "charity", "fortune", "liberty", "courage", "dignity", "glory", "justice", "mercy", "honour", "purity", "faith", "hope", "grief", "panic", "terror", "regret", "guilt", "shame", "envy", "pity", "reward", "punishment", "crime", "fault", "mistake", "flaw", "merit", "virtue", "vice", "habit", "custom", "trend", "fashion", "style", "taste", "mood"];
var allWordsListeningBasic = ["abroad", "academic", "academic record", "accents", "accept", "acceptable", "accidents", "accountable", "accountants", "accurate", "achievement", "acknowledgement", "actions", "actors", "addictive", "address", "administration", "administration officer", "admission", "adopt", "adults", "advance", "advance level", "advertise", "advertising", "advisors", "afternoon", "against", "agent", "ages", "aging", "agreement", "agriculture", "air pollution", "air pump", "air quality", "air-condition", "airline", "airplane", "airports", "alarming system", "alarms", "alter", "alternative", "alternative energy", "ambition", "ambulance", "amount", "angle", "animals behavior", "answer", "answering the phone", "antibiotics", "antifreeze", "antiseptic", "ants", "apologize", "apology", "appearance", "apple juice", "application form", "approaches", "april", "apron", "archives", "argentina", "argument", "armchair", "arms", "army", "arrangement", "arranging", "arrows", "art gallery", "artists", "artists club", "arts", "aspiration", "assess", "assessment", "assignment", "atlas", "atoms", "attack", "attack humans", "audience", "august", "aunt", "automatic", "automobile", "average", "back", "back problem", "back wheel", "backdoor", "background music", "backpacker", "badge", "bakery", "balance", "balcony", "ball", "balloons", "ban", "banana ride", "bananas", "band", "bank statement", "barbershop", "barcode", "bargain", "baseball coach", "basic", "bath", "bathrooms", "beaches", "bears", "bed and breakfast", "bedroom", "bedsit", "beer", "beginners", "beginning", "behaviors", "benefits", "big social event", "bike", "bikes", "bill", "bins", "biological", "biological control", "biological fishing", "biology lesson", "bird park", "bird-watching", "birth", "blanket", "block", "blood", "blue", "boards", "boat trip", "boats", "body fluids", "body language", "body shape", "boiler", "bones", "book in advance", "book loan", "book talk", "booking", "booking form", "bookkeeping", "bookshop", "booths", "boots", "boring", "bottie water", "bottle tops", "bottled water", "boxes", "brakes", "branches", "break", "breakdown", "breathing", "breed", "bricks", "bridges", "bright", "brilliant", "broad", "broader", "bronze", "brother-in-law", "brushes", "bucket", "builder", "built", "bunch", "burning time", "bus stop", "bus tickets", "bushes", "businessmanagement", "business area", "business cards", "business plan", "business visits", "butterfiies", "cab", "cabie", "cabin", "cabin key", "cable car", "calculating", "calculation", "call centre", "call diversion", "calls", "calm", "camel", "camel transportation", "cameraman", "cameras", "camp", "campsite", "campus", "canal", "candles", "canteen", "cap", "capacities", "captive", "car park", "car tyres", "car-park", "caravan", "carbon", "carbon dioxide", "card index", "card number", "career office", "carpenter", "carpets", "carrots", "cartoons", "case studies", "cash machine", "cashier", "castle", "castle hill", "castles", "casual", "casual clothes", "categories", "catering", "cattle", "causes", "cave", "celebrities", "cement", "centimeter", "central", "central heating", "central station", "ceremonies", "certificates", "chain", "chairman", "chalk", "challenge", "change", "changing room", "character", "charity worker", "cheapest budget", "check", "checklist", "chemical contaminants", "chemist", "chemistry lab", "chess", "chief executive", "child seat", "children background", "children mind", "china stone", "choice", "choose", "choosing", "cigar", "cinema", "ciothing sections", "circles", "circulation", "city", "city centre", "city council", "classical", "classical history", "classification", "classifying", "classroom tour", "clean", "clean products", "cleaner", "cleanest", "cleaning", "clear", "clear voice", "clever", "cliffs", "climbing", "clinic", "closed", "closed down", "cloud", "club", "club office", "clubhouse", "coaches", "coastal cities", "coastline", "coconut", "codes", "coffee machine", "coffee table", "colds", "collect money", "collecting", "collection", "college", "colour photos", "coloured", "colours", "comedy", "comfortable", "comics", "comment card", "commitment", "common", "common room", "communication system", "companionship", "comparison", "compensation", "competitive", "compiaints", "compiete", "compiex", "composers", "compounds", "comprehension", "compuisory", "compulsory and regular", "computerprogrammer", "computer centre", "computer office", "computer science", "computers", "concentrate", "concentration", "concert", "concert hall", "concert room", "concerts", "conclusions", "concrete", "condition", "conference centre", "conference hall", "conference pack", "confidence", "confirm", "confirmation", "confusion", "consistent", "consumers", "consumption", "contact detaiis", "containers", "contaminate", "context", "control", "conversation", "cook", "cookery", "cooling down", "cooperate", "cooperation", "cooperation loan", "copies", "corners", "correction", "corrupt", "cosmetics", "cost-effective", "cotton", "count", "country", "countryside living", "couple", "course", "course outline", "coursework", "cover", "craft", "cream", "creation", "creativity", "credit card", "credit rating", "crisis", "crocodiles", "crops", "crowded", "crown", "crying", "cultural", "culture awareness", "culture context", "cultures", "cup", "current", "curtains", "curved", "customers", "daily routine", "dairy", "damp", "dance", "dance class", "dance show", "dangerous", "dangerous traffic", "dark", "dark blue", "dark coloured", "darkroom", "data analysis", "day", "day off", "daylight", "decade", "december", "decision", "decline", "decorations", "decrease", "deep", "defense", "degrees", "demand", "democratic", "demonstrations", "density", "dentist", "department head", "department store", "deposit", "depression", "depth", "description", "desert locations", "deserts", "design research", "designers", "desk iamp", "destroy", "develop", "developing country", "diamond", "diaries", "dictation", "different", "difficult", "digestion", "digestive", "digging", "digital privacy", "digital store", "digital system", "dining room", "direct", "direction", "dirt", "disable people", "disappear", "discipline", "discussion", "diseases", "dismiss", "display", "distance", "distance learning", "distortion", "distribute", "district", "diversity", "diving", "diving mask", "doctors", "documentary", "documentation", "documents", "dolphins", "dome", "domestic", "donations", "donkeys", "door to door", "double", "double room", "double-grill", "downhill", "downstairs", "draft", "drama", "drawer", "drawing", "dreams", "dress code", "dressing", "dried", "drinking", "drinking and snacks", "drinking machines", "drinks", "drive", "driver", "driving", "driving license", "drop off", "drugs", "drums", "drying", "duck", "durable", "duration", "dust bag", "e-ticket", "early", "earning", "eat", "eating patterns", "eco-system", "ecology", "economical", "economics", "economics history", "edges", "editor", "education department", "education officer", "education plan", "education system", "effectiveness", "efficiency", "efficient", "elastic", "electric cars", "electricity", "electricity supply", "electronic", "electronic card", "electronic directory", "elephants", "elevator", "email address", "emails", "embassy", "emergency", "emotions", "emperor", "empty", "encourage", "end", "energy saving", "engineering", "engineers", "eniargement", "enjoyable", "entertainment", "entertainmentindustry", "entire", "entrance", "entry", "environment agency", "environment damage", "environmental", "equai", "error message", "escape", "essay writing", "essays", "estimate", "european", "evaluation", "evaporation", "evening meals", "evening news", "evenings", "exam", "exam preparation", "example", "excellent", "excitement", "exercises", "exhibitions", "exhibitor", "expansion", "expect", "expectations", "expensive", "experiment", "experimental facilities", "explain", "explanation", "explode", "exploration", "explosion", "export", "expose", "express trains", "external", "extra", "extra workload", "eye contacts", "eyedrops", "eyes", "eyesight", "face painting", "facilities", "fact", "factories", "factory", "fair", "famiiy", "families life", "family members", "family photo", "family relationship", "family ticket", "famous author", "fancy dress", "fans", "farmers", "farming", "farming products", "fast food shop", "fat", "faxing", "fear", "feathers", "february", "feed animals", "feed the shark", "feedback", "feeding", "feeding time", "feet", "fell", "fence", "fertilizers", "fiashiight", "fiavor", "fields", "fieldwork", "fight", "files", "fill", "films", "finance market", "finance office", "financial", "financial results", "fingers", "fire alarm", "fire drill", "fireplaces", "fires", "firewood", "firework", "fireworks", "first draft", "first-aid kit", "first-year students", "fish cake", "fish farm", "fish industry", "fishing", "fishing boats", "fishing lesson", "fishing net", "fitness", "fitness centre", "fitness level", "fiute", "flamingos", "flashing", "flexibility", "flexible", "flies", "flight", "floated", "flooding", "floodwater", "floors", "flourishment", "flu", "fluctuate", "fluent", "fluids", "focus", "fog", "folded", "font", "food chain", "food containers", "food intake", "food source", "food supply", "foods", "foot", "foot movement", "footbridges", "footprints", "forecast", "forest campsite", "forestry", "forests", "formal clothing", "formal garden", "formal meetings", "formats", "former worker", "fountain", "frame", "france", "free booklet", "free drink", "free entry", "free meal", "free parking", "free pick", "free repair", "free transportation", "freedom", "freezer", "freight", "french", "french styie", "frequency", "fresh", "fresh food", "friday", "fridge", "friendly", "friends", "friendship", "fringe", "frogs", "front", "front desk", "front page", "frozen", "fruit juice", "fruit tree", "fruitcake", "fruits", "frustration", "full time", "funding", "furniture", "further training", "future career", "game room", "games", "gaps", "garbage", "garden tools", "gardening", "gas", "gas tanks", "geese", "gene", "general", "general discussion", "general tour", "genetic", "geographical", "germany", "germs", "gioves", "girl club", "girls", "glass roof", "glasses", "global", "global market", "global payments", "glue", "goat", "gold", "goldfish", "golf court", "government agencies", "government election", "government policy", "grade", "graduai", "grain", "grammar", "grandfather", "grandmother", "grant", "graphics", "grasses", "green", "green button", "green tax", "green waste", "greenfield", "grey", "ground floor", "groundplan", "group discussion", "group meetings", "group size", "group trip", "groups", "growing", "growth opportunities", "guard", "guessing", "guided tour", "gun", "hairdresser", "hairs", "handbook", "handle", "handouts", "hands", "harbours", "hard", "hardworking", "harm", "harmful", "hat", "head office", "headache", "headlines", "headphones", "health check", "health club", "health department", "health problem", "health service", "healthcare", "healthy", "healthy soil", "heart", "heart disease", "heart rate", "heat", "heater", "heavy", "height", "helicopter", "help desk", "herbivorous", "herds", "hero", "high car taxes", "high temperature", "high user", "higher fees", "hiking", "hire", "historical maps", "hive", "home phone", "homework", "honest", "hook", "horror", "horse riding", "horsehair", "horses", "hot meal", "hotels", "hothouse", "house insurance", "house key", "housing", "human activities", "humans", "humor", "hunger", "hungry", "hurry up", "iand", "ianes", "iaptops", "iaw department", "ice pack", "ice skating", "identification", "iegroom", "ieisure", "iength", "images", "immigration", "immune", "important", "imported", "impossible", "improvement", "in danger", "in the town", "incineration plant", "incoming call", "increase", "independent", "india", "individual", "indoor", "industry", "infiuence", "informai", "information desk", "information sectors", "infrastructure", "ingredients", "ink", "insects", "inside", "instinct", "instinctive", "instructions", "insulation", "insurance", "insurance company", "intact", "integrate", "intensive", "interaction", "interest", "interest rates", "internal", "internal clock", "international", "international express", "international studies", "internet cafe", "internet connection", "internet line", "interview questions", "interview skills", "introduction", "invitations", "ioans", "iookout point", "iost", "iron", "irrigation", "isolation", "issue", "items", "iungs", "jacket", "january", "japanese", "jazz", "jet engine", "jewelry", "job interview", "job opportunities", "jogging", "joining", "joining fees", "joint", "jokes", "journaiism", "journalists", "journals", "juice bottles", "july", "june", "kangaroo", "keep fit", "kidney", "kilometers", "kindness", "king", "kitchen area", "kitchen hand", "kite", "knees", "knife", "knowiedge sharing", "lab", "labels", "laboratories", "laboratories report", "ladders", "lakes", "lakeside", "land bridge", "landlady", "landmarks", "languages", "large office", "large scale", "lateral-line", "laundry", "lawyers", "leaders", "leadership", "leadership style", "leak", "learner", "learning difficulty", "learning style", "learning zone", "leaves", "lectures", "left", "leg", "legal", "legal action", "levels", "liable", "library", "license", "lids", "life assurance", "lifecycle", "lifespan", "lighting", "lights", "limestone", "link", "lions", "liquid", "list", "literature", "live music", "living", "living expenses", "lizard", "local community", "local museum", "local newspaper", "local schools", "local shops", "local tribes", "location", "lock", "lock-up garage", "lockers", "logic", "logo", "long stick", "long strap", "long tables", "long time", "long-term", "lose weight", "lost children", "loud noises", "lounge", "low impact", "low nutrition", "low-risk investment", "lower", "loyal", "loyalty", "machinery", "machines", "magazines", "magic", "magnet", "mail", "mailing list", "main", "main hall", "maintenance", "make notes", "male and female", "mammals", "man-made", "management", "manufacture", "manufacturers", "mapping", "maps", "march", "marine piants", "market garden", "marketing", "mask", "massage", "mat", "matching", "math", "mathematics", "maturity", "maximum", "may", "meals", "measurement", "medal", "media", "media room", "media studies", "medical centre", "medication", "medicines", "meetings", "membership", "memories", "mental", "mental ability", "menu", "messages", "metals", "methodology", "methods", "micro-radiogram", "microbiology", "microfilm", "middle", "migrate", "mild", "military", "mineral soil", "minibus", "mining", "minivan", "minutes", "miss", "mission statement", "mobile phone", "modei", "modern", "modern language", "moist", "moisture", "mold", "monday", "money management", "monitor", "monkeys", "monthly", "monuments", "moods", "moraiity", "morning", "motel", "motivation", "motor", "mould", "mountain bike", "mountains", "movies", "multimedia", "muscle pain", "mushroom", "music festival", "music videos", "myth", "national holidays", "national newspaper", "national park", "native", "natural", "natural gas", "natural medicine", "navigation", "navigational", "necessary", "neck", "necklace", "negative", "negative effect", "negative thinking", "negotiation skills", "neighbours", "nesting", "nests", "nets", "networking", "newspapers", "night shifts", "night tour", "nitrogen", "non-native", "non-smoking room", "none", "normal", "north island", "northeast", "note system", "note-taking", "notes", "noticeboard", "november", "numbers", "nurse", "nursing", "nursing care", "nylon", "obesity", "objective matters", "objectives", "objects", "obligation", "observation", "occupancy", "ocean condition", "ocean currents", "october", "odor", "offer advice", "office assistant", "oil filter", "old clothes", "oldest", "olive oil", "online game", "online service", "online shopping", "open", "opera", "opera house", "opportunities", "opposite", "oral", "orange", "order", "organizations", "organize", "originality", "origins", "outcomes", "outline", "outside", "outstanding", "oven", "overdue books", "overfill", "overfishing", "overseas", "own food", "ozone layer", "packaging", "packing", "packing materials", "paddling pool", "paining", "painkiller", "painters", "painting ciass", "pairs", "paper jams", "paragraphs", "parents", "parking lot", "parking space", "parks", "part-time", "participation", "parties", "party hats", "pass", "passages", "passive", "passport photos", "password", "patients", "pattern", "patterns", "pay attention", "pay in cash", "payment", "peak", "peak season", "peer group", "pegs", "pennies", "pens", "perception", "performance", "perfumes", "permanent", "permission", "permit", "person", "personai alarm", "personal", "personalinformation", "personal interest", "personal officer", "personality", "persuading", "pesticides", "pet meat", "petrol", "petrol station", "pets", "pharmacy", "philosophers", "phone book", "phone card", "phone interviews", "phone number", "phone statistics", "photo card", "photocopies", "photocopy shop", "photography", "photos", "pianist", "piano life", "piano player", "pictures", "pillow", "pilots", "pine forests", "pioneer", "pipes", "pirates", "pizza", "pizza boxes", "placement test", "plan", "plane science", "planet science", "planner", "plant species", "plants", "plates", "platforms", "play area", "playground", "playroom", "pleasure", "pockets", "poison", "police helicopters", "policies", "polish", "polished", "political", "political man", "politician", "politics", "polluted", "popuiar", "population", "portable", "position", "post office", "post survey", "postbox", "postcard", "potatoes", "pots", "pounds", "poverty", "powder", "practicai course", "practical work", "predators", "predicting", "prepared", "preparing food", "presentation skills", "presentations", "presenting result", "preserved", "president", "pressed", "pressure", "prevalent", "prevention", "primary", "primary school", "printer", "printers", "printing press", "printing technology", "prison", "prisoners", "privacy company", "private", "private property", "prizes", "problem solving", "problems", "processing", "production", "productivity", "products", "professional learning", "profits", "programmes", "programs", "progress", "project background", "project outline", "project request", "promotion", "promotional", "protection policy", "protective clothing", "protein", "psychologist", "public areas", "public square", "public transport", "public transportation", "publication", "publishing", "pump water", "punctual", "pure", "purpose", "quality", "queen size", "questionnaire", "quiet", "quite", "quiz", "race car", "rack", "radar", "radio program", "radio signals", "railway line", "railway station", "railway tracks", "raining", "rainwater", "rainwear", "random", "range", "rare trees", "rationally", "rats", "reaction", "reading disorder", "reaiism", "realistic", "reasonable", "reasons", "receiver", "reception", "receptionist", "recommendation", "recorders", "recruit", "recycled materials", "recycling", "red blood cells", "reduction", "reference number", "references", "reflective", "refreshments", "refund", "registration", "reguiar", "regular exercises", "regulations", "reieased", "reinforce", "reinvest", "relatively", "relatives", "relaxation", "relevant", "reliable", "religions", "remember", "remote", "repair", "repaired cost", "repeat", "repel", "replacement", "report writing", "reporter", "reports", "representation", "request", "require", "rescue diver", "research approach", "research finding", "reservation", "residents", "resistant", "resources", "responsibility", "responsible", "rest area", "restrictions", "restroom", "retail", "retained", "retire", "retrain", "return", "return tickets", "reusable", "right", "ring abell", "rivals", "river trip", "river view", "riverside", "road map", "roads", "robots", "rockets", "rocks", "roll over", "room service", "roots", "rope", "ropes", "rose garden", "round", "round table", "rubber", "rubber blanket", "rubbish", "rules", "rumor", "runner", "rural", "rush", "russia", "sable", "sacred", "safari park", "safeguard", "safety check", "safety regulations", "safety rules", "sailing", "salad bar", "salads", "sales", "sales manager", "salesman", "saliva", "salts", "samples", "sandglass", "sandwiches", "sandy", "satellite", "satisfaction", "saturday", "save", "savings", "savvy", "scare", "scarf", "scent", "school fees", "school record", "science", "scientific", "scientific explorations", "scientific research", "scores", "scotland", "sculptures", "sea level", "seafood", "seagrass", "seals", "search", "search habits", "season", "seasonal", "seasoned", "seat", "seat reservation", "seating", "seaview", "secondary", "secondary school", "secretary", "section", "security code", "security officer", "seeds", "seif-iocking", "selection", "self-access centre", "self-centered", "self-defense", "self-drive", "self-employed", "self-employment", "self-evaluation", "selfish", "semester", "seminar group", "seminar room", "seminars", "send newsletters", "senior", "senior adviser", "senior management", "sensible exercise", "service manager", "services", "session", "settle", "sex", "shade", "shadow", "shaiiow", "shape", "share", "share ideas", "sharing", "shark nets", "sharp", "sheet", "shelf", "shipbuilding", "shipping", "ships", "shirt", "shoot", "shoppers", "shopping mall", "short", "short lecture", "shortlist", "show", "shower", "shrimp", "shuttle", "sick pay", "side gate", "sign", "signals", "signature", "silence", "silver", "silver coins", "silver paper", "similar", "singer", "singing", "sister", "sites", "situation", "situational", "skills focus", "skin", "sky", "slang", "slaves", "sleeping bag", "sleeping pills", "slide", "slide presentation", "slope", "small", "smaller areas", "smaller one", "smart", "smash", "smoke alarms", "smoking", "smooth road", "smoother", "snakes", "snowboarding", "soap", "sociable", "social activity", "social event", "social information", "social skills", "society", "socks", "soft", "soft sediment", "solar energy", "soldiers", "solid", "solution", "songs", "sort", "sound effect", "source", "souvenir", "space museum", "spanish", "spare", "spare keys", "spare room", "spears", "special", "special code", "special offers", "specialized", "specific", "speeches", "speed", "spelling", "spiders", "spine", "spoon", "sports centre", "sports equipment", "sports hall", "sports injury", "sports service", "spring", "spring water", "square", "stabilize", "stage", "stairlift", "stairs", "stand", "standard grade", "standard teaching", "stars", "starvation", "state park", "statement position", "steam", "steei", "stems", "stick", "stickers", "still", "stimulation", "stings", "stolen", "stomach", "stopwatch", "storage space", "store", "stories", "storm", "straight", "strain", "strangers", "strap", "strategies", "stream", "streets", "stressful", "stretching", "strict", "strike", "string", "strong", "structure", "stuck", "student card", "student loan", "student service", "student support", "student union", "studio", "study skill", "subjects", "subtopics", "subway", "suitable", "summarize", "summary report", "summer school", "sun hat", "sun position", "sun-cream", "sunlight", "sunscreen", "super", "supervise teams", "supervision", "support services", "supportive", "surface", "surfing", "surprise", "survey", "survey methods", "surveys", "sustainable", "swans", "sweaters", "sweetener", "swimming pool", "swimming suit", "switched off", "symboi", "take away", "take photos", "take risks", "tape", "tape recorder", "task", "tastes", "tax number", "taxes", "teaching experience", "teaching staff", "team leaders", "teams", "teamwork", "tears", "technical", "technician", "teenagers", "teeth", "telephone", "telephone interview", "telephone survey", "television drama", "television program", "tempie waiis", "temple", "tennis", "tennis court", "tents", "term", "tests", "textbook lesson", "textbooks", "textbooks allowance", "textile", "theatre", "theme", "theoretical", "theory chapters", "therapy", "think quickly", "threat", "thunderstorm", "thursday", "tickets", "tides", "timber", "time", "time consuming", "timetable", "tires", "tities", "toaster", "toilet", "tolerance", "tomatoes", "tone", "tools", "toothache", "top level", "topics", "torn", "total", "touching", "tourism", "tourist office", "tourists", "towels", "tower", "tower restaurant", "town", "town hall", "towns and cities", "toy factory", "toys", "trace", "tracking protection", "trade journals", "traders", "traditional", "traditional style", "traditional tools", "traffic", "traffic flow", "traffic lights", "traffic noise", "trains", "transiation", "translator", "transparent", "transport service", "transportation", "trash", "traveling", "trays", "treatment", "trends", "triangle", "triangle sharp", "tribes", "tropical", "tropical disease", "trousers", "true", "trumpet", "trust", "tuesday", "tuna", "turn", "tutorials", "tutors", "tv producer", "twice", "type", "type of rocks", "typing", "unanswered", "unapproachable", "uncomfortable", "uncontrolled", "undergraduate", "underground", "undersea world", "understand", "undeveloped", "unfair", "unfriendly", "unfurnished", "unhealthy", "uniform", "unlimited", "unnatural", "unpredictable", "unsocial", "unsure", "upstairs", "urban areas", "useless", "vanish", "variable", "varies", "various", "vegetable burger", "vegetarian", "vegetation", "ventilation system", "vertical", "vetting", "video recording", "video subtitles", "videocameras", "videos", "videotape", "videotape editor", "view shelter", "viewing shelter", "viewpoint", "villages", "visa", "visit", "visitors", "visual aids", "vitamin a", "vocabulary", "voice", "voices", "volcanic ash", "voluntary", "wait", "waiter", "waitress", "walking", "walking boots", "warehouse", "warm", "warm bath", "warm climate", "warm up", "warming", "warning", "washable shoes", "washbasin", "washing machine", "waste disposal", "watch", "watch time", "water collection tank", "water heater", "water level", "water pollution", "water treatment", "waterfall", "watering plants", "waterpower", "wax", "wealthy", "wealthy prince", "weapon", "weathers", "weed", "weeding", "weekend", "weight class", "welcome", "wetsuit", "whales", "wheelchair", "wheels", "white gold", "whiteboard", "whole", "wide", "wild", "willing", "windmills", "window iocks", "window view", "windows", "winds", "windsurfing", "wings", "winter", "wires", "wool", "words", "workbooks", "worker", "workforce", "workload", "workplace", "worksheet", "worms", "write", "write music", "writers", "writing", "written language", "written work", "wrong", "yellow", "yoga class", "young", "young children", "young graduates", "young people", "young teenagers", "zoom"];
var BUILTIN_DICTATION = {
    dictation: { id: 'dictation', name: '听力1000词', words: allWords, studyPage: 'listening.html', audioBase: '/tinglidanciceshi/audio/words/' },
    listening_basic: { id: 'listening_basic', name: '听力基础词汇', words: allWordsListeningBasic, studyPage: 'listening_basic.html', audioBase: '/tinglidanciceshi/audio/basic_words/' }
};
var currentDictationModuleId = 'dictation';
function getBuiltinDictation(moduleId) {
    const key = normalizeModuleType(moduleId || currentDictationModuleId);
    return BUILTIN_DICTATION[key] || BUILTIN_DICTATION.dictation;
}
function isBuiltinDictationModule(moduleId) {
    return !!BUILTIN_DICTATION[normalizeModuleType(moduleId)];
}


// 写作词伙分类数据（来自 xiezuocihuo 项目）
var phraseCategories = [
    {
        id: '小作文词伙一',
        name: '小作文词伙一',
        icon: '',
        group: '小作文',
        vocab: [
            { zh: '略微高于平均值', en: 'be slightly above the average' },
            { zh: '平稳地爬升', en: 'climb steadily/solidly' },
            { zh: '波动式爬升', en: 'climb up with fluctuations' },
            { zh: '持续上涨', en: 'continue to increase /soar' },
            { zh: '呈现持续的增长', en: 'display a continuous growth' },
            { zh: '从 38 稳定增长到 61', en: 'grow steadily from 38 to 61' },
            { zh: '在数值上呈现增长', en: 'illustrate an increase in a number' },
            { zh: '更快的增长', en: 'increase more rapidly' },
            { zh: '呈现一个大幅的增长', en: 'present a significant increase' },
            { zh: '匀速地增长', en: 'increase uniformly' },
            { zh: '急剧地下降', en: 'a dramatic decrease' },
            { zh: '一个快速的降幅', en: 'a drastic decrement' },
            { zh: '过去十年里一个轻微的下降', en: 'a modest dip/drop over the last decade' },
            { zh: '除了一次下跌以外', en: 'apart from a slump' },
            { zh: '预计会下降', en: 'be expected to fall steadily' },
            { zh: '继续保持下降', en: 'continue to decline' },
            { zh: '逐渐地从10%下降到 7%', en: 'decline gradually from 10% to 7%' },
            { zh: '明显地下降', en: 'decline noticeably' },
            { zh: '下降得越来越快', en: 'decrease more rapidly' },
            { zh: '尽管下降到1995年水平', en: 'despite a drop to 1995 level' },
        ],
    },
    {
        id: '小作文词伙二',
        name: '小作文词伙二',
        icon: '',
        group: '小作文',
        vocab: [
            { zh: '降到仅仅2.5%', en: 'dip/drop to only 2.5%' },
            { zh: '呈现轻微的下降', en: 'display a slight decrease' },
            { zh: '保持稳定', en: 'remain stable/steady' },
            { zh: '保持不变', en: 'stay unchanged' },
            { zh: '保持大概不变', en: 'remain roughly constant' },
            { zh: '在整个期间保持稳定', en: 'remain steady throughout the period' },
            { zh: '保持相同的水平', en: 'maintain the same level' },
            { zh: '达到 94%的峰值不变', en: 'reach a plateau at 94%' },
            { zh: '保持大致的不变的', en: 'remain roughly static' },
            { zh: '停滞了几乎十年', en: 'stagnated for nearly a decade' },
            { zh: '自从2000年以后稳定在19%', en: 'stabilize at 19% since 2000' },
            { zh: '预计会保持这个水平', en: 'be expected to maintain this level' },
            { zh: '伴随着波动下降', en: 'decrease with fluctuations' },
            { zh: '尽管最初有些波动', en: 'despite some initial fluctuations' },
            { zh: '降到34%的最低点', en: 'drop to its bottom at 34%' },
            { zh: '在 8000 位置上下波动', en: 'fluctuate around 8 thousand' },
            { zh: '微幅地波动', en: 'fluctuate moderately' },
            { zh: '在十年内波动式上升', en: 'fluctuate upwardly within a decade' },
            { zh: '增长的最大', en: 'have the biggest increase' },
            { zh: '在1995 年达到峰值 200 亿', en: 'peak at 2 billion in 1995' },
        ],
    },
    {
        id: '小作文词伙三',
        name: '小作文词伙三',
        icon: '',
        group: '小作文',
        vocab: [
            { zh: '占了学校预算的 25%', en: 'represent 25% of the school budget' },
            { zh: '增长超过八倍', en: 'rise more than eight fold' },
            { zh: '女性是男性的两倍', en: 'twice as many women as men' },
            { zh: '是2015 年的两倍尺寸大', en: 'be twice the size of it was in 2015' },
            { zh: '一个池子在东北角', en: 'a pond in the northeast corner' },
            { zh: '沿着街道南边', en: 'along the south side of the street' },
            { zh: '围绕着小镇中心', en: 'around the town center' },
            { zh: '在最初的阶段', en: 'at the initial stage' },
            { zh: '附加在紧挨着旅馆旁边', en: 'be added next to the hotel' },
            { zh: '被森林环绕', en: 'be circled by forests' },
            { zh: '紧挨在购物中心旁', en: 'be located on the shopping mall' },
            { zh: '在马路的对面', en: 'be on the opposite side of the road' },
            { zh: '经历三个不同的阶段', en: 'pass through three distinct stages' },
            { zh: '在最后的阶段', en: 'in the final phase/stage' },
            { zh: '在这个流程的第一阶段', en: 'at the first stage in the process' },
            { zh: '被整修成室内区域', en: 'be modified into an indoor area' },
            { zh: '被并列放置在了体育馆的左边(不接触)', en: 'be juxtaposed to the left of the gym' },
            { zh: '入口处的重新安置', en: 'the relocation of the entrance' },
            { zh: '被传送到一个地方进行混合', en: 'be transferred to a place to be mixed' },
            { zh: '把容器颠倒过来', en: 'turn the container upside down' },
        ],
    },
    {
        id: '暴力犯罪类',
        name: '暴力犯罪类',
        icon: '',
        group: '大作文',
        vocab: [
            { zh: '被绳之以法', en: 'be brought to justice' },
            { zh: '被认为是个威胁', en: 'be identified as a threat' },
            { zh: '违反法律', en: 'break laws' },
            { zh: '性格缺陷', en: 'character flaw' },
            { zh: '连带损伤', en: 'collateral damage' },
            { zh: '犯下严重的侵犯(罪)', en: 'commit serious offences' },
            { zh: '抑制犯罪', en: 'curb crime / deter crime' },
            { zh: '减少犯罪倾向', en: 'diminish criminal propensity' },
            { zh: '辨别是非', en: 'discriminate between right and wrong' },
            { zh: '危害社会稳定和安全', en: 'endanger social stability and safety' },
            { zh: '逃避惩罚', en: 'escape punishment' },
            { zh: '有震慑作用', en: 'have deterrent effect' },
            { zh: '憎恨社会', en: 'hold a grudge against society' },
            { zh: '侵犯隐私', en: 'intrusion of privacy' },
            { zh: '侵犯了..的隐私', en: 'invade one\'s privacy' },
            { zh: '青少年犯罪', en: 'juvenile delinquency' },
            { zh: '青少年罪犯', en: 'juvenile offenders' },
            { zh: '少年教养院', en: 'juvenile reformatory' },
            { zh: '守法的公民', en: 'law-abiding citizens' },
            { zh: '执法部门', en: 'law enforcement agencies' },
        ],
    },
    {
        id: '家庭旅游类',
        name: '家庭旅游类',
        icon: '',
        group: '大作文',
        vocab: [
            { zh: '满足他们的一些需求', en: 'address some of their needs' },
            { zh: '承担责任', en: 'assume the responsibility' },
            { zh: '平衡工作和生活', en: 'balance work and life' },
            { zh: '忙于家务', en: 'be swamped by household chores' },
            { zh: '被家务事拖累', en: 'be tied down to household chores' },
            { zh: '忙于他们的工作', en: 'bury themselves in work' },
            { zh: '车辆租赁公司', en: 'car rental company' },
            { zh: '生活成本', en: 'cost of living' },
            { zh: '导致人与人疏远', en: 'create alienation between people' },
            { zh: '可支配收入', en: 'disposable income' },
            { zh: '家务活', en: 'domestic chores' },
            { zh: '家庭暴力', en: 'domestic violence' },
            { zh: '促进旅游业的发展', en: 'facilitate the development of tourism' },
            { zh: '家庭归属感', en: 'family attachment' },
            { zh: '经济困难的家庭', en: 'financial-disadvantaged families' },
            { zh: '有好的生活质量', en: 'have a reasonable quality of life' },
            { zh: '家庭杂务', en: 'household chores' },
            { zh: '提高生活标准', en: 'improve living standards' },
            { zh: '保持低调', en: 'keep a low profile' },
            { zh: '过着充实的生活', en: 'lead a fulfilling life' },
        ],
    },
    {
        id: '健康饮食类',
        name: '健康饮食类',
        icon: '',
        group: '大作文',
        vocab: [
            { zh: '更好的生活质量', en: 'a better quality of life' },
            { zh: '采取健康的生活方式', en: 'adopt a healthy lifestyle' },
            { zh: '缓解粮食短缺', en: 'alleviate food shortage' },
            { zh: '对人们的健康有害', en: 'be harmful to human health' },
            { zh: '产生严重的健康问题', en: 'cause serious health problems' },
            { zh: '导致与压力相关的疾病', en: 'cause stress-related illness' },
            { zh: '转基因食品', en: 'genetically modified food' },
            { zh: '提高人们的生活水平', en: 'improve people\'s living standards' },
            { zh: '危害人类的健康', en: 'jeopardize human health' },
            { zh: '过着健康的生活', en: 'lead a healthy life' },
            { zh: '长期的副作用', en: 'long-term side effects' },
            { zh: '增加慢性疾病的患病率', en: 'increase the incidence of chronic illnesses' },
            { zh: '健康的饮食', en: 'a wholesome diet' },
            { zh: '提倡素食', en: 'advocate vegetarian diet' },
            { zh: '不健康的饮食', en: 'an unhealthy diet' },
            { zh: '是罪魁祸首', en: 'be the main culprit' },
            { zh: '不愿意戒烟', en: 'be unwilling to cease smoking' },
            { zh: '增强免疫力', en: 'boost the immune system' },
            { zh: '碳酸饮料', en: 'carbonated drinks' },
            { zh: '慢性疾病', en: 'chronic illnesses' },
        ],
    },
    {
        id: '媒体广告类',
        name: '媒体广告类',
        icon: '',
        group: '大作文',
        vocab: [
            { zh: '快速发展的产业', en: 'a fast-developing industry' },
            { zh: '真人秀节目', en: 'a reality TV program' },
            { zh: '针对儿童的广告宣传', en: 'advertisements aimed at children' },
            { zh: '被广告吸引', en: 'be intrigued by the advertisement' },
            { zh: '非常的昂贵', en: 'be prohibitively expensive' },
            { zh: '易受媒体的影响', en: 'be subjected to the influence of the media' },
            { zh: '冲动性购买产品', en: 'buy products on impulse' },
            { zh: '心血来潮买东西', en: 'buy something on a whim' },
            { zh: '代言一个体育服装品牌', en: 'endorse a brand of sportswear' },
            { zh: '代言一个指定的产品', en: 'endorse a particular brand' },
            { zh: '掩盖政治丑闻', en: 'cover up political scandals' },
            { zh: '刺激购买冲动', en: 'evoke impulsive buying' },
            { zh: '送货到家', en: 'have things delivered to their homes' },
            { zh: '高水平的媒体曝光', en: 'high level of media coverage' },
            { zh: '实施一定程度的审查', en: 'impose a degree of censorship' },
            { zh: '公益广告', en: 'non-profit advertisement' },
            { zh: '过度包装的商品', en: 'over-packaged products' },
            { zh: '黄金时段电视', en: 'prime-time television' },
            { zh: '娱乐业', en: 'show business' },
            { zh: '视觉享受', en: 'visual enjoyment' },
        ],
    },
    {
        id: '能源环保类',
        name: '能源环保类',
        icon: '',
        group: '大作文',
        vocab: [
            { zh: '以(牺牲)环境为代价', en: 'at the expense of the environment' },
            { zh: '禁止燃烧化石燃料', en: 'ban the burning of fossil fuels' },
            { zh: '对土壤退化视而不见', en: 'be blind to land degradation' },
            { zh: '对保护环境重要', en: 'be crucial to protecting the environment' },
            { zh: '对环境友好的', en: 'be environmentally friendly' },
            { zh: '有环境意识的', en: 'be environmentally conscious' },
            { zh: '破坏生态平衡', en: 'break ecological balance' },
            { zh: '造成不可逆转的损失', en: 'cause irreversible damage' },
            { zh: '构成了潜在的风险', en: 'constitute a potential risk' },
            { zh: '创造一个有利的环境', en: 'create a favorable condition' },
            { zh: '产生废气', en: 'create exhaust fumes' },
            { zh: '毁坏野生动物栖息地', en: 'destroy wildlife habitats' },
            { zh: '对生态系统产生深远的影响', en: 'exert a far-reaching impact on ecology' },
            { zh: '过渡地开采大自然', en: 'exploit the nature excessively' },
            { zh: '极端天气情况', en: 'extreme weather conditions' },
            { zh: '全球变暖', en: 'global warming' },
            { zh: '提高土地生产率', en: 'improve land productivity' },
            { zh: '导致..的迅速枯竭', en: 'lead to the rapid depletion of…' },
            { zh: '维持生态平衡', en: 'maintain the ecological balance' },
            { zh: '做出短期的牺牲', en: 'make the short-term sacrifice' },
        ],
    },
    {
        id: '品格教育类',
        name: '品格教育类',
        icon: '',
        group: '大作文',
        vocab: [
            { zh: '一种虐待的方式', en: 'a form of abuse' },
            { zh: '名牌大学', en: 'a prestigious university' },
            { zh: '在整个学校教育体系里', en: 'throughout the schooling system' },
            { zh: '放弃物质的追求', en: 'abandon the pursuit of materialism' },
            { zh: '改掉这一恶习', en: 'abandon the vile habit' },
            { zh: '学术能力', en: 'academic capabilities' },
            { zh: '学业优异的学生', en: 'academically advantaged students' },
            { zh: '发挥某人的潜力', en: 'achieve one\'s potential' },
            { zh: '适应未来的挑战', en: 'adapt to future challenges' },
            { zh: '承担教育花费', en: 'afford educational expenses' },
            { zh: '一个空头的承诺', en: 'an empty promise' },
            { zh: '重视教育背景', en: 'attach importance to education background' },
            { zh: '参加补习班', en: 'attend \'cram schools\'' },
            { zh: '避免拖延', en: 'avoid procrastination' },
            { zh: '从伦理上说是错误的/理论上说是错误的', en: 'be ethically wrong / theoretically wrong' },
            { zh: '遵从父母的意愿', en: 'be obedient to parents \'expectations' },
            { zh: '对学生带来巨大的好处', en: 'be of immense benefit to students' },
            { zh: '叛逆的', en: 'be rebellious' },
            { zh: '对他们的行为负责', en: 'be responsible for what they do' },
            { zh: '易受不良的影响', en: 'be vulnerable to negative influence' },
        ],
    },
    {
        id: '人文历史类',
        name: '人文历史类',
        icon: '',
        group: '大作文',
        vocab: [
            { zh: '全球性的语言', en: 'a global language' },
            { zh: '归属感', en: 'a sense of belonging' },
            { zh: '认同感', en: 'a sense of identity' },
            { zh: '习得一门外语', en: 'acquire a foreign language' },
            { zh: '建筑的风格', en: 'architectural styles' },
            { zh: '有经济和文化价值', en: 'be of commercial and cultural values' },
            { zh: '文化同化', en: 'cultural assimilation' },
            { zh: '文化退化', en: 'cultural devolution' },
            { zh: '文化多样性', en: 'cultural diversity' },
            { zh: '文化遗产', en: 'cultural heritage' },
            { zh: '文化身份', en: 'cultural identity' },
            { zh: '文化或历史景点', en: 'cultural or historical attractions' },
            { zh: '文化禁忌', en: 'cultural taboo' },
            { zh: '文化同一性', en: 'cultural uniformity' },
            { zh: '消除偏见和敌意', en: 'dispel prejudice and hostility' },
            { zh: '接受不同文化和价值观', en: 'embrace different cultures and values' },
            { zh: '濒临消失的语言', en: 'endangered language' },
            { zh: '表达个人品味和身份', en: 'express individual taste and identity' },
            { zh: '一直成为禁忌', en: 'have been a taboo' },
            { zh: '有利益冲突', en: 'have conflicting interests' },
        ],
    },
    {
        id: '商业职场类',
        name: '商业职场类',
        icon: '',
        group: '大作文',
        vocab: [
            { zh: '有成就感的事业', en: 'a fulfilling career' },
            { zh: '良好的工作前景', en: 'a good job prospect' },
            { zh: '前景乐观的职业', en: 'a promising career' },
            { zh: '工作的安全感', en: 'a sense of job security' },
            { zh: '失业期', en: 'a spell of unemployment' },
            { zh: '对一些技能精通', en: 'become proficient in some skills' },
            { zh: '职业愿景', en: 'career aspirations' },
            { zh: '职业成就', en: 'career achievement' },
            { zh: '上下班通勤时间', en: 'commuting time' },
            { zh: '竞争的优势', en: 'competitive advantage' },
            { zh: '消费品', en: 'consumer goods /products' },
            { zh: '培养人际关系能力', en: 'develop interpersonal skills' },
            { zh: '性别/年龄歧视', en: 'discriminate on the basis of gender' },
            { zh: '建立亲密的关系', en: 'build a close rapport' },
            { zh: '做出共同的努力', en: 'engage in a concerted effort' },
            { zh: '增加创造力', en: 'enhance creativity' },
            { zh: '增强团队合作', en: 'enhance teamwork spirit' },
            { zh: '建立性别平等', en: 'establish gender equality' },
            { zh: '没有实现工作生活的平衡', en: 'fail to achieve work-life balance' },
            { zh: '在他们工作中感觉安全', en: 'feel secure in their jobs' },
        ],
    },
    {
        id: '网络科技类',
        name: '网络科技类',
        icon: '',
        group: '大作文',
        vocab: [
            { zh: '比以前获取更多的信息', en: 'access more information than ever before' },
            { zh: '采用尖端的科技', en: 'adopt cutting-edge technology' },
            { zh: '寻求在线退款复杂而低效', en: 'be cumbersome to seek a refund online' },
            { zh: '可以无限制的上网', en: 'be given unlimited Internet access' },
            { zh: '沉溺于在线游戏', en: 'be addicted to online games' },
            { zh: '被网购快速的取代', en: 'be rapidly giving way to online shopping' },
            { zh: '被看做是一种必须的装备', en: 'be seen as a must-have device' },
            { zh: '不被诱惑干扰', en: 'be undistracted by temptations' },
            { zh: '成为一种耗费时间的诱惑', en: 'be a time-consuming temptation' },
            { zh: '又流行起来', en: 'come back into fashion' },
            { zh: '通过互联网和他人交流', en: 'communicate with others via the Internet' },
            { zh: '包含敏感信息', en: 'contain sensitive information' },
            { zh: '尖端的技术', en: 'cutting-edge technology' },
            { zh: '网络约会', en: 'digital/online dating' },
            { zh: '网络科技的革新', en: 'digital revolution' },
            { zh: '分散他们的注意力', en: 'distract their attention' },
            { zh: '运用最新科技技术', en: 'employ cutting-edge technology' },
            { zh: '没有抵挡住的诱惑', en: 'fail to resist the lure of...' },
            { zh: '政府对互联网的审查', en: 'government censorship of the Internet' },
            { zh: '安装过滤软件', en: 'install filtering software' },
        ],
    },
    {
        id: '政府社会类',
        name: '政府社会类',
        icon: '',
        group: '大作文',
        vocab: [
            { zh: '预算盈余', en: 'a budget surplus' },
            { zh: '公众对税收政策的强烈反对', en: 'a public backlash against tax policy' },
            { zh: '安全感', en: 'a sense of security' },
            { zh: '流动人口', en: 'a transient population' },
            { zh: '摒弃我们的传统习俗', en: 'abandon our traditional custom' },
            { zh: '积累社会经验', en: 'accumulate social experience' },
            { zh: '适应一个新环境', en: 'adapt to a new environment' },
            { zh: '足够的可支配收入', en: 'adequate disposable income' },
            { zh: '倡导新的生活方式', en: 'advocate the new lifestyle' },
            { zh: '老龄化人群', en: 'the elderly / the senior population' },
            { zh: '社会各个阶层', en: 'all walks of life' },
            { zh: '与现实隔绝', en: 'be detached from reality' },
            { zh: '逐渐得到社会重视', en: 'be increasingly valued by society' },
            { zh: '有更高的社会接受度', en: 'be more socially acceptable' },
            { zh: '成为政府首要任务', en: 'be the government\'s priority' },
            { zh: '处在贫困线以下', en: 'below the poverty line' },
            { zh: '迫于公众压力', en: 'bow to public pressure' },
            { zh: '带来不可估量的经济效益', en: 'bring immeasurable economic benefits' },
        ],
    },
];

// 基础词伙（高频核心写作词伙）
var foundationPhrases = [
    { zh: "一系列的问题", en: "a barrage of problems" },
    { zh: "一个产生影响的因素", en: "a contributing factor" },
    { zh: "关注的焦点", en: "a focus of attention" },
    { zh: "越来越多的证据", en: "a growing body of evidence" },
    { zh: "一件备受关注的事", en: "a matter of heightened concern" },
    { zh: "一个更可行的方法", en: "a more feasible approach" },
    { zh: "满足感", en: "a sense of fulfillment" },
    { zh: "一个非常短视的观点", en: "a very shortsighted view" },
    { zh: "重要的组成部分", en: "a vital component" },
    { zh: "大量的信息", en: "a wealth of information" },
    { zh: "一个众所周知的事实", en: "a well-known fact" },
    { zh: "各种各样的选择", en: "a wide range of options" },
    { zh: "大量的证据", en: "ample evidence" },
    { zh: "主要的原因", en: "primary cause" },
    { zh: "一个问题的症结", en: "the crux of a problem" },
    { zh: "迫在眉睫的危机", en: "the looming crisis" },
    { zh: "最主要的障碍", en: "the major barrier" },
    { zh: "自我满足感", en: "a sense of self-fulfillment" },
    { zh: "令人信服的证据", en: "compelling evidence" },
    { zh: "令人信服的理由", en: "compelling reasons" }
];

// 学习进度模块配置
// url: 外部页面链接（为空表示本页面内功能）
// target_type: 'fixed' = 固定目标, 'dynamic' = 根据学生目标分数动态计算
// 标准来源：雅思目标拆分.xlsx
var MODULES = [
    // 一、需要掌握百分比
    { id: 'writing_words', name: '小初单词', target_type: 'dynamic', targets: { 6: 100, 6.5: 100, 7: 100 }, unit: '%', url: '', icon: 'pencil' },
    { id: 'highschool_words', name: '高中单词', target_type: 'dynamic', targets: { 6: 85, 6.5: 95, 7: 100 }, unit: '%', url: '', icon: 'book' },
    { id: 'ielts_core', name: '雅思核心800词', target_type: 'dynamic', targets: { 6: 65, 6.5: 80, 7: 95 }, unit: '%', url: '', icon: 'star' },
    { id: 'grammar', name: '基础语法', target_type: 'dynamic', targets: { 6: 75, 6.5: 85, 7: 85 }, unit: '%', url: '', icon: 'academic' },
    { id: 'reading_synonym', name: '阅读同义替换', target_type: 'dynamic', targets: { 6: 70, 6.5: 80, 7: 90 }, unit: '%', url: '../tongyitihuan/index.html', test_url: '../tongyitihuanceshi/index.html', icon: 'eye' },
    { id: 'sentence', name: '长难句分析', target_type: 'dynamic', targets: { 6: 60, 6.5: 80, 7: 80 }, unit: '%', url: '../changnanju/index.html', test_url: '../changnanjuceshi/index.html', icon: 'analysis' },
    { id: 'dictation', name: '听力1000词', target_type: 'dynamic', targets: { 6: 70, 6.5: 80, 7: 90 }, unit: '%', url: '', icon: 'headphones' },
    { id: 'listening_basic', name: '听力基础词汇', target_type: 'dynamic', targets: { 6: 70, 6.5: 80, 7: 90 }, unit: '%', url: '', icon: 'headphones' },
    { id: 'listening_synonym', name: '听力同义替换', target_type: 'dynamic', targets: { 6: 70, 6.5: 80, 7: 90 }, unit: '%', url: '../daanjutingxie/index.html', test_url: '../daanjutingxieceshi/index.html', icon: 'headphones' },
    { id: 'writing_phrase', name: '写作词伙', target_type: 'dynamic', targets: { 6: 50, 6.5: 70, 7: 90 }, unit: '%', url: '../xiezuocihuo/index.html', test_url: '../xiezuocihuoceshi/index.html', icon: 'writing' },
    { id: 'writing_translate', name: '写作句子翻译', target_type: 'dynamic', targets: { 6: 50, 6.5: 70, 7: 90 }, unit: '%', url: '../juzifanyixin/index.html', test_url: '', icon: 'translate' },
    { id: 'writing_correction', name: '作文批改', target_type: 'dynamic', targets: { 6: 1, 6.5: 1, 7: 1 }, unit: '次', url: '../xiezuopigai/ielts-student-practice.html', test_url: '', icon: 'edit' },
    
    // 二、听力P4跟读：学习页练倍速，测试页按跟读匹配率计分（%）
    { id: 'listening_p4_speed', name: '听力P4跟读倍速', target_type: 'dynamic', targets: { 6: 70, 6.5: 80, 7: 90 }, unit: '%', url: '../P4gendu/index.html', test_url: '../P4genduceshi/index.html', icon: 'mic' },
    
    // 三、每项需要答对个数
    { id: 'reading_p1', name: '第一篇阅读', target_type: 'dynamic', targets: { 6: 9, 6.5: 11, 7: 12 }, unit: '个', url: '', icon: 'eye' },
    { id: 'reading_p2', name: '第二篇阅读', target_type: 'dynamic', targets: { 6: 8, 6.5: 10, 7: 10 }, unit: '个', url: '', icon: 'eye' },
    { id: 'reading_p3', name: '第三篇阅读', target_type: 'dynamic', targets: { 6: 6, 6.5: 6, 7: 8 }, unit: '个', url: '', icon: 'eye' },
    { id: 'listening_p1', name: '听力P1', target_type: 'dynamic', targets: { 6: 8, 6.5: 9, 7: 9 }, unit: '个', url: '', icon: 'headphones' },
    { id: 'listening_p2', name: '听力P2', target_type: 'dynamic', targets: { 6: 7, 6.5: 8, 7: 9 }, unit: '个', url: '', icon: 'headphones' },
    { id: 'listening_p3', name: '听力P3', target_type: 'dynamic', targets: { 6: 4, 6.5: 4, 7: 5 }, unit: '个', url: '', icon: 'headphones' },
    { id: 'listening_p4', name: '听力P4', target_type: 'dynamic', targets: { 6: 4, 6.5: 6, 7: 7 }, unit: '个', url: '', icon: 'headphones' },
    
    // 四、雅思单项目标分数
    { id: 'speaking', name: '口语练习', target_type: 'dynamic', targets: { 6: 5.5, 6.5: 6, 7: 6.5 }, unit: '分', url: '/kouyulianxi/index.html?build=20260822d', test_url: '/kouyulianxi/index.html', icon: 'message' },
    { id: 'writing_essay', name: '写作大作文', target_type: 'dynamic', targets: { 6: 5.5, 6.5: 6, 7: 6.5 }, unit: '分', url: '', icon: 'edit' },
    { id: 'writing_small', name: '写作小作文', target_type: 'dynamic', targets: { 6: 5.5, 6.5: 6, 7: 6.5 }, unit: '分', url: '', icon: 'edit' }
];

// 根据学生目标分数获取模块目标
function getModuleTarget(m) {
    if (m.target_type === 'dynamic' && m.targets) {
        const targetScore = currentStudent.target_score || 6.5;
        return m.targets[targetScore] || m.targets[6.5] || 80;
    }
    return m.target;
}

function getModuleTargetForScore(m, targetScore) {
    if (m && m.target_type === 'dynamic' && m.targets) {
        return m.targets[targetScore] || m.targets[6.5] || 80;
    }
    return m ? m.target : 80;
}

function getModuleById(moduleType) {
    const normalized = normalizeModuleType(moduleType);
    return MODULES.find(function(m) { return m.id === normalized; }) || null;
}

// 判断模块是否已开发上线：听力1000词为内置功能始终可用，
// 其余模块必须配置学习页面或测试页面才展示，避免暴露待开发页面
function isModuleAvailable(m) {
    return isBuiltinDictationModule(m.id) || !!m.url || !!m.test_url;
}

function normalizeModuleType(moduleType) {
    const map = {
        dictation_learn: 'dictation',
        listening_basic_learn: 'listening_basic',
        reading_synonym_test: 'reading_synonym',
        writing_phrase_test: 'writing_phrase',
        sentence_test: 'sentence',
        listening_synonym_test: 'listening_synonym',
        speaking_p1: 'speaking',
        speaking_p2: 'speaking',
        speaking_p3: 'speaking'
    };
    return map[moduleType] || moduleType || 'dictation';
}

function getModuleRecords(records, moduleId) {
    return (records || []).filter(function(r) {
        return normalizeModuleType(r.module_type || 'dictation') === moduleId;
    });
}

function getModuleSessions(sessions, moduleId) {
    return (sessions || []).filter(function(s) {
        return normalizeModuleType(s.module_type || 'dictation') === moduleId;
    });
}

function getStudySessions(sessions) {
    return window.TrackingUtils.filterStudySessions(sessions);
}

function getModuleStudySessions(sessions, moduleId) {
    return getModuleSessions(getStudySessions(sessions), moduleId);
}

function formatDuration(seconds) {
    seconds = Math.max(0, Number(seconds) || 0);
    if (seconds <= 0) return '-';
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    if (hours > 0) return hours + '小时' + mins + '分钟';
    if (mins > 0) return mins + '分钟' + secs + '秒';
    return secs + '秒';
}

function getSpeakingPracticedCount(sessions) {
    return (sessions || []).reduce(function(sum, s) {
        return sum + (Number(s.words_tested) || 0);
    }, 0);
}

function getSpeakingTotalQuestions(sessions) {
    var total = 0;
    (sessions || []).forEach(function(s) {
        var details = s.details;
        if (typeof details === 'string') {
            try { details = JSON.parse(details); } catch (e) { details = []; }
        }
        if (!Array.isArray(details)) return;
        details.forEach(function(d) {
            if (d && d.totalQuestions) total = Math.max(total, Number(d.totalQuestions) || 0);
        });
    });
    return total;
}

function getBestScore(records) {
    if (!records || records.length === 0) return 0;
    return Math.max.apply(null, records.map(function(r) { return Number(r.score) || 0; }));
}

function getPassCount(records) {
    return (records || []).filter(function(r) { return !!r.is_passed; }).length;
}

function getStudentTargetScoreValue(student) {
    const score = Number((student || currentStudent || {}).target_score);
    if (score === 6 || score === 7) return score;
    return 6.5;
}

function formatTargetValue(value, unit) {
    if (unit === '%') return value + '%';
    return value + (unit || '');
}

function getChinaDateKey(value) {
    return new Date(value || Date.now()).toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai' });
}

var _studentStandardsCache = null;
async function getPassThreshold(moduleId, student) {
    const normalized = normalizeModuleType(moduleId);
    const module = getModuleById(normalized);
    let threshold = getModuleTargetForScore(module, getStudentTargetScoreValue(student));
    try {
        if (!_studentStandardsCache) {
            const standardsResult = await apiFetch('/api/student/standards');
            if (standardsResult.error) throw new Error(standardsResult.error.message || 'standards error');
            _studentStandardsCache = standardsResult.data || [];
        }
        const row = (_studentStandardsCache || []).find(function(item) {
            return item.module_type === normalized;
        });
        if (row) {
            const targetScore = getStudentTargetScoreValue(student);
            if (targetScore === 7) threshold = row.score_7;
            else if (targetScore === 6) threshold = row.score_6;
            else threshold = row.score_6_5;
        }
    } catch (e) {
        console.warn('读取达标线失败，使用模块默认值:', e);
    }
    return Number(threshold) || 80;
}

const studySaveCache = {};

function appendModuleParams(url, params) {
    try {
        const finalUrl = new URL(url, window.location.href);
        Object.keys(params).forEach(function(key) {
            if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
                finalUrl.searchParams.set(key, params[key]);
            }
        });
        return finalUrl.href;
    } catch (e) {
        const query = Object.keys(params).filter(function(key) {
            return params[key] !== undefined && params[key] !== null && params[key] !== '';
        }).map(function(key) {
            return encodeURIComponent(key) + '=' + encodeURIComponent(params[key]);
        }).join('&');
        return url + (url.indexOf('?') >= 0 ? '&' : '?') + query;
    }
}

function buildDailyStudyRows(sessions, moduleId) {
    const rows = {};
    getStudySessions(sessions).forEach(function(session) {
        const dateKey = getChinaDateKey(session.created_at);
        if (!rows[dateKey]) {
            rows[dateKey] = { date: dateKey, moduleSeconds: 0, totalSeconds: 0, moduleCount: 0, totalCount: 0, latest: session.created_at };
        }
        const seconds = Number(session.duration_seconds) || 0;
        rows[dateKey].totalSeconds += seconds;
        rows[dateKey].totalCount += 1;
        if (normalizeModuleType(session.module_type) === moduleId) {
            rows[dateKey].moduleSeconds += seconds;
            rows[dateKey].moduleCount += 1;
        }
        if (new Date(session.created_at) > new Date(rows[dateKey].latest)) rows[dateKey].latest = session.created_at;
    });
    return Object.keys(rows).map(function(key) { return rows[key]; }).sort(function(a, b) {
        return new Date(b.latest) - new Date(a.latest);
    });
}
