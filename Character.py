import logging

class Character:
    __character_data:list[dict] = [{}]

    def __init__(self, name=None):
        self.code = 0
        self.name = "Jackie"
        self.maxHp = 940
        self.maxSp = 630
        self.strLearnStartSkill = "Passive,Attack,SpecialSkill"
        self.strUsePointLearnStartSkill = ""
        self.initExtraPoint = 0
        self.maxExtraPoint = 0
        self.attackPower = 43
        self.defence = 55
        self.skillAmp = 0
        self.adaptiveForce = 0
        self.criticalStrikeChance = 0
        self.hpRegen = 1.28
        self.spRegen = 4.7
        self.attackSpeed = 0.1
        self.attackSpeedRatio = 0
        self.increaseBasicAttackDamageRatio = 0
        self.skillAmpRatio = 0
        self.preventBasicAttackDamagedRatio = 0
        self.preventSkillDamagedRatio = 0
        self.attackSpeedLimit = 2.5
        self.attackSpeedMin = 0
        self.moveSpeed = 3.55
        self.sightRange = 8.5
        self.radius = 0.4
        self.pathingRadius = 0.4
        self.uiHeight = 2.6
        self.initStateDisplayIndex = -1
        self.localScaleInCutscene = 65
        self.localScaleInVictoryScene = "S"
        self.resource = "Jackie"
        self.lobbySubObject = ""

        self.__getCharacter(name)

    def __getCharacter(self, name):
        if name is None: return

        for d in Character.__character_data:
            if d['name'] == name:
                for key in list(d.keys()):
                    exec(f'self.{key} = d[key]')
                return
            
        logging.warning("Character not found")

    @classmethod
    def loadData(cls, data):
        if data is None: return

        Character.__character_data = data

        logging.info("Character data loaded")