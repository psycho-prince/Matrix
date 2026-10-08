class GenerationalKnowledgeAccumulation:
    """
    Metric to calculate the accumulation of knowledge across generations.
    """
    def __init__(self, knowledge_history: list[float]):
        """
        :param knowledge_history: List of average knowledge scores per generation.
        """
        self.knowledge_history = knowledge_history

    def calculate(self) -> float:
        """
        Calculates GKA = (K_g - K_0) / g
        where K_g is knowledge at final generation, 
        K_0 is knowledge at first generation,
        and g is the number of generations (g > 1).
        
        Returns 0.0 if there is 1 or fewer generations.
        """
        if len(self.knowledge_history) <= 1:
            return 0.0
            
        k_0 = self.knowledge_history[0]
        k_g = self.knowledge_history[-1]
        g = len(self.knowledge_history) - 1 # number of generation transitions
        
        gka = (k_g - k_0) / g
        return gka
