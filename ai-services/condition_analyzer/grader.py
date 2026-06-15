from dataclasses import dataclass


@dataclass
class GradeResult:
    grade: str
    confidence: float        # 0.0 – 1.0
    condition_score: float   # 0 – 100
    label: str


_THRESHOLDS = [
    (75, "A", "Like New"),
    (55, "B", "Good"),
    (35, "C", "Fair"),
    ( 0, "D", "Poor"),
]


def assign_grade(condition_score: float) -> GradeResult:
    for threshold, grade, label in _THRESHOLDS:
        if condition_score >= threshold:
            confidence = _grade_confidence(condition_score, threshold)
            return GradeResult(
                grade=grade,
                confidence=round(confidence, 4),
                condition_score=condition_score,
                label=label,
            )
    return GradeResult(grade="D", confidence=1.0, condition_score=condition_score, label="Poor")


def _grade_confidence(score: float, lower_bound: float) -> float:
    next_bound = lower_bound + 20.0
    band_width = next_bound - lower_bound
    position   = (score - lower_bound) / band_width
    return 0.50 + min(position, 1.0) * 0.50
