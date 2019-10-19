from json import loads as json_loads

from src.restriction import RestrictionType, Restriction

def test_can_overlap():
	r0 = Restriction(json_loads('''
		{
			"type": 1,
			"contents": ["PD-101", "FA-102", "FA-105", "LT-103", "LT-203", "LT-206"]
		}
	'''))
	
	r1 = Restriction(json_loads('''
		{
			"type": 2,
			"contents": [
				[
					"MS-301", "MS-302", "MS-303", "MS-304"
				],
				[
					"CH-103", "CH-104", "MA-103", "MA-104", "PH-201", "PH-202", "ER-*"
				]
			]
		}
	'''))
	
	r2 = Restriction(json_loads('''
		{
			"type": 2,
			"contents": [
				[
					"MS-301", "MS-302", "MS-303", "MS-304"
				],
				[
					"CH-103", "CH-104", "MA-103", "MA-104", "PH-201", "PH-202", "ER-*"
				],
				[
					"SO-101"
				]
			]
		}
	'''))
	
	r3 = Restriction(json_loads('''
		{
			"type": 1,
			"contents": ["BU-150", "MSL-*"]
		}
	'''))
	
	restriction_list = [r0, r1, r2, r3]
	
	assert Restriction.can_overlap(restriction_list, "PD-101", "MS-301")
	assert not Restriction.can_overlap(restriction_list, "PD-101", "LT-206")
	assert Restriction.can_overlap(restriction_list, "PD-101", "LT-205")
	assert Restriction.can_overlap(restriction_list, "BU-150", "SO-101")
	assert not Restriction.can_overlap(restriction_list, "BU-150", "MSL-250")
	assert not Restriction.can_overlap(restriction_list, "MS-304", "PH-202")
	assert Restriction.can_overlap([r0, r1], "MS-301", "SO-101")
	assert not Restriction.can_overlap(restriction_list, "MS-301", "SO-101")
	assert not Restriction.can_overlap(restriction_list, "SO-101", "MS-301")
	assert not Restriction.can_overlap(restriction_list, "MS-302", "ER-301")
	assert not Restriction.can_overlap(restriction_list, "ER-499", "MS-302")
	assert Restriction.can_overlap(restriction_list, "ER-499", "ER-301")