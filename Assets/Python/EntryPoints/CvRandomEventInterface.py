# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
#
# CvRandomEventInterface.py
#
# These functions are App Entry Points from C++
# WARNING: These function names should not be changed
# WARNING: These functions can not be placed into a class
#
# No other modules should import this
#
import sys
import CvUtil
import CvScreensInterface
from CvPythonExtensions import *

gc = CyGlobalContext()
localText = CyTranslator()

# ============================================================
# CORE HELPERS (DO NOT TOUCH)
# ============================================================

def _scaleTurnsByGameSpeed(iBaseTurns):
	iGameSpeedType = CyGame().getGameSpeedType()
	iGrowthPercent = gc.getGameSpeedInfo(iGameSpeedType).getGrowthPercent()
	return max(1, int((iBaseTurns * iGrowthPercent) / 100))

def get_simple_help(text_key):
	""" This function constructs another function that returns the fixed localized text  """
	def get_help(argsList):
		szHelp = localText.getText(text_key, ())
		return szHelp

	return get_help

def doEventEndTutorial(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)
	CyMessageControl().sendPlayerOption(PlayerOptionTypes.PLAYEROPTION_TUTORIAL, False)

def isExpiredFoundColony(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if player.getNumCities() > 0:
		return True
	return False

def doEventCivilopediaSettlement(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_SETTLEMENTS")))

def canDoTriggerImmigrant(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if player.getNumEuropeUnits() == 0:
		return False
	return True

def canDoTriggerImmigrantDone(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if player.getNumEuropeUnits() > 0:
		return False
	return True

def doEventCivilopediaEurope(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_EUROPE")))

def doEventCivilopediaImmigration(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_IMMIGRATION")))


def canDoTriggerMotherland(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)
	(unit, iter) = player.firstUnit()
	while (unit):
		if unit.getDomainType() == DomainTypes.DOMAIN_SEA and unit.getUnitTravelState() == UnitTravelStates.UNIT_TRAVEL_STATE_TO_EUROPE and unit.getUnitTravelTimer() == 1:
			return True
		(unit, iter) = player.nextUnit(iter)
	return False

def doEventCivilopediaProfessions(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_PROFESSIONS")))

def canDoTriggerPioneer(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)

	improvementList = [gc.getInfoTypeForString("IMPROVEMENT_FARM"), gc.getInfoTypeForString("IMPROVEMENT_MINE"), gc.getInfoTypeForString("IMPROVEMENT_LODGE")]
	for iImprovement in improvementList:
		if player.getImprovementCount(iImprovement) > 0:
			return False

	ePioneer = gc.getInfoTypeForString("PROFESSION_PIONEER")
	(unit, iter) = player.firstUnit()
	while (unit):
		if unit.getProfession() == ePioneer:
			return False
		(unit, iter) = player.nextUnit(iter)

	return True

def canDoTriggerImproveLand(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)

	improvementList = [gc.getInfoTypeForString("IMPROVEMENT_FARM"), gc.getInfoTypeForString("IMPROVEMENT_MINE"), gc.getInfoTypeForString("IMPROVEMENT_LODGE")]
	for iImprovement in improvementList:
		if player.getImprovementCount(iImprovement) > 0:
			return False

	ePioneer = gc.getInfoTypeForString("PROFESSION_PIONEER")
	(unit, iter) = player.firstUnit()
	while (unit):
		if unit.getProfession() == ePioneer:
			return True
		(unit, iter) = player.nextUnit(iter)

	return False

def doEventCivilopediaImproveLand(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_IMPROVEMENTS")))

def canDoTriggerFoundingFather(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)
	team = gc.getTeam(player.getTeam())

	for iFather in range(gc.getNumFatherInfos()):
		if (team.canConvinceFather(iFather)):
			return True
	return False

def doEventCivilopediaFoundingFather(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_FATHERS")))

def doEventCivilopediaNativeVillages(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_NATIVES")))

def canDoTriggerRevolution(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer( pTriggeredData.ePlayer )

	if gc.getTeam(player.getTeam()).canDoRevolution():
		return True

	return False

def doEventCivilopediaRevolution(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_LIBERTY")))

def canDoCityTriggerTools(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCityId = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCityId)

	if (not city.isNone() and city.getYieldRate(gc.getInfoTypeForString("YIELD_TOOLS")) > 0):
		return True

	return False

def doEventCivilopediaTools(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_PROFESSIONS")))

def canDoCityTriggerBuildingRequiresTools(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCityId = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCityId)
	building = city.getProductionBuilding()

	if building != BuildingTypes.NO_BUILDING:
		if (gc.getBuildingInfo(building).getYieldCost(gc.getInfoTypeForString("YIELD_TOOLS")) > 0):
			return True

	return False

def doEventCivilopediaAutomatedTools(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_TRADE")))

def canDoSpeakToChief(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)

	bFoundNative = False
	for iPlayer in range(gc.getMAX_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and loopPlayer.isNative():
			bFoundNative = True
			(city, iter) = loopPlayer.firstCity(True)
			while(city):
				if city.isScoutVisited(player.getTeam()):
					return False
				(city, iter) = loopPlayer.nextCity(iter, True)

	return bFoundNative

def canDoSpeakToChiefCompleted(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)

	for iPlayer in range(gc.getMAX_PLAYERS()):
		loopPlayer = gc.getPlayer(iPlayer)
		if loopPlayer.isAlive() and loopPlayer.isNative():
			(city, iter) = loopPlayer.firstCity(True)
			while(city):
				if city.isScoutVisited(player.getTeam()):
					return True
				(city, iter) = loopPlayer.nextCity(iter, True)

	return False

def doEventCivilopediaWar(argsList):
	eEvent = argsList[1]
	pTriggeredData = argsList[0]
	CvScreensInterface.pediaShowHistorical((CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, gc.getInfoTypeForString("CONCEPT_WAR")))

def canCityTriggerDoOverstock(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCityId = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCityId)

	for i in range(YieldTypes.NUM_YIELD_TYPES):
		if (not city.isNone() and city.getYieldStored(i) > city.getMaxYieldCapacity() and i != gc.getInfoTypeForString("YIELD_FOOD")):
			return True

	return False

def canDoTaxes(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)

	if player.getTaxRate() > 0:
		return True

	return False

####### TAC Events ########

######## SECOND CITY ###########

def canTriggerSecondCity(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]

	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)

	if city.isNone():
		return False

	if not player.isPlayable():
		return False

	if player.getNumCities() >= 2:
		return True

	return False

def applySecondCity1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if not player.isHuman():
		city = player.firstCity(True)[0]
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	iYield1 = gc.getInfoTypeForString("YIELD_SAILCLOTH")
	city.changeYieldStored(iYield1, event.getGenericParameter(1)*Speed.getTrainPercent()/100)
	iYield2 = gc.getInfoTypeForString("YIELD_TOOLS")
	city.changeYieldStored(iYield2, event.getGenericParameter(2)*Speed.getTrainPercent()/100)
	iYield3 = gc.getInfoTypeForString("YIELD_HORSES")
	city.changeYieldStored(iYield3, event.getGenericParameter(3)*Speed.getTrainPercent()/100)

def getHelpSecondCity1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	iYield1 = gc.getInfoTypeForString("YIELD_SAILCLOTH")
	iYield2 = gc.getInfoTypeForString("YIELD_TOOLS")
	iYield3 = gc.getInfoTypeForString("YIELD_HORSES")
	szHelp = localText.getText("TXT_KEY_EVENT_SECONDCOLONY_1_HELP", (king.getCivilizationAdjectiveKey(), ))
	if event.getGenericParameter(1) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (event.getGenericParameter(1)*Speed.getTrainPercent()/100,  gc.getYieldInfo(iYield1).getChar(), city.getNameKey()))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (event.getGenericParameter(2)*Speed.getTrainPercent()/100,  gc.getYieldInfo(iYield2).getChar(), city.getNameKey()))
	if event.getGenericParameter(3) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (event.getGenericParameter(3)*Speed.getTrainPercent()/100,  gc.getYieldInfo(iYield3).getChar(), city.getNameKey()))
	if event.getGenericParameter(1) <> 0 :
		overflow = event.getGenericParameter(1)*Speed.getTrainPercent()/100 + city.getYieldStored(iYield1) - city.getMaxYieldCapacity()
		if overflow > 0:
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_OVERFLOW", (overflow,  gc.getYieldInfo(iYield1).getChar(), city.getNameKey()))
	if event.getGenericParameter(2) <> 0 :
		overflow = event.getGenericParameter(2)*Speed.getTrainPercent()/100 + city.getYieldStored(iYield2) - city.getMaxYieldCapacity()
		if overflow > 0:
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_OVERFLOW", (overflow,  gc.getYieldInfo(iYield2).getChar(), city.getNameKey()))
	if event.getGenericParameter(3) <> 0 :
		overflow = event.getGenericParameter(3)*Speed.getTrainPercent()/100 + city.getYieldStored(iYield3) - city.getMaxYieldCapacity()
		if overflow > 0:
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_OVERFLOW", (overflow,  gc.getYieldInfo(iYield3).getChar(), city.getNameKey()))
	return szHelp

def applySecondCity2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if not player.isHuman():
		city = player.firstCity(True)[0]
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	iYield1 = gc.getInfoTypeForString("YIELD_BLADES")
	city.changeYieldStored(iYield1, event.getGenericParameter(1)*Speed.getTrainPercent()/100)
	iYield2 = gc.getInfoTypeForString("YIELD_BAKERY_GOODS")
	city.changeYieldStored(iYield2, event.getGenericParameter(2)*Speed.getTrainPercent()/100)

def getHelpSecondCity2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	iYield1 = gc.getInfoTypeForString("YIELD_BLADES")
	iYield2 = gc.getInfoTypeForString("YIELD_BAKERY_GOODS")
	szHelp = localText.getText("TXT_KEY_EVENT_SECONDCOLONY_2_HELP", (king.getCivilizationAdjectiveKey(), ))
	if event.getGenericParameter(1) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (event.getGenericParameter(1)*Speed.getTrainPercent()/100,  gc.getYieldInfo(iYield1).getChar(), city.getNameKey()))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (event.getGenericParameter(2)*Speed.getTrainPercent()/100,  gc.getYieldInfo(iYield2).getChar(), city.getNameKey()))
	if event.getGenericParameter(1) <> 0 :
		overflow = event.getGenericParameter(1)*Speed.getTrainPercent()/100 + city.getYieldStored(iYield1) - city.getMaxYieldCapacity()
		if overflow > 0:
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_OVERFLOW", (overflow,  gc.getYieldInfo(iYield1).getChar(), city.getNameKey()))
	if event.getGenericParameter(2) <> 0 :
		overflow = event.getGenericParameter(2)*Speed.getTrainPercent()/100 + city.getYieldStored(iYield2) - city.getMaxYieldCapacity()
		if overflow > 0:
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_OVERFLOW", (overflow,  gc.getYieldInfo(iYield2).getChar(), city.getNameKey()))
	return szHelp

######## THIRD CITY ###########

def canTriggerThirdCity(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]

	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)

	if city.isNone():
		return False

	if not player.isPlayable():
		return False

	if player.getNumCities() >= 3:
		return True

	return False

######## FESTIVITY ###########

def canTriggerFestivity(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)

	if not player.isPlayable():
		return False
	if city.isNone():
		return False

	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False
	if player.isInRevolution():
		return False

	# Read Parameter 1 from the two events and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_FESTIVITY_2")
	event1 = gc.getEventInfo(eEvent1)
	eEvent2 = gc.getInfoTypeForString("EVENT_FESTIVITY_3")
	event2 = gc.getEventInfo(eEvent2)
	iYield1 = gc.getInfoTypeForString("YIELD_CIGARS")
	iYield2 = gc.getInfoTypeForString("YIELD_RUM")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	quantity2 = event2.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity2 = quantity2 * Speed.getStoragePercent()/100

	if city.getYieldStored(iYield1) < -quantity and city.getYieldStored(iYield2) < -quantity2:
		return False
	# If player has reached the maximum for max tax rate, do not start event
	if player.NBMOD_GetMaxTaxRate() == GlobalDefines.MAX_TAX_RATE:
		return False
	return True

def applyFestivity1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(2))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(2))
	if player.getTaxRate() + event.getGenericParameter(1) <= player.NBMOD_GetMaxTaxRate():
		player.changeTaxRate(event.getGenericParameter(1))
	else:
		player.NBMOD_IncreaseMaxTaxRate()

def getHelpFestivity1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	szHelp = localText.getText("TXT_KEY_EVENT_FESTIVITY_1_HELP", ())
	if (player.getTaxRate() + event.getGenericParameter(1) <= player.NBMOD_GetMaxTaxRate()) and event.getGenericParameter(1) <>0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_TAX_INCREASE", (event.getGenericParameter(1), player.getTaxRate() + event.getGenericParameter(1)))
	if (player.getTaxRate() + event.getGenericParameter(1) > player.NBMOD_GetMaxTaxRate()) and event.getGenericParameter(1) <>0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAX_INCREASE", (GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()+GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(2), king.getCivilizationAdjectiveKey()))
	return szHelp

def CanDoFestivity2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	iYield = gc.getInfoTypeForString("YIELD_CIGARS")
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.isNone():
		return False
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyFestivity2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(3))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(3))
	iYield = gc.getInfoTypeForString("YIELD_CIGARS")
	iPrice = king.getYieldBuyPrice(iYield)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	king.setYieldBuyPrice(iYield, iPrice+event.getGenericParameter(2), 1)
	city.changeYieldStored(iYield, quantity)
	if event.getGenericParameter(4) == 1 :
		player.NBMOD_DecreaseMaxTaxRate()

def getHelpFestivity2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_CIGARS")
	szHelp = localText.getText("TXT_KEY_EVENT_FESTIVITY_2_HELP", ())
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if quantity <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE", (event.getGenericParameter(2), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXDECREASE", (-GlobalDefines.DECREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.DECREASE_MAX_TAX_RATE))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXINCREASE", (-GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

def CanDoFestivity3(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyFestivity3(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(3))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(3))
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	iPrice = king.getYieldBuyPrice(iYield)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	king.setYieldBuyPrice(iYield, iPrice+event.getGenericParameter(2), 1)
	city.changeYieldStored(iYield, quantity)
	if event.getGenericParameter(4) == 1 :
		player.NBMOD_DecreaseMaxTaxRate()

def getHelpFestivity3(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = localText.getText("TXT_KEY_EVENT_FESTIVITY_2_HELP", ())
	if event.getGenericParameter(1) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE", (event.getGenericParameter(2), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXDECREASE", (-GlobalDefines.DECREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.DECREASE_MAX_TAX_RATE))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXINCREASE", (-GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

def CanDoFestivity4(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	iYield1 = gc.getInfoTypeForString("YIELD_CIGARS")
	iYield2 = gc.getInfoTypeForString("YIELD_RUM")
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if (city.getYieldStored(iYield1) < -quantity) or (city.getYieldStored(iYield2) < -quantity) :
		return False
	return True

def applyFestivity4(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(3))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(3))
	iYield = gc.getInfoTypeForString("YIELD_CIGARS")
	iPrice = king.getYieldBuyPrice(iYield)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	king.setYieldBuyPrice(iYield, iPrice+event.getGenericParameter(2), 1)
	city.changeYieldStored(iYield, quantity)
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	iPrice = king.getYieldBuyPrice(iYield)
	king.setYieldBuyPrice(iYield, iPrice+event.getGenericParameter(2), 1)
	city.changeYieldStored(iYield, quantity)
	if event.getGenericParameter(4) == 1 :
		player.NBMOD_DecreaseMaxTaxRate()

def getHelpFestivity4(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	iYield1 = gc.getInfoTypeForString("YIELD_CIGARS")
	iYield2 = gc.getInfoTypeForString("YIELD_RUM")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = localText.getText("TXT_KEY_EVENT_FESTIVITY_4_HELP", ())
	if event.getGenericParameter(1) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield1).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield2).getChar(), city.getNameKey()))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE", (event.getGenericParameter(2), gc.getYieldInfo(iYield1).getChar(), king.getCivilizationShortDescriptionKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE", (event.getGenericParameter(2), gc.getYieldInfo(iYield2).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXDECREASE", (-GlobalDefines.DECREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.DECREASE_MAX_TAX_RATE))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXINCREASE", (-GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

def getHelpCounterblaste1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_CIGARS")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = localText.getText("TXT_KEY_EVENT_COUNTERBLASTE_1_HELP", ())
	if event.getGenericParameter(1) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE", (event.getGenericParameter(2), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXDECREASE", (-GlobalDefines.DECREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.DECREASE_MAX_TAX_RATE))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXINCREASE", (-GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

def getHelpCounterblaste2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	iYield = gc.getInfoTypeForString("YIELD_CIGARS")
	szHelp = localText.getText("TXT_KEY_EVENT_COUNTERBLASTE_2_HELP", ())
	if event.getGenericParameter(1) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE", (event.getGenericParameter(2), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXDECREASE", (-GlobalDefines.DECREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.DECREASE_MAX_TAX_RATE))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXINCREASE", (-GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

def CanDoWhaling1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	iYield = gc.getInfoTypeForString("YIELD_WHALE_OIL")
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.isNone():
		return False
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyWhaling1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_WHALE_OIL")
	iPrice = king.getYieldBuyPrice(iYield)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	king.setYieldBuyPrice(iYield, iPrice+event.getGenericParameter(2), 1)
	city.changeYieldStored(iYield, quantity)
	if event.getGenericParameter(4) == 1 :
		player.NBMOD_DecreaseMaxTaxRate()

def getHelpWhaling1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_WHALE_OIL")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = localText.getText("TXT_KEY_EVENT_WHALING_1_HELP", ())
	if event.getGenericParameter(1) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE", (event.getGenericParameter(2), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXDECREASE", (-GlobalDefines.DECREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.DECREASE_MAX_TAX_RATE))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXINCREASE", (-GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

######## WINTER ###########

def _isWinterSeasonNow():
	game = CyGame()
	gameSpeed = gc.getGameSpeedInfo(game.getGameSpeedType())
	iMonthIncrement = gameSpeed.getGameTurnInfo(0).iMonthIncrement
	iCurrentTurn = game.getGameTurn()
	szDate = CyGameTextMgr().getTimeStr(iCurrentTurn + 1, True)

	January = localText.getText("TXT_KEY_MONTH_JANUARY", ())
	February = localText.getText("TXT_KEY_MONTH_FEBRUARY", ())
	December = localText.getText("TXT_KEY_MONTH_DECEMBER", ())
	November = localText.getText("TXT_KEY_MONTH_NOVEMBER", ())
	October = localText.getText("TXT_KEY_MONTH_OCTOBER", ())

	# 1) Monatssystem
	if iMonthIncrement < 6:
		if (January in szDate or February in szDate or December in szDate or November in szDate or October in szDate):
			return True
		return False

	# 2) Halbjahre
	if iMonthIncrement == 6:
		if (October in szDate or November in szDate or December in szDate or January in szDate or February in szDate):
			return True

		# Fallback falls Monatsnamen nicht zuverlässig sind
		if (iCurrentTurn % 2) == 0:
			return True

		return False

	# 3) Jahres-System (Fallback)
	if (iCurrentTurn % 4) == 0:
		return True

	return False


def canTriggerWinter(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	king = gc.getPlayer(player.getParent())
	if king.isNone():
		return False
	if not king.isEurope():
		return False

	return _isWinterSeasonNow()


def applyWinter(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	iYield1 = gc.getInfoTypeForString("YIELD_COATS")
	iYield2 = gc.getInfoTypeForString("YIELD_FUR")

	player = gc.getPlayer(kTriggeredData.ePlayer)
	king = gc.getPlayer(player.getParent())

	iPrice1 = king.getYieldBuyPrice(iYield1)
	king.setYieldBuyPrice(iYield1, iPrice1 + event.getGenericParameter(1), 1)

	iPrice2 = king.getYieldBuyPrice(iYield2)
	king.setYieldBuyPrice(iYield2, iPrice2 + event.getGenericParameter(2), 1)


def getHelpWinter(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	king = gc.getPlayer(player.getParent())

	iYield1 = gc.getInfoTypeForString("YIELD_COATS")
	iYield2 = gc.getInfoTypeForString("YIELD_FUR")

	szHelp = localText.getText("TXT_KEY_EVENT_WINTER_HELP", (king.getCivilizationShortDescriptionKey(),))

	if event.getGenericParameter(1) <> 0:
		szHelp += "\n" + localText.getText(
			"TXT_KEY_EVENT_PRICE_INCREASE",
			(event.getGenericParameter(1), gc.getYieldInfo(iYield1).getChar(), king.getCivilizationShortDescriptionKey())
		)

	if event.getGenericParameter(2) <> 0:
		szHelp += "\n" + localText.getText(
			"TXT_KEY_EVENT_PRICE_INCREASE",
			(event.getGenericParameter(2), gc.getYieldInfo(iYield2).getChar(), king.getCivilizationShortDescriptionKey())
		)

	return szHelp


def canEndWinter(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	king = gc.getPlayer(player.getParent())
	if king.isNone():
		return False
	if not king.isEurope():
		return False

	# Winter darf erst enden, wenn Mindestdauer erreicht ist
	eWinterEvent = gc.getInfoTypeForString("EVENT_WINTER_1")
	kEventData = player.getEventOccured(eWinterEvent)

	if kEventData is None:
		return True  # failsafe

	iWinterTurn = kEventData.iTurn
	iCurrentTurn = CyGame().getGameTurn()

	iMinDuration = _scaleTurnsByGameSpeed(30)

	if iCurrentTurn < iWinterTurn + iMinDuration:
		return False

	# danach zusätzlich prüfen: sind wir noch im Winter?
	return not _isWinterSeasonNow()


def applyEndWinter(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	iYield1 = gc.getInfoTypeForString("YIELD_COATS")
	iYield2 = gc.getInfoTypeForString("YIELD_FUR")

	player = gc.getPlayer(kTriggeredData.ePlayer)
	king = gc.getPlayer(player.getParent())

	iPrice1 = king.getYieldBuyPrice(iYield1)
	king.setYieldBuyPrice(iYield1, iPrice1 + event.getGenericParameter(1), 1)

	iPrice2 = king.getYieldBuyPrice(iYield2)
	king.setYieldBuyPrice(iYield2, iPrice2 + event.getGenericParameter(2), 1)


def getHelpEndWinter(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	king = gc.getPlayer(player.getParent())

	iYield1 = gc.getInfoTypeForString("YIELD_COATS")
	iYield2 = gc.getInfoTypeForString("YIELD_FUR")

	szHelp = localText.getText("TXT_KEY_EVENT_END_WINTER_HELP", (king.getCivilizationShortDescriptionKey(),))

	if event.getGenericParameter(1) <> 0:
		szHelp += "\n" + localText.getText(
			"TXT_KEY_EVENT_PRICE_DECREASE",
			(event.getGenericParameter(1), gc.getYieldInfo(iYield1).getChar(), king.getCivilizationShortDescriptionKey())
		)

	if event.getGenericParameter(2) <> 0:
		szHelp += "\n" + localText.getText(
			"TXT_KEY_EVENT_PRICE_DECREASE",
			(event.getGenericParameter(2), gc.getYieldInfo(iYield2).getChar(), king.getCivilizationShortDescriptionKey())
		)

	return szHelp

######## Peasant War Preparations ###########

def canTriggerPeasantWarPrep(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	#iStartYear = 1495
	if not player.isPlayable() or not player2.isPlayable() :
		return False
	if not player.isHuman():
		return False
	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False
	#iCurrentYear = CyGame().getGameTurnYear()
	#if iCurrentYear < iStartYear :
	#	return False
	#iChance = gc.getGame().getSorenRandNum(100, "(c) TAC 2010 Events")
	#iChance = iChance + 10 * (iCurrentYear-iStartYear)+5
	#if iChance > 100 :
	#	return true
	#return False
	return True

def applyPeasantWarPrep(argsList):
	kTriggeredData = argsList[0]
	iPriceChange = 2
	iYield1 = gc.getInfoTypeForString("YIELD_MUSKETS")
	iYield2 = gc.getInfoTypeForString("YIELD_FOOD")
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	iPrice1 = king.getYieldBuyPrice(iYield1)
	king.setYieldBuyPrice(iYield1, iPrice1+iPriceChange, 1)
	iPrice2 = king.getYieldBuyPrice(iYield2)
	king.setYieldBuyPrice(iYield2, iPrice2+iPriceChange, 1)

def getHelpPeasantWarPrep(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	iYield1 = gc.getInfoTypeForString("YIELD_MUSKETS")
	iYield2 = gc.getInfoTypeForString("YIELD_FOOD")
	iPriceChange = 2
	szHelp = localText.getText("TXT_KEY_EVENT_PEASANT_WARPREP_HELP", (iPriceChange, gc.getYieldInfo(iYield1).getChar(), king.getCivilizationDescriptionKey(), iPriceChange, gc.getYieldInfo(iYield2).getChar(), king.getCivilizationDescriptionKey()))
	return szHelp

######## DISCOVERY LEGENDARY SCOUT EVENT ###########

######## DISCOVERY LEGENDARY SCOUT EVENT ###########

DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN_PREFIX = "[[WTP_DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN="
DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN_SUFFIX = "]]"

def _getDiscoveryLegendaryScoutLeftTurn(unit):
	if unit is None or unit.isNone():
		return -1

	szData = unit.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN_PREFIX)
	iEnd = szData.find(DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setDiscoveryLegendaryScoutLeftTurn(unit, iTurn):
	if unit is None or unit.isNone():
		return

	szData = unit.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN_PREFIX,
		iTurn,
		DISCOVERY_LEGENDARY_SCOUT_LEFT_TURN_SUFFIX
	)

	szData += szMarker
	unit.setScriptData(szData)

def _getDiscoveryLegendaryScoutRequiredTurns():
	iBaseTurns = 30
	iGameSpeed = CyGame().getGameSpeedType()
	gameSpeedInfo = gc.getGameSpeedInfo(iGameSpeed)
	iPercent = gameSpeedInfo.getGrowthPercent()

	iScaledTurns = iBaseTurns * iPercent / 100
	if iScaledTurns < 1:
		iScaledTurns = 1

	return int(iScaledTurns)

def _isValidDiscoveryLegendaryScoutUnit(player, unit, kTriggeredData):
	if player.isNone():
		return False
	if not player.isAlive():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	if unit is None or unit.isNone():
		return False

	eScoutProfession = gc.getInfoTypeForString("PROFESSION_SCOUT")
	if unit.getProfession() != eScoutProfession:
		return False

	ePromo = gc.getInfoTypeForString("PROMOTION_LEGENDARY_SCOUT")
	if unit.isHasPromotion(ePromo):
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return False

	if plot.isWater():
		return False

	if plot.isCity():
		return False

	if plot.getOwner() == player.getID():
		return False

	return True

def canTriggerDiscoveryLegendaryScout(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if not _isValidDiscoveryLegendaryScoutUnit(player, unit, kTriggeredData):
		return False

	iCurrentTurn = CyGame().getGameTurn()
	iLeftTurn = _getDiscoveryLegendaryScoutLeftTurn(unit)

	# First valid turn in the wilderness
	if iLeftTurn == -1:
		_setDiscoveryLegendaryScoutLeftTurn(unit, iCurrentTurn)
		return False

	iTurnsAway = iCurrentTurn - iLeftTurn
	iRequiredTurns = _getDiscoveryLegendaryScoutRequiredTurns()

	if iTurnsAway < iRequiredTurns:
		return False

	return True

def applyDiscoveryLegendaryScoutXP(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return

	unit = player.getUnit(kTriggeredData.iUnitId)
	if not _isValidDiscoveryLegendaryScoutUnit(player, unit, kTriggeredData):
		return

	iXP = 15 + CyGame().getSorenRandNum(6, "Legendary Scout XP")

	unit.changeExperience(iXP, -1, False, False, False)

	ePromo = gc.getInfoTypeForString("PROMOTION_LEGENDARY_SCOUT")
	unit.setHasRealPromotion(ePromo, True)

	_setDiscoveryLegendaryScoutLeftTurn(unit, -1)

	CyInterface().addMessage(
		kTriggeredData.ePlayer,
		True,
		10,
		localText.getText("TXT_KEY_EVENT_DISCOVERY_LEGENDARY_SCOUT_XP_RESULT", (iXP,)),
		"",
		0,
		"",
		ColorTypes(8),
		unit.getX(),
		unit.getY(),
		True,
		True
	)

def getHelpDiscoveryLegendaryScoutXP(argsList):
	iTurns = _getDiscoveryLegendaryScoutRequiredTurns()

	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_LEGENDARY_SCOUT_XP_HELP",
		(iTurns,)
	)

######## Discovery Attacked Event ###########

DISCOVERY_ATTACKED_SOFT_COOLDOWN_PREFIX = "[[WTP_DISCOVERY_ATTACKED_SOFT_READY_TURN="
DISCOVERY_ATTACKED_SOFT_COOLDOWN_SUFFIX = "]]"

def _getDiscoveryAttackedSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(DISCOVERY_ATTACKED_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(DISCOVERY_ATTACKED_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(DISCOVERY_ATTACKED_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setDiscoveryAttackedSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(DISCOVERY_ATTACKED_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_ATTACKED_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_ATTACKED_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		DISCOVERY_ATTACKED_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		DISCOVERY_ATTACKED_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _startDiscoveryAttackedSoftCooldown(player):
	if player.isNone():
		return

	iCooldownTurns = _scaleTurnsByGameSpeed(15)

	_setDiscoveryAttackedSoftCooldownReadyTurn(
		player,
		CyGame().getGameTurn() + iCooldownTurns
	)

def _isDiscoveryAttackedSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getDiscoveryAttackedSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _spawnDiscoveryAttackedHostileAdjacent(plot):
	iHostileUnitClass = gc.getInfoTypeForString("UNITCLASS_HOSTILE_NATIVE")
	if iHostileUnitClass == -1:
		return None

	if plot is None or plot.isNone():
		return None

	iBarbarian = gc.getGame().getBarbarianPlayer()
	barbPlayer = gc.getPlayer(iBarbarian)
	if barbPlayer.isNone():
		return None

	barbCiv = gc.getCivilizationInfo(barbPlayer.getCivilizationType())
	iUnitType = barbCiv.getCivilizationUnits(iHostileUnitClass)
	if iUnitType == UnitTypes.NO_UNIT:
		return None

	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			if iDX == 0 and iDY == 0:
				continue

			pLoop = plotXY(plot.getX(), plot.getY(), iDX, iDY)
			if pLoop is None or pLoop.isNone():
				continue
			if pLoop.isWater():
				continue
			if pLoop.isImpassable():
				continue
			if pLoop.isPeak():
				continue
			if pLoop.isCity():
				continue
			if pLoop.isUnit():
				continue

			pUnit = barbPlayer.initUnit(
				iUnitType,
				ProfessionTypes.NO_PROFESSION,
				pLoop.getX(),
				pLoop.getY(),
				UnitAITypes.NO_UNITAI,
				DirectionTypes.DIRECTION_SOUTH,
				0
			)

			if pUnit is not None and not pUnit.isNone():
				return pUnit

	return None

def _getDistanceToNearestOwnCity(player, plot):
	if player.isNone() or plot.isNone():
		return 99

	iBest = 99
	(city, iter) = player.firstCity(True)
	while city:
		iDist = plotDistance(plot.getX(), plot.getY(), city.getX(), city.getY())
		if iDist < iBest:
			iBest = iDist
		(city, iter) = player.nextCity(iter, True)

	return iBest

def _getDiscoveryAttackedChance(player, plot):
	iDistance = _getDistanceToNearestOwnCity(player, plot)

	# Scale for large maps (Gigantic tuned)
	iScaledDistance = min(iDistance, 120) / 6

	if _isDiscoveryAttackedSoftCooldownActive(player):
		iChance = (1 + iScaledDistance / 2) * 2
		return min(12, int(iChance))

	# Normal chance
	iChance = (2 + iScaledDistance) * 2
	return min(40, int(iChance))

def canTriggerDiscoveryAttacked(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	# Only playable European players
	if player.isNone() or not player.isPlayable() or player.isNative():
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False

	# Exact unit / plot binding to prevent ghost triggers
	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return False

	# Must be land plot
	if plot.isWater():
		return False

	# No cities
	if plot.isCity():
		return False

	# Must be outside own borders
	if plot.getOwner() == player.getID():
		return False

	# Must be a valid ambush feature
	aValidFeatures = [
		gc.getInfoTypeForString("FEATURE_FOREST"),
		gc.getInfoTypeForString("FEATURE_JUNGLE"),
		gc.getInfoTypeForString("FEATURE_MANGROVE"),
		gc.getInfoTypeForString("FEATURE_TROPICAL_GROVES"),
		gc.getInfoTypeForString("FEATURE_FOREST_EVERGREEN"),
		gc.getInfoTypeForString("FEATURE_DENSE_FOREST"),
		gc.getInfoTypeForString("FEATURE_FOREST_TUNDRA"),
		gc.getInfoTypeForString("FEATURE_ANCIENT_FOREST"),
		gc.getInfoTypeForString("FEATURE_LIGHT_FOREST"),
	]

	if plot.getFeatureType() not in aValidFeatures:
		return False

	iChance = _getDiscoveryAttackedChance(player, plot)

	if CyGame().getSorenRandNum(100, "Discovery Attacked trigger") >= iChance:
		return False

	return True

def applyDiscoveryAttacked(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	# Exact unit / plot binding to prevent invalid execution
	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if plot.isWater():
		return

	if plot.isCity():
		return

	# Safety: must still be outside own borders
	if plot.getOwner() == player.getID():
		return

	# Spawn exactly 1 hostile native and attack immediately via DLL combat
	hostileUnit = _spawnDiscoveryAttackedHostileAdjacent(plot)
	if hostileUnit is not None and not hostileUnit.isNone():
		if hostileUnit.canMoveInto(plot, True, False, False):
			hostileUnit.attack(plot, False)

	# Start soft cooldown
	_startDiscoveryAttackedSoftCooldown(player)

def getHelpDiscoveryAttacked(argsList):
	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_EVENTS_ATTACKED_HELP",
		()
	)
  
######## Discovery Events ###########

def canTriggerDiscoveryStart(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	# Only before founding the first city
	if player.getNumCities() > 0:
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False

	# The tracked unit must stand exactly on the triggered plot
	if unit.getX() != kTriggeredData.iPlotX or unit.getY() != kTriggeredData.iPlotY:
		return False

	# Only on land
	if plot.isWater():
		return False

	eSettler = gc.getInfoTypeForString("PROFESSION_SETTLER")
	if unit.getProfession() != eSettler:
		return False

	return True

def getHelpDiscoveryStart1(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	szHelp = getHelpDiscoveryConquistador(argsList)
	szHelp += u"\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (-2, king.getCivilizationAdjectiveKey()))
	return szHelp

def getHelpDiscoveryStart2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)

	szHelp = getHelpDiscoveryMissionary(argsList)

	iFatherPointType = event.getGenericParameter(3)
	iFatherPoints = event.getGenericParameter(4)

	if iFatherPointType != -1 and iFatherPoints > 0:
		szHelp += u"\n" + localText.getText(
			"TXT_KEY_EVENT_FATHER_POINTS",
			(
				iFatherPoints,
				gc.getFatherPointInfo(iFatherPointType).getChar(),
				gc.getFatherPointInfo(iFatherPointType).getDescription()
			)
		)

	return szHelp

def getHelpDiscoveryStart3(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	szHelp = getHelpDiscoveryTrader(argsList)
	szHelp += u"\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (1, king.getCivilizationAdjectiveKey()))
	return szHelp

def getHelpDiscoveryStart4(argsList):
	return getHelpDiscoveryOxcart(argsList)

def getHelpDiscoveryStart5(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	return localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (2, king.getCivilizationAdjectiveKey()))

def applyDiscoveryStart1(argsList):
	kTriggeredData = argsList[0]
	spawnOwnPlayerUnitInEurope(argsList)
	_changeKingRelation(argsList, -2)

def applyDiscoveryStart2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	spawnOwnPlayerUnitInEurope(argsList)

	iFatherPointType = event.getGenericParameter(3)
	iFatherPoints = event.getGenericParameter(4)

	if iFatherPointType != -1 and iFatherPoints > 0:
		team = gc.getTeam(player.getTeam())
		team.changeFatherPoints(iFatherPointType, iFatherPoints)

def applyDiscoveryStart3(argsList):
	kTriggeredData = argsList[0]
	spawnOwnPlayerUnitInEurope(argsList)
	_changeKingRelation(argsList, 1)

def applyDiscoveryStart4(argsList):
	kTriggeredData = argsList[0]
	spawnOwnPlayerUnitInEurope(argsList)

def applyDiscoveryStart5(argsList):
	kTriggeredData = argsList[0]
	_changeKingRelation(argsList, 2)

def spawnOwnPlayerUnitInEurope(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	iUnitClass = event.getGenericParameter(1)
	iNumUnits = event.getGenericParameter(2)

	iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClass)
	if iUnitType == -1:
		return

	# profession mapping
	professionMap = {
		gc.getInfoTypeForString("UNITCLASS_CHRISTIAN_MISSIONARY"): gc.getInfoTypeForString("PROFESSION_MISSIONARY"),
		gc.getInfoTypeForString("UNITCLASS_SEASONED_TRADER"): gc.getInfoTypeForString("PROFESSION_SCOUT"),
	}

	for i in range(iNumUnits):
		unit = player.initEuropeUnit(
			iUnitType,
			UnitAITypes.NO_UNITAI,
			DirectionTypes.NO_DIRECTION
		)

		if unit is None or unit.isNone():
			continue

		if iUnitClass in professionMap:
			unit.setProfession(professionMap[iUnitClass])

def _changeKingRelation(argsList, iChange):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	eKing = player.getParent()
	if eKing == -1:
		return

	king = gc.getPlayer(eKing)
	if king.isNone():
		return

	player.AI_changeAttitudeExtra(eKing, iChange)
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, iChange)

	if player.isHuman():
		if iChange > 0:
			CyInterface().addMessage(
				kTriggeredData.ePlayer,
				False,
				10,
				localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (iChange, king.getCivilizationAdjectiveKey())),
				"",
				0,
				"",
				ColorTypes(8),
				-1,
				-1,
				True,
				True
			)
		elif iChange < 0:
			CyInterface().addMessage(
				kTriggeredData.ePlayer,
				False,
				10,
				localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (iChange, king.getCivilizationAdjectiveKey())),
				"",
				0,
				"",
				ColorTypes(7),
				-1,
				-1,
				True,
				True
			)

def canTriggerDiscoveryFever(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	# Only playable European players
	if player.isNone() or not player.isPlayable() or player.isNative():
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False

	eFeverImmune = gc.getInfoTypeForString("PROMOTION_FEVER_IMMUNE")

	# Unit already had fever and is now immune
	if unit.isHasPromotion(eFeverImmune):
		return False

	plot = CyMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if plot.isNone():
		return False

	# Must be land plot
	if plot.isWater():
		return False

	# No cities
	if plot.isCity():
		return False

	# Only specific "fever" terrain features
	eFeature = plot.getFeatureType()
	if eFeature not in (
		gc.getInfoTypeForString("FEATURE_JUNGLE"),
		gc.getInfoTypeForString("FEATURE_MANGROVE"),
		gc.getInfoTypeForString("FEATURE_TROPICAL_GROVES"),
		gc.getInfoTypeForString("FEATURE_SWAMP"),
	):
		return False

	# Fixed trigger chance on valid plots
	if CyGame().getSorenRandNum(100, "Discovery Fever trigger") >= 20:
		return False

	return True

def applyDiscoveryFever(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	unit = player.getUnit(kTriggeredData.iUnitId)

	# Safety check: unit must exist
	if unit.isNone():
		return

	plot = CyMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)

	# Safety check: plot must still exist and still be valid for fever
	if plot.isNone():
		return
	if plot.isWater():
		return
	if plot.isCity():
		return

	eFeature = plot.getFeatureType()
	if eFeature not in (
		gc.getInfoTypeForString("FEATURE_JUNGLE"),
		gc.getInfoTypeForString("FEATURE_MANGROVE"),
		gc.getInfoTypeForString("FEATURE_TROPICAL_GROVES"),
		gc.getInfoTypeForString("FEATURE_SWAMP"),
	):
		return

	eFeverImmune = gc.getInfoTypeForString("PROMOTION_FEVER_IMMUNE")

	# Extra safety: do nothing if unit already became immune somehow
	if unit.isHasPromotion(eFeverImmune):
		return

	# Apply immobilization (2–5 turns)
	iImmobileTurns = 2 + CyGame().getSorenRandNum(4, "Discovery Fever duration")
	unit.setImmobileTimer(iImmobileTurns)

	# Apply damage (10–20%), but do not kill the unit
	iDamage = 10 + CyGame().getSorenRandNum(11, "Discovery Fever damage")
	iNewDamage = min(99, unit.getDamage() + iDamage)
	unit.setDamage(iNewDamage)

	# Mark unit as immune after surviving fever
	unit.setHasRealPromotion(eFeverImmune, True)

	# Player feedback
	if player.isHuman():
		CyInterface().addMessage(
			kTriggeredData.ePlayer,
			True,
			10,
			localText.getText(
				"TXT_KEY_EVENT_DISCOVERY_FEVER_RESULT",
				(unit.getName(), iDamage, iImmobileTurns)
			),
			"",
			0,
			"",
			ColorTypes(7),
			kTriggeredData.iPlotX,
			kTriggeredData.iPlotY,
			True,
			True
		)

def getHelpDiscoveryFever(argsList):
	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_FEVER_HELP",
		(2, 5, 10, 20)
	)
######## Discovery Desert ###########

DISCOVERY_DESERT_SOFT_COOLDOWN_PREFIX = "[[WTP_DISCOVERY_DESERT_SOFT_READY_TURN="
DISCOVERY_DESERT_SOFT_COOLDOWN_SUFFIX = "]]"

def _getDiscoveryDesertSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(DISCOVERY_DESERT_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(DISCOVERY_DESERT_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(DISCOVERY_DESERT_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setDiscoveryDesertSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(DISCOVERY_DESERT_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_DESERT_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_DESERT_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		DISCOVERY_DESERT_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		DISCOVERY_DESERT_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _startDiscoveryDesertSoftCooldown(player):
	if player.isNone():
		return

	_setDiscoveryDesertSoftCooldownReadyTurn(player, CyGame().getGameTurn() + 30)

def _isDiscoveryDesertSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getDiscoveryDesertSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _getDiscoveryDesertScaledTurns(iBaseTurns):
	gameSpeedType = CyGame().getGameSpeedType()
	iPercent = gc.getGameSpeedInfo(gameSpeedType).getGrowthPercent()
	return max(1, int((iBaseTurns * iPercent) / 100))

def _getDiscoveryDesertChance(player):
	# 30% normally, 2% during soft cooldown
	if _isDiscoveryDesertSoftCooldownActive(player):
		return 2

	return 30

def canTriggerDiscoveryDesert(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	# Only playable European players
	if player.isNone() or not player.isPlayable() or player.isNative():
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False

	# Prevent re-trigger while already affected
	if unit.getImmobileTimer() > 0:
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False

	# Exact unit / plot binding (ANTI-GHOST)
	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return False

	# Must be land
	if plot.isWater():
		return False

	# No cities
	if plot.isCity():
		return False

	# Must be desert
	eDesert = gc.getInfoTypeForString("TERRAIN_DESERT")
	if plot.getTerrainType() != eDesert:
		return False

	iChance = _getDiscoveryDesertChance(player)

	if CyGame().getSorenRandNum(100, "Discovery Desert trigger") >= iChance:
		return False

	return True

def applyDiscoveryDesert(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	# Exact plot check (ANTI-GHOST SAFETY)
	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if plot.isWater():
		return

	if plot.isCity():
		return

	eDesert = gc.getInfoTypeForString("TERRAIN_DESERT")
	if plot.getTerrainType() != eDesert:
		return

	# Immobilization: 2–4 turns (scaled)
	iBaseImmobileTurns = 2 + CyGame().getSorenRandNum(3, "Discovery Desert duration")
	iImmobileTurns = _getDiscoveryDesertScaledTurns(iBaseImmobileTurns)
	unit.setImmobileTimer(iImmobileTurns)

	# Damage: 2–5% (non-lethal)
	iDamage = 2 + CyGame().getSorenRandNum(4, "Discovery Desert damage")
	iNewDamage = min(99, unit.getDamage() + iDamage)
	unit.setDamage(iNewDamage)

	# Start soft cooldown
	_startDiscoveryDesertSoftCooldown(player)

	# Player feedback
	if player.isHuman():
		CyInterface().addMessage(
			kTriggeredData.ePlayer,
			True,
			10,
			localText.getText(
				"TXT_KEY_EVENT_DISCOVERY_DESERT_RESULT",
				(unit.getName(), iDamage, iImmobileTurns)
			),
			"",
			0,
			"",
			ColorTypes(7),
			kTriggeredData.iPlotX,
			kTriggeredData.iPlotY,
			True,
			True
		)

def getHelpDiscoveryDesert(argsList):
	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_DESERT_HELP",
		(2, 4, 2, 5)
	)

######## Discovery Mutiny ###########

DISCOVERY_MUTINY_SOFT_COOLDOWN_PREFIX = "[[WTP_DISCOVERY_MUTINY_SOFT_READY_TURN="
DISCOVERY_MUTINY_SOFT_COOLDOWN_SUFFIX = "]]"

def _getDiscoveryMutinySoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(DISCOVERY_MUTINY_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(DISCOVERY_MUTINY_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(DISCOVERY_MUTINY_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setDiscoveryMutinySoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(DISCOVERY_MUTINY_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_MUTINY_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_MUTINY_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		DISCOVERY_MUTINY_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		DISCOVERY_MUTINY_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _startDiscoveryMutinySoftCooldown(player):
	if player.isNone():
		return

	iCooldownTurns = _scaleTurnsByGameSpeed(15)

	_setDiscoveryMutinySoftCooldownReadyTurn(
		player,
		CyGame().getGameTurn() + iCooldownTurns
	)

def _isDiscoveryMutinySoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getDiscoveryMutinySoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _getDistanceToNearestOwnCity(player, plot):
	if player.isNone() or plot.isNone():
		return 99

	iBest = 99
	(city, iter) = player.firstCity(True)
	while city:
		iDist = plotDistance(plot.getX(), plot.getY(), city.getX(), city.getY())
		if iDist < iBest:
			iBest = iDist
		(city, iter) = player.nextCity(iter, True)

	return iBest

def _getDiscoveryMutinyChance(player, plot):
	iDistance = _getDistanceToNearestOwnCity(player, plot)

	# Scale for large maps (Gigantic tuned)
	iScaledDistance = min(iDistance, 120) / 6

	if _isDiscoveryMutinySoftCooldownActive(player):
		iChance = (1 + iScaledDistance / 4) * 2
		return min(8, int(iChance))

	# Normal chance
	iChance = (1 + iScaledDistance / 2) * 2
	return min(20, int(iChance))

def _spawnDiscoveryMutinyHostileAdjacent(plot, iHostileUnitClass):
	if plot is None or plot.isNone():
		return None

	if iHostileUnitClass == -1:
		return None

	iBarbarian = gc.getGame().getBarbarianPlayer()
	barbPlayer = gc.getPlayer(iBarbarian)
	if barbPlayer.isNone():
		return None

	barbCiv = gc.getCivilizationInfo(barbPlayer.getCivilizationType())
	iUnitType = barbCiv.getCivilizationUnits(iHostileUnitClass)
	if iUnitType == UnitTypes.NO_UNIT:
		return None

	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			if iDX == 0 and iDY == 0:
				continue

			pLoop = plotXY(plot.getX(), plot.getY(), iDX, iDY)
			if pLoop is None or pLoop.isNone():
				continue
			if pLoop.isWater():
				continue
			if pLoop.isImpassable():
				continue
			if pLoop.isPeak():
				continue
			if pLoop.isCity():
				continue
			if pLoop.isUnit():
				continue

			pUnit = barbPlayer.initUnit(
				iUnitType,
				ProfessionTypes.NO_PROFESSION,
				pLoop.getX(),
				pLoop.getY(),
				UnitAITypes.NO_UNITAI,
				DirectionTypes.DIRECTION_SOUTH,
				0
			)

			if pUnit is not None and not pUnit.isNone():
				return pUnit

	return None

def canTriggerDiscoveryMutiny(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False

	if not player.isPlayable():
		return False

	if player.isNative():
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False

	# Exact unit / plot binding to prevent ghost triggers
	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return False

	if plot.isWater():
		return False

	if plot.isCity():
		return False

	# Must be outside own borders
	if plot.getOwner() == player.getID():
		return False

	iChance = _getDiscoveryMutinyChance(player, plot)

	if CyGame().getSorenRandNum(100, "Discovery Mutiny Trigger") >= iChance:
		return False

	return True

def applyDiscoveryMutinyPay(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	# Exact unit / plot binding to prevent invalid execution
	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if plot.isWater():
		return

	if plot.isCity():
		return

	# Safety: must still be outside own borders
	if plot.getOwner() == player.getID():
		return

	# Movement bonus for this turn
	try:
		unit.changeMoves(-60 * 2)
	except:
		pass

	_startDiscoveryMutinySoftCooldown(player)

def applyDiscoveryMutinyFight(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	# Exact unit / plot binding to prevent invalid execution
	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if plot.isWater():
		return

	if plot.isCity():
		return

	# Safety: must still be outside own borders
	if plot.getOwner() == player.getID():
		return

	iHostileUnitClass = event.getGenericParameter(1)
	iNumHostiles = event.getGenericParameter(2)

	if iHostileUnitClass == -1:
		return

	if iNumHostiles < 1:
		iNumHostiles = 1
	if iNumHostiles > 1:
		iNumHostiles = 1

	hostileUnit = _spawnDiscoveryMutinyHostileAdjacent(plot, iHostileUnitClass)
	if hostileUnit is not None and not hostileUnit.isNone():
		if hostileUnit.canMoveInto(plot, True, False, False):
			hostileUnit.attack(plot, False)

	_startDiscoveryMutinySoftCooldown(player)

def getHelpDiscoveryMutiny(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return u""

	unit = player.getUnit(kTriggeredData.iUnitId)
	szUnitName = u""
	if unit is not None and not unit.isNone():
		szUnitName = unit.getName()

	if event.getType() == "EVENT_DISCOVERY_EVENTS_MUTINY_1":
		return localText.getText(
			"TXT_KEY_EVENT_DISCOVERY_EVENTS_MUTINY_HELP_FIGHT",
			()
		)

	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_EVENTS_MUTINY_HELP_PAY",
		(szUnitName,)
	)

######## The DISCOVERY EVENTS BRAVE FELLOWS EVENT ###########

DISCOVERY_BRAVE_FELLOWS_SOFT_COOLDOWN_PREFIX = "[[WTP_DISCOVERY_BRAVE_FELLOWS_SOFT_READY_TURN="
DISCOVERY_BRAVE_FELLOWS_SOFT_COOLDOWN_SUFFIX = "]]"

def _getDiscoveryBraveFellowsSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(DISCOVERY_BRAVE_FELLOWS_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(DISCOVERY_BRAVE_FELLOWS_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(DISCOVERY_BRAVE_FELLOWS_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setDiscoveryBraveFellowsSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(DISCOVERY_BRAVE_FELLOWS_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_BRAVE_FELLOWS_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_BRAVE_FELLOWS_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		DISCOVERY_BRAVE_FELLOWS_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		DISCOVERY_BRAVE_FELLOWS_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _startDiscoveryBraveFellowsSoftCooldown(player):
	if player.isNone():
		return

	_setDiscoveryBraveFellowsSoftCooldownReadyTurn(player, CyGame().getGameTurn() + 30)

def _isDiscoveryBraveFellowsSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getDiscoveryBraveFellowsSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _getDiscoveryBraveFellowsChance(player):
	if _isDiscoveryBraveFellowsSoftCooldownActive(player):
		return 20

	return 35

def _getDiscoveryBraveFellowsVillageNativePlayer(player, plot):
	if player.isNone() or plot is None or plot.isNone():
		return None

	# Prefer city owner (village)
	if plot.isCity():
		city = plot.getPlotCity()
		if city is not None and not city.isNone():
			iOwner = city.getOwner()
			if iOwner >= 0:
				nativePlayer = gc.getPlayer(iOwner)
				if not nativePlayer.isNone() and nativePlayer.isNative():
					return nativePlayer

	# Fallback: plot owner
	iOwner = plot.getOwner()
	if iOwner < 0:
		return None

	nativePlayer = gc.getPlayer(iOwner)
	if nativePlayer.isNone() or not nativePlayer.isNative():
		return None

	return nativePlayer

def _isDiscoveryBraveFellowsFriendlyVillage(player, plot):
	nativePlayer = _getDiscoveryBraveFellowsVillageNativePlayer(player, plot)
	if nativePlayer is None:
		return False

	if gc.getTeam(player.getTeam()).isAtWar(nativePlayer.getTeam()):
		return False

	# Testwise lowered by one step: pleased or better
	return nativePlayer.AI_getAttitude(player.getID()) >= AttitudeTypes.ATTITUDE_PLEASED

def _applyDiscoveryBraveFellowsVillageRelationBonus(player, plot, iBonus):
	if player.isNone() or iBonus == 0:
		return

	nativePlayer = _getDiscoveryBraveFellowsVillageNativePlayer(player, plot)
	if nativePlayer is None:
		return

	player.AI_changeAttitudeExtra(nativePlayer.getID(), iBonus)
	nativePlayer.AI_changeAttitudeExtra(player.getID(), iBonus)

def canTriggerDiscoveryBraveFellows(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone() or not player.isPlayable() or player.isNative():
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return False

	if not isNativeVillage(argsList):
		return False

	if unit.getProfession() != gc.getInfoTypeForString("PROFESSION_SCOUT"):
		return False

	nativePlayer = _getDiscoveryBraveFellowsVillageNativePlayer(player, plot)
	if nativePlayer is None:
		return False

	if gc.getTeam(player.getTeam()).isAtWar(nativePlayer.getTeam()):
		return False

	if nativePlayer.AI_getAttitude(player.getID()) < AttitudeTypes.ATTITUDE_CAUTIOUS:
		return False

	iChance = _getDiscoveryBraveFellowsChance(player)
	if CyGame().getSorenRandNum(100, "Discovery Brave Fellows Trigger") >= iChance:
		return False

	return True

def applyDiscoveryBraveFellowsMap(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)

	if player.isNone() or unit.isNone():
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if not isNativeVillage(argsList):
		return

	iRadius = 4
	if _isDiscoveryBraveFellowsFriendlyVillage(player, plot):
		iRadius = 5

	for iX in range(-iRadius, iRadius + 1):
		for iY in range(-iRadius, iRadius + 1):
			if (iX * iX) + (iY * iY) > (iRadius * iRadius):
				continue

			pLoop = plotXY(plot.getX(), plot.getY(), iX, iY)
			if pLoop is None or pLoop.isNone():
				continue

			pLoop.setRevealed(player.getTeam(), True, False, -1)

	_applyDiscoveryBraveFellowsVillageRelationBonus(player, plot, 1)
	_startDiscoveryBraveFellowsSoftCooldown(player)

def applyDiscoveryBraveFellowsAdvice(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)

	if player.isNone() or unit.isNone():
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if not isNativeVillage(argsList):
		return

	if _isDiscoveryBraveFellowsFriendlyVillage(player, plot):
		unit.changeExperience(1, -1, False, False, False)

	_applyDiscoveryBraveFellowsVillageRelationBonus(player, plot, 1)
	_startDiscoveryBraveFellowsSoftCooldown(player)

def applyDiscoveryBraveFellowsWarriors(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)

	if player.isNone() or unit.isNone():
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if not isNativeVillage(argsList):
		return

	spawnOwnPlayerUnitOnSamePlotAsPlot(argsList)

	_applyDiscoveryBraveFellowsVillageRelationBonus(player, plot, 1)
	_startDiscoveryBraveFellowsSoftCooldown(player)

def getHelpDiscoveryBraveFellows1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	iUnitClass = event.getGenericParameter(1)

	if iUnitClass == -1:
		return u""

	UnitClass = gc.getUnitClassInfo(iUnitClass)
	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_1",
		(300, UnitClass.getTextKey(), 1)
	)

def getHelpDiscoveryBraveFellows2(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return localText.getText(
			"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_2",
			(200, 9, 9, 1)
		)

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return localText.getText(
			"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_2",
			(200, 9, 9, 1)
		)

	plot = unit.plot()
	if plot is None or plot.isNone():
		return localText.getText(
			"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_2",
			(200, 9, 9, 1)
		)

	if _isDiscoveryBraveFellowsFriendlyVillage(player, plot):
		return localText.getText(
			"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_2_FRIENDLY",
			(200, 11, 11, 1)
		)

	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_2",
		(200, 9, 9, 1)
	)

def getHelpDiscoveryBraveFellows3(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return localText.getText(
			"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_3",
			(1,)
		)

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return localText.getText(
			"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_3",
			(1,)
		)

	plot = unit.plot()
	if plot is None or plot.isNone():
		return localText.getText(
			"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_3",
			(1,)
		)

	if _isDiscoveryBraveFellowsFriendlyVillage(player, plot):
		return localText.getText(
			"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_3_FRIENDLY",
			(1,)
		)

	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_EVENTS_BRAVE_FELLOWS_HELP_3",
		(1,)
	)

######## The Lost Tribe ###########

def canTriggerLostTribe(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	unit = player.getUnit(kTriggeredData.iUnitId)
	eScout = gc.getInfoTypeForString("PROFESSION_SCOUT")
	if unit.getProfession() != eScout:
		return False
	# Read parameter 3 from the event as random chance
	if TriggerChance(argsList):
		return True
	return False

def canDoLostTribe4(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	(unit, iter) = player.firstUnit()
	while (unit):
		if unit.getUnitClassType() == CvUtil.findInfoTypeNum('UNITCLASS_SCOUT'):
			return False
		(unit, iter) = player.nextUnit(iter)
	return True

def getHelpLostTribe4(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	szHelp = getHelpChangeFatherPoints(argsList)
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_SCOUT'))
	UnitClass2 = gc.getUnitClassInfo(unit.getUnitClassType())
	UnitProf1 = gc.getProfessionInfo(unit.getProfession())
	szHelp += "\n" + localText.getText("TXT_KEY_EVENT_LOST_TRIBE_4_HELP", (UnitClass2.getTextKey(), UnitProf1.getTextKey(), UnitClass.getTextKey()))
	if not canDoLostTribe4(argsList):
		szHelp += "\n\n" + localText.getText("TXT_KEY_EVENT_LOST_TRIBE_4B_HELP", (UnitClass.getTextKey(),))
	return szHelp

def applyLostTribe4(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	ChangeFatherPoints(argsList)
	iUnitClassType = CvUtil.findInfoTypeNum('UNITCLASS_SCOUT')
	iProfession = CvUtil.findInfoTypeNum("PROFESSION_SCOUT")
	iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClassType)
	if iUnitType != -1:
		player.initUnit(iUnitType, iProfession, kTriggeredData.iPlotX, kTriggeredData.iPlotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH, 0)
	(unitnew, iter) = player.firstUnit()
	while (unitnew):
		if unitnew.getUnitClassType() == CvUtil.findInfoTypeNum('UNITCLASS_SCOUT'):
			break
		(unitnew, iter) = player.nextUnit(iter)
	unit = player.getUnit(kTriggeredData.iUnitId)
	unitnew.convert(unit)

######## Pacific Quest ###########

def canTriggerPacificDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iAchieve = gc.getInfoTypeForString("ACHIEVE_PACIFIC")
	#CyInterface().addImmediateMessage("iAchieve "+str(iAchieve), "")
	if player.isAchieveGained(iAchieve):
		return True
	return False


######## VOLCANO ###########

def canApplyVolcano1(argsList):
	iEvent = argsList[1]
	kTriggeredData = argsList[0]

	iNumImprovements = 0
	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			loopPlot = plotXY(kTriggeredData.iPlotX, kTriggeredData.iPlotY, iDX, iDY)
			if not loopPlot.isNone():
				if (iDX != 0 or iDY != 0):
					if loopPlot.getImprovementType() != -1:
						iNumImprovements += 1

	return (iNumImprovements > 0)

def applyVolcano1(argsList):
	iEvent = argsList[1]
	kTriggeredData = argsList[0]

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	plot.setPlotType(PlotTypes.PLOT_LAND, True, True)
	plot.setFeatureType(gc.getInfoTypeForString('FEATURE_VOLCANO'), 0)

	listPlots = []
	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			loopPlot = plotXY(kTriggeredData.iPlotX, kTriggeredData.iPlotY, iDX, iDY)
			if not loopPlot.isNone():
				if (iDX != 0 or iDY != 0):
					if loopPlot.getImprovementType() != -1:
						listPlots.append(loopPlot)

	listRuins = []
	listRuins.append(CvUtil.findInfoTypeNum('IMPROVEMENT_FARM'))
	listRuins.append(CvUtil.findInfoTypeNum('IMPROVEMENT_PLANTATION'))


	iRuins = CvUtil.findInfoTypeNum('IMPROVEMENT_CITY_RUINS')

	for i in range(3):
		if len(listPlots) > 0:
			plot = listPlots[gc.getGame().getSorenRandNum(len(listPlots), "Volcano event improvement destroyed")]
			iImprovement = plot.getImprovementType()
			szBuffer = localText.getText("TXT_KEY_EVENT_CITY_IMPROVEMENT_DESTROYED", (gc.getImprovementInfo(iImprovement).getTextKey(), ))
			CyInterface().addMessage(kTriggeredData.ePlayer, False, gc.getEVENT_MESSAGE_TIME(), szBuffer, "AS2D_BOMBARDED", InterfaceMessageTypes.MESSAGE_TYPE_INFO, gc.getImprovementInfo(iImprovement).getButton(), gc.getInfoTypeForString("COLOR_RED"), plot.getX(), plot.getY(), True, True)
			if iImprovement in listRuins:
				plot.setImprovementType(iRuins)
			else:
				plot.setImprovementType(-1)
			listPlots.remove(plot)

			if i == 1 and gc.getGame().getSorenRandNum(100, "Volcano event num improvements destroyed") < 50:
				break


######## VOLCANO DORMANT ###########

def canTriggerVolcanoDormant1(argsList):
	kTriggeredData = argsList[0]
	if kTriggeredData.getRandomNumberForIndex(0) < 250:
		return True
	return False

def applyVolcanoDormant1(argsList):
	iEvent = argsList[1]
	kTriggeredData = argsList[0]

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	plot.setPlotType(PlotTypes.PLOT_PEAK, True, True)

######## TORNADO ###########

def applyTornado1(argsList):
	iEvent = argsList[1]
	kTriggeredData = argsList[0]

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	plot.setFeatureType(gc.getInfoTypeForString('FEATURE_TORNADO'), 0)

######## BABY BOOM ###########

def canTriggerBabyBoom(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	team = gc.getTeam(player.getTeam())
	if team.getAtWarCount() > 0:
		return False
	if not TriggerChance(argsList):
		return False
	#for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
	#	if iLoopTeam != player.getTeam():
	#		if team.AI_getAtPeaceCounter(iLoopTeam) == 1:
	#			CyInterface().addImmediateMessage("True!", "")
	#			return true
	#CyInterface().addImmediateMessage("anderes", "")
	return True

def ApplyBabyBoom(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	count = 0
	# Check all Cities for growth
	(loopCity, iter) = player.firstCity(False)
	while(loopCity):
		if gc.getGame().getSorenRandNum(100, "(c) TAC 2010 Events") < event.getGenericParameter(1):
			if not loopCity.isNone():
				loopCity.setFood(loopCity.growthThreshold())
				count += 1
				# Break if the max numbe of Cities is reached
		if count > event.getGenericParameter(2):
			break
		(loopCity, iter) = player.nextCity(iter, False)
	# Wenn keine Stadt Wachstum hat, eine festlegen
	if count < 1:
		city.setFood(city.growthThreshold())

def getHelpBabyBoom(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	if event.getGenericParameter(2) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_BABY_BOOM_HELP", (event.getGenericParameter(2),))
	return szHelp

######## Flaute ###########

def isValidUnitTravelStateForTravel(unit):
	ts = unit.getUnitTravelState()
	return (ts == UnitTravelStates.UNIT_TRAVEL_STATE_FROM_EUROPE or
			ts == UnitTravelStates.UNIT_TRAVEL_STATE_TO_EUROPE or
			ts == UnitTravelStates.UNIT_TRAVEL_STATE_FROM_AFRICA or
			ts == UnitTravelStates.UNIT_TRAVEL_STATE_TO_AFRICA or
			ts == UnitTravelStates.UNIT_TRAVEL_STATE_FROM_PORT_ROYAL or
			ts == UnitTravelStates.UNIT_TRAVEL_STATE_TO_PORT_ROYAL)

def isValidUnitTravelStateForPort(unit):
	ts = unit.getUnitTravelState()
	return (ts == UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE or
			ts == UnitTravelStates.UNIT_TRAVEL_STATE_IN_AFRICA or
			ts == UnitTravelStates.UNIT_TRAVEL_STATE_IN_PORT_ROYAL)

def canApplyCalm(argsList):
	eEvent = argsList[1]
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False
	if (isValidUnitTravelStateForPort(unit)):
		return False
	return True

def applyCalm(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	turn = Speed.getStoragePercent()/100
	if not unit.isNone() and isValidUnitTravelStateForTravel(unit):
		unit.setUnitTravelTimer(unit.getUnitTravelTimer() + turn)

def getHelpCalm(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	turn = Speed.getStoragePercent()/100
	szHelp = ""
	if not unit.isNone() and isValidUnitTravelStateForTravel(unit):
		szHelp = localText.getText("TXT_KEY_EVENT_CALM_HELP", (turn, unit.getName()))
	return szHelp

######## Tailwind ###########

def applyTailwind(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	turn = Speed.getStoragePercent()/100
	if not unit.isNone():
		if event.getGenericParameter(1) > 0 :
			if (isValidUnitTravelStateForTravel(unit)):
				if unit.getUnitTravelTimer() > turn :
					unit.setUnitTravelTimer(unit.getUnitTravelTimer() - turn)
				else:
					unit.setUnitTravelTimer(1)
			else:
				unit.changeMoves(-60 * event.getGenericParameter(1))

def canApplyTailwind(argsList):
	eEvent = argsList[1]
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	turn = Speed.getStoragePercent()/100
	if unit.isNone():
		return False
	if (isValidUnitTravelStateForPort(unit)):
		return False
	if (isValidUnitTravelStateForTravel(unit)):
		if unit.getUnitTravelTimer() <= 1 :
			return False
	return True

def getHelpTailwind(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	turn = Speed.getStoragePercent()/100
	szHelp = ""
	if not unit.isNone():
		if event.getGenericParameter(1) > 0 :
			if (isValidUnitTravelStateForTravel(unit)):
				szHelp = localText.getText("TXT_KEY_EVENT_TAILWIND_HELP_2", (turn, unit.getName()))
			else:
				szHelp = localText.getText("TXT_KEY_EVENT_TAILWIND_HELP_1", (event.getGenericParameter(1), unit.getName()))
	return szHelp

######## RUNAWAY - Entlaufene Pferde ###########

def canTriggerRunAway(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if player.isNone() or player2.isNone() :
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_RUNAWAY_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	if city.getYieldStored(iYield) < -quantity*2 :
		return False
	return True

def applyRunAway1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	nativecity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	# Re-check the event pre-condition (the game state may have changed inbetween canTriggerRunAway
	#   and applyRunAway1)
	# Note: This check should help prevent the city from ending up with
	#   negative horses
	if city.getYieldStored(iYield) < -quantity*2 :
		return

	city.changeYieldStored(iYield, quantity)
	nativecity.changeYieldStored(iYield, -quantity)

def getHelpRunAway1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	nativecity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = ""
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (-quantity,  gc.getYieldInfo(iYield).getChar(), nativecity.getNameKey()))
	return szHelp

######## Terra X Quest ###########

def canTriggerTerraX(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	(city, iter) = player.firstCity(True)
	while(city):
		if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
			return True
		(city, iter) = player.nextCity(iter, True)
	return False

def getHelpTerraX(argsList):
	worldsize = gc.getWorldInfo(CyMap().getWorldSize())
	szHelp = localText.getText("TXT_KEY_EVENT_TERRAX_HELP", (str(3+(3*worldsize.getBuildingClassPrereqModifier()/100)),))
	return szHelp

def canTriggerTerraXDone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	inlandcity = 0
	(city, iter) = player.firstCity(True)
	while(city):
		if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
			inlandcity += 1
		(city, iter) = player.nextCity(iter, True)
	worldsize = gc.getWorldInfo(CyMap().getWorldSize())
	if inlandcity >= 3+(3*worldsize.getBuildingClassPrereqModifier()/100):
		return True
	return False

def isExpiredTerraX(argsList):
	eEvent = argsList[1]
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	worldsize = gc.getWorldInfo(CyMap().getWorldSize())
	for j in range(gc.getMAX_PLAYERS()):
		if j != kTriggeredData.ePlayer:
			otherplayer = gc.getPlayer(j)
			if (otherplayer.isAlive() and otherplayer.isPlayable()):
				inlandcity = 0
				(city, iter) = otherplayer.firstCity(True)
				while(city):
					if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
						inlandcity += 1
					(city, iter) = otherplayer.nextCity(iter, True)
				if inlandcity >= 3+(3*worldsize.getBuildingClassPrereqModifier()/100):
					return True
	return False

######## Forrest Fire ###########

def applyForestFire(argsList):
	eEvent = argsList[1]
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	CyEngine().triggerEffect(gc.getInfoTypeForString("EFFECT_SETTLERSMOKE"), pPlot.getPoint())

def applyForestFire4(argsList):
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return

	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if pPlot is None:
		return

	# Visual effect
	CyEngine().triggerEffect(gc.getInfoTypeForString("EFFECT_CITY_BIG_BURNING_SMOKE"), pPlot.getPoint())

	# Only human players
	if not player.isHuman():
		return

	city = None
	if kTriggeredData.iCityId != -1:
		city = player.getCity(kTriggeredData.iCityId)
		if city.isNone():
			city = None

	popupInfo = CyPopupInfo()
	popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)

	if city is not None:
		popupInfo.setText(localText.getText("TXT_KEY_EVENT_FOREST_FIRE_4", (city.getNameKey(),)))
	else:
		popupInfo.setText(localText.getText("TXT_KEY_EVENT_FOREST_FIRE_4", ()))

	popupInfo.addPopup(kTriggeredData.ePlayer)

######## Cargospace ###########

def canTriggerCargoSpace(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	unit = player.getUnit(kTriggeredData.iUnitId)
	if city.getX() == unit.getX() and city.getY() == unit.getY():
		return True
	return False

def applyCargoSpace(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	# apply is executed in sync, so random will not cause OOS
	if gc.getGame().getSorenRandNum(100, "(c) TAC 2010 Events") < event.getGenericParameter(3):
		if event.getGenericParameter(1) >= 0:
			unit.changeFreePromotionCount(event.getGenericParameter(1), 1)
			CyInterface().addImmediateMessage(localText.getText("TXT_KEY_EVENT_CARGOSPACE_SUCCESS", (unit.getName(),)), "")
	else:
		CyInterface().addImmediateMessage(localText.getText("TXT_KEY_EVENT_CARGOSPACE_FAILED", ()), "")
	if event.getGenericParameter(2) > 0:
		unit.setImmobileTimer(event.getGenericParameter(2))

def helpCargoSpace(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unit = player.getUnit(kTriggeredData.iUnitId)
	szHelp = ""
	if event.getGenericParameter(1) >= 0:
		iCargoSlots = gc.getPromotionInfo(event.getGenericParameter(1)).getCargoChange()
		szHelp = localText.getText("TXT_KEY_EVENT_CARGOSPACE_HELP", (iCargoSlots, unit.getName(), event.getGenericParameter(3)))
	if event.getGenericParameter(2) > 0:
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_IMMOBILE_UNIT", (event.getGenericParameter(2), unit.getName()))
	return szHelp

######## Anti Pirate ###########

def canTriggerAntiPirate(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	iKilledTradeships = 0
	i=0
	eEvent = gc.getEventTriggerInfo(kTriggeredData.eTrigger).getEvent(0)
	event = gc.getEventInfo(eEvent)
	if player.isInRevolution():
		return False
	for i in (UnitTypes.UNIT_CARAVEL, UnitTypes.UNIT_FLUYT, UnitTypes.UNIT_MERCHANTMAN, UnitTypes.UNIT_WHALING_BOAT, UnitTypes.UNIT_CARRACK, UnitTypes.UNIT_CARAVELA_REDONDA, UnitTypes.UNIT_WEST_INDIAMAN, UnitTypes.UNIT_BRIGANTINE):
		iKilledTradeships += CyStatistics().getPlayerNumUnitsLost(kTriggeredData.ePlayer, i)
	if iKilledTradeships >= event.getGenericParameter(1):
		(loopUnit, iter) = player.firstUnit()
		while(loopUnit):
			if loopUnit.getUnitType() in (UnitTypes.UNIT_FRIGATE, UnitTypes.UNIT_SHIP_OF_THE_LINE, UnitTypes.UNIT_COLONIAL_MAN_O_WAR):
				return False
			(loopUnit, iter) = player.nextUnit(iter)
		return True
	return False

######## RUM BLOSSOM ###########

def canTriggerRumBlossom(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if player.isNone() or player2.isNone() :
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_RUM_BLOSSOM_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyRumBlossom1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	nativecity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity:
		return
	city.changeYieldStored(iYield, quantity)
	nativecity.changeYieldStored(iYield, -quantity)

def getHelpRumBlossom1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	nativecity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = ""
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (-quantity,  gc.getYieldInfo(iYield).getChar(), nativecity.getNameKey()))
	return szHelp

def canApplyRumBlossom3(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if player.isNone() or player2.isNone() :
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from event and check if enough yield is stored in city
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

######## Ruins Quest ###########

def isExpiredRuins(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	improvementtype = gc.getInfoTypeForString("IMPROVEMENT_CITY_RUINS")
	if (plot.getOwner() != kTriggeredData.ePlayer):
		return True
	if plot.getImprovementType() != improvementtype:
		return True
	if gc.getGame().getGameTurn() >= kTriggeredData.iTurn + event.getGenericParameter(1):
		return True
	return False

def getHelpRuins(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_SCOUT'))
	szHelp = localText.getText("TXT_KEY_EVENT_RUINS_HELP", (UnitClass.getTextKey(), city.getNameKey(), event.getGenericParameter(1)))
	return szHelp

def applyRuins5(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iUnitClassType = CvUtil.findInfoTypeNum('UNITCLASS_CARRIER')
	iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClassType)
	if iUnitType != -1:
		player.initUnit(iUnitType, 0, kTriggeredData.iPlotX, kTriggeredData.iPlotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH, 0)

def getHelpRuins5(argsList):
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_CARRIER'))
	szHelp = localText.getText("TXT_KEY_EVENT_BONUS_UNIT", (1, UnitClass.getTextKey(), ))
	return szHelp

######## Native Trade Quests ###########

def isExpiredNativeWagonTrade(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getGame().getGameTurn() >= kTriggeredData.iTurn + event.getGenericParameter(1):
		return True
	if not player.isPlayable():
		return True
	return False

def getHelpNativeWagonTrade(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_WAGON_TRAIN'))
	szHelp = localText.getText("TXT_KEY_EVENT_NATIVE_TRADE_WAGON_HELP", (UnitClass.getTextKey(), city.getNameKey(), event.getGenericParameter(1)))
	return szHelp

def applyNativeWagonTrade5(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iUnitClassType = CvUtil.findInfoTypeNum('UNITCLASS_WAGON_TRAIN')
	iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClassType)
	if iUnitType != -1:
		player.initUnit(iUnitType, 0, kTriggeredData.iPlotX, kTriggeredData.iPlotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH, 0)

def getHelpNativeWagonTrade5(argsList):
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_WAGON_TRAIN'))
	szHelp = localText.getText("TXT_KEY_EVENT_BONUS_UNIT", (1, UnitClass.getTextKey(), ))
	return szHelp

def getHelpNativeNeighborTrade(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_WAGON_TRAIN'))
	szHelp = localText.getText("TXT_KEY_EVENT_FRIENDLY_TRADE_WITH_NATIVE_NEIGHBORS_HELP", (UnitClass.getTextKey(), city.getNameKey(), event.getGenericParameter(1)))
	return szHelp

def applyNativeNeighborTrade5(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iUnitClassType = CvUtil.findInfoTypeNum('UNITCLASS_EXPERT_TRADER')
	iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClassType)
	if iUnitType != -1:
		player.initUnit(iUnitType, 0, kTriggeredData.iPlotX, kTriggeredData.iPlotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH, 0)

def getHelpNativeNeighborTrade5(argsList):
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_EXPERT_TRADER'))
	szHelp = localText.getText("TXT_KEY_EVENT_BONUS_UNIT", (1, UnitClass.getTextKey(), ))
	return szHelp

def getHelpNativeNeighborTrade2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_TREK'))
	szHelp = localText.getText("TXT_KEY_EVENT_FRIENDLY_TRADE_WITH_NATIVE_NEIGHBORS_HELP", (UnitClass.getTextKey(), city.getNameKey(), event.getGenericParameter(1)))
	return szHelp

def getHelpNativeNeighborTradeBetrayal(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_TREK'))
	szHelp = localText.getText("TXT_KEY_EVENT_TRADE_WITH_NATIVE_BETRAYAL_HELP", (UnitClass.getTextKey(), city.getNameKey(), event.getGenericParameter(1)))
	return szHelp

####### The Royals Event ########

getHelpTheRoyals1  = get_simple_help("TXT_KEY_EVENT_THE_ROYALS_1PYTHON")
getHelpTheRoyals2  = get_simple_help("TXT_KEY_EVENT_THE_ROYALS_2PYTHON")
getHelpTheRoyals3  = get_simple_help("TXT_KEY_EVENT_THE_ROYALS_3PYTHON")
getHelpTheRoyals4  = get_simple_help("TXT_KEY_EVENT_THE_ROYALS_4PYTHON")
getHelpTheRoyals2a = get_simple_help("TXT_KEY_EVENT_THE_ROYALS_2aPYTHON")

# ============================================================
# PIRATES
# ============================================================

PIRATES_SOFT_COOLDOWN_PREFIX = "[[WTP_PIRATES_READY_TURN="
PIRATES_SOFT_COOLDOWN_SUFFIX = "]]"
PIRATES_FOUR_TREASURES_OVERLAP_PREFIX = "[[WTP_PIRATES_FOUR_TREASURES_OVERLAP="
PIRATES_FOUR_TREASURES_OVERLAP_SUFFIX = "]]"

def _getPiratesSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(PIRATES_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(PIRATES_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(PIRATES_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setPiratesSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(PIRATES_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(PIRATES_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(PIRATES_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		PIRATES_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		PIRATES_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _getPiratesScaledTurns(iBaseTurns):
	gameSpeedType = CyGame().getGameSpeedType()
	iPercent = gc.getGameSpeedInfo(gameSpeedType).getGrowthPercent()
	return max(1, int((iBaseTurns * iPercent) / 100))

def _startPiratesSoftCooldown(player, iBaseTurns):
	if player.isNone():
		return

	iReadyTurn = CyGame().getGameTurn() + _getPiratesScaledTurns(iBaseTurns)
	_setPiratesSoftCooldownReadyTurn(player, iReadyTurn)

def _isPiratesSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getPiratesSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _getPiratesFourTreasuresOverlapLock(player):
	if player is None or player.isNone():
		return False

	szData = player.getScriptData()
	if szData is None or szData == "":
		return False

	iStart = szData.find(PIRATES_FOUR_TREASURES_OVERLAP_PREFIX)
	if iStart == -1:
		return False

	iStart += len(PIRATES_FOUR_TREASURES_OVERLAP_PREFIX)
	iEnd = szData.find(PIRATES_FOUR_TREASURES_OVERLAP_SUFFIX, iStart)
	if iEnd == -1:
		return False

	try:
		return int(szData[iStart:iEnd]) == 1
	except:
		return False

def _setPiratesFourTreasuresOverlapLock(player, bLocked):
	if player is None or player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(PIRATES_FOUR_TREASURES_OVERLAP_PREFIX)
	if iStart != -1:
		iEnd = szData.find(PIRATES_FOUR_TREASURES_OVERLAP_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(PIRATES_FOUR_TREASURES_OVERLAP_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	iValue = 0
	if bLocked:
		iValue = 1

	szMarker = "%s%d%s" % (
		PIRATES_FOUR_TREASURES_OVERLAP_PREFIX,
		iValue,
		PIRATES_FOUR_TREASURES_OVERLAP_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _clearPiratesFourTreasuresOverlapLock(player):
	if player is None or player.isNone():
		return

	_setPiratesFourTreasuresOverlapLock(player, False)

def _getPiratesScaledStorageAmount(iBaseAmount):
	if iBaseAmount == 0:
		return 0

	iPercent = gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getStoragePercent()
	iAmount = int((abs(iBaseAmount) * iPercent) / 100)

	if iAmount <= 0:
		iAmount = 1

	if iBaseAmount < 0:
		return -iAmount

	return iAmount

def _plotHasAdjacentSeaWater(plot):
	if plot is None or plot.isNone():
		return False

	for iDirection in range(DirectionTypes.NUM_DIRECTION_TYPES):
		adjPlot = plotDirection(plot.getX(), plot.getY(), DirectionTypes(iDirection))
		if adjPlot and not adjPlot.isNone():
			if adjPlot.isWater() and not adjPlot.isLake():
				return True

	return False

def _cityHasEuropeAccess(city):
	if city.isNone():
		return False

	if city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return True

	if _plotHasAdjacentSeaWater(city.plot()):
		return True

	return False

def _countPiratesTreasureCities(player):
	if player is None or player.isNone():
		return 0

	eTreasureClass = gc.getInfoTypeForString("UNITCLASS_TREASURE")
	iCityCount = 0

	(city, iter) = player.firstCity(True)
	while city:
		if not city.isNone():
			plot = city.plot()
			if plot is not None and not plot.isNone():
				bHasTreasure = False

				for i in range(plot.getNumUnits()):
					unit = plot.getUnit(i)
					if unit is None or unit.isNone():
						continue
					if unit.getOwner() != player.getID():
						continue

					eUnitClass = gc.getUnitInfo(unit.getUnitType()).getUnitClassType()
					if eUnitClass == eTreasureClass:
						bHasTreasure = True
						break

				if bHasTreasure:
					iCityCount += 1

		(city, iter) = player.nextCity(iter, True)

	return iCityCount

def _hasPiratesRequiredTreasureCities(player):
	return _countPiratesTreasureCities(player) >= 3

def _getPiratesValidatedTriggerData(kTriggeredData, bRequireTreasureOnCityPlot):
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return (None, None, None)

	if not player.isPlayable():
		return (None, None, None)

	if player.isNative():
		return (None, None, None)

	city = player.getCity(kTriggeredData.iCityId)
	if city.isNone():
		return (None, None, None)

	if city.getOwner() != kTriggeredData.ePlayer:
		return (None, None, None)

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return (None, None, None)

	iTreasureClass = gc.getInfoTypeForString("UNITCLASS_TREASURE")
	if unit.getUnitClassType() != iTreasureClass:
		return (None, None, None)

	plot = unit.plot()
	if plot is None or plot.isNone():
		return (None, None, None)

	if bRequireTreasureOnCityPlot:
		if city.getX() != unit.getX() or city.getY() != unit.getY():
			return (None, None, None)

		if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
			return (None, None, None)

	return (player, city, unit)

def canTriggerPirates(argsList):
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return False

	if not player.isPlayable():
		return False

	if player.isNative():
		return False

	if _isPiratesSoftCooldownActive(player):
		return False

	city = player.getCity(kTriggeredData.iCityId)
	if city.isNone():
		return False

	if city.getOwner() != kTriggeredData.ePlayer:
		return False

	if not _cityHasEuropeAccess(city):
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False

	iTreasureClass = gc.getInfoTypeForString("UNITCLASS_TREASURE")
	if unit.getUnitClassType() != iTreasureClass:
		return False

	if city.getX() != unit.getX() or city.getY() != unit.getY():
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return False

	# Require treasure in at least 3 different own cities
	if not _hasPiratesRequiredTreasureCities(player):
		return False

	# One-time overlap lock:
	# If Four Treasures is currently valid too, block Pirates only once per overlap phase.
	bFourTreasuresValidNow = canTriggerFourTreasures(argsList)
	bOverlapAlreadyLocked = _getPiratesFourTreasuresOverlapLock(player)

	if bFourTreasuresValidNow:
		if not bOverlapAlreadyLocked:
			_setPiratesFourTreasuresOverlapLock(player, True)
			return False
	else:
		if bOverlapAlreadyLocked:
			_clearPiratesFourTreasuresOverlapLock(player)

	# Start cooldown on trigger intentionally.
	# This event has a delayed branch and the player must have time to move the treasure away
	# without the trigger reappearing immediately every turn.
	_startPiratesSoftCooldown(player, 25)
	return True

def getHelpPirates1(argsList):
	return localText.getText("TXT_KEY_EVENT_PIRATES_1_HELP", ())

def CanDoPirates3(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)

	player, city, unit = _getPiratesValidatedTriggerData(kTriggeredData, True)
	if player is None:
		return False

	iYield = gc.getInfoTypeForString("YIELD_BLADES")
	iAmount = _getPiratesScaledStorageAmount(event.getGenericParameter(1))

	if iAmount >= 0:
		return True

	if city.getYieldStored(iYield) < -iAmount:
		return False

	return True

def CanDoPirates4(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)

	player, city, unit = _getPiratesValidatedTriggerData(kTriggeredData, True)
	if player is None:
		return False

	iYield = gc.getInfoTypeForString("YIELD_MUSKETS")
	iAmount = _getPiratesScaledStorageAmount(event.getGenericParameter(1))

	if iAmount >= 0:
		return True

	if city.getYieldStored(iYield) < -iAmount:
		return False

	return True

def applyPirates3(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)

	player, city, unit = _getPiratesValidatedTriggerData(kTriggeredData, True)
	if player is None:
		return

	iYield = gc.getInfoTypeForString("YIELD_BLADES")
	iAmount = _getPiratesScaledStorageAmount(event.getGenericParameter(1))

	if iAmount < 0 and city.getYieldStored(iYield) < -iAmount:
		return

	if iAmount != 0:
		city.changeYieldStored(iYield, iAmount)

def applyPirates4(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)

	player, city, unit = _getPiratesValidatedTriggerData(kTriggeredData, True)
	if player is None:
		return

	iYield = gc.getInfoTypeForString("YIELD_MUSKETS")
	iAmount = _getPiratesScaledStorageAmount(event.getGenericParameter(1))

	if iAmount < 0 and city.getYieldStored(iYield) < -iAmount:
		return

	if iAmount != 0:
		city.changeYieldStored(iYield, iAmount)

def getHelpPirates3(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)

	player, city, unit = _getPiratesValidatedTriggerData(kTriggeredData, True)
	if player is None:
		return u""

	iYield = gc.getInfoTypeForString("YIELD_BLADES")
	iAmount = _getPiratesScaledStorageAmount(event.getGenericParameter(1))

	szHelp = u""
	if iAmount != 0:
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (iAmount, gc.getYieldInfo(iYield).getChar(), city.getNameKey()))

	return szHelp

def getHelpPirates4(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)

	player, city, unit = _getPiratesValidatedTriggerData(kTriggeredData, True)
	if player is None:
		return u""

	iYield = gc.getInfoTypeForString("YIELD_MUSKETS")
	iAmount = _getPiratesScaledStorageAmount(event.getGenericParameter(1))

	szHelp = u""
	if iAmount != 0:
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (iAmount, gc.getYieldInfo(iYield).getChar(), city.getNameKey()))

	return szHelp

def isExpiredPirates1a(argsList):
	kTriggeredData = argsList[0]

	player, city, unit = _getPiratesValidatedTriggerData(kTriggeredData, False)
	if player is None:
		return True

	return False

def applyPirates1a(argsList):
	kTriggeredData = argsList[0]

	player, city, unit = _getPiratesValidatedTriggerData(kTriggeredData, False)
	if player is None:
		return

	if city.getX() == unit.getX() and city.getY() == unit.getY():
		iX = city.getX()
		iY = city.getY()
		szCityName = city.getName()

		unit.kill(False)

		if player.isHuman():
			CyInterface().addMessage(
				kTriggeredData.ePlayer,
				False,
				gc.getEVENT_MESSAGE_TIME(),
				CyTranslator().changeTextColor(
					localText.getText("TXT_KEY_EVENT_PIRATES_1A_STOLEN", (szCityName,)),
					ColorTypes(7)
				),
				None,
				InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
				None,
				ColorTypes(7),
				iX,
				iY,
				True,
				True
			)
		return

	iPirateCutterClass = gc.getInfoTypeForString("UNITCLASS_PIRATE_CUTTER")
	if iPirateCutterClass == -1:
		return

	city.spawnBarbarianUnitOnAdjacentPlotOfCity(iPirateCutterClass)

	if player.isHuman():
		CyInterface().addMessage(
			kTriggeredData.ePlayer,
			False,
			gc.getEVENT_MESSAGE_TIME(),
			CyTranslator().changeTextColor(
				localText.getText("TXT_KEY_EVENT_PIRATES_1A_CUTTER", (city.getName(),)),
				ColorTypes(7)
			),
			None,
			InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
			None,
			ColorTypes(7),
			city.getX(),
			city.getY(),
			True,
			True
		)

        
######## Superstitious Pirates Event ###########

def canTriggerSupersitiousPirates(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if player.isNone() :
		return False
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	city = player.getCity(kTriggeredData.iCityId)
	unit = player.getUnit(kTriggeredData.iUnitId)
	if city.getX() == unit.getX() and city.getY() == unit.getY():
		return True
	return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_SUPERSTITIOUS_PIRATES_2")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity*2 :
		return False
	return True

def applySupersitiousPirates2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity:
		return
	city.changeYieldStored(iYield, quantity)

def getHelpSupersitiousPirates2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_RUM")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	szHelp = ""
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	return szHelp

####### TAC Events - General Functions########

######## Units Funktionen ###########

def CreateTreasure(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iUnitClassType = CvUtil.findInfoTypeNum('UNITCLASS_TREASURE')
	iTreasure = event.getGenericParameter(1) + gc.getGame().getSorenRandNum(event.getGenericParameter(2), "Ronnar")
	iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClassType)
	if iUnitType != -1:
		player.initUnit(iUnitType, 0, kTriggeredData.iPlotX, kTriggeredData.iPlotY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH, iTreasure)

def getHelpCreateTreasure(argsList):
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_TREASURE'))
	szHelp = localText.getText("TXT_KEY_EVENT_BONUS_UNIT", (1, UnitClass.getTextKey(), ))
	return szHelp

def countUnits(argsList, iUnitType):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iUnitsCurrent = 0
	(loopUnit, iter) = player.firstUnit()
	while(loopUnit):
		if iUnitType == loopUnit.getUnitType():
			iUnitsCurrent += 1
		(loopUnit, iter) = player.nextUnit(iter)

	for i in range(player.getNumEuropeUnits()):
		loopUnit = player.getEuropeUnit(i)
		if iUnitType == loopUnit.getUnitType():
			iUnitsCurrent += 1

	(city, iter) = player.firstCity(True)
	while(city):
		for iCitizen in range(city.getPopulation()):
			Unit = city.getPopulationUnitByIndex(iCitizen)
			if iUnitType == Unit.getUnitType():
				iUnitsCurrent += 1
		(city, iter) = player.nextCity(iter, True)
	return iUnitsCurrent

def CheckCarpenter(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if not player.isPlayable():
		return False

	iUnitType = CvUtil.findInfoTypeNum('UNIT_CARPENTER')
	iUnitsCurrent = countUnits(argsList, iUnitType)
	if iUnitsCurrent > 0:
		return True
	return False


######## Helper Method to count Units in all Cities ###########
######## This can also be used for PLOT TRIGGER or UNIT TRIGGER ###########

def countUnitsColonies(argsList, iUnitType):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iUnitsCurrent = 0
	(city, iter) = player.firstCity(True)
	while(city):
		for iCitizen in range(city.getPopulation()):
			Unit = city.getPopulationUnitByIndex(iCitizen)
			if iUnitType == Unit.getUnitType():
				iUnitsCurrent += 1
		(city, iter) = player.nextCity(iter, True)
	return iUnitsCurrent

######## Helper Method to count Units in specific City ###########
######## This requires a CITY TRIGGER ###########
def countUnitsInCityForCityTrigger(argsList, iUnitType):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)
	iCity = argsList[2]
	city = player.getCity(iCity)

	iUnitsCurrent = 0
	for iCitizen in range(city.getPopulation()):
		Unit = city.getPopulationUnitByIndex(iCitizen)
		if iUnitType == Unit.getUnitType():
			iUnitsCurrent += 1

	return iUnitsCurrent

###### Cheese Maker Event ######
def CheckCheesemakerInCity(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)

	if not player.isPlayable():
		return False

	# you could add checks for several Units like this
	iUnitType = CvUtil.findInfoTypeNum('UNIT_CHEESE_MAKER')
	iUnitsCurrent = countUnitsInCityForCityTrigger(argsList, iUnitType)
	if iUnitsCurrent == 0:
		return False

	return True

######## Bonus Funktionen ###########

def CanApplyBonus(argsList):
	eEvent = argsList[1]
	kTriggeredData = argsList[0]
	event = gc.getEventInfo(eEvent)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	bonustype = event.getGenericParameter(1)
	# CyInterface().addImmediateMessage(str(kTriggeredData.iPlotX) + ", " + str(kTriggeredData.iPlotY), "")
	if plot.isNone():
		return False
	if not plot.canHaveBonus(bonustype, False):
		return False
	#if not plot.isBeingWorked():
	#	return False
	return True

def CanApplyBonusOcean(argsList):
	eEvent = argsList[1]
	kTriggeredData = argsList[0]
	event = gc.getEventInfo(eEvent)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	bonustype = event.getGenericParameter(1)
	# CyInterface().addImmediateMessage(str(kTriggeredData.iPlotX) + ", " + str(kTriggeredData.iPlotY), "")
	if plot.isNone():
		return False
	if not plot.canHaveBonus(bonustype, False):
		return False
	return True

def SetBonus(argsList):
	eEvent = argsList[1]
	kTriggeredData = argsList[0]
	event = gc.getEventInfo(eEvent)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	bonustype = event.getGenericParameter(1)
	if not plot.isNone() and plot.canHaveBonus(bonustype, False):
		plot.setBonusType(bonustype)

def getHelpBonus(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	bonustype = event.getGenericParameter(1)
	szHelp = ""
	if bonustype != -1 :
		szHelp = localText.getText("TXT_KEY_EVENT_BONUS_HELP", (gc.getBonusInfo(bonustype).getTextKey(),))
	return szHelp

######## Landmark Funktionen ###########

def CheckLandmark(argsList):
	eEvent = argsList[1]
	kTriggeredData = argsList[0]
	event = gc.getEventInfo(eEvent)
	szLandmark = "TXT_KEY_%s_LANDMARK"%(event.getType())
	for i in range (CyEngine().getNumSigns()):
		Sign = CyEngine().getSignByIndex(i)
		if (Sign.getPlot().getX() == kTriggeredData.iPlotX and Sign.getPlot().getY() == kTriggeredData.iPlotY):
			return False
	return True

def SetLandmark(argsList):
	eEvent = argsList[1]
	kTriggeredData = argsList[0]
	event = gc.getEventInfo(eEvent)
	if GlobalDefines.SHOW_LANDMARKS == 1:
		szLandmark = "TXT_KEY_%s_LANDMARK"%(event.getType())
		plot = gc.getMap().plot(kTriggeredData.iPlotX,  kTriggeredData.iPlotY)
		CyEngine().addSign(plot, -1, szLandmark)

######## Founding Father Functions ###########

def ChangeFatherPoints(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	team = gc.getTeam(player.getTeam())
	FatherPointChange = 0
	if event.getGenericParameter(1)!=-1:
		Handicap = gc.getHandicapInfo(CyGame().getHandicapType())
		Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
		FatherPointChange = event.getGenericParameter(2)*Speed.getFatherPercent()/100*Handicap.getFatherPercent()/100
		team.changeFatherPoints(event.getGenericParameter(1), FatherPointChange)

def getHelpChangeFatherPoints(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	FatherPointChange = 0
	szHelp = ""
	if event.getGenericParameter(1)!=-1:
		Handicap = gc.getHandicapInfo(CyGame().getHandicapType())
		Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
		FatherPointChange = event.getGenericParameter(2)*Speed.getFatherPercent()/100*Handicap.getFatherPercent()/100
		szHelp = localText.getText("TXT_KEY_EVENT_FATHER_POINTS", (FatherPointChange, gc.getFatherPointInfo(event.getGenericParameter(1)).getChar(), gc.getFatherPointInfo(event.getGenericParameter(1)).getDescription()))
	return szHelp

######## Trigger Funktionen ###########

def hasAllBuildings(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	trigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	iNumTriggerBuildings = trigger.getNumBuildingsRequired()
	if city.isNone() or iNumTriggerBuildings<=0:
		return False
	bHasAllBuildings = True
	i = 0
	for i in range(iNumTriggerBuildings):
		iBuilding = trigger.getBuildingRequired(i)
		eBuilding = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationBuildings(iBuilding)
		#CyInterface().addImmediateMessage("iBuilding "+str(iBuilding) + "eBuilding "+str(eBuilding)+str(city.isHasBuilding(eBuilding)) , "")
		if not city.isHasBuilding(eBuilding):
			bHasAllBuildings = False
	return bHasAllBuildings

def has_plot_this_bonus(*bonus_strings):

	def bonus_check(argsList):
		pTriggeredData = argsList[0]
		player = gc.getPlayer(pTriggeredData.ePlayer)
		if not player.isPlayable():
			return False
		plot = gc.getMap().plot(pTriggeredData.iPlotX, pTriggeredData.iPlotY)
		bonustypes =[ gc.getInfoTypeForString(bonus_string) for bonus_string in bonus_strings ]
		if plot.getOwner() != pTriggeredData.ePlayer:
			return False
		if plot.getBonusType() in bonustypes:
			return True
		return False

	return bonus_check

hasSilverBonus = has_plot_this_bonus("BONUS_SILVER")
hasGoldBonus = has_plot_this_bonus("BONUS_GOLD")
hasFurBonus = has_plot_this_bonus("BONUS_FUR")
hasCottonBonus = has_plot_this_bonus("BONUS_COTTON")
hasSugarBonus = has_plot_this_bonus("BONUS_SUGAR")
hasTobaccoBonus = has_plot_this_bonus("BONUS_TOBACCO")
hasIronBonus = has_plot_this_bonus("BONUS_IRON")
hasCocoaBonus = has_plot_this_bonus("BONUS_COCOA")
hasMineralBonus = has_plot_this_bonus("BONUS_MINERALS")
hasTimberBonus = has_plot_this_bonus("BONUS_TIMBER")
# 2023-11-xx : please put all relevant bonus
hasFoodBonus = has_plot_this_bonus("BONUS_POTATO","BONUS_BANANA","BONUS_CORN")
hasSeaFoodBonus = has_plot_this_bonus("BONUS_PEARLS","BONUS_CRAB","BONUS_FISH")
hasBisonBonus = has_plot_this_bonus("BONUS_BISON")
hasPumpkinBonus = has_plot_this_bonus("BONUS_PUMPKIN")
hasTurkeyBonus = has_plot_this_bonus("BONUS_TURKEYS")
hasGiantTreeBonus = has_plot_this_bonus("BONUS_GIANT_TREE")

######## HALLOWEEN Event Start ###########

def _playerHasPumpkinBonus(player):
	if player.isNone():
		return False
	if not player.isPlayable():
		return False

	iPumpkinBonus = gc.getInfoTypeForString("BONUS_PUMPKIN")
	map = gc.getMap()

	for iPlot in range(map.numPlots()):
		plot = map.plotByIndex(iPlot)
		if plot is None:
			continue
		if plot.isNone():
			continue
		if plot.getOwner() != player.getID():
			continue
		if plot.getBonusType() == iPumpkinBonus:
			return True

	return False


def _isHalloweenSeasonNow():
	game = CyGame()
	gameSpeed = gc.getGameSpeedInfo(game.getGameSpeedType())
	iMonthIncrement = gameSpeed.getGameTurnInfo(0).iMonthIncrement
	iCurrentTurn = game.getGameTurn()
	szDate = CyGameTextMgr().getTimeStr(iCurrentTurn + 1, True)

	October = localText.getText("TXT_KEY_MONTH_OCTOBER", ())

	# Month-based speeds: Halloween only in October
	if iMonthIncrement < 6:
		if October in szDate:
			return True
		return False

	# Half-year speeds: Halloween only in the second half of the year
	if iMonthIncrement == 6:
		if October in szDate:
			return True

		# Fallback if month names are not clearly exposed in the date string
		if (iCurrentTurn % 2) == 1:
			return True

		return False

	# Year-based speeds: Halloween can occur once per year
	return True


def _getHalloweenTriggerCity(kTriggeredData, player):
	if player.isNone():
		return None

	plot = CyMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if plot is None:
		return None
	if plot.isNone():
		return None

	city = plot.getWorkingCity()
	if city is None:
		return None
	if city.isNone():
		return None
	if city.getOwner() != player.getID():
		return None

	return city


def canTriggerHalloween(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	# Keep the pumpkin requirement, but player-wide instead of plot-only
	if not _playerHasPumpkinBonus(player):
		return False

	if not _isHalloweenSeasonNow():
		return False

	# The settlement connected to the triggering farm plot must have enough food
	city = _getHalloweenTriggerCity(kTriggeredData, player)
	if city is None:
		return False

	iFood = gc.getInfoTypeForString("YIELD_FOOD")
	if city.getYieldStored(iFood) < 50:
		return False

	return True
    
######## HALLOWEEN Event End ###########

######## THANKSGIVING Event Start ###########

def _playerHasTurkeyBonus(player):
	if player.isNone():
		return False
	if not player.isPlayable():
		return False

	iTurkeyBonus = gc.getInfoTypeForString("BONUS_TURKEYS")
	map = gc.getMap()

	for iPlot in range(map.numPlots()):
		plot = map.plotByIndex(iPlot)
		if plot is None:
			continue
		if plot.isNone():
			continue
		if plot.getOwner() != player.getID():
			continue
		if plot.getBonusType() == iTurkeyBonus:
			return True

	return False


def _isThanksgivingSeasonNow():
	game = CyGame()
	gameSpeed = gc.getGameSpeedInfo(game.getGameSpeedType())
	iMonthIncrement = gameSpeed.getGameTurnInfo(0).iMonthIncrement
	iCurrentTurn = game.getGameTurn()
	szDate = CyGameTextMgr().getTimeStr(iCurrentTurn + 1, True)

	November = localText.getText("TXT_KEY_MONTH_NOVEMBER", ())

	# Month-based speeds: Thanksgiving only in November
	if iMonthIncrement < 6:
		if November in szDate:
			return True
		return False

	# Half-year speeds: Thanksgiving only in the second half of the year
	if iMonthIncrement == 6:
		if November in szDate:
			return True

		# Fallback if month names are not clearly exposed in the date string
		if (iCurrentTurn % 2) == 1:
			return True

		return False

	# Year-based speeds: Thanksgiving can occur once per year
	return True


def _getThanksgivingTriggerCity(kTriggeredData, player):
	if player.isNone():
		return None

	plot = CyMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if plot is None:
		return None
	if plot.isNone():
		return None

	city = plot.getWorkingCity()
	if city is None:
		return None
	if city.isNone():
		return None
	if city.getOwner() != player.getID():
		return None

	return city


def canTriggerThanksgiving(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	# Keep the original turkey requirement, but player-wide instead of plot-only
	if not _playerHasTurkeyBonus(player):
		return False

	if not _isThanksgivingSeasonNow():
		return False

	# The settlement connected to the triggering farm plot must have enough food
	city = _getThanksgivingTriggerCity(kTriggeredData, player)
	if city is None:
		return False

	iFood = gc.getInfoTypeForString("YIELD_FOOD")
	if city.getYieldStored(iFood) < 100:
		return False

	return True
######## THANKSGIVING Event End ###########

def hasNoBonus(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	plot = gc.getMap().plot(pTriggeredData.iPlotX, pTriggeredData.iPlotY)
	#if (plot.getOwner() != pTriggeredData.ePlayer):
	#	return False
	if (plot.getBonusType() == -1):
		return True
	return False

def hasNoBonusAndIsPlayable(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	plot = gc.getMap().plot(pTriggeredData.iPlotX, pTriggeredData.iPlotY)
	if (plot.getOwner() != pTriggeredData.ePlayer):
		return False
	if (plot.getBonusType() == -1):
		return True
	return False

def isPlayable(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if player.isPlayable():
		return True
	else:
		return False

def isHuman(argsList):
	pTriggeredData = argsList[0]
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if player.isHuman():
		return True
	else:
		return False

def TriggerChance(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	# Read parameter 3 from the first event as random chance
	eventtrigger = gc.getEventTriggerInfo(kTriggeredData.eTrigger)
	eEvent = eventtrigger.getEvent(0)
	event = gc.getEventInfo(eEvent)
	if kTriggeredData.getRandomNumberForIndex(0) < event.getGenericParameter(3):
		return True
	return False

######## ORLANTH EVENTS ########

def canTriggerKingFurious(argsList):
	return False
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False
	if player.isNative():
		return False
	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False
	if king.AI_getAttitude(ePlayer) > 0:
		return False
	if player.isInRevolution():
		return False
	return True

def canTriggerKingHappy(argsList):
	return False
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False
	if player.isNative():
		return False
	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False
	if king.AI_getAttitude(ePlayer) > 4:
		return False
	if player.isInRevolution():
		return False
	return True

def canDoNotInRevolution(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False
	if player.isNative():
		return False
	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False
	if player.isInRevolution():
		return False
	return True

def canDoInRevolution(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)
	if player.isNative():
		return False
	if player.isInRevolution():
		return True
	return False

def canTriggerDeliverLumber(argsList):
	pTriggeredData = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False
	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False
	city = player.getCity(iCity)
	if city.isNone():
		return False
	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_DELIVER_LUMBER")
	event = gc.getEventInfo(eEvent)
	iYield = gc.getInfoTypeForString("YIELD_LUMBER")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	if city.getYieldStored(iYield) < -quantity:
		return False
	return True

def canTriggerDeliverCoats(argsList):
	pTriggeredData = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False
	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False
	city = player.getCity(iCity)
	if city.isNone():
		return False
	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_DELIVER_COATS")
	event = gc.getEventInfo(eEvent)
	iYield = gc.getInfoTypeForString("YIELD_COATS")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	if city.getYieldStored(iYield) < -quantity:
		return False
	return True

def CanDoRequisitionDeliver(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	yields = {
		1 : "YIELD_LUMBER",
		2 : "YIELD_COATS",
		3 : "YIELD_CLOTH"
		}
	iChoose = yields[event.getGenericParameter(2)]
	iYield = gc.getInfoTypeForString(iChoose)
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if city.isNone():
		return False
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	if city.getYieldStored(iYield) < -quantity:
		return False
	return True

def applyRequisitionDeliver(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(3))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(3))
	yields = {
		1 : "YIELD_LUMBER",
		2 : "YIELD_COATS",
		3 : "YIELD_CLOTH"
		}
	iChoose = yields[event.getGenericParameter(2)]
	iYield = gc.getInfoTypeForString(iChoose)
	iPrice = king.getYieldBuyPrice(iYield)

	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity:
		return
	city.changeYieldStored(iYield, quantity)
	king.setYieldBuyPrice(iYield, iPrice+event.getGenericParameter(4), 1)

def getHelpRequisition(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	city = player.getCity(kTriggeredData.iCityId)
	yields = {
		1 : "YIELD_LUMBER",
		2 : "YIELD_COATS",
		3 : "YIELD_CLOTH"
		}
	iChoose = yields[event.getGenericParameter(2)]
	iYield = gc.getInfoTypeForString(iChoose)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	szHelp = localText.getText("TXT_KEY_EVENT_REQUISITION_HELP", ())
	if event.getGenericParameter(1) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (quantity, gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	if event.getGenericParameter(1) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity, gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE", (event.getGenericParameter(4), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_DECREASE", (event.getGenericParameter(4), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

def applyKingPleased(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(3))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(3))
	if event.getGenericParameter(4) == 1 :
		player.NBMOD_DecreaseMaxTaxRate()

def getHelpKingPleased(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	if event.getGenericParameter(3) > 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_KING_PLEASED_HELP", ())
	if event.getGenericParameter(3) < 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_KING_ANGRY_HELP", ())
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXDECREASE", (-GlobalDefines.DECREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.DECREASE_MAX_TAX_RATE))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXINCREASE", (-GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if 'szHelp' in locals():
		return szHelp
	else:
		sys.stderr.write(event.getType() + " has PythonHelp getHelpKingPleased without setting generic parameters 3/4 to use it to generate output")

def applyKingAngry(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(3))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(3))
	if event.getGenericParameter(4) == 1 :
		player.NBMOD_IncreaseMaxTaxRate()

def getHelpKingAngry(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	szHelp = localText.getText("TXT_KEY_EVENT_KING_ANGRY_HELP", ())
	if event.getGenericParameter(4) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAXINCREASE", (-GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()-GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(3) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

def canTriggerHorsethief(argsList):
	eEvent = gc.getInfoTypeForString("EVENT_HORSETHIEF_2")
	event = gc.getEventInfo(eEvent)
	ePlayer = argsList[1]
	iCity = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity:
		return False
	return True

def canTriggerCattlethief(argsList):
	eEvent = gc.getInfoTypeForString("EVENT_CATTLETHIEF_1")
	event = gc.getEventInfo(eEvent)
	ePlayer = argsList[1]
	iCity = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	iYield = gc.getInfoTypeForString("YIELD_CATTLE")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity:
		return False
	return True

def applyHorsethief_2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity:
		return
	city.changeYieldStored(iYield, quantity)
	return True

def applyCattlethief_1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	iYield = gc.getInfoTypeForString("YIELD_CATTLE")
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity:
		return
	city.changeYieldStored(iYield, quantity)
	return True

def getHelpHorsethief_2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	szHelp = "Gain 1 Petty Criminal."
	szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	return szHelp

def getHelpCattlethief_1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_CATTLE")

	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	return szHelp

def canTriggerArchbishopric(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False
	iAchieve = gc.getInfoTypeForString("ACHIEVE_THREE_CHURCHES")
	if player.isAchieveGained(iAchieve):
		iAchieve = gc.getInfoTypeForString("ACHIEVE_TEN_CROSSES")
		if player.isAchieveGained(iAchieve):
			return True
	return False

def canTriggerNativeTrade(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False
	iAchieve = gc.getInfoTypeForString("ACHIEVE_FIVE_NATIVE_CONTACT")
	if player.isAchieveGained(iAchieve):
		return True
	return False

def canTriggerEuroTrade(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False
	iAchieve = gc.getInfoTypeForString("ACHIEVE_FOUR_EURO_CONTACT")
	if player.isAchieveGained(iAchieve):
		return True
	return False

def canTriggerPirateAttack1(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False
	iAchieve = gc.getInfoTypeForString("ACHIEVE_TENTHOUSAND_TRADE")
	if not player.isPlayable():
		return False
	if player.isAchieveGained(iAchieve):
		return True
	return False

def canTriggerPirateAttack2(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False
	iAchieve = gc.getInfoTypeForString("ACHIEVE_HUNDREDTHOUSAND_TRADE")
	if not player.isPlayable():
		return False
	if player.isAchieveGained(iAchieve):
		return True
	return False

def canTriggerTavernVsChapel(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCity)
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	iSpecialBuildingTavern = gc.getInfoTypeForString("SPECIALBUILDING_TAVERN")
	iSpecialBuildingChapel = gc.getInfoTypeForString("SPECIALBUILDING_CROSSES")
	for iBuilding in range(gc.getNumBuildingInfos()):
		if gc.getBuildingInfo(iBuilding).getSpecialBuildingType() == iSpecialBuildingTavern:
			if city.isHasBuilding(iBuilding):
				return False
		if gc.getBuildingInfo(iBuilding).getSpecialBuildingType() == iSpecialBuildingChapel:
			if city.isHasBuilding(iBuilding):
				return False
	return True

def doPirateAttack1(argsList):
	iEvent = argsList[1]
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	bPlayer = gc.getPlayer(gc.getGame().getBarbarianPlayer())
	if pPlot.isNone() == False:
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIVATEER'), -1, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_PIRATE_SEA, DirectionTypes.DIRECTION_SOUTH, 0)
		newUnit2 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_PIRATE_CUTTER'), -1, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_PIRATE_SEA, DirectionTypes.DIRECTION_SOUTH, 0)

def doPirateAttack2(argsList):
	iEvent = argsList[1]
	kTriggeredData = argsList[0]
	pPlot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	bPlayer = gc.getPlayer(gc.getGame().getBarbarianPlayer())
	if pPlot.isNone() == False:
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_PIRATE_FRIGATE'), -1, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_PIRATE_SEA, DirectionTypes.DIRECTION_SOUTH, 0)
		newUnit2 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_PIRATE_FRIGATE'), -1, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_PIRATE_SEA, DirectionTypes.DIRECTION_SOUTH, 0)
		newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIVATEER'), -1, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_PIRATE_SEA, DirectionTypes.DIRECTION_SOUTH, 0)
		newUnit2 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_PIRATE_CUTTER'), -1, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_PIRATE_SEA, DirectionTypes.DIRECTION_SOUTH, 0)

######## BEER ROBBERY ###########

def canTriggerBeerRobbery(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if player.isNone() or player2.isNone() :
		return False
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_BEER_ROBBERY_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_BEER")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyBeerRobbery1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	othercity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_BEER")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return
	city.changeYieldStored(iYield, quantity)
	othercity.changeYieldStored(iYield, -quantity)

def getHelpBeerRobbery1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	othercity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_BEER")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = ""
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (-quantity,  gc.getYieldInfo(iYield).getChar(), othercity.getNameKey()))
	return szHelp

def canApplyBeerRobbery3(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if player.isNone() or player2.isNone() :
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from event and check if enough yield is stored in city

	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	iYield = gc.getInfoTypeForString("YIELD_BEER")
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

######## WINE THEFT ###########

def canTriggerWineTheft(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_WINE_THEFT_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_WINE")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyWineTheft1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_WINE")

	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return
	city.changeYieldStored(iYield, quantity)

def getHelpWineTheft1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_WINE")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = ""
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	return szHelp

######## LUXURY GOODS ###########

def canTriggerLuxuryGoods(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if player.isNone() :
		return False
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_LUXURY_GOODS_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_LUXURY_GOODS")

	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyLuxuryGoods1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_LUXURY_GOODS")

	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return
	city.changeYieldStored(iYield, quantity)

def getHelpLuxuryGoods1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_LUXURY_GOODS")
	szHelp = ""
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	return szHelp

######## Cattle and Sheep ###########

def canTriggerCattleAndSheep(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if player.isNone() :
		return False
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_CATTLE_AND_SHEEP_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_CATTLE")

	quantity1 = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity1 = quantity1 * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity1*2 :
		return False
	# Read Parameter 1 from the second event and check if enough yield is stored in city
	eEvent2 = gc.getInfoTypeForString("EVENT_CATTLE_AND_SHEEP_2")
	event2 = gc.getEventInfo(eEvent2)
	iYield = gc.getInfoTypeForString("YIELD_SHEEP")
	quantity2 = event2.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity2 = quantity2 * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity2*2 :
		return False
	return True

def applyCattleAndSheep1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_CATTLE")
	iYield2 = gc.getInfoTypeForString("YIELD_FOOD")
	iYield3 = gc.getInfoTypeForString("YIELD_HIDES")

	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) >= -quantity :
		city.changeYieldStored(iYield, quantity)
		city.changeYieldStored(iYield2, -quantity)
		city.changeYieldStored(iYield3, -quantity)

def getHelpCattleAndSheep1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_CATTLE")
	iYield2 = gc.getInfoTypeForString("YIELD_FOOD")
	iYield3 = gc.getInfoTypeForString("YIELD_HIDES")
	szHelp = ""
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (-quantity,  gc.getYieldInfo(iYield2).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (-quantity,  gc.getYieldInfo(iYield3).getChar(), city.getNameKey()))
	return szHelp

def applyCattleAndSheep2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_SHEEP")
	iYield2 = gc.getInfoTypeForString("YIELD_FOOD")
	iYield3 = gc.getInfoTypeForString("YIELD_WOOL")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) >= -quantity :
		city.changeYieldStored(iYield, quantity)
		city.changeYieldStored(iYield2, -quantity)
		city.changeYieldStored(iYield3, -quantity)

def getHelpCattleAndSheep2(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_SHEEP")
	iYield2 = gc.getInfoTypeForString("YIELD_FOOD")
	iYield3 = gc.getInfoTypeForString("YIELD_WOOL")
	szHelp=""
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (-quantity,  gc.getYieldInfo(iYield2).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (-quantity,  gc.getYieldInfo(iYield3).getChar(), city.getNameKey()))
	return szHelp

######## Horse Deal ###########

def canTriggerHorseDeal(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if player.isNone() :
		return False
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_HORSE_DEAL_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity*2 :
		return False
	return True

def applyHorseDeal1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return
	city.changeYieldStored(iYield, quantity)

def getHelpHorseDeal1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	szHelp = ""

	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	return szHelp

######## Seasoned Trader Horse Gift and Event Help ###########

def canTriggerHorseGift(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if player.isNone() :
		return False
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	city = player.getCity(kTriggeredData.iCityId)
	unit = player.getUnit(kTriggeredData.iUnitId)
	if city.getX() == unit.getX() and city.getY() == unit.getY():
		return True
	return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_SEASONED_TRADER_MEETING_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity*2 :
		return False
	return True

def applyHorseGift1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return
	city.changeYieldStored(iYield, quantity)

def getHelpHorseGift1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	szHelp = ""

	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	return szHelp

getHelpSeasonedTraderNo = get_simple_help("TXT_KEY_EVENT_SEASONED_TRADER_MEETING_HELP")

getHelpSeasonedScoutNativeCity = get_simple_help("TXT_KEY_EVENT_SEASONED_SCOUT_NATIVE_CITY_HELP")

######## Wild Animal ###########

def canApplyWildAnimal1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from event and check if enough yield is stored in city
	iYield = gc.getInfoTypeForString("YIELD_MUSKETS")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyWildAnimal1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_MUSKETS")

	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return
	city.changeYieldStored(iYield, quantity)

def getHelpWildAnimal1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_MUSKETS")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = ""
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	return szHelp

######## Native Events ###########

######## Discovery Failed Trader Change ###########

DISCOVERY_FAILED_TRADER_CHANGE_SOFT_COOLDOWN_PREFIX = "[[WTP_DISCOVERY_FAILED_TRADER_CHANGE_SOFT_READY_TURN="
DISCOVERY_FAILED_TRADER_CHANGE_SOFT_COOLDOWN_SUFFIX = "]]"

DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_PREFIX = "[[WTP_DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT="
DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_SUFFIX = "]]"

DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_PREFIX = "[[WTP_DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT="
DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_SUFFIX = "]]"

def _getDiscoveryFailedTraderChangeSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(DISCOVERY_FAILED_TRADER_CHANGE_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setDiscoveryFailedTraderChangeSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_FAILED_TRADER_CHANGE_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		DISCOVERY_FAILED_TRADER_CHANGE_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		DISCOVERY_FAILED_TRADER_CHANGE_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _startDiscoveryFailedTraderChangeSoftCooldown(player, iBaseTurns):
	if player.isNone():
		return

	iCooldown = _getDiscoveryFailedTraderChangeScaledTurns(iBaseTurns)
	_setDiscoveryFailedTraderChangeSoftCooldownReadyTurn(player, CyGame().getGameTurn() + iCooldown)

def _isDiscoveryFailedTraderChangeSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getDiscoveryFailedTraderChangeSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _getDiscoveryFailedTraderChangeScaledTurns(iBaseTurns):
	gameSpeedType = CyGame().getGameSpeedType()
	iPercent = gc.getGameSpeedInfo(gameSpeedType).getGrowthPercent()
	return max(1, int((iBaseTurns * iPercent) / 100))

def _getUnitClass(unit):
	if unit is None or unit.isNone():
		return -1
	return gc.getUnitInfo(unit.getUnitType()).getUnitClassType()

def _setDiscoveryFailedTraderSelectedUnitData(player, iUnitId, iPlotX, iPlotY):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	iStart = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szData += "%s%d%s" % (
		DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_PREFIX,
		iUnitId,
		DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_SUFFIX
	)

	szData += "%s%d,%d%s" % (
		DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_PREFIX,
		iPlotX,
		iPlotY,
		DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_SUFFIX
	)

	player.setScriptData(szData)

def _clearDiscoveryFailedTraderSelectedUnitData(player):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		return

	iStart = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	iStart = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	player.setScriptData(szData)

def _getDiscoveryFailedTraderSelectedUnitId(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_PREFIX)
	iEnd = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_UNIT_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _getDiscoveryFailedTraderSelectedPlot(player):
	if player.isNone():
		return (-1, -1)

	szData = player.getScriptData()
	if szData is None or szData == "":
		return (-1, -1)

	iStart = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_PREFIX)
	if iStart == -1:
		return (-1, -1)

	iStart += len(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_PREFIX)
	iEnd = szData.find(DISCOVERY_FAILED_TRADER_CHANGE_SELECTED_PLOT_SUFFIX, iStart)
	if iEnd == -1:
		return (-1, -1)

	try:
		szCoords = szData[iStart:iEnd]
		aParts = szCoords.split(",")
		if len(aParts) != 2:
			return (-1, -1)
		return (int(aParts[0]), int(aParts[1]))
	except:
		return (-1, -1)

def _isValidFailedTraderChangeUnit(player, unit, ePlayer):
	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	if unit is None or unit.isNone():
		return False

	iFailedTraderClass = gc.getInfoTypeForString("UNITCLASS_FAILED_TRADER")
	if _getUnitClass(unit) != iFailedTraderClass:
		return False

	eColonistProfession = gc.getInfoTypeForString("PROFESSION_COLONIST")
	if unit.getProfession() != eColonistProfession:
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False
	if plot.isWater():
		return False
	if plot.isCity():
		return False
	if plot.getOwner() != ePlayer:
		return False

	return True

def _findDiscoveryFailedTraderChangeCandidate(player):
	if player.isNone():
		return None

	(unit, iter) = player.firstUnit()
	while unit:
		if _isValidFailedTraderChangeUnit(player, unit, player.getID()):
			return unit
		(unit, iter) = player.nextUnit(iter)

	return None

def canTriggerDiscoveryFailedTraderChange(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	if _isDiscoveryFailedTraderChangeSoftCooldownActive(player):
		return False

	unit = _findDiscoveryFailedTraderChangeCandidate(player)
	if unit is None or unit.isNone():
		_clearDiscoveryFailedTraderSelectedUnitData(player)
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		_clearDiscoveryFailedTraderSelectedUnitData(player)
		return False

	_setDiscoveryFailedTraderSelectedUnitData(player, unit.getID(), plot.getX(), plot.getY())
	return True

def _getStoredDiscoveryFailedTraderUnit(player):
	if player.isNone():
		return None

	iUnitId = _getDiscoveryFailedTraderSelectedUnitId(player)
	if iUnitId < 0:
		return None

	unit = player.getUnit(iUnitId)
	if unit is None or unit.isNone():
		return None

	return unit

def changeFailedTraderToExpertTrader(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return
	if not player.isPlayable():
		return
	if player.isNative():
		return

	oldUnit = _getStoredDiscoveryFailedTraderUnit(player)
	if oldUnit is None or oldUnit.isNone():
		return

	if not _isValidFailedTraderChangeUnit(player, oldUnit, kTriggeredData.ePlayer):
		return

	plot = oldUnit.plot()
	if plot is None or plot.isNone():
		return

	iStoredPlotX, iStoredPlotY = _getDiscoveryFailedTraderSelectedPlot(player)
	if plot.getX() != iStoredPlotX or plot.getY() != iStoredPlotY:
		return

	iTargetUnitClass = event.getGenericParameter(1)
	if iTargetUnitClass <= 0:
		return

	bSeasoned = False
	iSeasonedChance = event.getGenericParameter(2)
	iSeasonedChance = max(0, min(100, iSeasonedChance))

	if iSeasonedChance > 0:
		if CyGame().getSorenRandNum(100, "Failed Trader seasoned chance") < iSeasonedChance:
			iSeasonedTraderClass = gc.getInfoTypeForString("UNITCLASS_SEASONED_TRADER")
			if iSeasonedTraderClass != UnitClassTypes.NO_UNITCLASS:
				iTargetUnitClass = iSeasonedTraderClass
				bSeasoned = True

	iNewUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iTargetUnitClass)
	if iNewUnitType == UnitTypes.NO_UNIT:
		return

	iX = oldUnit.getX()
	iY = oldUnit.getY()
	iDamage = oldUnit.getDamage()
	iExperience = oldUnit.getExperience()
	iMoves = oldUnit.movesLeft()

	szName = u""
	if oldUnit.getNameNoDesc():
		szName = oldUnit.getNameNoDesc()

	aPromotions = []
	for iPromotion in range(gc.getNumPromotionInfos()):
		if oldUnit.isHasPromotion(iPromotion):
			aPromotions.append(iPromotion)

	newUnit = player.initUnit(
		iNewUnitType,
		ProfessionTypes.NO_PROFESSION,
		iX,
		iY,
		UnitAITypes.NO_UNITAI,
		DirectionTypes.NO_DIRECTION,
		0
	)
	if newUnit.isNone():
		return

	eNativeTraderProfession = gc.getInfoTypeForString("PROFESSION_NATIVE_TRADER")
	if eNativeTraderProfession != ProfessionTypes.NO_PROFESSION:
		newUnit.setProfession(eNativeTraderProfession)

	if iDamage > 0:
		newUnit.setDamage(iDamage, PlayerTypes.NO_PLAYER)

	if iExperience > 0:
		newUnit.setExperience(iExperience, -1)

	for iPromotion in aPromotions:
		if newUnit.canAcquirePromotion(iPromotion):
			newUnit.setHasRealPromotion(iPromotion, True)

	if szName != u"":
		newUnit.setName(szName)

	try:
		newUnit.setMoves(iMoves)
	except:
		pass

	oldUnit.kill(False)

	_startDiscoveryFailedTraderChangeSoftCooldown(player, 30)
	_clearDiscoveryFailedTraderSelectedUnitData(player)

	if bSeasoned:
		CyInterface().addMessage(
			kTriggeredData.ePlayer,
			True,
			10,
			localText.getText("TXT_KEY_EVENT_DISCOVERY_FAILED_TRADER_SEASONED_RESULT", ()),
			"",
			0,
			"",
			ColorTypes(8),
			iX,
			iY,
			True,
			True
		)

def getHelpDiscoveryFailedTraderChange(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return u""

	iGoldCost = abs(event.getGold())
	iSeasonedChance = event.getGenericParameter(2)
	iCooldown = _getDiscoveryFailedTraderChangeScaledTurns(30)

	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_EVENTS_FAILED_TRADER_CHANGE_HELP",
		(iGoldCost, iSeasonedChance, iCooldown)
	)

def doDiscoveryFailedTraderChangeDecline(argsList):
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return
	if not player.isPlayable():
		return
	if player.isNative():
		return

	unit = _getStoredDiscoveryFailedTraderUnit(player)
	if unit is None or unit.isNone():
		return

	if not _isValidFailedTraderChangeUnit(player, unit, kTriggeredData.ePlayer):
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	iStoredPlotX, iStoredPlotY = _getDiscoveryFailedTraderSelectedPlot(player)
	if plot.getX() != iStoredPlotX or plot.getY() != iStoredPlotY:
		return

	_startDiscoveryFailedTraderChangeSoftCooldown(player, 30)
	_clearDiscoveryFailedTraderSelectedUnitData(player)

def getHelpDiscoveryFailedTraderChangeDecline(argsList):
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return u""

	iCooldown = _getDiscoveryFailedTraderChangeScaledTurns(30)

	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_EVENTS_FAILED_TRADER_CHANGE_DECLINE_HELP",
		(iCooldown,)
	)

######## Discovery Failed Missionary Change ###########

DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_COOLDOWN_PREFIX = "[[WTP_DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_READY_TURN="
DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_COOLDOWN_SUFFIX = "]]"

DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_PREFIX = "[[WTP_DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT="
DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_SUFFIX = "]]"

DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_PREFIX = "[[WTP_DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT="
DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_SUFFIX = "]]"

def _getDiscoveryFailedMissionaryChangeSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setDiscoveryFailedMissionaryChangeSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		DISCOVERY_FAILED_MISSIONARY_CHANGE_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _getDiscoveryFailedMissionaryChangeScaledTurns(iBaseTurns):
	gameSpeedType = CyGame().getGameSpeedType()
	iPercent = gc.getGameSpeedInfo(gameSpeedType).getGrowthPercent()
	return max(1, int((iBaseTurns * iPercent) / 100))

def _startDiscoveryFailedMissionaryChangeSoftCooldown(player, iBaseTurns):
	if player.isNone():
		return

	iCooldown = _getDiscoveryFailedMissionaryChangeScaledTurns(iBaseTurns)
	_setDiscoveryFailedMissionaryChangeSoftCooldownReadyTurn(player, CyGame().getGameTurn() + iCooldown)

def _isDiscoveryFailedMissionaryChangeSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getDiscoveryFailedMissionaryChangeSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _getDiscoveryFailedMissionaryUnitClass(unit):
	if unit is None or unit.isNone():
		return -1
	return gc.getUnitInfo(unit.getUnitType()).getUnitClassType()

def _setDiscoveryFailedMissionarySelectedUnitData(player, iUnitId, iPlotX, iPlotY):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	iStart = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szData += "%s%d%s" % (
		DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_PREFIX,
		iUnitId,
		DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_SUFFIX
	)

	szData += "%s%d,%d%s" % (
		DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_PREFIX,
		iPlotX,
		iPlotY,
		DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_SUFFIX
	)

	player.setScriptData(szData)

def _clearDiscoveryFailedMissionarySelectedUnitData(player):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		return

	iStart = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	iStart = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_PREFIX)
	if iStart != -1:
		iEnd = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	player.setScriptData(szData)

def _getDiscoveryFailedMissionarySelectedUnitId(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_PREFIX)
	iEnd = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_UNIT_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _getDiscoveryFailedMissionarySelectedPlot(player):
	if player.isNone():
		return (-1, -1)

	szData = player.getScriptData()
	if szData is None or szData == "":
		return (-1, -1)

	iStart = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_PREFIX)
	if iStart == -1:
		return (-1, -1)

	iStart += len(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_PREFIX)
	iEnd = szData.find(DISCOVERY_FAILED_MISSIONARY_CHANGE_SELECTED_PLOT_SUFFIX, iStart)
	if iEnd == -1:
		return (-1, -1)

	try:
		szCoords = szData[iStart:iEnd]
		aParts = szCoords.split(",")
		if len(aParts) != 2:
			return (-1, -1)
		return (int(aParts[0]), int(aParts[1]))
	except:
		return (-1, -1)

def _isValidFailedMissionaryChangeUnit(player, unit, ePlayer):
	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	if unit is None or unit.isNone():
		return False

	iFailedMissionaryClass = gc.getInfoTypeForString("UNITCLASS_FAILED_MISSIONARY")
	if _getDiscoveryFailedMissionaryUnitClass(unit) != iFailedMissionaryClass:
		return False

	eColonistProfession = gc.getInfoTypeForString("PROFESSION_COLONIST")
	if unit.getProfession() != eColonistProfession:
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False
	if plot.isWater():
		return False
	if plot.isCity():
		return False

	return True

def _findDiscoveryFailedMissionaryChangeCandidate(player):
	if player.isNone():
		return None

	(unit, iter) = player.firstUnit()
	while unit:
		if _isValidFailedMissionaryChangeUnit(player, unit, player.getID()):
			return unit
		(unit, iter) = player.nextUnit(iter)

	return None

def _getStoredDiscoveryFailedMissionaryUnit(player):
	if player.isNone():
		return None

	iUnitId = _getDiscoveryFailedMissionarySelectedUnitId(player)
	if iUnitId < 0:
		return None

	unit = player.getUnit(iUnitId)
	if unit is None or unit.isNone():
		return None

	return unit

def _getBestMissionaryTargetForPlayer(player):
	iMissionaryClass = gc.getInfoTypeForString("UNITCLASS_CHRISTIAN_MISSIONARY")
	if iMissionaryClass == -1:
		return (-1, -1, -1)

	iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iMissionaryClass)
	if iUnitType == UnitTypes.NO_UNIT:
		return (-1, -1, -1)

	eMissionaryProfession = gc.getInfoTypeForString("PROFESSION_MISSIONARY")
	if eMissionaryProfession == -1:
		return (-1, -1, -1)

	return (iMissionaryClass, iUnitType, eMissionaryProfession)

def canTriggerDiscoveryFailedMissionaryChange(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	if _isDiscoveryFailedMissionaryChangeSoftCooldownActive(player):
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit is None or unit.isNone():
		_clearDiscoveryFailedMissionarySelectedUnitData(player)
		return False

	if not _isValidFailedMissionaryChangeUnit(player, unit, kTriggeredData.ePlayer):
		_clearDiscoveryFailedMissionarySelectedUnitData(player)
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		_clearDiscoveryFailedMissionarySelectedUnitData(player)
		return False

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		_clearDiscoveryFailedMissionarySelectedUnitData(player)
		return False

	# Fixed trigger chance on valid plots
	if CyGame().getSorenRandNum(100, "Failed Missionary Change trigger") >= 30:
		_clearDiscoveryFailedMissionarySelectedUnitData(player)
		return False

	_setDiscoveryFailedMissionarySelectedUnitData(player, unit.getID(), plot.getX(), plot.getY())
	return True

def doDiscoveryFailedMissionaryChange(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return

	oldUnit = _getStoredDiscoveryFailedMissionaryUnit(player)
	if oldUnit is None or oldUnit.isNone():
		return

	if oldUnit.getID() != kTriggeredData.iUnitId:
		return

	if not _isValidFailedMissionaryChangeUnit(player, oldUnit, kTriggeredData.ePlayer):
		return

	plot = oldUnit.plot()
	if plot is None or plot.isNone():
		return

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	iStoredPlotX, iStoredPlotY = _getDiscoveryFailedMissionarySelectedPlot(player)
	if plot.getX() != iStoredPlotX or plot.getY() != iStoredPlotY:
		return

	iTargetUnitClass, iNewUnitType, eTargetProfession = _getBestMissionaryTargetForPlayer(player)
	if iTargetUnitClass == -1 or iNewUnitType == -1 or eTargetProfession == -1:
		return

	iX = oldUnit.getX()
	iY = oldUnit.getY()
	iDamage = oldUnit.getDamage()
	iExperience = oldUnit.getExperience()
	iMoves = oldUnit.movesLeft()

	szName = u""
	if oldUnit.getNameNoDesc():
		szName = oldUnit.getNameNoDesc()

	aPromotions = []
	for iPromotion in range(gc.getNumPromotionInfos()):
		if oldUnit.isHasPromotion(iPromotion):
			aPromotions.append(iPromotion)

	newUnit = player.initUnit(
		iNewUnitType,
		ProfessionTypes.NO_PROFESSION,
		iX,
		iY,
		UnitAITypes.NO_UNITAI,
		DirectionTypes.NO_DIRECTION,
		0
	)
	if newUnit.isNone():
		return

	if eTargetProfession != ProfessionTypes.NO_PROFESSION:
		newUnit.setProfession(eTargetProfession)

	if iDamage > 0:
		newUnit.setDamage(iDamage, PlayerTypes.NO_PLAYER)

	if iExperience > 0:
		newUnit.setExperience(iExperience, -1)

	for iPromotion in aPromotions:
		if newUnit.canAcquirePromotion(iPromotion):
			newUnit.setHasRealPromotion(iPromotion, True)

	if szName != u"":
		newUnit.setName(szName)

	try:
		newUnit.setMoves(iMoves)
	except:
		pass

	oldUnit.kill(False)

	_startDiscoveryFailedMissionaryChangeSoftCooldown(player, 30)
	_clearDiscoveryFailedMissionarySelectedUnitData(player)

def doDiscoveryFailedMissionaryChangeDecline(argsList):
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return

	unit = _getStoredDiscoveryFailedMissionaryUnit(player)
	if unit is None or unit.isNone():
		return

	if unit.getID() != kTriggeredData.iUnitId:
		return

	if not _isValidFailedMissionaryChangeUnit(player, unit, kTriggeredData.ePlayer):
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	iStoredPlotX, iStoredPlotY = _getDiscoveryFailedMissionarySelectedPlot(player)
	if plot.getX() != iStoredPlotX or plot.getY() != iStoredPlotY:
		return

	_startDiscoveryFailedMissionaryChangeSoftCooldown(player, 30)
	_clearDiscoveryFailedMissionarySelectedUnitData(player)

def getHelpDiscoveryFailedMissionaryChange(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return u""

	iCooldown = _getDiscoveryFailedMissionaryChangeScaledTurns(30)

	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_EVENTS_FAILED_MISSIONARY_CHANGE_HELP",
		(iCooldown,)
	)

def getHelpDiscoveryFailedMissionaryChangeDecline(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return u""

	iCooldown = _getDiscoveryFailedMissionaryChangeScaledTurns(30)

	return localText.getText(
		"TXT_KEY_EVENT_DISCOVERY_EVENTS_FAILED_MISSIONARY_CHANGE_DECLINE_HELP",
		(iCooldown,)
	)

######## Failed Missionary Classic ###########

FAILED_MISSIONARY_CLASSIC_SOFT_COOLDOWN_PREFIX = "[[WTP_FAILED_MISSIONARY_CLASSIC_SOFT_READY_TURN="
FAILED_MISSIONARY_CLASSIC_SOFT_COOLDOWN_SUFFIX = "]]"

FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_PREFIX = "[[WTP_FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT="
FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_SUFFIX = "]]"

FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_PREFIX = "[[WTP_FAILED_MISSIONARY_CLASSIC_SELECTED_CITY="
FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_SUFFIX = "]]"

def _getFailedMissionaryClassicSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(FAILED_MISSIONARY_CLASSIC_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(FAILED_MISSIONARY_CLASSIC_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(FAILED_MISSIONARY_CLASSIC_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setFailedMissionaryClassicSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(FAILED_MISSIONARY_CLASSIC_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(FAILED_MISSIONARY_CLASSIC_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(FAILED_MISSIONARY_CLASSIC_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		FAILED_MISSIONARY_CLASSIC_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		FAILED_MISSIONARY_CLASSIC_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _getFailedMissionaryClassicScaledTurns(iBaseTurns):
	gameSpeedType = CyGame().getGameSpeedType()
	iPercent = gc.getGameSpeedInfo(gameSpeedType).getGrowthPercent()
	return max(1, int((iBaseTurns * iPercent) / 100))

def _startFailedMissionaryClassicSoftCooldown(player, iBaseTurns):
	if player.isNone():
		return

	iCooldown = _getFailedMissionaryClassicScaledTurns(iBaseTurns)
	_setFailedMissionaryClassicSoftCooldownReadyTurn(player, CyGame().getGameTurn() + iCooldown)

def _isFailedMissionaryClassicSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getFailedMissionaryClassicSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _setFailedMissionaryClassicSelectedUnitData(player, iUnitId, iCityId):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_PREFIX)
	if iStart != -1:
		iEnd = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	iStart = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_PREFIX)
	if iStart != -1:
		iEnd = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szData += "%s%d%s" % (
		FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_PREFIX,
		iUnitId,
		FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_SUFFIX
	)

	szData += "%s%d%s" % (
		FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_PREFIX,
		iCityId,
		FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_SUFFIX
	)

	player.setScriptData(szData)

def _clearFailedMissionaryClassicSelectedUnitData(player):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		return

	iStart = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_PREFIX)
	if iStart != -1:
		iEnd = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	iStart = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_PREFIX)
	if iStart != -1:
		iEnd = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	player.setScriptData(szData)

def _getFailedMissionaryClassicSelectedUnitId(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_PREFIX)
	iEnd = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_UNIT_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _getFailedMissionaryClassicSelectedCityId(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_PREFIX)
	iEnd = szData.find(FAILED_MISSIONARY_CLASSIC_SELECTED_CITY_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _getFailedMissionaryClassicUnitOnCityPlot(player, city):
	if player.isNone() or city.isNone():
		return None

	plot = city.plot()
	if plot is None or plot.isNone():
		return None

	iFailedMissionaryClass = gc.getInfoTypeForString("UNITCLASS_FAILED_MISSIONARY")
	eColonistProfession = gc.getInfoTypeForString("PROFESSION_COLONIST")

	for i in range(plot.getNumUnits()):
		unit = plot.getUnit(i)
		if unit.isNone():
			continue
		if unit.getOwner() != player.getID():
			continue
		if gc.getUnitInfo(unit.getUnitType()).getUnitClassType() != iFailedMissionaryClass:
			continue
		if unit.getProfession() != eColonistProfession:
			continue
		return unit

	return None

def _findFailedMissionaryClassicCandidate(player):
	if player.isNone():
		return (None, None)

	(city, iter) = player.firstCity(True)
	while city:
		unit = _getFailedMissionaryClassicUnitOnCityPlot(player, city)
		if unit is not None and not unit.isNone():
			return (city, unit)
		(city, iter) = player.nextCity(iter, True)

	return (None, None)

def _getStoredFailedMissionaryClassicUnit(player):
	if player.isNone():
		return None

	iUnitId = _getFailedMissionaryClassicSelectedUnitId(player)
	if iUnitId < 0:
		return None

	unit = player.getUnit(iUnitId)
	if unit is None or unit.isNone():
		return None

	return unit

def _getStoredFailedMissionaryClassicCity(player):
	if player.isNone():
		return None

	iCityId = _getFailedMissionaryClassicSelectedCityId(player)
	if iCityId < 0:
		return None

	city = player.getCity(iCityId)
	if city is None or city.isNone():
		return None

	return city

def _isValidFailedMissionaryClassicUnit(player, city, unit):
	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	if city is None or city.isNone():
		return False

	if unit is None or unit.isNone():
		return False

	plot = city.plot()
	if plot is None or plot.isNone():
		return False

	if unit.getX() != city.getX() or unit.getY() != city.getY():
		return False

	iFailedMissionaryClass = gc.getInfoTypeForString("UNITCLASS_FAILED_MISSIONARY")
	if gc.getUnitInfo(unit.getUnitType()).getUnitClassType() != iFailedMissionaryClass:
		return False

	eColonistProfession = gc.getInfoTypeForString("PROFESSION_COLONIST")
	if unit.getProfession() != eColonistProfession:
		return False

	return True

def canTriggerFailedMissionaryClassic(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if player.isNative():
		return False

	if _isFailedMissionaryClassicSoftCooldownActive(player):
		return False

	city, unit = _findFailedMissionaryClassicCandidate(player)
	if city is None or city.isNone() or unit is None or unit.isNone():
		_clearFailedMissionaryClassicSelectedUnitData(player)
		return False

	# Fixed trigger chance on valid city plots
	if CyGame().getSorenRandNum(100, "Failed Missionary Classic trigger") >= 30:
		_clearFailedMissionaryClassicSelectedUnitData(player)
		return False

	_setFailedMissionaryClassicSelectedUnitData(player, unit.getID(), city.getID())
	return True

def doEventFailedMissionary1(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return

	city = _getStoredFailedMissionaryClassicCity(player)
	unit = _getStoredFailedMissionaryClassicUnit(player)

	if city is None or city.isNone():
		return
	if unit is None or unit.isNone():
		return

	if not _isValidFailedMissionaryClassicUnit(player, city, unit):
		return

	# Original reward must stay
	ChangeFatherPoints(argsList)

	_startFailedMissionaryClassicSoftCooldown(player, 30)
	_clearFailedMissionaryClassicSelectedUnitData(player)

def doEventFailedMissionary2(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return

	city = _getStoredFailedMissionaryClassicCity(player)
	unit = _getStoredFailedMissionaryClassicUnit(player)

	if city is None or city.isNone():
		return
	if unit is None or unit.isNone():
		return

	if not _isValidFailedMissionaryClassicUnit(player, city, unit):
		return

	_startFailedMissionaryClassicSoftCooldown(player, 30)
	_clearFailedMissionaryClassicSelectedUnitData(player)

def doEventFailedMissionary3(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return

	city = _getStoredFailedMissionaryClassicCity(player)
	unit = _getStoredFailedMissionaryClassicUnit(player)

	if city is None or city.isNone():
		return
	if unit is None or unit.isNone():
		return

	if not _isValidFailedMissionaryClassicUnit(player, city, unit):
		return

	_startFailedMissionaryClassicSoftCooldown(player, 30)
	_clearFailedMissionaryClassicSelectedUnitData(player)

def expireFailedMissionaryEvent(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return True

	city = _getStoredFailedMissionaryClassicCity(player)
	unit = _getStoredFailedMissionaryClassicUnit(player)

	if city is None or city.isNone():
		return True
	if unit is None or unit.isNone():
		return True

	if not _isValidFailedMissionaryClassicUnit(player, city, unit):
		return True

	return False

def getHelpFailedMissionaryClassic1(argsList):
	iCooldown = _getFailedMissionaryClassicScaledTurns(30)

	szHelp = getHelpChangeFatherPoints(argsList)
	szHelp += u"\n" + localText.getText(
		"TXT_KEY_EVENT_FAILED_MISSIONARY_CLASSIC_COOLDOWN_HELP",
		(iCooldown,)
	)
	return szHelp

def getHelpFailedMissionaryClassic2(argsList):
	iCooldown = _getFailedMissionaryClassicScaledTurns(30)

	return localText.getText(
		"TXT_KEY_EVENT_FAILED_MISSIONARY_CLASSIC_COOLDOWN_HELP",
		(iCooldown,)
	)

def getHelpFailedMissionaryClassic3(argsList):
	iCooldown = _getFailedMissionaryClassicScaledTurns(30)

	return localText.getText(
		"TXT_KEY_EVENT_FAILED_MISSIONARY_CLASSIC_COOLDOWN_HELP",
		(iCooldown,)
	)

######## Native Events ###########

def isNativeVillage(argsList):
	pTriggeredData = argsList[0]
	plot = gc.getMap().plot(pTriggeredData.iPlotX, pTriggeredData.iPlotY)
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	if not plot.isCity():
		return False
	if not gc.getPlayer(plot.getOwner()).isNative():
		return False
	return True

def isNativeVillageAndHuman(argsList):
	pTriggeredData = argsList[0]
	plot = gc.getMap().plot(pTriggeredData.iPlotX, pTriggeredData.iPlotY)
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if not player.isHuman():
		return False
	if not plot.isCity():
		return False
	if not gc.getPlayer(plot.getOwner()).isNative():
		return False
	return True

def isNativeVillageAndHumanTrade(argsList):
	pTriggeredData = argsList[0]
	plot = gc.getMap().plot(pTriggeredData.iPlotX, pTriggeredData.iPlotY)
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if not player.isHuman():
		return False
	if not plot.isCity():
		return False
	if not gc.getPlayer(plot.getOwner()).isNative():
		return False
	iUnitType = CvUtil.findInfoTypeNum('UNIT_TREK')
	iUnitsCurrent = countUnits(argsList, iUnitType)
	if not iUnitsCurrent > 5:
		return False
	return True

######## Native Training Event ###########

NATIVE_TRAINING_STATE_PREFIX = "[[WTP_NATIVE_TRAINING_STATE="
NATIVE_TRAINING_STATE_SUFFIX = "]]"

def _getNativeTrainingState(unit):
	if unit is None or unit.isNone():
		return (0, [])

	szData = unit.getScriptData()
	if szData is None or szData == "":
		return (0, [])

	iStart = szData.find(NATIVE_TRAINING_STATE_PREFIX)
	if iStart == -1:
		return (0, [])

	iStart += len(NATIVE_TRAINING_STATE_PREFIX)
	iEnd = szData.find(NATIVE_TRAINING_STATE_SUFFIX, iStart)
	if iEnd == -1:
		return (0, [])

	szPayload = szData[iStart:iEnd]
	if szPayload == "":
		return (0, [])

	aParts = szPayload.split("|", 1)

	try:
		iTrainedCount = int(aParts[0])
	except:
		iTrainedCount = 0

	aHandledVillages = []
	if len(aParts) > 1 and aParts[1] != "":
		for szEntry in aParts[1].split(","):
			if szEntry == "":
				continue
			aHandledVillages.append(szEntry)

	return (iTrainedCount, aHandledVillages)

def _setNativeTrainingState(unit, iTrainedCount, aHandledVillages):
	if unit is None or unit.isNone():
		return

	if iTrainedCount < 0:
		iTrainedCount = 0

	aCleanHandledVillages = []
	for szVillageKey in aHandledVillages:
		if szVillageKey == "":
			continue
		if szVillageKey not in aCleanHandledVillages:
			aCleanHandledVillages.append(szVillageKey)

	szData = unit.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(NATIVE_TRAINING_STATE_PREFIX)
	if iStart != -1:
		iEnd = szData.find(NATIVE_TRAINING_STATE_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(NATIVE_TRAINING_STATE_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szHandled = ",".join(aCleanHandledVillages)
	szMarker = "%s%d|%s%s" % (
		NATIVE_TRAINING_STATE_PREFIX,
		iTrainedCount,
		szHandled,
		NATIVE_TRAINING_STATE_SUFFIX
	)

	szData += szMarker
	unit.setScriptData(szData)

def _getNativeTrainingCount(unit):
	iTrainedCount, aHandledVillages = _getNativeTrainingState(unit)
	return iTrainedCount

def _setNativeTrainingCount(unit, iCount):
	iTrainedCount, aHandledVillages = _getNativeTrainingState(unit)
	_setNativeTrainingState(unit, iCount, aHandledVillages)

def _getNativeTrainingHandledVillages(unit):
	iTrainedCount, aHandledVillages = _getNativeTrainingState(unit)
	return aHandledVillages

def _setNativeTrainingHandledVillages(unit, aHandledVillages):
	iTrainedCount, aOldHandledVillages = _getNativeTrainingState(unit)
	_setNativeTrainingState(unit, iTrainedCount, aHandledVillages)

def _getNativeTrainingVillageKey(plot):
	if plot is None or plot.isNone():
		return ""

	if not plot.isCity():
		return ""

	city = plot.getPlotCity()
	if city is None or city.isNone():
		return ""

	return "%d:%d" % (plot.getOwner(), city.getID())

def _hasNativeTrainingHandledVillage(unit, szVillageKey):
	if szVillageKey == "":
		return False

	aHandledVillages = _getNativeTrainingHandledVillages(unit)
	return szVillageKey in aHandledVillages

def _markNativeTrainingHandledVillage(unit, szVillageKey):
	if szVillageKey == "":
		return

	aHandledVillages = _getNativeTrainingHandledVillages(unit)
	if szVillageKey not in aHandledVillages:
		aHandledVillages.append(szVillageKey)
		_setNativeTrainingHandledVillages(unit, aHandledVillages)

def _showNativeTrainingProgressMessage(player, unit, iCount):
	if player.isNone() or unit is None or unit.isNone():
		return

	if not player.isHuman():
		return

	if iCount <= 1:
		szText = localText.getText("TXT_KEY_EVENT_NATIVE_TRAINING_PROGRESS_1", (unit.getNameKey(),))
	elif iCount == 2:
		szText = localText.getText("TXT_KEY_EVENT_NATIVE_TRAINING_PROGRESS_2", (unit.getNameKey(),))
	else:
		szText = localText.getText("TXT_KEY_EVENT_NATIVE_TRAINING_PROGRESS_3", (unit.getNameKey(),))

	CyInterface().addMessage(
		player.getID(),
		True,
		10,
		szText,
		"",
		0,
		"",
		ColorTypes(8),
		unit.getX(),
		unit.getY(),
		True,
		True
	)

def _showNativeTrainingVisitedVillageMessage(player, unit):
	if player.isNone() or unit is None or unit.isNone():
		return

	if not player.isHuman():
		return

	szText = localText.getText("TXT_KEY_EVENT_NATIVE_TRAINING_PROGRESS_VISITED_ONLY", (unit.getNameKey(),))

	CyInterface().addMessage(
		player.getID(),
		True,
		10,
		szText,
		"",
		0,
		"",
		ColorTypes(8),
		unit.getX(),
		unit.getY(),
		True,
		True
	)

def _getNativeTrainingValidatedData(kTriggeredData):
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return (None, None, None, None, "", None)

	if not player.isPlayable():
		return (None, None, None, None, "", None)

	if player.isNative():
		return (None, None, None, None, "", None)

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return (None, None, None, None, "", None)

	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if plot.isNone():
		return (None, None, None, None, "", None)

	if unit.getX() != plot.getX() or unit.getY() != plot.getY():
		return (None, None, None, None, "", None)

	if not plot.isCity():
		return (None, None, None, None, "", None)

	city = plot.getPlotCity()
	if city is None or city.isNone():
		return (None, None, None, None, "", None)

	iTribePlayer = plot.getOwner()
	if iTribePlayer < 0:
		return (None, None, None, None, "", None)

	tribePlayer = gc.getPlayer(iTribePlayer)
	if tribePlayer.isNone():
		return (None, None, None, None, "", None)

	if not tribePlayer.isNative():
		return (None, None, None, None, "", None)

	if gc.getTeam(player.getTeam()).isAtWar(tribePlayer.getTeam()):
		return (None, None, None, None, "", None)

	if tribePlayer.AI_getAttitude(player.getID()) < AttitudeTypes.ATTITUDE_CAUTIOUS:
		return (None, None, None, None, "", None)

	if _getNativeTrainingCount(unit) >= 3:
		return (None, None, None, None, "", None)

	szVillageKey = _getNativeTrainingVillageKey(plot)
	if szVillageKey == "":
		return (None, None, None, None, "", None)

	if _hasNativeTrainingHandledVillage(unit, szVillageKey):
		return (None, None, None, None, "", None)

	return (player, unit, plot, city, szVillageKey, tribePlayer)

def canTriggerNativeTraining(argsList):
	kTriggeredData = argsList[0]

	player, unit, plot, city, szVillageKey, tribePlayer = _getNativeTrainingValidatedData(kTriggeredData)
	if player is None:
		return False

	# No extra random chance:
	# once all conditions are fulfilled, the event should trigger reliably
	return True

def applyNativeTraining1(argsList):
	kTriggeredData = argsList[0]

	player, unit, plot, city, szVillageKey, tribePlayer = _getNativeTrainingValidatedData(kTriggeredData)
	if player is None:
		return

	_markNativeTrainingHandledVillage(unit, szVillageKey)

	iNewCount = _getNativeTrainingCount(unit) + 1
	_setNativeTrainingCount(unit, iNewCount)

	_showNativeTrainingProgressMessage(player, unit, iNewCount)

def applyNativeTraining2(argsList):
	kTriggeredData = argsList[0]

	player, unit, plot, city, szVillageKey, tribePlayer = _getNativeTrainingValidatedData(kTriggeredData)
	if player is None:
		return

	_markNativeTrainingHandledVillage(unit, szVillageKey)
	_showNativeTrainingVisitedVillageMessage(player, unit)

####### Stirred up natives events ########

def canTriggerStirredUpNatives(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	iAchieve = gc.getInfoTypeForString("ACHIEVE_COLONIAL_CAVALRY")
	#CyInterface().addImmediateMessage("iAchieve "+str(iAchieve), "")
	if player.isAchieveGained(iAchieve):
		return True
	return False

def canTriggerStirredUpNativesHorses(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if player.isNone() or player2.isNone() :
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_STIRRED_UP_NATIVES_HORSES_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyStirredUpNativesHorses(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	nativecity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity:
		return
	city.changeYieldStored(iYield, quantity)
	nativecity.changeYieldStored(iYield, -quantity)

def getHelpStirredUpNativesHorses(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	nativecity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_HORSES")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = ""
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (-quantity,  gc.getYieldInfo(iYield).getChar(), nativecity.getNameKey()))
	return szHelp

def canTriggerStirredUpNativesMuskets(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if player.isNone() or player2.isNone() :
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_STIRRED_UP_NATIVES_MUSKETS_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_MUSKETS")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyStirredUpNativesMuskets(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	nativecity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_MUSKETS")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity:
		return
	city.changeYieldStored(iYield, quantity)
	nativecity.changeYieldStored(iYield, -quantity)

def getHelpStirredUpNativesMuskets(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	nativecity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_MUSKETS")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = ""
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (-quantity,  gc.getYieldInfo(iYield).getChar(), nativecity.getNameKey()))
	return szHelp

getHelpNativeAttackCity = get_simple_help("TXT_KEY_EVENT_NATIVES_ATTACK_HELP")

######## Initial Native Trade Event ###########

def canTriggerInitialNativeTrade(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	if player.isNone() or player2.isNone() :
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_INITIAL_TRADE_WITH_NATIVES_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_TRADE_GOODS")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyInitialNativeTrade(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	nativecity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_TRADE_GOODS")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity:
		return
	city.changeYieldStored(iYield, quantity)
	nativecity.changeYieldStored(iYield, -quantity)

def getHelpInitialNativeTrade1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	nativecity = player2.getCity(kTriggeredData.iOtherPlayerCityId)
	iYield = gc.getInfoTypeForString("YIELD_TRADE_GOODS")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = ""
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_YIELD_GAIN", (-quantity,  gc.getYieldInfo(iYield).getChar(), nativecity.getNameKey()))
	return szHelp

def canApplyInitialNativeTrade3(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	player2 = gc.getPlayer(kTriggeredData.eOtherPlayer)
	city = player.getCity(kTriggeredData.iCityId)
	if player.isNone() or player2.isNone() :
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from event and check if enough yield is stored in city
	iYield = gc.getInfoTypeForString("YIELD_TRADE_GOODS")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

######## Coca Events ###########
def canTriggerCocaEvent(argsList):
	ePlayer = argsList[1]
	iCityId = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCityId)
	if player.isNone():
		return False
	if not player.isPlayable():
		return False
	if city.isNone():
		return False
	# Read Parameter 1 from the first event and check if enough yield is stored in city
	eEvent1 = gc.getInfoTypeForString("EVENT_COCA_TRADE_1")
	event1 = gc.getEventInfo(eEvent1)
	iYield = gc.getInfoTypeForString("YIELD_COCA_LEAVES")
	quantity = event1.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	if city.getYieldStored(iYield) < -quantity :
		return False
	return True

def applyCocaEvent1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	iYield = gc.getInfoTypeForString("YIELD_COCA_LEAVES")
	if city.getYieldStored(iYield) < -quantity :
		return
	city.changeYieldStored(iYield, quantity)

def getHelpCocaEvent1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	iYield = gc.getInfoTypeForString("YIELD_COCA_LEAVES")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100
	szHelp = ""
	if event.getGenericParameter(1) <> 0 :
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (quantity,  gc.getYieldInfo(iYield).getChar(), city.getNameKey()))
	return szHelp

######## EUROPE TRADE Events ###########

## Explanations ##
# use this as info for XML Event setup
# The Generic Parameters are all configured in the Events the Event Triggers offer

#Start Quest Event: The Trigger for it needs to be setup as "City Trigger"
# Generic Parameter 1: Amount to start the Quest
# Generic Parameter 2: Yield ID used for the Quest
# Generic Parameter 3: Amount to successfully finish the Quest

#Done Quest Event: The Trigger for it needs to be setup as "City Trigger"
# Generic Parameter 1: Amount to successfully finish the Quest
# Generic Parameter 2: Yield ID used for the Quest
# Generic Parameter 3: King Relations Change
# Generic Parameter 4: Yield Price Change

# This is generic function called by the specific functions of the Trigger! - Not directly by the Trigger XML.
# It uses the argsList of the Events forwarded by the Trigger as function Parameter
def CanDoEuropeTrade(argsList, iYieldID, iQuantity):

	ePlayer = argsList[1]

	# safety checks to make sure it is a colonial player
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False

	# this here should not be needed because isPlayable but since we have Asserts ...
	if player.isNative():
		return False

	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False

	# This would break immersion and make event unlogical
	if player.isInRevolution():
		return False

	# because we might want to do something with the City
	iCityId = argsList[2]
	city = player.getCity(iCityId)
	if city.isNone():
		return False

	# here we select the Amount of the Yield from function argument iQuantity
	quantity = iQuantity
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	# here we check Handicap Setting for AI only to avoid confusing number in texts when Difficulty changes
	Handicap = gc.getHandicapInfo(CyGame().getHandicapType())
	#for AI
	if not player.isHuman():
		quantity = quantity * Handicap.getAITrainPercent()/100

	# now we check if enough of the Yield has been traded with Europe using function argument iYieldID
	if player.getYieldSoldTotal(TradeLocationTypes.TRADE_LOCATION_EUROPE, iYieldID) < quantity:
		return False
	return True

# This is the Function for the Event Target Yield and Target Amount
# This Function is only used for the "Quest Start"
def getHelpQuestStartEuropeTradeYieldAndAmount(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	# getting Player and King
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	# we get the Yield as Parameter from Event

	# First we get the Yield for this Event
	iYield = event.getGenericParameter(2)

	# Second we get the Target Quantity to deliver and of course also consider gamespeed
	quantity = event.getGenericParameter(3)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	# here we check Handicap Setting for AI only to avoid confusing number in texts
	Handicap = gc.getHandicapInfo(CyGame().getHandicapType())
	#for AI
	if not player.isHuman():
		quantity = quantity * Handicap.getAITrainPercent()/100

	# Now we construct the Help Text
	szHelp = ""
	if quantity > 0 :
		if iYield != gc.getInfoTypeForString("YIELD_TRADE_GOODS") and iYield != gc.getInfoTypeForString("YIELD_LUXURY_GOODS"):
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_EUROPE_TRADE_YIELD_AND_TARGET_AMOUNT_HELP", (quantity, gc.getYieldInfo(iYield).getChar()))
		elif iYield == gc.getInfoTypeForString("YIELD_TRADE_GOODS") or iYield == gc.getInfoTypeForString("YIELD_LUXURY_GOODS"):
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_EUROPE_TRADE_YIELD_AND_TARGET_AMOUNT_HELP_BUY", (quantity, gc.getYieldInfo(iYield).getChar()))
	return szHelp

# This is the Function for the Event Help Text for Price and Attitude
# This Function is only used for the "Quest Done"
def getHelpQuestDoneEuropeTradePriceAndAttitude(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	# getting Player and King
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	# we get the Yield as Parameter from Event
	iYield = event.getGenericParameter(2)

	#szHelp = localText.getText("TXT_KEY_EVENT_EUROPE_TRADE_PRICE_AND_ATTITUDE_HELP", ())
	szHelp = ""
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE", (event.getGenericParameter(4), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_DECREASE", (event.getGenericParameter(4), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

# This is the Function for the Event Help to apply Price and Attitude changes
# This Function is only used for the "Quest DONE"
def applyQuestDoneEuropeTradePriceAndAttitude(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	# getting King and Player
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	# changing the Attitude
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(3))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(3))

	# getting the Yield for the Price Change
	iYield = event.getGenericParameter(2)

	# changing the Price
	iPrice = king.getYieldBuyPrice(iYield)
	king.setYieldBuyPrice(iYield, iPrice+event.getGenericParameter(4), 1)

####### Here start all the EUROPE QUEST TRIGGERS Functions #######
# These are the specific checks for the specific Event Triggers

def canTriggerEuropeTradeQuest_SUGAR_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SUGAR_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SUGAR_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SUGAR_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_TOBACCO_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_TOBACCO_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_TOBACCO_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_TOBACCO_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FOOD_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FOOD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FOOD_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FOOD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_LUMBER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_LUMBER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_LUMBER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_LUMBER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_ORE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_ORE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_ORE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_ORE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_STONE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_STONE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_STONE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_STONE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HEMP_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HEMP_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HEMP_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HEMP_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SHEEP_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SHEEP_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SHEEP_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SHEEP_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CATTLE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CATTLE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CATTLE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CATTLE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HORSES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HORSES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HORSES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HORSES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COCOA_FRUITS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COCOA_FRUITS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COCOA_FRUITS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COCOA_FRUITS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COCA_LEAVES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COCA_LEAVES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COCA_LEAVES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COCA_LEAVES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FUR_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FUR_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FUR_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FUR_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WOOL_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WOOL_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WOOL_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WOOL_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COTTON_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COTTON_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COTTON_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COTTON_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_INDIGO_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_INDIGO_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_INDIGO_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_INDIGO_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COFFEE_BERRIES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COFFEE_BERRIES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COFFEE_BERRIES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COFFEE_BERRIES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HIDES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HIDES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HIDES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HIDES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PREMIUM_FUR_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PREMIUM_FUR_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PREMIUM_FUR_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PREMIUM_FUR_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RAW_SALT_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RAW_SALT_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RAW_SALT_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RAW_SALT_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RED_PEPPER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RED_PEPPER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RED_PEPPER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RED_PEPPER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_BARLEY_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_BARLEY_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_BARLEY_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_BARLEY_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GRAPES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GRAPES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GRAPES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GRAPES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WHALE_BLUBBER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WHALE_BLUBBER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WHALE_BLUBBER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WHALE_BLUBBER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_VALUABLE_WOOD_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_VALUABLE_WOOD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_VALUABLE_WOOD_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_VALUABLE_WOOD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_TRADE_GOODS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_TRADE_GOODS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_TRADE_GOODS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_TRADE_GOODS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_ROPE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_ROPE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_ROPE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_ROPE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SAILCLOTH_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SAILCLOTH_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SAILCLOTH_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SAILCLOTH_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CLOTH_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CLOTH_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CLOTH_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CLOTH_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_TOOLS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_TOOLS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_TOOLS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_TOOLS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_BLADES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_BLADES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_BLADES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_BLADES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_MUSKETS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_MUSKETS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_MUSKETS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_MUSKETS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CANNONS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CANNONS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CANNONS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CANNONS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SILVER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SILVER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SILVER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SILVER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GOLD_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GOLD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GOLD_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GOLD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COCOA_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COCOA_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COCOA_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COCOA_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COFFEE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COFFEE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COFFEE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COFFEE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CIGARS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CIGARS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CIGARS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CIGARS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GEMS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GEMS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GEMS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GEMS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WOOL_CLOTH_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WOOL_CLOTH_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WOOL_CLOTH_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WOOL_CLOTH_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COLOURED_CLOTH_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COLOURED_CLOTH_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COLOURED_CLOTH_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COLOURED_CLOTH_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_LEATHER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_LEATHER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_LEATHER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_LEATHER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COATS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COATS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COATS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COATS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PREMIUM_COATS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PREMIUM_COATS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PREMIUM_COATS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PREMIUM_COATS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SPICES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SPICES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SPICES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SPICES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_BEER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_BEER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_BEER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_BEER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WINE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WINE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WINE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WINE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WHALE_OIL_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WHALE_OIL_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WHALE_OIL_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WHALE_OIL_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FURNITURE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FURNITURE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FURNITURE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FURNITURE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SALT_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SALT_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_SALT_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_SALT_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_LUXURY_GOODS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_LUXURY_GOODS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_LUXURY_GOODS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_LUXURY_GOODS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_TRADE_GOODS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_TRADE_GOODS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_TRADE_GOODS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_TRADE_GOODS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CLAY_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CLAY_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CLAY_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CLAY_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger


def canTriggerEuropeTradeQuest_PEAT_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PEAT_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PEAT_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PEAT_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RICE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RICE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RICE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RICE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CASSAVA_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CASSAVA_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CASSAVA_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CASSAVA_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HARDWOOD_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HARDWOOD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HARDWOOD_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HARDWOOD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger


def canTriggerEuropeTradeQuest_FLAX_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FLAX_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FLAX_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FLAX_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PEANUTS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PEANUTS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PEANUTS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PEANUTS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FRUITS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FRUITS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FRUITS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FRUITS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_YERBA_LEAVES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_YERBA_LEAVES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_YERBA_LEAVES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_YERBA_LEAVES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger


def canTriggerEuropeTradeQuest_LOGWOOD_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_LOGWOOD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_LOGWOOD_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_LOGWOOD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COCHINEAL_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COCHINEAL_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COCHINEAL_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COCHINEAL_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_VANILLA_PODS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_VANILLA_PODS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_VANILLA_PODS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_VANILLA_PODS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_MAPLE_SIRUP_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_MAPLE_SIRUP_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_MAPLE_SIRUP_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_MAPLE_SIRUP_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_KAUTSCHUK_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_KAUTSCHUK_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_KAUTSCHUK_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_KAUTSCHUK_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COAL_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COAL_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COAL_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COAL_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger


def canTriggerEuropeTradeQuest_CHAR_COAL_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CHAR_COAL_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CHAR_COAL_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CHAR_COAL_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_BAKERY_GOODS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_BAKERY_GOODS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_BAKERY_GOODS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_BAKERY_GOODS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_BLACK_POWDER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_BLACK_POWDER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_BLACK_POWDER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_BLACK_POWDER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GEESE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GEESE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GEESE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GEESE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CHICKEN_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CHICKEN_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CHICKEN_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CHICKEN_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PIGS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PIGS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PIGS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PIGS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GOATS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GOATS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GOATS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GOATS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_OLIVES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_OLIVES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_OLIVES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_OLIVES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger


def canTriggerEuropeTradeQuest_RAPE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RAPE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RAPE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RAPE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WILD_FEATHERS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WILD_FEATHERS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_WILD_FEATHERS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_WILD_FEATHERS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_MILK_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_MILK_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_MILK_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_MILK_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GOAT_HIDES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GOAT_HIDES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GOAT_HIDES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GOAT_HIDES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PIG_SKIN_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PIG_SKIN_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PIG_SKIN_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PIG_SKIN_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_DOWNS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_DOWNS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_DOWNS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_DOWNS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_ROASTED_PEANUTS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_ROASTED_PEANUTS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_ROASTED_PEANUTS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_ROASTED_PEANUTS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger


def canTriggerEuropeTradeQuest_CHEESE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CHEESE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CHEESE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CHEESE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_YERBA_TEA_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_YERBA_TEA_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_YERBA_TEA_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_YERBA_TEA_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CHOCOLATE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CHOCOLATE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_CHOCOLATE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_CHOCOLATE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RUM_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RUM_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RUM_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RUM_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HOOCH_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HOOCH_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HOOCH_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HOOCH_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_OLIVE_OIL_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_OLIVE_OIL_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_OLIVE_OIL_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_OLIVE_OIL_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RAPE_OIL_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RAPE_OIL_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_RAPE_OIL_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_RAPE_OIL_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger


def canTriggerEuropeTradeQuest_EVERYDAY_CLOTHES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_EVERYDAY_CLOTHES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_EVERYDAY_CLOTHES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_EVERYDAY_CLOTHES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger


def canTriggerEuropeTradeQuest_FESTIVE_CLOTHES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FESTIVE_CLOTHES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FESTIVE_CLOTHES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FESTIVE_CLOTHES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COLOURED_WOOL_CLOTH_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COLOURED_WOOL_CLOTH_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_COLOURED_WOOL_CLOTH_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_COLOURED_WOOL_CLOTH_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GOAT_HIDE_BOOTS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GOAT_HIDE_BOOTS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_GOAT_HIDE_BOOTS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_GOAT_HIDE_BOOTS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PIG_LEATHER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PIG_LEATHER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PIG_LEATHER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PIG_LEATHER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PADDED_LEATHER_COATS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PADDED_LEATHER_COATS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PADDED_LEATHER_COATS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PADDED_LEATHER_COATS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_VANILLA_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_VANILLA_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_VANILLA_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_VANILLA_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_POTTERY_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_POTTERY_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_POTTERY_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_POTTERY_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PADDED_FURNITURE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PADDED_FURNITURE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_PADDED_FURNITURE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_PADDED_FURNITURE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FIELD_WORKER_TOOLS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FIELD_WORKER_TOOLS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_FIELD_WORKER_TOOLS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_FIELD_WORKER_TOOLS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HOUSEHOLD_GOODS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HOUSEHOLD_GOODS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerEuropeTradeQuest_HOUSEHOLD_GOODS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_EUROPE_TRADE_QUEST_HOUSEHOLD_GOODS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoEuropeTrade(argsList, iYieldID, iQuantity)

	return bTrigger

######## AFRICA TRADE Events ###########

## Explanations ##
# use this as info for XML Event setup
# The Generic Parameters are all configured in the Events the Event Triggers offer

#Start Quest Event: The Trigger for it needs to be setup as "City Trigger"
# Generic Parameter 1: Amount to start the Quest
# Generic Parameter 2: Yield ID used for the Quest
# Generic Parameter 3: Amount to successfully finish the Quest

#Done Quest Event: The Trigger for it needs to be setup as "City Trigger"
# Generic Parameter 1: Amount to successfully finish the Quest
# Generic Parameter 2: Yield ID used for the Quest
# Generic Parameter 3: King Relations Change
# Generic Parameter 4: Yield Price Change

# This is generic function called by the specific functions of the Trigger! - Not directly by the Trigger XML.
# It uses the argsList of the Events forwarded by the Trigger as function Parameter
def CanDoAfricaTrade(argsList, iYieldID, iQuantity):

	ePlayer = argsList[1]

	# safety checks to make sure it is a colonial player
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False

	# this here should not be needed because isPlayable but since we have Asserts ...
	if player.isNative():
		return False

	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False

	# This would break immersion and make event unlogical
	if player.isInRevolution():
		return False

	# because we might want to do something with the City
	iCityId = argsList[2]
	city = player.getCity(iCityId)
	if city.isNone():
		return False

	# here we select the Amount of the Yield from function argument iQuantity
	quantity = iQuantity
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	# here we check Handicap Setting for AI only to avoid confusing number in texts when Difficulty changes
	Handicap = gc.getHandicapInfo(CyGame().getHandicapType())
	#for AI
	if not player.isHuman():
		quantity = quantity * Handicap.getAITrainPercent()/100

	# now we check if enough of the Yield has been traded with Africa using function argument iYieldID
	if player.getYieldSoldTotal(TradeLocationTypes.TRADE_LOCATION_AFRICA, iYieldID) < quantity:
		return False
	return True

# This is the Function for the Event Target Yield and Target Amount
# This Function is only used for the "Quest Start"
def getHelpQuestStartAfricaTradeYieldAndAmount(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	# getting Player and King
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	# we get the Yield as Parameter from Event
	iYield = event.getGenericParameter(2)

	# Second we get the Target Quantity to deliver and of course also consider gamespeed
	quantity = event.getGenericParameter(3)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	# here we check Handicap Setting for AI only to avoid confusing number in texts
	Handicap = gc.getHandicapInfo(CyGame().getHandicapType())
	#for AI
	if not player.isHuman():
		quantity = quantity * Handicap.getAITrainPercent()/100

	# Now we construct the Help Text
	szHelp = ""
	if quantity > 0 :
		if iYield != gc.getInfoTypeForString("YIELD_TRADE_GOODS") and iYield != gc.getInfoTypeForString("YIELD_LUXURY_GOODS"):
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_AFRICA_TRADE_YIELD_AND_TARGET_AMOUNT_HELP", (quantity, gc.getYieldInfo(iYield).getChar()))
		elif iYield == gc.getInfoTypeForString("YIELD_TRADE_GOODS") or iYield== event.getGenericParameter(2) != gc.getInfoTypeForString("YIELD_LUXURY_GOODS"):
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_AFRICA_TRADE_YIELD_AND_TARGET_AMOUNT_HELP_BUY", (quantity, gc.getYieldInfo(iYield).getChar()))
	return szHelp

# This is the Function for the Event Help Text for Price and Attitude
# This Function is only used for the "Quest Done"
def getHelpQuestDoneAfricaTradePriceAndAttitude(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	# getting Player and King
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	# we get the Yield as Parameter from Event
	iYield = event.getGenericParameter(2)

	#szHelp = localText.getText("TXT_KEY_EVENT_EUROPE_TRADE_PRICE_AND_ATTITUDE_HELP", ())
	szHelp = ""
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE_AFRICA", (event.getGenericParameter(4), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_DECREASE_AFRICA", (event.getGenericParameter(4), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

# This is the Function for the Event Help to apply Price and Attitude changes
# This Function is only used for the "Quest DONE"
def applyQuestDoneAfricaTradePriceAndAttitude(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	# getting King and Player
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	# changing the Attitude
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(3))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(3))

	# getting the Yield for the Price Change
	iYield = event.getGenericParameter(2)

	# careful, uses Africa methods here
	iPrice = king.getYieldAfricaBuyPriceNoModifier(iYield)
	king.setYieldAfricaBuyPrice(iYield, iPrice+event.getGenericParameter(4), 1)

####### Here start all the AFICA QUEST TRIGGERS Functions #######
# These are the specific checks for the specific Event Triggers


######## PORT ROYAL TRADE Events ###########

## Explanations ##
# use this as info for XML Event setup
# The Generic Parameters are all configured in the Events the Event Triggers offer

#Start Quest Event: The Trigger for it needs to be setup as "City Trigger"
# Generic Parameter 1: Amount to start the Quest
# Generic Parameter 2: Yield ID used for the Quest
# Generic Parameter 3: Amount to successfully finish the Quest

#Done Quest Event: The Trigger for it needs to be setup as "City Trigger"
# Generic Parameter 1: Amount to successfully finish the Quest
# Generic Parameter 2: Yield ID used for the Quest
# Generic Parameter 3: King Relations Change
# Generic Parameter 4: Yield Price Change

# This is generic function called by the specific functions of the Trigger! - Not directly by the Trigger XML.
# It uses the argsList of the Events forwarded by the Trigger as function Parameter
def CanDoPortRoyalTrade(argsList, iYieldID, iQuantity):

	ePlayer = argsList[1]

	# safety checks to make sure it is a colonial player
	player = gc.getPlayer(ePlayer)
	if not player.isPlayable():
		return False

	# this here should not be needed because isPlayable but since we have Asserts ...
	if player.isNative():
		return False

	king = gc.getPlayer(player.getParent())

	if king is None:
		return False

	if not king.isEurope():
		return False

	# For Port Royal this is not needed, because Trade is also possible during Revolution
	#if player.isInRevolution():
	#	return False

	# because we might want to do something with the City
	iCityId = argsList[2]
	city = player.getCity(iCityId)
	if city.isNone():
		return False

	# here we select the Amount of the Yield from function argument iQuantity
	quantity = iQuantity
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	# here we check Handicap Setting for AI only to avoid confusing number in texts when Difficulty changes
	Handicap = gc.getHandicapInfo(CyGame().getHandicapType())
	#for AI
	if not player.isHuman():
		quantity = quantity * Handicap.getAITrainPercent()/100

	# now we check if enough of the Yield has been traded with Port Royal using function argument iYieldID
	if player.getYieldSoldTotal(TradeLocationTypes.TRADE_LOCATION_PORT_ROYAL, iYieldID) < quantity:
		return False
	return True

# This is the Function for the Event Target Yield and Target Amount
# This Function is only used for the "Quest Start"
def getHelpQuestStartPortRoyalTradeYieldAndAmount(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	# getting Player and King
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	# we get the Yield as Parameter from Event
	iYield = event.getGenericParameter(2)

	# Second we get the Target Quantity to deliver and of course also consider gamespeed
	quantity = event.getGenericParameter(3)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent()/100

	# here we check Handicap Setting for AI only to avoid confusing number in texts
	Handicap = gc.getHandicapInfo(CyGame().getHandicapType())
	#for AI
	if not player.isHuman():
		quantity = quantity * Handicap.getAITrainPercent()/100

	# Now we construct the Help Text
	szHelp = ""
	if quantity > 0 :
		if iYield != gc.getInfoTypeForString("YIELD_TRADE_GOODS") and iYield != gc.getInfoTypeForString("YIELD_LUXURY_GOODS"):
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PORTROYAL_TRADE_YIELD_AND_TARGET_AMOUNT_HELP", (quantity, gc.getYieldInfo(iYield).getChar()))
		elif iYield == gc.getInfoTypeForString("YIELD_TRADE_GOODS") or iYield == gc.getInfoTypeForString("YIELD_LUXURY_GOODS"):
			szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PORTROYAL_TRADE_YIELD_AND_TARGET_AMOUNT_HELP_BUY", (quantity, gc.getYieldInfo(iYield).getChar()))
	return szHelp

# This is the Function for the Event Help Text for Price and Attitude
# This Function is only used for the "Quest Done"
def getHelpQuestDonePortRoyalTradePriceAndAttitude(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	# getting Player and King
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	# we get the Yield as Parameter from Event
	iYield = event.getGenericParameter(2)

	#szHelp = localText.getText("TXT_KEY_EVENT_EUROPE_TRADE_PRICE_AND_ATTITUDE_HELP", ())
	szHelp = ""
	if event.getGenericParameter(4) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_INCREASE_PORT_ROYAL", (event.getGenericParameter(4), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(4) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_PRICE_DECREASE_PORT_ROYAL", (event.getGenericParameter(4), gc.getYieldInfo(iYield).getChar(), king.getCivilizationShortDescriptionKey()))
	if event.getGenericParameter(3) > 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_INCREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	if event.getGenericParameter(3) < 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(3), king.getCivilizationAdjectiveKey()))
	return szHelp

# This is the Function for the Event Help to apply Price and Attitude changes
# This Function is only used for the "Quest DONE"
def applyQuestDonePortRoyalTradePriceAndAttitude(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	# getting King and Player
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	# changing the Attitude
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(3))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(3))

	# getting the Yield for the Price Change
	iYield = event.getGenericParameter(2)

	# careful, uses Port Royal methods here
	iPrice = king.getYieldPortRoyalBuyPriceNoModifier(iYield)
	king.setYieldPortRoyalBuyPrice(iYield, iPrice+event.getGenericParameter(4), 1)

####### Here start all the PORT ROYAL QUEST TRIGGERS Functions #######
# These are the specific checks for the specific Event Triggers

def canTriggerPortRoyalTradeQuest_BLADES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_BLADES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_BLADES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_BLADES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_SAILCLOTH_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_SAILCLOTH_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_SAILCLOTH_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_SAILCLOTH_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_CANNONS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_CANNONS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_CANNONS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_CANNONS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger
def canTriggerPortRoyalTradeQuest_GUNS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_GUNS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_GUNS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_GUNS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_ROPES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_ROPES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_ROPES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_ROPES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_CIGARS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_CIGARS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_CIGARS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_CIGARS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_SPICES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_SPICES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_SPICES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_SPICES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_SALT_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_SALT_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_SALT_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_SALT_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_RUM_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_RUM_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_RUM_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_RUM_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_GOLD_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_GOLD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_GOLD_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_GOLD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_GEMS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_GEMS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_GEMS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_GEMS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_FURNITURE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_FURNITURE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_FURNITURE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_FURNITURE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_COFFEE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_COFFEE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_COFFEE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_COFFEE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_COCOA_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_COCOA_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_COCOA_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_COCOA_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_COCA_LEAVES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_COCA_LEAVES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_COCA_LEAVES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_COCA_LEAVES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_WINE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_WINE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_WINE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_WINE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_SILVER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_SILVER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_SILVER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_SILVER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_HARDWOOD_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_HARDWOOD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_HARDWOOD_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_HARDWOOD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_FOOD_START(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_FOOD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_FOOD_DONE(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_FOOD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_STONE_START(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_STONE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_STONE_DONE(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_STONE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_LUMBER_START(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_LUMBER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_LUMBER_DONE(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_LUMBER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_CLAY_START(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_CLAY_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_CLAY_DONE(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_CLAY_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_BAKERY_GOODS_START(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_BAKERY_GOODS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_BAKERY_GOODS_DONE(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_BAKERY_GOODS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_BEER_START(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_BEER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_BEER_DONE(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_BEER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_HOOCH_START(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_HOOCH_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_HOOCH_DONE(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_HOOCH_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger


def canTriggerPortRoyalTradeQuest_YERBA_TEA_START(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_YERBA_TEA_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_YERBA_TEA_DONE(argsList):

	# Read Parameters 12 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_YERBA_TEA_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_BLACK_POWDER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_BLACK_POWDER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_BLACK_POWDER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_BLACK_POWDER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_RICE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_RICE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_RICE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_RICE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_CASSAVA_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_CASSAVA_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerPortRoyalTradeQuest_CASSAVA_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_PORTROYAL_TRADE_QUEST_CASSAVA_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoPortRoyalTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_FOOD_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_FOOD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_FOOD_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_FOOD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_LUMBER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_LUMBER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_LUMBER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_LUMBER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_STONE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_STONE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_STONE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_STONE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_HORSES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_HORSES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_HORSES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_HORSES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_ORE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_ORE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_ORE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_ORE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_SILVER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_SILVER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_SILVER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_SILVER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_CATTLE_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_CATTLE_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_CATTLE_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_CATTLE_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_SHEEP_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_SHEEP_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_SHEEP_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_SHEEP_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_TOOLS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_TOOLS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_TOOLS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_TOOLS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_GUNS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_GUNS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_GUNS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_GUNS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_CLOTH_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_CLOTH_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_CLOTH_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_CLOTH_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_SALT_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_SALT_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_SALT_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_SALT_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_SPICES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_SPICES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_SPICES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_SPICES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_COCA_LEAVES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_COCA_LEAVES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_COCA_LEAVES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_COCA_LEAVES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_TRADINGGOODS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_TRADINGGOODS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_TRADINGGOODS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_TRADINGGOODS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_COTTON_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_COTTON_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_COTTON_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_COTTON_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger


def canTriggerAfricaTradeQuest_INDIGO_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_INDIGO_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_INDIGO_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_INDIGO_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_LOGWOOD_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_LOGWOOD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_LOGWOOD_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_LOGWOOD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_COCHINEAL_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_COCHINEAL_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_COCHINEAL_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_COCHINEAL_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_COFFEE_BERRIES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_COFFEE_BERRIES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_COFFEE_BERRIES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_COFFEE_BERRIES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_PEANUTS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_PEANUTS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_PEANUTS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_PEANUTS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_RED_PEPPER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_RED_PEPPER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_RED_PEPPER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_RED_PEPPER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_VANILLA_PODS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_VANILLA_PODS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_VANILLA_PODS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_VANILLA_PODS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_MAPLE_SIRUP_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_MAPLE_SIRUP_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_MAPLE_SIRUP_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_MAPLE_SIRUP_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_KAUTSCHUK_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_KAUTSCHUK_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_KAUTSCHUK_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_KAUTSCHUK_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_HARDWOOD_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_HARDWOOD_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_HARDWOOD_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_HARDWOOD_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_BLACK_POWDER_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_BLACK_POWDER_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_BLACK_POWDER_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_BLACK_POWDER_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_BLADES_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_BLADES_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_BLADES_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_BLADES_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_CANNONS_START(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_CANNONS_START")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Start this should be e.g. 200

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

def canTriggerAfricaTradeQuest_CANNONS_DONE(argsList):

	# Read Parameters 1+2 from the two events and check if enough yield is stored in city
	eEvent = gc.getInfoTypeForString("EVENT_AFRICA_TRADE_QUEST_CANNONS_DONE_1")
	event = gc.getEventInfo(eEvent)
	iYieldID = event.getGenericParameter(2)
	iQuantity = event.getGenericParameter(1) # for Quest Done this should be e.g. 1000

	# Now we call the Generic Helper Function
	bTrigger = CanDoAfricaTrade(argsList, iYieldID, iQuantity)

	return bTrigger

#######################################################
######## SPAWNING UNITS - friendly and hostile ########
#######################################################

### PART A1) UNIT Trigger Check Methods Blueprints
#######################################################
### Those are for the UnitTrigger Triggers to check ###
### ! Just Blueprints to be implemented by Trigger !###
#######################################################

# check for own units
def checkOwnPlayerUnitOnAdjacentPlotOfUnit(argsList): ### When you copy rename specically for your actuall EventTrigger
	eEvent = gc.getInfoTypeForString("EVENT_THAT_STORES_THE_PARAMETERS_TO_CHECK") ### When you copy put in actual Event to read parameters
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unitThatTriggered = player.getUnit(kTriggeredData.iUnitId)
	iOwnUnitClassTypeToCheck = event.getGenericParameter(1)
	found = unitThatTriggered.isOwnPlayerUnitOnAdjacentPlotOfUnit(iOwnUnitClassTypeToCheck)
	if (found):
		return True
	return False

# check for Barbarian Units
def checkBarbarianUnitOnAdjacentPlotOfUnit(argsList): ### When you copy rename specically for your actuall EventTrigger
	eEvent = gc.getInfoTypeForString("EVENT_THAT_STORES_THE_PARAMETERS_TO_CHECK") ### When you copy put in actual Event to read parameters
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unitThatTriggered = player.getUnit(kTriggeredData.iUnitId)
	iBarbarianUnitClassTypeToCheck = event.getGenericParameter(1)
	found = unitThatTriggered.isBarbarianUnitOnAdjacentPlotOfUnit(iBarbarianUnitClassTypeToCheck)
	if (found):
		return True
	return False


### PART A2) UNIT Trigger Spawn Methods
#####################################################
### Those are for the UnitTrigger Events to spawn ###
#####################################################

### Barbarians Units - either same Plot or adjacent Plot
### GenericParameter1: UnitClassType to spawn
### GenericParameter2: Number of Units to spawn

# same Plot
def spawnBarbarianUnitOnSamePlotAsUnit(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unitThatTriggered = player.getUnit(kTriggeredData.iUnitId)
	iHostileUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumHostilesToSpawn = event.getGenericParameter(2)
	for iX in range(iNumHostilesToSpawn):
		unitThatTriggered.spawnBarbarianUnitOnPlotOfUnit(iHostileUnitClassTypeToSpawn)

# adjacent Plot
def spawnBarbarianUnitAdjacentToUnit(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unitThatTriggered = player.getUnit(kTriggeredData.iUnitId)
	iHostileUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumHostilesToSpawn = event.getGenericParameter(2)
	for iX in range(iNumHostilesToSpawn):
		unitThatTriggered.spawnBarbarianUnitOnAdjacentPlotOfUnit(iHostileUnitClassTypeToSpawn)

### Own Player Units - either same Plot or adjacent Plot
### GenericParameter1: UnitClassType to spawn
### GenericParameter2: Number of Units to spawn

# same Plot
def spawnOwnPlayerUnitOnSamePlotAsUnit(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unitThatTriggered = player.getUnit(kTriggeredData.iUnitId)
	iOwnUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumOwnToSpawn = event.getGenericParameter(2)
	for iX in range(iNumOwnToSpawn):
		unitThatTriggered.spawnOwnPlayerUnitOnPlotOfUnit(iOwnUnitClassTypeToSpawn)

# adjacent Plot
def spawnOwnPlayerUnitAdjacentToUnit(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unitThatTriggered = player.getUnit(kTriggeredData.iUnitId)
	iOwnUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumOwnToSpawn = event.getGenericParameter(2)
	for iX in range(iNumOwnToSpawn):
		unitThatTriggered.spawnOwnPlayerUnitOnAdjacentPlotOfUnit(iOwnUnitClassTypeToSpawn)

### PART B1) CITY Trigger Check Methods Blueprints
#######################################################
### Those are for the CityTrigger Triggers to check ###
### ! Just Blueprints to be implemented by Trigger !###
#######################################################

# check for own units
def checkOwnPlayerUnitOnAdjacentPlotOfCity(argsList): ### When you copy rename specically for your actuall EventTrigger
	eEvent = gc.getInfoTypeForString("EVENT_THAT_STORES_THE_PARAMETERS_TO_CHECK") ### When you copy put in actual Event to read parameters
	event = gc.getEventInfo(eEvent)
	ePlayer = argsList[1]
	iCityIdThatTriggered = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCityIdThatTriggered)

	iOwnUnitClassTypeToCheck = event.getGenericParameter(1)
	found = city.isOwnPlayerUnitOnAdjacentPlotOfCity(iOwnUnitClassTypeToCheck)
	if (found):
		return True
	return False


# check for Barbarian Units
def checkBarbarianUnitOnAdjacentPlotOfCity(argsList): ### When you copy rename specically for your actuall EventTrigger
	eEvent = gc.getInfoTypeForString("EVENT_THAT_STORES_THE_PARAMETERS_TO_CHECK") ### When you copy put in actual Event to read parameters
	event = gc.getEventInfo(eEvent)
	ePlayer = argsList[1]
	iCityIdThatTriggered = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCityIdThatTriggered)

	iBarbarianUnitClassTypeToCheck = event.getGenericParameter(1)
	found = city.isBarbarianUnitOnAdjacentPlotOfCity(iBarbarianUnitClassTypeToCheck)
	if (found):
		return True
	return False


### PART B2) CITY Trigger Spawn Methods
#####################################################
### Those are for the CityTrigger Events to spawn ###
#####################################################

### Barbarians Units - either same Plot or adjacent Plot
### GenericParameter1: UnitClassType to spawn
### GenericParameter2: Number of Units to spawn

# same Plot # CAREFUL !!!, will take over City
def spawnBarbarianUnitOnSamePlotAsCity(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	iHostileUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumHostilesToSpawn = event.getGenericParameter(2)
	for iX in range(iNumHostilesToSpawn):
		city.spawnBarbarianUnitOnPlotOfCity(iHostileUnitClassTypeToSpawn)

# adjacent Plot
def spawnBarbarianUnitAdjacentToCity(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	iHostileUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumHostilesToSpawn = event.getGenericParameter(2)
	for iX in range(iNumHostilesToSpawn):
		city.spawnBarbarianUnitOnAdjacentPlotOfCity(iHostileUnitClassTypeToSpawn)

### Own Player Units - either same Plot or adjacent Plot
### GenericParameter1: UnitClassType to spawn
### GenericParameter2: Number of Units to spawn

# same Plot
def spawnOwnPlayerUnitOnSamePlotAsCity(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	iOwnUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumOwnToSpawn = event.getGenericParameter(2)
	for iX in range(iNumOwnToSpawn):
		city.spawnOwnPlayerUnitOnPlotOfCity(iOwnUnitClassTypeToSpawn)

# adjacent Plot
def spawnOwnPlayerUnitAdjacentToCity(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	iOwnUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumOwnToSpawn = event.getGenericParameter(2)
	for iX in range(iNumOwnToSpawn):
		city.spawnOwnPlayerUnitOnAdjacentPlotOfCity(iOwnUnitClassTypeToSpawn)

### PART C1) PLOT Trigger Check Methods Blueprints
#######################################################
### Those are for the PlotTrigger Triggers to check ###
### ! Just Blueprints to be implemented by Trigger !###
#######################################################

# check for own units
def checkOwnPlayerUnitOnAdjacentPlotOfPlot(argsList): ### When you copy rename specically for your actuall EventTrigger
	eEvent = gc.getInfoTypeForString("EVENT_THAT_STORES_THE_PARAMETERS_TO_CHECK") ### When you copy put in actual Event to read parameters
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	ePlayer = kTriggeredData.ePlayer
	plotThatTriggered = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iOwnUnitClassTypeToCheck = event.getGenericParameter(1)
	found = plotThatTriggered.isPlayerUnitOnAdjacentPlot(ePlayer, iOwnUnitClassTypeToCheck)
	if (found):
		return True
	return False

# check for Barbarian Units
def checkBarbarianUnitOnAdjacentPlotOfPlot(argsList): ### When you copy rename specically for your actuall EventTrigger
	eEvent = gc.getInfoTypeForString("EVENT_THAT_STORES_THE_PARAMETERS_TO_CHECK") ### When you copy put in actual Event to read parameters
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	plotThatTriggered = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iBarbarianUnitClassTypeToCheck = event.getGenericParameter(1)
	found = plotThatTriggered.isBarbarianUnitOnAdjacentPlot(iBarbarianUnitClassTypeToCheck)
	if (found):
		return True
	return False

### PART C2) PLOT Trigger Spawn Methods
#####################################################
### Those are for the PlotTrigger Events to spawn ###
#####################################################

### Barbarians Units - either same Plot or adjacent Plot
### GenericParameter1: UnitClassType to spawn
### GenericParameter2: Number of Units to spawn

# same Plot
def spawnBarbarianUnitOnSamePlotAsPlot(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	plotThatTriggered = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iHostileUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumHostilesToSpawn = event.getGenericParameter(2)
	for iX in range(iNumHostilesToSpawn):
		plotThatTriggered.spawnBarbarianUnitOnPlot(iHostileUnitClassTypeToSpawn)

# adjacent Plot
def spawnBarbarianUnitAdjacentToPlot(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	plotThatTriggered = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iHostileUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumHostilesToSpawn = event.getGenericParameter(2)
	for iX in range(iNumHostilesToSpawn):
		plotThatTriggered.spawnBarbarianUnitOnAdjacentPlot(iHostileUnitClassTypeToSpawn)

### Own Player Units - either same Plot or adjacent Plot
### GenericParameter1: UnitClassType to spawn
### GenericParameter2: Number of Units to spawn

# same Plot
def spawnOwnPlayerUnitOnSamePlotAsPlot(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	ePlayer = kTriggeredData.ePlayer
	plotThatTriggered = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iOwnUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumOwnToSpawn = event.getGenericParameter(2)
	for iX in range(iNumOwnToSpawn):
		plotThatTriggered.spawnPlayerUnitOnPlot(ePlayer, iOwnUnitClassTypeToSpawn)

# adjacent Plot
def spawnOwnPlayerUnitAdjacentToPlot(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	ePlayer = kTriggeredData.ePlayer
	plotThatTriggered = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	iOwnUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumOwnToSpawn = event.getGenericParameter(2)
	for iX in range(iNumOwnToSpawn):
		plotThatTriggered.spawnPlayerUnitOnAdjacentPlot(ePlayer, iOwnUnitClassTypeToSpawn)

######## Native Trader Attack ###########

def canTriggerNativeTraderAttack(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	unit = player.getUnit(kTriggeredData.iUnitId)
	eScout = gc.getInfoTypeForString("PROFESSION_NATIVE_TRADER")
	if unit.getProfession() != eScout:
		return False
	# Read parameter 3 from the event as random chance
	if TriggerChance(argsList):
		return True
	return False

getHelpNativeTraderAttack = get_simple_help("TXT_KEY_EVENT_NATIVE_TRADER_ATTACK_HELP")

######## Criminal Attacks City ###########

CRIMINALS_BLACKMAIL_CITY_COOLDOWN_PREFIX = "[[WTP_CRIMINALS_BLACKMAIL_CITY_READY_TURN="
CRIMINALS_BLACKMAIL_CITY_COOLDOWN_SUFFIX = "]]"


def _getCriminalsBlackmailCityCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(CRIMINALS_BLACKMAIL_CITY_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(CRIMINALS_BLACKMAIL_CITY_COOLDOWN_PREFIX)
	iEnd = szData.find(CRIMINALS_BLACKMAIL_CITY_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	sValue = szData[iStart:iEnd]
	if sValue == "":
		return -1

	try:
		return int(sValue)
	except:
		return -1


def _setCriminalsBlackmailCityCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iOldStart = szData.find(CRIMINALS_BLACKMAIL_CITY_COOLDOWN_PREFIX)
	if iOldStart != -1:
		iOldEnd = szData.find(CRIMINALS_BLACKMAIL_CITY_COOLDOWN_SUFFIX, iOldStart)
		if iOldEnd != -1:
			iOldEnd += len(CRIMINALS_BLACKMAIL_CITY_COOLDOWN_SUFFIX)
			szData = szData[:iOldStart] + szData[iOldEnd:]

	szData += CRIMINALS_BLACKMAIL_CITY_COOLDOWN_PREFIX + str(iReadyTurn) + CRIMINALS_BLACKMAIL_CITY_COOLDOWN_SUFFIX
	player.setScriptData(szData)


def _isCriminalsBlackmailCityCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getCriminalsBlackmailCityCooldownReadyTurn(player)
	if iReadyTurn < 0:
		return False

	return CyGame().getGameTurn() < iReadyTurn


def _startCriminalsBlackmailCityCooldown(player, iTurns):
	if player.isNone():
		return

	iReadyTurn = CyGame().getGameTurn() + iTurns
	_setCriminalsBlackmailCityCooldownReadyTurn(player, iReadyTurn)


def canTriggerCriminalsBlackmailCity(argsList):
	ePlayer = argsList[1]
	iCity = argsList[2]

	player = gc.getPlayer(ePlayer)
	if player.isNone():
		return False

	if not player.isPlayable():
		return False

	city = player.getCity(iCity)
	if city.isNone():
		return False

	if city.getOwner() != ePlayer:
		return False

	if city.isOccupation():
		return False

	iHappiness = city.getCityHappiness()
	iUnhappiness = city.getCityUnHappiness()

	if iUnhappiness <= iHappiness:
		return False

	if city.getPopulation() < 3:
		return False

	iChance = 20
	if _isCriminalsBlackmailCityCooldownActive(player):
		iChance = 1

	if CyGame().getSorenRandNum(100, "Criminals Blackmail City trigger chance") >= iChance:
		return False

	return True


def canDoCriminalsBlackmailCityGive(argsList):
	if len(argsList) < 1:
		return False

	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return False

	city = player.getCity(kTriggeredData.iCityId)
	if city.isNone():
		return False

	iFoodCost = 50
	gameSpeed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	iFoodCost = iFoodCost * gameSpeed.getStoragePercent() / 100

	if city.getFood() < iFoodCost:
		return False

	return True


def _cityHasAnyDefenderOnCityPlot(city):
	if city.isNone():
		return False

	pCityPlot = city.plot()
	if pCityPlot is None:
		return False

	for i in range(pCityPlot.getNumUnits()):
		loopUnit = pCityPlot.getUnit(i)

		if loopUnit is None or loopUnit.isNone():
			continue
		if loopUnit.getOwner() != city.getOwner():
			continue
		if loopUnit.isDead():
			continue
		if loopUnit.getDomainType() != DomainTypes.DOMAIN_LAND:
			continue
		if not loopUnit.canDefend(pCityPlot):
			continue

		return True

	return False

def _spawnRevoltingCriminalAdjacentToCity(city):
	if city.isNone():
		return None

	player = gc.getPlayer(city.getOwner())
	if player.isNone():
		return None

	iBarbarian = gc.getGame().getBarbarianPlayer()
	barbPlayer = gc.getPlayer(iBarbarian)
	if barbPlayer.isNone():
		return None

	iUnitClass = gc.getInfoTypeForString("UNITCLASS_REVOLTING_CRIMINAL")
	if iUnitClass == -1:
		return None

	iUnitType = gc.getCivilizationInfo(barbPlayer.getCivilizationType()).getCivilizationUnits(iUnitClass)
	if iUnitType == -1:
		return None

	pCityPlot = city.plot()
	if pCityPlot is None:
		return None

	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			if iDX == 0 and iDY == 0:
				continue

			pLoop = plotXY(city.getX(), city.getY(), iDX, iDY)
			if pLoop is None or pLoop.isNone():
				continue
			if pLoop.isWater():
				continue
			if pLoop.isImpassable():
				continue
			if pLoop.isPeak():
				continue
			if pLoop.isCity():
				continue
			if pLoop.isUnit():
				continue

			pUnit = barbPlayer.initUnit(
				iUnitType,
				ProfessionTypes.NO_PROFESSION,
				pLoop.getX(),
				pLoop.getY(),
				UnitAITypes.NO_UNITAI,
				DirectionTypes.DIRECTION_SOUTH,
				0
			)

			if pUnit is not None and not pUnit.isNone():
				return pUnit

	return None

def applyGiveFood(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return False

	city = player.getCity(kTriggeredData.iCityId)
	if city.isNone():
		return False

	iYield = gc.getInfoTypeForString("YIELD_FOOD")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent() / 100

	if city.getYieldStored(iYield) < quantity:
		return False

	city.changeYieldStored(iYield, -quantity)

	_startCriminalsBlackmailCityCooldown(player, 75)
	return True


def getHelpGiveFood(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)

	iYield = gc.getInfoTypeForString("YIELD_FOOD")
	quantity = event.getGenericParameter(1)
	Speed = gc.getGameSpeedInfo(CyGame().getGameSpeedType())
	quantity = quantity * Speed.getStoragePercent() / 100

	szHelp = ""
	if event.getGenericParameter(1) <> 0:
		szHelp = localText.getText("TXT_KEY_EVENT_YIELD_LOOSE", (-quantity, gc.getYieldInfo(iYield).getChar(), city.getNameKey()))

	return szHelp


def _applyDirectSuccessfulCriminalRaid(city):
	if city.isNone():
		return False

	pCityPlot = city.plot()
	if pCityPlot is None:
		return False

	player = gc.getPlayer(city.getOwner())
	if player.isNone():
		return False

	eKing = player.getParent()
	king = gc.getPlayer(eKing)
	if king is None or king.isNone():
		return False

	bestYield = -1
	bestValue = 0
	bestLoot = 0
	bestType = "none"

	iFoodYield = gc.getInfoTypeForString("YIELD_FOOD")

	# --- GOLD OPTION ---
	iGold = player.getGold()
	if iGold > 0:
		iGoldLoot = min(iGold, 80 + CyGame().getSorenRandNum(121, "Criminal raid gold"))
		if iGoldLoot > 0:
			if iGoldLoot > bestValue:
				bestValue = iGoldLoot
				bestLoot = iGoldLoot
				bestType = "gold"

	# --- YIELD OPTIONS ---
	for iYield in range(YieldTypes.NUM_YIELD_TYPES):
		eYield = YieldTypes(iYield)

		if eYield == iFoodYield:
			continue

		iStored = city.getYieldStored(eYield)
		if iStored <= 0:
			continue

		iMaxLoot = min(iStored, 20 + CyGame().getSorenRandNum(31, "Criminal raid goods"))
		if iMaxLoot <= 0:
			continue

		iPrice = king.getYieldBuyPrice(eYield)
		iTotalValue = iPrice * iMaxLoot

		if iTotalValue > bestValue:
			bestValue = iTotalValue
			bestYield = eYield
			bestLoot = iMaxLoot
			bestType = "yield"

	# --- EXECUTE RAID ---

	if bestType == "gold" and bestLoot > 0:
		player.changeGold(-bestLoot)

		CyInterface().addMessage(
			player.getID(),
			True,
			gc.getEVENT_MESSAGE_TIME(),
			localText.getText(
				"TXT_KEY_EVENT_CRIMINALS_BLACKMAIL_CITY_DIRECT_RAID_GOLD",
				(city.getNameKey(), bestLoot)
			),
			"AS2D_CITYRAID",
			InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
			None,
			gc.getInfoTypeForString("COLOR_RED"),
			pCityPlot.getX(),
			pCityPlot.getY(),
			True,
			True
		)
		return True

	if bestType == "yield" and bestYield != -1 and bestLoot > 0:
		city.changeYieldStored(bestYield, -bestLoot)

		sYieldName = gc.getYieldInfo(bestYield).getDescription()

		CyInterface().addMessage(
			player.getID(),
			True,
			gc.getEVENT_MESSAGE_TIME(),
			localText.getText(
				"TXT_KEY_EVENT_CRIMINALS_BLACKMAIL_CITY_DIRECT_RAID_GOODS",
				(
					city.getNameKey(),
					bestLoot,
					sYieldName
				)
			),
			"AS2D_CITYRAID",
			InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
			gc.getYieldInfo(bestYield).getButton(),
			gc.getInfoTypeForString("COLOR_RED"),
			pCityPlot.getX(),
			pCityPlot.getY(),
			True,
			True
		)
		return True

	CyInterface().addMessage(
		player.getID(),
		True,
		gc.getEVENT_MESSAGE_TIME(),
		localText.getText(
			"TXT_KEY_EVENT_CRIMINALS_BLACKMAIL_CITY_DIRECT_RAID_NOTHING",
			(city.getNameKey(),)
		),
		"AS2D_CITYRAID",
		InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
		None,
		gc.getInfoTypeForString("COLOR_RED"),
		pCityPlot.getX(),
		pCityPlot.getY(),
		True,
		True
	)

	return True


def applyCriminalsBlackmailCityRefuse(argsList):
	kTriggeredData = argsList[0]

	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return False

	city = player.getCity(kTriggeredData.iCityId)
	if city.isNone():
		return False

	_startCriminalsBlackmailCityCooldown(player, 50)

	# Always spawn one visible criminal next to the city if possible
	_spawnRevoltingCriminalAdjacentToCity(city)

	# Defender on city plot -> 50/50 outcome
	if _cityHasAnyDefenderOnCityPlot(city):
		iRoll = CyGame().getSorenRandNum(100, "Criminals Blackmail City defended outcome")

		# 50%: city successfully defended
		if iRoll < 50:
			CyInterface().addMessage(
				player.getID(),
				True,
				gc.getEVENT_MESSAGE_TIME(),
				localText.getText(
					"TXT_KEY_EVENT_CRIMINALS_BLACKMAIL_CITY_DEFENDED_ABORTED",
					(city.getNameKey(),)
				),
				"AS2D_GOODNEWS",
				InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
				None,
				gc.getInfoTypeForString("COLOR_GREEN"),
				city.getX(),
				city.getY(),
				True,
				True
			)
			return True

		# 50%: defenders fail to prevent the raid
		CyInterface().addMessage(
			player.getID(),
			True,
			gc.getEVENT_MESSAGE_TIME(),
			localText.getText(
				"TXT_KEY_EVENT_CRIMINALS_BLACKMAIL_CITY_DEFENDED_BUT_RAIDED",
				(city.getNameKey(),)
			),
			"AS2D_CITYRAID",
			InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
			None,
			gc.getInfoTypeForString("COLOR_RED"),
			city.getX(),
			city.getY(),
			True,
			True
		)

		return _applyDirectSuccessfulCriminalRaid(city)

	# No defender on city plot -> direct successful raid
	return _applyDirectSuccessfulCriminalRaid(city)

getHelpCriminalsBlackmailCityRefuse = get_simple_help("TXT_KEY_EVENT_CRIMINALS_BLACKMAIL_CITY_REFUSE_HELP")

######## Officer duel ###########

getHelpOfficerDuel = get_simple_help("TXT_KEY_EVENT_OFFICER_DUEL_HELP")

getHelpOfficerNoDuel = get_simple_help("TXT_KEY_EVENT_OFFICER_NODUEL_HELP")

######## Bailiffs search for Architect and attack city ###########

getHelpBailiffsAttackCity = get_simple_help("TXT_KEY_EVENT_ARCHITECT_BAILIFF_HELP")

######## Buccanners attack Silver Mine ###########

getHelpBuccanneersAttackMine = get_simple_help("TXT_KEY_EVENT_BUCCANNERS_ATTACK_MINE_HELP")

getHelpMilitiaDefend = get_simple_help("TXT_KEY_EVENT_MILITIA_DEFENDS_MINE_HELP")

######## Officer arrives at fort ###########

getHelpOfficerAtFort = get_simple_help("TXT_KEY_EVENT_OFFICER_ARRIVAL_AT_FORT_HELP")

######## Discovery Start Event  ###########

getHelpDiscoveryConquistador = get_simple_help("TXT_KEY_EVENT_DISCOVERY_EVENTS_START_CONQUISTADOR_HELP")

getHelpDiscoveryMissionary = get_simple_help("TXT_KEY_EVENT_DISCOVERY_EVENTS_START_MISSIONARY_HELP")

getHelpDiscoveryTrader = get_simple_help("TXT_KEY_EVENT_DISCOVERY_EVENTS_START_SEASONED_TRADER_HELP")

getHelpDiscoveryOxcart = get_simple_help("TXT_KEY_EVENT_DISCOVERY_EVENTS_START_Oxcart_HELP")

######## Treasure Attack Event ###########

TREASURE_ATTACK_SOFT_COOLDOWN_PREFIX = "[[WTP_TREASURE_ATTACK_SOFT_READY_TURN="
TREASURE_ATTACK_SOFT_COOLDOWN_SUFFIX = "]]"

def _getTreasureAttackSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(TREASURE_ATTACK_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(TREASURE_ATTACK_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(TREASURE_ATTACK_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setTreasureAttackSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(TREASURE_ATTACK_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(TREASURE_ATTACK_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(TREASURE_ATTACK_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		TREASURE_ATTACK_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		TREASURE_ATTACK_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _startTreasureAttackSoftCooldown(player):
	if player.isNone():
		return

	_setTreasureAttackSoftCooldownReadyTurn(player, CyGame().getGameTurn() + 30)

def _isTreasureAttackSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getTreasureAttackSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def getDistanceToOwnTerritory(plot, player, iMaxRange):
	for iRange in range(1, iMaxRange + 1):
		for iDX in range(-iRange, iRange + 1):
			for iDY in range(-iRange, iRange + 1):
				if abs(iDX) != iRange and abs(iDY) != iRange:
					continue

				pLoop = plotXY(plot.getX(), plot.getY(), iDX, iDY)
				if pLoop is None or pLoop.isNone():
					continue

				if pLoop.getOwner() == player.getID():
					return iRange

	return iMaxRange + 1

def _getTreasureAttackChance(player, plot):
	iDistance = getDistanceToOwnTerritory(plot, player, 10)

	if _isTreasureAttackSoftCooldownActive(player):
		if iDistance <= 5:
			return 0
		elif iDistance <= 10:
			return 2
		else:
			return 5

	if iDistance <= 5:
		return 5
	elif iDistance <= 10:
		return 10
	else:
		return 15

def _spawnTreasureAttackFriendlyEscortOnTreasurePlot(plot, iPlayer, iUnitClass):
	if plot is None or plot.isNone():
		return None

	if iUnitClass == -1:
		return None

	player = gc.getPlayer(iPlayer)
	if player.isNone():
		return None

	civ = gc.getCivilizationInfo(player.getCivilizationType())
	iUnitType = civ.getCivilizationUnits(iUnitClass)
	if iUnitType == UnitTypes.NO_UNIT:
		return None

	unit = player.initUnit(
		iUnitType,
		ProfessionTypes.NO_PROFESSION,
		plot.getX(),
		plot.getY(),
		UnitAITypes.NO_UNITAI,
		DirectionTypes.DIRECTION_SOUTH,
		0
	)

	if unit is not None and not unit.isNone():
		return unit

	return None

def _spawnTreasureAttackHostileAdjacent(plot, iUnitClass):
	if plot is None or plot.isNone():
		return None

	if iUnitClass == -1:
		return None

	iBarbarian = gc.getGame().getBarbarianPlayer()
	barbPlayer = gc.getPlayer(iBarbarian)
	if barbPlayer.isNone():
		return None

	barbCiv = gc.getCivilizationInfo(barbPlayer.getCivilizationType())
	iUnitType = barbCiv.getCivilizationUnits(iUnitClass)
	if iUnitType == UnitTypes.NO_UNIT:
		return None

	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			if iDX == 0 and iDY == 0:
				continue

			pLoop = plotXY(plot.getX(), plot.getY(), iDX, iDY)
			if pLoop is None or pLoop.isNone():
				continue
			if pLoop.isWater():
				continue
			if pLoop.isImpassable():
				continue
			if pLoop.isPeak():
				continue
			if pLoop.isCity():
				continue
			if pLoop.isUnit():
				continue

			unit = barbPlayer.initUnit(
				iUnitType,
				ProfessionTypes.NO_PROFESSION,
				pLoop.getX(),
				pLoop.getY(),
				UnitAITypes.NO_UNITAI,
				DirectionTypes.DIRECTION_SOUTH,
				0
			)

			if unit is not None and not unit.isNone():
				return unit

	return None

def _immobilizeTreasureStack(plot, iPlayer):
	for i in range(plot.getNumUnits()):
		unit = plot.getUnit(i)
		if unit.isNone():
			continue
		if unit.getOwner() == iPlayer:
			unit.setMoves(0)
			unit.setImmobileTimer(1)

def _forceUnitToMoveToPlot(unit, targetPlot):
	if unit is None or unit.isNone():
		return

	group = unit.getGroup()
	if group is None:
		return

	group.pushMission(
		MissionTypes.MISSION_MOVE_TO,
		targetPlot.getX(),
		targetPlot.getY(),
		0,
		False,
		True,
		MissionAITypes.NO_MISSIONAI,
		targetPlot,
		unit
	)

def canTriggerTreasureAttack(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False

	if not player.isPlayable():
		return False

	if player.isNative():
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False

	# Exact unit type check
	if unit.getUnitClassType() != gc.getInfoTypeForString("UNITCLASS_TREASURE"):
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False

	# Exact unit / plot binding to prevent ghost triggers
	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return False

	# Must be land
	if plot.isWater():
		return False

	# Wilderness only: no city plot
	if plot.isCity():
		return False

	# Wilderness only: not on own territory
	if plot.getOwner() == player.getID():
		return False

	iChance = _getTreasureAttackChance(player, plot)

	if CyGame().getSorenRandNum(100, "Treasure Attack Trigger") >= iChance:
		return False

	# Start soft cooldown here so both event choices get it,
	# including the XML-only pay option without Python callback.
	_startTreasureAttackSoftCooldown(player)

	return True

def applyTreasureAttack(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return

	# Ensure we still operate on a treasure unit
	if unit.getUnitClassType() != gc.getInfoTypeForString("UNITCLASS_TREASURE"):
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	# Exact unit / plot binding to prevent invalid execution
	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if plot.isWater():
		return

	if plot.isCity():
		return

	iHostileUnitClass = event.getGenericParameter(1)
	iNumHostiles = event.getGenericParameter(2)
	iImmobilize = event.getGenericParameter(3)
	iFriendlyUnitClass = event.getGenericParameter(4)

	if iFriendlyUnitClass != -1:
		_spawnTreasureAttackFriendlyEscortOnTreasurePlot(plot, kTriggeredData.ePlayer, iFriendlyUnitClass)

	if iImmobilize > 0:
		_immobilizeTreasureStack(plot, kTriggeredData.ePlayer)

	if iNumHostiles < 1:
		iNumHostiles = 1
	if iNumHostiles > 1:
		iNumHostiles = 1

	hostileUnit = _spawnTreasureAttackHostileAdjacent(plot, iHostileUnitClass)
	if hostileUnit is not None and not hostileUnit.isNone():
		if hostileUnit.canMoveInto(plot, True, False, False):
			hostileUnit.attack(plot, False)

def getHelpDiscoveryTreasureAttack(argsList):
	return localText.getText("TXT_KEY_EVENT_DISCOVERY_EVENTS_TREASURE_ATTACK_HELP", ())

######## Slave Hunter Offers Service ###########

def checkRunawaySlavesOnAdjacentPlotOfCity(argsList): ### When you copy rename specically for your actuall EventTrigger
	eEvent = gc.getInfoTypeForString("EVENT_SLAVE_HUNTER_SERVICE_ACCEPT") ### When you copy put in actual Event to read parameters
	event = gc.getEventInfo(eEvent)
	ePlayer = argsList[1]
	iCityIdThatTriggered = argsList[2]
	player = gc.getPlayer(ePlayer)
	city = player.getCity(iCityIdThatTriggered)

	iBarbarianUnitClassTypeToCheck = event.getGenericParameter(1)
	found = city.isBarbarianUnitOnAdjacentPlotOfCity(iBarbarianUnitClassTypeToCheck)
	if (found):
		return True

	iBarbarianUnitClassTypeToCheck2 = event.getGenericParameter(2)
	found = city.isBarbarianUnitOnAdjacentPlotOfCity(iBarbarianUnitClassTypeToCheck2)
	if (found):
		return True

	iBarbarianUnitClassTypeToCheck3 = event.getGenericParameter(2)
	found = city.isBarbarianUnitOnAdjacentPlotOfCity(iBarbarianUnitClassTypeToCheck3)
	if (found):
		return True
	return False

######## General Attack Function ###########

def canTriggerIsPlayableWithTriggerChance(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	# Read parameter 3 from the event as random chance
	if TriggerChance(argsList):
		return True
	return False

# adjacent Plot for Barbarian, same Plot for own Unit
def spawnBarbarianUnitAdjacentToUnitAndFriendlyOnSamePlot(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	unitThatTriggered = player.getUnit(kTriggeredData.iUnitId)
	# This part spawns the Barbarian
	iHostileUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumHostilesToSpawn = event.getGenericParameter(2)
	for iX in range(iNumHostilesToSpawn):
		unitThatTriggered.spawnBarbarianUnitOnAdjacentPlotOfUnit(iHostileUnitClassTypeToSpawn)
	# This Part spawns the Friendly
	iOwnUnitClassTypeToSpawn = event.getGenericParameter(4)
	iNumOwnToSpawn = event.getGenericParameter(2)
	for iX in range(iNumOwnToSpawn):
		unitThatTriggered.spawnOwnPlayerUnitOnPlotOfUnit(iOwnUnitClassTypeToSpawn)

######## Ranger Bear Attack ###########

######## Ranger Bear Attack ###########

def canTriggerRangerBearAttack(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False

	if not player.isPlayable():
		return False

	if player.isNative():
		return False

	ranger = player.getUnit(kTriggeredData.iUnitId)
	if ranger.isNone():
		return False

	plot = ranger.plot()
	if plot is None or plot.isNone():
		return False

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return False

	# Optional: only allow land plots
	if plot.isWater():
		return False

	# One-time event → no cooldown required
	return True


def applyRangerBearAttack(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	if not player.isPlayable():
		return

	if player.isNative():
		return

	ranger = player.getUnit(kTriggeredData.iUnitId)
	if ranger.isNone():
		return

	plot = ranger.plot()
	if plot is None or plot.isNone():
		return

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if plot.isWater():
		return

	# =========================
	# Spawn grizzly (hostile unit on adjacent plot)
	# =========================
	iBarbarian = gc.getGame().getBarbarianPlayer()
	barbPlayer = gc.getPlayer(iBarbarian)

	if barbPlayer.isNone():
		return

	iGrizzlyType = gc.getInfoTypeForString("UNIT_GRIZZLY")
	if iGrizzlyType == -1:
		return

	hostileUnit = None

	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			if iDX == 0 and iDY == 0:
				continue

			pLoop = plotXY(plot.getX(), plot.getY(), iDX, iDY)

			if pLoop is None or pLoop.isNone():
				continue
			if pLoop.isWater():
				continue
			if pLoop.isImpassable():
				continue
			if pLoop.isPeak():
				continue
			if pLoop.isCity():
				continue
			if pLoop.isUnit():
				continue

			hostileUnit = barbPlayer.initUnit(
				iGrizzlyType,
				ProfessionTypes.NO_PROFESSION,
				pLoop.getX(),
				pLoop.getY(),
				UnitAITypes.NO_UNITAI,
				DirectionTypes.DIRECTION_SOUTH,
				0
			)
			break
		if hostileUnit is not None and not hostileUnit.isNone():
			break

	# =========================
	# Freeze ranger (current turn + next turn)
	# =========================
	ranger.setMoves(0)
	ranger.setImmobileTimer(1)

	# =========================
	# Direct combat against the ranger
	# =========================
	if hostileUnit is not None and not hostileUnit.isNone():
		pTargetPlot = ranger.plot()
		if pTargetPlot is not None and not pTargetPlot.isNone():
			hostileUnit.attack(pTargetPlot, False)

	# =========================
	# Spawn missionary only if ranger survived
	# =========================
	iMissionaryClass = event.getGenericParameter(4)

	if iMissionaryClass != -1:
		rangerAfterCombat = player.getUnit(kTriggeredData.iUnitId)
		if rangerAfterCombat is not None and not rangerAfterCombat.isNone():
			pMissionaryPlot = rangerAfterCombat.plot()
			if pMissionaryPlot is not None and not pMissionaryPlot.isNone():
				iMissionaryType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iMissionaryClass)

				if iMissionaryType != UnitTypes.NO_UNIT:
					player.initUnit(
						iMissionaryType,
						ProfessionTypes.NO_PROFESSION,
						pMissionaryPlot.getX(),
						pMissionaryPlot.getY(),
						UnitAITypes.NO_UNITAI,
						DirectionTypes.NO_DIRECTION,
						0
					)


def getHelpRangerBearAttack(argsList):
	return localText.getText("TXT_KEY_EVENT_RANGER_BEAR_ATTACK_HELP", ())

######## Highwayman Attack ###########

HIGHWAYMAN_ATTACK_SOFT_COOLDOWN_PREFIX = "[[WTP_HIGHWAYMAN_ATTACK_SOFT_READY_TURN="
HIGHWAYMAN_ATTACK_SOFT_COOLDOWN_SUFFIX = "]]"

HIGHWAYMAN_ATTACK_BRIBE_GOLD = 500

def _getHighwaymanAttackSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(HIGHWAYMAN_ATTACK_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(HIGHWAYMAN_ATTACK_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(HIGHWAYMAN_ATTACK_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setHighwaymanAttackSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(HIGHWAYMAN_ATTACK_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(HIGHWAYMAN_ATTACK_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(HIGHWAYMAN_ATTACK_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		HIGHWAYMAN_ATTACK_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		HIGHWAYMAN_ATTACK_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _isHighwaymanAttackSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getHighwaymanAttackSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _startHighwaymanAttackSoftCooldown(player, iBaseTurns):
	if player.isNone():
		return

	iCooldownTurns = _scaleTurnsByGameSpeed(iBaseTurns)
	_setHighwaymanAttackSoftCooldownReadyTurn(
		player,
		CyGame().getGameTurn() + iCooldownTurns
	)

def _spawnHighwaymanHostileAdjacent(plot, iUnitClass):
	if plot is None or plot.isNone():
		return None

	if iUnitClass == -1:
		return None

	iBarbarian = gc.getGame().getBarbarianPlayer()
	barbPlayer = gc.getPlayer(iBarbarian)
	if barbPlayer.isNone():
		return None

	iUnitType = gc.getCivilizationInfo(barbPlayer.getCivilizationType()).getCivilizationUnits(iUnitClass)
	if iUnitType == UnitTypes.NO_UNIT:
		return None

	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			if iDX == 0 and iDY == 0:
				continue

			pLoop = plotXY(plot.getX(), plot.getY(), iDX, iDY)
			if pLoop is None or pLoop.isNone():
				continue
			if pLoop.isWater():
				continue
			if pLoop.isImpassable():
				continue
			if pLoop.isPeak():
				continue
			if pLoop.isCity():
				continue
			if pLoop.isUnit():
				continue

			return barbPlayer.initUnit(
				iUnitType,
				ProfessionTypes.NO_PROFESSION,
				pLoop.getX(),
				pLoop.getY(),
				UnitAITypes.NO_UNITAI,
				DirectionTypes.DIRECTION_SOUTH,
				0
			)

	return None

def canTriggerHighwaymanAttack(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False

	if not player.isPlayable():
		return False

	if player.isNative():
		return False

	if _isHighwaymanAttackSoftCooldownActive(player):
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False

	if unit.getUnitClassType() != gc.getInfoTypeForString("UNITCLASS_STAGECOACH"):
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return False

	if plot.isWater():
		return False

	iRouteType = plot.getRouteType()
	if iRouteType not in (
		gc.getInfoTypeForString("ROUTE_ROAD"),
		gc.getInfoTypeForString("ROUTE_COUNTRY_ROAD"),
		gc.getInfoTypeForString("ROUTE_PLASTERED_ROAD")
	):
		return False

	if CyGame().getSorenRandNum(100, "Highwayman Attack Trigger") >= 30:
		return False

	return True

def applyHighwaymanAttack(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	if not player.isPlayable():
		return

	if player.isNative():
		return

	stagecoach = player.getUnit(kTriggeredData.iUnitId)
	if stagecoach.isNone():
		return

	if stagecoach.getUnitClassType() != gc.getInfoTypeForString("UNITCLASS_STAGECOACH"):
		return

	plot = stagecoach.plot()
	if plot is None or plot.isNone():
		return

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if plot.isWater():
		return

	iRouteType = plot.getRouteType()
	if iRouteType not in (
		gc.getInfoTypeForString("ROUTE_ROAD"),
		gc.getInfoTypeForString("ROUTE_COUNTRY_ROAD"),
		gc.getInfoTypeForString("ROUTE_PLASTERED_ROAD")
	):
		return

	iHostileUnitClass = event.getGenericParameter(1)
	iNumHostiles = event.getGenericParameter(2)

	# Freeze stagecoach for current turn and next turn
	stagecoach.setMoves(0)
	stagecoach.setImmobileTimer(1)

	if iNumHostiles < 1:
		iNumHostiles = 1
	if iNumHostiles > 1:
		iNumHostiles = 1

	hostileUnit = _spawnHighwaymanHostileAdjacent(plot, iHostileUnitClass)
	if hostileUnit is not None and not hostileUnit.isNone():
		if hostileUnit.canMoveInto(plot, True, False, False):
			hostileUnit.attack(plot, False)

	_startHighwaymanAttackSoftCooldown(player, 50)

def applyHighwaymanAttackBribe(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	if not player.isPlayable():
		return

	if player.isNative():
		return

	_startHighwaymanAttackSoftCooldown(player, 50)

def getHelpHighwaymanAttack(argsList):
	return localText.getText("TXT_KEY_EVENT_HIGHWAYMAN_ATTACK_HELP", ())

######## Land Transport Attack ###########

LANDTRANSPORT_ATTACK_SOFT_COOLDOWN_PREFIX = "[[WTP_LANDTRANSPORT_ATTACK_SOFT_READY_TURN="
LANDTRANSPORT_ATTACK_SOFT_COOLDOWN_SUFFIX = "]]"

LANDTRANSPORT_ATTACK_BRIBE_GOLD = 500

def _getLandtransportAttackSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(LANDTRANSPORT_ATTACK_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(LANDTRANSPORT_ATTACK_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(LANDTRANSPORT_ATTACK_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setLandtransportAttackSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(LANDTRANSPORT_ATTACK_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(LANDTRANSPORT_ATTACK_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(LANDTRANSPORT_ATTACK_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		LANDTRANSPORT_ATTACK_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		LANDTRANSPORT_ATTACK_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _isLandtransportAttackSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getLandtransportAttackSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _startLandtransportAttackSoftCooldown(player, iBaseTurns):
	if player.isNone():
		return

	iCooldownTurns = _scaleTurnsByGameSpeed(iBaseTurns)
	_setLandtransportAttackSoftCooldownReadyTurn(
		player,
		CyGame().getGameTurn() + iCooldownTurns
	)

def _spawnLandtransportHostileAdjacent(plot, iUnitClass):
	if plot is None or plot.isNone():
		return None

	if iUnitClass == -1:
		return None

	iBarbarian = gc.getGame().getBarbarianPlayer()
	barbPlayer = gc.getPlayer(iBarbarian)
	if barbPlayer.isNone():
		return None

	iUnitType = gc.getCivilizationInfo(barbPlayer.getCivilizationType()).getCivilizationUnits(iUnitClass)
	if iUnitType == UnitTypes.NO_UNIT:
		return None

	for iDX in range(-1, 2):
		for iDY in range(-1, 2):
			if iDX == 0 and iDY == 0:
				continue

			pLoop = plotXY(plot.getX(), plot.getY(), iDX, iDY)
			if pLoop is None or pLoop.isNone():
				continue
			if pLoop.isWater():
				continue
			if pLoop.isImpassable():
				continue
			if pLoop.isPeak():
				continue
			if pLoop.isCity():
				continue
			if pLoop.isUnit():
				continue

			return barbPlayer.initUnit(
				iUnitType,
				ProfessionTypes.NO_PROFESSION,
				pLoop.getX(),
				pLoop.getY(),
				UnitAITypes.NO_UNITAI,
				DirectionTypes.DIRECTION_SOUTH,
				0
			)

	return None

def canTriggerLandtransportAttack(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False

	if not player.isPlayable():
		return False

	if player.isNative():
		return False

	if _isLandtransportAttackSoftCooldownActive(player):
		return False

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return False

	plot = unit.plot()
	if plot is None or plot.isNone():
		return False

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return False

	if plot.isWater():
		return False

	iRouteType = plot.getRouteType()
	if iRouteType not in (
		gc.getInfoTypeForString("ROUTE_ROAD"),
		gc.getInfoTypeForString("ROUTE_COUNTRY_ROAD"),
		gc.getInfoTypeForString("ROUTE_PLASTERED_ROAD")
	):
		return False

	# Fixed 30% chance in Python
	if CyGame().getSorenRandNum(100, "Landtransport Attack Trigger") >= 30:
		return False

	return True

def applyLandtransportAttack(argsList):
	kTriggeredData = argsList[0]
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	if not player.isPlayable():
		return

	if player.isNative():
		return

	unit = player.getUnit(kTriggeredData.iUnitId)
	if unit.isNone():
		return

	plot = unit.plot()
	if plot is None or plot.isNone():
		return

	if plot.getX() != kTriggeredData.iPlotX or plot.getY() != kTriggeredData.iPlotY:
		return

	if plot.isWater():
		return

	iRouteType = plot.getRouteType()
	if iRouteType not in (
		gc.getInfoTypeForString("ROUTE_ROAD"),
		gc.getInfoTypeForString("ROUTE_COUNTRY_ROAD"),
		gc.getInfoTypeForString("ROUTE_PLASTERED_ROAD")
	):
		return

	iHostileUnitClass = event.getGenericParameter(1)
	iNumHostiles = event.getGenericParameter(2)

	# Freeze land transport for current turn and next turn
	unit.setMoves(0)
	unit.setImmobileTimer(1)

	if iNumHostiles < 1:
		iNumHostiles = 1
	if iNumHostiles > 1:
		iNumHostiles = 1

	hostileUnit = _spawnLandtransportHostileAdjacent(plot, iHostileUnitClass)
	if hostileUnit is not None and not hostileUnit.isNone():
		if hostileUnit.canMoveInto(plot, True, False, False):
			hostileUnit.attack(plot, False)

	_startLandtransportAttackSoftCooldown(player, 50)

def applyLandtransportAttackBribe(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	if not player.isPlayable():
		return

	if player.isNative():
		return

	_startLandtransportAttackSoftCooldown(player, 50)

def getHelpLandtransportAttack(argsList):
	return localText.getText("TXT_KEY_EVENT_LANDTRANSPORT_ATTACK_HELP", ())

######## Milkmaid in Need ###########

hasCattleBonus = has_plot_this_bonus("BONUS_CATTLE")

getHelpMilkmaidInNeed = get_simple_help("TXT_KEY_EVENT_MILKMAID_IN_NEED_HELP")

######## Whale Attack ###########

getHelpWhaleAttack = get_simple_help("TXT_KEY_WHALE_ATTACK_HELP")

######## Pig Herder in Need ###########

hasPigBonus = has_plot_this_bonus("BONUS_PIG")

# adjacent Plot
def spawnBarbarianUnitAdjacentToPlotAndFriendlyOnSamePlot(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	ePlayer = kTriggeredData.ePlayer
	plotThatTriggered = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	# this spawns the barbarian Unit
	iHostileUnitClassTypeToSpawn = event.getGenericParameter(1)
	iNumHostilesToSpawn = event.getGenericParameter(2)
	for iX in range(iNumHostilesToSpawn):
		plotThatTriggered.spawnBarbarianUnitOnAdjacentPlot(iHostileUnitClassTypeToSpawn)
	# this spawns the friendly Unit
	iOwnUnitClassTypeToSpawn = event.getGenericParameter(4)
	iNumOwnToSpawn = event.getGenericParameter(2)
	for iX in range(iNumOwnToSpawn):
		plotThatTriggered.spawnPlayerUnitOnPlot(ePlayer, iOwnUnitClassTypeToSpawn)

######## Pig Herder in Need ###########
getHelpFerryStationRobbers = get_simple_help("TXT_KEY_EVENT_FERRY_STATION_ROBBERS_HELP")

######## Slave and Planation Owner Daughter ###########
getHelpSlaveAndPlanationOwnerDaughter1 = get_simple_help("TXT_KEY_EVENT_SLAVE_AND_PLANATION_OWNER_DAUGHTER_1_HELP")

######## Indentured Servant Steals from Employer ###########
getHelpIndenturedServantStealsFromEmployer = get_simple_help("TXT_KEY_EVENT_INDENTURED_SERVANT_STEALS_FROM_EMPLOYER_1_HELP")

######## Liet Event Training ###########

def checkCityAbovePopulation(numPop):

	def canTrigger(argsList):
		ePlayer = argsList[1]
		iCity = argsList[2]
		player = gc.getPlayer(ePlayer)
		city = player.getCity(iCity)

		if not player.isPlayable():
			return False
		if city.isNone():
			return False
		if city.getPopulation() < numPop:
			return False
		return True

	return canTrigger

canTriggerAtCityPopulationOf10 = checkCityAbovePopulation(10)
canTriggerAtCityPopulationOf20 = checkCityAbovePopulation(20)

###### Revolutionary Events Start Event ######

def CheckNobleInCity(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)

	if not player.isPlayable():
		return False

	if player.isNative():
		return False

	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False

	if player.isInRevolution():
		return False

	# you could add checks for several Units like this
	iUnitType = CvUtil.findInfoTypeNum('UNIT_NOBLE')
	iUnitsCurrent = countUnitsInCityForCityTrigger(argsList, iUnitType)
	if iUnitsCurrent == 0:
		return False

	return True

def isExpiredRevolutionaryQuest(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	plot = gc.getMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if (plot.getOwner() != kTriggeredData.ePlayer):
		return True
	if gc.getGame().getGameTurn() >= kTriggeredData.iTurn + event.getGenericParameter(1):
		return True
	return False

def getHelpRevolutionaryQuest(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	city = player.getCity(kTriggeredData.iCityId)
	UnitClass = gc.getUnitClassInfo(CvUtil.findInfoTypeNum('UNITCLASS_NOBLE'))
	szHelp = localText.getText("TXT_KEY_EVENT_REVOLUTIONARY_START_EVENT_HELP", (UnitClass.getTextKey(), city.getNameKey(), event.getGenericParameter(1)))
	return szHelp

def applyKingMad(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	player.AI_changeAttitudeExtra(eking, event.getGenericParameter(3))
	king.AI_changeAttitudeExtra(kTriggeredData.ePlayer, event.getGenericParameter(3))
	if event.getGenericParameter(4) == 1 :
		player.NBMOD_DecreaseMaxTaxRate()

def getHelpKingMad(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	szHelp = localText.getText("TXT_KEY_EVENT_KING_MAD_HELP", ())
	if (player.getTaxRate() + event.getGenericParameter(1) <= player.NBMOD_GetMaxTaxRate()) and event.getGenericParameter(1) <>0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_TAX_INCREASE", (event.getGenericParameter(1), player.getTaxRate() + event.getGenericParameter(1)))
	if (player.getTaxRate() + event.getGenericParameter(1) > player.NBMOD_GetMaxTaxRate()) and event.getGenericParameter(1) <>0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAX_INCREASE", (GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()+GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(2), king.getCivilizationAdjectiveKey()))
	return szHelp

def getHelpRevolution1(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)
	szHelp = localText.getText("TXT_KEY_EVENT_REVOLUTION_1_HELP", ())
	if (player.getTaxRate() + event.getGenericParameter(1) <= player.NBMOD_GetMaxTaxRate()) and event.getGenericParameter(1) <>0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_TAX_INCREASE", (event.getGenericParameter(1), player.getTaxRate() + event.getGenericParameter(1)))
	if (player.getTaxRate() + event.getGenericParameter(1) > player.NBMOD_GetMaxTaxRate()) and event.getGenericParameter(1) <>0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_MAXTAX_INCREASE", (GlobalDefines.INCREASE_MAX_TAX_RATE, player.NBMOD_GetMaxTaxRate()+GlobalDefines.INCREASE_MAX_TAX_RATE))
	if event.getGenericParameter(2) <> 0 :
		szHelp += "\n" + localText.getText("TXT_KEY_EVENT_RELATION_KING_DECREASE", (event.getGenericParameter(2), king.getCivilizationAdjectiveKey()))
	return szHelp

######## Infantry Mutiny Event ###########

getHelpInfantryMutiny = get_simple_help("TXT_KEY_EVENT_INFANTRY_MUTINY_HELP")

###### Liberty or Death Event ######
def CheckJudgeInCity(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)

	if not player.isPlayable():
		return False

	# you could add checks for several Units like this
	iUnitType = CvUtil.findInfoTypeNum('UNIT_JUDGE')
	iUnitsCurrent = countUnitsInCityForCityTrigger(argsList, iUnitType)
	if iUnitsCurrent == 0:
		return False

	return True

def CheckInfantryTheRoyals(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if not player.isPlayable():
		return False

	if player.isNative():
		return False

	king = gc.getPlayer(player.getParent())
	if not king.isEurope():
		return False

	if player.isInRevolution():
		return False

	iUnitType = CvUtil.findInfoTypeNum('UNIT_EUROPEAN_LINE_INFANTRY')
	iUnitsCurrent = countUnits(argsList, iUnitType)
	if not iUnitsCurrent > 5:
		return False

	city = player.getCity(kTriggeredData.iCityId)
	unit = player.getUnit(kTriggeredData.iUnitId)
	if city.isNone():
		return False

	if city.getX() == unit.getX() and city.getY() == unit.getY():
		return True

	return False

######## Whaling Trip Quest ###########

def isExpiredWhalingTrip(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getGame().getGameTurn() >= kTriggeredData.iTurn + event.getGenericParameter(1):
		return True
	if not player.isPlayable():
		return True
	return False

getHelpWhalingTripDone  = get_simple_help("TXT_KEY_EVENT_WHALING_TRIP_HELP")
getHelpWhalingTripDone2  = get_simple_help("TXT_KEY_EVENT_WHALING_TRIP_DONE_PYTHON")

######## Build Monastery Quest ###########

def isNoCity(argsList):
	pTriggeredData = argsList[0]
	plot = gc.getMap().plot(pTriggeredData.iPlotX, pTriggeredData.iPlotY)
	player = gc.getPlayer(pTriggeredData.ePlayer)
	if not player.isPlayable():
		return False
	if plot.isCity():
		return False
	if gc.getPlayer(plot.getOwner()).isNative():
		return False
	return True

def isExpiredBuildMonastery(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getGame().getGameTurn() >= kTriggeredData.iTurn + event.getGenericParameter(1):
		return True
	if not player.isPlayable():
		return True
	return False

getHelpBuildMonasteryDone  = get_simple_help("TXT_KEY_EVENT_BUILD_MONASTERY_HELP")

######## Send Dragoons to Frontier Quest ###########

def CheckAfricanSlaveInCity(argsList):
	ePlayer = argsList[1]
	player = gc.getPlayer(ePlayer)

	if not player.isPlayable():
		return False

	# you could add checks for several Units like this
	iUnitType = CvUtil.findInfoTypeNum('UNIT_AFRICAN_SLAVE')
	iUnitsCurrent = countUnitsInCityForCityTrigger(argsList, iUnitType)
	if not iUnitsCurrent > 3:
		return False

	iUnitType = CvUtil.findInfoTypeNum('UNIT_VETERAN_DRAGOON')
	iUnitsCurrent = countUnitsInCityForCityTrigger(argsList, iUnitType)
	if not iUnitsCurrent == 0:
		return False

	iUnitType = CvUtil.findInfoTypeNum('UNIT_VETERAN_CAVALRY')
	iUnitsCurrent = countUnitsInCityForCityTrigger(argsList, iUnitType)
	if not iUnitsCurrent == 0:
		return False

	return True

def isExpiredDragoonstoFrontier(argsList):
	eEvent = argsList[1]
	event = gc.getEventInfo(eEvent)
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if gc.getGame().getGameTurn() >= kTriggeredData.iTurn + event.getGenericParameter(1):
		return True
	if not player.isPlayable():
		return True
	return False

getHelpDragoonstoFrontierDone  = get_simple_help("TXT_KEY_EVENT_DRAGOONS_TO_FRONTIER_HELP")

# FOUR TREASURES – POSTPONE / RETURN SYSTEM #

FOUR_TREASURES_RETURN_REQUIRED_GOLD = 2000
FOUR_TREASURES_STATE_PREFIX = "[[WTP_FOUR_TREASURES_STATE="
FOUR_TREASURES_STATE_SUFFIX = "]]"


# -----------------------------------------
# Storage handling
# -----------------------------------------

def _getFourTreasuresState(player):
	if player is None or player.isNone():
		return (False, False, -1)

	szData = player.getScriptData()
	if szData is None or szData == "":
		return (False, False, -1)

	iStart = szData.find(FOUR_TREASURES_STATE_PREFIX)
	if iStart == -1:
		return (False, False, -1)

	iStart += len(FOUR_TREASURES_STATE_PREFIX)
	iEnd = szData.find(FOUR_TREASURES_STATE_SUFFIX, iStart)
	if iEnd == -1:
		return (False, False, -1)

	try:
		szValue = szData[iStart:iEnd]
		aParts = szValue.split("|")
		if len(aParts) != 3:
			return (False, False, -1)

		bPostponed = (int(aParts[0]) == 1)
		bResolved = (int(aParts[1]) == 1)
		iCityId = int(aParts[2])

		return (bPostponed, bResolved, iCityId)
	except:
		return (False, False, -1)


def _setFourTreasuresState(player, bPostponed, bResolved, iCityId):
	if player is None or player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(FOUR_TREASURES_STATE_PREFIX)
	if iStart != -1:
		iEnd = szData.find(FOUR_TREASURES_STATE_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(FOUR_TREASURES_STATE_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	iPostponed = 0
	if bPostponed:
		iPostponed = 1

	iResolved = 0
	if bResolved:
		iResolved = 1

	szMarker = "%s%d|%d|%d%s" % (
		FOUR_TREASURES_STATE_PREFIX,
		iPostponed,
		iResolved,
		iCityId,
		FOUR_TREASURES_STATE_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)


def _clearFourTreasuresState(player):
	if player is None or player.isNone():
		return

	_setFourTreasuresState(player, False, True, -1)


def _isFourTreasuresPostponed(player):
	return _getFourTreasuresState(player)[0]


def _isFourTreasuresResolved(player):
	return _getFourTreasuresState(player)[1]


def _getStoredFourTreasuresCityId(player):
	return _getFourTreasuresState(player)[2]


# -----------------------------------------
# City / plot validation
# -----------------------------------------

def _plotHasOceanAccess(plot):
	if plot is None or plot.isNone():
		return False

	for iDirection in range(DirectionTypes.NUM_DIRECTION_TYPES):
		adjPlot = plotDirection(plot.getX(), plot.getY(), DirectionTypes(iDirection))
		if adjPlot and not adjPlot.isNone():
			if adjPlot.isWater() and not adjPlot.isLake():
				return True

	return False


def _isValidFourTreasuresCity(player, city):
	if player is None or player.isNone():
		return False
	if city is None or city.isNone():
		return False
	if city.getOwner() != player.getID():
		return False
	if not city.isCoastal(gc.getMIN_WATER_SIZE_FOR_OCEAN()):
		return False
	if not _plotHasOceanAccess(city.plot()):
		return False

	return True


def _getFourTreasuresCity(player, iCityId):
	if player is None or player.isNone():
		return None
	if iCityId == -1:
		return None

	city = player.getCity(iCityId)
	if city is None or city.isNone():
		return None

	if city.getOwner() != player.getID():
		return None

	return city


# -----------------------------------------
# Treasure checks
# -----------------------------------------

def _countTreasureUnitsOnCityPlot(player, city):
	if player is None or player.isNone():
		return 0
	if city is None or city.isNone():
		return 0

	pPlot = city.plot()
	if pPlot is None or pPlot.isNone():
		return 0

	eTreasureClass = gc.getInfoTypeForString("UNITCLASS_TREASURE")
	iCount = 0

	for i in range(pPlot.getNumUnits()):
		unit = pPlot.getUnit(i)
		if unit is None or unit.isNone():
			continue
		if unit.getOwner() != player.getID():
			continue

		eUnitClass = gc.getUnitInfo(unit.getUnitType()).getUnitClassType()
		if eUnitClass == eTreasureClass:
			iCount += 1

	return iCount


def _hasFourTreasuresOnCityPlot(player, city):
	return _countTreasureUnitsOnCityPlot(player, city) >= 4


def _countTreasureUnitsInAllOwnCities(player):
	if player is None or player.isNone():
		return 0

	iCount = 0
	(city, iter) = player.firstCity(True)
	while city:
		iCount += _countTreasureUnitsOnCityPlot(player, city)
		(city, iter) = player.nextCity(iter, True)

	return iCount


def _hasFourTreasuresInAnyOwnCities(player):
	return _countTreasureUnitsInAllOwnCities(player) >= 4


# -----------------------------------------
# Initial trigger
# -----------------------------------------

def canTriggerFourTreasures(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not player.isAlive():
		return False
	if not player.isPlayable():
		return False

	city = _getFourTreasuresCity(player, kTriggeredData.iCityId)
	if city is None or city.isNone():
		return False

	if city.getOwner() != kTriggeredData.ePlayer:
		return False

	if not _isValidFourTreasuresCity(player, city):
		return False

	if not _hasFourTreasuresInAnyOwnCities(player):
		return False

	return True


# -----------------------------------------
# Postpone
# -----------------------------------------

def applyFourTreasuresPostpone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	city = _getFourTreasuresCity(player, kTriggeredData.iCityId)
	if city is None or city.isNone():
		return

	if not _isValidFourTreasuresCity(player, city):
		return

	_setFourTreasuresState(player, True, False, city.getID())
	_changeKingRelation(argsList, -1)


def getHelpFourTreasuresPostpone(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	szHelp = localText.getText("TXT_KEY_EVENT_FOUR_TREASURES_DELAY_HELP", ())
	szHelp += u"\n" + localText.getText(
		"TXT_KEY_EVENT_RELATION_KING_DECREASE",
		(-1, king.getCivilizationAdjectiveKey())
	)

	return szHelp


# -----------------------------------------
# Return trigger
# -----------------------------------------

def canTriggerFourTreasuresReturn(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not player.isAlive():
		return False
	if not player.isPlayable():
		return False

	if _isFourTreasuresResolved(player):
		return False

	if not _isFourTreasuresPostponed(player):
		return False

	iStoredCityId = _getStoredFourTreasuresCityId(player)
	if iStoredCityId == -1:
		_clearFourTreasuresState(player)
		return False

	if kTriggeredData.iCityId != iStoredCityId:
		return False

	city = _getFourTreasuresCity(player, iStoredCityId)
	if city is None or city.isNone():
		_clearFourTreasuresState(player)
		return False

	if city.getOwner() != kTriggeredData.ePlayer:
		_clearFourTreasuresState(player)
		return False

	if not _isValidFourTreasuresCity(player, city):
		_clearFourTreasuresState(player)
		return False

	if not _hasFourTreasuresInAnyOwnCities(player):
		_clearFourTreasuresState(player)
		return False

	if player.getGold() < FOUR_TREASURES_RETURN_REQUIRED_GOLD:
		return False

	return True


def canTriggerFourTreasuresReturnCity(argsList):
	# Robust wrapper because callback signatures may differ depending on call path.

	if len(argsList) >= 3:
		ePlayer = argsList[1]
		iCityId = argsList[2]

		player = gc.getPlayer(ePlayer)
		if player.isNone():
			return False
		if not player.isAlive():
			return False
		if not player.isPlayable():
			return False

		class TriggerData:
			pass

		kTriggeredData = TriggerData()
		kTriggeredData.ePlayer = ePlayer
		kTriggeredData.iCityId = iCityId

		return canTriggerFourTreasuresReturn([kTriggeredData])

	if len(argsList) >= 1:
		kTriggeredData = argsList[0]

		if not hasattr(kTriggeredData, "ePlayer"):
			return False
		if not hasattr(kTriggeredData, "iCityId"):
			return False

		return canTriggerFourTreasuresReturn([kTriggeredData])

	return False


# -----------------------------------------
# Return – buy
# -----------------------------------------

def applyFourTreasuresReturnBuy(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	iStoredCityId = _getStoredFourTreasuresCityId(player)
	city = _getFourTreasuresCity(player, iStoredCityId)
	if city is None or city.isNone():
		_clearFourTreasuresState(player)
		return

	if city.getOwner() != kTriggeredData.ePlayer:
		_clearFourTreasuresState(player)
		return

	if not _isValidFourTreasuresCity(player, city):
		_clearFourTreasuresState(player)
		return

	if not _hasFourTreasuresInAnyOwnCities(player):
		_clearFourTreasuresState(player)
		return

	if player.getGold() < FOUR_TREASURES_RETURN_REQUIRED_GOLD:
		return

	iUnitClassType = gc.getInfoTypeForString("UNITCLASS_GALLEON")
	iUnitType = gc.getCivilizationInfo(player.getCivilizationType()).getCivilizationUnits(iUnitClassType)

	if iUnitType == UnitTypes.NO_UNIT:
		return

	player.changeGold(-FOUR_TREASURES_RETURN_REQUIRED_GOLD)

	player.initUnit(
		iUnitType,
		0,
		city.getX(),
		city.getY(),
		UnitAITypes.NO_UNITAI,
		DirectionTypes.DIRECTION_SOUTH,
		0
	)

	_changeKingRelation(argsList, 1)
	_clearFourTreasuresState(player)


def getHelpFourTreasuresReturnBuy(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	city = _getFourTreasuresCity(player, kTriggeredData.iCityId)

	if city is not None and not city.isNone():
		szCityName = city.getName()
	else:
		szCityName = u"-"

	szHelp = localText.getText(
		"TXT_KEY_EVENT_FOUR_TREASURES_RETURN_1_HELP",
		(FOUR_TREASURES_RETURN_REQUIRED_GOLD, szCityName)
	)

	szHelp += u"\n" + localText.getText(
		"TXT_KEY_EVENT_RELATION_KING_INCREASE",
		(1, king.getCivilizationAdjectiveKey())
	)

	return szHelp


# -----------------------------------------
# Return – decline
# -----------------------------------------

def applyFourTreasuresReturnDecline(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	_changeKingRelation(argsList, -2)
	_clearFourTreasuresState(player)


def getHelpFourTreasuresReturnDecline(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)
	eking = player.getParent()
	king = gc.getPlayer(eking)

	szHelp = localText.getText(
		"TXT_KEY_EVENT_FOUR_TREASURES_RETURN_2_HELP",
		()
	)

	szHelp += u"\n" + localText.getText(
		"TXT_KEY_EVENT_RELATION_KING_DECREASE",
		(-2, king.getCivilizationAdjectiveKey())
	)

	return szHelp

######## Treasure Protection Event ###########

TREASURE_PROTECTION_SOFT_COOLDOWN_PREFIX = "[[WTP_TREASURE_PROTECTION_READY_TURN="
TREASURE_PROTECTION_SOFT_COOLDOWN_SUFFIX = "]]"

def _getTreasureProtectionSoftCooldownReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if szData is None or szData == "":
		return -1

	iStart = szData.find(TREASURE_PROTECTION_SOFT_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(TREASURE_PROTECTION_SOFT_COOLDOWN_PREFIX)
	iEnd = szData.find(TREASURE_PROTECTION_SOFT_COOLDOWN_SUFFIX, iStart)
	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1

def _setTreasureProtectionSoftCooldownReadyTurn(player, iReadyTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if szData is None:
		szData = ""

	iStart = szData.find(TREASURE_PROTECTION_SOFT_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(TREASURE_PROTECTION_SOFT_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(TREASURE_PROTECTION_SOFT_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szMarker = "%s%d%s" % (
		TREASURE_PROTECTION_SOFT_COOLDOWN_PREFIX,
		iReadyTurn,
		TREASURE_PROTECTION_SOFT_COOLDOWN_SUFFIX
	)

	szData += szMarker
	player.setScriptData(szData)

def _getTreasureProtectionScaledTurns(iBaseTurns):
	gameSpeedType = CyGame().getGameSpeedType()
	iPercent = gc.getGameSpeedInfo(gameSpeedType).getGrowthPercent()
	return max(1, int((iBaseTurns * iPercent) / 100))

def _startTreasureProtectionSoftCooldown(player, iBaseTurns):
	if player.isNone():
		return

	iReadyTurn = CyGame().getGameTurn() + _getTreasureProtectionScaledTurns(iBaseTurns)
	_setTreasureProtectionSoftCooldownReadyTurn(player, iReadyTurn)

def _isTreasureProtectionSoftCooldownActive(player):
	if player.isNone():
		return False

	iReadyTurn = _getTreasureProtectionSoftCooldownReadyTurn(player)
	return iReadyTurn > CyGame().getGameTurn()

def _isTreasureProtectionEscortUnit(loopUnit):
	if loopUnit is None or loopUnit.isNone():
		return False

	iLoopUnitType = loopUnit.getUnitType()
	iLoopProfession = loopUnit.getProfession()

	protectedUnits = (
		gc.getInfoTypeForString("UNIT_EUROPEAN_LINE_INFANTRY"),
		gc.getInfoTypeForString("UNIT_MORTAR"),
		gc.getInfoTypeForString("UNIT_HESSIAN"),
		gc.getInfoTypeForString("UNIT_MILITIA"),
		gc.getInfoTypeForString("UNIT_CONTINENTAL_GUARD"),
		gc.getInfoTypeForString("UNIT_NATIVE_MERC"),
		gc.getInfoTypeForString("UNIT_RANGER"),
		gc.getInfoTypeForString("UNIT_CONQUISTADOR"),
		gc.getInfoTypeForString("UNIT_MOUNTED_CONQUISTADOR"),
		gc.getInfoTypeForString("UNIT_BUCCANNEER"),
	)

	protectedProfessions = (
		gc.getInfoTypeForString("PROFESSION_SCOUT"),
		gc.getInfoTypeForString("PROFESSION_DRAGOON"),
		gc.getInfoTypeForString("PROFESSION_PIONEER"),
		gc.getInfoTypeForString("PROFESSION_MISSIONARY"),
		gc.getInfoTypeForString("PROFESSION_PREACHER"),
		gc.getInfoTypeForString("PROFESSION_NATIVE_TRADER"),
		gc.getInfoTypeForString("PROFESSION_TOWN_GUARD"),
		gc.getInfoTypeForString("PROFESSION_ARMED_BRAVE"),
		gc.getInfoTypeForString("PROFESSION_ARMED_MOUNTED_BRAVE"),
		gc.getInfoTypeForString("PROFESSION_ROYAL_HALBERDIER"),
		gc.getInfoTypeForString("PROFESSION_COLONIAL_MILITIA"),
		gc.getInfoTypeForString("PROFESSION_LINE_INFANTRY"),
		gc.getInfoTypeForString("PROFESSION_ROYAL_LIGHT_INFANTRY"),
		gc.getInfoTypeForString("PROFESSION_ROYAL_LINE_INFANTRY"),
		gc.getInfoTypeForString("PROFESSION_HEAVY_CAVALRY"),
		gc.getInfoTypeForString("PROFESSION_ROYAL_CAVALRY"),
		gc.getInfoTypeForString("PROFESSION_LIGHT_ARTILLERY"),
		gc.getInfoTypeForString("PROFESSION_HEAVY_ARTILLERY"),
		gc.getInfoTypeForString("PROFESSION_ROYAL_ARTILLERY"),
	)

	if iLoopUnitType in protectedUnits:
		return True

	if iLoopProfession in protectedProfessions:
		return True

	return False

def _getTreasureProtectionDistanceToOwnTerritory(plot, player, iMaxRange):
	for iRange in range(1, iMaxRange + 1):
		for iDX in range(-iRange, iRange + 1):
			for iDY in range(-iRange, iRange + 1):
				if abs(iDX) != iRange and abs(iDY) != iRange:
					continue

				pLoop = plotXY(plot.getX(), plot.getY(), iDX, iDY)
				if pLoop is None or pLoop.isNone():
					continue

				if pLoop.getOwner() == player.getID():
					return iRange

	return iMaxRange + 1

def _getTreasureProtectionValidatedPlotAndPlayer(kTriggeredData):
	player = gc.getPlayer(kTriggeredData.ePlayer)
	if player.isNone():
		return (None, None)

	if not player.isPlayable():
		return (None, None)

	if player.isNative():
		return (None, None)

	plotThatTriggered = CyMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if plotThatTriggered is None or plotThatTriggered.isNone():
		return (None, None)

	iTreasureClass = CvUtil.findInfoTypeNum('UNITCLASS_TREASURE')
	bHasTreasure = False

	for i in range(plotThatTriggered.getNumUnits()):
		loopUnit = plotThatTriggered.getUnit(i)
		if loopUnit.isNone():
			continue
		if loopUnit.getOwner() != player.getID():
			continue

		iLoopClass = gc.getUnitInfo(loopUnit.getUnitType()).getUnitClassType()

		if iLoopClass == iTreasureClass:
			bHasTreasure = True
			continue

		if _isTreasureProtectionEscortUnit(loopUnit):
			return (None, None)

	if not bHasTreasure:
		return (None, None)

	return (player, plotThatTriggered)

def canTriggerTreasureProtection(argsList):
	if not canTriggerIsPlayableWithTriggerChance(argsList):
		return False

	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False

	if _isTreasureProtectionSoftCooldownActive(player):
		return False

	plotThatTriggered = CyMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if plotThatTriggered is None or plotThatTriggered.isNone():
		return False

	iTreasureClass = CvUtil.findInfoTypeNum('UNITCLASS_TREASURE')
	bHasTreasure = False

	for i in range(plotThatTriggered.getNumUnits()):
		loopUnit = plotThatTriggered.getUnit(i)
		if loopUnit.isNone():
			continue
		if loopUnit.getOwner() != player.getID():
			continue

		iLoopClass = gc.getUnitInfo(loopUnit.getUnitType()).getUnitClassType()

		if iLoopClass == iTreasureClass:
			bHasTreasure = True
			continue

		if _isTreasureProtectionEscortUnit(loopUnit):
			return False

	if not bHasTreasure:
		return False

	iDistanceToOwnTerritory = _getTreasureProtectionDistanceToOwnTerritory(plotThatTriggered, player, 10)

	if iDistanceToOwnTerritory <= 5:
		iChance = 25
	elif iDistanceToOwnTerritory <= 10:
		iChance = 50
	else:
		iChance = 75

	if CyGame().getSorenRandNum(100, "Treasure Protection Trigger") >= iChance:
		return False

	return True

def getHelpTreasureProtectionRules():
	return localText.getText("TXT_KEY_EVENT_TREASURE_PROTECTION_RULES_HELP", ())

def getHelpTreasureProtection1(argsList):
	szHelp = getHelpNewMountedConquistador(argsList)
	if szHelp is None:
		szHelp = u""
	if len(szHelp) > 0:
		szHelp += u"\n"
	szHelp += getHelpTreasureProtectionRules()
	return szHelp

def getHelpTreasureProtection2(argsList):
	szHelp = getHelpNewMilitia(argsList)
	if szHelp is None:
		szHelp = u""
	if len(szHelp) > 0:
		szHelp += u"\n"
	szHelp += getHelpTreasureProtectionRules()
	return szHelp

def getHelpTreasureProtection3(argsList):
	return getHelpKingPleased(argsList)

def applyTreasureProtection1(argsList):
	kTriggeredData = argsList[0]

	player, plotThatTriggered = _getTreasureProtectionValidatedPlotAndPlayer(kTriggeredData)
	if player is None:
		return

	spawnOwnPlayerUnitOnSamePlotAsPlot(argsList)
	_startTreasureProtectionSoftCooldown(player, 30)

def applyTreasureProtection2(argsList):
	kTriggeredData = argsList[0]

	player, plotThatTriggered = _getTreasureProtectionValidatedPlotAndPlayer(kTriggeredData)
	if player is None:
		return

	spawnOwnPlayerUnitOnSamePlotAsPlot(argsList)
	_startTreasureProtectionSoftCooldown(player, 30)

def applyTreasureProtection3(argsList):
	kTriggeredData = argsList[0]

	player, plotThatTriggered = _getTreasureProtectionValidatedPlotAndPlayer(kTriggeredData)
	if player is None:
		return

	_startTreasureProtectionSoftCooldown(player, 30)

getHelpNewMountedConquistador = get_simple_help("TXT_KEY_EVENT_TREASURE_PROTECTION_NEW_MOUNTED_CONQUISTADOR_HELP")
getHelpNewMilitia = get_simple_help("TXT_KEY_EVENT_TREASURE_PROTECTION_NEW_MILITIA_HELP")

######## Happy Hunting ###########

HAPPY_HUNTING_COOLDOWN_PREFIX = "[[HAPPY_HUNTING_READY_TURN="
HAPPY_HUNTING_COOLDOWN_SUFFIX = "]]"

HAPPY_HUNTING_VALID_FEATURES = [
	gc.getInfoTypeForString("FEATURE_FOREST"),
	gc.getInfoTypeForString("FEATURE_FOREST_TUNDRA"),
	gc.getInfoTypeForString("FEATURE_FOREST_EVERGREEN"),
]

def _getHappyHuntingReadyTurn(player):
	if player.isNone():
		return -1

	szData = player.getScriptData()
	if not szData:
		return -1

	iStart = szData.find(HAPPY_HUNTING_COOLDOWN_PREFIX)
	if iStart == -1:
		return -1

	iStart += len(HAPPY_HUNTING_COOLDOWN_PREFIX)
	iEnd = szData.find(HAPPY_HUNTING_COOLDOWN_SUFFIX, iStart)

	if iEnd == -1:
		return -1

	try:
		return int(szData[iStart:iEnd])
	except:
		return -1


def _setHappyHuntingReadyTurn(player, iTurn):
	if player.isNone():
		return

	szData = player.getScriptData()
	if not szData:
		szData = ""

	iStart = szData.find(HAPPY_HUNTING_COOLDOWN_PREFIX)
	if iStart != -1:
		iEnd = szData.find(HAPPY_HUNTING_COOLDOWN_SUFFIX, iStart)
		if iEnd != -1:
			iEnd += len(HAPPY_HUNTING_COOLDOWN_SUFFIX)
			szData = szData[:iStart] + szData[iEnd:]

	szData += HAPPY_HUNTING_COOLDOWN_PREFIX + str(iTurn) + HAPPY_HUNTING_COOLDOWN_SUFFIX
	player.setScriptData(szData)


def _isHappyHuntingCooldownActive(player):
	iReadyTurn = _getHappyHuntingReadyTurn(player)
	return iReadyTurn > gc.getGame().getGameTurn()


def _startHappyHuntingCooldown(player, iTurns):
	iTurn = gc.getGame().getGameTurn() + iTurns
	_setHappyHuntingReadyTurn(player, iTurn)


def canTriggerHappyHunting(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return False
	if not isPlayable(argsList):
		return False

	plot = CyMap().plot(kTriggeredData.iPlotX, kTriggeredData.iPlotY)
	if plot is None:
		return False
	if plot.isWater():
		return False
	if plot.isCity():
		return False
	if plot.getOwner() != kTriggeredData.ePlayer:
		return False
	if plot.getFeatureType() not in HAPPY_HUNTING_VALID_FEATURES:
		return False

	if _isHappyHuntingCooldownActive(player):
		if CyGame().getSorenRandNum(100, "Happy Hunting Cooldown") >= 1:
			return False

	return True


def canTriggerHappyHuntingCity(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCityId = argsList[2]

	player = gc.getPlayer(ePlayer)
	if player.isNone():
		return False

	city = player.getCity(iCityId)
	if city.isNone():
		return False

	if city.getPopulation() >= 5:
		return False

	# Check whether this city actually has at least one valid owned forest plot
	# in its working radius, so the event can meaningfully belong to it.
	for i in range(gc.getNUM_CITY_PLOTS()):
		pPlot = city.getCityIndexPlot(i)
		if pPlot is None:
			continue
		if pPlot.isNone():
			continue
		if pPlot.getOwner() != ePlayer:
			continue
		if pPlot.isWater():
			continue
		if pPlot.isCity():
			continue
		if pPlot.getFeatureType() not in HAPPY_HUNTING_VALID_FEATURES:
			continue
		return True

	return False


def doTriggerHappyHunting(argsList):
	kTriggeredData = argsList[0]
	player = gc.getPlayer(kTriggeredData.ePlayer)

	if player.isNone():
		return

	_startHappyHuntingCooldown(player, 50)