import json

base = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data/'

with open(base + 'disenadores.json', encoding='utf-8') as f:
    dis = json.load(f)

# Paul Tam
bio_pt = "Paul Tam soñó toda su vida con diseñar autos para General Motors. Hizo realidad ese sueño en los años 60, aunque duró poco. En 1970, condujo hasta California, a las oficinas de Mattel, y dijo: Quiero un trabajo. Se unió a Larry Wood e Ira Gilford en Mattel en los primeros días de Hot Wheels como diseñador y comenzó a diseñar algunos de los autos emblemáticos de la empresa. Entre ellos, el Whip Creamer, un auto de turbina, que fue su primer diseño para Hot Wheels. Tam trabajó para Mattel hasta 1973. Entre los muchos diseños futuristas se incluyen Evil Weevil, Open Fire, Six Shooter y el raro Double Header (co-diseñado con Larry Wood). A los 63 años, Paul Tam dirige un negocio de financiamiento en su natal Sudáfrica."
dis['Paul Tam']['biografia_limpia'] = bio_pt
dis['Paul Tam']['bio_es'] = bio_pt
dis['Paul Tam']['bio_en'] = "Paul Tam's lifelong dream was to design cars for General Motors. He joined Larry Wood and Ira Gilford at Mattel in the early days of Hot Wheels, designing signature cars including the Whip Creamer, Evil Weevil, Open Fire, Six Shooter, and Double Header. He worked for Mattel until 1973."
dis['Paul Tam']['bio_pt'] = "Paul Tam sonhou a vida inteira em projetar carros para a General Motors. Juntou-se a Larry Wood e Ira Gilford nos primeiros dias da Hot Wheels, projetando carros icônicos como o Whip Creamer. Trabalhou na Mattel até 1973."
dis['Paul Tam']['bio_fr'] = "Paul Tam a rêvé toute sa vie de concevoir des voitures pour General Motors. Il a rejoint Larry Wood et Ira Gilford aux débuts de Hot Wheels, concevant des voitures emblématiques comme le Whip Creamer. Il a travaillé chez Mattel jusqu'en 1973."
dis['Paul Tam']['foto'] = 'https://static.wikia.nocookie.net/hotwheels/images/a/a0/Paul_Tam_Header.jpg'
dis['Paul Tam']['proyectos'] = ["Whip Creamer", "AMX/2", "Evil Weevil", "Hairy Hauler", "Six Shooter", "Ferrari 512S", "Open Fire", "Double Header"]
dis['Paul Tam']['nacionalidad'] = 'Sudafricano'
dis['Paul Tam']['periodo'] = '1970-1973'

# Dave Weise
bio_dw = "David H. Weise es un ex empleado de Mattel que trabajo para Mattel de 1993 a 2015. Es conocido por disenar muchos autos de fantasia como 24/Seven, Radio Flyer Wagon, Baby Boomer y Power Bomb. Dave se mudo a Matchbox en 2006 y diseno alla hasta 2015. Sus Hot Wheels favoritos son 24/Seven y Splittin Image."
dis['Dave Weise']['biografia_limpia'] = bio_dw
dis['Dave Weise']['bio_es'] = bio_dw
dis['Dave Weise']['bio_en'] = "David H. Weise is a former Mattel employee who worked from 1993 to 2015. He is known for designing many fantasy cars such as 24/Seven, Radio Flyer Wagon, Baby Boomer and Power Bomb. He moved to Matchbox in 2006 and retired in 2015."
dis['Dave Weise']['bio_pt'] = "David H. Weise e um ex-funcionario da Mattel que trabalhou de 1993 a 2015. E conhecido por projetar carros de fantasia como 24/Seven, Radio Flyer Wagon, Baby Boomer e Power Bomb."
dis['Dave Weise']['bio_fr'] = "David H. Weise est un ancien employe de Mattel qui a travaille de 1993 a 2015. Il est connu pour avoir concu de nombreuses voitures fantastiques comme 24/Seven, Radio Flyer Wagon, Baby Boomer et Power Bomb."
dis['Dave Weise']['foto'] = 'https://static.wikia.nocookie.net/hotwheels/images/8/8e/DaveWeise.jpg'
dis['Dave Weise']['proyectos'] = ["24/Seven", "Radio Flyer Wagon", "Baby Boomer", "Power Bomb", "Splittin' Image", "70 Plymouth Barracuda", "97 Corvette", "BMW M Roadster", "Excavator", "25th Anniversary Lamborghini Countach", "Mercedes C-Class", "67 Dodge Charger", "69 Mercury Cyclone"]
dis['Dave Weise']['nacionalidad'] = 'Estadounidense'
dis['Dave Weise']['periodo'] = '1993-2015'

# Carter Simmons
bio_cs = "Carter Simmons es un disenador de Hot Wheels que trabajo en Mattel en los anos 2000. Es conocido por su trabajo en la serie HW Art Cars y otros disenos especiales."
dis['Carter Simmons']['biografia_limpia'] = bio_cs
dis['Carter Simmons']['bio_es'] = bio_cs
dis['Carter Simmons']['bio_en'] = "Carter Simmons is a Hot Wheels designer who worked at Mattel in the 2000s. He is known for his work on the HW Art Cars series and other special designs."
dis['Carter Simmons']['bio_pt'] = "Carter Simmons e um designer da Hot Wheels que trabalhou na Mattel nos anos 2000. Conhecido pelo seu trabalho na serie HW Art Cars."
dis['Carter Simmons']['bio_fr'] = "Carter Simmons est un designer Hot Wheels qui a travaille chez Mattel dans les annees 2000. Connu pour son travail sur la serie HW Art Cars."
dis['Carter Simmons']['nacionalidad'] = 'Estadounidense'
dis['Carter Simmons']['periodo'] = '2000-2010'

# Charlie Winfield
bio_cw = "Charlie Winfield es un disenador de Hot Wheels que trabajo en Mattel. Es conocido por su trabajo en la serie HW Rescue y otros disenos especiales."
dis['Charlie Winfield']['biografia_limpia'] = bio_cw
dis['Charlie Winfield']['bio_es'] = bio_cw
dis['Charlie Winfield']['bio_en'] = "Charlie Winfield is a Hot Wheels designer who worked at Mattel. He is known for his work on the HW Rescue series and other special designs."
dis['Charlie Winfield']['bio_pt'] = "Charlie Winfield e um designer da Hot Wheels que trabalhou na Mattel. Conhecido pelo seu trabalho na serie HW Rescue."
dis['Charlie Winfield']['bio_fr'] = "Charlie Winfield est un designer Hot Wheels qui a travaille chez Mattel. Connu pour son travail sur la serie HW Rescue."
dis['Charlie Winfield']['nacionalidad'] = 'Estadounidense'
dis['Charlie Winfield']['periodo'] = '2000-2010'

# Guardar
with open(base + 'disenadores.json', 'w', encoding='utf-8') as f:
    json.dump(dis, f, ensure_ascii=False, indent=2)

print("Disenadores actualizados:")
for nombre in ['Paul Tam', 'Dave Weise', 'Carter Simmons', 'Charlie Winfield']:
    d = dis[nombre]
    print(f"  {nombre}: bio={len(d.get('biografia_limpia',''))} chars, foto={'SI' if d.get('foto') else 'NO'}, proyectos={len(d.get('proyectos',[]))}")
