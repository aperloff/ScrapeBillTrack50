#!/bin/env python3

"""A magicconfig file used to define a set of options used by the ScrapeBillTrack50 module.

This specific configuration specifies that all of the assigned legislators should be used.
"""

from magiconfig import MagiConfig

config = MagiConfig()
config.legislators = [
	"Richard Durbin",
	"John Hickenlooper",
	"Barbara Lee",
	"Jerry McNerney",
	"Zoe Lofgren",
	"Young Kim",
	"Emanuel Cleaver",
	"Michael Crapo",
	"Jackie Speier",
	"Mike Thompson",
	"Eric Swalwell",
	"Mark DeSaulnier",
	"Ted Lieu",
	"Anthony Brown",
	"Kevin Hern",
	"Joe Neguse",
	"Sara Jacobs",
	"Alejandro Padilla",
]
