import pprint
import sqlite3
conn = sqlite3.connect('ACVI_Parts/ACVI_Parts.sqlite')
c = conn.cursor()
pp = pprint.PrettyPrinter(indent = 1, width = 160, compact = False) 
c.execute('''PRAGMA foreign_keys = ON''')


# Удаление таблиц
c.execute('''DROP TABLE IF EXISTS ac_build''')

c.execute('''DROP TABLE IF EXISTS generator_stats''')
c.execute('''DROP TABLE IF EXISTS fcs_stats''')
c.execute('''DROP TABLE IF EXISTS booster_stats''')

c.execute('''DROP TABLE IF EXISTS leg_stats''')
c.execute('''DROP TABLE IF EXISTS arm_stats''')
c.execute('''DROP TABLE IF EXISTS core_stats''')
c.execute('''DROP TABLE IF EXISTS head_stats''')

c.execute('''DROP TABLE IF EXISTS frame_stats''')
c.execute('''DROP TABLE IF EXISTS parts''')


# Удаление пердставлений
c.execute('''DROP VIEW IF EXISTS ac_build_specs''')

c.execute('''DROP VIEW IF EXISTS full_head_stats''')
c.execute('''DROP VIEW IF EXISTS full_core_stats''')
c.execute('''DROP VIEW IF EXISTS full_arms_stats''')
c.execute('''DROP VIEW IF EXISTS full_legs_stats''')

c.execute('''DROP VIEW IF EXISTS full_booster_stats''')
c.execute('''DROP VIEW IF EXISTS full_fcs_stats''')
c.execute('''DROP VIEW IF EXISTS full_generator_stats''')


# Таблицы
c.execute('''CREATE TABLE IF NOT EXISTS parts (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL UNIQUE,
          category TEXT NOT NULL CHECK (category IN ('Head', 'Core', 'Arms', 'Legs', 'R-Arm', 'L-Arm', 'R-Back', 'L-Back', 'Booster', 'FCS', 'Generator')),
          manufacturer TEXT CHECK (manufacturer IN ('Balam', 'Dafeng Core Industries', 'RaD', 'Rubicon Research Institute', 'ALLMIND', 'Arquebus ADD', 'Arquebus', 'BAWS', 'Schneider', 'Elcano')),
          weight INTEGER NOT NULL,
          en_load INTEGER NOT NULL,
          description TEXT NOT NULL)
''')

c.execute('''CREATE TABLE IF NOT EXISTS frame_stats (
    frame_id INTEGER PRIMARY KEY,
    ap INTEGER NOT NULL,
    anti_kinetic INTEGER NOT NULL,
    anti_energy INTEGER NOT NULL,
    anti_explosive INTEGER NOT NULL,
    attitude_stability INTEGER NOT NULL,
        FOREIGN KEY (frame_id) REFERENCES parts(id))
''')

c.execute('''CREATE TABLE IF NOT EXISTS head_stats (
    head_id INTEGER PRIMARY KEY,
    system_recovery INTEGER NOT NULL,
    scan_distance INTEGER NOT NULL,
    scan_duration REAL NOT NULL,
        FOREIGN KEY (head_id) REFERENCES frame_stats(frame_id))
''')

c.execute('''CREATE TABLE IF NOT EXISTS core_stats (
    core_id INTEGER PRIMARY KEY,
    booster_efficiency_adj INTEGER NOT NULL,
    generator_output_adj INTEGER NOT NULL,
    generator_supply_adj INTEGER NOT NULL,
        FOREIGN KEY (core_id) REFERENCES frame_stats(frame_id))
''')

c.execute('''CREATE TABLE IF NOT EXISTS arm_stats (
    arm_id INTEGER PRIMARY KEY,
    arms_load_limit INTEGER NOT NULL,
    recoil_control INTEGER NOT NULL,
    firearms_specialization INTEGER NOT NULL,
    melee_specialization INTEGER NOT NULL,
        FOREIGN KEY (arm_id) REFERENCES frame_stats(frame_id))
''')

c.execute('''CREATE TABLE IF NOT EXISTS leg_stats (
    leg_id INTEGER PRIMARY KEY,
    load_limit INTEGER NOT NULL,
    leg_type TEXT NOT NULL CHECK (leg_type IN ('Bipedal', 'Reverse Joint', 'Tetrapod', 'Tank', 'Hover')),
    jump_distance INTEGER, --поля jump_distance и jump_height могут быть NULL значением
    jump_height INTEGER, --Ибо ноги типа tank и hover не могут прыгать
        FOREIGN KEY (leg_id) REFERENCES frame_stats(frame_id))
''')

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

c.execute('''CREATE TABLE IF NOT EXISTS fcs_stats (
    fcs_id INTEGER PRIMARY KEY,
    close_assist INTEGER NOT NULL,
    medium_assist INTEGER NOT NULL,
    long_assist INTEGER NOT NULL,
    missile_lock_correction INTEGER NOT NULL,
    multi_lock_correction INTEGER NOT NULL,
        FOREIGN KEY (fcs_id) REFERENCES parts(id))
''')

c.execute('''CREATE TABLE IF NOT EXISTS generator_stats (
    generator_id INTEGER PRIMARY KEY,
    en_capacity INTEGER NOT NULL,
    en_recharge INTEGER NOT NULL,
    supply_recovery INTEGER NOT NULL,
    post_recovery_en_supply INTEGER NOT NULL,
    en_output INTEGER NOT NULL,
        FOREIGN KEY (generator_id) REFERENCES parts(id))
''')

c.execute('''CREATE TABLE IF NOT EXISTS ac_build (
          build_id INTEGER PRIMARY KEY AUTOINCREMENT,
          build_name TEXT NOT NULL,
          head_id INTEGER,
          core_id INTEGER,
          arms_id INTEGER,
          legs_id INTEGER,
          booster_id INTEGER,
          fcs_id INTEGER,
          generator_id INTEGER,
            FOREIGN KEY(head_id) REFERENCES parts(id),
            FOREIGN KEY(core_id) REFERENCES parts(id),
            FOREIGN KEY(arms_id) REFERENCES parts(id),
            FOREIGN KEY(legs_id) REFERENCES parts(id),
            FOREIGN KEY(booster_id) REFERENCES parts(id),
            FOREIGN KEY(fcs_id) REFERENCES parts(id),
            FOREIGN KEY(generator_id) REFERENCES parts(id))
''')

# Данные
parts_data = [(1, 'IB-C03H: HAL 826', 'Head', 'Rubicon Research Institute', 3760, 215, 'Head part for the HAL 826 piloted AC, developed long ago by the Rubicon Research Institute. The last of the Ibis Series and the only piloted Ibis craft, it was built to be the final safety valve to prevent a Coral Collapse.'),
              (2, '20-082 MIND BETA', 'Head', 'ALLMIND', 3460, 128, 'Model head part developed by ALLMIND. In line with a change in approach, this part maximized stability at the expense of armor robustness.'),
              (3, '20-081 MIND ALPHA', 'Head', 'ALLMIND', 3350, 142, 'Head part developed my ALLMIND for model ACs. Designed as part of a research project to extend human sensory capabilities, with numberous optimizations to create an AC that, to the pilot, feels like an extension of the body.'),
              (4, 'HC-2000/BC SHADE EYE', 'Head', 'RaD', 3090, 163, 'Custom part derived from the scout AC head developed by RaD. Comprehensively rebuilt for combat by an anonymous independent mercenary group, this model takes some steps forward but sacrifices the minimalism of its predecessor.'),
              (5, 'VE-44A', 'Head', 'Arquebus ADD', 3640, 182, 'Heavyweight head part designed by Arquebus ADD. Incoporates cutting-edge technology to enable defiance of the PCA. This models distinctive curved armor plating provides solid defense against damage of all kinds.'),
              (6, 'VP-44D', 'Head', 'Arquebus', 3260, 177, 'Head part developed by Arquebus, derived from an existing model. Engineered in anticipation of regular use by the Vespers, this model features further improvements to stability.'),
              (7, 'HD-033M VERRILL', 'Head', 'Balam', 3830, 240, 'Retrofitted head part developed by Balam. This high-end model is a strong performer with a hefty energy footprint, and features an intimidating spider-eye design chosen to suit the tastes of the Redguns commander.'),
              (8, 'AH-J-124/RC JAILBREAK', 'Head', 'BAWS', 4250, 95, 'Junk. Originally a head part for an old-generation AC developed by BAWS. RaD engineers infiltrated Institute City to make field repairs—just enough to make this part operable, but not enough to fix its weathered armor.'),
              (9, 'HS-5000 APPETIZER', 'Head', 'RaD', 3000, 103, 'Head part for a combat AC developed by RaD. though it was assembled from a patchwork of reclaimed resources, RaD mobilized its entire engineering team to fine-tune its design for formidable performance.'),
              (10, 'IA-C01H: EPHEMERA', 'Head', 'Rubicon Research Institute', 4330, 235, 'Head part for the EPHEMERA unpiloted ACs, developed long ago by the Rubicon Research Institute. An old development quirk allows for piloted operation, but one should not any concessions for the limit of human sight.'),
              (11, 'EL-PH-00 ALBA', 'Head', 'Elcano', 2600, 205, 'A new head part developed by Elcano. This model utilizes technology recovered from Furlong Dynamics to achieve improved overall balance and precise AC control.'),
              (12, 'VE-44B', 'Head', 'Arquebus ADD', 4320, 265, 'Special head part designed by Arquebus ADD. Engineered to accommodate a proposal from V.VII, this model maximizes scanning performance, positioning its overall performance close to that of a surveillance-orientated concept model.'),
              (13, 'VP-44S', 'Head', 'Arquebus', 3080, 148, 'Mass-produced head part developed by Arquebus. A number of refinements and updates have been made to the strong foundation laid by the preceding model, creating a masterpiece in the realm of second-generation AC parts.'),
              (14, 'NACHTREIHER/44E', 'Head', 'Schneider', 2320, 210, 'Lightweight head part developed by Schneider. Schneider is a specialist in aerodynamic research, and this model reflects their experience with a light but highly stable build.'),
              (15, 'KASUAR/44Z', 'Head', 'Schneider', 2590, 254, 'Expanded head part developed by Schneider. This model further improves on stability but with a higher energy burden, resulting in excellent performance in aerial combat.'),
              (16, 'HD-012 MELANDER C3', 'Head', 'Balam', 3300, 165, 'Custom head part developed by Balam. Altered to improve combat suitability, the revisions to this model include partial armor plating and the addition of a scanner module.'),
              (17, 'HD-011 MELANDER', 'Head', 'Balam', 3160, 135, 'Medium-weight head part developed by Balam. The simple design and solid performance of this model make it suited for mass production—reflecting Balams strategy of overwhelming its enemies with its material superiority.'),
              (18, 'HC-3000 WRECKER', 'Head', 'RaD', 3800, 102, 'Head part for construction ACs developed by RaD. Specced for demolition work, this model makes up for combat performance shortcomings with its sturdiness and outstanding defensive performance.'),
              (19, 'HC-2000 FINDER EYE', 'Head', 'RaD', 2670, 125, 'Head part for scout ACs developed by RaD. Originally specced for surveying terrain, this model makes up for what it lacks in combat performance with a light energy footprint and commendable ease of use.'),
              (20, 'EL-TH-10 FIRMEZA', 'Head', 'Elcano', 2570, 134, 'Lightweight head part developed by Elcano. In keeping with Elcanos roots in producing and forging steel, this model exhibits craftsman-like flair, being light while providing reliable defenses.'),
              (21, 'AH-J-124 BASHO', 'Head', 'BAWS', 4600, 95, 'Head part developed by BAWS for an old-generation AC. Said AC was one of the earliest models, developed to succeed MT-class machines, and modern fans for such classic hardware are fond of its characteristic bulk.'),
              (22, 'DF-HD-08 TIAN-QIANG', 'Head', 'BAWS', 1230, 88, 'Head part developed by Dafeng Core Industries for the heavyweight TIAN-QIANG AC. Incorporates only the most essential functionality with a minimalist build in keeping with Dafengs "stout tree, slender branches philosophy.'),

              (23, 'IB-C03C: HAL 826', 'Core', 'Rubicon Research Institute', 18520, 366, 'Core part for the HAL 826 piloted AC, developed long ago by the Rubicon Research Institute. The last of the Ibis Series and the only piloted Ibis craft, if was built to be the final safety valve to prevent Coral Collapse.'),
              (24, 'IA-C01C: EPHEMERA', 'Core', 'Rubicon Research Institute', 13200, 412, 'Core part for the EPHEMERA unpiloted ACs, developed long ago by the Rubicon Research Institute. An old development quirk allows for piloted operation, but the core box makes only perfunctory concessions for a human occupant.'),
              (25, '07-061 MIND ALPHA', 'Core', 'ALLMIND', 16510, 364, 'Core part developed by ALLMIND for model ACs. Designed as part of a research project to extend human sensory capabilities, with numerous optimizations to create an AC that, to the pilot, feels like an extension of the body.'),
              (26, 'CS-5000 MAIN DISH', 'Core', 'RaD', 23600, 413, 'Core part for a combat AC developed by RaD. though it was assembled from a patchwork of reclaimed resources, RaD mobilized its entire engineering team to fine-tune its design for formidable performance.'),
              (27, 'AC-J-120/RC JAILBREAK', 'Core', 'BAWS', 12350, 300, 'Junk. Originally a core part for an old-generation AC developed by BAWS. RaD engineers infiltrated Institute City to make field repairs—just enough to make this part operable, but not enough to fix its weathered armor.'),
              (28, 'EL-PC-00 ALBA', 'Core', 'Elcano', 12000, 315, 'A new core part developed by Elcano. This model utilizes technological insights derived from analysing Schneider ACs to achieve improved overall balance and high suitability for aerial combat'),
              (29, 'VE-40A', 'Core', 'Arquebus ADD', 21100, 432, 'Heavyweight core part designed by Arquebus ADD. Incorporates cutting-edge technology to enable defiance of the PCA. This model features excellent generator output adjustment and solid defense against damage of all kinds.'),
              (30, 'VP-40S', 'Core', 'Arquebus', 15030, 337, 'Mass-produced core part developed by Arquebus. A number of refinements and updates have been made to the strong foundation laid by the preceding model, creating a masterpiece in the realm second-generation AC parts.'),
              (31, 'NACHTREIHER/40E', 'Core', 'Schneider', 9820, 330, 'Lightweight core part developed by Schneider. Schneider is a specialist in aerodynamic research, and this model reflects their experience with a light and highly agile build.'),
              (32, 'EL-TC-10 FIRMEZA', 'Core', 'Elcano', 10890, 351, 'Lightweight core part developed by Elcano. In keeping with Elcanos roots in producing and forging steel, this model exhibits craftsman-like flair, being light while providing reliable defenses.'),
              (33, 'DF-BD-08 TIAN-QIANG', 'Core', 'Dafeng Core Industries', 20650, 388, 'Core part developed by Dafeng Core Industries for the heavyweight TIAN-QIANG AC. This is the "trunk" in Dafengs "stout tree, slender branches philosophy; a defensive foundation with extremely heavy, sturdy armor.'),
              (34, 'CC-3000 WRECKER', 'Core', 'RaD', 19000, 310, 'Core part for construction ACs developed by RaD. Specced for demolition work, this model make up for combat performance shortcomings with its sturdiness and outstanding physical defences.'),
              (35, 'BD-012 MELANDER C3', 'Core', 'Balam', 14050, 322, 'Custom core part developed by Balam. Altered to improve combat suitability, this model features a lighter basic frame enhanced with partial armor plating to maintain a modest weight.'),
              (36, 'BD-011 MELANDER', 'Core', 'Balam', 15800, 304, 'Medium-weight core part developed by Balam. The simple design and solid performance of this model make it suited for mass production—reflecting Balams strategy of overwhelming its enemies with its material superiority.'),
              (37, 'AC-J-120 BASHO', 'Core', 'BAWS', 16100, 300, 'Core part developed by BAWS for an old-generation AC. Said AC was one of the earliest models, developed to succeed MT-class machines, and modern fans of such classic hardware are fond of its characteristic bulk.'),
              (38, 'CC-2000 ORBITER', 'Core', 'RaD', 12650, 267, 'Core part for scout ACs developed by RaD. Originally specced for extravehicular activity in space, this model makes up for what it lacks in combat performance with a light energy footprint and commendable ease of use.'),

              (39, 'VP-46D', 'Arms', 'Arquebus', 10990, 248, 'Arm parts developed by Arquebus, derived from an existing model. Engineered in anticipation of regular use by the Vespers, this model features further improvements to performance.'),
              (40, 'IA-C01A: EPHEMERA', 'Arms', 'Rubicon Research Institute', 12700, 312, 'Arm parts for the EPHEMERA unpiloted ACs, developed long ago by the Rubicon Research Institute. An old development quirk allows for piloted operation, albeit with actuation translation that outstrips the capability of human nerves.'),
              (41, 'AS-5000 SALAD', 'Arms', 'RaD', 20940, 356, 'Arm parts for a combat AC developed by RaD. though it was assembled from a patchwork of reclaimed resources, RaD mobilized its entire engineering team to fine-tune its design for formidable performance.'),
              (42, 'AA-J-123/RC JAILBREAK', 'Arms', 'BAWS', 8480, 210, 'Junk. Originally arm parts for an old-generation AC developed by BAWS. RaD engineers infiltrated Institute City to make field repairs—just enough to make this part operable, but not enough to fix its weathered armor.'),
              (43, 'VE-46A', 'Arms', 'Arquebus ADD', 22210, 380, 'Heavyweight arm parts designed by Arquebus ADD. Incorporates cutting-edge technology to enable defiance of the PCA. This models distinctive curved armor plating proved solid defence against damage of all kinds.'),
              (44, 'VP-46S', 'Arms', 'Arquebus', 14020, 278, 'Mass-produced arm parts developed by Arquebus. A number of refinements and updates have been made to the strong foundation laid by the preceding model, creating a masterpiece in the realm of second-generation AC parts.'),
              (45, 'NACHTREIHER/46E', 'Arms', 'Schneider', 11420, 302, 'Lightweight arm parts developed by Schneider. Schneider is a specialist in aerodynamic research, and this model reflects their experience with a light and highly agile build.'),
              (46, 'EL-TA-10 FIRMEZA', 'Arms', 'Elcano', 11220, 270, 'Lightweight arm parts developed by Elcano. In keeping with Elcanos roots in producing and forging steel, this model exhibits craftsman-like flair, being light while providing dependable carrying capacity.'),
              (47, 'DF-AR-09 TIAN-LAO', 'Arms', 'Dafeng Core Industries', 26740, 266, 'Revised arm parts developed by Dafeng Core Industries. This model attempts to further refine Dafengs (stout tree, slender branches) philosophy by enhancing the durability of the armor plating around the shoulders.'),
              (48, 'DF-AR-08 TIAN-QIANG', 'Arms', 'Dafeng Core Industries', 20020, 295, 'Arm parts developed by Dafeng Core Industries for the heavyweight TIAN-QIANG AC. Built to embody Dafengs (stout tree, slender branches) philosophy, their weight is balanced by heavy upper arms and lighter forearms.'),
              (49, 'AR-012 MELANDER C3', 'Arms', 'Balam', 12300, 232, 'Custom arm parts developed by Balam. Altered to improve combat suitability, this model features a lighter basic frame while also enhancing arm maneuverability.'),
              (50, 'AC-3000 WRECKER', 'Arms', 'RaD', 14650, 220, 'Arm parts for construction ACs developed by RaD. Specced for demolition work, this model make up for combat performance shortcomings with its sturdiness and excellent recoil control.'),
              (51, 'AC-2000 TOOL ARM', 'Arms', 'Balam', 11300, 216, 'Arm parts for scout ACs developed by RaD. Originally specced for recovering scrap, this model makes up for what it lacks in combat performance with a light energy footprint and commendable ease of use.'),
              (52, 'AA-J-123 BASHO', 'Arms', 'BAWS', 10480, 210, 'Arm parts developed by BAWS for an old-generation AC. Said AC was one of the earliest models, developed to succeed MT-class machines, and modern fans of such classic hardware are fond of its characteristic bulk.'),
              (53, '04-101 MIND ALPHA', 'Arms', 'ALLMIND', 16960, 358, 'Arm parts developed by ALLMIND for model ACs. Designed as part of a research project to extend human sensory capabilities, with numerous optimizations to create an AC that, to the pilot, feels like an extension of the body.'),
              (54, 'AR-011 MELANDER', 'Arms', 'Balam', 13650, 265, 'Medium-weight arm parts developed by Balam. The simple design and solid performance of this model make it suited for mass production—reflecting Balams strategy of overwhelming its enemies with its material superiority.'),              
              
              (55, 'VE-42B', 'Legs', 'Arquebus ADD', 46600, 824, 'Special tank parts designed by Arquebus ADD. Prioritizes hovering performance and forward propulsion to focus on aerial combat. During development, the specs were stolen and leaked by an independent mercenary.'),
              (56, 'AL-J-121/RC JAILBREAK', 'Legs', 'BAWS', 18560, 300, 'Junk. Originally bipedal leg parts for an old-generation AC developed by BAWS. RaD engineers infiltrated Institute City to make field repairs—just enough to make this part operable, but not enough to fix its weathered armor.'),
              (57, 'IA-C01L: EPHEMERA', 'Legs', 'Rubicon Research Institute', 15200, 398, 'Bipedal legs for EPHEMERA unpiloted ACs, developed long ago by the Rubicon Research Institute. An old development quirk allows for piloted operation, albeit with actuation translation that outstrips the capability of human nerves.'),
              (58, '06-041 MIND ALPHA', 'Legs', 'ALLMIND', 22110, 432, 'Bipedal legs developed by ALLMIND for model ACs. Designed as part of a research project to extend human sensory capabilities, with numerous optimization to create an AC that, to the pilot, feels like an extension of the body.'),
              (59, 'EL-TL-11 FORTALEZA', 'Legs', 'Elcano', 24650, 620, 'Lightweight tank parts developed by Elcano. Inspired by wheelchairs made for competitive sports, this product was an instant success with soldier who had lost the use of their legs in combat but still pined for the battlefield.'),
              (60, 'VE-42A', 'Legs', 'Arquebus ADD', 28950, 465, 'Heavyweight bipedal leg parts designed by Arquebus ADD. Incorporates cutting-edge technology to enable defiance of the PCA. This model utilizes hover movement or increased loading capacity and greatly improved stability.'),
              (61, 'AL-J-121 BASHO', 'Legs', 'BAWS', 20520, 300, 'Bipedal legs developed by BAWS for an old-generation AC. Said AC was one of the earliest models, developed to succeed MT-class machines, and moderns fans of such classic hardware are fond of its characteristic bulk.'),
              (62, 'VP-422', 'Legs', 'Arquebus', 17900, 387, 'Mass-produced bipedal leg parts developed by Arquebus. A number of refinements and updates have been made to the strong foundation laid by the preceding model, creating a masterpiece in the realm of second-generation AC parts.'),
              (63, 'LG-011 MELANDER', 'Legs', 'Balam', 18700, 365, 'Medium-weight bipedal leg parts developed by Balam. The simple design and solid performance of this model make it suited for mass production—reflecting Balams strategy of overwhelming its enemies with its material superiority.'),
              (64, '2S-5000 DESSERT', 'Legs', 'RaD', 25880, 420, 'Bipedal leg parts for a combat AC developed by RaD. though it was assembled from a patchwork of reclaimed resources, RaD mobilized its entire engineering team to fine-tune its design for formidable performance.'),
              (65, 'LG-022T BORNEMISSZA', 'Legs', 'Balam', 49800, 455, 'Heavyweight tank parts developed by Balam. Designed with the simple goal of turning ACs into tanks capable of carrying the heavy weapons manufactured by Dafeng Core Industries.'),
              (66, 'LG-033M VERRILL', 'Legs', 'Balam', 36200, 675, 'Tetrapod leg option developed by Balam. The design division was all but held at gunpoint to produce a model that satisfied the Redguns demand for a highly mobile AC platform also capable of supporting heavy weaponry.'),
              (67, 'NACHTREIHER/42E', 'Legs', 'Schneider', 14030, 462, 'Lightweight bipedal leg parts developed by Schneider. Schneider is a specialist in aerodynamic research, and this model reflects their experience with a light and highly agile build.'),
              (68, 'LG-012 MELANDER C3', 'Legs', 'Balam', 17210, 355, 'Custom bipedal leg parts developed by Balam. Altered to improve combat suitability, this model features a lighter basic frame enhanced with partial armor plating to maintain a modest weight.'),
              (69, 'VP-424', 'Legs', 'Arquebus', 31600, 760, 'Tetrapod leg parts developed by Arquebus, derived from an existing model. Intended for tetrapods deployed along-side Arquebuss bipedal and reverse-joint ACs, this model focuses on mobility to enable hovering-based fire support.'),
              (70, '06-042 MIND BETA', 'Legs', 'ALLMIND', 22000, 426, 'Alternative reverse-joint legs developed by ALLMIND. Marking a new approach, this part explores changes in human sensory perception though introduction of alien elements; in this case, animal-like digitigrade legs.'),
              (71, 'RC-2000 SPRING CHICKEN', 'Legs', 'RaD', 25890, 402, 'Heavyweight reverse-joint legs for scout ACs developed by RaD. Originally specced for resource transportation rather than combat, these legs are capable of leaping up to high positions while supporting a significant weight burden.'),
              (72, 'KASUAR/42Z', 'Legs', 'Schneider', 19060, 388, 'Lightweight reverse-joint legs developed by Schneider. These legs sacrifice stability and defensive performance to provide exceptional jumping performance, enabling agile transitions to aerial combat—as is Schneiders forte'),
              (73, 'EL-TL-10 FIRMEZA', 'Legs', 'Elcano', 11200, 378, 'Lightweight bipedal leg parts developed by Elcano. In keeping with Elcanos roots in producing and forging steel, this model exhibits craftsman-like flair, being light yet retaining high load capacity.'),
              (74, '2C-3000 WRECKER', 'Legs', 'RaD', 21680, 680, 'Bipedal leg parts for construction ACs developed by RaD. Specced for demolition work, this model make up for combat performance shortcomings with its sturdiness and outstanding loading capacity.'),
              (75, '2C-2000 CRAWLER', 'Legs', 'RaD', 16300, 280, 'Bipedal legs for scout ACs developed by RaD. Originally specced for surface surveys of astronomical objects, this model makes up for what it lacks in combat performance with a light energy footprint and commendable ease of use.'),
              (76, 'DF-LG-08 TIAN-QIANG', 'Legs', 'Dafeng Core Industries', 23600, 400, 'Bipdedal legs developed by Dafeng Core Industries for the heavyweight TIAN-QIANG AC. Built to embody Dafengs "stout tree, slender branches" philosophy, their weight is balanced by heavy upper legs and lighter lower legs.'),
              
              (77, 'BC-0400 MULE', 'Booster', 'RaD', 970, 200, 'Booster developed by RaD for heavyweight machines. Designed for heavy-industry ACs primarily working on the ground, it suffers from a slow vertical boost but boasts excellent energy efficiency.'),
              (78, 'Test_78', 'Booster', 'RaD', 0, 0, '0'),
              (79, 'Test_79', 'Booster', 'RaD', 0, 0, '0'),
              (80, 'Test_80', 'Booster', 'RaD', 0, 0, '0'),
              (81, 'Test_81', 'Booster', 'RaD', 0, 0, '0'),
              (82, 'Test_82', 'Booster', 'RaD', 0, 0, '0'),
              (83, 'Test_83', 'Booster', 'RaD', 0, 0, '0'),
              (84, 'Test_84', 'Booster', 'RaD', 0, 0, '0'),
              (85, 'Test_85', 'Booster', 'RaD', 0, 0, '0'),

              (86, 'VE-21B', 'FCS', 'Arquebus ADD', 160, 388, 'Long-range combat FCS designed by Arquebus ADD. Retains ADDs earlier focus of obliterating targets at range, while also improving missile performance across the board to enable a "walking fortress" style of AC.'),
              (87, 'Test_87', 'FCS', 'RaD', 0, 0, '0'),
              (88, 'Test_88', 'FCS', 'RaD', 0, 0, '0'),
              (89, 'Test_89', 'FCS', 'RaD', 0, 0, '0'),
              (90, 'Test_90', 'FCS', 'RaD', 0, 0, '0'),
              (91, 'Test_91', 'FCS', 'RaD', 0, 0, '0'),
              (92, 'Test_92', 'FCS', 'RaD', 0, 0, '0'),
              (93, 'Test_93', 'FCS', 'RaD', 0, 0, '0'),
              (94, 'Test_94', 'FCS', 'RaD', 0, 0, '0'),

              (95, 'VE-20C', 'Generator', 'Arquebus ADD', 10130, 4090, 'Circulating-current generator developed by Arquebus ADD. Features improved EN capacity and output while retaining a focus on energy weapon stabilization. However, it suffers from a heavy weight burden and recharging difficulties.'),
              (96, 'Test_96', 'Generator', 'RaD', 0, 0, '0'),
              (97, 'Test_97', 'Generator', 'RaD', 0, 0, '0'),
              (98, 'Test_98', 'Generator', 'RaD', 0, 0, '0'),
              (99, 'Test_99', 'Generator', 'RaD', 0, 0, '0'),
              (100, 'Test_100', 'Generator', 'RaD', 0, 0, '0'),
              (101, 'Test_101', 'Generator', 'RaD', 0, 0, '0'),
              (102, 'Test_102', 'Generator', 'RaD', 0, 0, '0'),
              (103, 'Test_103', 'Generator', 'RaD', 0, 0, '0'),
              (104, 'Test_104', 'Generator', 'RaD', 0, 0, '0'),
              (105, 'Test_105', 'Generator', 'RaD', 0, 0, '0'),
              (106, 'Test_106', 'Generator', 'RaD', 0, 0, '0')]
c.executemany("INSERT INTO parts (id, name, category, manufacturer, weight, en_load, description) VALUES (?, ?, ?, ?, ?, ?, ?)", parts_data)
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

                    (23, 3670, 451, 469, 463, 385),
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

                    (39, 1620, 196, 230, 190, 0),
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

                    (55, 8600, 379, 460, 415, 924),
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

arm_stats_data = [(39, 11800, 70, 133, 117),
                  (40, 12680, 98, 104, 106),
                  (41, 18700, 130, 88, 80),
                  (42, 10520, 45, 45, 112),
                  (43, 21300, 160, 80, 76),
                  (44, 14520, 106, 102, 92),
                  (45, 12730, 52, 160, 95),
                  (46, 13540, 86, 122, 110),
                  (47, 17200, 135, 95, 68),
                  (48, 19500, 145, 92, 84),
                  (49, 12000, 92, 128, 102),
                  (50, 15800, 232, 26, 13),
                  (51, 13300, 90, 96, 100),
                  (52, 10520, 66, 53, 158),
                  (53, 15550, 132, 103, 79),
                  (54, 15100, 107, 100, 96)]
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

booster_stats_data = [(77, 5417, 4434, 405, 17500, 0.46, 670, 0.58, 80000, 7584, 381, 7018, 390),
                      (78, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                      (79, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                      (80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                      (81, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                      (82, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                      (83, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                      (84, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                      (85, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
c.executemany("INSERT INTO booster_stats (booster_id, thrust, upward_thrust, upward_en_consumption, qb_thrust, qb_jet_duration, qb_en_consumption, qb_reload_time, qb_reload_ideal_weight, ab_thrust, ab_en_consumption, melee_attack_thrust, melee_attack_en_consumption) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", booster_stats_data)
conn.commit()

fcs_stats_data = [(86, 15, 50, 80, 97, 70), 
                  (87, 0, 0, 0, 0, 0), 
                  (88, 0, 0, 0, 0, 0), 
                  (89, 0, 0, 0, 0, 0), 
                  (90, 0, 0, 0, 0, 0), 
                  (91, 0, 0, 0, 0, 0), 
                  (92, 0, 0, 0, 0, 0), 
                  (93, 0, 0, 0, 0, 0), 
                  (94, 0, 0, 0, 0, 0)]
c.executemany("INSERT INTO fcs_stats (fcs_id, close_assist, medium_assist, long_assist, missile_lock_correction, multi_lock_correction) VALUES (?, ?, ?, ?, ?, ?)", fcs_stats_data)
conn.commit()


generator_stats_data = [(95, 3690, 555, 377, 720, 128),
                        (96, 0, 0, 0, 0, 0),
                        (97, 0, 0, 0, 0, 0),
                        (98, 0, 0, 0, 0, 0),
                        (99, 0, 0, 0, 0, 0),
                        (100, 0, 0, 0, 0, 0),
                        (101, 0, 0, 0, 0, 0),
                        (102, 0, 0, 0, 0, 0),
                        (103, 0, 0, 0, 0, 0),
                        (104, 0, 0, 0, 0, 0),
                        (105, 0, 0, 0, 0, 0),
                        (106, 0, 0, 0, 0, 0),]
c.executemany("INSERT INTO generator_stats (generator_id, en_capacity, en_recharge, supply_recovery, post_recovery_en_supply, en_output) VALUES (?, ?, ?, ?, ?, ?)", generator_stats_data)
conn.commit()

ac_build_data = [(1, 'Test Build', 1, 23, 39, 55, 77, 86, 95)]
c.executemany("INSERT INTO ac_build (build_id, build_name, head_id, core_id, arms_id, legs_id, booster_id, fcs_id, generator_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", ac_build_data)
conn.commit()

# Создание пердставлений полных статов деталей
c.execute('''CREATE VIEW IF NOT EXISTS full_head_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.weight, p.en_load, p.description,
          fs.ap, fs.anti_kinetic, fs.anti_energy, fs.anti_explosive, fs.attitude_stability,
          hs.system_recovery, hs.scan_distance, hs.scan_duration
          FROM parts AS p
          JOIN frame_stats AS fs ON p.id = fs.frame_id
          JOIN head_stats AS hs ON fs.frame_id = hs.head_id
''')

c.execute('''CREATE VIEW IF NOT EXISTS full_core_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.weight, p.en_load, p.description,
          fs.ap, fs.anti_kinetic, fs.anti_energy, fs.anti_explosive, fs.attitude_stability,
          cs.booster_efficiency_adj, cs.generator_output_adj, cs.generator_supply_adj
          FROM parts AS p
          JOIN frame_stats AS fs ON p.id = fs.frame_id
          JOIN core_stats AS cs ON fs.frame_id = cs.core_id
''')

c.execute('''CREATE VIEW IF NOT EXISTS full_arm_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.weight, p.en_load, p.description,
          fs.ap, fs.anti_kinetic, fs.anti_energy, fs.anti_explosive, fs.attitude_stability,
          rs.arms_load_limit, rs.recoil_control, rs.firearms_specialization, rs.melee_specialization
          FROM parts AS p
          JOIN frame_stats AS fs ON p.id = fs.frame_id
          JOIN arm_stats AS rs ON fs.frame_id = rs.arm_id
''')

c.execute('''CREATE VIEW IF NOT EXISTS full_leg_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.weight, p.en_load, p.description,
          fs.ap, fs.anti_kinetic, fs.anti_energy, fs.anti_explosive, fs.attitude_stability,
          ls.load_limit, ls.leg_type, ls.jump_distance, ls.jump_height
          FROM parts AS p
          JOIN frame_stats AS fs ON p.id = fs.frame_id
          JOIN leg_stats AS ls ON fs.frame_id = ls.leg_id
''')

c.execute('''CREATE VIEW IF NOT EXISTS full_booster_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.weight, p.en_load, p.description,
          bs.booster_id, bs.thrust, bs.upward_thrust, bs.upward_en_consumption, bs.qb_thrust, bs.qb_jet_duration, bs.qb_en_consumption, bs.qb_reload_time, bs.qb_reload_ideal_weight, bs.ab_thrust, bs.ab_en_consumption, bs.melee_attack_thrust, bs.melee_attack_en_consumption
          FROM parts AS p
          JOIN booster_stats AS bs ON p.id = bs.booster_id
''')

c.execute('''CREATE VIEW IF NOT EXISTS full_fcs_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.weight, p.en_load, p.description,
          fcs.fcs_id, fcs.close_assist, fcs.medium_assist, fcs.long_assist, fcs.missile_lock_correction, fcs.multi_lock_correction
          FROM parts AS p
          JOIN fcs_stats AS fcs ON p.id = fcs.fcs_id
''')

c.execute('''CREATE VIEW IF NOT EXISTS full_generator_stats AS
          SELECT p.id, p.name, p.category, p.manufacturer, p.weight, p.en_load, p.description,
          gs.generator_id, gs.en_capacity, gs.en_recharge, gs.supply_recovery, gs.post_recovery_en_supply, gs.en_output
          FROM parts AS p
          JOIN generator_stats AS gs ON p.id = gs.generator_id
''')

c.execute('''CREATE VIEW IF NOT EXISTS ac_build_specs AS
          SELECT b.build_id, b.build_name,

          p_h.name AS head_name,
          p_c.name AS core_name,
          p_a.name AS arms_name,
          p_l.name AS legs_name,
          p_bst.name AS booster_name,
          p_fcs.name AS fcs_name,
          p_gen.name AS generator_name,

          (IFNULL(p_h.weight, 0) + IFNULL(p_c.weight, 0) + IFNULL(p_a.weight, 0) + IFNULL(p_l.weight, 0) + IFNULL(p_bst.weight, 0) + IFNULL(p_fcs.weight, 0) + IFNULL(p_gen.weight, 0)) AS total_weight,
    
          (IFNULL(p_h.en_load, 0) + IFNULL(p_c.en_load, 0) + IFNULL(p_a.en_load, 0) + IFNULL(p_l.en_load, 0) + IFNULL(p_bst.en_load, 0) + IFNULL(p_fcs.en_load, 0) + IFNULL(p_gen.en_load, 0)) AS total_en_load,
    
          (IFNULL(f_h.ap, 0) + IFNULL(f_c.ap, 0) + IFNULL(f_a.ap, 0) + IFNULL(f_l.ap, 0)) AS total_ap,
          (IFNULL(f_h.anti_kinetic, 0) + IFNULL(f_c.anti_kinetic, 0) + IFNULL(f_a.anti_kinetic, 0) + IFNULL(f_l.anti_kinetic, 0)) AS total_anti_kinetic,
          (IFNULL(f_h.anti_energy, 0) + IFNULL(f_c.anti_energy, 0) + IFNULL(f_a.anti_energy, 0) + IFNULL(f_l.anti_energy, 0)) AS total_anti_energy,
          (IFNULL(f_h.anti_explosive, 0) + IFNULL(f_c.anti_explosive, 0) + IFNULL(f_a.anti_explosive, 0) + IFNULL(f_l.anti_explosive, 0)) AS total_anti_explosive,
          (IFNULL(f_h.attitude_stability, 0) + IFNULL(f_c.attitude_stability, 0) + IFNULL(f_a.attitude_stability, 0) + IFNULL(f_l.attitude_stability, 0)) AS total_attitude_stability,

          IFNULL(f_l_stats.load_limit, 0) AS legs_load_limit,
          IFNULL(f_a_stats.arms_load_limit, 0) AS arms_load_limit,
          IFNULL(g_stats.en_output, 0) AS generator_en_output,
          IFNULL(g_stats.en_capacity, 0) AS generator_en_capacity
                    
          FROM ac_build AS b

          LEFT JOIN parts p_h   ON b.head_id = p_h.id
          LEFT JOIN parts p_c   ON b.core_id = p_c.id
          LEFT JOIN parts p_a   ON b.arms_id = p_a.id
          LEFT JOIN parts p_l   ON b.legs_id = p_l.id
          LEFT JOIN parts p_bst ON b.booster_id = p_bst.id
          LEFT JOIN parts p_fcs ON b.fcs_id = p_fcs.id
          LEFT JOIN parts p_gen ON b.generator_id = p_gen.id

          LEFT JOIN frame_stats f_h ON b.head_id = f_h.frame_id
          LEFT JOIN frame_stats f_c ON b.core_id = f_c.frame_id
          LEFT JOIN frame_stats f_a ON b.arms_id = f_a.frame_id
          LEFT JOIN frame_stats f_l ON b.legs_id = f_l.frame_id

          LEFT JOIN leg_stats f_l_stats ON b.legs_id = f_l_stats.leg_id
          LEFT JOIN arm_stats f_a_stats ON b.arms_id = f_a_stats.arm_id
          LEFT JOIN generator_stats g_stats ON b.generator_id = g_stats.generator_id
''')


conn.close()