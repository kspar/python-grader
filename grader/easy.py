import argparse
import os.path
import traceback

import grader

TESTER_MARKER = "tester.py"


def format_result_title(result, filename=None):
    status = 'OK' if result["success"] else 'VIGA'
    if filename:
        caption = filename.replace(".py", "") + ": " + result["description"]
    else:
        caption = result["description"]
    title = '===== TEST: {} =====\n>>> {}\n'.format(caption, status)
    return title


def format_result(r, filename=None):
    title = format_result_title(r, filename)
    error_message = ""
    if not r["success"]:
        error_message += "\n" + r["error_message"].replace("AssertionError: ", "")
        if "AssertionError:" not in r["error_message"]:
            error_message += "\n\nTäielik veateade:\n" + r["traceback"] or r["stderr"]
            error_message += '\n\n'
    return "{0}{1}".format(title, error_message)


def run_test_suite(tester_file, solution_file=None, asset_files=[], show_filename=False):
    if solution_file is None:
        if tester_file == "tester.py":
            solution_file = "submission"
        else:
            solution_file = tester_file.replace(TESTER_MARKER, "")

    points = 0
    max_points = 0
    file_missing = False

    if os.path.exists(solution_file):
        try:
            grader_result = grader.test_module(tester_file, solution_file, other_files=asset_files)

            if not grader_result["results"]:
                print("Probleem testmimisel:", grader_result)

            for r in grader_result["results"]:
                max_points += grader_result.get("grade", 1.0)
                if r["success"]:
                    points += grader_result.get("grade", 1.0)

                print(format_result(r, solution_file if show_filename else None))

        except Exception as e:
            print("Viga esitatud faili testimisel")
            traceback.print_exc()
    else:
        file_missing = True
        print("Ei leidnud faili '" + solution_file + "'")

    return points, max_points, file_missing


def run_all_test_suites(solution_file, asset_files):
    points = 0
    max_points = 0
    missing_files = 0

    tester_files = sorted(list(filter(lambda fn: fn.endswith(TESTER_MARKER), os.listdir('.'))))

    for file in tester_files:
        p, mp, missing = run_test_suite(file, solution_file=solution_file, asset_files=asset_files,
                                        show_filename=len(tester_files) > 1)
        points += p
        max_points += mp

        if missing:
            missing_files += 1

    return points, max_points, missing_files


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

    solution_filename = args.solution_file
    if args.no_solution_file:
        solution_filename = empty_file('tmp-empty.py')
    points, max_points, missing_files = run_all_test_suites(solution_filename, args.assets)
    grade = points / max_points * 100 if max_points > 0 else 0

    print("#" * 50)
    print('Points: ' + str(points))
    print('Max points: ' + str(max_points))
    print('Grade: ' + str(round(grade)))
