from typing import Dict


class RevenuePredictor:

    def predict(self, deal_data: Dict) -> float:
        return self._rule_based_score(deal_data)

    def _rule_based_score(self, deal_data: Dict) -> float:
        score = 0

        amount = deal_data.get("amount", 0)
        interaction = deal_data.get("interaction_count", 0)
        days = deal_data.get("days_open", 0)

        score += 20 if amount > 10000 else 10
        score += 30 if interaction > 5 else 10
        score += 30 if days < 30 else 10

        return min(score / 100, 1.0)


def predict_deal_probability(deal_data: Dict) -> float:
    predictor = RevenuePredictor()
    return predictor.predict(deal_data)
