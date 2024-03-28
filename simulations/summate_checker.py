from pedal import *

match = find_match("""
def summate():
    __expr__
""")

if not match:
    explain("You have not defined the function", label="missing_function")
elif match['__expr__'].find_match("summate()"):
    explain("You are doing recursion, don't do that", label="used_recursion")

assert_equal(call('summate', [1,3,5]), 9)