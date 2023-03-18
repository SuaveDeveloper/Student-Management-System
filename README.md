# Student-Management-System
How to use this API:

This API can be used by following this instructions:

Go to https://pythonanywhere.com to launch the PythonAnywhere web application.

Create a student or admin account:

After selecting "admin" from a drop-down menu of administrative routes, go to the "/admin/register" route to create an admin account.
After selecting "students" from a drop-down selection of student routes, go to the "/students/register" route to create a student account.
To generate a JWT token, log in using the '/auth/login' route. This access token should not be copied with quotation marks.

Click "Authorize" at the upper right after scrolling up. Enter the JWT token in the appropriate format, as in:

This bearer's a really long hex string.
After clicking "Authorize," click "Close."
You can now use the numerous options in "students," "courses," and "admin" to create, view, update, and delete admins, students, courses, grades, and more. Also available are:

all students in a course
Every course a student takes
grades in letters and percentages for each student (eg: A)
The CGPA of a student is determined by adding together all of their grades from all of their courses.
When completed, click "Authorize" once more in the top right corner to "Logout."
