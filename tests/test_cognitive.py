import pytest
from core.cognitive.modules.perceiver import Perceiver
from core.cognitive.modules.critic import Critic

def test_perceiver_analysis():
    p = Perceiver()
    res = p.analyze("Test Goal")
    assert "intent" in res

def test_critic_audit():
    c = Critic()
    assert c.audit(["evidence"], "goal") is True
    assert c.audit([], "goal") is False
