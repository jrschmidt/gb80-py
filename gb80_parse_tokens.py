# ####    List of allowable parse tokens.    ####
# 
# Lines entered in the terminal are parsed into a list of tokens from this list.
# 
# A new line is initially given the single token <raw_string>. Then the tokenize()
# method attempts to parse the line, returning a single tag <error> if something
# is wrong with it.
# 
# A line that is not erroneous will be either a 'command' line or a 'program' line.
# A command line is a terminal command like CLEAR, LIST, or RUN. They will be parsed
# with the token <command>, followed by a command token like <clear>, <list> <run>.
# A program line will be parsed with the token <program_line>, followed by first the
# line number, then the other tokens defining the structure of the program line.
# 
# Note - Besides the tokens, a parse list can also contain literal values, strings
# or numbers. These literal values will be preceeded by a token identifying it as a
# specific type of value, such as <string_literal>, <number_literal> or <line_number>.


parse_tokens = [
    "<raw_string>",
    "<parse_complete>",
    "<no_match>",
    "<error>",
    "<undefined>",
    "<remainder_string>",
    "<original_line>",
    "<console_command>",
    "<clear>",
    "<list>",
    "<run>",
    "<delete_program_line>"
    "<program_line>",
    "<line_number>",
    "<line_number_ref>",
    "<single_space>",
    "<remark>",
    "<goto>",
    "<gosub>",
    "<gosub_return>",
    "<if_then>",
    "<if>",
    "<then>",
    "<input>",
    "<semicolon>",
    "<end>",
    "<numeric_variable>",
    "<string_variable>",
    "<string_literal>",
    "<numeric_literal>",
    "<unparsed_expression>"
    "<numeric_expression>",
    "<string_expression>",
    "<boolean_expression>",
    "<plus>",
    "<minus>",
    "<times>",
    "<divide>",
    "<power>",
    "<left_paren>",
    "<right_paren>",
    "<equals>",
    "<not_equal>",
    "<greater_than>",
    "<greater_equal>",
    "<lesser_than>",
    "<lesser_equal>"
]