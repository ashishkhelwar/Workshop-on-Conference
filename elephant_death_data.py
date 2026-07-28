#!/usr/bin/env python3
"""
Structured dataset transcribed & translated from two official Chhattisgarh
Forest Department registers:
  1) Dharamjaigarh Forest Division — Elephant Deaths 2020–2026 (calendar year)
  2) Raigarh Forest Division — Last Five Years Elephant Death (financial year)
District: Raigarh (C.G.)

Each record = one dead elephant. Multi-death incidents are split into rows.
"""

# age_class from numeric age (years). None age → class given explicitly.
def age_class(age):
    if age is None: return None
    if age < 0.09: return 'Newborn (<1 mo)'
    if age < 1:    return 'Calf (<1 yr)'
    if age < 5:    return 'Juvenile (1–5 yr)'
    if age < 15:   return 'Sub-adult (5–15 yr)'
    return 'Adult (>15 yr)'

# cause groups (standardised)
ELEC='Electrocution'; DROWN='Drowning / water body'; DISEASE='Disease (infectious)'
LIGHT='Lightning (vajrapat)'; FALL='Fall / difficult terrain'; OLDAGE='Old age / natural'
FIGHT='Inter-elephant fight'; BIRTH='Birth / newborn complication'; HEAT='Heat stroke'
INJURY='Injury (fall in nala/brain)'; WEAK='Weakness/emaciation'; TRAIN='Train hit'

# Records: (division, date_iso, cyear, range, location, cause_group, cause_detail,
#           nat_unnat, sex, age_years, age_cls_override, legal_action, pm_lab)
R = []
def add(div, date, cy, rng, loc, cg, cd, nu, sex, age, cls, action, pmlab):
    R.append(dict(division=div, date=date, cyear=cy, range=rng, location=loc,
                  cause_group=cg, cause_detail=cd, nat=nu, sex=sex,
                  age=age, age_class=cls or age_class(age),
                  action=action, pmlab=pmlab))

D='Dharamjaigarh'
add(D,'2020-06-16',2020,'Dharamjaigarh','Gersa / Sararkhar (revenue land)',ELEC,'Electric current — illegal live wire','Unnatural','M',12,None,'Yes (accused named)','PM')
add(D,'2020-06-18',2020,'Chhal','Beharamar / Kokhikhar',ELEC,'Electric current — illegal live wire','Unnatural','M',37,'Adult (>15 yr)','Yes (accused named)','PM')
add(D,'2020-09-23',2020,'Dharamjaigarh','Taraimar / Medhrmar (private farmland)',ELEC,'Electric current — illegal live wire','Unnatural','M',30,None,'Yes (accused named)','PM')
add(D,'2021-03-29',2021,'Boro','Thekurajam / Sangapani',FALL,'Fell from hill','Natural','M',18,None,'No','PM')
add(D,'2021-06-22',2021,'Chhal','Banhar',ELEC,'Electric current — illegal live wire','Unnatural','F',15,'Sub-adult (5–15 yr)','Yes (accused named)','PM')
add(D,'2021-08-14',2021,'Boro','Hinjhar',OLDAGE,'Natural death','Natural','F',52,None,'No','PM')
add(D,'2021-08-22',2021,'Dharamjaigarh','Potiya / Dariinala',ELEC,'Electric current — illegal live wire','Unnatural','M',16,None,'Yes (accused named)','PM')
add(D,'2022-02-04',2022,'Lailunga','Bhalumada / Sonajori',FALL,'Fell backward from hill','Natural','F',42,None,'No','PM')
add(D,'2022-07-31',2022,'Chhal','Singhigadai / Hati',LIGHT,'Lightning strike','Natural','M',41,None,'No','PM')
add(D,'2022-09-26',2022,'Bakaruma','Jamabira',LIGHT,'Lightning strike','Natural','F',45,None,'No','PM')
add(D,'2022-10-14',2022,'Chhal','Khenta Bahri / Hati',ELEC,'Electric current — illegal live wire','Unnatural','M',20,None,'Yes (3 accused)','PM')
add(D,'2022-11-22',2022,'Dharamjaigarh','Potiya / Jamghat',FALL,'Old age; slipped from steep hill','Natural','M',62,None,'No','PM')
add(D,'2023-01-10',2023,'Dharamjaigarh','Gersa / Baigin Jharia',ELEC,'Electric current — illegal live wire','Unnatural','M',75,None,'Yes (3 accused)','PM')
add(D,'2023-02-04',2023,'Dharamjaigarh','Gersa',OLDAGE,'Old age','Natural','F',75,None,'No','PM')
add(D,'2023-04-17',2023,'Chhal','Banhar / Chuhkimar (groundnut field)',ELEC,'Electric current — illegal live wire','Unnatural','M',5,None,'Yes (accused named)','PM')
add(D,'2023-06-15',2023,'Chhal','Puranga / Chaukdhoda',FIGHT,'Injury (internal & external) in inter-elephant fight','Natural','M',1,None,'No','PM')
add(D,'2023-09-10',2023,'Dharamjaigarh','Baysi / Samarfudga',ELEC,'Electric current — illegal live wire','Unnatural','M',45,None,'Yes (accused named)','PM')
add(D,'2023-10-11',2023,'Dharamjaigarh','Baysi / Tahdand',ELEC,'Electrocution under 11 kV line (accidental)','Unnatural','M',50,None,'No','PM')
add(D,'2023-10-23',2023,'Chhal','Beharamar / Marghatipatra',ELEC,'Electric current — illegal live wire','Unnatural','F',42,None,'Yes (4 accused)','PM')
add(D,'2023-12-20',2023,'Boro','Khamhar / Junapara',ELEC,'Electric current — illegal live wire','Unnatural','M',15,'Sub-adult (5–15 yr)','Yes (2 accused)','PM')
add(D,'2024-09-03',2024,'Chhal','Kida / Kajubari Nawanar',BIRTH,'Newborn died during birth','Natural','U',0.0,'Newborn (<1 mo)','No','PM')
add(D,'2024-11-17',2024,'Boro','Rwaqul / Pradhanjharia',BIRTH,'Newborn; fell on sharp stump during movement','Natural','U',0.05,'Newborn (<1 mo)','No','PM')
add(D,'2024-11-21',2024,'Chhal','Hati / Hathimuda',DROWN,'Drowned in department-built pond','Natural','U',0.05,'Newborn (<1 mo)','No','PM')
add(D,'2025-01-21',2025,'Dharamjaigarh','Kraundha 451 PF (revenue land)',ELEC,'Electric current','Unnatural','M',10,None,'Yes (accused named)','PM')
add(D,'2025-01-31',2025,'Dharamjaigarh','Beharamar 572 RF',OLDAGE,'Natural death','Natural','M',60,None,'No','PM')
add(D,'2025-03-18',2025,'Chhal','Puranga / Jampali / Chitamada',DROWN,'Drowned in pond','Natural','F',None,'Calf (<1 yr)','No','PM')
add(D,'2025-10-28',2025,'Chhal','Auranara / Saraimuda pond',DROWN,'Drowned in pond','Natural','F',None,'Calf (<1 yr)','No','PM')
add(D,'2026-04-22',2026,'Lailunga','Amapali',DISEASE,'Acute serohaemorrhagic pneumonia','Natural','M',0.08,'Newborn (<1 mo)','No','PM+Lab')
add(D,'2026-05-08',2026,'Chhal','Singhijhap / Ghoghra Dam',DISEASE,'Acute hepatitis of bacterial origin','Natural','M',0.5,'Calf (<1 yr)','No','PM+Lab')
add(D,'2026-05-11',2026,'Chhal','Chhal / Kera Jharia dam',DISEASE,'Bacterial septicaemia','Natural','M',0.46,'Calf (<1 yr)','No','PM+Lab')
add(D,'2026-05-24',2026,'Chhal','Edu / Amabada pond',DROWN,'Calf drowned','Natural','M',1.75,None,'No','PM+Lab')

G='Raigarh'
add(G,'2022-06-12',2022,'Gharghoda','Chimtapani',HEAT,'Heat stroke (loo)','Natural','U',0.125,'Calf (<1 yr)','No','PM')
add(G,'2022-11-20',2022,'Gharghoda','Amlidih',ELEC,'Electric current','Unnatural','F',11,None,'—','PM')
add(G,'2022-12-09',2022,'Gharghoda','Pusalda',ELEC,'Electric current','Unnatural','F',1,None,'—','PM')
add(G,'2024-10-26',2024,'Tamnar','Kachkoba',ELEC,'Electric current','Unnatural','F',2.5,None,'—','PM+Lab')
add(G,'2024-10-26',2024,'Tamnar','Kachkoba',ELEC,'Electric current','Unnatural','F',55,None,'—','PM+Lab')
add(G,'2024-10-26',2024,'Tamnar','Kachkoba',ELEC,'Electric current (makhna/tuskless bull)','Unnatural','M',65,None,'—','PM+Lab')
add(G,'2024-12-31',2024,'Gharghoda','Dehridih',DROWN,'Stuck in Panikhet dam marsh','Natural','M',2,None,'—','PM+Lab')
add(G,'2025-01-14',2025,'Gharghoda','Charmar',DROWN,'Drowned in Rabo dam','Natural','F',0.2,'Calf (<1 yr)','—','PM+Lab')
add(G,'2025-01-22',2025,'Gharghoda','Dehridih',DROWN,'Stuck in Panikhet dam marsh','Natural','F',2,None,'—','PM+Lab')
add(G,'2025-05-12',2025,'Gharghoda','Charmar',INJURY,'Brain injury','Natural','F',0.25,'Calf (<1 yr)','—','PM+Lab')
add(G,'2025-05-25',2025,'Gharghoda','Charmar',DROWN,'Drowned in water','Natural','M',0.42,'Calf (<1 yr)','—','PM+Lab')
add(G,'2025-10-20',2025,'Tamnar','Kerakhol',ELEC,'Electric current','Unnatural','M',20,None,'—','PM')
add(G,'2025-11-25',2025,'Tamnar','Saraipali',DROWN,'Drowned in water','Natural','M',0.58,'Calf (<1 yr)','—','PM+Lab')
add(G,'2025-12-20',2025,'Raigarh','Bangursiyan',DROWN,'Drowned in water','Natural','M',0.5,'Calf (<1 yr)','—','PM+Lab')
add(G,'2026-01-28',2026,'Gharghoda','Kaya',INJURY,'Fell in Sakra nala — internal injury','Natural','M',1,None,'—','PM')
add(G,'2026-02-21',2026,'Tamnar','Jhingol',WEAK,'Weakness / emaciation','Natural','F',None,'Calf (<1 yr)','—','PM')
add(G,'2026-03-11',2026,'Gharghoda','Charratangar',ELEC,'Electric current','Unnatural','F',2.5,None,'—','PM+Lab')
add(G,'2026-03-11',2026,'Gharghoda','Charratangar',ELEC,'Electric current','Unnatural','M',2.5,None,'—','PM+Lab')
add(G,'2026-06-01',2026,'Kharsia','Gurda',DROWN,'Drowned in water','Natural','M',0.3,'Calf (<1 yr)','—','Pending')
add(G,'2026-06-16',2026,'Gharghoda','Charmar',TRAIN,'Hit by goods train','Unnatural','F',45,None,'—','Pending')

if __name__ == '__main__':
    from collections import Counter
    print('Total records:', len(R))
    print('By division:', Counter(r['division'] for r in R))
    print('By cause:', Counter(r['cause_group'] for r in R))
    print('By nat/unnat:', Counter(r['nat'] for r in R))
