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
    en_load INTEGER)
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
parts_data = [(1, 'HC-2000 FINDER EYE', 'Head', 'RaD', 12000, 1420, 110),
              (2, 'CC-2000 ORBITER', 'Core', 'RaD', 18000, 15300, 242),
              (3, 'LG-011 MELANDER', 'Legs', 'Balam', 45000, 16200, 180),
              (4, 'RF-024 TURNER', 'R-Arm', 'Balam', 35000, 3620, 140),
              (5, 'BST-G1/P10', 'Booster', 'Furlong', 22000, 1440, 220),
              (6, 'VP-20S', 'Generator', 'Arquebus', 32000, 3420, 0)]
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