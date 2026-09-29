"""战场补给与后勤系统 - 红态测试"""
import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from battleground.logistics import LogisticsSystem

class TestCaptureMechanism:
    def test_supply_point_needs_capture(self):
        ls = LogisticsSystem()
        assert ls.needs_capture("point_a") == True

class TestSupplyInterception:
    def test_supply_lines_can_be_intercepted(self):
        ls = LogisticsSystem()
        assert ls.can_intercept_supply("line_1") == True

class TestTransportTime:
    def test_longer_distance_takes_more_time(self):
        ls = LogisticsSystem()
        t1 = ls.get_transport_time(10)
        t2 = ls.get_transport_time(100)
        assert t2 > t1

class TestConsumption:
    def test_more_troops_consume_more(self):
        ls = LogisticsSystem()
        c1 = ls.get_consumption(100, 1.0)
        c2 = ls.get_consumption(10000, 1.0)
        assert c2 > c1

class TestCaptureBonus:
    def test_capturing_supply_point_gives_bonus(self):
        ls = LogisticsSystem()
        bonus = ls.get_capture_bonus("point_a")
        assert bonus != {}

class TestStorageLimit:
    def test_supply_has_storage_limit(self):
        ls = LogisticsSystem()
        limit = ls.get_storage_limit()
        assert limit < 10000

class TestSupplyTypes:
    def test_multiple_supply_types(self):
        ls = LogisticsSystem()
        types = ls.get_supply_types()
        assert len(types) > 1

class TestActivationCooldown:
    def test_captured_point_has_cooldown(self):
        ls = LogisticsSystem()
        cd = ls.get_activation_cooldown()
        assert cd > 0

class TestRetreatTransfer:
    def test_retreat_transfers_some_supplies(self):
        ls = LogisticsSystem()
        rate = ls.get_retreat_transfer_rate()
        assert rate > 0
