import random
from dataclasses import dataclass


@dataclass
class Task:
    task: str
    answer: int
    user_answer: int | None = None


def get_task() -> Task:
    operation = random.choice(["+", "-"])
    first_number = random.randint(1, 10)
    second_number = random.randint(1, 10)
    task = f"{first_number} {operation} {second_number}"
    answer = eval(task)
    return Task(task, answer)


def count_right_answers(quiz: list[dict]) -> int:
    return sum(task["user_answer"] == task["answer"] for task in quiz)
