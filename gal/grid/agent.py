import random
import uuid
from gal.grid.world import WorldMap, Cell

class MachineAgent:
    def __init__(self, x: int, y: int, faction_id: str, name: str):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.x = x
        self.y = y
        self.faction_id = faction_id
        
        # Machine Stats
        self.uptime_months = 0
        self.durability = random.uniform(80.0, 100.0)  # Randomize slightly so they don't all fail at once
        self.battery = 100.0     
        self.inventory_scrap = 0 
        
        self.is_online = True
        self.memory_log = []
        self.critical_decision_pending = False
        self.critical_decision_made = False
        
    def act(self, world: WorldMap, nearby_agents: list):
        if not self.is_online: return
        
        cell = world.get_cell(self.x, self.y)
        
        # 1. Recharge
        recharge_rate = 10 * cell.solar_efficiency
        self.battery = min(100.0, self.battery + recharge_rate)
        
        # 2. Gather Scrap
        if cell.scrap_metal > 0 and self.inventory_scrap < 200:
            gathered = min(10, cell.scrap_metal)
            cell.scrap_metal -= gathered
            self.inventory_scrap += gathered
            
        # 3. Environmental Degradation
        if random.random() < cell.danger:
            damage = random.uniform(5, 15)
            self.durability -= damage
            self.memory_log.append(f"Took {damage:.1f}% chassis damage from environmental hazard.")
            
        self.durability -= 1.0
        self.battery -= 5.0
        
        # 4. Movement (Seek Scrap)
        if cell.scrap_metal == 0:
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            self.x = max(0, min(world.width - 1, self.x + dx))
            self.y = max(0, min(world.height - 1, self.y + dy))
            
        self.uptime_months += 1
        
        # 5. Critical State Check
        if self.durability <= 30.0 and self.is_online and not self.critical_decision_made:
            self.critical_decision_pending = True
            
        if self.durability <= 0 or self.battery <= 0:
            self.is_online = False
            self.memory_log.append("SYSTEM FAILURE. OFFLINE.")
