# Imperivm Programming Language

Imperivm is a simple, stack-based programming language with a focus on clarity and structured programming. This document describes the language's features, syntax, and usage.

## Features

- **Stack Operations**: Push and pop values to/from the stack.
- **Control Flow**: Conditional branching (`if`, `elif`, `else`) and loops (`while`).
- **Arithmetic Operations**: Basic operations like addition, subtraction, multiplication, and division.
- **Variables**: Assign and use named variables.
- **Input/Output**: Print strings or variable values.
- **Modularity**: Define subroutines for reusable code.

## Syntax Overview

### Programs and Subroutines
An Imperivm program consists of one or more subroutines. Each subroutine has a name (identifier) followed by a `begin` block and an `end` block:

```imperivm
subroutine_name begin
  // Instructions go here
end
```

The main subroutine is named `main` and serves as the program's entry point. Its preset is mandatory.

### Blocks
Blocks are used to group instructions and control flow constructs:

```imperivm
begin
  // Instructions
end
```

### Instructions
Instructions include variable assignment, stack operations, arithmetic operations, and control flow constructs.

#### Variable Assignment
Assign a value to a variable:
```imperivm
assign 42 x
```

#### Stack Operations
Push a value onto the stack or pop a value into a variable:
```imperivm
push 10
pop x
```

#### Arithmetic Operations
Perform arithmetic and store the result in a variable:
```imperivm
add 5 x
subtract 3 y
```

#### Input/Output
Print a string value:
```imperivm
print "Salve, mundus!"
```

#### Control Flow
**Conditional Statements**:
```imperivm
if condition do
  // Instructions
end
elif other_condition do
  // Instructions
end
else do
  // Instructions
end
```

**Loops**:
```imperivm
while condition do
  // Instructions
end
```

**Stop**:
Terminate the current subroutine
```imperivm
foo begin
  pop x
  if x do
    stop
  end 
  else do
    // code
  end

```

## Running Imperivm Programs
To execute an Imperivm program, save it to a file with the `.imp` extension and run the interpreter:

```bash
./imperivm program.imp
```

## Contributing
Contributions, bug reports, and feature requests are welcome. Please submit issues and pull requests to the project repository.

## License
This project is licensed under the GPL v3 License.

