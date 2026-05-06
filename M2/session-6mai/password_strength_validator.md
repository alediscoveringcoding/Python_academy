The Password Strength Validator Challenge
You are building a password security checker for a new app.

Your job is to help the platform evaluate passwords, detect weak patterns, and give useful feedback to users before they create an account.

This challenge is all about practicing string manipulation in a real-world style problem.
Why this challenge matters
Modern developers do not just build features.

They also protect users.

A password field may look simple, but behind it there is a lot of careful thinking:

checking text rules
validating user input
detecting risky patterns
giving clear feedback
designing logic that can evolve over time

In this lab, students will practice:

analyzing strings
validating text against rules
searching for patterns
combining multiple checks into one system
thinking like developers who care about security and usability
The Story
A startup launches a new platform.

Before users can create an account, their password must be checked.

Some users choose weak passwords that are easy to guess. Some use their own name. Some use obvious patterns like:

all lowercase letters
only numbers
repeated characters
simple sequences
very common passwords

Your task is to create a password validation system that can inspect passwords and provide meaningful feedback.
Main Goals
Students should build functions that can:

clean and normalize password-related input when needed
check password length
detect uppercase, lowercase, digits, and special characters
detect weak patterns
identify common passwords
validate whether a password is strong enough
generate structured feedback for the user
Required Functions
1. check_length(password)
Check whether the password meets the minimum length rule.

Expected behavior:

verify that the password is not too short
optionally warn if it is extremely long or suspiciously simple despite length
return useful feedback, not only a yes/no answer
2. check_character_types(password)
Inspect the character variety inside the password.

Expected behavior:

detect whether the password contains lowercase letters
detect whether it contains uppercase letters
detect whether it contains digits
detect whether it contains special characters
summarize what is missing
3. contains_common_password(password)
Check whether the password is too common.

Expected behavior:

compare against a list of known weak passwords
ideally perform the check in a case-insensitive way
treat very common choices as high risk
4. contains_personal_info(password, username)
Check whether the password includes obvious personal information.

Expected behavior:

detect whether the password contains the username or parts of it
optionally handle simple variations like lowercase matching
flag passwords that are too predictable because of personal data
5. has_repeated_or_sequential_patterns(password)
Detect patterns that make the password weak.

Possible examples:

repeated characters
repeated chunks
sequences like consecutive numbers or letters
keyboard-style easy patterns

Expected behavior:

identify simple, guessable structure
return clear feedback about why the pattern is weak
6. calculate_strength(password, username=None)
Estimate the overall strength of the password.

Expected behavior:

combine the results of previous checks
classify the password using levels such as weak, medium, strong
explain the decision instead of returning only a label
7. validate_password(password, username=None)
Build the final validator.

This function should:

apply all important checks
collect errors and warnings
produce a final decision
return structured data that another part of the app could use
Analytical Thinking Markers
Before writing each function, students should stop and ask:

What exactly is the input?
What should the output look like?
What makes a password weak in the real world?
Should the check be case-sensitive or case-insensitive?
What patterns are obvious to attackers but easy to miss as programmers?
What counts as a strict failure, and what counts as a warning?
Can I split this into helper functions?
If the password rules change later, will my code be easy to update?
Engineering Mindset Prompts
Use these as checkpoints during the lab.
Security Thinking
What kinds of passwords do users usually choose when they are lazy?
What kinds of passwords are easy for attackers to guess?
Is length alone enough to make a password strong?
Can a password look complex but still be weak?
Validation Thinking
Which rules are mandatory?
Which rules improve quality but should not necessarily block the user?
How can I return feedback that is both useful and structured?
Pattern Detection
What repeated patterns should count as risky?
How do I detect simple sequences?
Should I look at the password as a whole or character by character?
Maintainability
Am I repeating the same logic in multiple places?
Could one helper function make the validator cleaner?
If I add a new rule tomorrow, where should it fit?
Suggested Test Passwords
Use these ideas for testing:

a very short password
a password with only lowercase letters
a password with only digits
a password with lowercase and uppercase letters but no numbers
a password with letters and numbers but no special characters
a password containing the username
a password with repeated characters
a password with a simple sequence
a common password
a strong password with a good mix of character types and no obvious patterns
Output Idea
Students can return dictionaries that include:

whether the password is valid
what errors were found
what warnings were found
what requirements were met
what requirements were missing
the final strength level
the reasons behind that strength score
Optional Extensions
For stronger students, add one or more of these:

calculate a numeric score from 0 to 100
suggest how to improve a weak password
generate stronger password recommendations
detect keyboard patterns
compare multiple passwords and rank them by strength
assign risk labels such as safe, warning, and blocked
Teaching Goal
This is not only a string exercise.

It is a security thinking exercise.

Students should learn to ask:

What makes data trustworthy?
What makes validation useful?
How do I design checks that are strict but fair?
How do I turn security rules into readable code?
How do I avoid solving only the happy path?
Final Challenge Prompt
Build a password strength validator that can inspect passwords, detect weak patterns, and provide clear feedback before an account is created.

Your solution should be broken into small functions, tested with multiple examples, and written clearly enough that another developer can extend it later.

Think like a real engineer: not just about making it work, but about making it robust, secure, and maintainable.


Recommendation
To make the two options feel truly parallel, I’d name them like this:

Option 1: The Social Media Sanitizer Challenge
Option 2: The Password Strength Validator Challenge

That creates a very clean “pick one” experience.
Nice teaching move
You can also add a short intro above both:
Pick Your Challenge
Choose one of the following labs:

build a system that cleans and validates social media posts
build a system that checks password strength and detects weak patterns

In both labs, your goal is the same: write clean Python, think analytically, and design small reusable functions.
Completion status
Task completed
I crafted the markdown-only password validator lab brief
It is structured to closely match the social media sanitizer version

If you want, next I can also:

turn this into a shorter Google Docs version
make both briefs same exact section order and wording style
create a third option so students can choose from 3 labs

