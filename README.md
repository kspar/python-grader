Python Grader
=============

---------------
This project is a fork of Karl-Aksel Puulmann's Bachelor's thesis. The following two links serve as a better introduction to the original project than this readme does.

* [Link to poster introducing project](http://macobo.github.io/python-grader/poster.pdf)
* [Link to thesis](http://macobo.github.io/python-grader/thesis.pdf)

-------

This is a module for automatically testing homework solutions that has been used for giving feedback for homeworks and midterms for various first-year programming courses at University of Tartu.

What this project does differently from conventional unit-testing frameworks is allow testing of interactive, input-output based programs as well as more conventional function/class based programs, meanwhile retaining a simple and powerful interface for doing that.

For the student, feedback provided by the module should be helpful for debugging and understanding where they went wrong.

For the teacher, the advantage over using normal unit tests is that it allows to move from purely-manual based input-output testing to a more structured and consistent framework that saves time.

## Setup

**Prerequsite**: Install python3.3 (or python3.4), preferably use a virtualenv.

For full setup guide which involves building python from source and setting up a virtualenv, 
see [INSTALL.md](INSTALL.md)

```bash
git clone https://github.com/kspar/python-grader.git
cd python-grader
sudo python3 setup.py install
```

To run tests for this module, run `python3 run_tests.py`.


### Running test on a file
To tester on a solution, run `python -m grader <tester_file> <solution_file>`.

For example, to run the above tester (in the tasks folder) on the sample solution:
```bash
cd tasks/
python -m grader Examples/interactive_search_tester.py Examples/interactive_search_solution.py
```
