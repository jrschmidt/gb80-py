from typing import Literal, NotRequired, TypedDict


# --- Numeric expression sub-objects ---

class NumericLiteralExp(TypedDict):
    op: Literal["<numeric_literal>"]
    number: float

class NumericVariableExp(TypedDict):
    op: Literal["<numeric_variable>"]
    variable: str

class NumericRandomExp(TypedDict):
    op: Literal["<random>"]

type NumericFunctionExp = NumericRandomExp

class NumericOpExp(TypedDict):
    operand: str
    term1: "NumericExp"
    term2: "NumericExp"

type NumericExp = NumericLiteralExp | NumericVariableExp | NumericFunctionExp | NumericOpExp


# --- String expression sub-objects ---

class StringLiteralExp(TypedDict):
    op: Literal["<string_literal>"]
    string: str

class StringVariableExp(TypedDict):
    op: Literal["<string_variable>"]
    variable: str

class StringOpExp(TypedDict):
    op: Literal["<string_concatenation>"]
    terms: list[StringLiteralExp | StringVariableExp]

type StringExp = StringLiteralExp | StringVariableExp | StringOpExp


# --- Boolean expression sub-objects ---

class NumericBooleanExp(TypedDict):
    comparator: str
    variable: str
    term: NumericLiteralExp | NumericVariableExp

class StringBooleanExp(TypedDict):
    comparator: str
    variable: str
    term: StringLiteralExp | StringVariableExp

type BooleanExp = NumericBooleanExp | StringBooleanExp


# --- Line objects ---

class RemarkLine(TypedDict):
    op_type: Literal["<remark>"]
    text: str

class GotoLine(TypedDict):
    op_type: Literal["<goto>"]
    destination: int
    text: str

class IfThenLine(TypedDict):
    op_type: Literal["<if_then>"]
    expression: BooleanExp
    destination: int
    text: str

class NumericAssignmentLine(TypedDict):
    op_type: Literal["<numeric_assignment>"]
    variable: str
    expression: NumericExp
    text: str

class StringAssignmentLine(TypedDict):
    op_type: Literal["<string_assignment>"]
    variable: str
    expression: StringExp
    text: str

class PrintStringVariableLine(TypedDict):
    op_type: Literal["<print_string_variable>"]
    variable: str
    text: str

class PrintStringLiteralLine(TypedDict):
    op_type: Literal["<print_string_literal>"]
    string: str
    text: str

class PrintNumericVariableLine(TypedDict):
    op_type: Literal["<print_numeric_variable>"]
    variable: str
    text: str

class NumericInputLine(TypedDict):
    op_type: Literal["<numeric_input>"]
    variable: str
    text: str
    query_string: NotRequired[str]

class StringInputLine(TypedDict):
    op_type: Literal["<string_input>"]
    variable: str
    text: str
    query_string: NotRequired[str]

class EndLine(TypedDict):
    op_type: Literal["<end>"]
    text: str


type BasicLine = (
    RemarkLine | GotoLine | IfThenLine |
    NumericAssignmentLine | StringAssignmentLine |
    PrintStringVariableLine | PrintStringLiteralLine | PrintNumericVariableLine |
    NumericInputLine | StringInputLine |
    EndLine
)

type ProgramLines = dict[int, BasicLine]
