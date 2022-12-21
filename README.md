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

## Language features

### Expressions

#### Arithmetic expressions

div0 powNeg

#### Boolean expressions

expressions are also booleans

### Assignations and variables

Visibility, errors and names
name conventions

### Conditionals

### While loop

### Print
print can be multiline
;

### Functions

name convention
overload
declared in any order
declared only at main

## Test units

## The interpreter


DOCUMENTAR EXTENSIÓN DE VARIAS EXPRESIONES Y ;
