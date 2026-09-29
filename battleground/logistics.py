"""战场补给与后勤系统"""
from dataclasses import dataclass, field


# 补给类型：弹药/药品/工程/燃油，各自独立
SUPPLY_TYPES = ["ammo", "medical", "engineering", "fuel"]

# 运输速度：单位距离每秒
TRANSPORT_SPEED = 1.0

# 基础消耗系数：每兵每秒
BASE_CONSUMPTION_PER_TROOP = 0.1


class LogisticsSystem:
    def __init__(self):
        self.supply_points: dict = {}  # 补给点需占领才能使用
        self.supply_lines: dict = {}  # 补给线可被截断
        self.transport_speed: float = TRANSPORT_SPEED  # 运输按距离计时
        self.base_consumption: float = BASE_CONSUMPTION_PER_TROOP  # 按兵力与强度
        self.capture_reward: dict = {"points": 100, "resource_bonus": 0.2}
        self.storage_limit: int = 1000  # 囤积上限，超过浪费
        self.supply_types: list = list(SUPPLY_TYPES)
        self.activation_cooldown: float = 30.0  # 占领后激活冷却（秒）
        self.retreat_transfer_rate: float = 0.5  # 撤退可转移50%
        self.capture_duration: float = 5.0  # 占领读条时间（秒）

    def needs_capture(self, point_id: str) -> bool:
        # 补给点需要占领（带读条）才能使用
        return True

    def can_intercept_supply(self, line_id: str) -> bool:
        # 补给线需要保护，可被敌方截断
        return True

    def get_transport_time(self, distance: float) -> float:
        # 运输时间按距离计算，远距离需要更久
        if distance <= 0:
            return 0.0
        return distance / self.transport_speed

    def get_consumption(self, troops: int, intensity: float) -> float:
        # 消耗按兵力数量和战斗强度计算
        return self.base_consumption * troops * max(intensity, 0.0)

    def get_capture_bonus(self, point_id: str) -> dict:
        # 占领补给点给予团队积分和资源加成
        return dict(self.capture_reward)

    def get_storage_limit(self) -> int:
        # 囤积上限，超过部分浪费
        return self.storage_limit

    def get_supply_types(self) -> list:
        # 弹药/药品/工程/燃油，各自独立
        return list(self.supply_types)

    def get_activation_cooldown(self) -> float:
        # 占领后的激活冷却时间（秒）
        return self.activation_cooldown

    def get_retreat_transfer_rate(self) -> float:
        # 撤退时可转移的补给比例，运输按距离计时
        return self.retreat_transfer_rate
