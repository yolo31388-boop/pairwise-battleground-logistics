"""战场补给与后勤系统"""
from dataclasses import dataclass, field

SUPPLY_TYPES = ["ammo", "medical", "engineering", "fuel"]


@dataclass
class SupplyPoint:
    point_id: str
    owner: str = ""
    capture_progress: float = 0.0
    capture_time: float = 5.0
    cooldown_remaining: float = 0.0

    @property
    def captured(self) -> bool:
        return bool(self.owner) and self.capture_progress >= self.capture_time

    @property
    def usable(self) -> bool:
        return self.captured and self.cooldown_remaining <= 0


@dataclass
class SupplyLine:
    line_id: str
    protected: bool = False
    cut: bool = False


class LogisticsSystem:
    def __init__(self):
        self.supply_points: dict = {}
        self.supply_lines: dict = {}
        self.transport_speed: float = 10.0  # 距离单位/秒
        self.base_consumption: float = 0.1  # 每兵每秒基础消耗
        self.capture_reward: dict = {"team_points": 100, "resource_bonus": 0.1}
        self.storage_limit: int = 1000
        self.supply_types: list = list(SUPPLY_TYPES)
        self.activation_cooldown: float = 30.0
        self.retreat_transfer_rate: float = 0.5
        self.stockpile: dict = {t: 0 for t in self.supply_types}

    # bug1: 补给点需要占领才能使用
    def needs_capture(self, point_id: str) -> bool:
        point = self.supply_points.get(point_id)
        return point is None or not point.usable

    def capture_point(self, point_id: str, faction: str, elapsed: float) -> bool:
        point = self.supply_points.setdefault(point_id, SupplyPoint(point_id))
        point.owner = faction
        point.capture_progress += elapsed
        if point.captured:
            point.cooldown_remaining = self.activation_cooldown
            return True
        return False

    # bug2: 补给线可被截断，截断后前线补给减少
    def can_intercept_supply(self, line_id: str) -> bool:
        line = self.supply_lines.get(line_id)
        return line is None or not line.protected

    def frontline_supply_factor(self, line_id: str) -> float:
        line = self.supply_lines.get(line_id)
        return 0.25 if (line and line.cut) else 1.0

    # bug3: 运输时间按距离计算
    def get_transport_time(self, distance: float) -> float:
        return distance / self.transport_speed

    # bug4: 消耗按兵力数量和战斗强度计算
    def get_consumption(self, troops: int, intensity: float) -> float:
        return self.base_consumption * troops * intensity

    # bug5: 占领补给点给团队积分和资源加成
    def get_capture_bonus(self, point_id: str) -> dict:
        point = self.supply_points.get(point_id)
        if point is None or point.captured:
            return dict(self.capture_reward)
        return {}

    # bug6: 囤积上限，超过浪费
    def get_storage_limit(self) -> int:
        return self.storage_limit

    def store(self, supply_type: str, amount: int) -> int:
        if supply_type not in self.stockpile:
            raise ValueError(f"unknown supply type: {supply_type}")
        self.stockpile[supply_type] = min(
            self.stockpile[supply_type] + amount, self.storage_limit
        )
        return self.stockpile[supply_type]

    # bug7: 补给分类型，各自独立
    def get_supply_types(self) -> list:
        return list(self.supply_types)

    # bug8: 占领后有激活冷却
    def get_activation_cooldown(self) -> float:
        return self.activation_cooldown

    # bug9: 撤退时转移部分补给，有运输时间
    def get_retreat_transfer_rate(self) -> float:
        return self.retreat_transfer_rate

    def retreat_transfer(self, supply_type: str, distance: float) -> dict:
        amount = int(self.stockpile.get(supply_type, 0) * self.retreat_transfer_rate)
        self.stockpile[supply_type] -= amount
        return {"amount": amount, "arrival_time": self.get_transport_time(distance)}
