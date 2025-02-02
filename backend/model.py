import easyocr
import cv2
import numpy as np
import re
from sentence_transformers import SentenceTransformer, util
from sympy import simplify, sympify

def extract_text(image_path):
    reader = easyocr.Reader(['en'])
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = reader.readtext(gray, detail=0)
    # return "\n".join(results)
    return [line.strip() for line in results if line.strip()]


nlp_model = SentenceTransformer('all-MiniLM-L6-v2')

def is_numerical(answer):
    return bool(re.fullmatch(r'[-+]?\d*\.?\d+', answer.strip()))

def is_algebraic(expression):
    try:
        sympify(expression)
        return True
    except:
        return False

def grade_nlp_answer(correct_answer, student_answer):
    # print("Grading descriptive answer...")
    correct_embedding = nlp_model.encode(correct_answer, convert_to_tensor=True)
    student_embedding = nlp_model.encode(student_answer, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(correct_embedding, student_embedding).item()
    print(f"Similarity Score: {similarity}")

    if similarity >= 0.85:
        return "Full Marks", similarity
    elif similarity >= 0.6:
        return "Partial Marks", similarity
    else:
        return "Incorrect", similarity

def check_exact_match(correct_answer, student_answer):
    # print("Checking exact numerical match...")
    return float(correct_answer) == float(student_answer)

def check_with_tolerance(correct_answer, student_answer, tolerance=0.01):
    # print("Checking numerical match with tolerance...")
    return abs(float(correct_answer) - float(student_answer)) <= tolerance

def check_equivalent_expressions(correct_expr, student_expr):
    # print("Checking algebraic expressions...")
    try:
        correct_expr = sympify(correct_expr)
        student_expr = sympify(student_expr)
        return simplify(correct_expr) == simplify(student_expr)
    except:
        return False

def grade_answer(correct_answer, student_answer, tolerance=0.01):
    # print("Starting grading...")

    # Check if it's a numerical value
    if is_numerical(correct_answer) and is_numerical(student_answer):
        # print("Grading numerical answer...")

        if check_exact_match(correct_answer, student_answer):
            return "Full Marks (Exact Match)"
        elif check_with_tolerance(correct_answer, student_answer, tolerance):
            return f"Partial Marks (Close, within {tolerance})"
        else:
            return "Incorrect (Numerical Mismatch)"
    
    # Check if it's an algebraic expression
    elif is_algebraic(correct_answer) and is_algebraic(student_answer):
        # print("Grading algebraic expression...") 

        if check_equivalent_expressions(correct_answer, student_answer):
            return "Full Marks (Equivalent Expressions)"
        else:
            return "Incorrect (Formula Mismatch)"
    
    # Otherwise, assume it's a descriptive text
    else:
        # print("Grading descriptive text...")
        return grade_nlp_answer(correct_answer, student_answer)

image_path = "static/image.png"
student_descriptive = extract_text(image_path)

correct_descriptive = "Newton's first law states that an object in motion stays in motion unless acted upon by an external force."
correct_numerical = "9.81"
correct_formula = "(x+1)^2"

for i, text in enumerate(student_descriptive):
    text_filename = f"extracted_text_{i+1}.txt"
    with open(text_filename, "w") as text_file:
        text_file.write(text)
    # print(f"\nExtracted text for line {i+1} saved as '{text_filename}'")

    # print(f"\nExtracted Student Answer for line {i+1}:\n", text)
    if is_numerical(text):
        # print("\nGrading Result:\n", grade_answer(correct_numerical, text))
        result = grade_answer(correct_numerical, text)
        print(f"\nGrading Result for line {i+1}: {result}")
    elif is_algebraic(text):
        # print("\nGrading Result:\n", grade_answer(correct_formula, text))
        result = grade_answer(correct_formula, text)
        print(f"\nGrading Result for line {i+1}: {result}")
    else:
        # print("\nGrading Result:\n", grade_answer(correct_descriptive, text))
        result = grade_answer(correct_descriptive, text)
        print(f"\nGrading Result for line {i+1}: {result}")
