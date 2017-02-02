import grader
from grader.utils import quote_text_block
import os.path
import traceback
import argparse
import sys
from pprint import pprint

TESTER_MARKER = "tester.py"


def format_result_title(result, filename=None):
    status = 'OK' if result["success"] else 'VIGA'
    if filename:
        caption = filename.replace(".py", "") + ": " + result["description"]
    else:
        caption = result["description"]
    return '-{} ... {}'.format(caption, status)


def format_result(r, filename=None):
    title = format_result_title(r, filename)
    error_message = ""
    if not r["success"]:
        error_message += "\n" + r["error_message"].replace("AssertionError: ", "")
        if "AssertionError:" not in r["error_message"]:
            error_message += "\n\nTäielik veateade:" + quote_text_block(r["traceback"] or r["stderr"])
    return "{0}{1}".format(title, error_message)


def run_test_suite(tester_file, solution_file=None, asset_files=[], show_filename=False):
    if solution_file is None:
        if tester_file == "tester.py":
            solution_file = os.environ.get("VPL_SUBFILE0")
            assert solution_file, "$VPL_SUBFILE0 is not defined, env is " + str(os.environ)
        else:
            solution_file = tester_file.replace(TESTER_MARKER, "")

    points = 0
    max_points = 0
    file_missing = False

    if os.path.exists(solution_file):
        try:
            grader_result = grader.test_module(tester_file, solution_file, other_files=asset_files)
            print(grader_result)

            if not grader_result["results"]:
                print("Probleem testmimisel:", grader_result)

            for r in grader_result["results"]:
                # TODO: should it be r.get("grade", 1.0) ???
                max_points += grader_result.get("grade", 1.0)
                if r["success"]:
                    points += grader_result.get("grade", 1.0)

                print("<|--")
                print(format_result(r, solution_file if show_filename else None))
                print("--|>")
                # make it easier to distinguish separate tests
                print()
                print()

        except Exception as e:
            # TODO: what about max points here?
            print("<|--")
            print("-Viga faili {} testimisel".format(solution_file))
            traceback.print_exc()
            print("--|>")
    else:
        file_missing = True
        print("<|--")
        print("-Ei leidnud faili '" + solution_file + "'")
        print("--|>")

    return points, max_points, file_missing


def run_all_test_suites(solution_file, asset_files):
    points = 0
    max_points = 0
    missing_files = 0

    tester_files = sorted(list(filter(lambda fn: fn.endswith(TESTER_MARKER), os.listdir('.'))))

    for file in tester_files:
        p, mp, missing = run_test_suite(file, solution_file=solution_file, asset_files=asset_files, show_filename=len(tester_files) > 1)
        points += p
        max_points += mp

        # make it easier to distinguish separate test suites
        print(60 * "#")

        if missing:
            missing_files += 1

    return points, max_points, missing_files


def show_moodle_grade(points, max_points):
    print("Points:", points, ", max_points:", max_points)
    moodle_min_grade = float(os.environ.get("VPL_GRADEMIN", 0))
    moodle_max_grade = float(os.environ.get("VPL_GRADEMAX", 0))

    if moodle_min_grade == moodle_max_grade == 0:
        return

    if moodle_min_grade == 1 and moodle_max_grade == 2:
        # Arvestatud / mittearvestatud
        if points != max_points:
            print("Grade :=>> 1")  # Mittearvestatud
        else:
            print("Grade :=>> 2")  # Arvestatud

    elif max_points * moodle_max_grade > 0:
        moodle_grade = 1.0 * points / max_points * moodle_max_grade
        print("Grade :=>> {:3.1f}".format(moodle_grade))

def empty_file(filename):
    with open(filename, mode='w', encoding='utf-8') as f:
        f.write("")
    return filename

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--assets', nargs='*', default=[])
    parser.add_argument('--solution-file', nargs='?')
    parser.add_argument('--no-solution-file', action='store_true')
    args = parser.parse_args()

    solution_file = args.solution_file
    if args.no_solution_file:
        solution_file = empty_file('tmp-empty.py')
    points, max_points, missing_files = run_all_test_suites(solution_file, args.assets)
    if missing_files == 0:
        show_moodle_grade(points, max_points)
