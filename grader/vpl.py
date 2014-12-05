import grader
from grader.utils import quote_text_block
import os.path
import traceback
import sys
from pprint import pprint

TESTER_MARKER = "_tester"

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
            error_message += "\n\nTäielik veateade:" + quote_text_block(r["traceback"])
    return "{0}{1}".format(title, error_message)
    

def run_test_suite(tester_file, solution_file=None, show_filename=False):
    if solution_file == None:
        if tester_file == "tester.py":
            solution_file = os.environ.get("VPL_SUBFILE0")
            assert solution_file, "$VPL_SUBFILE0 is not defined"
        else:
            solution_file = tester_file.replace(TESTER_MARKER, "")

    points = 0
    max_points = 0
    
    if os.path.exists(solution_file):
        try:
            grader_result = grader.test_module(tester_file, solution_file)
            #pprint(grader_result)
            if not grader_result["results"]:
                print("Probleem testmimisel:", grader_result)
        
            for r in grader_result["results"]:
                print("<|--")
                print(format_result(r, solution_file if show_filename else None))
                max_points += grader_result.get("grade", 1.0)
                if grader_result["success"]:
                    points += grader_result.get("grade", 1.0)
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
        print("<|--")
        print("-Ei leidnud faili '" + solution_file + "'")
        print("--|>")
        
    
    return points, max_points
    

def run_all_test_suites():
    points = 0
    max_points = 0

    files = sorted([f for f in os.listdir(".") if f.endswith(TESTER_MARKER + ".py") or f == "tester.py"])
    for file in files:
        p, mp = run_test_suite(file, show_filename=len(files) > 1)
        points += p
        max_points += mp

        # make it easier to distinguish separate test suites
        print(60 * "#")
    
    return points, max_points


def show_moodle_grade(points, max_points):
    moodle_max_grade = float(os.environ.get("VPL_GRADEMAX", 0))
    
    if max_points * moodle_max_grade > 0:
        moodle_grade = 1.0 * points / max_points * moodle_max_grade
        print("Grade :=>> {:3.1f}".format(moodle_grade))


if __name__ == '__main__':
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        points, max_points = run_test_suite(*sys.argv[1:])
        # TODO: introduce cmd-line parameter for suppressing grade
        #show_moodle_grade(points, max_points)
    else:
        points, max_points = run_all_test_suites()
        # TODO: Can't detect max_points when some testers are not run
        # because user hasn't submitted the solution file
                    

