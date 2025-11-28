CPSC 110 Lab 6 Due: Fri Oct. 18, 2024, 9:00am

General Lab Instructions:
1. All assignments will be submitted through Canvas. If you submit multiple times, the most recent submission will be graded.

2. You will typically explain your code from the last lab to the instructor at the beginning of the next lab to receive your full marks and feedback.

3. If you work with other people, list all of your names on the assignment. Each assignment will specify how many others you can work with.

4. Please review the collage’s plagiarism policies. As a general rule, copy/paste should never be used for any code. Ever. You may discuss topics with other students and reference online materials, but the final assignment must be written by the student. If you reference materials/people besides the textbook/instructor then cite this in a file contributions.txt. Full citations are not necessary, a bullet point list of the materials/people that you references is suitable.

5. Code will be graded for functionality as well as quality. This means code that should be easy to read with descriptive variable names and appropriate comments.

6. You should aim to stick to the concepts we have already covered in class. For example, do not use ”if statements” on assignment 1 since it was not covered in lecture 1. If you have studied programming elsewhere then it is tempting to jump ahead, but full marks will only be given to assignments that are focused on this course’s content.

7. Code that cannot run successively in Python 3 will receive a zero. Make sure you are using the correct python version and allow yourself enough time for thorough testing.

8. At the start of each assignment will be a list of the required files for submission. All files should be com- pressed in one zip folder named <studentnumber>_<yourname >_LAB < number >_CPSC110.zip. For example: 21870110_LUKESKYWALKER_LAB01_CPSC110.zip

Required files:

- character.py
- food.py
- game.py
- install.py
- keys.py
- opponent.py
- player.py
- README.md
- run.py
- sprite.py
- tests.py

# Lab 06: How to Design Programs
In this lab, we're looking at our interactive game program that we designed last class and **refactoring** it. This is a common way to design programs and is a big part of programming. 

See the [Refactoring Guru](https://refactoring.guru) for an in-depth discussion of how and when to refactor. 

Today we will be applying the lessons from our discussion of **type-of**, **part-of**, and **collection-of** relationships (or inheritance, composition, and aggregation respectively).

Start by downloading the code at [https://github.com/CC-CPSC-110/lab06](https://github.com/CC-CPSC-110/lab06).

# Problem 1: Refactor to make `Sprite`
If you remember from last class, we had `Food` and `Player`. You'll notice that both have `x`, `y`, and `size` properties. Create a new class called `Sprite` that has those properties, then ensure that `Food` and `Player` extend `Sprite` by using a **type-of** relationship. 

Write any appropriate tests in `tests.py`. Run your game to ensure that nothing has really changed.

# Problem 2: Create an `Opponent` Class
We now want to create an `Opponent` that tries to eat the `Food` before the `Player` does. 

We can go about this in two ways. One would be to simply copy everything from `Player`. The other would be to create a **type-of** relationship with another class, and let both `Player` and `Opponent` extend that class.

For now, analyze what is similar about the needs of a computer-controlled `Opponent` and a human-controlled `Player`. Make notes in the `Opponent` class for yourself about what can stay the same, and what needs to change.

Write any tests you need in `tests.py`. Run your game.

# Problem 3: Create a `Character` Class
We now want to create an `Character` class that will make `Player` and `Opponent` have the same functionality.

Based off of your notes from `Opponent` (and any hints that I've left in the code), create the `Character` class which extends `Sprite` and has both `Player` and `Opponent` inherit from it. 

Remember that the goal is minimum duplicate code. Anything duplicated should be in the parent `Character` class. Anything different should be in the child classes.

Write any tests you need in `tests.py`. Run your game.

# Problem 4: Instantiate, move and draw your `Opponent`
Make sure that the opponent exists and can move. I've given some example code for `Opponent` and `Sprite`. You may have to modify bits and pieces. 

Use the full HtDF process to fill out and debug the rest of the move process. Write purpose statements, examples, and tests.

# Problem 5: Refactor `draw`
Now that everything has inheritance, we should be able to make `draw` much shorter. Design a way to use **type-of**, **part-of**, and **collection-of** together so that you can make draw as short as possible.
