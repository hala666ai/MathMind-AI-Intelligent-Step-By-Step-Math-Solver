import sympy as sp
import re
import random

# ============================
# 1) NLP PARSER
# ============================

def parse_problem(text):
    text = text.lower().strip()

    # Detect differentiation
    if "derivative" in text or "تفاضل" in text or "اشتق" in text:
        match = re.search(r"of (.*)", text)
        if match:
            expr = match.group(1)
            return {"type": "derivative", "expr": expr}

    # Detect solving equations
    if "solve" in text or "حل" in text:
        match = re.search(r"solve (.*)", text)
        if match:
            expr = match.group(1)
            return {"type": "solve", "expr": expr}

    # Detect probability
    if "probability" in text or "احتمال" in text:
        return {"type": "probability", "expr": text}

    # Fallback: treat as algebraic expression
    return {"type": "algebra", "expr": text}


# ============================
# 2) MATH ENGINE
# ============================

def solve_derivative(expr):
    x = sp.symbols('x')
    try:
        f = sp.sympify(expr)
        df = sp.diff(f, x)
        return f, df
    except:
        return None, None


def solve_equation(expr):
    x = sp.symbols('x')
    try:
        eq = sp.sympify(expr)
        sol = sp.solve(eq, x)
        return eq, sol
    except:
        return None, None


def solve_algebra(expr):
    x = sp.symbols('x')
    try:
        simplified = sp.simplify(expr)
        return simplified
    except:
        return None


def solve_probability(text):
    # Simple probability engine
    if "coin" in text or "عملة" in text:
        return "Probability of heads = 1/2, tails = 1/2"

    if "dice" in text or "نرد" in text:
        return "Probability of rolling any number (1–6) = 1/6"

    return "Probability problem detected, but needs more details."


# ============================
# 3) EXPLANATION ENGINE
# ============================

def explain_steps(result, mode="neutral", problem_type="algebra", expr=None):
    if result is None:
        return "I couldn't understand the problem. Try rewriting it."

    if problem_type == "derivative":
        f, df = result
        base = f"The derivative of f(x) = {f} is f'(x) = {df}."

        if mode == "kids":
            return base + "\n\nThink of the derivative as how fast the function changes."
        elif mode == "pro":
            return base + "\n\nUsing symbolic differentiation rules, we applied linearity and power rules."
        return base

    if problem_type == "solve":
        eq, sol = result
        base = f"Solving the equation {eq} gives solutions: {sol}"

        if mode == "kids":
            return base + "\n\nWe try to isolate x step by step until we find its value."
        elif mode == "pro":
            return base + "\n\nWe used algebraic manipulation and SymPy's symbolic solver."
        return base

    if problem_type == "algebra":
        base = f"Simplified expression: {result}"

        if mode == "kids":
            return base + "\n\nWe made the expression shorter and easier to understand."
        elif mode == "pro":
            return base + "\n\nThis simplification uses algebraic identities and symbolic reduction."
        return base

    if problem_type == "probability":
        base = f"Probability result: {result}"

        if mode == "kids":
            return base + "\n\nProbability tells us how likely something is to happen."
        elif mode == "pro":
            return base + "\n\nThis is based on classical probability theory."
        return base


# ============================
# 4) ERROR DETECTOR
# ============================

def detect_student_error(student_answer, correct_answer):
    try:
        s = sp.simplify(student_answer)
        c = sp.simplify(correct_answer)
        if s == c:
            return "Your answer is correct!"
        else:
            return f"Your answer is not correct. Try checking your algebra steps."
    except:
        return "I couldn't analyze your answer."


# ============================
# 5) MAIN AI FUNCTION
# ============================

def MathMind_AI(problem, mode="neutral", student_answer=None):
    parsed = parse_problem(problem)
    ptype = parsed["type"]
    expr = parsed["expr"]

    if ptype == "derivative":
        result = solve_derivative(expr)
        explanation = explain_steps(result, mode, "derivative", expr)

    elif ptype == "solve":
        result = solve_equation(expr)
        explanation = explain_steps(result, mode, "solve", expr)

    elif ptype == "probability":
        result = solve_probability(expr)
        explanation = explain_steps(result, mode, "probability", expr)

    else:
        result = solve_algebra(expr)
        explanation = explain_steps(result, mode, "algebra", expr)

    # If student answer provided → check correctness
    if student_answer:
        correctness = detect_student_error(student_answer, str(result))
        return explanation + "\n\n" + correctness

    return explanation


# ============================
# 6) DEMO
# ============================

if __name__ == "__main__":
    print("=== MathMind AI ===")
    while True:
        q = input("\nEnter a math problem: ")
        mode = input("Mode (kids/pro/neutral): ")
        print("\nAI:", MathMind_AI(q, mode))