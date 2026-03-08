# Top 75 US Vehicles 2025 - Vehicle List
vehicles = [
    {"rank": 1, "brand": "Ford", "model": "F-150", "trims": ["F-150"], "segment": "Full-Size Truck", "sales": 828832},
    {"rank": 2, "brand": "Ford", "model": "Explorer", "trims": ["XLT", "ST", "Platinum", "Tremor"], "segment": "Three-Row SUV", "sales": 222706},
    {"rank": 3, "brand": "Ford", "model": "Escape", "trims": ["S", "SE", "SEL", "Titanium"], "segment": "Compact SUV", "sales": 143434},
    {"rank": 4, "brand": "Ford", "model": "Bronco", "trims": ["Base", "Big Bend", "Black Diamond", "Wildtrak"], "segment": "Mid-Size SUV", "sales": 146007},
    {"rank": 5, "brand": "Ford", "model": "Maverick", "trims": ["XL", "XLT", "Lariat", "King Ranch"], "segment": "Compact Truck", "sales": 155051},
    {"rank": 6, "brand": "Chevrolet", "model": "Silverado", "trims": ["WT", "RST", "LT", "High Country", "ZR2"], "segment": "Full-Size Truck", "sales": 362909},
    {"rank": 7, "brand": "Chevrolet", "model": "Equinox", "trims": ["LS", "LT", "RS", "Premier", "ACTIV"], "segment": "Compact SUV", "sales": 274356},
    {"rank": 8, "brand": "Chevrolet", "model": "Trax", "trims": ["LS", "LT", "RS", "ACTIV"], "segment": "Subcompact SUV", "sales": 206339},
    {"rank": 9, "brand": "Chevrolet", "model": "Traverse", "trims": ["LS", "LT", "Premier", "High Country"], "segment": "Three-Row SUV", "sales": 148278},
    {"rank": 10, "brand": "Chevrolet", "model": "Tahoe", "trims": ["LS", "LT", "RST", "High Country"], "segment": "Full-Size SUV", "sales": 114202},
    {"rank": 11, "brand": "Toyota", "model": "RAV4", "trims": ["LE", "XLE", "Adventure", "Prime"], "segment": "Compact SUV", "sales": 479288},
    {"rank": 12, "brand": "Toyota", "model": "Camry", "trims": ["LE", "XLE", "SE", "TRD"], "segment": "Midsize Sedan", "sales": 316185},
    {"rank": 13, "brand": "Toyota", "model": "Tacoma", "trims": ["SR", "SR5", "TRD", "Limited"], "segment": "Compact Truck", "sales": 274638},
    {"rank": 14, "brand": "Toyota", "model": "Corolla", "trims": ["L", "LE", "SE", "XLE"], "segment": "Compact Sedan", "sales": 310000},
    {"rank": 15, "brand": "Toyota", "model": "Highlander", "trims": ["L", "LE", "XLE", "Limited", "Platinum"], "segment": "Three-Row SUV", "sales": 235000},
    {"rank": 16, "brand": "Honda", "model": "CR-V", "trims": ["LX", "EX", "EX-L", "Sport Touring"], "segment": "Compact SUV", "sales": 403768},
    {"rank": 17, "brand": "Honda", "model": "Civic", "trims": ["Sport", "EX", "Touring", "Si", "Type R"], "segment": "Compact Car", "sales": 242005},
    {"rank": 18, "brand": "Honda", "model": "Accord", "trims": ["Sport", "EX", "EX-L", "Touring"], "segment": "Midsize Sedan", "sales": 174000},
    {"rank": 19, "brand": "Honda", "model": "Pilot", "trims": ["EX", "EX-L", "Touring", "Elite"], "segment": "Three-Row SUV", "sales": 124209},
    {"rank": 20, "brand": "Honda", "model": "HR-V", "trims": ["LX", "EX", "EX-L", "Sport Touring"], "segment": "Subcompact SUV", "sales": 148871},
    {"rank": 21, "brand": "RAM", "model": "1500", "trims": ["Tradesman", "Big Horn", "Laramie", "Rebel"], "segment": "Full-Size Truck", "sales": 254000},
    {"rank": 22, "brand": "RAM", "model": "2500 HD", "trims": ["Tradesman", "Power Wagon", "Laramie", "Limited"], "segment": "Heavy-Duty Truck", "sales": 74000},
    {"rank": 23, "brand": "RAM", "model": "3500 HD", "trims": ["Tradesman", "Laramie", "Limited", "SRW/DRW"], "segment": "Heavy-Duty Truck", "sales": 32000},
    {"rank": 24, "brand": "RAM", "model": "ProMaster", "trims": ["2500", "3500", "Cargo", "Passenger"], "segment": "Cargo Van", "sales": 35000},
    {"rank": 25, "brand": "RAM", "model": "Chassis Cab", "trims": ["2500", "3500", "4500", "5500"], "segment": "Commercial Platform", "sales": 12000},
    {"rank": 26, "brand": "GMC", "model": "Sierra", "trims": ["Pro", "SLE", "AT4", "Denali", "Denali Ultimate"], "segment": "Full-Size Truck", "sales": 267000},
    {"rank": 27, "brand": "GMC", "model": "Yukon", "trims": ["SLE", "SLT", "AT4", "Denali"], "segment": "Full-Size SUV", "sales": 87000},
    {"rank": 28, "brand": "GMC", "model": "Yukon XL", "trims": ["SLE", "SLT", "AT4", "Denali"], "segment": "Full-Size SUV", "sales": 58000},
    {"rank": 29, "brand": "GMC", "model": "Terrain", "trims": ["SL", "SLE", "SLT", "Denali"], "segment": "Compact SUV", "sales": 95000},
    {"rank": 30, "brand": "GMC", "model": "Acadia", "trims": ["SL", "SLE", "SLT", "AT4", "Denali"], "segment": "Three-Row SUV", "sales": 78000},
    {"rank": 31, "brand": "Nissan", "model": "Rogue", "trims": ["S", "SV", "SL", "Platinum"], "segment": "Compact SUV", "sales": 245000},
    {"rank": 32, "brand": "Nissan", "model": "Altima", "trims": ["2.5 S", "2.5 SV", "3.5 SL", "3.5 Platinum"], "segment": "Midsize Sedan", "sales": 98000},
    {"rank": 33, "brand": "Nissan", "model": "Sentra", "trims": ["S", "SV", "SR", "SL"], "segment": "Compact Sedan", "sales": 92000},
    {"rank": 34, "brand": "Nissan", "model": "Murano", "trims": ["S", "SV", "SL", "Platinum"], "segment": "Midsize SUV", "sales": 87000},
    {"rank": 35, "brand": "Nissan", "model": "Ariya", "trims": ["Sensible", "Customizable", "Performance"], "segment": "EV Crossover", "sales": 57000},
    {"rank": 36, "brand": "Hyundai", "model": "Tucson", "trims": ["SE", "SEL", "Ultimate", "N Line"], "segment": "Compact SUV", "sales": 315000},
    {"rank": 37, "brand": "Hyundai", "model": "Elantra", "trims": ["SE", "SEL", "Limited", "N"], "segment": "Compact Sedan", "sales": 142404},
    {"rank": 38, "brand": "Hyundai", "model": "Santa Fe", "trims": ["SE", "SEL", "Limited", "Ultimate", "N Line"], "segment": "Midsize SUV", "sales": 142404},
    {"rank": 39, "brand": "Hyundai", "model": "Palisade", "trims": ["SE", "SEL", "Limited", "Calligraphy"], "segment": "Three-Row SUV", "sales": 123929},
    {"rank": 40, "brand": "Hyundai", "model": "Venue", "trims": ["SE", "SEL", "Ultimate"], "segment": "Subcompact SUV", "sales": 29805},
    {"rank": 41, "brand": "Kia", "model": "Sportage", "trims": ["LX", "S", "EX", "SX", "GT-Line"], "segment": "Compact SUV", "sales": 318000},
    {"rank": 42, "brand": "Kia", "model": "K4", "trims": ["LX", "S", "EX", "GT-Line"], "segment": "Compact Sedan", "sales": 132000},
    {"rank": 43, "brand": "Kia", "model": "Telluride", "trims": ["LX", "S", "EX", "SX"], "segment": "Three-Row SUV", "sales": 125000},
    {"rank": 44, "brand": "Kia", "model": "Seltos", "trims": ["LX", "S", "EX"], "segment": "Subcompact SUV", "sales": 95000},
    {"rank": 45, "brand": "Kia", "model": "Niro", "trims": ["LX", "S", "EX", "SX", "EV"], "segment": "Compact SUV/Hybrid", "sales": 88000},
    {"rank": 46, "brand": "Jeep", "model": "Wrangler", "trims": ["Sport", "Willys", "Rubicon", "392"], "segment": "Compact SUV/Off-Road", "sales": 193000},
    {"rank": 47, "brand": "Jeep", "model": "Grand Cherokee", "trims": ["Laredo", "Limited", "Trailhawk", "Summit"], "segment": "Midsize SUV", "sales": 132000},
    {"rank": 48, "brand": "Jeep", "model": "Cherokee", "trims": ["Latitude", "Limited", "Trailhawk"], "segment": "Compact SUV", "sales": 98000},
    {"rank": 49, "brand": "Jeep", "model": "Compass", "trims": ["Sport", "Latitude", "Limited", "Trailhawk"], "segment": "Subcompact SUV", "sales": 87000},
    {"rank": 50, "brand": "Jeep", "model": "Renegade", "trims": ["Sport", "Latitude", "Limited", "Trailhawk"], "segment": "Subcompact SUV", "sales": 48000},
    {"rank": 51, "brand": "Subaru", "model": "Crosstrek", "trims": ["Base", "Premium", "Sport", "Limited"], "segment": "Compact SUV", "sales": 168000},
    {"rank": 52, "brand": "Subaru", "model": "Outback", "trims": ["Base", "Premium", "Onyx Edition", "Limited"], "segment": "Midsize Wagon", "sales": 145000},
    {"rank": 53, "brand": "Subaru", "model": "Forester", "trims": ["Base", "Premium", "Sport", "Limited", "Touring"], "segment": "Compact SUV", "sales": 142000},
    {"rank": 54, "brand": "Subaru", "model": "Legacy", "trims": ["Base", "Premium", "Sport", "Limited"], "segment": "Midsize Sedan", "sales": 95000},
    {"rank": 55, "brand": "Subaru", "model": "Ascent", "trims": ["Base", "Premium", "Limited", "Touring"], "segment": "Three-Row SUV", "sales": 78000},
    {"rank": 56, "brand": "Mazda", "model": "CX-5", "trims": ["2.5 S", "2.5 Preferred", "2.5 Premium", "Turbo"], "segment": "Compact SUV", "sales": 145000},
    {"rank": 57, "brand": "Mazda", "model": "CX-50", "trims": ["2.5 S", "2.5 Preferred", "2.5 Premium", "Turbo"], "segment": "Compact SUV", "sales": 118000},
    {"rank": 58, "brand": "Mazda", "model": "Mazda3", "trims": ["2.5 S", "2.5 Preferred", "2.5 Premium"], "segment": "Compact Car", "sales": 87000},
    {"rank": 59, "brand": "Mazda", "model": "CX-30", "trims": ["2.5 S", "2.5 Preferred", "2.5 Premium"], "segment": "Subcompact SUV", "sales": 82000},
    {"rank": 60, "brand": "Mazda", "model": "Mazda6", "trims": ["2.5 S", "2.5 Preferred", "2.5 Premium"], "segment": "Midsize Sedan", "sales": 45000},
    {"rank": 61, "brand": "Volkswagen", "model": "Jetta", "trims": ["S", "SE", "SEL", "GLI"], "segment": "Compact Sedan", "sales": 94000},
    {"rank": 62, "brand": "Volkswagen", "model": "Passat", "trims": ["2.0T", "2.0T R-Line", "V6"], "segment": "Midsize Sedan", "sales": 67000},
    {"rank": 63, "brand": "Volkswagen", "model": "Tiguan", "trims": ["S", "SE", "SEL", "R"], "segment": "Compact SUV", "sales": 92000},
    {"rank": 64, "brand": "Volkswagen", "model": "ID.4", "trims": ["Standard", "Pro", "Pro S", "Pro Max"], "segment": "Compact EV", "sales": 62000},
    {"rank": 65, "brand": "Volkswagen", "model": "Golf", "trims": ["S", "SE", "GTI", "R"], "segment": "Compact Hatchback", "sales": 58000},
    {"rank": 66, "brand": "Tesla", "model": "Model Y", "trims": ["Standard", "Long Range", "Performance"], "segment": "Compact/Midsize EV", "sales": 300000},
    {"rank": 67, "brand": "Tesla", "model": "Model 3", "trims": ["Standard", "Long Range", "Performance"], "segment": "Compact EV Sedan", "sales": 90000},
    {"rank": 68, "brand": "Tesla", "model": "Model X", "trims": ["Long Range", "Plaid"], "segment": "Midsize EV SUV", "sales": 45000},
    {"rank": 69, "brand": "Tesla", "model": "Model S", "trims": ["Long Range", "Plaid"], "segment": "Premium EV Sedan", "sales": 38000},
    {"rank": 70, "brand": "Tesla", "model": "Cybertruck", "trims": ["RWD", "AWD", "Cyberbeast"], "segment": "Electric Pickup", "sales": 62000},
    {"rank": 71, "brand": "Lexus", "model": "RX", "trims": ["350h", "350", "500h", "F Sport"], "segment": "Midsize Luxury SUV", "sales": 155000},
    {"rank": 72, "brand": "Lexus", "model": "NX", "trims": ["350h", "350", "500h", "F Sport"], "segment": "Compact Luxury SUV", "sales": 128000},
    {"rank": 73, "brand": "Lexus", "model": "ES", "trims": ["250", "350", "350h", "F Sport"], "segment": "Midsize Luxury Sedan", "sales": 74000},
    {"rank": 74, "brand": "Lexus", "model": "GX", "trims": ["550", "F Sport", "Overtrail"], "segment": "Full-Size Luxury SUV", "sales": 68000},
    {"rank": 75, "brand": "Lexus", "model": "LX", "trims": ["570h", "F Sport", "Ultra Luxury"], "segment": "Full-Size Luxury SUV", "sales": 42000},
]

def get_vehicle_list():
    """Return the list of top 75 vehicles."""
    return vehicles

def get_vehicle_by_rank(rank):
    """Get a specific vehicle by rank."""
    for vehicle in vehicles:
        if vehicle["rank"] == rank:
            return vehicle
    return None

def get_vehicles_by_brand(brand):
    """Get all vehicles from a specific brand."""
    return [v for v in vehicles if v["brand"].lower() == brand.lower()]
