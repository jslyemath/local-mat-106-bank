import slye_math as sm
import random
import math
from fractions import Fraction


def generate(**kwargs):
    # We will only divide certain shapes certain ways in area models
    # 'shape' : [ways to divide]
    shapes_dict = {
        'circle': [2, 3, 4, 6, 8],
        'isosceles trapezoid': [2, 3, 6],
        'equilateral triangle': [2, 3],
        'regular hexagon': [2, 3, 4, 6],
        'rectangle': [2, 3, 4, 5, 6, 8],
        'semicircle': [2, 3, 4]
    }

    def gen_easy_line_prob():
        # Gives students a problem where the given is 1

        shape = 'line'
        # Choose from tick locations that have multiple divisors
        orig_loc = random.choice([6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 28])
        orig_num = 1
        orig_denom = 1

        # Remove cases that are too easy for the requested denominator
        possible_requested_denoms = [x for x in sm.divisors(orig_loc) if x not in [1, 2, orig_loc]]
        requested_denom = random.choice(possible_requested_denoms)

        # Keep requested location within reasonable bounds
        possible_requested_nums = sm.rel_primes(requested_denom, stop=math.ceil(30 * requested_denom / orig_loc))
        requested_num = random.choice(possible_requested_nums)

        requested_loc = orig_loc * requested_num // requested_denom

        return shape, orig_loc, orig_num, orig_denom, requested_loc, requested_num, requested_denom

    def gen_hard_line_prob():
        # Gives students a problem where the given is not 1
        # Still easy enough that the denominator of the requested fraction can be obtained by subdivision of orig denom

        shape = 'line'
        # Choose from tick locations that have lots of divisors
        orig_loc = random.choice([12, 16, 18, 20, 24, 28, 30])

        # Given numerator must divide tick location, but avoid original tick location itself
        orig_loc_divisors = sm.divisors(orig_loc)
        orig_loc_divisors.remove(orig_loc)
        orig_num = random.choice(orig_loc_divisors)

        # Choose denominator that doesn't force us to simplify the fraction, and that prevents whole numbers
        potential_orig_denoms = sm.rel_primes(orig_num, stop=20)
        potential_orig_denoms.remove(1)
        orig_denom = random.choice(potential_orig_denoms)

        # To be able to subdivide, we need to carefully choose our requested denominator to share a divisor
        # Kick out 1 in certain cases to prevent edge cases
        remaining_divisors = sm.divisors(orig_loc / orig_num)
        if orig_num == 1:
            remaining_divisors.remove(1)
        k = random.choice(remaining_divisors)
        requested_denom = k * orig_denom
        potential_requested_nums = list(range(1, math.ceil(30 * orig_num * k / orig_loc)))

        # Prevent requested fraction from equaling given fraction
        if orig_num * requested_denom % orig_denom == 0:
            if orig_num * requested_denom // orig_denom in potential_requested_nums:
                potential_requested_nums.remove(orig_num * requested_denom // orig_denom)
        requested_num = random.choice(potential_requested_nums)

        # Calculate tick mark of requested fraction
        requested_loc = orig_loc // (orig_num * k) * requested_num

        # Simplifying the fraction for beauty and creating fun cases where requested denom ends up less than given denom
        requested_num, requested_denom = Fraction(requested_num, requested_denom).as_integer_ratio()

        return shape, orig_loc, orig_num, orig_denom, requested_loc, requested_num, requested_denom

    def gen_easy_area_prob():
        shape = random.choice(list(shapes_dict.keys()))
        model_denom = int(random.choice(shapes_dict[shape]))
        model_num = int(random.choice(sm.rel_primes(model_denom, stop=5 * model_denom)))
        orig_denom = int(1)
        orig_num = int(1)
        requested_num, requested_denom = model_num, model_denom

        return shape, model_num, model_denom, orig_num, orig_denom, requested_num, requested_denom

    def gen_hard_area_prob():
        shape = random.choice(list(shapes_dict.keys()))
        model_denom = int(random.choice(shapes_dict[shape]))
        model_num = int(random.choice(sm.rel_primes(model_denom, stop=5 * model_denom)))
        orig_denom = int(random.randint(2, 9))
        orig_num = int(random.choice(sm.rel_primes(orig_denom)))
        requested_num, requested_denom = Fraction(orig_num * model_num, orig_denom * model_denom).as_integer_ratio()

        return shape, model_num, model_denom, orig_num, orig_denom, requested_num, requested_denom

    hard_problem_type = random.choice(['number line', 'area model'])

    if hard_problem_type == 'number line':
        p1_type, p1_orig_loc, p1_orig_num, p1_orig_denom, p1_requested_loc, p1_requested_num, p1_requested_denom = gen_easy_line_prob()
        p1_text = f'Given the number line below, mark the value '
        p1_math = f'\\dfrac{{{p1_requested_num}}}{{{p1_requested_denom}}}'
        p1_prob_text = f'Number line with 1 labeled {p1_orig_loc} spaces to the right of 0'
        p1_ans_text = (f'A number line that is the same as the one given above, but with a blue point for '
                       f'{p1_requested_num}/{p1_requested_denom} labeled {p1_requested_loc} '
                       f'spaces to the right of 0.')
        p1_model_num = None
        p1_model_denom = None

        p2_type, p2_model_num, p2_model_denom, p2_orig_num, p2_orig_denom, p2_requested_num, p2_requested_denom = gen_easy_area_prob()
        p2_text = f'If one {p2_type} represents 1, draw an area model for '
        p2_math = f'\\dfrac{{{p2_requested_num}}}{{{p2_requested_denom}}}'
        p2_prob_text = ''
        p2_ans_text = (f'A model of {p2_type}(s) each split equally into {p2_model_denom} parts. A total of '
                       f'{p2_model_num} are shaded to represent {p2_requested_num}/{p2_requested_denom}.')
        p2_orig_loc = None
        p2_requested_loc = None

        p3_type, p3_orig_loc, p3_orig_num, p3_orig_denom, p3_requested_loc, p3_requested_num, p3_requested_denom = gen_hard_line_prob()
        p3_text_1 = f'Given the number line below, mark the value '
        p3_math_1 = ''
        p3_text_2 = ''
        p3_math_2 = f'\\dfrac{{{p3_requested_num}}}{{{p3_requested_denom}}}'
        p3_prob_text = f'Number line with {p3_orig_num}/{p3_orig_denom} labeled {p3_orig_loc} spaces to the right of 0'
        p3_ans_text = (f'A number line that is the same as the one given above, but with a blue point for '
                       f'{p3_requested_num}/{p3_requested_denom} labeled {p3_requested_loc} '
                       f'spaces to the right of 0.')
        p3_model_num = None
        p3_model_denom = None
    else:
        p1_type, p1_model_num, p1_model_denom, p1_orig_num, p1_orig_denom, p1_requested_num, p1_requested_denom = gen_easy_area_prob()
        p1_text = f'If one {p1_type} represents 1, draw an area model for '
        p1_math = f'\\dfrac{{{p1_requested_num}}}{{{p1_requested_denom}}}'
        p1_prob_text = ''
        p1_ans_text = (f'A model of {p1_type}(s) each split equally into {p1_model_denom} parts. A total of '
                       f'{p1_model_num} are shaded to represent {p1_requested_num}/{p1_requested_denom}.')
        p1_orig_loc = None
        p1_requested_loc = None

        p2_type, p2_orig_loc, p2_orig_num, p2_orig_denom, p2_requested_loc, p2_requested_num, p2_requested_denom = gen_easy_line_prob()
        p2_text = f'Given the number line below, mark the value '
        p2_math = f'\\dfrac{{{p2_requested_num}}}{{{p2_requested_denom}}}'
        p2_prob_text = f'Number line with 1 labeled {p2_orig_loc} spaces to the right of 0'
        p2_ans_text = (f'A number line that is the same as the one given above, but with a blue point for '
                       f'{p2_requested_num}/{p2_requested_denom} labeled {p2_requested_loc} '
                       f'spaces to the right of 0.')
        p2_model_num = None
        p2_model_denom = None

        p3_type, p3_model_num, p3_model_denom, p3_orig_num, p3_orig_denom, p3_requested_num, p3_requested_denom = gen_hard_area_prob()
        p3_text_1 = f'If one {p3_type} represents '
        p3_math_1 = f'\\dfrac{{{p3_orig_num}}}{{{p3_orig_denom}}}'
        p3_text_2 = ', draw an area model for '
        p3_math_2 = f'\\dfrac{{{p3_requested_num}}}{{{p3_requested_denom}}}'
        p3_prob_text = ''
        p3_ans_text = (f'A model of {p3_type}(s) each split equally into {p3_model_denom} parts. A total of '
                       f'{p3_model_num} are shaded. This makes it appear to be an area model for '
                       f'{p3_model_num}/{p3_model_denom}, but given that one {p3_type} is {p3_orig_num}/{p3_orig_denom}'
                       f'to represent {p3_requested_num}/{p3_requested_denom}.')
        p3_orig_loc = None
        p3_requested_loc = None
    return {
        'p1_type': p1_type,
        'p1_orig_loc': p1_orig_loc,
        'p1_orig_num': p1_orig_num,
        'p1_orig_denom': p1_orig_denom,
        'p1_requested_loc': p1_requested_loc,
        'p1_requested_num': p1_requested_num,
        'p1_requested_denom': p1_requested_denom,
        'p1_model_num': p1_model_num,
        'p1_model_denom': p1_model_denom,
        'p1_text': p1_text,
        'p1_math': p1_math,
        'p1_prob_text': p1_prob_text,
        'p1_ans_text': p1_ans_text,

        'p2_type': p2_type,
        'p2_orig_loc': p2_orig_loc,
        'p2_orig_num': p2_orig_num,
        'p2_orig_denom': p2_orig_denom,
        'p2_requested_loc': p2_requested_loc,
        'p2_requested_num': p2_requested_num,
        'p2_requested_denom': p2_requested_denom,
        'p2_model_num': p2_model_num,
        'p2_model_denom': p2_model_denom,
        'p2_text': p2_text,
        'p2_math': p2_math,
        'p2_prob_text': p2_prob_text,
        'p2_ans_text': p2_ans_text,

        'p3_type': p3_type,
        'p3_orig_loc': p3_orig_loc,
        'p3_orig_num': p3_orig_num,
        'p3_orig_denom': p3_orig_denom,
        'p3_requested_loc': p3_requested_loc,
        'p3_requested_num': p3_requested_num,
        'p3_requested_denom': p3_requested_denom,
        'p3_model_num': p3_model_num,
        'p3_model_denom': p3_model_denom,
        'p3_text_1': p3_text_1,
        'p3_math_1': p3_math_1,
        'p3_text_2': p3_text_2,
        'p3_math_2': p3_math_2,
        'p3_prob_text': p3_prob_text,
        'p3_ans_text': p3_ans_text,
    }

print(generate())