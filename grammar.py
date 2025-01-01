from parsimonious.grammar import Grammar

imperivm = Grammar(
    r"""
    program         = subroutine (sp_0n br ws_0n subroutine)* ws_0n
    subroutine      = identifier ws_1n block
    block           = begin ws_1n (instruction (sp_0n br ws_0n instruction)*)? ws_1n end
    instruction     = assignment / conditional / loop / stack_op / arithmetic_op / boolean_op / io_op / stop / identifier / halt / store / load

    assignment      = assign sp_1n value sp_1n identifier
    conditional     = if sp_1n value ws_1n block (ws_1n elif sp_1n value ws_1n block)* (ws_1n else ws_1n block)?
    loop            = while sp_1n value ws_1n block
    stack_op        = (push sp_1n value) / (pop sp_1n identifier)
    arithmetic_op   = (add / subtract / multiply / divide) sp_1n value sp_1n identifier
    boolean_op      = (and / or / xor / negate / not) sp_1n identifier
    io_op           = print sp_1n value
    halt            = exit sp_1n value

    value           = identifier / literal
    literal         = integer / float / string

    identifier      = !reserved ~r"[a-z][a-z0-9_]*"i
    
    integer         = ~r"-?(0|([1-9][0-9]*))"
    float           = ~r"-?(0|([1-9][0-9]*))\.[0-9]+"
    string          = quote string_text quote

    quote           = "\""
    string_text     = ~r"([^\"\\]|\\.)*"

    br              = ~r"\n"
    ws_0n           = ~r"\s*"
    ws_1n           = ~r"\s+"
    sp_0n           = ~r"[ \t]*"
    sp_1n           = ~r"[ \t]+"

    reserved        = begin / end / stop / if / elif / else / while / push
                        / pop / assign / add / subtract / multiply / divide
                        / and / or / xor / not / print / exit / store / load
    begin           = ~r"begin"i / ~r"do"i
    exit            = ~r"exit"i
    end             = ~r"end"i
    stop            = ~r"stop"i
    if              = ~r"if"i
    elif            = ~r"elif"i
    else            = ~r"else"i
    while           = ~r"while"i
    push            = ~r"push"i
    pop             = ~r"pop"i
    assign          = ~r"assign"i
    add             = ~r"add"i
    subtract        = ~r"subtract"i
    multiply        = ~r"multiply"i
    divide          = ~r"divide"i
    and             = ~r"and"i
    or              = ~r"or"i
    xor             = ~"xor"i
    negate          = ~r"negate"i
    not             = ~"not"i
    print           = ~r"print"i
    store           = ~r"store"i
    load            = ~r"load"i
    """
)
