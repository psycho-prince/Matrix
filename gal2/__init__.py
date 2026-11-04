"""GAL 2.0 experimental research implementation."""
from .agent import Agent
from .adaptive_inheritance import AdaptationPolicy, adaptive_inherit
from .inheritance import inherit_capabilities, verify_inherited_capability
from .models import Capability, Evidence, EvaluationReport, MemoryKind, MemoryRecord, Task
__all__=["Agent","AdaptationPolicy","adaptive_inherit","inherit_capabilities",
         "verify_inherited_capability","Capability","Evidence","EvaluationReport",
         "MemoryKind","MemoryRecord","Task"]
