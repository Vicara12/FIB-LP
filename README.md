# Funx

Funx is a programming language that can be used to evaluate functions
and expressions.

```
Sum a b {
    a + b
}

sum <- 0
i <- -10

while i < 100 and sum >= 0 {
    if i < 0 {
        i <- i+1
    }
    elseif i < 100 {
        sum <- (Sum sum i)
        i <- i+1
    }
    else {
        print "This should not happen";
    }
}

sum

print "That is the result of adding the first " i " numbers";
```

The code above shows several features of the language (which will be reviewed in detail in the following sections). First a function called `Sum` is declared, then the variables `sum` and `i` (as can be seen, the language is case sensitive) are declared, which are used in a while loop to add the numbers from 1 to 100. Finally the results are printed. As can be seen, any statement that returns a value outside a function (such as an arithmetic or boolean expression) is printed.

The result of running this sample code is

```
Out: 4950
That is the result of adding the first 100 numbers
```

## Building and executing

To build the language just execute the command *make* inside the main project folder. This will generate the visitors, check proper code format and execute all the unit tests.

To run funx code from the terminal, execute the funx.py script with the file containing the code as the first argument.

To build the web application, execute the command *make server* in the root path of the project. This will automatically run the application script (app.py) and start the server.

## Language features

In the following sections all the different features of the language will be detailed.

### Code sections

The code is divided in two different sections: the *main code* and the *function code*. The main code is the one that is not inside a function, in contrast to the function code.

Function and main code behave differently in two ways. The first one is that functions can only be declared in main code, that is, it is not possible to declare a function inside a function. The second one is that, whenever a statement returns a value in the main code the result is printed and the code continues execution, whereas in the function code the result is not printed and is the returned value of the function.

This is an addition to the project statement, where the program would stop when encountering a value in the main code. However, this does not break the compatibility with the statement, as any code that can be executed by the original language can be also executed in this language.

### Comments

A comment is a section of code that is ignored by the interpreter. Any line that follows the character # is a comment.

### Expressions

Expressions, together with function calls, are the only types that return a value. They can be of two different types: arithmetic and boolean.

Expressions can be used to print values in the main code, return values in functions, as parameters in function calls, in print statements and in loops and conditionals. The code sample below shows some uses:

```
# this expression shows the value 4
(2+2)

# these two assign the result of the expression to the variable
var1 <- 4^2
var2 <- not (True and False)

# this expression returns the value 42 when the function is called
Answer parameter {
    42
}

# this line prints "2+3 = 5"
print "2+3 = " (2+3);

# here is an example of an expression in a loop and conditional
i <- 0

while i < 10 {
    if i > 5 {
        print "the value of i is " i;
    }
}
```

Finally, it is important to keep in mind that line breaks do not separate expressions. For example, this code

```
2+2
-1+6
```
Returns 9, not 4 and 5. In order to keep expressions separated use parentheses.

#### Arithmetic expressions

Arithmetic expressions are a type of expression that returns an integer number. The operators ordered by decreasing precedence are:

1. Parentheses: ()
2. Exponentiation by naturals: ^
3. Multiplication, integer division and modulus: * / %
4. Addition and difference: + -
5. Negation: -

It is important to emphasize that the division always returns an integer value (for example 3/2 = 1), and that division by zero causes an exception to be raised. Also, exponentiation by negative numbers is also undefined and will cause an exception.

#### Boolean expressions

Boolean expressions are a type of expression that can only return True or False. The operators ordered by decreasing precedence are:

1. Parentheses: ()
2. Negation: not
3. Logical AND: and
4. Logical OR: or
5. Less than, le than, greater than, ge than, equals and different: < <= > >= = !=

An arithmetic expression can be converted to a boolean expression where zero equals False and any other value equals True.

### Assignations and variables

Values returned by an expression or by a function call can be stored into a variable. The syntax is:

```
varname <- value
```

Where the first letter of the variable name must be lowercase and contain only alphanumerical symbols (both upper and lowercase). If a variable that does not exist gets called, this will result in an exception.

Variables are only visible within their context, which means that main variables can only be accessed in the main section of the code and something similar happens for variables inside functions.

### Conditionals

Conditionals must contain an *if* statement and optionally several *elseif* and a final *else*. The syntax is as follows:

```
if boolean_expression {
    code block
} else if boolean_expression {
    code block
} else {
    code block
}
```

For example:

```
if var = 0 {
    print "variable is zero";
} elseif var < 10 {
    print "variable is lower than ten";
} else {
    print "variable is greater than 10";
}
```

### While loop

The loop's syntax is as follows:

```
while boolean_expression {
    code block
}
```

For example:

```
while i < 10 {
    i
    i <- 10
}
```

### Print

The *print* statement allows the user to output text and everything that returns a value to the terminal. Print statements can be multiline and must be followed by the ; character.

Those are several examples on the use of *print*:

```
print "Hello world!";

print "This will be
displayed in two lines";

print "The result of 4+2 is " 4+2;

# this is a function, it will be discussed later
Dos dummy_value {2}

print "Calling the function Dos " (Dos 3);

x <- 5
print "The value " x " is held by the variable x";
```

### Functions

Functions are declared as follows:

```
FuncName param1 param2 param3 {
    code block
}
```

The name of the function must begin with an uppercase letter and can contain alphanumerical characters (both uppercase and lowercase).

The value returned by the function is the one given by the first statement executed that returns something. Here are several examples

```
Fact1 n {
    if n < 1 {
        1 # this statement returns the value 1
    }
    n*(Fact n-1) # this statement returns the value n*(n-1)!
    # code execution never reaches this point
}

Fact2 n {
    # this is not the return statement because
    # it does not return anything
    result <- 1

    if n > 1 {
        result <- n*(Fact2 n-1) # this is also not the return statement
    }

    # this statement returns the value of *result*, so the function
    # returns there
    result

    1/0 # this code is never executed
}
```

Functions can be overloaded, that is, there can be several functions with the same name. However, they must differ in the number of parameters. If two functions are declared with the same name and number of arguments, this will raise an exception. Also, all the names of the function parameters must be different, an exception is raised otherwise.

Function overload can be problematic in some situations. For an example, consider the following code:

```
Func {
    42
}

Func a {
    127
}

Func
Func
```

One would expect this code to output the value 42 twice, but in reality it shows the number 127 once. This is because it interprets the second call to *Func* as the parameter for the first call. One option to avoid this would be to use parentheses on function calls, but an alternative is to use the optional character ';' to indicate the end of a function call.

As stated before, functions can be only declared at the main section code and not inside functions, conditionals or loops. They can also be declared in any order, and a function can be declared after being called.

Obviously, if a function is called with a name and number of arguments that does not coincide with any previously declared, this will raise an exception.

### List of all the extra features added to the language

Below is a list of all the features added to the program and that were not present in the original project statement.

1. Main code can handle more than one expression
2. Parentheses.
3. Exponentiation.
4. Boolean operands *not*, *and*, *or* and !=.
5. Numerical value to boolean conversion.
6. *elseif* and *else* blocks in conditionals.
7. The *print* statement.
8. The function call separator ;
9. Function overload.
10. Function declaration after function call.

## Test units

As programming a language is a very coupled task, because implementing a new feature can cause bugs on other parts of the language, a system of unit tests has been developed.

Tests must be inside the *tests* folder and end with the .funx extension. A test is a file that contains funx code, and where the expected output is written inside the file preceded by ##.

To execute the unit tests, just execute tests.sh script. This script is also automatically executed whenever the project is recompiled with *make*. This script will execute all the test files and compare the results with the expected ones. If any of them differs, a warning will pop out in the terminal and the actual and expected results are shown.

## The web interpreter

Finally, a web interpreter for the language is also available.

The interpreter is divided in four sections. In the upper left corner there is a text area where new code can be inserted and executed. The results will be shown in the scrollable section at its right, where the most recent ones are shown above. The other two sections, located below the new code area are the declared functions and global variables section. These two sections are also scrollable and show most recently declared functions first.