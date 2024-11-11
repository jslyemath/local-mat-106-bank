import slye_math as sm
import random
from fractions import Fraction
import inflect
from datetime import datetime


def generate(**kwargs):
    def flag_dimensions():
        locations_with_adjectives = [
            ('Hyrule', 'Hylian'),
            ('Labrynna', 'Labrynnian'),
            ('Holodrum', 'Holodrumian'),
            ('Ylisse', 'Ylissean'),
            ('Altea', 'Altean'),
            ('Isle Delfino', 'Delfinian'),
            ('Tortimer Island', 'Tortimerian'),
            ('Gallia', 'Gallian'),
            ('Daein', 'Daein'),
            ('Neo Arcadia', 'Neo Arcadian'),
            ('Archanea', 'Archanean'),
            ('Magvel', 'Magvelian'),
            ('Aionios', 'Aionian'),
            ('Tethe\'alla', 'Tethe\'allan'),
            ('Sylvarant', 'Sylvaranti'),
            ('Dream Land', 'Dreamlandian'),
            ('Popstar', 'Popstarian'),
            ('Aeos Island', 'Aeosian'),
            ('New Donk City', 'New Donk City'),
            ('Inkopolis', 'Inkopolissean'),
            ('Splatsville', 'Splatlandian'),
            ('Gusty Gulch', 'Gusty Gulchian'),
            ('Zora\'s Domain', 'Zoran'),
            ('Lorule', 'Lorulian'),
            ('Termina', 'Terminian'),
            ('Valla', 'Vallite'),
            ('Norfair', 'Norfairian'),
            ('Kanto', 'Kantonian'),
            ('Johto', 'Johtonian'),
            ('Hoenn', 'Hoennian'),
            ('Sinnoh', 'Sinnohan'),
            ('Unova', 'Unovan'),
            ('Kalos', 'Kalosian'),
            ('Alola', 'Alolan'),
            ('Galar', 'Galarian'),
            ('Paldea', 'Paldean')
        ]
        
        location, proper_adjective = random.choice(locations_with_adjectives)

        ratio_width = random.randint(5, 20)
        possible_ratio_lengths = sm.rel_primes(ratio_width, start=ratio_width, stop=ratio_width*3)
        ratio_length = random.choice(possible_ratio_lengths)

        swap_length_width = random.choice([True, False])

        if swap_length_width:
            ratio_length, ratio_width = ratio_width, ratio_length

        ratio_part_and_value = [('length', ratio_length), ('width', ratio_width)]
        random.shuffle(ratio_part_and_value)

        fractional_part_denom = random.randint(1,5)

        if fractional_part_denom == 1:
            fractional_part_num = 0
        else:
            fractional_part_num = random.choice(sm.rel_primes(fractional_part_denom))

        start_dim_whole = random.randint(5, 25)
        start_dim_frac = Fraction(fractional_part_num, fractional_part_denom)
        starting_dimension = start_dim_whole + start_dim_frac

        dimension_to_find, given_dimension = random.choices(['length', 'width'], k=2)

        to_find_num, to_find_denom = 'x', sm.mixed_number(starting_dimension, format='latex')

        answer = starting_dimension * ratio_part_and_value[0][1] / ratio_part_and_value[1][1]

        if given_dimension == ratio_part_and_value[0][0]:
            to_find_num, to_find_denom = to_find_denom, to_find_num
            answer = starting_dimension * ratio_part_and_value[1][1] / ratio_part_and_value[0][1]

        problem = (
            f"For every flag of {location}, the ratio of its {ratio_part_and_value[0][0]} to its "
            f"{ratio_part_and_value[1][0]} must be ${ratio_part_and_value[0][1]}:{ratio_part_and_value[1][1]}$. "
            f"If a {proper_adjective} flag is to be produced with a \\textbf{{{given_dimension}}} of "
            f"${sm.mixed_number(starting_dimension, format='latex')}$ ft, what should its "
            f"\\textbf{{{dimension_to_find}}} be? "
            f"Give your final answer as a mixed number, if necessary. Don't forget to write the correct "
            f"units in your final answer."
        )

        solution = (
            f"If we place the given ratio in a proportion with our known length and width (being careful to "
            f"attend to matching the order of the numerators and denominators), we get "
            f"\\[ \\dfrac{{{ratio_part_and_value[0][1]}}}{{{ratio_part_and_value[1][1]}}} = "
            f"\\dfrac{{{to_find_num}}}{{{to_find_denom}}}, \\] "
            f"where $x$ is the unknown {dimension_to_find}. Solving this proportion, we get "
            f"\\[ x = {sm.mixed_number(answer, format='latex')}\\]"
        )
        return problem, solution

    available_versions = [flag_dimensions]

    prob_sol_function = random.choice(available_versions)

    problem, solution = prob_sol_function()
    return {
        'problem': problem,
        'solution': solution,
    }

print(generate())