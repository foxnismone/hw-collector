#!/usr/bin/env python3
"""Integra fotos, currículum y proyectos de diseñadores + asigna diseñadores a modelos."""

import json
import re

# Datos extraídos de Fandom Wiki (web_extract) - 2025
DATOS_FANDOM = {
    'Ira Gilford': {
        'foto': 'https://static.wikia.nocookie.net/hotwheels/images/7/7a/Ira_Gilford_Header.jpg/revision/latest/scale-to-width-down/300',
        'bio': 'Ira Bailey Gilford is a former Hot Wheels designer who worked at Mattel from 1967 to 1970. He is most known for designing a large number of the 1969 cars, The Spoilers, The Heavys and most notably, the Twin Mill, Hot Wheels\'s first original design. Prior to working for Mattel, Gilford worked for the Chrysler Corporation. Gilford was recommended to the position by his friend Harry Bradley, Hot Wheels\'s first designer. Gilford left Mattel around 1970. He currently works as an independent contractor in the digital arts field and a painter.',
        'periodo': '1967-1970',
        'nacionalidad': 'Estadounidense',
        'proyectos': ['Custom Volkswagen', 'Brabham Repco F1', 'Chaparral 2G', 'Classic \'31 Ford Woody', 'Classic \'32 Ford Vicky', 'Classic \'36 Ford Coupe', 'Classic \'57 T-Bird', 'Custom AMX', 'Custom Charger', 'Custom Continental Mark III', 'Custom Police Cruiser', 'Ford Mark IV', 'Indy Eagle', 'Lola GT70', 'Lotus Turbine', 'Maserati Mistral', 'McLaren M6A', 'Mercedes-Benz 280SL', 'Rolls-Royce Silver Shadow', 'Shelby Turbine', 'Splittin\' Image', 'Torero', 'Turbofire', 'Twin Mill', 'Volkswagen Beach Bomb', 'Ambulance', 'Carabo', 'Cement Mixer', 'Classic Nomad', 'Dump Truck', 'Ferrari 312P', 'Fire Engine', 'Heavy Chevy', 'King \'Kuda', 'Light My Firebird', 'Mantis', 'Moving Van', 'Nitty Gritty Kitty', 'Porsche 917', 'Power Pad', 'Swingin\' Wing', 'TNT-Bird', 'Tow Truck', 'Boss Hoss', 'Fuel Tanker', 'Racer Rig', 'Scooper', 'Snorkel', 'Sugar Caddy', 'Team Trailer', 'Waste Wagon', 'Exhausted', 'Billboard Truck', 'Racing Truck', 'Ramp Truck', 'Vending Truck'],
    },
    'Harry Bradley': {
        'foto': 'https://static.wikia.nocookie.net/hotwheels/images/9/9c/HarryBradley.jpg/revision/latest/scale-to-width-down/300',
        'bio': 'Harry Bentley Bradley was an American automotive designer who is often considered the father of Hot Wheels designs; as Hot Wheels\'s very first designer, he created the original "Sweet 16" cars of 1968. Bradley worked for Mattel from 1966 to 1969. Born in Boston in 1936, Bradley suffered polio from a young age; despite this, he nurtured his talents drawing automobiles and continued sketching in hospitals as he received treatment for his condition. Prior to working for Hot Wheels, Bradley worked for General Motors, having been recruited in 1962, as well as being a builder of his own show cars such as the La Jolla, Blind Faith and the Deora. Bradley was recruited by Mattel in 1966, who wanted a designer from one of the Big 3 automakers to help design their vehicles. Bradley drove his 1964 Chevrolet El Camino to California; it is said that Mattel founder Elliot Handler saw Bradley\'s El Camino in the parking lot and quipped "Those are some hot wheels." Bradley\'s ties with GM were pivotal to the creation of some of the earliest Hot Wheels models. Lore has it that to design one of these GM models, the Custom Corvette, Bradley drove to Detroit in 1967 and snuck into GM\'s offices after working hours. Having worked in GM\'s design offices in the past, he was able to locate the area where the design blueprints were stored; he would take the blueprints for the upcoming 1968 Corvette by hiding them in his crutches, then drive back to California where he designed the model off those blueprints. Due to this it is often claimed the Hot Wheels version of the Corvette came out before the actual Corvette hit dealerships, much to GM\'s consternation, although various dating of prototypes and the corroboration of other dates states that this might not have been the case. Regardless, the Corvette was a highly popular model and caused great publicity for Mattel. Bradley left Mattel in 1969. The story behind how he left varies; some sources say he felt Hot Wheels would not take off and as such left the brand thinking it would only be a fad, while other sources say he was fired due to his refusal to be reassigned to the staples division of Mattel, with his manager fully convinced that the Hot Wheels line would fail. Others state that his firing might have been related to the aforementioned stunt he pulled regarding the Custom Corvette if indeed he did pull it off. This thought about failure held true for a time as Hot Wheels as a brand was not making any money with Mattel many a time considering retiring the brand and making numerous changes to cut costs, although in retrospect, he should have stayed and continued designing as the brand began turning a profit quickly during the mid 1970s. Prior to leaving Mattel, he recommended his friend Ira Gilford for the position, which the latter accepted. After leaving Mattel, Bradley started a design firm and did work on a number of projects. He then went on to become a lecturer at the Art Central College of Design, the institute from which many future Hot Wheels designers would graduate; he would also sporadically design new cars, with one of the last cars he did around the tail end of his "active period" being his "shark fin" 1993 Infiniti J30, although his last project was apparently a Pontiac he did for a friend circa 2010. Bradley passed away on 13 May 2023, aged 86.',
        'periodo': '1966-1969',
        'nacionalidad': 'Estadounidense',
        'proyectos': ['Beatnik Bandit', 'Custom Barracuda', 'Custom Camaro', 'Custom Cougar', 'Custom Corvette', 'Custom Eldorado', 'Custom Firebird', 'Custom Fleetside', 'Custom Mustang', 'Custom T-Bird', 'Custom Volkswagen', 'Deora', 'Ford J-Car', 'Hot Heap', 'Python', 'Silhouette', 'Oscar Mayer Wienermobile'],
    },
    'Paul Tam': {
        'foto': 'https://static.wikia.nocookie.net/hotwheels/images/a/a0/Paul_Tam_Header.jpg/revision/latest/scale-to-width-down/300',
        'bio': 'Paul Tam\'s lifelong dream was to design cars for General Motors. He realized that dream in the 1960\'s, though it was short-lived. In 1970, he then drove to California, to the offices of Mattel - makers of Hot Wheels - and said, "I want a job." "Just like that," Paul says. "Brash." But it worked. Paul joined with Larry Wood and Ira Gilford at Mattel in the early days of Hot Wheels cars to work as a designer and started designing some of the company\'s signature cars. Among them the Whip Creamer, a turbine car, which was his very first design for Hot Wheels. The turbine in the back was a blue-sky idea of a power source that could harness the sun\'s energy and drive the vehicle. To make the wheel spin, an opening was designed so that a kid could spin the turbine by blowing on it. The Whip Creamer was a playful and whimsical name suggested for it. Each car had to have a feature; the turbine which actually spun and you could see it, was the feature, hence the clear roof which extended all the way to the back. Tam continued to work for Mattel until 1973. Among the many futuristic designs Tam thought up for Mattel include some of the collector\'s favorites such as Evil Weevil, Open Fire, Six Shooter and the rare Double Header (co-designed with Larry Wood.) Talking about the Beach Bomb, he says, "I remember proposing another bus for the beach crowd with paisley all over it. They were rejected and discarded literally into the trash can... Someone\'s trash is the next man\'s treasure." Paul brought home prototypes, some of them with clear, unpainted bodies, so father and son, Alec, could "test drive" them together. By 1975, however, when Alec was 5, the family moved back to Paul\'s native South Africa, where father and son started to bond over bigger cars. They settled in Cradock, a small town 150 miles north of Port Elizabeth, where they ran a motorcycle repair shop. At 63, today Paul Tam runs a financing business, TAMI FIN, in his native South Africa. He continues to make public appearances at conventions, such as the one that celebrated the 40th Anniversary of Hot Wheels, and which took place in Chicago, Illinois, in May 2008. He also has a son called Alec Tam who now works for the Hot Wheels company himself.',
        'periodo': '1970-1973',
        'nacionalidad': 'Sudafricano',
        'proyectos': ['Whip Creamer', 'AMX/2', 'Evil Weevil', 'Hairy Hauler', 'Six Shooter', 'Ferrari 512S', 'Open Fire', 'Double Header'],
    },
    'Howard Rees': {
        'foto': 'https://static.wikia.nocookie.net/hotwheels/images/e/ef/Howard_Rees_Header.jpg/revision/latest/scale-to-width-down/300',
        'bio': 'Howard K. Rees is a former Hot Wheels designer who worked at Mattel from 1969 to 1975. Prior to his work at Mattel, he accepted a position at Ford of Europe. Rees left the Hot Wheels design team in 1971 to design the Major Matt Mason action figures, recommending a friend of his named Larry Wood to the position. Rees left Mattel entirely in 1975 and became a painter, which he still is to this day.',
        'periodo': '1969-1975',
        'nacionalidad': 'Estadounidense',
        'proyectos': ['Jack Rabbit Special', 'Mighty Maverick', 'Mod Quad', 'Paddy Wagon', 'Peeping Bomb', 'Red Baron', 'Sand Crab', 'Seasider', 'The Demon', 'Cockney Cab', 'Crew Car', 'Noodle Head', 'Short Order'],
    },
    'Jun Imai': {
        'foto': 'https://static.wikia.nocookie.net/hotwheels/images/b/b3/Junwiki.jpg/revision/latest/scale-to-width-down/300',
        'bio': 'Jun Imai is a Japanese-American former Hot Wheels designer who worked at Mattel from 2004 to 2018. Although his designs include classic American muscle cars and fantasy cars, he is most known for his Japanese cars. He has made replicas of his own 1:1 vehicles; the \'71 Datsun Bluebird 510 Wagon, the Nissan Fairlady Z and the Datsun 620. He left Mattel in 2018; he currently acts as the creative director of Kaido House, a company he founded selling automotive enthusiast merchandise and later morphing into a line of highly-detailed diecast cars manufactured in collaboration with TrueScale Miniatures and marketed as a subline to their Mini GT product line. His Kaido House brand also appeared on various Hot Wheels cars and he maintains a good relationship with his ex-colleagues.',
        'periodo': '2004-2018',
        'nacionalidad': 'Japonés-Americano',
        'proyectos': ['Rocket Box', 'Symbolic', 'Subaru Impreza WRX', 'Chicane', 'Covelight', 'High Voltage', 'RD-05', 'RD-08', '\'07 Cadillac Escalade', 'Chrysler Firepower Concept', 'Corvette C6R', 'Med-Evil', 'Dieselboy', 'Nissan Titan', 'Nerve Hammer', 'Toyota AE-86 Corolla', '\'64 Lincoln Continental', '\'69 Ford Mustang', '\'70 Pontiac Firebird', 'Buick Grand National', 'Nitro Doorslammer', '\'70 Pontiac GTO', 'Bad Mudder 2', 'Custom \'77 Dodge Van', 'Dragtor', 'HW40', '\'67 Shelby GT-500', '\'68 Olds 442', '\'70 Plymouth Roadrunner', '\'70 Ford Torino', '\'70 Nova', '\'77 Pontiac Firebird T/A', '\'80 El Camino', '\'83 Chevy Silverado', '\'92 Ford Mustang', '\'07 Ford Mustang', '3 Roses', 'Delila Street Car', 'Gray Ghost', 'GRX', 'Kellie "Gearbox" Kalinkov', 'Mach 4', 'Mach 5', 'Mach 6', 'Musha Motors Race Car', 'Prince Kabala Race Car', 'Racer X Race Car', 'Racer X Street Car', 'Snake Oiler Race Car', 'Snake Oiler Street Car', 'Sonic "Boom Boom" Renaldi', 'Taejo Togokhan Street Car', 'Thor-Axine Street Car', 'Circle Tracker', 'Brit Speed', 'Ferrari 250 GTO', '\'70 Buick GSX', 'AMC Javelin AMX', 'Volkswagen Type 181', 'Avant Garde', 'Barbaric', 'Datsun Bluebird 510', 'Bread Box', 'Dodge Charger Drift Car', 'Mazda Furai', 'Sandblaster', 'Salt Shaker', '\'10 Pro Stock Camaro', 'Tyrrell P34', 'Sting Rod II', '\'86 Monte Carlo SS', 'Toyota Land Cruiser FJ40', '\'66 Dodge A100', 'Buzzkill', 'Hamm on Wheels', 'Lotso Speed', 'Speedin\' Stretch', 'Turbo Chunk', 'Woody Wagon', 'Danicar', '\'70 Pontiac GTO Judge', 'Nissan Skyline 2000GT-R', 'Nissan Skyline H/T 2000 GT-X', '\'10 Chevy Impala', 'Circle Trucker', 'Street Shaker', '\'51 GMC C.O.E.', 'Haulin\' Gas', 'Cargo Cruiser', 'Diesel Chief', '\'65 Ford Galaxie', '\'66 Chevelle', '\'70 Ford Mustang Boss 302', '\'71 AMC Javelin', 'Bullseye MHP', 'Dasch N\' Dog', 'Jammin\' Jessie', 'Land Speed Lenny', 'Rocky Road', 'R.C. To Go', 'Zurg GT', 'Troy Soldier', '\'12 Ford Mustang Boss 302 Laguna Seca', '2013 SRT Viper', 'Mars Rover Curiosity', 'Quicksand', 'BMW 2002', '\'12 Corvette Z06', 'Mazda RX-7', '\'10 Toyota Tundra', 'Indy 500 Oval', 'Mad Manga', 'Custom \'12 Ford Mustang', '\'84 Mustang SVO', '1987 Toyota Pickup Truck', '\'78 Ford Mustang II', 'Porsche 914-6', '\'69 Ford Mustang Boss 302', '\'76 Greenwood Corvette', '\'78 Porsche 935-78', '\'92 BMW M3', '\'67 Austin Mini Van', 'Volkswagen T1 Panel Bus', 'Turbo Hauler', '\'69 Dodge Charger Daytona', '\'70 Chevy Chevelle SS', '\'70 Toyota Celica', '\'13 Ford Mustang GT', 'Bullet Proof', 'Bump Around', 'Drift Rod', 'Hot Wheels High', 'Lamborghini Aventador J', 'Max Steel Motorcycle', 'Pagani Huayra', 'Porsche 918 Spyder', 'Toyota 2000GT', 'Toyota Supra', '\'71 Datsun Bluebird 510 Wagon', '\'85 Ford Bronco', 'Porsche 993 GT2', '\'49 Ford F1', 'Clear Speeder', 'Datsun 620', 'Max Steel Turbo Racer', 'Driftsta', 'Honda Odyssey', 'Nissan Fairlady Z', 'Skate Brigade', 'Vision', 'Boba Fett\'s Slave I', '\'95 Mazda RX-7', 'Aisle Driver', 'Custom Datsun 240Z', 'Fairlady 2000', 'Mazda REPU', 'Porsche 934.5', 'Time Shifter', 'Volkswagen T2 Pickup', 'Daffy Duck', '\'71 Porsche 911', 'Custom Ford Maverick', 'HW50 Concept', 'Track Manga', '\'69 Nissan Skyline Van', 'Nissan Laurel 2000 SGX', 'Nissan Skyline GT-R (BNR32)', 'Roborace Robocar', 'RWB Porsche 930', 'Nissan Skyline Silhouette'],
    },
    'Tyler Charest': {
        'foto': 'https://static.wikia.nocookie.net/hotwheels/images/0/0c/TylerCharest.jpg/revision/latest/scale-to-width-down/300',
        'bio': 'Tyler J. Charest is a Hot Wheels designer who has worked at Mattel since 2015, where he currently serves as a lead designer; he was a Hot Wheels designer from 2015 to 2020. Prior to his work at Mattel, he developed concepts for Toyota Boshoku America and worked as an industrial designer; he also interned at Mattel for three months as an "innovation design intern" in 2014 before joining Mattel full-time. He currently works as associate manager of the Matchbox design team.',
        'periodo': '2015-presente',
        'nacionalidad': 'Estadounidense',
        'proyectos': ['Red Skull', 'Ant-Man', 'Tour de Fast', 'Turbot', 'Doc Ock', 'Doctor Strange', 'Green Arrow', 'The Joker GT', 'The Riddler', 'Boom Car', 'Quad Rod', 'Solid Muscle', 'Speedy Pérez', 'Turbo Rooster', 'Aquaman', 'Doomsday', 'Elektra', 'Elite Praetorian Guard', 'Iron Fist', 'Luke Skywalker', 'Nebula', 'Rose', 'Supergirl', 'Tasmanian Devil', 'Valkyrie', 'Alien Invasion', 'Gas Monkey Garage', 'Megalodon', 'Dune Daddy', 'Chewbacca', 'Hulkbuster 2.0', 'Iron Man Mark 50', 'Maleficent', 'Mosasaurus', 'Qi\'ra', 'Starfire', 'Triceratops', 'Hot Wheels', 'Hot Wheels Racing #1', 'Podium Crasher', 'Psycho-Delic', 'Alpine A110', 'Moto Wing', 'Muscle Bound', 'Aquaman', 'Batman', 'Bo Peep', 'Captain America', 'Chewbacca', 'D-O', 'Darth Vader', 'Deathstroke', 'Donald Duck', 'Dory', 'Duke Caboom', 'Forky', 'Gambit', 'Harley Quinn', 'Jedi Luke Skywalker', 'Mera', 'Mouse Droid', 'Shazam', 'Spider-Gwen', 'Spider-Man', 'Stormtrooper', 'Superman', 'The Joker GT', 'The Mandalorian', 'Thor', 'War Machine', 'Wolverine', 'Wonder Woman', 'Baja Buster', 'Finn Bálor', 'Hooligan', 'Sasha Banks', 'Wild Streak', 'Captain Hook', 'Cheshire Cat', 'Donatello', 'Heavy Infantry Mandalorian', 'Michelangelo', 'Mulan', 'Raphael', 'Reaper', 'Ryu', 'Taskmaster', 'The Cheetah', 'HWSF Tactical Unit', 'Luigi', '\'17 Nissan GT-R (R35)', 'Cybertruck', 'Rodger Dodger', 'Water Bomber', 'Keroppi', 'Teela', 'Bigfoot', 'Gunkster', 'Race Ace', 'Velociraptor \'Blue\'', '2020 Chevrolet Corvette C8', 'Tesla Roadster', 'The Batmobile RC', 'GMC Hummer EV', 'Porsche 911 GT3', 'Mailed It!', 'Lamborghini Revuelto', 'Nissan Z', 'Ferrari SF90 Stradale Assetto Fiorano', 'Ford Mustang GTD', 'Nissan Skyline GT-R (R32) Pandem', 'PT Fast', 'Crashing Canine', 'Aston Martin Vantage', 'Dodge Viper ACR', 'Ferrari F1-89', 'Ferrari F1-2000', 'Lamborghini Temerario Alleggerita', '1999 Honda Civic Type R'],
    },
    'Ryu Asada': {
        'foto': 'https://static.wikia.nocookie.net/hotwheels/images/0/0c/RyuAsada.jpg/revision/latest/scale-to-width-down/300',
        'bio': 'Ryu Asada was a Japanese Hot Wheels designer who worked at Mattel from 2004 to 2021 and oversaw the design of cars in the basic $1 mainline lineup as a Designer Project Lead, taking over from Jun Imai. Born in Osaka, he pursued a degree at the Art Center College of Design after emigrating to the United States. After graduating, he initially began work as a designer for Matchbox from 2004 to 2012; he first designed for Hot Wheels in 2009 as a "guest designer", and would join the Hot Wheels design team three years later. He passed away on 23 March 2021 at the age of 42 from cancer. A mini-segment of the 2022 mainline, dubbed Ryu\'s Rides, as well as the Ryu Asada Award for the 2021 Hot Wheels Legends Tour, were both created to celebrate his life and to honor his legacy.',
        'periodo': '2004-2021',
        'nacionalidad': 'Japonés',
        'proyectos': ['Gearonimo', 'Formula Street', 'Honda S2000', 'Rennen Rig', 'Super Blitzen', 'Bucket O\' Speed', 'Bentley Continental Supersports', 'Baja Truck', '1985 Honda CR-X', '\'67 Chevy C10', '\'12 Acura NSX Concept', '\'14 Corvette Stingray', 'Scion FR-S', 'Speedbox', 'Speed Dozer', 'BMW K 1300 R', '\'90 Honda Civic EF', '\'14 Corvette Stingray Convertible', '2015 Ford Mustang GT', 'Ducati 1199 Panigale', 'Hi-Tech Missile', 'Mastretta MXR', 'MR11', 'Porsche 934 Turbo RSR', 'Porsche Panamera', 'Project Speeder', 'Rig Storm', 'Ryura LX', '\'90 Acura NSX', '\'15 Jaguar F-Type Project 7', 'Aston Martin Vantage GT3', 'Backdrafter', 'Batman: Arkham Knight Batmobile', 'BMW M4', 'Corvette C7.R', 'Custom \'15 Ford Mustang', 'GT Hunter', 'Hover Storm', 'Lotus Esprit S1', 'McLaren P1', 'Nitro Tailgater', 'Ollie Rocket', 'Pedal Driver', 'SRT Viper GTS-R', 'Super Volt', 'Tesla Model S', 'The Haulinator', '\'63 Chevy II', '\'15 Mazda MX-5 Miata', '\'17 Acura NSX', '\'17 Ford F-150 Raptor', 'Blade Raider', 'Blitzspeeder', 'Bone Speeder', 'Crate Racer', 'Custom \'72 Chevy LUV', 'Custom \'01 Acura Integra GSR', 'Dawgzilla', 'Grass Chomper', 'Honda Monkey Z50', 'HW Formula Solar', 'Renault Sport R.S. 01', 'Tanknator', '\'68 Corvette - Gas Monkey Garage', 'Jawa', 'Mario', '\'15 Mercedes-AMG GT', '\'16 Honda Civic Type R', '2016 Ford GT Race', '\'17 Nissan GT-R (R35)', '\'17 Pagani Huayra Roadster', 'Baja Hauler', 'Gazella R', 'Head Starter', 'Milano', 'Porsche 934.5', 'Roller Toaster', 'Sky Dome', 'Street Wiener', 'Tesla Model X', 'Track Hammer', 'Cyborg', 'Loki', '\'71 Porsche 911', '\'85 Honda City Turbo II', '\'16 Cadillac ATS-V R', '2016 BMW M2', '\'17 Audi RS 6 Avant', 'Airuption', 'Bogzilla', 'Bubble Matic', 'Buns of Steel', 'Corvette C7 Z06 Convertible', 'Cyber Speeder', 'Lamborghini Countach Pace Car', 'McLaren 720S', 'Nissan Skyline GT-R (BCNR33)', 'Nissan Skyline RS (KDR30)', 'Porsche 918 Spyder', 'Quick Bite', 'Rising Heat', 'Skull Shaker', '\'88 Honda CR-X', '\'91 Mazda MX-5 Miata', '\'96 Porsche Carrera', '\'16 Bugatti Chiron', '\'16 Lamborghini Centenario Roadster', '2018 Honda Civic Type R', '\'19 Mercedes-Benz A-Class', 'Audi RS 5 Coupé', 'Aston Martin Vulcan', 'Chrysler Pacifica', 'Custom \'18 Ford Mustang GT', 'Heavy Hitcher', 'Jaguar XE SV Project 8', 'McLaren Senna', 'Slide Kick', 'Rodger Dodger 2.0', 'Runway Res-Q', 'Tesla Model 3', '\'70 Volkswagen Baja Bug', '\'89 Mazda Savanna RX-7 FC3S', '\'89 Porsche 944 Turbo', '\'98 Honda Prelude', '\'98 Subaru Impreza 22B STi-Version', '\'99 Ford F-150 SVT Lightning', '\'17 Lamborghini Urus', '2018 Bentley Continental GT3', '2019 Audi R8 Spyder', '\'19 Corvette ZR1 Convertible', '2020 Koenigsegg Jesko', '\'20 Jeep Gladiator', '2020 Ram 1500 Rebel', 'Astana Hotto', 'Duck N\' Roll', 'Formula E Gen 2 Car', 'Manga Tuner', 'Mattel Dream Mobile', 'McLaren Speedtail', 'Pixel Shaker', 'Speed Driver', 'Total Disposal', 'Veloci-Racer', 'Volvo 850 Estate', 'Hyperfin', 'Honda Civic EG', '2003 Honda NSX Type-R', '\'67 Ford GT40 Mk.IV', '\'94 Audi Avant RS2', '\'94 Bugatti EB110 SS', '\'99 Honda Civic Type R (EK9)', '2020 Jaguar F-Type', '\'20 Toyota GR Supra', 'Ain\'t Fare', 'Car-de-Asada', 'Corvette C8.R', 'Custom \'70 Honda N600', 'Dodge Van', 'Draftnator', 'GT-Scorcher', 'Lancia Delta Integrale', 'LB-Silhouette WORKS GT Nissan 35GT-RR VER.2', 'LB-WORKS Lamborghini Huracán Coupé', 'Lethal Diesel', 'McLaren F1', 'Mercedes-Benz 500 E', 'Nissan R390 GT1', 'Porsche 935', 'Raijin Express', 'Sand Burner', 'Tooned Twin Mill', 'Toyota Land Cruiser', 'Ion Motors Thresher', '\'87 Ford Sierra Cosworth', '\'20 Toyota Tacoma', 'Classic TV Series Batmobile', 'Ford Mustang Mach-E 1400', 'Mighty K', 'Nissan Skyline 2000GT-R LBWK', 'Sweet Driver', 'Toon\'d \'83 Chevy Silverado', 'Tooned Volkswagen Golf Mk1', 'LB Super Silhouette Nissan Silvia (S15)'],
    },
    'Abe Lugo': {
        'foto': 'https://static.wikia.nocookie.net/hotwheels/images/0/0c/AbeLugo.jpg/revision/latest/scale-to-width-down/300',
        'bio': 'Abraham Lugo is a former Hot Wheels and Matchbox designer who has been with Mattel from 2008 to 2025. Prior to joining Mattel, he was a designer at Jakks Pacific. Lugo was part of the Hot Wheels design team from 2008 through 2011 and subsequently joined the Matchbox design team; he departed the company in 2025.',
        'periodo': '2008-2025',
        'nacionalidad': 'Estadounidense',
        'proyectos': ['Honda Odyssey', 'Nissan Fairlady Z', 'Skate Brigade', 'Vision', 'Boba Fett\'s Slave I', 'Alpine A110', 'Moto Wing', 'Muscle Bound', 'Aquaman', 'Batman', 'Bo Peep', 'Captain America', 'Chewbacca', 'D-O', 'Darth Vader', 'Deathstroke', 'Donald Duck', 'Dory', 'Duke Caboom', 'Forky', 'Gambit', 'Harley Quinn', 'Jedi Luke Skywalker', 'Mera', 'Mouse Droid', 'Shazam', 'Spider-Gwen', 'Spider-Man', 'Stormtrooper', 'Superman', 'The Joker GT', 'The Mandalorian', 'Thor', 'War Machine', 'Wolverine', 'Wonder Woman', 'Baja Buster', 'Finn Bálor', 'Hooligan', 'Sasha Banks', 'Captain Hook', 'Cheshire Cat', 'Donatello', 'Heavy Infantry Mandalorian', 'Michelangelo', 'Mulan', 'Raphael', 'Reaper', 'Ryu', 'Taskmaster', 'The Cheetah', 'HWSF Tactical Unit', 'Luigi', '\'17 Nissan GT-R (R35)', 'Cybertruck', 'Rodger Dodger', 'Water Bomber', 'Keroppi', 'Teela', 'Bigfoot', 'Gunkster', 'Race Ace', 'Velociraptor \'Blue\'', '2020 Chevrolet Corvette C8', 'Tesla Roadster', 'The Batmobile RC', 'GMC Hummer EV', 'Porsche 911 GT3', 'Mailed It!', 'Lamborghini Revuelto', 'Nissan Z', 'Ferrari SF90 Stradale Assetto Fiorano', 'Ford Mustang GTD', 'Nissan Skyline GT-R (R32) Pandem', 'PT Fast', 'Crashing Canine', 'Aston Martin Vantage', 'Dodge Viper ACR', 'Ferrari F1-89', 'Ferrari F1-2000', 'Lamborghini Temerario Alleggerita', '1999 Honda Civic Type R'],
    },
    'Larry Wood': {
        'foto': 'https://static.wikia.nocookie.net/hotwheels/images/0/0c/LarryWood.jpg/revision/latest/scale-to-width-down/300',
        'bio': 'Larry Wood is a former Hot Wheels designer who worked at Mattel from 1970 to 2004. He is one of the most prolific Hot Wheels designers, with over 200 designs to his name. He is best known for designing the Snake and Mongoose dragsters, as well as the Bye-Focal and Tri Baby.',
        'periodo': '1970-2004',
        'nacionalidad': 'Estadounidense',
        'proyectos': ['Tri Baby', 'Jack Rabbit Special', 'Mongoose', 'Snake', 'Bye-Focal'],
    },
}

# Tool numbers extraídos de las páginas de diseñadores (Fandom)
TOOL_NUMBERS = {
    # Ira Gilford (1968-2008) - 50 modelos
    '6220': 'Ira Gilford', '6264': 'Ira Gilford', '6256': 'Ira Gilford',
    '6251': 'Ira Gilford', '6250': 'Ira Gilford', '6253': 'Ira Gilford',
    '6252': 'Ira Gilford', '6267': 'Ira Gilford', '6268': 'Ira Gilford',
    '6266': 'Ira Gilford', '6269': 'Ira Gilford', '6257': 'Ira Gilford',
    '6263': 'Ira Gilford', '6254': 'Ira Gilford', '6262': 'Ira Gilford',
    '6277': 'Ira Gilford', '6255': 'Ira Gilford', '6275': 'Ira Gilford',
    '6276': 'Ira Gilford', '6265': 'Ira Gilford', '6261': 'Ira Gilford',
    '6260': 'Ira Gilford', '6259': 'Ira Gilford', '6258': 'Ira Gilford',
    '6274': 'Ira Gilford', '6451': 'Ira Gilford', '6420': 'Ira Gilford',
    '6452': 'Ira Gilford', '6404': 'Ira Gilford', '6453': 'Ira Gilford',
    '6417': 'Ira Gilford', '6454': 'Ira Gilford', '6408': 'Ira Gilford',
    '6190': 'Ira Gilford', '6412': 'Ira Gilford', '6423': 'Ira Gilford',
    '6455': 'Ira Gilford', '6405': 'Ira Gilford', '6416': 'Ira Gilford',
    '6459': 'Ira Gilford', '6422': 'Ira Gilford', '6407': 'Ira Gilford',
    '6450': 'Ira Gilford', '6499': 'Ira Gilford', '6018': 'Ira Gilford',
    '6194': 'Ira Gilford', '6193': 'Ira Gilford', '6020': 'Ira Gilford',
    '6418': 'Ira Gilford', '6019': 'Ira Gilford', '6192': 'Ira Gilford',
    'C2732': 'Ira Gilford', 'L3530': 'Ira Gilford', 'K3373': 'Ira Gilford',
    'L2096': 'Ira Gilford', 'L8704': 'Ira Gilford',
    
    # Harry Bradley (1968) - 16 modelos (Sweet 16)
    '6217': 'Harry Bradley', '6211': 'Harry Bradley', '6208': 'Harry Bradley',
    '6205': 'Harry Bradley', '6215': 'Harry Bradley', '6218': 'Harry Bradley',
    '6212': 'Harry Bradley', '6213': 'Harry Bradley', '6206': 'Harry Bradley',
    '6207': 'Harry Bradley', '6220': 'Harry Bradley', '6210': 'Harry Bradley',
    '6214': 'Harry Bradley', '6219': 'Harry Bradley', '6216': 'Harry Bradley',
    '6209': 'Harry Bradley', '3029': 'Harry Bradley',
    
    # Howard Rees (1970-1971) - 12 modelos
    '6421': 'Howard Rees', '6414': 'Howard Rees', '6456': 'Howard Rees',
    '6402': 'Howard Rees', '6403': 'Howard Rees', '6419': 'Howard Rees',
    '6400': 'Howard Rees', '6413': 'Howard Rees', '6401': 'Howard Rees',
    '6466': 'Howard Rees', '6183': 'Howard Rees', '6000': 'Howard Rees',
    '6176': 'Howard Rees',
    
    # Paul Tam (1970-1973) - 8 modelos
    '6457': 'Paul Tam', '6460': 'Paul Tam', '6471': 'Paul Tam',
    '6458': 'Paul Tam', '6003': 'Paul Tam', '6021': 'Paul Tam',
    '5881': 'Paul Tam', '5880': 'Paul Tam',
    
    # Larry Wood (1970-1971) - 5 modelos
    '6424': 'Larry Wood', '6410': 'Larry Wood', '6409': 'Larry Wood',
    '6187': 'Larry Wood',
    
    # Jun Imai (2005-2018) - 100+ modelos
    'G6073': 'Jun Imai', 'G6716': 'Jun Imai', 'G6707': 'Jun Imai',
    'G8091': 'Jun Imai', 'G8120': 'Jun Imai', 'G8089': 'Jun Imai',
    'G8111': 'Jun Imai', 'G8114': 'Jun Imai', 'J3275': 'Jun Imai',
    'J3255': 'Jun Imai', 'J3266': 'Jun Imai', 'J3271': 'Jun Imai',
    'J3273': 'Jun Imai', 'J3272': 'Jun Imai', 'J3252': 'Jun Imai',
    'J3243': 'Jun Imai', 'K6158': 'Jun Imai', 'K6136': 'Jun Imai',
    'K6148': 'Jun Imai', 'K6142': 'Jun Imai', 'K6135': 'Jun Imai',
    'L9944': 'Jun Imai', 'L9935': 'Jun Imai', 'L9922': 'Jun Imai',
    'L9921': 'Jun Imai', 'M3315': 'Jun Imai', 'M0519': 'Jun Imai',
    'M0520': 'Jun Imai', 'M0518': 'Jun Imai', 'M0429': 'Jun Imai',
    'M0428': 'Jun Imai', 'M0513': 'Jun Imai', 'M0517': 'Jun Imai',
    'M0514': 'Jun Imai', 'M0512': 'Jun Imai', 'M0516': 'Jun Imai',
    'N2797': 'Jun Imai', 'M5933': 'Jun Imai', 'M5924': 'Jun Imai',
    'M5921': 'Jun Imai', 'N3259': 'Jun Imai', 'M5920': 'Jun Imai',
    'M5916': 'Jun Imai', 'M5922': 'Jun Imai', 'M5927': 'Jun Imai',
    'M5932': 'Jun Imai', 'M5925': 'Jun Imai', 'M5919': 'Jun Imai',
    'M5918': 'Jun Imai', 'M5931': 'Jun Imai', 'N3258': 'Jun Imai',
    'M5928': 'Jun Imai', 'M5938': 'Jun Imai',
    'R0929': 'Jun Imai', 'R6457': 'Jun Imai', 'R0946': 'Jun Imai',
    'R0945': 'Jun Imai', 'R0951': 'Jun Imai', 'R6450': 'Jun Imai',
    'R6451': 'Jun Imai', 'R0938': 'Jun Imai', 'R6455': 'Jun Imai',
    'R6454': 'Jun Imai', 'R3754': 'Jun Imai', 'R1185': 'Jun Imai',
    'P4830': 'Jun Imai', 'R2518': 'Jun Imai', 'R2519': 'Jun Imai',
    'R2520': 'Jun Imai', 'W4480': 'Jun Imai',
    'T9671': 'Jun Imai', 'T9681': 'Jun Imai', 'X0092': 'Jun Imai',
    'T9703': 'Jun Imai', 'T9707': 'Jun Imai', 'T9716': 'Jun Imai',
    'T9719': 'Jun Imai', 'V5254': 'Jun Imai', 'V5256': 'Jun Imai',
    'V0149': 'Jun Imai', 'V0141': 'Jun Imai', 'T8467': 'Jun Imai',
    'T8536': 'Jun Imai', 'T8451': 'Jun Imai', 'T8456': 'Jun Imai',
    'T8547': 'Jun Imai', 'T8548': 'Jun Imai', 'T8554': 'Jun Imai',
    'T8551': 'Jun Imai', 'T8552': 'Jun Imai', 'T8550': 'Jun Imai',
    'T8553': 'Jun Imai', 'V5289': 'Jun Imai', 'V5296': 'Jun Imai',
    'V5299': 'Jun Imai', 'Y4712': 'Jun Imai', 'V5307': 'Jun Imai',
    'V5309': 'Jun Imai', 'V5311': 'Jun Imai', 'V5319': 'Jun Imai',
    'V5328': 'Jun Imai', 'V5330': 'Jun Imai', 'V5332': 'Jun Imai',
    'X0135': 'Jun Imai', 'W3777': 'Jun Imai', 'W3774': 'Jun Imai',
    'W4594': 'Jun Imai', 'W4622': 'Jun Imai', 'W8313': 'Jun Imai',
    'W8304': 'Jun Imai', 'W8302': 'Jun Imai', 'W8303': 'Jun Imai',
    'W6636': 'Jun Imai', 'W6635': 'Jun Imai', 'W4416': 'Jun Imai',
    
    # Tyler Charest (2015-2027) - 50+ modelos
    'CGD55': 'Tyler Charest', 'CGD61': 'Tyler Charest',
    'DHP35': 'Tyler Charest', 'DHP31': 'Tyler Charest', 'DJJ49': 'Tyler Charest',
    'DJJ48': 'Tyler Charest', 'DJM21': 'Tyler Charest', 'DTJ61': 'Tyler Charest',
    'DJP11': 'Tyler Charest', 'DTX11': 'Tyler Charest', 'DTX28': 'Tyler Charest',
    'DTX17': 'Tyler Charest', 'DTW98': 'Tyler Charest', 'DTX23': 'Tyler Charest',
    'DXM53': 'Tyler Charest', 'DXM57': 'Tyler Charest', 'DXM04': 'Tyler Charest',
    'FDJ72': 'Tyler Charest', 'DXM11': 'Tyler Charest', 'FDK38': 'Tyler Charest',
    'DXM07': 'Tyler Charest', 'FLG50': 'Tyler Charest', 'DXN52': 'Tyler Charest',
    'DXT11': 'Tyler Charest', 'FLG61': 'Tyler Charest', 'FLG51': 'Tyler Charest',
    'FLH51': 'Tyler Charest', 'FLJ07': 'Tyler Charest', 'FLJ79': 'Tyler Charest',
    'FLJ13': 'Tyler Charest', 'FLJ05': 'Tyler Charest', 'FLW79': 'Tyler Charest',
    'FYJ54': 'Tyler Charest', 'FYK11': 'Tyler Charest', 'FYJ59': 'Tyler Charest',
    'GGX61': 'Tyler Charest', 'GGX64': 'Tyler Charest', 'GJJ04': 'Tyler Charest',
    'GJJ97': 'Tyler Charest', 'GGX68': 'Tyler Charest', 'GJJ05': 'Tyler Charest',
    'GJJ06': 'Tyler Charest', 'GJJ27': 'Tyler Charest', 'GJJ30': 'Tyler Charest',
    'GJH93': 'Tyler Charest', 'FYV64': 'Tyler Charest', 'GJF13': 'Tyler Charest',
    'GKD17': 'Tyler Charest', 'GWB72': 'Tyler Charest', 'GXG30': 'Tyler Charest',
    'GWB73': 'Tyler Charest', 'GRX48': 'Tyler Charest', 'GRM64': 'Tyler Charest',
    'GRM25': 'Tyler Charest', 'GTK55': 'Tyler Charest', 'HCB57': 'Tyler Charest',
    'GTH79': 'Tyler Charest', 'GTP58': 'Tyler Charest', 'HBL42': 'Tyler Charest',
    'HJP78': 'Tyler Charest', 'HBL43': 'Tyler Charest', 'HLT19': 'Tyler Charest',
    'HLT20': 'Tyler Charest', 'HRY82': 'Tyler Charest', 'HWW55': 'Tyler Charest',
    'HTP16': 'Tyler Charest', 'JGD09': 'Tyler Charest', 'JBH04': 'Tyler Charest',
    'JGD10': 'Tyler Charest', 'JJH59': 'Tyler Charest', 'JHY68': 'Tyler Charest',
    'JHW59': 'Tyler Charest', 'JMM78': 'Tyler Charest', 'JNB88': 'Tyler Charest',
    'JHW60': 'Tyler Charest', 'JJY56': 'Tyler Charest',
    
    # Ryu Asada (2009-2021) - 50+ modelos
    'N4039': 'Ryu Asada', 'R0937': 'Ryu Asada', 'T9690': 'Ryu Asada',
    'T9689': 'Ryu Asada', 'T9687': 'Ryu Asada', 'T8549': 'Ryu Asada',
    'V5324': 'Ryu Asada', 'X0139': 'Ryu Asada', 'W3776': 'Ryu Asada',
    'X1637': 'Ryu Asada', 'X1640': 'Ryu Asada', 'X1620': 'Ryu Asada',
    'X1627': 'Ryu Asada', 'X1653': 'Ryu Asada', 'BJF58': 'Ryu Asada',
    'BFD13': 'Ryu Asada', 'BDC77': 'Ryu Asada', 'BDD19': 'Ryu Asada',
    'BDD18': 'Ryu Asada', 'BDC78': 'Ryu Asada', 'BDD10': 'Ryu Asada',
    'CFH17': 'Ryu Asada', 'BDC82': 'Ryu Asada', 'BDD16': 'Ryu Asada',
    'BDD09': 'Ryu Asada', 'BDD20': 'Ryu Asada', 'CFH16': 'Ryu Asada',
    'CFH06': 'Ryu Asada', 'CFH15': 'Ryu Asada', 'CFG75': 'Ryu Asada',
    'CFG82': 'Ryu Asada', 'CFH07': 'Ryu Asada', 'CFH01': 'Ryu Asada',
    'CFH00': 'Ryu Asada', 'CFG96': 'Ryu Asada', 'CFG91': 'Ryu Asada',
    'CFG74': 'Ryu Asada', 'CFH20': 'Ryu Asada', 'CFG77': 'Ryu Asada',
    'DHN92': 'Ryu Asada', 'CFG87': 'Ryu Asada', 'CFG99': 'Ryu Asada',
    'CFH08': 'Ryu Asada', 'CFH03': 'Ryu Asada', 'CFG89': 'Ryu Asada',
    'DHP13': 'Ryu Asada', 'DHP05': 'Ryu Asada', 'DHN99': 'Ryu Asada',
    'DHP19': 'Ryu Asada', 'DHN94': 'Ryu Asada', 'DHN91': 'Ryu Asada',
    'DHN87': 'Ryu Asada', 'DHP24': 'Ryu Asada', 'DHP17': 'Ryu Asada',
    'DHP06': 'Ryu Asada', 'DHP18': 'Ryu Asada', 'DHP25': 'Ryu Asada',
    'DHP16': 'Ryu Asada', 'DHP36': 'Ryu Asada', 'DHP01': 'Ryu Asada',
    'DHP21': 'Ryu Asada', 'DHN90': 'Ryu Asada', 'DJL64': 'Ryu Asada',
    'DMH74': 'Ryu Asada', 'DTW84': 'Ryu Asada', 'DTW88': 'Ryu Asada',
    'DTW92': 'Ryu Asada', 'DTW99': 'Ryu Asada', 'DTW86': 'Ryu Asada',
    'DTX12': 'Ryu Asada', 'FJV99': 'Ryu Asada', 'DTX05': 'Ryu Asada',
    'DTX03': 'Ryu Asada', 'DTW87': 'Ryu Asada', 'DTX14': 'Ryu Asada',
    'DTX07': 'Ryu Asada', 'DTX19': 'Ryu Asada', 'DTX01': 'Ryu Asada',
    'DTX06': 'Ryu Asada', 'DXM55': 'Ryu Asada', 'DXM12': 'Ryu Asada',
    'FJV41': 'Ryu Asada', 'FJV43': 'Ryu Asada', 'FJV57': 'Ryu Asada',
    'FJV53': 'Ryu Asada', 'FJW00': 'Ryu Asada', 'FJV77': 'Ryu Asada',
    'FJV61': 'Ryu Asada', 'FJV75': 'Ryu Asada', 'FJV59': 'Ryu Asada',
    'FJV40': 'Ryu Asada', 'FJV64': 'Ryu Asada', 'FJV79': 'Ryu Asada',
    'DTW83': 'Ryu Asada', 'FJV51': 'Ryu Asada', 'FJV44': 'Ryu Asada',
    'FPT66': 'Ryu Asada', 'FJX81': 'Ryu Asada', 'FJV55': 'Ryu Asada',
    'FJV73': 'Ryu Asada', 'FYB70': 'Ryu Asada', 'FYB66': 'Ryu Asada',
    'FYB71': 'Ryu Asada', 'GHB57': 'Ryu Asada', 'GHB56': 'Ryu Asada',
    'GHB54': 'Ryu Asada', 'GHB55': 'Ryu Asada', 'GHB42': 'Ryu Asada',
    'GHB33': 'Ryu Asada', 'GHB36': 'Ryu Asada', 'GHB29': 'Ryu Asada',
    'GHB28': 'Ryu Asada', 'GHB34': 'Ryu Asada', 'GHB39': 'Ryu Asada',
    'GHB41': 'Ryu Asada', 'GHB31': 'Ryu Asada', 'GBT71': 'Ryu Asada',
    'GBT53': 'Ryu Asada', 'GCT01': 'Ryu Asada', 'HCT21': 'Ryu Asada',
    'HCT18': 'Ryu Asada', 'HCT04': 'Ryu Asada', 'HCT06': 'Ryu Asada',
    'HCT32': 'Ryu Asada', 'HCW32': 'Ryu Asada', 'HCT40': 'Ryu Asada',
    'HCT26': 'Ryu Asada', 'HCT27': 'Ryu Asada', 'HCT23': 'Ryu Asada',
    
    # Abe Lugo (2008-2025) - 50+ modelos
    'DHP26': 'Abe Lugo', 'DHP27': 'Abe Lugo', 'DHR63': 'Abe Lugo',
    'DJJ56': 'Abe Lugo', 'DPV28': 'Abe Lugo', 'FYB39': 'Abe Lugo',
    'FYB60': 'Abe Lugo', 'FYB77': 'Abe Lugo', 'FLH33': 'Abe Lugo',
    'FYV52': 'Abe Lugo', 'GCY58': 'Abe Lugo', 'FYT97': 'Abe Lugo',
    'FYT23': 'Abe Lugo', 'FYT27': 'Abe Lugo', 'FYT18': 'Abe Lugo',
    'FYV44': 'Abe Lugo', 'FYV94': 'Abe Lugo', 'FYV90': 'Abe Lugo',
    'GCY59': 'Abe Lugo', 'GCY57': 'Abe Lugo', 'FYV27': 'Abe Lugo',
    'FYV37': 'Abe Lugo', 'FYT19': 'Abe Lugo', 'FXW57': 'Abe Lugo',
    'GJJ21': 'Abe Lugo', 'FYV50': 'Abe Lugo', 'FLG56': 'Abe Lugo',
    'FYV06': 'Abe Lugo', 'FYT99': 'Abe Lugo', 'FYV13': 'Abe Lugo',
    'FYT98': 'Abe Lugo', 'FYV36': 'Abe Lugo', 'GBT71': 'Abe Lugo',
    'GCR97': 'Abe Lugo', 'FYJ68': 'Abe Lugo', 'GCY58': 'Abe Lugo',
    'FYB47': 'Abe Lugo', 'FYB36': 'Abe Lugo', 'FYB45': 'Abe Lugo',
    'FYB41': 'Abe Lugo', 'FYB67': 'Abe Lugo', 'FYB59': 'Abe Lugo',
    'FYB40': 'Abe Lugo', 'FYB68': 'Abe Lugo', 'FYB58': 'Abe Lugo',
    'FYB50': 'Abe Lugo', 'GNN33': 'Abe Lugo', 'GJR67': 'Abe Lugo',
    'GJR80': 'Abe Lugo', 'GRT69': 'Abe Lugo', 'GRX30': 'Abe Lugo',
    'GRX27': 'Abe Lugo', 'GRX25': 'Abe Lugo', 'GRX29': 'Abe Lugo',
    'GRX20': 'Abe Lugo', 'GRX52': 'Abe Lugo', 'GRX26': 'Abe Lugo',
    'GRX31': 'Abe Lugo', 'GRX47': 'Abe Lugo', 'GRX53': 'Abe Lugo',
    'GRX51': 'Abe Lugo', 'GRX63': 'Abe Lugo', 'GRX61': 'Abe Lugo',
    'GRX57': 'Abe Lugo', 'GRX60': 'Abe Lugo', 'GRX49': 'Abe Lugo',
    'GRX55': 'Abe Lugo', 'GRX41': 'Abe Lugo', 'GRY93': 'Abe Lugo',
    'HCT23': 'Abe Lugo',
}

def limpiar_nombre(nombre):
    """Limpia nombre de modelo para coincidencia flexible."""
    nombre = nombre.strip().lower()
    nombre = re.sub(r'\[\[|\]\]', '', nombre)
    nombre = re.sub(r'\|.*', '', nombre)
    nombre = re.sub(r'\s+', ' ', nombre)
    return nombre.strip()

def main():
    # Cargar datos
    catalogo = json.load(open('data/catalog_web.json', encoding='utf-8'))
    disenadores = json.load(open('data/disenadores.json', encoding='utf-8'))
    
    print(f'Modelos: {len(catalogo)}')
    print(f'Diseñadores: {len(disenadores)}')
    
    # 1. Actualizar diseñadores con fotos, bio, periodo, nacionalidad y proyectos
    actualizados_disa = 0
    for nombre, datos in DATOS_FANDOM.items():
        if nombre in disenadores:
            disenadores[nombre].update({
                'foto': datos['foto'],
                'bio': datos['bio'],
                'periodo': datos['periodo'],
                'nacionalidad': datos['nacionalidad'],
                'proyectos': datos['proyectos'],
            })
            actualizados_disa += 1
    
    # 2. Asignar diseñadores a modelos por tool number
    asignados = 0
    for modelo in catalogo:
        tool = str(modelo.get('t', ''))
        if tool in TOOL_NUMBERS:
            disenador = TOOL_NUMBERS[tool]
            if disenador in disenadores:
                modelo['diseñador'] = disenador
                asignados += 1
    
    # Guardar
    with open('data/disenadores.json', 'w', encoding='utf-8') as f:
        json.dump(disenadores, f, ensure_ascii=False, indent=2)
    
    with open('data/catalog_web.json', 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, separators=(',', ':'))
    
    con_disenador = len([m for m in catalogo if m.get('diseñador')])
    con_foto = len([d for d in disenadores.values() if d.get('foto')])
    con_bio = len([d for d in disenadores.values() if d.get('bio')])
    con_proyectos = len([d for d in disenadores.values() if d.get('proyectos')])
    
    print(f'\n=== RESULTADOS ===')
    print(f'Diseñadores actualizados: {actualizados_disa}')
    print(f'Con foto: {con_foto}')
    print(f'Con biografía: {con_bio}')
    print(f'Con proyectos: {con_proyectos}')
    print(f'Modelos con diseñador: {con_disenador} ({con_disenador*100//len(catalogo)}%)')

if __name__ == '__main__':
    main()
