# Imperivm Programming Language

Imperivm is a simple, stack-based programming language with a focus on clarity and structured programming. This document
describes the language's features, syntax, and usage.

## Features

- **Memory Operations**: Memory management is handled using a stack (`push`, `pop`) and a heap (`store`, `load`)
- **Control Flow**: Conditional branching (`if`, `elif`, `else`) and loops (`while`).
- **Arithmetic Operations**: Basic operations like addition, subtraction, multiplication, and division.
- **Logic Operations**: Basic logic operations (`and`, `or`, `xor`,`not`, `negate`)
- **Variables**: Assign and use named variables (`let`).
- **Input/Output**: Print strings or variable values.
- **Modularity**: Define subroutines for reusable code.
- **Comments**: Supports comments anywhere in the code using `#`

## Syntax Overview

### Programs and Subroutines

An Imperivm program consists of one or more subroutines. Each subroutine has a name (identifier) followed by a `begin`
block and an `end` block:

```imperivm
subroutine_name begin
  # Instructions go here
end
```

The main subroutine is named `main` and serves as the program's entry point. Its preset is mandatory.

### Blocks

Blocks are used to group instructions and control flow constructs:

```imperivm
begin
  # Instructions
end
```

### Instructions

Instructions include variable assignment, stack operations, arithmetic operations, and control flow constructs.

#### Variable Assignment

Assign a value to a variable:

```imperivm
push 42
let x
```


#### Memory Operations

**Stack**
The stack is used for basic, temporary storage. It follows a last-in, first-out (LIFO) structure.
Values can be pushed onto the stack and popped off as needed.
This is typical for storing intermediate results and controlling the flow of execution.

```imperivm
push 10   # Pushes 10 onto the stack
pop x     # Pops the top value off the stack and assigns it to variable x
```

**Heap**
The heap is a dynamically allocated memory space where values can be stored at specific memory addresses.
The `store` operation saves values from the stack into specified addresses, while the `load` operation retrieves them.
This allows for more complex, persistent memory storage, where values are not lost after execution steps, unlike in the
stack.

```
push 5     # Pushes the value to be stored
push 0     # Pushes the memory address
store      # Stores the value 5 at address 0 in the heap

push 0     # Pushes the memory address
load       # Loads the value from address 0 in the heap back onto the stack
```

In summary, Imperivm uses the stack for temporary, local storage and the heap for dynamic, addressable memory storage.

#### Arithmetic Operations

Perform arithmetic and store the result in a variable:

```imperivm
add 5 x
subtract 3 y
```

#### Boolean Operations

```
# Performs a bitwise AND between the value in the stack and the value of the target variable.
and target
```

```
# Performs a bitwise OR between the value in the stack and the value of the target variable.
or target
```

```
# Performs a bitwise XOR between the value in the stack and the value of the target variable.
xor target
```

```
#  Applies a bitwise NOT to the value of the target variable.
negate target
```

```
# Converts the value of the target variable to either 0 (false) or the original value (true).
not target
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
  # Instructions
end
elif other_condition do
  # Instructions
end
else do
  # Instructions
end
```

**Loops**:

```imperivm
while condition do
  # Instructions
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
    # code
  end

```

**Exit**
Terminates the program by returning the specified code. Variables can be used

```imperivm
exit x   # Terminates the program and returns x value.
```

## Running Imperivm Programs

To execute an Imperivm program, save it to a file with the `.imp` extension and run the interpreter:

```bash
./imperivm program.imp
```

## Contributing

Contributions, bug reports, and feature requests are welcome. Please submit issues and pull requests to the project
repository.

## License

This project is licensed under the GPL v3 License.

