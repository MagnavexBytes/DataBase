import pprint
import sqlite3
conn = sqlite3.connect('ACVI_Parts/ACVI_Parts.sqlite')
c = conn.cursor()
pp = pprint.PrettyPrinter(indent = 1, width = 160, compact = False) 
c.execute('''PRAGMA foreign_keys = ON''')


# Удаление таблиц целиком
c.execute('''DROP TABLE IF EXISTS generator_stats''')
c.execute('''DROP TABLE IF EXISTS fcs_stats''')
c.execute('''DROP TABLE IF EXISTS booster_stats''')
c.execute('''DROP TABLE IF EXISTS weapon_stats''')

c.execute('''DROP TABLE IF EXISTS leg_stats''')
c.execute('''DROP TABLE IF EXISTS arm_stats''')
c.execute('''DROP TABLE IF EXISTS core_stats''')
c.execute('''DROP TABLE IF EXISTS head_stats''')

c.execute('''DROP TABLE IF EXISTS frame_stats''')
c.execute('''DROP TABLE IF EXISTS parts''')

c.execute('''DROP VIEW IF EXISTS full_head_stats''')
c.execute('''DROP VIEW IF EXISTS full_core_stats''')
c.execute('''DROP VIEW IF EXISTS full_arms_stats''')
c.execute('''DROP VIEW IF EXISTS full_legs_stats''')


# Таблицы
# Таблица характеристик, присутствующих у всех деталей
c.execute('''CREATE TABLE IF NOT EXISTS parts (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL UNIQUE,
          category TEXT NOT NULL CHECK (category IN ('Head', 'Core', 'Arms', 'Legs', 'R-Arm', 'L-Arm', 'R-Back', 'L-Back', 'Booster', 'FCS', 'Generator')),
          manufacturer TEXT CHECK (manufacturer IN ('Balam', 'Dafeng Core Industries', 'RaD', 'Rubicon Research Institute', 'ALLMIND', 'Arquebus ADD', 'Arquebus', 'BAWS', 'Schneider', 'Elcano')),
          price INTEGER NOT NULL,
          weight INTEGER NOT NULL,
          en_load INTEGER NOT NULL,
          description TEXT NOT NULL)
''')

# Таблица характеристик, присутствующих только у оружия
c.execute('''CREATE TABLE IF NOT EXISTS weapon_stats (
            weapon_id INTEGER PRIMARY KEY,
            attack_power INTEGER,
            impact INTEGER,
            damage_type TEXT CHECK (damage_type IN ('Kinetic', 'Energy', 'Explosion', 'Coral')),
            FOREIGN KEY (weapon_id) REFERENCES parts(id))
''')

# Промежуточная таблица характеристик, присутствующих у всех частей каркаса
c.execute('''CREATE TABLE IF NOT EXISTS frame_stats (
    frame_id INTEGER PRIMARY KEY,
    ap INTEGER,
    anti_kinetic INTEGER,
    anti_energy INTEGER,
    anti_explosive INTEGER,
    attitude_stability INTEGER,
    FOREIGN KEY (frame_id) REFERENCES parts(id))
''')

# Таблица характеристик, присутствующих только у частей голов
c.execute('''CREATE TABLE IF NOT EXISTS head_stats (
    head_id INTEGER PRIMARY KEY,
    system_recovery INTEGER,
    scan_distance INTEGER,
    scan_duration REAL,
    FOREIGN KEY (head_id) REFERENCES frame_stats(frame_id))
''')

# Таблица характеристик, присутствующих только у частей корпуса
c.execute('''CREATE TABLE IF NOT EXISTS core_stats (
    core_id INTEGER PRIMARY KEY,
    booster_efficiency_adj INTEGER,
    generator_output_adj INTEGER,
    generator_supply_adj INTEGER,
    FOREIGN KEY (core_id) REFERENCES frame_stats(frame_id))
''')

# Таблица характеристик, присутствующих только у частей рук
c.execute('''CREATE TABLE IF NOT EXISTS arm_stats (
    arm_id INTEGER PRIMARY KEY,
    arms_load_limit INTEGER,
    recoil_control INTEGER,
    firearms_specialization INTEGER,
    melee_specialization INTEGER,
    FOREIGN KEY (arm_id) REFERENCES frame_stats(frame_id))
''')

# Таблица характеристик, характерных только для деталей ног
c.execute('''CREATE TABLE IF NOT EXISTS leg_stats (
    leg_id INTEGER PRIMARY KEY,
    load_limit INTEGER NOT NULL,
    leg_type TEXT CHECK (leg_type IN ('Bipedal', 'Reverse Joint', 'Tetrapod', 'Tank', 'Hover')),
    jump_distance INTEGER, --поля jump_distance и jump_height могут быть NULL значением
    jump_height INTEGER, --Ибо ноги типа tank и hover не могут прыгать
    FOREIGN KEY (leg_id) REFERENCES frame_stats(frame_id))
''')

# Таблица характеристик, присутствующих только у частей ускорителей
c.execute('''CREATE TABLE IF NOT EXISTS booster_stats (
    booster_id INTEGER PRIMARY KEY,
    thrust INTEGER  NOT NULL,
    upward_thrust INTEGER  NOT NULL,
    upward_en_consumption INTEGER  NOT NULL,
    qb_thrust INTEGER  NOT NULL,
    qb_jet_duration REAL  NOT NULL,
    qb_en_consumption INTEGER  NOT NULL,
    qb_reload_time REAL  NOT NULL,
    qb_reload_ideal_weight INTEGER  NOT NULL,
    ab_thrust INTEGER  NOT NULL,
    ab_en_consumption INTEGER  NOT NULL,
    melee_attack_thrust INTEGER  NOT NULL,
    melee_attack_en_consumption INTEGER  NOT NULL,
    FOREIGN KEY (booster_id) REFERENCES parts(id))
''')

# Таблица характеристик, присутствующих только у частей СУО
c.execute('''CREATE TABLE IF NOT EXISTS fcs_stats (
    fcs_id INTEGER PRIMARY KEY,
    close_assist INTEGER NOT NULL,
    medium_assist INTEGER NOT NULL,
    long_assist INTEGER NOT NULL,
    missile_lock_correction INTEGER NOT NULL,
    multi_lock_correction INTEGER NOT NULL,
    FOREIGN KEY (fcs_id) REFERENCES parts(id))
''')

# Таблица характеристик, присутствующих только у частей генератора
c.execute('''CREATE TABLE IF NOT EXISTS generator_stats (
    generator_id INTEGER PRIMARY KEY,
    en_capacity INTEGER NOT NULL,
    en_recharge INTEGER NOT NULL,
    supply_recovery INTEGER NOT NULL,
    post_recovery_en_supply INTEGER NOT NULL,
    en_output INTEGER NOT NULL,
    FOREIGN KEY (generator_id) REFERENCES parts(id))
''')


# Данные
parts_data = [(1, 'IB-C03H: HAL 826', 'Head', 'Rubicon Research Institute', 0, 3760, 215, 'Head part for the HAL 826 piloted AC, developed long ago by the Rubicon Research Institute. The last of the Ibis Series and the only piloted Ibis craft, it was built to be the final safety valve to prevent a Coral Collapse.'),
              (2, '20-082 MIND BETA', 'Head', 'ALLMIND', 0, 3460, 128, 'Model head part developed by ALLMIND. In line with a change in approach, this part maximized stability at the expense of armor robustness.'),
              (3, '20-081 MIND ALPHA', 'Head', 'ALLMIND', 0, 3350, 142, 'Head part developed my ALLMIND for model ACs. Designed as part of a research project to extend human sensory capabilities, with numberous optimizations to create an AC that, to the pilot, feels like an extension of the body.'),
              (4, 'HC-2000/BC SHADE EYE', 'Head', 'RaD', 0, 3090, 163, 'Custom part derived from the scout AC head developed by RaD. Comprehensively rebuilt for combat by an anonymous independent mercenary group, this model takes some steps forward but sacrifices the minimalism of its predecessor.'),
              (5, 'VE-44A', 'Head', 'Arquebus ADD', 0, 3640, 182, 'Heavyweight head part designed by Arquebus ADD. Incoporates cutting-edge technology to enable defiance of the PCA. This models distinctive curved armor plating provides solid defense against damage of all kinds.'),
              (6, 'VP-44D', 'Head', 'Arquebus', 0, 3260, 177, 'Head part developed by Arquebus, derived from an existing model. Engineered in anticipation of regular use by the Vespers, this model features further improvements to stability.'),
              (7, 'HD-033M VERRILL', 'Head', 'Balam', 0, 3830, 240, 'Retrofitted head part developed by Balam. This high-end model is a strong performer with a hefty energy footprint, and features an intimidating spider-eye design chosen to suit the tastes of the Redguns commander.'),
              (8, 'AH-J-124/RC JAILBREAK', 'Head', 'BAWS', 0, 4250, 95, 'Junk. Originally a head part for an old-generation AC developed by BAWS. RaD engineers infiltrated Institute City to make field repairs—just enough to make this part operable, but not enough to fix its weathered armor.'),
              (9, 'HS-5000 APPETIZER', 'Head', 'RaD', 0, 3000, 103, 'Head part for a combat AC developed by RaD. though it was assembled from a patchwork of reclaimed resources, RaD mobilized its entire engineering team to fine-tune its design for formidable performance.'),
              (10, 'IA-C01H: EPHEMERA', 'Head', 'Rubicon Research Institute', 0, 4330, 235, 'Head part for the EPHEMERA unpiloted ACs, developed long ago by the Rubicon Research Institute. An old development quirk allows for piloted operation, but one should not any concessions for the limit of human sight.'),
              (11, 'EL-PH-00 ALBA', 'Head', 'Elcano', 0, 2600, 205, 'A new head part developed by Elcano. This model utilizes technology recovered from Furlong Dynamics to achieve improved overall balance and precise AC control.'),
              (12, 'VE-44B', 'Head', 'Arquebus ADD', 0, 4320, 265, 'Special head part designed by Arquebus ADD. Engineered to accommodate a proposal from V.VII, this model maximizes scanning performance, positioning its overall performance close to that of a surveillance-orientated concept model.'),
              (13, 'VP-44S', 'Head', 'Arquebus', 0, 3080, 148, 'Mass-produced head part developed by Arquebus. A number of refinements and updates have been made to the strong foundation laid by the preceding model, creating a masterpiece in the realm of second-generation AC parts.'),
              (14, 'NACHTREIHER/44E', 'Head', 'Schneider', 0, 2320, 210, 'Lightweight head part developed by Schneider. Schneider is a specialist in aerodynamic research, and this model reflects their experience with a light but highly stable build.'),
              (15, 'KASUAR/44Z', 'Head', 'Schneider', 0, 2590, 254, 'Expanded head part developed by Schneider. This model further improves on stability but with a higher energy burden, resulting in excellent performance in aerial combat.'),
              (16, 'HD-012 MELANDER C3', 'Head', 'Balam', 0, 3300, 165, 'Custom head part developed by Balam. Altered to improve combat suitability, the revisions to this model include partial armor plating and the addition of a scanner module.'),
              (17, 'HD-011 MELANDER', 'Head', 'Balam', 0, 3160, 135, 'Medium-weight head part developed by Balam. The simple design and solid performance of this model make it suited for mass production—reflecting Balams strategy of overwhelming its enemies with its material superiority.'),
              (18, 'HC-3000 WRECKER', 'Head', 'RaD', 0, 3800, 102, 'Head part for construction ACs developed by RaD. Specced for demolition work, this model makes up for combat performance shortcomings with its sturdiness and outstanding defensive performance.'),
              (19, 'HC-2000 FINDER EYE', 'Head', 'RaD', 0, 2670, 125, 'Head part for scout ACs developed by RaD. Originally specced for surveying terrain, this model makes up for what it lacks in combat performance with a light energy footprint and commendable ease of use.'),
              (20, 'EL-TH-10 FIRMEZA', 'Head', 'Elcano', 0, 2570, 134, 'Lightweight head part developed by Elcano. In keeping with Elcanos roots in producing and forging steel, this model exhibits craftsman-like flair, being light while providing reliable defenses.'),
              (21, 'AH-J-124 BASHO', 'Head', 'BAWS', 0, 4600, 95, 'Head part developed by BAWS for an old-generation AC. Said AC was one of the earliest models, developed to succeed MT-class machines, and modern fans for such classic hardware are fond of its characteristic bulk.'),
              (22, 'DF-HD-08 TIAN-QIANG', 'Head', 'BAWS', 0, 1230, 88, 'Head part developed by Dafeng Core Industries for the heavyweight TIAN-QIANG AC. Incorporates only the most essential functionality with a minimalist build in keeping with Dafengs "stout tree, slender branches philosophy.'),

              (23, 'IB-C03C: HAL 826', 'Core', 'Rubicon Research Institute', 0, 18520, 366, 'Core part for the HAL 826 piloted AC, developed long ago by the Rubicon Research Institute. The last of the Ibis Series and the only piloted Ibis craft, if was built to be the final safety valve to prevent Coral Collapse.'),
              (24, 'IA-C01C: EPHEMERA', 'Core', 'Rubicon Research Institute', 0, 13200, 412, 'Core part for the EPHEMERA unpiloted ACs, developed long ago by the Rubicon Research Institute. An old development quirk allows for piloted operation, but the core box makes only perfunctory concessions for a human occupant.'),
              (25, '07-061 MIND ALPHA', 'Core', 'ALLMIND', 0, 16510, 364, 'Core part developed by ALLMIND for model ACs. Designed as part of a research project to extend human sensory capabilities, with numerous optimizations to create an AC that, to the pilot, feels like an extension of the body.'),
              (26, 'CS-5000 MAIN DISH', 'Core', 'RaD', 0, 23600, 413, 'Core part for a combat AC developed by RaD. though it was assembled from a patchwork of reclaimed resources, RaD mobilized its entire engineering team to fine-tune its design for formidable performance.'),
              (27, 'AC-J-120/RC JAILBREAK', 'Core', 'BAWS', 0, 12350, 300, 'Junk. Originally a core part for an old-generation AC developed by BAWS. RaD engineers infiltrated Institute City to make field repairs—just enough to make this part operable, but not enough to fix its weathered armor.'),
              (28, 'EL-PC-00 ALBA', 'Core', 'Elcano', 0, 12000, 315, 'A new core part developed by Elcano. This model utilizes technological insights derived from analysing Schneider ACs to achieve improved overall balance and high suitability for aerial combat'),
              (29, 'VE-40A', 'Core', 'Arquebus ADD', 0, 21100, 432, 'Heavyweight core part designed by Arquebus ADD. Incorporates cutting-edge technology to enable defiance of the PCA. This model features excellent generator output adjustment and solid defense against damage of all kinds.'),
              (30, 'VP-40S', 'Core', 'Arquebus', 0, 15030, 337, 'Mass-produced core part developed by Arquebus. A number of refinements and updates have been made to the strong foundation laid by the preceding model, creating a masterpiece in the realm second-generation AC parts.'),
              (31, 'NACHTREIHER/40E', 'Core', 'Schneider', 0, 9820, 330, 'Lightweight core part developed by Schneider. Schneider is a specialist in aerodynamic research, and this model reflects their experience with a light and highly agile build.'),
              (32, 'EL-TC-10 FIRMEZA', 'Core', 'Elcano', 0, 10890, 351, 'Lightweight core part developed by Elcano. In keeping with Elcanos roots in producing and forging steel, this model exhibits craftsman-like flair, being light while providing reliable defenses.'),
              (33, 'DF-BD-08 TIAN-QIANG', 'Core', 'Dafeng Core Industries', 0, 20650, 388, 'Core part developed by Dafeng Core Industries for the heavyweight TIAN-QIANG AC. This is the "trunk" in Dafengs "stout tree, slender branches philosophy; a defensive foundation with extremely heavy, sturdy armor.'),
              (34, 'CC-3000 WRECKER', 'Core', 'RaD', 0, 19000, 310, 'Core part for construction ACs developed by RaD. Specced for demolition work, this model make up for combat performance shortcomings with its sturdiness and outstanding physical defences.'),
              (35, 'BD-012 MELANDER C3', 'Core', 'Balam', 0, 14050, 322, 'Custom core part developed by Balam. Altered to improve combat suitability, this model features a lighter basic frame enhanced with partial armor plating to maintain a modest weight.'),
              (36, 'BD-011 MELANDER', 'Core', 'Balam', 0, 15800, 304, 'Medium-weight core part developed by Balam. The simple design and solid performance of this model make it suited for mass production—reflecting Balams strategy of overwhelming its enemies with its material superiority.'),
              (37, 'AC-J-120 BASHO', 'Core', 'BAWS', 0, 16100, 300, 'Core part developed by BAWS for an old-generation AC. Said AC was one of the earliest models, developed to succeed MT-class machines, and modern fans of such classic hardware are fond of its characteristic bulk.'),
              (38, 'CC-2000 ORBITER', 'Core', 'RaD', 0, 12650, 267, 'Core part for scout ACs developed by RaD. Originally specced for extravehicular activity in space, this model makes up for what it lacks in combat performance with a light energy footprint and commendable ease of use.'),

              (39, 'VP-46D', 'Arms', 'Arquebus', 0, 10990, 248, 'Arm parts developed by Arquebus, derived from an existing model. Engineered in anticipation of regular use by the Vespers, this model features further improvements to performance.'),
              (40, 'IA-C01A: EPHEMERA', 'Arms', 'Rubicon Research Institute', 0, 12700, 312, 'Arm parts for the EPHEMERA unpiloted ACs, developed long ago by the Rubicon Research Institute. An old development quirk allows for piloted operation, albeit with actuation translation that outstrips the capability of human nerves.'),
              (41, 'AS-5000 SALAD', 'Arms', 'RaD', 0, 20940, 356, 'Arm parts for a combat AC developed by RaD. though it was assembled from a patchwork of reclaimed resources, RaD mobilized its entire engineering team to fine-tune its design for formidable performance.'),
              (42, 'AA-J-123/RC JAILBREAK', 'Arms', 'BAWS', 0, 8480, 210, 'Junk. Originally arm parts for an old-generation AC developed by BAWS. RaD engineers infiltrated Institute City to make field repairs—just enough to make this part operable, but not enough to fix its weathered armor.'),
              (43, 'VE-46A', 'Arms', 'Arquebus ADD', 0, 22210, 380, 'Heavyweight arm parts designed by Arquebus ADD. Incorporates cutting-edge technology to enable defiance of the PCA. This models distinctive curved armor plating proved solid defence against damage of all kinds.'),
              (44, 'VP-46S', 'Arms', 'Arquebus', 0, 14020, 278, 'Mass-produced arm parts developed by Arquebus. A number of refinements and updates have been made to the strong foundation laid by the preceding model, creating a masterpiece in the realm of second-generation AC parts.'),
              (45, 'NACHTREIHER/46E', 'Arms', 'Schneider', 0, 11420, 302, 'Lightweight arm parts developed by Schneider. Schneider is a specialist in aerodynamic research, and this model reflects their experience with a light and highly agile build.'),
              (46, 'EL-TA-10 FIRMEZA', 'Arms', 'Elcano', 0, 11220, 270, 'Lightweight arm parts developed by Elcano. In keeping with Elcanos roots in producing and forging steel, this model exhibits craftsman-like flair, being light while providing dependable carrying capacity.'),
              (47, 'DF-AR-09 TIAN-LAO', 'Arms', 'Dafeng Core Industries', 0, 26740, 266, 'Revised arm parts developed by Dafeng Core Industries. This model attempts to further refine Dafengs (stout tree, slender branches) philosophy by enhancing the durability of the armor plating around the shoulders.'),
              (48, 'DF-AR-08 TIAN-QIANG', 'Arms', 'Dafeng Core Industries', 0, 20020, 295, 'Arm parts developed by Dafeng Core Industries for the heavyweight TIAN-QIANG AC. Built to embody Dafengs (stout tree, slender branches) philosophy, their weight is balanced by heavy upper arms and lighter forearms.'),
              (49, 'AR-012 MELANDER C3', 'Arms', 'Balam', 0, 12300, 232, 'Custom arm parts developed by Balam. Altered to improve combat suitability, this model features a lighter basic frame while also enhancing arm maneuverability.'),
              (50, 'AC-3000 WRECKER', 'Arms', 'RaD', 0, 14650, 220, 'Arm parts for construction ACs developed by RaD. Specced for demolition work, this model make up for combat performance shortcomings with its sturdiness and excellent recoil control.'),
              (51, 'AC-2000 TOOL ARM', 'Arms', 'Balam', 0, 11300, 216, 'Arm parts for scout ACs developed by RaD. Originally specced for recovering scrap, this model makes up for what it lacks in combat performance with a light energy footprint and commendable ease of use.'),
              (52, 'AA-J-123 BASHO', 'Arms', 'BAWS', 0, 10480, 210, 'Arm parts developed by BAWS for an old-generation AC. Said AC was one of the earliest models, developed to succeed MT-class machines, and modern fans of such classic hardware are fond of its characteristic bulk.'),
              (53, '04-101 MIND ALPHA', 'Arms', 'ALLMIND', 0, 16960, 358, 'Arm parts developed by ALLMIND for model ACs. Designed as part of a research project to extend human sensory capabilities, with numerous optimizations to create an AC that, to the pilot, feels like an extension of the body.'),
              (54, 'AR-011 MELANDER', 'Arms', 'Balam', 0, 13650, 265, 'Medium-weight arm parts developed by Balam. The simple design and solid performance of this model make it suited for mass production—reflecting Balams strategy of overwhelming its enemies with its material superiority.'),              
              
              (55, 'VE-42B', 'Legs', 'Arquebus ADD', 0, 46600, 824, 'Special tank parts designed by Arquebus ADD. Prioritizes hovering performance and forward propulsion to focus on aerial combat. During development, the specs were stolen and leaked by an independent mercenary.'),
              (56, 'AL-J-121/RC JAILBREAK', 'Legs', 'BAWS', 0, 18560, 300, 'Junk. Originally bipedal leg parts for an old-generation AC developed by BAWS. RaD engineers infiltrated Institute City to make field repairs—just enough to make this part operable, but not enough to fix its weathered armor.'),
              (57, 'IA-C01L: EPHEMERA', 'Legs', 'Rubicon Research Institute', 0, 15200, 398, 'Bipedal legs for EPHEMERA unpiloted ACs, developed long ago by the Rubicon Research Institute. An old development quirk allows for piloted operation, albeit with actuation translation that outstrips the capability of human nerves.'),
              (58, '06-041 MIND ALPHA', 'Legs', 'ALLMIND', 0, 22110, 432, 'Bipedal legs developed by ALLMIND for model ACs. Designed as part of a research project to extend human sensory capabilities, with numerous optimization to create an AC that, to the pilot, feels like an extension of the body.'),
              (59, 'EL-TL-11 FORTALEZA', 'Legs', 'Elcano', 0, 24650, 620, 'Lightweight tank parts developed by Elcano. Inspired by wheelchairs made for competitive sports, this product was an instant success with soldier who had lost the use of their legs in combat but still pined for the battlefield.'),
              (60, 'VE-42A', 'Legs', 'Arquebus ADD', 0, 28950, 465, 'Heavyweight bipedal leg parts designed by Arquebus ADD. Incorporates cutting-edge technology to enable defiance of the PCA. This model utilizes hover movement or increased loading capacity and greatly improved stability.'),
              (61, 'AL-J-121 BASHO', 'Legs', 'BAWS', 0, 20520, 300, 'Bipedal legs developed by BAWS for an old-generation AC. Said AC was one of the earliest models, developed to succeed MT-class machines, and moderns fans of such classic hardware are fond of its characteristic bulk.'),
              (62, 'VP-422', 'Legs', 'Arquebus', 0, 17900, 387, 'Mass-produced bipedal leg parts developed by Arquebus. A number of refinements and updates have been made to the strong foundation laid by the preceding model, creating a masterpiece in the realm of second-generation AC parts.'),
              (63, 'LG-011 MELANDER', 'Legs', 'Balam', 0, 18700, 365, 'Medium-weight bipedal leg parts developed by Balam. The simple design and solid performance of this model make it suited for mass production—reflecting Balams strategy of overwhelming its enemies with its material superiority.'),
              (64, '2S-5000 DESSERT', 'Legs', 'RaD', 0, 25880, 420, 'Bipedal leg parts for a combat AC developed by RaD. though it was assembled from a patchwork of reclaimed resources, RaD mobilized its entire engineering team to fine-tune its design for formidable performance.'),
              (65, 'LG-022T BORNEMISSZA', 'Legs', 'Balam', 0, 49800, 455, 'Heavyweight tank parts developed by Balam. Designed with the simple goal of turning ACs into tanks capable of carrying the heavy weapons manufactured by Dafeng Core Industries.'),
              (66, 'LG-033M VERRILL', 'Legs', 'Balam', 0, 36200, 675, 'Tetrapod leg option developed by Balam. The design division was all but held at gunpoint to produce a model that satisfied the Redguns demand for a highly mobile AC platform also capable of supporting heavy weaponry.'),
              (67, 'NACHTREIHER/42E', 'Legs', 'Schneider', 0, 14030, 462, 'Lightweight bipedal leg parts developed by Schneider. Schneider is a specialist in aerodynamic research, and this model reflects their experience with a light and highly agile build.'),
              (68, 'LG-012 MELANDER C3', 'Legs', 'Balam', 0, 17210, 355, 'Custom bipedal leg parts developed by Balam. Altered to improve combat suitability, this model features a lighter basic frame enhanced with partial armor plating to maintain a modest weight.'),
              (69, 'VP-424', 'Legs', 'Arquebus', 0, 31600, 760, 'Tetrapod leg parts developed by Arquebus, derived from an existing model. Intended for tetrapods deployed along-side Arquebuss bipedal and reverse-joint ACs, this model focuses on mobility to enable hovering-based fire support.'),
              (70, '06-042 MIND BETA', 'Legs', 'ALLMIND', 0, 22000, 426, 'Alternative reverse-joint legs developed by ALLMIND. Marking a new approach, this part explores changes in human sensory perception though introduction of alien elements; in this case, animal-like digitigrade legs.'),
              (71, 'RC-2000 SPRING CHICKEN', 'Legs', 'RaD', 0, 25890, 402, 'Heavyweight reverse-joint legs for scout ACs developed by RaD. Originally specced for resource transportation rather than combat, these legs are capable of leaping up to high positions while supporting a significant weight burden.'),
              (72, 'KASUAR/42Z', 'Legs', 'Schneider', 0, 19060, 388, 'Lightweight reverse-joint legs developed by Schneider. These legs sacrifice stability and defensive performance to provide exceptional jumping performance, enabling agile transitions to aerial combat—as is Schneiders forte'),
              (73, 'EL-TL-10 FIRMEZA', 'Legs', 'Elcano', 0, 11200, 378, 'Lightweight bipedal leg parts developed by Elcano. In keeping with Elcanos roots in producing and forging steel, this model exhibits craftsman-like flair, being light yet retaining high load capacity.'),
              (74, '2C-3000 WRECKER', 'Legs', 'RaD', 0, 21680, 680, 'Bipedal leg parts for construction ACs developed by RaD. Specced for demolition work, this model make up for combat performance shortcomings with its sturdiness and outstanding loading capacity.'),
              (75, '2C-2000 CRAWLER', 'Legs', 'RaD', 0, 16300, 280, 'Bipedal legs for scout ACs developed by RaD. Originally specced for surface surveys of astronomical objects, this model makes up for what it lacks in combat performance with a light energy footprint and commendable ease of use.'),
              (76, 'DF-LG-08 TIAN-QIANG', 'Legs', 'Dafeng Core Industries', 0, 23600, 400, 'Bipdedal legs developed by Dafeng Core Industries for the heavyweight TIAN-QIANG AC. Built to embody Dafengs "stout tree, slender branches" philosophy, their weight is balanced by heavy upper legs and lighter lower legs.'),
              
              (77, 'Test', 'Booster', 'Balam', 0, 0, 0, 'Test')]

c.executemany("INSERT INTO parts (id, name, category, manufacturer, price, weight, en_load, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", parts_data)
conn.commit()

frame_stats_data = [(1, 930, 169, 182, 180, 436),
                    (2, 520, 158, 164, 150, 536),
                    (3, 820, 178, 186, 173, 365),
                    (4, 770, 174, 167, 181, 448),
                    (5, 1060, 179, 188, 178, 393),

                    (6, 0, 0, 0, 0, 0),
                    (7, 0, 0, 0, 0, 0),
                    (8, 0, 0, 0, 0, 0),
                    (9, 0, 0, 0, 0, 0),
                    (10, 0, 0, 0, 0, 0),
                    (11, 0, 0, 0, 0, 0),
                    (12, 0, 0, 0, 0, 0),
                    (13, 0, 0, 0, 0, 0),
                    (14, 0, 0, 0, 0, 0),
                    (15, 0, 0, 0, 0, 0),
                    (16, 0, 0, 0, 0, 0),
                    (17, 0, 0, 0, 0, 0),
                    (18, 0, 0, 0, 0, 0),
                    (19, 0, 0, 0, 0, 0),
                    (20, 0, 0, 0, 0, 0),
                    (21, 0, 0, 0, 0, 0),
                    (22, 0, 0, 0, 0, 0),

                    (23, 0, 0, 0, 0, 0),
                    (24, 0, 0, 0, 0, 0),
                    (25, 0, 0, 0, 0, 0),
                    (26, 0, 0, 0, 0, 0),
                    (27, 0, 0, 0, 0, 0),
                    (28, 0, 0, 0, 0, 0),
                    (29, 0, 0, 0, 0, 0),
                    (30, 0, 0, 0, 0, 0),
                    (31, 0, 0, 0, 0, 0),
                    (32, 0, 0, 0, 0, 0),
                    (33, 0, 0, 0, 0, 0),
                    (34, 0, 0, 0, 0, 0),
                    (35, 0, 0, 0, 0, 0),
                    (36, 0, 0, 0, 0, 0),
                    (37, 0, 0, 0, 0, 0),
                    (38, 0, 0, 0, 0, 0),

                    (39, 0, 0, 0, 0, 0),
                    (40, 0, 0, 0, 0, 0),
                    (41, 0, 0, 0, 0, 0),
                    (42, 0, 0, 0, 0, 0),
                    (43, 0, 0, 0, 0, 0),
                    (44, 0, 0, 0, 0, 0),
                    (45, 0, 0, 0, 0, 0),
                    (46, 0, 0, 0, 0, 0),
                    (47, 0, 0, 0, 0, 0),
                    (48, 0, 0, 0, 0, 0),
                    (49, 0, 0, 0, 0, 0),
                    (50, 0, 0, 0, 0, 0),
                    (51, 0, 0, 0, 0, 0),
                    (52, 0, 0, 0, 0, 0),
                    (53, 0, 0, 0, 0, 0),
                    (54, 0, 0, 0, 0, 0),

                    (55, 0, 0, 0, 0, 0),
                    (56, 0, 0, 0, 0, 0),
                    (57, 0, 0, 0, 0, 0),
                    (58, 0, 0, 0, 0, 0),
                    (59, 0, 0, 0, 0, 0),
                    (60, 0, 0, 0, 0, 0),
                    (61, 0, 0, 0, 0, 0),
                    (62, 0, 0, 0, 0, 0),
                    (63, 0, 0, 0, 0, 0),
                    (64, 0, 0, 0, 0, 0),
                    (65, 0, 0, 0, 0, 0),
                    (66, 0, 0, 0, 0, 0),
                    (67, 0, 0, 0, 0, 0),
                    (68, 0, 0, 0, 0, 0),
                    (69, 0, 0, 0, 0, 0),
                    (70, 0, 0, 0, 0, 0),
                    (71, 0, 0, 0, 0, 0),
                    (72, 0, 0, 0, 0, 0),
                    (73, 0, 0, 0, 0, 0),
                    (74, 0, 0, 0, 0, 0),
                    (75, 0, 0, 0, 0, 0),
                    (76, 0, 0, 0, 0, 0)]
c.executemany("INSERT INTO frame_stats (frame_id, ap, anti_kinetic, anti_energy, anti_explosive, attitude_stability) VALUES (?, ?, ?, ?, ?, ?)", frame_stats_data)
conn.commit()

head_stats_data = [(1, 125, 600, 16.8),
                   (2, 116, 540, 12.0),
                   (3, 103, 320, 6.0),
                   (4, 115, 450, 10.8),
                   (5, 104, 490, 12.6),
                   (6, 100, 530, 14.4),
                   (7, 107, 510, 7.8),
                   (8, 60, 400, 6.0),
                   (9, 78, 610, 6.0),
                   (10, 132, 550, 4.8),
                   (11, 105, 500, 3.6),
                   (12, 154, 700, 18.0),
                   (13, 112, 520, 7.2),
                   (14, 92, 280, 13.2),
                   (15, 108, 620, 5.4),
                   (16, 95, 580, 12.0),
                   (17, 110, 310, 4.8),
                   (18, 55, 270, 3.0),
                   (19, 98, 290, 4.2),
                   (20, 55, 330, 15.0),
                   (21, 68, 340, 14.4),
                   (22, 50, 250, 7.0)]
c.executemany("INSERT INTO head_stats (head_id, system_recovery, scan_distance, scan_duration) VALUES (?, ?, ?, ?)", head_stats_data)
conn.commit()

core_stats_data = [(23, 96, 120, 108),
                   (24, 101, 126, 96),
                   (25, 95, 112, 104),
                   (26, 79, 97, 112),
                   (27, 119, 83, 94),
                   (28, 115, 101, 105),
                   (29, 81, 122, 95),
                   (30, 102, 106, 102),
                   (31, 349, 126, 84),
                   (32, 111, 104, 89),
                   (33, 76, 114, 90),
                   (34, 80, 96, 100),
                   (35, 103, 102, 103),
                   (36, 98, 105, 97),
                   (37, 119, 83, 94),
                   (38, 100, 103, 93)]
c.executemany("INSERT INTO core_stats (core_id, booster_efficiency_adj, generator_output_adj, generator_supply_adj) VALUES (?, ?, ?, ?)", core_stats_data)
conn.commit()

arm_stats_data = [(39, 0, 0, 0, 0),
                  (40, 0, 0, 0, 0),
                  (41, 0, 0, 0, 0),
                  (42, 0, 0, 0, 0),
                  (43, 0, 0, 0, 0),
                  (44, 0, 0, 0, 0),
                  (45, 0, 0, 0, 0),
                  (46, 0, 0, 0, 0),
                  (47, 0, 0, 0, 0),
                  (48, 0, 0, 0, 0),
                  (49, 0, 0, 0, 0),
                  (50, 0, 0, 0, 0),
                  (51, 0, 0, 0, 0),
                  (52, 0, 0, 0, 0),
                  (53, 0, 0, 0, 0),
                  (54, 0, 0, 0, 0)]
c.executemany("INSERT INTO arm_stats (arm_id, arms_load_limit, recoil_control, firearms_specialization, melee_specialization) VALUES (?, ?, ?, ?, ?)", arm_stats_data)
conn.commit()

leg_stats_data = [(55, 91000, 'Tank', None, None),
                  (56, 62600, 'Bipedal', 125, 25),
                  (57, 55050, 'Bipedal', 99, 27),
                  (58, 63810, 'Bipedal', 83, 22),
                  (59, 69300, 'Tank', None, None),
                  (60, 85700, 'Bipedal', 30, 14),
                  (61, 62600, 'Bipedal', 125, 25),
                  (62, 58620, 'Bipedal', 92, 23),
                  (63, 60520, 'Bipedal', 87, 22),
                  (64, 77100, 'Bipedal', 50, 19),
                  (65, 100300, 'Tank', None, None),
                  (66, 76200, 'Tetrapod', 82, 15),
                  (67, 48650, 'Bipedal', 228, 52),
                  (68, 55440, 'Bipedal', 98, 26),
                  (69, 69800, 'Tetrapod', 103, 18),
                  (70, 61600, 'Reverse Joint', 334, 60),
                  (71, 68360, 'Reverse Joint', 317, 70),
                  (72, 47820, 'Reverse Joint', 386, 80),
                  (73, 52100, 'Bipedal', 115, 28),
                  (74, 68900, 'Bipedal', 76, 17),
                  (75, 51200, 'Bipedal', 90, 24),
                  (76, 82600, 'Bipedal', 60, 20)]
c.executemany("INSERT INTO leg_stats (leg_id, load_limit, leg_type, jump_distance, jump_height) VALUES (?, ?, ?, ?, ?)", leg_stats_data)
conn.commit()

# weapon_stats_data = [(4, 135, 110, 'Kinetic')]
# c.executemany("INSERT INTO weapon_stats (weapon_id, attack_power, impact, damage_type) VALUES (?, ?, ?, ?)", weapon_stats_data)
# conn.commit()

# booster_stats_data = [(5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
# c.executemany("INSERT INTO booster_stats (booster_id, thrust, upward_thrust, upward_en_consumption, qb_thrust, qb_jet_duration, qb_en_consumption, qb_reload_time, qb_reload_ideal_weight, ab_thrust, ab_en_consumption, melee_attack_thrust, melee_attack_en_consumption) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", booster_stats_data)
# conn.commit()

# generator_stats_data = [(6, 2620, 892, 434, 1200, 3400)]
# c.executemany("INSERT INTO generator_stats (generator_id, en_capacity, en_recharge, supply_recovery, post_recovery_en_supply, en_output) VALUES (?, ?, ?, ?, ?, ?)", generator_stats_data)
# conn.commit()

# Создание новых таблиц полных статов деталей каркаса 
c.execute('''CREATE VIEW IF NOT EXISTS full_head_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.price, p.weight, p.en_load, p.description,
          fs.ap, fs.anti_kinetic, fs.anti_energy, fs.anti_explosive, fs.attitude_stability,
          hs.system_recovery, hs.scan_distance, hs.scan_duration
          FROM parts AS p
          LEFT JOIN frame_stats AS fs ON p.id = fs.frame_id
          LEFT JOIN head_stats AS hs ON fs.frame_id = hs.head_id
          WHERE p.id BETWEEN 1 AND 22
''')

c.execute('''CREATE VIEW IF NOT EXISTS full_core_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.price, p.weight, p.en_load, p.description,
          fs.ap, fs.anti_kinetic, fs.anti_energy, fs.anti_explosive, fs.attitude_stability,
          cs.booster_efficiency_adj, cs.generator_output_adj, cs.generator_supply_adj
          FROM parts AS p
          LEFT JOIN frame_stats AS fs ON p.id = fs.frame_id
          LEFT JOIN core_stats AS cs ON fs.frame_id = cs.core_id
          WHERE p.id BETWEEN 23 AND 38
''')

c.execute('''CREATE VIEW IF NOT EXISTS full_arm_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.price, p.weight, p.en_load, p.description,
          fs.ap, fs.anti_kinetic, fs.anti_energy, fs.anti_explosive, fs.attitude_stability,
          rs.arms_load_limit, rs.recoil_control, rs.firearms_specialization, rs.melee_specialization
          FROM parts AS p
          LEFT JOIN frame_stats AS fs ON p.id = fs.frame_id
          LEFT JOIN arm_stats AS rs ON fs.frame_id = rs.arm_id
          WHERE p.id BETWEEN 39 AND 54
''')

c.execute('''CREATE VIEW IF NOT EXISTS full_leg_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.price, p.weight, p.en_load, p.description,
          fs.ap, fs.anti_kinetic, fs.anti_energy, fs.anti_explosive, fs.attitude_stability,
          ls.load_limit, ls.leg_type, ls.jump_distance, ls.jump_height
          FROM parts AS p
          LEFT JOIN frame_stats AS fs ON p.id = fs.frame_id
          LEFT JOIN leg_stats AS ls ON fs.frame_id = ls.leg_id
          WHERE p.id BETWEEN 55 AND 76
''')


# c.execute("SELECT id FROM parts")
# existing_ids = {row[0] for row in c.fetchall()}
# missing_ids = [item[0] for item in frame_stats_data if item[0] not in existing_ids]
# if missing_ids:
#     print(f"Ошибка! Эти ID отсутствуют в таблице parts: {missing_ids}")
# else:
#     print("С ID все в порядке. Проблема в другом.")

conn.close()