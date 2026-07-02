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
    "<parse_complete>",
    "<no_match>",
    "<error>",
    "<remainder_string>",
    "<original_line>",

    "<console_command>",
    "<clear>",
    "<list>",
    "<run>",
    "<save>",
    "<load>",
    "<files>",
    "<filename>",
    "<delete_program_line>",
    "<help>",

    "<program_line>",
    "<line_number>",
    "<line_number_ref>",
    "<single_space>",

    "<remark>",
    "<numeric_assignment>",
    "<string_assignment>",
    "<goto>",
    "<if_then>",
    "<if>",
    "<then>",
    "<print>",
    "<input>",
    "<query_string>",
    "<receiving_variable>",
    "<semicolon>",
    "<end>",

    "<numeric_expression>",
    "<numeric_expression_end>",
    "<numeric_literal>",
    "<numeric_variable>",
    "<numeric_operation>",
    "<numeric_singleton>",

    "<string_expression>",
    "<string_expression_end>",
    "<string_literal>",
    "<string_variable>",
    "<string_operation>",
    "<string_singleton>",

    "<concatenate>",
    "<plus>",
    "<minus>",
    "<times>",
    "<divide>",
    "<power>",
    "<left_paren>",
    "<right_paren>",
    "<random>",

    "<boolean_expression>",
    "<num_bool_expression>",
    "<str_bool_expression>",
    "<boolean_expression_end>",
    "<equals>",
    "<not_equal>",
    "<greater_than>",
    "<greater_equal>",
    "<lesser_than>",
    "<lesser_equal>",
    "<numeric_equals>",
    "<string_equals>",
    "<numeric_not_equal>",
    "<string_not_equal>",

    "<numeric_print>",
    "<string_print>",
    "<numeric_input>",
    "<string_input>"
]