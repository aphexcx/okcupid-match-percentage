__author__ = 'Afik Cohen'

import math
import sys
import json

IMPORTANCE = [0, 1, 10, 50, 250]


def satisfaction(profile, other_profile):
    """Return the percentage (float) of how satisfied profile is with other_profile.
    """
    # make a quick dict keyed by questionId to make navigating answers faster and easier
    my_answers = {answer['questionId']: answer for answer in profile['answers']}
    otherp_answers = {answer['questionId']: answer for answer in other_profile['answers']}

    # how much did other_profile's answers make us happy?
    correct_points = 0
    possible_points = 0
    for answer in otherp_answers:
        if answer in my_answers:
            # we both answered this question.
            # calculate this answer's value, which is the importance value profile placed on it
            answer_value = IMPORTANCE[my_answers[answer]['importance']]
            # first, add this question's importance value to the sum of possible attainable points
            possible_points += answer_value
            # other_profile gets correct points if their answer is in my acceptableAnswers
            if otherp_answers[answer]['answer'] in my_answers[answer]['acceptableAnswers']:
                correct_points += answer_value

    # force float division
    return float(correct_points) / float(possible_points)


def main():
    output = {'results': []}

    # read in input json
    with open('input.json', 'r') as f:
        inputjson = json.load(f)

    profiles = inputjson['profiles']
    for profile in profiles:
        # build json output for this profile
        profile_output = {'profileId': profile['id'],
                          'matches': []}
        # calculate match percentage against all other profiles
        matches = []
        for other_profile in profiles:
            if other_profile['id'] == profile['id']:
                # dont calculate against our own profile
                continue
            # calculate match percentage with OKC's formula:
            # "a mathematical expression of how happy you'd be with eachother"
            match_score = math.sqrt(satisfaction(profile, other_profile) * satisfaction(other_profile, profile))

            # build json output for this match
            match_output = {'profileId': other_profile['id'],
                            'score': match_score}
            matches.append(match_output)

        #filter out the top 10 matches
        top10matches = sorted(matches, key=lambda match: match['score'], reverse=True)[:10]
        profile_output['matches'] = top10matches

        output['results'].append(profile_output)

    # write out the output json
    with open('output.json', 'w') as outf:
        json.dump(output, outf, indent=1)

    return 0


if __name__ == '__main__':
    sys.exit(main())