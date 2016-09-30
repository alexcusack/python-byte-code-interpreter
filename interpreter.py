def LOAD_FAST(frame, bytes):
  frame['stack'].append(frame['args'][bytes[0]])
  return 2

def BINARY_ADD(frame, bytes):
  # pop of frame.stack
  popped = frame['stack'].pop()
  frame['stack'][len(frame['stack']) - 1] += popped
  return 2

def BINARY_SUBTRACT(frame, bytes):
  # pop of frame.stack
  popped = frame['stack'].pop()
  frame['stack'][len(frame['stack']) - 1] -= popped
  return 2

def RETURN_VALUE(frame, bytes):
  return 2

def STORE_FAST(frame, bytes):
  popped = frame['stack'].pop()
  frame['args'].append(popped)
  return 2

def POP_JUMP_IF_FALSE(frame, bytes):
  # check top of stack
  top = frame['stack'].pop()
  if (top): # bool was true, so return offset 2
    return 2
  offset = bytes[0]
  return offset - frame['index']

def COMPARE_OP(frame, bytes):
  popped = frame['stack'].pop()
  top = frame['stack'][len(frame['stack']) - 1]
  # set top of stack to result of compare op
  frame['stack'][len(frame['stack']) - 1] = OPERATORS[bytes[0]](top, popped)
  return 2

def BINARY_MULTIPLY(frame, bytes):
  popped = frame['stack'].pop()
  frame['stack'][len(frame['stack']) - 1] *= popped
  return 2

def LOAD_GLOBAL(frame, bytes):
  name = frame['names'][bytes[0]]
  frame['stack'].append(name)
  return 2

def LOAD_CONST(frame, bytes):
  const = frame['consts'][bytes[0]]
  frame['stack'].append(const)
  return 2

def CALL_FUNCTION(frame, bytes):
  print('frame', frame)
  print('bytes', bytes)
  # pop bytes[0] number of values off the stack
  # call function with poooped values
  popped_values = []
  for x in xrange(1, bytes[0]):
    popped_values.append(frame['stack'].pop())

  return 2

def evalOpcode(code, frame, bytes):
  return OPCODES[code](frame, bytes)

def evaluate(codeObject, *args):
  frame = {
   'stack': [],
   'args': list(args),
   'index': 0,
   'consts': codeObject.__code__.co_consts,
   'names': codeObject.__code__.co_names,
  }

  bytes = [int (b) for b in codeObject.__code__.co_code]
  print(bytes)
  index = 0
  while index < len(bytes):
    if (bytes[index] == 83):
      return frame['stack'][0]
    offset = evalOpcode(bytes[index], frame, bytes[index + 1:])
    index = index + offset
    frame['index'] = index


# SPEC
# =======================================================
def add(a, b):
  return a + b

def subtract(a, b):
  return a - b

def goALittleCrasy(a, b, c):
  return c - (a + b)

def goCrasy(a, b, c):
  d = a + b
  return d - c

def conditional(a, b, c):
  if (a > b):
    return c
  return a + b

def constant():
  d = 4
  e = 5
  return d

def addRecursion(a, b):
  c = a + b
  if (c < 5):
    return addRecursion(a, c)
  return c

def factr(a):
  if (a <= 1):
    return 1
  return a * (factr(a - 1))

def multiply(a, b):
  return a * b

OPERATORS = {
  0: lambda a, b: a < b,
  4: lambda a, b: a > b
}

OPCODES = {
  20: BINARY_MULTIPLY,
  23: BINARY_ADD,
  24: BINARY_SUBTRACT,
  83: RETURN_VALUE,
  100: LOAD_CONST,
  107: COMPARE_OP,
  114: POP_JUMP_IF_FALSE,
  116: LOAD_GLOBAL,
  124: LOAD_FAST,
  125: STORE_FAST,
  131: CALL_FUNCTION,
}

# TESTS
# =======================================================
# assert(evaluate(add, 1, 2) == 3)
# assert(evaluate(subtract, 1, 2) == -1)
# assert(evaluate(goALittleCrasy, 1, 2, 5) == 2)
# assert(evaluate(goCrasy, 1, 2, 5) == -2)
# assert(evaluate(goCrasy, 1, 2, 5) == -2)
# assert(evaluate(conditional, 1, 2, 5) == 3) # fall through
# assert(evaluate(conditional, 2, 1, 5) == 5) # branch into if block
# assert(evaluate(multiply, 3, 3) == 9)
# assert(evaluate(constant) == 4)
print(evaluate(addRecursion, 1, 1))

# [124, 0, 124, 1, 23, 0, 125, 2, 124, 2, 100, 1, 107, 0, 114, 26, 116, 0, 124, 0, 124, 2, 131, 2, 83, 0, 124, 2, 83, 0]