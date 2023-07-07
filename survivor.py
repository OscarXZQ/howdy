class Survivor:
    def __init__(self, answers, action_plan, important_questions=None, description=None, feelings=None, impact=None):
        self.answers = answers
        self.action_plan = action_plan
        self.important_questions = important_questions or [0, 1, 2, 3]
        self.description = description or ""
        self.feelings = feelings or ""
        self.impact = impact or ""
    
    def update_important_mcqs(self, new_important_mcqs):
        self.important_questions = new_important_mcqs
    
    # Calculate the similarity between this survivor and another survivor
    def calculate_similarity(self, another_survivor):
        matching_answers = 0
        for index, (self_answer, another_answer) in enumerate(zip(self.answers, another_survivor.answers), start=0):
            if index not in self.important_questions:
                continue
            if index == 0:
                for option in range(6):
                    if (option in self_answer and option in another_answer) or (option not in self_answer and option not in another_answer):
                        matching_answers += 1/6
            elif index == 1 or index == 3:
                for option in range(3):
                    if (option in self_answer and option in another_answer) or (option not in self_answer and option not in another_answer):
                        matching_answers += 1/3
            else:
                if self_answer == another_answer:
                    matching_answers += 1
        return matching_answers
    
    # Find the top 3 survivors that are most similar to this survivor
    def find_most_similar_survivors(self, all_survivors):
        # Calculate similarity scores between this survivor and all existing survivors
        similarities = [(index, self.calculate_similarity(survivor)) for index, survivor in enumerate(all_survivors)]
        
        # Sort and get the indices of the top 3 similar survivors
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
        top_indices = [index for index, _ in sorted_similarities[:3]]

        # Return the top 3 similar survivors
        return [all_survivors[index] for index in top_indices]
    
    # Get recommended action items for this survivor
    def get_recommended_action_items(self, all_survivors):
        most_similar_survivors = self.find_most_similar_survivors(all_survivors)
        rec_action_items = []
        for similar_survivor in most_similar_survivors:
            for stakeholder, actions in similar_survivor.action_plan.items():
                for action in actions:
                    rec_action_items.append((stakeholder, action))
        return rec_action_items
    
    # Get recommended action items for this survivor, divided into same stakeholder and different stakeholder
    def divide_recommended_action_items(self, all_survivors):
        recommended_items = self.get_recommended_action_items(all_survivors)
        
        stakeholder_set = set(self.action_plan.keys())
        from_same_stakeholder = []
        from_different_stakeholder = []

        for stakeholder, action in recommended_items:
            if stakeholder in stakeholder_set:
                from_same_stakeholder.append((stakeholder, action))
            else:
                from_different_stakeholder.append((stakeholder, action))

        return from_same_stakeholder, from_different_stakeholder
    
    def update_action_plan(self, new_action_plan):
        action_items = {}
        current_stakeholder = None
        for item in new_action_plan:
            current_stakeholder = item['stakeholder']
            current_action = item['action']
            if current_stakeholder not in action_items:
                action_items[current_stakeholder] = [current_action]
            else:
                action_items[current_stakeholder].append(current_action)
        self.action_plan = action_items