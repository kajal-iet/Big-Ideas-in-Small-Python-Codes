# Overview

The Collatz sequence (or 3n + 1 problem) is a simple yet fascinating mathematical problem:
Start with any positive integer n.
If n is even, the next number is n / 2.
If n is odd, the next number is 3 * n + 1.
Repeat until n becomes 1.
It is believed (but not proven) that all starting numbers eventually reach 1.
This program generates the sequence from a user-provided starting number and can display it step by step.

How It Works

The program checks if n is even using n % 2 == 0.

If even, n is divided by 2.

If odd, n is multiplied by 3 and incremented by 1.

Steps repeat until n == 1.

# TODO List
[ ] Stats Panel

Total steps
Maximum value reached
Count of odd vs even numbers

[Done] Odd/Even Highlighting

A color-coded table:
✅ Green = even
✅ Red = odd

[Done] Charts

Line chart
Bar chart

[ ] Download Options

TXT
CSV

[Done] Comparison Mode

Enter:
5, 12, 27, 33, 87


⭐ Why This Project Is Useful

It makes an abstract mathematical idea easy to visualize and understand.

It turns a mysterious unsolved problem into an interactive exploration tool.

It helps beginners practice core programming concepts in a real context.

It allows users to observe how algorithms behave step-by-step instead of just reading about them.

It demonstrates how simple rules can generate complex patterns — a key idea in computer science.

It provides immediate feedback, helping learners experiment and discover patterns on their own.

It encourages curiosity and exploration by showing unexpected number behavior.

It gives a foundation for moving into more advanced topics like simulation, recursion, and mathematical modeling.