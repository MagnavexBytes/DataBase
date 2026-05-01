import pprint
import sqlite3
conn = sqlite3.connect('ACVI_Parts/ACVI_Parts.sqlite')
c = conn.cursor()
pp = pprint.PrettyPrinter(indent = 1, width = 160, compact = False) 
c.execute('''PRAGMA foreign_keys = ON''')


# Удаление таблиц целиком
c.execute('''DROP TABLE IF EXISTS expansion_stats''')
c.execute('''DROP TABLE IF EXISTS generator_stats''')
c.execute('''DROP TABLE IF EXISTS fcs_stats''')
c.execute('''DROP TABLE IF EXISTS booster_stats''')
c.execute('''DROP TABLE IF EXISTS leg_stats''')
c.execute('''DROP TABLE IF EXISTS arm_stats''')
c.execute('''DROP TABLE IF EXISTS core_stats''')
c.execute('''DROP TABLE IF EXISTS head_stats''')
c.execute('''DROP TABLE IF EXISTS frame_stats''')
c.execute('''DROP TABLE IF EXISTS weapon_stats''')
c.execute('''DROP TABLE IF EXISTS parts''')


# Таблицы
# Таблица характеристик, присутствующих у всех деталей
c.execute('''CREATE TABLE IF NOT EXISTS parts (
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL UNIQUE,
          category TEXT NOT NULL, -- ДОБАВИТЬ IN 'Head', 'Core', 'Arms', 'Legs', 'R-Arm', 'L-Arm', 'R-Back', 'L-Back', 'Booster', 'FCS', 'Generator', 'Expansion'
          manufacturer TEXT,
          price INTEGER,
          weight INTEGER,
          en_load INTEGER,
          description TEXT)
''')

# Таблица характеристик, присутствующих только у оружия
c.execute('''CREATE TABLE IF NOT EXISTS weapon_stats (
            part_id INTEGER PRIMARY KEY,
            attack_power INTEGER,
            impact INTEGER,
            damage_type TEXT, --ДОБАВИТЬ IN Kinetic, Energy, Explosion, Coral
            FOREIGN KEY (part_id) REFERENCES parts(id))
''')

# Промежуточная таблица характеристик, присутствующих у всех частей каркаса
c.execute('''CREATE TABLE IF NOT EXISTS frame_stats (
    part_id INTEGER PRIMARY KEY,
    ap INTEGER,
    anti_kinetic INTEGER,
    anti_energy INTEGER,
    anti_explosive INTEGER,
    attitude_stability INTEGER,
    -- system_recovery INTEGER,
    FOREIGN KEY (part_id) REFERENCES parts(id))
''')

# Таблица характеристик, присутствующих только у частей голов
c.execute('''CREATE TABLE head_stats (
    part_id INTEGER PRIMARY KEY,
    scan_distance INTEGER,
    scan_duration REAL,
    FOREIGN KEY (part_id) REFERENCES frame_stats(part_id))
''')

# Таблица характеристик, присутствующих только у частей корпуса
c.execute('''CREATE TABLE core_stats (
    part_id INTEGER PRIMARY KEY,
    booster_efficiency_adj INTEGER,
    generator_output_adj INTEGER,
    generator_supply_adj INTEGER,
    FOREIGN KEY (part_id) REFERENCES frame_stats(part_id))
''')

# Таблица характеристик, присутствующих только у частей рук
c.execute('''CREATE TABLE arm_stats (
    part_id INTEGER PRIMARY KEY,
    arms_load_limit INTEGER,
    recoil_control INTEGER,
    firearms_specialization INTEGER,
    melee_specialization INTEGER,
    FOREIGN KEY (part_id) REFERENCES frame_stats(part_id))
''')

# Таблица характеристик, характерных только для деталей ног
c.execute('''CREATE TABLE leg_stats (
    part_id INTEGER PRIMARY KEY,
    load_limit INTEGER,
    leg_type TEXT, -- ДОБАВИТЬ IN Bipedal, Reverse Joint, Tetrapod, Tank
    FOREIGN KEY (part_id) REFERENCES frame_stats(part_id))
''')

# Таблица характеристик, присутствующих только у частей ускорителей
c.execute('''CREATE TABLE booster_stats (
    part_id INTEGER PRIMARY KEY,
    thrust INTEGER,
    upward_thrust INTEGER,
    quick_boost_thrust INTEGER,
    quick_boost_en_consumption INTEGER,
    qb_reload_time REAL,
    melee_attack_thrust INTEGER,
    FOREIGN KEY (part_id) REFERENCES parts(id))
''')

# Таблица характеристик, присутствующих только у частей СУО
c.execute('''CREATE TABLE fcs_stats (
    part_id INTEGER PRIMARY KEY,
    close_assist INTEGER,   -- ДОБАВИТЬ CHECK > 130м
    medium_assist INTEGER,  -- ДОБАВИТЬ CHECK < 130м AND > 260м
    long_assist INTEGER,    -- ДОБАВИТЬ CHECK > 260м
    missile_lock_correction INTEGER,
    multi_lock_correction INTEGER,
    FOREIGN KEY (part_id) REFERENCES parts(id))
''')

# Таблица характеристик, присутствующих только у частей генератора
c.execute('''CREATE TABLE generator_stats (
    part_id INTEGER PRIMARY KEY,
    en_capacity INTEGER,
    en_recharge INTEGER,
    supply_recovery INTEGER,
    post_recovery_en_supply INTEGER,
    en_output INTEGER,
    FOREIGN KEY (part_id) REFERENCES parts(id))
''')

# Таблица характеристик, присутствующих только у частей расширений
c.execute('''CREATE TABLE expansion_stats (
    part_id INTEGER PRIMARY KEY,
    uses INTEGER,
    resilience INTEGER,
    duration REAL,
    FOREIGN KEY (part_id) REFERENCES parts(id))
''')


# Данные
parts_data = [(1, 'IB-C03H: HAL 826', 'Head', 'Rubicon Research Institute', 0, 3760, 215, 'Head part for the HAL 826 piloted AC, developed long ago by the Rubicon Research Institute. The last of the Ibis Series and the only piloted Obis craft, it was built to be the final safety valve to prevent a Coral Collapse.'),
              (2, '20-082 MIND BETA', 'Head', 'ALLMIND', 0, 3460, 128, 'Model head part developed by ALLMIND. In line with a change in approach, this part maximized stability at the expense of armor robustness.'),
              (3, '20-081 MIND ALPHA', 'Head', 'ALLMIND', 0, 3350, 142, 'Head part developed my ALLMIND for model ACs. Designed as part of a research project to extend human sensory capabilities, with numberous optimizations to create an AC that, to the pilot, feels like an extension of the body.'),
              (4, 'HC-2000/BC SHADE EYE', 'Head', 'RaD', 0, 3090, 163, 'Custom part derived from the scout AC head developed by RaD. Comprehensively rebuilt for combat by an anonymous independent mercenary group, this model takes some steps forward but sacrifices the minimalism of its predecessor.'),
              (5, 'VE-44A', 'Head', 'Arquebus ADD', 0, 3640, 182, 'Heavyweight head part designed by Arquebus ADD. Incoporates cutting-edge technology to enable defiance of the PCA. This models distinctive curved armor plating provides solid defense against damage of all kinds.'),
              (6, 'VP-44D', 'Head', 'Arquebus', 0, 3260, 177, 'Head part developed by Arquebus, derived from an existing model. Engineered in anticipation of regular use by the Vespers, this model features further improvements to stability.'),
              (7, 'HD-033M VERRILL', 'Head', 'Balam', 0, 3830, 240, 'Retrofitted head part developed by Balam. This high-end model is a strong performer with a hefty energy footprint, and features an intimidating spider-eye design chosen to suit the tastes of the Redguns commander.'),
              (8, 'AH-J-124/RC JAILBREAK', 'Head', 'BAWS', 0, 4250, 95, 'Junk. Originally a head part for an old-generation AC developed by BAWS. RaD engineers infiltrated Institute City to make field repairs—just enough to make this part operable, but not enough to fix its weathered armor.'),
              (9, 'HS-5000 APPETIZER', 'Head', 'RaD', 0, 3000, 103, 'Head part for a combat AC developed by RaD. though it was assembled from a patchwork of reclaimed resources, RaD mobilized its entire engineering team to fine-tune its design for formidable performance.'),
              (10, 'IA-C01H: EPHEMERA', 'Head', 'Rubicon Research Institute', 0, 4330, 235, 'Head part for the EPHEMERA unpiloted ACs, devloped long ago by the Rubicon Research Institute. An old development quirk allows for piloted operation, but one should not any concessions for the limit of human sight.'),
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
              (22, 'DF-HD-08 TIAN-QIANG', 'Dafeng Core Industries', 'BAWS', 0, 1230, 88, 'Head part developed by Dafeng Core Industries for the heavyweight TIAN-QIANG AC. Incorporates only the most essential functionality with a minimalist build in keeping with Dafengs "stout tree, slender branches philosophy.'),

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

              (39, 'LG-011 MELANDER', 'Arms', 'Balam', 0, 16200, 180),

              (40, 'LG-011 MELANDER', 'Legs', 'Balam', 0, 16200, 180),

              (40, 'RF-024 TURNER', 'R-Arm', 'Balam', 0, 3620, 140),

              (50, 'BST-G1/P10', 'Booster', 'Furlong', 0, 1440, 220),

              (50, 'BST-G1/P10', 'Expansion', '', 0, 1440, 220),

              (60, 'VP-20S', 'Generator', 'Arquebus', 0, 3420, 0)]
c.executemany("INSERT OR IGNORE INTO parts (id, name, category, manufacturer, price, weight, en_load) VALUES (?, ?, ?, ?, ?, ?, ?)", parts_data)
conn.commit()

frame_stats_data = [(1, 380, 110, 80, 95, 120),
                    (2, 2850, 420, 380, 410, 450),
                    (3, 1450, 280, 240, 260, 350)]
c.executemany("INSERT OR IGNORE INTO frame_stats (part_id, ap, anti_kinetic, anti_energy, anti_explosive, attitude_stability) VALUES (?, ?, ?, ?, ?, ?)", frame_stats_data)
conn.commit()

head_stats_data = [(1, 450, 3.5)]
c.executemany("INSERT OR IGNORE INTO head_stats (part_id, scan_distance, scan_duration) VALUES (?, ?, ?)", head_stats_data)
conn.commit()

leg_stats_data = [(3, 52000, 'Bipedal')]
c.executemany("INSERT OR IGNORE INTO leg_stats (part_id, load_limit, leg_type) VALUES (?, ?, ?)", leg_stats_data)
conn.commit()

weapon_stats_data = [(4, 135, 110, 'Kinetic')]
c.executemany("INSERT OR IGNORE INTO weapon_stats (part_id, attack_power, impact, damage_type) VALUES (?, ?, ?, ?)", weapon_stats_data)
conn.commit()

booster_stats_data = [(5, 4800, 3200, 12500)]
c.executemany("INSERT OR IGNORE INTO booster_stats (part_id, thrust, upward_thrust, quick_boost_thrust) VALUES (?, ?, ?, ?)", booster_stats_data)
conn.commit()

generator_stats_data = [(6, 2620, 892, 434, 1200, 3400)]
c.executemany("INSERT OR IGNORE INTO generator_stats (part_id, en_capacity, en_recharge, supply_recovery, post_recovery_en_supply, en_output) VALUES (?, ?, ?, ?, ?, ?)", generator_stats_data)
conn.commit()


conn.close()