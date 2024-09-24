#!/usr/bin/env python3

# pylint: disable=too-many-lines

"""
======= pySELL =================================================================
        
        A Python based Simple E-Learning Language 
        for the simple creation of interactive courses

LICENSE GPLv3

AUTHOR  Andreas Schwenk <mailto:contact@compiler-construction.com>

DOCS    Refer to https://github.com/andreas-schwenk/pysell and read the
        descriptions at the end of the page

INSTALL Run 'pip install pysell', or use the stand-alone implementation sell.py

CMD     pysell [-J] PATH
        
        -J          is optional and generates a JSON output file for debugging        
   
EXAMPLE pysell examples/ex1.txt

        outputs files examples/ex1.html and examples/ex1_DEBUG.html

FAQ
    
    Q: Why is this file so large?
    A: The goal is to offer pySELL as a single file for easy sharing.

    Q: Why not package and publish pySELL as a module?
    A: That's already available! Simply run "pip install pysell" 
       to install it as a package.
"""


import base64
import datetime
import io
import json
import os
import re
import sys
from typing import Self


class SellError(Exception):
    """exception"""


# pylint: disable-next=too-few-public-methods
class Lexer:
    """Scanner that takes a string input and returns a sequence of tokens;
    one at a time."""

    def __init__(self, src: str) -> None:
        """sets the source to be scanned"""
        # the source code
        self.src: str = src
        # the current token
        self.token: str = ""
        # the current input position
        self.pos: int = 0
        # set the first token to self.token
        self.next()

    def next(self) -> None:
        """gets the next token"""
        # start with a fresh token
        self.token = ""
        # loop up to the next special character
        stop = False
        while not stop and self.pos < len(self.src):
            # get the next character from the input
            ch = self.src[self.pos]
            # in case that we get a special character (a.k.a delimiter),
            # we stop
            if ch in "`^'\"%#*$()[]{}\\,.:;+-*/_!<>\t\n =?|&":
                # if the current token is not empty, return it for now and
                # keep the delimiter to the next call of next()
                if len(self.token) > 0:
                    return
                # a delimiter stops further advancing in the input
                stop = True
                # keep quotes as a single token. Supported quote types are
                # double quotes ("...") and accent grave quotes (`...`)
                if ch in '"`':
                    kind = ch  # " or `
                    self.token += ch
                    self.pos += 1
                    # advance to the quotation end
                    while self.pos < len(self.src):
                        if self.src[self.pos] == kind:
                            break
                        self.token += self.src[self.pos]
                        self.pos += 1
            # add the current character to the token
            self.token += ch
            self.pos += 1


# # lexer tests
# lex = Lexer('a"x"bc 123 *blub* $`hello, world!`123$')
# while len(lex.token) > 0:
#     print(lex.token)
#     lex.next()
# exit(0)

# For drawing random variables and to calculate the sample solution, we will
# be executing Python code that is embedded in the quiz descriptions.
# The evaluation of code will populate local variables. Its data types also
# depend on the used libraries.
# The following lists cluster some of these types.
boolean_types = ["<class 'bool'>", "<class 'numpy.bool_'>"]
int_types = [
    "<class 'int'>",
    "<class 'numpy.int64'>",
    "<class 'sympy.core.numbers.Integer'>",
    "<class 'sage.rings.integer.Integer'>",
    "<class 'sage.rings.finite_rings.integer_mod.IntegerMod_int'>",
]
float_types = ["<class 'float'>"]

# The following list contains all of Pythons basic keywords. These are used
# in syntax highlighting in "*_DEBUG.html" files.
python_kws = [
    "and",
    "as",
    "assert",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "False",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "None",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "True",
    "try",
    "while",
    "with",
    "yield",
]

# The following list of identifiers may be in locals of Python source that
# uses "sympy". These identifiers must be skipped in the JSON output.
skipVariables = [
    "acos",
    "acosh",
    "acoth",
    "asin",
    "asinh",
    "atan",
    "atan2",
    "atanh",
    "ceil",
    "ceiling",
    "cos",
    "cosh",
    "cot",
    "coth",
    "exp",
    "floor",
    "ln",
    "log",
    "pi",
    "round",
    "sin",
    "sinc",
    "sinh",
    "tan",
    "transpose",
]


# The following function rangeZ is provided as pseudo-intrinsic
# function in Python scripts, embedded into the question descriptions.
# It is an alternative version for "range", that excludes the zero.
# This is beneficial for drawing random numbers of questions for math classes.
# (the next line disables a warning, about camel-case function names)
# pylint: disable-next=invalid-name
def rangeZ(*a):
    """implements 'range', but excludes the zero"""
    r = []
    if len(a) == 1:
        r = list(range(a[0]))
    elif len(a) == 2:
        r = list(range(a[0], a[1]))
    elif len(a) == 3:
        r = list(range(a[0], a[1], a[2]))
    if 0 in r:
        r.remove(0)
    return r


# TODO: add comments starting from here


class TextNode:
    """Tree structure for the question text"""

    def __init__(self, type_: str, data: str = "") -> None:
        self.type: str = type_
        self.data: str = data
        self.children: list[TextNode] = []

    # pylint: disable-next=too-many-branches,too-many-statements
    def parse(self) -> None:
        """parses text recursively"""
        if self.type == "root":
            self.children = [TextNode(" ", "")]
            lines = self.data.split("\n")
            self.data = ""
            for line in lines:
                line = line.strip()
                if len(line) == 0:
                    continue
                type_ = line[0]  # refer to "types" below
                if type_ not in "[(-!":
                    type_ = " "
                if type_ != self.children[-1].type:
                    self.children.append(TextNode(type_, ""))
                self.children[-1].type = type_
                self.children[-1].data += line + "\n"
                if line.endswith("\\\\"):
                    # line break
                    # TODO: this is NOT allowed, if we are within math mode!!
                    self.children[-1].data = self.children[-1].data[:-3] + "\n"
                    self.children.append(TextNode(" ", ""))
            types = {
                " ": "paragraph",
                "(": "single-choice",
                "[": "multi-choice",
                "-": "itemize",
                "!": "command",
            }
            for child in self.children:
                child.type = types[child.type]
                child.parse()

        elif self.type in ("multi-choice", "single-choice"):
            options = self.data.strip().split("\n")
            self.data = ""
            for option in options:
                node = TextNode("answer")
                self.children.append(node)
                text = ""
                if self.type == "multi-choice":
                    text = "]".join(option.split("]")[1:]).strip()
                else:
                    text = ")".join(option.split(")")[1:]).strip()
                if option.startswith("[!"):
                    # conditionally set option
                    # TODO: check, if variable exists and is of type bool
                    var_id = option[2:].split("]")[0]
                    node.children.append(TextNode("var", var_id))
                else:
                    # statically set option
                    correct = option.startswith("[x]") or option.startswith("(x)")
                    node.children.append(
                        TextNode("bool", "true" if correct else "false")
                    )
                node.children.append(TextNode("paragraph", text))
                node.children[1].parse()

        elif self.type == "itemize":
            items = self.data.strip().split("\n")
            self.data = ""
            for child in items:
                node = TextNode("paragraph", child[1:].strip())
                self.children.append(node)
                node.parse()

        elif self.type == "paragraph":
            lex = Lexer(self.data.strip())
            self.data = ""
            self.children.append(self.parse_span(lex))

        elif self.type == "command":
            if (
                ".svg" in self.data
                or ".png" in self.data
                or ".jpg" in self.data
                or ".jpeg" in self.data
            ):
                self.parse_image()
            else:
                # TODO: report error
                pass

        else:
            raise SellError("unimplemented")

    def parse_image(self) -> Self:
        """parses an image inclusion"""
        img_path = self.data[1:].strip()
        img_width = 100  # percentage
        if ":" in img_path:
            tokens = img_path.split(":")
            img_path = tokens[0].strip()
            img_width = tokens[1].strip()
        self.type = "image"
        self.data = img_path
        self.children.append(TextNode("width", img_width))

    def parse_span(self, lex: Lexer) -> Self:
        """parses a span element"""
        # grammar: span = { item };
        #          item = bold | math | input | string_var | plus_minus | text;
        #          bold = "*" { item } "*";
        #          math = "$" { item } "$";
        #          input = "%" ["!"] var;
        #          string_var = "&" var;
        #          plus_minus = "+" "-";
        #          text = "\\" | otherwise;
        span = TextNode("span")
        while lex.token != "":
            span.children.append(self.parse_item(lex))
        return span

    # pylint: disable-next=too-many-return-statements
    def parse_item(self, lex: Lexer, math_mode=False) -> Self:
        """parses a single item of a span/paragraph"""
        if not math_mode and lex.token == "*":
            return self.parse_bold_italic(lex)
        if lex.token == "$":
            return self.parse_math(lex)
        if not math_mode and lex.token == "%":
            return self.parse_input(lex)
        if not math_mode and lex.token == "&":
            return self.parse_string_var(lex)
        if math_mode and lex.token == "+":
            n = TextNode("text", lex.token)
            lex.next()
            if lex.token == "-":
                # "+-" automatically chooses "+" or "-",
                # depending on the sign or the following variable.
                # For the variable itself, only its absolute value is used.
                n.data += lex.token
                n.type = "plus_minus"
                lex.next()
            return n
        if not math_mode and lex.token == "\\":
            lex.next()
            if lex.token == "\\":
                lex.next()
            return TextNode("text", "<br/>")
        n = TextNode("text", lex.token)
        lex.next()
        return n

    def parse_bold_italic(self, lex: Lexer) -> Self:
        """parses bold or italic text"""
        node = TextNode("italic")
        if lex.token == "*":
            lex.next()
        if lex.token == "*":
            node.type = "bold"
            lex.next()
        while lex.token not in ("", "*"):
            node.children.append(self.parse_item(lex))
        if lex.token == "*":
            lex.next()
        if lex.token == "*":
            lex.next()
        return node

    def parse_math(self, lex: Lexer) -> Self:
        """parses inline math or display style math"""
        math = TextNode("math")
        if lex.token == "$":
            lex.next()
        if lex.token == "$":
            math.type = "display-math"
            lex.next()
        while lex.token not in ("", "$"):
            math.children.append(self.parse_item(lex, True))
        if lex.token == "$":
            lex.next()
        if math.type == "display-math" and lex.token == "$":
            lex.next()
        return math

    def parse_input(self, lex: Lexer) -> Self:
        """parses an input element field"""
        input_ = TextNode("input")
        if lex.token == "%":
            lex.next()
        if lex.token == "!":
            input_.type = "input2"
            lex.next()
        input_.data = lex.token.strip()
        lex.next()
        return input_

    def parse_string_var(self, lex: Lexer) -> Self:
        """parses a string variable"""
        sv = TextNode("string_var")
        if lex.token == "&":
            lex.next()
        sv.data = lex.token.strip()
        lex.next()
        return sv

    def optimize(self) -> Self:
        """optimizes the current text node recursively. E.g. multiple pure
        text items are concatenated into a single text node."""
        children_opt = []
        for c in self.children:
            opt = c.optimize()
            if (
                opt.type == "text"
                and opt.data.startswith('"') is False
                and opt.data.startswith("`") is False
                and len(children_opt) > 0
                and children_opt[-1].type == "text"
                and children_opt[-1].data.startswith('"') is False
                and children_opt[-1].data.startswith("`") is False
            ):
                children_opt[-1].data += opt.data
            else:
                children_opt.append(opt)
        self.children = children_opt
        return self

    def to_dict(self) -> dict:
        """recursively exports the text node instance to a dictionary"""
        # t := type, d := data, c := children
        return {
            "t": self.type,
            "d": self.data,
            "c": list(map(lambda o: o.to_dict(), self.children)),
        }


# pylint: disable-next=too-many-instance-attributes
class Question:
    """Question of the quiz"""

    def __init__(self, input_dirname: str, src_line_no: int) -> None:
        self.input_dirname: str = input_dirname
        self.src_line_no: int = src_line_no
        self.title: str = ""
        self.points: int = 1
        self.python_src: str = ""
        self.variables: set[str] = set()
        self.instances: list[dict] = []
        self.text_src: str = ""
        self.text: TextNode = None
        self.error: str = ""
        self.python_src_tokens: set[str] = set()

    def build(self) -> None:
        """builds a question from text and Python sources"""
        if len(self.python_src) > 0:
            self.analyze_python_code()
            instances_str = []
            if len(self.error) == 0:
                for _ in range(0, 5):
                    # try to generate instances distinct to prior once
                    # TODO: give up and keep less than 5, if applicable!
                    instance = {}
                    instance_str = ""
                    for _ in range(0, 10):
                        self.error = ""
                        instance = self.run_python_code()
                        instance_str = str(instance)
                        if instance_str not in instances_str:
                            break
                    instances_str.append(instance_str)
                    self.instances.append(instance)
                    # if there is no randomization in the input, then one instance is enough
                    if "rand" not in self.python_src:
                        break
                if "No module named" in self.error:
                    print("!!! " + self.error)
        self.text = TextNode("root", self.text_src)
        self.text.parse()
        var_occurrences: set[str] = set()
        self.post_process_text(self.text, False, var_occurrences)
        self.text.optimize()

    # pylint: disable-next=too-many-branches
    def post_process_text(
        self, node: TextNode, math, var_occurrences: set[str]
    ) -> None:
        """post processes the textual part. For example, a semantical check
        for the existing of referenced variables is applied. Also images
        are loaded and stringified."""
        for c in node.children:
            self.post_process_text(
                c,
                math or node.type == "math" or node.type == "display-math",
                var_occurrences,
            )
        if node.type == "input":
            if node.data.startswith('"'):
                # gap question
                node.type = "gap"
                node.data = node.data.replace('"', "")
            elif node.data in self.variables:
                var_id = node.data
                if var_id in var_occurrences:
                    self.error += "It is not allowed to refer to a variable "
                    self.error += "twice or more. Hint: Create a copy of "
                    self.error += f"variable '{var_id}' in Python and ask for "
                    self.error += "the new variable name. "
                    self.error += f"Example code: '{var_id}2 = {var_id}'."
                    self.error += f"Then ask for '%{var_id}2'."
                else:
                    var_occurrences.add(var_id)
            elif node.data not in self.variables:
                # ask for numerical/term variable
                var_id = node.data
                self.error += f"Unknown input variable '{var_id}'. "
        elif node.type == "string_var":
            var_id = node.data
            if var_id not in self.variables:
                self.error += f"Unknown string variable '{var_id}'. "
        elif node.type == "text":
            if (
                math
                and len(node.data) >= 2
                and node.data.startswith('"')
                and node.data.endswith('"')
            ):
                node.data = node.data[1:-1]
            elif math and (node.data in self.variables):
                node.type = "var"
            elif (
                not math
                and len(node.data) >= 2
                and node.data.startswith("`")
                and node.data.endswith("`")
            ):
                node.type = "code"
                node.data = node.data[1:-1]
        elif node.type == "image":
            # TODO: warning, if file size is (too) large
            path = os.path.join(self.input_dirname, node.data)
            img_type = os.path.splitext(path)[1][1:]
            supported_img_types = ["svg", "png", "jpg", "jpeg"]
            if img_type not in supported_img_types:
                self.error += f"ERROR: image type '{img_type}' is not supported. "
                self.error += f"Use one of {', '.join(supported_img_types)}"
            elif os.path.isfile(path) is False:
                self.error += "ERROR: cannot find image at path '" + path + '"'
            else:
                # load image
                f = open(path, "rb")
                data = f.read()
                f.close()
                b64 = base64.b64encode(data)
                node.children.append(TextNode("data", b64.decode("utf-8")))

    def float_to_str(self, v: float) -> str:
        """Converts float to string and cuts '.0' if applicable"""
        s = str(v)
        if s.endswith(".0"):
            return s[:-2]
        return s

    def analyze_python_code(self) -> None:
        """Get all tokens from Python source code. This is required to filter
        out all locals from libraries (refer to method run_python_code).
        Since relevant tokens are only those in the left-hand side of an
        assignment, we filter out non-assignment statements, as well as
        the right-hand side of statements. As a side effect, irrelevant symbols
        of packages are also filtered out (e.g. 'mod', is populated to the
        locals, when using 'sage.all.power_mod')"""
        lines = self.python_src.split("\n")
        for line in lines:
            if "=" not in line:
                continue
            lhs = line.split("=")[0]
            lex = Lexer(lhs)
            while len(lex.token) > 0:
                self.python_src_tokens.add(lex.token)
                lex.next()
        # check for forbidden code
        if "matplotlib" in self.python_src and "show(" in self.python_src:
            self.error += "Remove the call show(), "
            self.error += "since this would result in MANY open windows :-)"

    # pylint: disable-next=too-many-locals,too-many-branches,too-many-statements
    def run_python_code(self) -> dict:
        """Runs the questions python code and gathers all local variables."""
        local_variables = {}
        res = {}
        src = self.python_src
        try:
            # pylint: disable-next=exec-used
            exec(src, globals(), local_variables)
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            # print(e)
            self.error += str(e) + ". "
            return res
        for local_id, value in local_variables.items():
            if local_id in skipVariables or (local_id not in self.python_src_tokens):
                continue
            type_str = str(type(value))
            if type_str in ("<class 'module'>", "<class 'function'>"):
                continue
            self.variables.add(local_id)
            t = ""  # type
            v = ""  # value
            if type_str in boolean_types:
                t = "bool"
                v = str(value).lower()
            elif type_str in int_types:
                t = "int"
                v = str(value)
            elif type_str in float_types:
                t = "float"
                v = self.float_to_str(value)
            elif type_str == "<class 'complex'>":
                t = "complex"
                # convert "-0" to "0"
                real = 0 if value.real == 0 else value.real
                imag = 0 if value.imag == 0 else value.imag
                v = self.float_to_str(real) + "," + self.float_to_str(imag)
            elif type_str == "<class 'list'>":
                t = "vector"
                v = str(value).replace("[", "").replace("]", "").replace(" ", "")
            elif type_str == "<class 'set'>":
                t = "set"
                v = (
                    str(value)
                    .replace("{", "")
                    .replace("}", "")
                    .replace(" ", "")
                    .replace("j", "i")
                )
            elif type_str == "<class 'sympy.matrices.dense.MutableDenseMatrix'>":
                # e.g. 'Matrix([[-1, 0, -2], [-1, 5*sin(x)*cos(x)/7, 2], [-1, 2, 0]])'
                t = "matrix"
                v = str(value)[7:-1]
                v = v.replace("**", "^")
            elif (
                type_str == "<class 'numpy.matrix'>"
                or type_str == "<class 'numpy.ndarray'>"
            ):
                # e.g. '[[ -6 -13 -12]\n [-17  -3 -20]\n [-14  -8 -16]\n [ -7 -15  -8]]'
                t = "matrix"
                v = re.sub(" +", " ", str(value))  # remove double spaces
                v = re.sub(r"\[ ", "[", v)  # remove space(s) after "["
                v = re.sub(r" \]", "]", v)  # remove space(s) before "]"
                v = v.replace(" ", ",").replace("\n", "")
            elif type_str == "<class 'str'>":
                t = "string"
                v = value
            else:
                t = "term"
                v = str(value).replace("**", "^")
                # in case that an ODE is contained in the question
                # and only one constant ("C1") is present, then substitute
                # "C1" by "C"
                if "dsolve" in self.python_src:
                    if "C2" not in v:
                        v = v.replace("C1", "C")
            # t := type, v := value
            v = v.replace("I", "i")  # reformat sympy imaginary part
            res[local_id] = {"t": t, "v": v}
        if len(self.variables) > 50:
            self.error += "ERROR: Wrong usage of Python imports. Refer to pySELL docs!"
            # TODO: write the docs...

        if "matplotlib" in self.python_src and "plt" in local_variables:
            plt = local_variables["plt"]
            buf = io.BytesIO()
            plt.savefig(buf, format="svg", transparent=True)
            buf.seek(0)
            svg = buf.read()
            b64 = base64.b64encode(svg)
            res["__svg_image"] = {"t": "svg", "v": b64.decode("utf-8")}
            plt.clf()
        return res

    def to_dict(self) -> dict:
        """recursively exports the question to a dictionary"""
        return {
            "title": self.title,
            "points": self.points,
            "error": self.error,
            "is_ode": "dsolve"  # contains an Ordinary Differential Equation
            in self.python_src,
            "variables": list(self.variables),
            "instances": self.instances,
            "text": self.text.to_dict(),
            # the following is only relevant for debugging purposes,
            # i.e. only present in _DEBUG.html
            "src_line": self.src_line_no,
            "text_src_html": self.syntax_highlight_text(self.text_src),
            "python_src_html": self.syntax_highlight_python(self.python_src),
            "python_src_tokens": list(self.python_src_tokens),
        }

    # pylint: disable-next=too-many-branches,too-many-statements
    def syntax_highlight_text_line(self, src: str) -> str:
        """syntax highlights a single questions text line and returns the
        formatted code in HTML format"""
        html = ""
        math = False
        code = False
        bold = False
        italic = False
        n = len(src)
        i = 0
        while i < n:
            ch = src[i]
            if ch == " ":
                html += "&nbsp;"
            elif not math and ch == "%":
                html += '<span style="color:green; font-weight: bold;">'
                html += ch
                if i + 1 < n and src[i + 1] == "!":
                    html += src[i + 1]
                    i += 1
                html += "</span>"
            elif ch == "*" and i + 1 < n and src[i + 1] == "*":
                i += 1
                bold = not bold
                if bold:
                    html += '<span style="font-weight: bold;">'
                    html += "**"
                else:
                    html += "**"
                    html += "</span>"
            elif ch == "*":
                italic = not italic
                if italic:
                    html += '<span style="font-style: italic;">'
                    html += "*"
                else:
                    html += "*"
                    html += "</span>"
            elif ch == "$":
                display_style = False
                if i + 1 < n and src[i + 1] == "$":
                    display_style = True
                    i += 1
                math = not math
                if math:
                    html += '<span style="color:#FF5733; font-weight: bold;">'
                    html += ch
                    if display_style:
                        html += ch
                else:
                    html += ch
                    if display_style:
                        html += ch
                    html += "</span>"
            elif ch == "`":
                code = not code
                if code:
                    html += '<span style="color:#33A5FF; font-weight: bold;">'
                    html += ch
                else:
                    html += ch
                    html += "</span>"
            else:
                html += ch
            i += 1
        if math:
            html += "</span>"
        if code:
            html += "</span>"
        if italic:
            html += "</span>"
        if bold:
            html += "</bold>"
        return html

    def red_colored_span(self, inner_html: str) -> str:
        """embeds HTML code into a red colored span"""
        return '<span style="color:#FF5733; font-weight:bold">' + inner_html + "</span>"

    def syntax_highlight_text(self, src: str) -> str:
        """syntax highlights a questions text and returns the formatted code in
        HTML format"""
        html = ""
        lines = src.split("\n")
        for line in lines:
            if len(line.strip()) == 0:
                continue
            if line.startswith("-"):
                html += self.red_colored_span("-")
                line = line[1:].replace(" ", "&nbsp;")
            elif line.startswith("["):
                l1 = line.split("]")[0] + "]".replace(" ", "&nbsp;")
                html += self.red_colored_span(l1)
                line = "]".join(line.split("]")[1:]).replace(" ", "&nbsp;")
            elif line.startswith("("):
                l1 = line.split(")")[0] + ")".replace(" ", "&nbsp;")
                html += self.red_colored_span(l1)
                line = ")".join(line.split(")")[1:]).replace(" ", "&nbsp;")
            html += self.syntax_highlight_text_line(line)
            html += "<br/>"
        return html

    def syntax_highlight_python(self, src: str) -> str:
        """syntax highlights a questions python code and returns the formatted
        code in HTML format"""
        lines = src.split("\n")
        html = ""
        for line in lines:
            if len(line.strip()) == 0:
                continue
            lex = Lexer(line)
            while len(lex.token) > 0:
                if len(lex.token) > 0 and lex.token[0] >= "0" and lex.token[0] <= "9":
                    html += '<span style="color:green; font-weight:bold">'
                    html += lex.token + "</span>"
                elif lex.token in python_kws:
                    html += '<span style="color:#FF5733; font-weight:bold">'
                    html += lex.token + "</span>"
                else:
                    html += lex.token.replace(" ", "&nbsp;")
                lex.next()
            html += "<br/>"
        return html


def compile_input_file(input_dirname: str, src: str) -> dict:
    """compiles a SELL input file to JSON"""
    lang = "en"  # language
    title = ""
    author = ""
    info = ""
    timer = -1  # time limit for the worksheet (default: off)
    grade = False  # True, if the worksheet is evaluated and graded for all questions
    questions = []
    question = None
    parsing_python = False
    lines = src.split("\n")
    for line_no, line in enumerate(lines):
        line = line.split("#")[0]  # remove comments
        line_not_stripped = line
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith("LANG"):
            lang = line[4:].strip()
        elif line.startswith("TITLE"):
            title = line[5:].strip()
        elif line.startswith("AUTHOR"):
            author = line[6:].strip()
        elif line.startswith("INFO"):
            info = line[4:].strip()
        elif line.startswith("GRADE"):
            grade = True
        elif line.startswith("TIMER"):
            timer = int(line[5:].strip())  # TODO: handle parse integer errors
        elif line.startswith("QUESTION"):
            question = Question(input_dirname, line_no + 1)
            questions.append(question)
            # extract title and points
            #   pattern = TITLE [ "(" INT "pts)" ];
            pattern = r"(?P<title>.+?)(?:\s\((?P<num>\d+)\spts\))?$"
            match = re.match(pattern, line[8:].strip())
            if match:
                title = match.group("title").strip()
                num = match.group("num")  # This will be None if not present
                # print(f"Title: {title}, Points: {num}")
            question.title = title
            question.points = 1 if num is None else int(num)
            parsing_python = False
        elif question is not None:
            if line.startswith('"""'):
                parsing_python = not parsing_python
            else:
                if parsing_python:
                    question.python_src += (
                        line_not_stripped.replace("\t", "    ") + "\n"
                    )
                else:
                    question.text_src += line + "\n"
    for question in questions:
        question.build()
    return {
        "lang": lang,
        "title": title,
        "author": author,
        "date": datetime.datetime.today().strftime("%Y-%m-%d"),
        "info": info,
        "timer": timer,
        "grade": grade,
        "questions": list(map(lambda o: o.to_dict(), questions)),
    }


# the following code is automatically generated and updated by file "build.py"
# @begin(html)
HTML: str = b''
HTML += b'<!DOCTYPE html> <html> <head> <meta charset="UTF-8" /> <titl'
HTML += b'e>pySELL Quiz</title> <meta name="viewport" content="width=d'
HTML += b'evice-width, initial-scale=1.0" /> <link rel="icon" type="im'
HTML += b'age/x-icon" href="data:image/x-icon;base64,AAABAAEAEBAAAAEAI'
HTML += b'ABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAA'
HTML += b'AAAAACqqqr/PDw8/0VFRf/V1dX////////////09Pb/trbO/3t7q/9wcLH/c'
HTML += b'XG0/3NzqP+iosH/5OTr////////////j4+P/wAAAP8KCgr/x8fH///////k5'
HTML += b'Or/bGym/y4ukP8kJJD/IiKR/yIikv8jI5H/KCiP/1BQnP/Jydz//////5CQk'
HTML += b'P8BAQH/DAwM/8jIyP/7+/v/cHCo/yIij/8lJZP/KSmR/z4+lf9AQJH/Li6Q/'
HTML += b'yUlkv8jI5H/TEya/9/f6P+QkJD/AQEB/wwMDP/Ly8r/ycna/y4ujv8lJZP/N'
HTML += b'DSU/5+fw//j4+v/5+fs/76+0v9LS5f/JSWS/yYmkP+Skrr/kJCQ/wAAAP8MD'
HTML += b'Az/zc3L/5aWvP8iIo//ISGQ/39/sf////7/////////////////n5+7/yMjj'
HTML += b'P8kJJH/bm6p/5CQkP8BAQH/CgoK/6SkpP+Skp//XV2N/1dXi//Hx9X//////'
HTML += b'///////////9fX1/39/rP8kJI7/JCSR/25upP+QkJD/AQEB/wEBAf8ODg7/F'
HTML += b'BQT/xUVE/8hIR//XV1c/8vL0P/IyNv/lZW7/1panP8rK5D/JiaT/ycnjv+bm'
HTML += b'7v/kJCQ/wEBAf8AAAD/AAAA/wAAAP8AAAD/AAAH/wAAK/8aGmv/LCyO/yQkj'
HTML += b'/8jI5L/JSWT/yIikP9dXZ//6enu/5CQkP8BAQH/BQUF/0xMTP9lZWT/Pz9N/'
HTML += b'wUFVP8AAGz/AABu/xYWhf8jI5L/JCSP/zY2k/92dq7/4ODo//////+QkJD/A'
HTML += b'QEB/wwMDP/IyMj//Pz9/2lppf8ZGYf/AgJw/wAAZ/8cHHL/Zmak/5ubv//X1'
HTML += b'+T//v7+////////////kJCQ/wEBAf8MDAz/ycnJ/9/f6f85OZT/IyOR/wcHZ'
HTML += b'P8AAB7/UVFZ//n5+P//////0dHd/7i4yf++vs7/7e3z/5CQkP8AAAD/DAwM/'
HTML += b'87Ozf/Y2OP/MjKQ/x8fjv8EBEr/AAAA/1xcWv//////6ent/0tLlf8kJIn/M'
HTML += b'jKL/8fH2v+QkJD/AQEB/wcHB/98fHv/jo6T/yUlc/8JCXj/AABi/wAAK/9eX'
HTML += b'nj/trbS/2xspv8nJ5H/IyOT/0pKm//m5uz/kJCQ/wEBAf8AAAD/AAAA/wAAA'
HTML += b'P8AACH/AABk/wAAbf8EBHD/IyOM/ykpkv8jI5H/IyOS/ysrjP+kpMP//////'
HTML += b'5GRkf8CAgL/AQEB/wEBAf8BAQH/AgIE/woKK/8ZGWj/IyOG/ycnj/8nJ4//M'
HTML += b'DCS/0xMmf+lpcP/+vr6///////Pz8//kZGR/5CQkP+QkJD/kJCQ/5OTk/+ws'
HTML += b'K//zs7V/8LC2f+goL3/oaG+/8PD2P/n5+z/////////////////AAAAAAAAA'
HTML += b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
HTML += b'AAAAAAAAAAAAAAAAA==" sizes="16x16" /> <link rel="stylesheet"'
HTML += b' href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.'
HTML += b'min.css" integrity="sha384-n8MVd4RsNIU0tAv4ct0nTaAbDJwPJzDEa'
HTML += b'qSD1odI+WdtXRGWt2kTvGFasHpSy3SV" crossorigin="anonymous" /> '
HTML += b'<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/'
HTML += b'katex.min.js" integrity="sha384-XjKyOOlGwcjNTAIQHIpgOno0Hl1Y'
HTML += b'QqzUOEleOLALmuqehneUG+vnGctmUb0ZY0l8" crossorigin="anonymous'
HTML += b'" ></script> <style> :root { --grey: #2c2c2c; --green: rgb(2'
HTML += b'4, 82, 1); --red: rgb(123, 0, 0); } html, body { font-family'
HTML += b': Arial, Helvetica, sans-serif; margin: 0; padding: 0; backg'
HTML += b'round-color: white; } .contents { max-width: 1024px; margin-'
HTML += b'left: auto; margin-right: auto; padding: 0; } h1 { text-alig'
HTML += b'n: center; font-size: 28pt; word-wrap: break-word; margin-bo'
HTML += b'ttom: 10px; user-select: none; } img { width: 100%; display:'
HTML += b' block; margin-left: auto; margin-right: auto; user-select: '
HTML += b'none; } .author { text-align: center; font-size: 16pt; margi'
HTML += b'n-bottom: 24px; user-select: none; } .courseInfo { text-alig'
HTML += b'n: center; user-select: none; } .footer { position: relative'
HTML += b'; bottom: 0; font-size: small; text-align: center; line-heig'
HTML += b'ht: 1.8; color: white; background-color: #2c2c2c; margin: 0;'
HTML += b' padding: 10px; user-select: none; } .question { position: r'
HTML += b'elative; /* required for feedback overlays */ color: black; '
HTML += b'background-color: white; border-style: solid; border-width: '
HTML += b'6px; border-color: white; padding: 4px; margin-top: 32px; ma'
HTML += b'rgin-bottom: 32px; -webkit-box-shadow: 0px 0px 6px 3px #e8e8'
HTML += b'e8; box-shadow: 0px 0px 6px 3px #e8e8e8; overflow-x: auto; o'
HTML += b'verflow-y: hidden; } .button-group { display: flex; align-it'
HTML += b'ems: center; justify-content: center; text-align: center; ma'
HTML += b'rgin-left: auto; margin-right: auto; }  @media (min-width: 8'
HTML += b'00px) { .question { border-radius: 12px; padding: 16px; marg'
HTML += b'in: 16px; } }  .questionFeedback { opacity: 1.8; z-index: 10'
HTML += b'; display: none; position: absolute; pointer-events: none; l'
HTML += b'eft: 0%; top: 0%; width: 100%; height: 100%; text-align: cen'
HTML += b'ter; font-size: 4vw; text-shadow: 0px 0px 18px rgba(0, 0, 0,'
HTML += b' 0.15); background-color: rgba(255, 255, 255, 0.95); padding'
HTML += b': 10px; justify-content: center; align-items: center; /*padd'
HTML += b'ing-top: 20px; padding-bottom: 20px;*/ /*border-style: solid'
HTML += b'; border-width: 4px; border-color: rgb(200, 200, 200); borde'
HTML += b'r-radius: 16px; -webkit-box-shadow: 0px 0px 18px 5px rgba(0,'
HTML += b' 0, 0, 0.66); box-shadow: 0px 0px 18px 5px rgba(0, 0, 0, 0.6'
HTML += b'6);*/ } .questionTitle { user-select: none; font-size: 24pt;'
HTML += b' } .code { font-family: "Courier New", Courier, monospace; c'
HTML += b'olor: black; background-color: rgb(235, 235, 235); padding: '
HTML += b'2px 5px; border-radius: 5px; margin: 1px 2px; } .debugCode {'
HTML += b' font-family: "Courier New", Courier, monospace; padding: 4p'
HTML += b'x; margin-bottom: 5px; background-color: black; color: white'
HTML += b'; border-radius: 5px; opacity: 0.85; overflow-x: scroll; } .'
HTML += b'debugInfo { text-align: end; font-size: 10pt; margin-top: 2p'
HTML += b'x; color: rgb(64, 64, 64); } ul { user-select: none; margin-'
HTML += b'top: 0; margin-left: 0px; padding-left: 20px; } .inputField '
HTML += b'{ position: relative; width: 32px; height: 24px; font-size: '
HTML += b'14pt; border-style: solid; border-color: black; border-radiu'
HTML += b's: 5px; border-width: 0.2; padding-left: 5px; padding-right:'
HTML += b' 5px; outline-color: black; background-color: transparent; m'
HTML += b'argin: 1px; } .inputField:focus { outline-color: maroon; } .'
HTML += b'equationPreview { position: absolute; top: 120%; left: 0%; p'
HTML += b'adding-left: 8px; padding-right: 8px; padding-top: 4px; padd'
HTML += b'ing-bottom: 4px; background-color: rgb(128, 0, 0); border-ra'
HTML += b'dius: 5px; font-size: 12pt; color: white; text-align: start;'
HTML += b' z-index: 100; opacity: 0.95; } .button { padding-left: 8px;'
HTML += b' padding-right: 8px; padding-top: 5px; padding-bottom: 5px; '
HTML += b'font-size: 12pt; background-color: rgb(0, 150, 0); color: wh'
HTML += b'ite; border-style: none; border-radius: 4px; height: 36px; c'
HTML += b'ursor: pointer; } .buttonRow { display: flex; align-items: b'
HTML += b'aseline; margin-top: 12px; } .matrixResizeButton { width: 20'
HTML += b'px; background-color: black; color: #fff; text-align: center'
HTML += b'; border-radius: 3px; position: absolute; z-index: 1; height'
HTML += b': 20px; cursor: pointer; margin-bottom: 3px; } a { color: bl'
HTML += b'ack; text-decoration: underline; } .timer { display: none; p'
HTML += b'osition: fixed; left: 0; top: 0; padding: 5px 15px; backgrou'
HTML += b'nd-color: rgb(32, 32, 32); color: white; opacity: 1; font-si'
HTML += b'ze: 32pt; z-index: 1000; /*margin: 2px; border-radius: 10px;'
HTML += b'*/ border-bottom-right-radius: 10px; text-align: center; fon'
HTML += b't-family: "Courier New", Courier, monospace; } .eval { text-'
HTML += b'align: center; } </style> </head> <body> <div id="timer" cla'
HTML += b'ss="timer">02:34</div> <h1 id="title"></h1> <div style="marg'
HTML += b'in-top: 15px"></div> <div class="author" id="author"></div> '
HTML += b'<p id="courseInfo1" class="courseInfo"></p> <p id="courseInf'
HTML += b'o2" class="courseInfo"></p> <h1 id="debug" class="debugCode"'
HTML += b' style="display: none">DEBUG VERSION</h1>  <br />  <div clas'
HTML += b's="contents"> <div id="questions"></div>  <div id="stop-now"'
HTML += b' class="eval" style="display: none"> <button id="stop-now-bt'
HTML += b'n" class="button" style="background-color: var(--green)" > j'
HTML += b'etzt auswerten (TODO: translate) </button> </div>  <div id="'
HTML += b'questions-eval" class="eval" style="display: none"> <br /> <'
HTML += b'h2 id="questions-eval-text"></h2> <h1 id="questions-eval-per'
HTML += b'centage">0 %</h1> </div> </div>  <br /><br /><br /><br />  <'
HTML += b'div class="footer"> <div class="contents"> <span id="date"><'
HTML += b'/span> &mdash; This quiz was developed using pySELL, a <a hr'
HTML += b'ef="https://pysell.org" style="text-decoration: none; color:'
HTML += b' white" >Python-based Simple E-Learning Language </a> &mdash'
HTML += b'; <a href="https://pysell.org" style="color: white">https://'
HTML += b'pysell.org</a> <br /> <span style="width: 64px"> <img style='
HTML += b'"max-width: 48px; padding: 16px 0px" src="data:image/svg+xml'
HTML += b';base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4K'
HTML += b'PCEtLSBDcmVhdGVkIHdpdGggSW5rc2NhcGUgKGh0dHA6Ly93d3cuaW5rc2Nh'
HTML += b'cGUub3JnLykgLS0+Cjxzdmcgd2lkdGg9IjEwMG1tIiBoZWlnaHQ9IjEwMG1t'
HTML += b'IiB2ZXJzaW9uPSIxLjEiIHZpZXdCb3g9IjAgMCAxMDAgMTAwIiB4bWxucz0i'
HTML += b'aHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRw'
HTML += b'Oi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIj4KIDxkZWZzPgogIDxsaW5lYXJH'
HTML += b'cmFkaWVudCBpZD0ibGluZWFyR3JhZGllbnQzNjU4IiB4MT0iMjguNTI3IiB4'
HTML += b'Mj0iMTI4LjUzIiB5MT0iNzkuNjQ4IiB5Mj0iNzkuNjQ4IiBncmFkaWVudFRy'
HTML += b'YW5zZm9ybT0ibWF0cml4KDEuMDE2MSAwIDAgMS4wMTYxIC0yOS43OSAtMzAu'
HTML += b'OTI4KSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgogICA8c3Rv'
HTML += b'cCBzdG9wLWNvbG9yPSIjNTkwMDVlIiBvZmZzZXQ9IjAiLz4KICAgPHN0b3Ag'
HTML += b'c3RvcC1jb2xvcj0iI2FkMDA3ZiIgb2Zmc2V0PSIxIi8+CiAgPC9saW5lYXJH'
HTML += b'cmFkaWVudD4KIDwvZGVmcz4KIDxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0i'
HTML += b'MTAwIiByeT0iMCIgZmlsbD0idXJsKCNsaW5lYXJHcmFkaWVudDM2NTgpIi8+'
HTML += b'CiA8ZyBmaWxsPSIjZmZmIj4KICA8ZyB0cmFuc2Zvcm09Im1hdHJpeCguNDA3'
HTML += b'NDMgMCAwIC40MDc0MyAtNDIuODQyIC0zNi4xMzYpIiBzdHJva2Utd2lkdGg9'
HTML += b'IjMuNzc5NSIgc3R5bGU9InNoYXBlLWluc2lkZTp1cmwoI3JlY3Q5NTItNyk7'
HTML += b'c2hhcGUtcGFkZGluZzo2LjUzMTQ0O3doaXRlLXNwYWNlOnByZSIgYXJpYS1s'
HTML += b'YWJlbD0iU0VMTCI+CiAgIDxwYXRoIGQ9Im0xNzEuMDEgMjM4LjM5cS0yLjEx'
HTML += b'Mi0yLjY4OC01LjU2OC00LjIyNC0zLjM2LTEuNjMyLTYuNTI4LTEuNjMyLTEu'
HTML += b'NjMyIDAtMy4zNiAwLjI4OC0xLjYzMiAwLjI4OC0yLjk3NiAxLjE1Mi0xLjM0'
HTML += b'NCAwLjc2OC0yLjMwNCAyLjExMi0wLjg2NCAxLjI0OC0wLjg2NCAzLjI2NCAw'
HTML += b'IDEuNzI4IDAuNjcyIDIuODggMC43NjggMS4xNTIgMi4xMTIgMi4wMTYgMS40'
HTML += b'NCAwLjg2NCAzLjM2IDEuNjMyIDEuOTIgMC42NzIgNC4zMiAxLjQ0IDMuNDU2'
HTML += b'IDEuMTUyIDcuMiAyLjU5MiAzLjc0NCAxLjM0NCA2LjgxNiAzLjY0OHQ1LjA4'
HTML += b'OCA1Ljc2cTIuMDE2IDMuMzYgMi4wMTYgOC40NDggMCA1Ljg1Ni0yLjIwOCAx'
HTML += b'MC4xNzYtMi4xMTIgNC4yMjQtNS43NiA3LjAwOHQtOC4zNTIgNC4xMjgtOS42'
HTML += b'OTYgMS4zNDRxLTcuMjk2IDAtMTQuMTEyLTIuNDk2LTYuODE2LTIuNTkyLTEx'
HTML += b'LjMyOC03LjI5NmwxMC43NTItMTAuOTQ0cTIuNDk2IDMuMDcyIDYuNTI4IDUu'
HTML += b'MTg0IDQuMTI4IDIuMDE2IDguMTYgMi4wMTYgMS44MjQgMCAzLjU1Mi0wLjM4'
HTML += b'NHQyLjk3Ni0xLjI0OHExLjM0NC0wLjg2NCAyLjExMi0yLjMwNHQwLjc2OC0z'
HTML += b'LjQ1NnEwLTEuOTItMC45Ni0zLjI2NHQtMi43ODQtMi40cS0xLjcyOC0xLjE1'
HTML += b'Mi00LjQxNi0yLjAxNi0yLjU5Mi0wLjk2LTUuOTUyLTIuMDE2LTMuMjY0LTEu'
HTML += b'MDU2LTYuNDMyLTIuNDk2LTMuMDcyLTEuNDQtNS41NjgtMy42NDgtMi40LTIu'
HTML += b'MzA0LTMuOTM2LTUuNDcyLTEuNDQtMy4yNjQtMS40NC03Ljg3MiAwLTUuNjY0'
HTML += b'IDIuMzA0LTkuNjk2dDYuMDQ4LTYuNjI0IDguNDQ4LTMuNzQ0cTQuNzA0LTEu'
HTML += b'MjQ4IDkuNTA0LTEuMjQ4IDUuNzYgMCAxMS43MTIgMi4xMTIgNi4wNDggMi4x'
HTML += b'MTIgMTAuNTYgNi4yNHoiLz4KICAgPHBhdGggZD0ibTE5MS44NCAyODguN3Yt'
HTML += b'NjcuOTY4aDUyLjE5bC0xLjI5ODggMTMuOTJoLTM1LjA1MXYxMi43NjhoMzMu'
HTML += b'NDE5bC0xLjI5ODggMTMuMTUyaC0zMi4xMnYxNC4xMTJoMzEuNTg0bC0xLjI5'
HTML += b'ODggMTQuMDE2eiIvPgogIDwvZz4KICA8ZyB0cmFuc2Zvcm09Im1hdHJpeCgu'
HTML += b'NDA3NDMgMCAwIC40MDc0MyAtNDAuMTY4IC03OC4wODIpIiBzdHJva2Utd2lk'
HTML += b'dGg9IjMuNzc5NSIgc3R5bGU9InNoYXBlLWluc2lkZTp1cmwoI3JlY3Q5NTIt'
HTML += b'OS05KTtzaGFwZS1wYWRkaW5nOjYuNTMxNDQ7d2hpdGUtc3BhY2U6cHJlIiBh'
HTML += b'cmlhLWxhYmVsPSJweSI+CiAgIDxwYXRoIGQ9Im0xODcuNDMgMjY0LjZxMCA0'
HTML += b'Ljk5Mi0xLjUzNiA5LjZ0LTQuNTEyIDguMTZxLTIuODggMy40NTYtNy4xMDQg'
HTML += b'NS41Njh0LTkuNiAyLjExMnEtNC40MTYgMC04LjM1Mi0xLjcyOC0zLjkzNi0x'
HTML += b'LjgyNC02LjE0NC00Ljg5NmgtMC4xOTJ2MjguMzJoLTE1Ljc0NHYtNzAuODQ4'
HTML += b'aDE0Ljk3NnY1Ljg1NmgwLjI4OHEyLjIwOC0yLjg4IDYuMDQ4LTQuOTkyIDMu'
HTML += b'OTM2LTIuMjA4IDkuMjE2LTIuMjA4IDUuMTg0IDAgOS40MDggMi4wMTZ0Ny4x'
HTML += b'MDQgNS40NzJxMi45NzYgMy40NTYgNC41MTIgOC4wNjQgMS42MzIgNC41MTIg'
HTML += b'MS42MzIgOS41MDR6bS0xNS4yNjQgMHEwLTIuMzA0LTAuNzY4LTQuNTEyLTAu'
HTML += b'NjcyLTIuMjA4LTIuMTEyLTMuODQtMS4zNDQtMS43MjgtMy40NTYtMi43ODR0'
HTML += b'LTQuODk2LTEuMDU2cS0yLjY4OCAwLTQuOCAxLjA1NnQtMy42NDggMi43ODRx'
HTML += b'LTEuNDQgMS43MjgtMi4zMDQgMy45MzYtMC43NjggMi4yMDgtMC43NjggNC41'
HTML += b'MTJ0MC43NjggNC41MTJxMC44NjQgMi4yMDggMi4zMDQgMy45MzYgMS41MzYg'
HTML += b'MS43MjggMy42NDggMi43ODR0NC44IDEuMDU2cTIuNzg0IDAgNC44OTYtMS4w'
HTML += b'NTZ0My40NTYtMi43ODRxMS40NC0xLjcyOCAyLjExMi0zLjkzNiAwLjc2OC0y'
HTML += b'LjMwNCAwLjc2OC00LjYwOHoiLz4KICAgPHBhdGggZD0ibTIyNC4yOSAyOTUu'
HTML += b'OXEtMS40NCAzLjc0NC0zLjI2NCA2LjYyNC0xLjcyOCAyLjk3Ni00LjIyNCA0'
HTML += b'Ljk5Mi0yLjQgMi4xMTItNS43NiAzLjE2OC0zLjI2NCAxLjA1Ni03Ljc3NiAx'
HTML += b'LjA1Ni0yLjIwOCAwLTQuNjA4LTAuMjg4LTIuMzA0LTAuMjg4LTQuMDMyLTAu'
HTML += b'NzY4bDEuNzI4LTEzLjI0OHExLjE1MiAwLjM4NCAyLjQ5NiAwLjU3NiAxLjQ0'
HTML += b'IDAuMjg4IDIuNTkyIDAuMjg4IDMuNjQ4IDAgNS4yOC0xLjcyOCAxLjYzMi0x'
HTML += b'LjYzMiAyLjc4NC00LjcwNGwxLjUzNi0zLjkzNi0xOS45NjgtNDcuMDRoMTcu'
HTML += b'NDcybDEwLjY1NiAzMC43MmgwLjI4OGw5LjUwNC0zMC43MmgxNi43MDR6Ii8+'
HTML += b'CiAgPC9nPgogIDxwYXRoIGQ9Im02OC4wOTYgMTUuNzc1aDcuODAyOWwtOC45'
HTML += b'ODU0IDY5Ljc5MWgtNy44MDN6IiBzdHJva2Utd2lkdGg9IjEuMTE3NiIvPgog'
HTML += b'IDxwYXRoIGQ9Im04My44NTMgMTUuNzQ4aDcuODAzbC04Ljk4NTQgNjkuNzkx'
HTML += b'aC03LjgwM3oiIHN0cm9rZS13aWR0aD0iMS4xMTc2Ii8+CiA8L2c+Cjwvc3Zn'
HTML += b'Pgo=" /> </span> <span id="data-policy"></span> </div> </div'
HTML += b'>  <script>let debug = false; let quizSrc = {};var sell=(()='
HTML += b'>{var R=Object.defineProperty;var oe=Object.getOwnPropertyDe'
HTML += b'scriptor;var ce=Object.getOwnPropertyNames;var he=Object.pro'
HTML += b'totype.hasOwnProperty;var pe=(a,e)=>{for(var t in e)R(a,t,{g'
HTML += b'et:e[t],enumerable:!0})},de=(a,e,t,i)=>{if(e&&typeof e=="obj'
HTML += b'ect"||typeof e=="function")for(let s of ce(e))!he.call(a,s)&'
HTML += b'&s!==t&&R(a,s,{get:()=>e[s],enumerable:!(i=oe(e,s))||i.enume'
HTML += b'rable});return a};var ue=a=>de(R({},"__esModule",{value:!0})'
HTML += b',a);var ge={};pe(ge,{init:()=>fe});function w(a=[]){let e=do'
HTML += b'cument.createElement("div");return e.append(...a),e}function'
HTML += b' U(a=[]){let e=document.createElement("ul");return e.append('
HTML += b'...a),e}function j(a){let e=document.createElement("li");ret'
HTML += b'urn e.appendChild(a),e}function W(a){let e=document.createEl'
HTML += b'ement("input");return e.spellcheck=!1,e.type="text",e.classL'
HTML += b'ist.add("inputField"),e.style.width=a+"px",e}function F(){le'
HTML += b't a=document.createElement("button");return a.type="button",'
HTML += b'a.classList.add("button"),a}function k(a,e=[]){let t=documen'
HTML += b't.createElement("span");return e.length>0?t.append(...e):t.i'
HTML += b'nnerHTML=a,t}function z(a,e,t=!1){katex.render(e,a,{throwOnE'
HTML += b'rror:!1,displayMode:t,macros:{"\\\\RR":"\\\\mathbb{R}","\\\\NN":"\\'
HTML += b'\\mathbb{N}","\\\\QQ":"\\\\mathbb{Q}","\\\\ZZ":"\\\\mathbb{Z}","\\\\CC"'
HTML += b':"\\\\mathbb{C}"}})}function T(a,e=!1){let t=document.createEl'
HTML += b'ement("span");return z(t,a,e),t}function O(a,e){let t=Array('
HTML += b'e.length+1).fill(null).map(()=>Array(a.length+1).fill(null))'
HTML += b';for(let i=0;i<=a.length;i+=1)t[0][i]=i;for(let i=0;i<=e.len'
HTML += b'gth;i+=1)t[i][0]=i;for(let i=1;i<=e.length;i+=1)for(let s=1;'
HTML += b's<=a.length;s+=1){let c=a[s-1]===e[i-1]?0:1;t[i][s]=Math.min'
HTML += b'(t[i][s-1]+1,t[i-1][s]+1,t[i-1][s-1]+c)}return t[e.length][a'
HTML += b'.length]}var q=\'<svg xmlns="http://www.w3.org/2000/svg" heig'
HTML += b'ht="28" viewBox="0 0 448 512"><path d="M384 80c8.8 0 16 7.2 '
HTML += b'16 16V416c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V96c0-8.8'
HTML += b' 7.2-16 16-16H384zM64 32C28.7 32 0 60.7 0 96V416c0 35.3 28.7'
HTML += b' 64 64 64H384c35.3 0 64-28.7 64-64V96c0-35.3-28.7-64-64-64H6'
HTML += b'4z"/></svg>\',K=\'<svg xmlns="http://www.w3.org/2000/svg" heig'
HTML += b'ht="28" viewBox="0 0 448 512"><path d="M64 80c-8.8 0-16 7.2-'
HTML += b'16 16V416c0 8.8 7.2 16 16 16H384c8.8 0 16-7.2 16-16V96c0-8.8'
HTML += b'-7.2-16-16-16H64zM0 96C0 60.7 28.7 32 64 32H384c35.3 0 64 28'
HTML += b'.7 64 64V416c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V9'
HTML += b'6zM337 209L209 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-'
HTML += b'9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L303 175c9.4-9.4 24.6-9'
HTML += b'.4 33.9 0s9.4 24.6 0 33.9z"/>\',X=\'<svg xmlns="http://www.w3.'
HTML += b'org/2000/svg" height="28" viewBox="0 0 512 512"><path d="M46'
HTML += b'4 256A208 208 0 1 0 48 256a208 208 0 1 0 416 0zM0 256a256 25'
HTML += b'6 0 1 1 512 0A256 256 0 1 1 0 256z"/></svg>\',Z=\'<svg xmlns="'
HTML += b'http://www.w3.org/2000/svg" height="28" viewBox="0 0 512 512'
HTML += b'"><path d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm'
HTML += b'0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209c9.4-9'
HTML += b'.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-111 111-47-47c-9.4-9.4-'
HTML += b'24.6-9.4-33.9 0s-9.4 24.6 0 33.9l64 64c9.4 9.4 24.6 9.4 33.9'
HTML += b' 0L369 209z"/></svg>\',I=\'<svg xmlns="http://www.w3.org/2000/'
HTML += b'svg" width="50" height="25" viewBox="0 0 384 512" fill="whit'
HTML += b'e"><path d="M73 39c-14.8-9.1-33.4-9.4-48.5-.9S0 62.6 0 80V43'
HTML += b'2c0 17.4 9.4 33.4 24.5 41.9s33.7 8.1 48.5-.9L361 297c14.3-8.'
HTML += b'7 23-24.2 23-41s-8.7-32.2-23-41L73 39z"/></svg>\',Y=\'<svg xml'
HTML += b'ns="http://www.w3.org/2000/svg" width="50" height="25" viewB'
HTML += b'ox="0 0 512 512" fill="white"><path d="M0 224c0 17.7 14.3 32'
HTML += b' 32 32s32-14.3 32-32c0-53 43-96 96-96H320v32c0 12.9 7.8 24.6'
HTML += b' 19.8 29.6s25.7 2.2 34.9-6.9l64-64c12.5-12.5 12.5-32.8 0-45.'
HTML += b'3l-64-64c-9.2-9.2-22.9-11.9-34.9-6.9S320 19.1 320 32V64H160C'
HTML += b'71.6 64 0 135.6 0 224zm512 64c0-17.7-14.3-32-32-32s-32 14.3-'
HTML += b'32 32c0 53-43 96-96 96H192V352c0-12.9-7.8-24.6-19.8-29.6s-25'
HTML += b'.7-2.2-34.9 6.9l-64 64c-12.5 12.5-12.5 32.8 0 45.3l64 64c9.2'
HTML += b' 9.2 22.9 11.9 34.9 6.9s19.8-16.6 19.8-29.6V448H352c88.4 0 1'
HTML += b'60-71.6 160-160z"/></svg>\';var G={en:"This page operates ent'
HTML += b'irely in your browser and does not store any data on externa'
HTML += b'l servers.",de:"Diese Seite wird in Ihrem Browser ausgef\\xFC'
HTML += b'hrt und speichert keine Daten auf Servern.",es:"Esta p\\xE1gi'
HTML += b'na se ejecuta en su navegador y no almacena ning\\xFAn dato e'
HTML += b'n los servidores.",it:"Questa pagina viene eseguita nel brow'
HTML += b'ser e non memorizza alcun dato sui server.",fr:"Cette page f'
HTML += b'onctionne dans votre navigateur et ne stocke aucune donn\\xE9'
HTML += b'e sur des serveurs."},J={en:"* this page to receive a new se'
HTML += b't of randomized tasks.",de:"Sie k\\xF6nnen diese Seite *, um '
HTML += b'neue randomisierte Aufgaben zu erhalten.",es:"Puedes * esta '
HTML += b'p\\xE1gina para obtener nuevas tareas aleatorias.",it:"\\xC8 p'
HTML += b'ossibile * questa pagina per ottenere nuovi compiti randomiz'
HTML += b'zati",fr:"Vous pouvez * cette page pour obtenir de nouvelles'
HTML += b' t\\xE2ches al\\xE9atoires"},$={en:"Refresh",de:"aktualisieren'
HTML += b'",es:"recargar",it:"ricaricare",fr:"recharger"},ee={en:["awe'
HTML += b'some","great","well done","nice","you got it","good"],de:["s'
HTML += b'uper","gut gemacht","weiter so","richtig"],es:["impresionant'
HTML += b'e","genial","correcto","bien hecho"],it:["fantastico","grand'
HTML += b'e","corretto","ben fatto"],fr:["g\\xE9nial","super","correct"'
HTML += b',"bien fait"]},te={en:["please complete all fields"],de:["bi'
HTML += b'tte alles ausf\\xFCllen"],es:["por favor, rellene todo"],it:['
HTML += b'"compilare tutto"],fr:["remplis tout s\'il te plait"]},se={en'
HTML += b':["try again","still some mistakes","wrong answer","no"],de:'
HTML += b'["leider falsch","nicht richtig","versuch\'s nochmal"],es:["i'
HTML += b'nt\\xE9ntalo de nuevo","todav\\xEDa algunos errores","respuest'
HTML += b'a incorrecta"],it:["riprova","ancora qualche errore","rispos'
HTML += b'ta sbagliata"],fr:["r\\xE9essayer","encore des erreurs","mauv'
HTML += b'aise r\\xE9ponse"]},ie={en:"Evaluation",de:"Auswertung",es:"E'
HTML += b'valuaci\\xF3n",it:"Valutazione",fr:"\\xC9valuation"},ne={en:"E'
HTML += b'valuate now",de:"Jetzt auswerten",es:"Evaluar ahora",it:"Val'
HTML += b'uta ora",fr:"\\xC9valuer maintenant"},ae={en:"Data Policy: Th'
HTML += b'is website does not collect, store, or process any personal '
HTML += b'data on external servers. All functionality is executed loca'
HTML += b'lly in your browser, ensuring complete privacy. No cookies a'
HTML += b're used, and no data is transmitted to or from the server. Y'
HTML += b'our activity on this site remains entirely private and local'
HTML += b' to your device.",de:"Datenschutzrichtlinie: Diese Website s'
HTML += b'ammelt, speichert oder verarbeitet keine personenbezogenen D'
HTML += b'aten auf externen Servern. Alle Funktionen werden lokal in I'
HTML += b'hrem Browser ausgef\\xFChrt, um vollst\\xE4ndige Privatsph\\xE4'
HTML += b're zu gew\\xE4hrleisten. Es werden keine Cookies verwendet, u'
HTML += b'nd es werden keine Daten an den Server gesendet oder von die'
HTML += b'sem empfangen. Ihre Aktivit\\xE4t auf dieser Seite bleibt vol'
HTML += b'lst\\xE4ndig privat und lokal auf Ihrem Ger\\xE4t.",es:"Pol\\xE'
HTML += b'Dtica de datos: Este sitio web no recopila, almacena ni proc'
HTML += b'esa ning\\xFAn dato personal en servidores externos. Toda la '
HTML += b'funcionalidad se ejecuta localmente en su navegador, garanti'
HTML += b'zando una privacidad completa. No se utilizan cookies y no s'
HTML += b'e transmiten datos hacia o desde el servidor. Su actividad e'
HTML += b'n este sitio permanece completamente privada y local en su d'
HTML += b'ispositivo.",it:"Politica sui dati: Questo sito web non racc'
HTML += b'oglie, memorizza o elabora alcun dato personale su server es'
HTML += b'terni. Tutte le funzionalit\\xE0 vengono eseguite localmente '
HTML += b'nel tuo browser, garantendo una privacy completa. Non vengon'
HTML += b'o utilizzati cookie e nessun dato viene trasmesso da o verso'
HTML += b' il server. La tua attivit\\xE0 su questo sito rimane complet'
HTML += b'amente privata e locale sul tuo dispositivo.",fr:"Politique '
HTML += b'de confidentialit\\xE9: Ce site web ne collecte, ne stocke ni'
HTML += b' ne traite aucune donn\\xE9e personnelle sur des serveurs ext'
HTML += b'ernes. Toutes les fonctionnalit\\xE9s sont ex\\xE9cut\\xE9es lo'
HTML += b'calement dans votre navigateur, garantissant une confidentia'
HTML += b'lit\\xE9 totale. Aucun cookie n\\u2019est utilis\\xE9 et aucune'
HTML += b' donn\\xE9e n\\u2019est transmise vers ou depuis le serveur. V'
HTML += b'otre activit\\xE9 sur ce site reste enti\\xE8rement priv\\xE9e '
HTML += b'et locale sur votre appareil."};function P(a,e=!1){let t=new'
HTML += b' Array(a);for(let i=0;i<a;i++)t[i]=i;if(e)for(let i=0;i<a;i+'
HTML += b'+){let s=Math.floor(Math.random()*a),c=Math.floor(Math.rando'
HTML += b'm()*a),o=t[s];t[s]=t[c],t[c]=o}return t}function N(a,e,t=-1)'
HTML += b'{if(t<0&&(t=a.length),t==1){e.push([...a]);return}for(let i='
HTML += b'0;i<t;i++){N(a,e,t-1);let s=t%2==0?i:0,c=a[s];a[s]=a[t-1],a['
HTML += b't-1]=c}}var E=class a{constructor(e,t){this.m=e,this.n=t,thi'
HTML += b's.v=new Array(e*t).fill("0")}getElement(e,t){return e<0||e>='
HTML += b'this.m||t<0||t>=this.n?"":this.v[e*this.n+t]}resize(e,t,i){i'
HTML += b'f(e<1||e>50||t<1||t>50)return!1;let s=new a(e,t);s.v.fill(i)'
HTML += b';for(let c=0;c<s.m;c++)for(let o=0;o<s.n;o++)s.v[c*s.n+o]=th'
HTML += b'is.getElement(c,o);return this.fromMatrix(s),!0}fromMatrix(e'
HTML += b'){this.m=e.m,this.n=e.n,this.v=[...e.v]}fromString(e){this.m'
HTML += b'=e.split("],").length,this.v=e.replaceAll("[","").replaceAll'
HTML += b'("]","").split(",").map(t=>t.trim()),this.n=this.v.length/th'
HTML += b'is.m}getMaxCellStrlen(){let e=0;for(let t of this.v)t.length'
HTML += b'>e&&(e=t.length);return e}toTeXString(e=!1,t=!0){let i="";t?'
HTML += b'i+=e?"\\\\left[\\\\begin{array}":"\\\\begin{bmatrix}":i+=e?"\\\\left'
HTML += b'(\\\\begin{array}":"\\\\begin{pmatrix}",e&&(i+="{"+"c".repeat(th'
HTML += b'is.n-1)+"|c}");for(let s=0;s<this.m;s++){for(let c=0;c<this.'
HTML += b'n;c++){c>0&&(i+="&");let o=this.getElement(s,c);try{o=v.pars'
HTML += b'e(o).toTexString()}catch{}i+=o}i+="\\\\\\\\"}return t?i+=e?"\\\\en'
HTML += b'd{array}\\\\right]":"\\\\end{bmatrix}":i+=e?"\\\\end{array}\\\\right'
HTML += b')":"\\\\end{pmatrix}",i}},v=class a{constructor(){this.root=nu'
HTML += b'll,this.src="",this.token="",this.skippedWhiteSpace=!1,this.'
HTML += b'pos=0}clone(){let e=new a;return e.root=this.root.clone(),e}'
HTML += b'getVars(e,t="",i=null){if(i==null&&(i=this.root),i.op.starts'
HTML += b'With("var:")){let s=i.op.substring(4);(t.length==0||t.length'
HTML += b'>0&&s.startsWith(t))&&e.add(s)}for(let s of i.c)this.getVars'
HTML += b'(e,t,s)}setVars(e,t=null){t==null&&(t=this.root);for(let i o'
HTML += b'f t.c)this.setVars(e,i);if(t.op.startsWith("var:")){let i=t.'
HTML += b'op.substring(4);if(i in e){let s=e[i].clone();t.op=s.op,t.c='
HTML += b's.c,t.re=s.re,t.im=s.im}}}renameVar(e,t,i=null){i==null&&(i='
HTML += b'this.root);for(let s of i.c)this.renameVar(e,t,s);i.op.start'
HTML += b'sWith("var:")&&i.op.substring(4)===e&&(i.op="var:"+t)}eval(e'
HTML += b',t=null){let s=r.const(),c=0,o=0,l=null;switch(t==null&&(t=t'
HTML += b'his.root),t.op){case"const":s=t;break;case"+":case"-":case"*'
HTML += b'":case"/":case"^":{let n=this.eval(e,t.c[0]),h=this.eval(e,t'
HTML += b'.c[1]);switch(t.op){case"+":s.re=n.re+h.re,s.im=n.im+h.im;br'
HTML += b'eak;case"-":s.re=n.re-h.re,s.im=n.im-h.im;break;case"*":s.re'
HTML += b'=n.re*h.re-n.im*h.im,s.im=n.re*h.im+n.im*h.re;break;case"/":'
HTML += b'c=h.re*h.re+h.im*h.im,s.re=(n.re*h.re+n.im*h.im)/c,s.im=(n.i'
HTML += b'm*h.re-n.re*h.im)/c;break;case"^":l=new r("exp",[new r("*",['
HTML += b'h,new r("ln",[n])])]),s=this.eval(e,l);break}break}case".-":'
HTML += b'case"abs":case"acos":case"acosh":case"asin":case"asinh":case'
HTML += b'"atan":case"atanh":case"ceil":case"cos":case"cosh":case"cot"'
HTML += b':case"exp":case"floor":case"ln":case"log":case"log10":case"l'
HTML += b'og2":case"round":case"sin":case"sinc":case"sinh":case"sqrt":'
HTML += b'case"tan":case"tanh":{let n=this.eval(e,t.c[0]);switch(t.op)'
HTML += b'{case".-":s.re=-n.re,s.im=-n.im;break;case"abs":s.re=Math.sq'
HTML += b'rt(n.re*n.re+n.im*n.im),s.im=0;break;case"acos":l=new r("*",'
HTML += b'[r.const(0,-1),new r("ln",[new r("+",[r.const(0,1),new r("sq'
HTML += b'rt",[new r("-",[r.const(1,0),new r("*",[n,n])])])])])]),s=th'
HTML += b'is.eval(e,l);break;case"acosh":l=new r("*",[n,new r("sqrt",['
HTML += b'new r("-",[new r("*",[n,n]),r.const(1,0)])])]),s=this.eval(e'
HTML += b',l);break;case"asin":l=new r("*",[r.const(0,-1),new r("ln",['
HTML += b'new r("+",[new r("*",[r.const(0,1),n]),new r("sqrt",[new r("'
HTML += b'-",[r.const(1,0),new r("*",[n,n])])])])])]),s=this.eval(e,l)'
HTML += b';break;case"asinh":l=new r("*",[n,new r("sqrt",[new r("+",[n'
HTML += b'ew r("*",[n,n]),r.const(1,0)])])]),s=this.eval(e,l);break;ca'
HTML += b'se"atan":l=new r("*",[r.const(0,.5),new r("ln",[new r("/",[n'
HTML += b'ew r("-",[r.const(0,1),new r("*",[r.const(0,1),n])]),new r("'
HTML += b'+",[r.const(0,1),new r("*",[r.const(0,1),n])])])])]),s=this.'
HTML += b'eval(e,l);break;case"atanh":l=new r("*",[r.const(.5,0),new r'
HTML += b'("ln",[new r("/",[new r("+",[r.const(1,0),n]),new r("-",[r.c'
HTML += b'onst(1,0),n])])])]),s=this.eval(e,l);break;case"ceil":s.re=M'
HTML += b'ath.ceil(n.re),s.im=Math.ceil(n.im);break;case"cos":s.re=Mat'
HTML += b'h.cos(n.re)*Math.cosh(n.im),s.im=-Math.sin(n.re)*Math.sinh(n'
HTML += b'.im);break;case"cosh":l=new r("*",[r.const(.5,0),new r("+",['
HTML += b'new r("exp",[n]),new r("exp",[new r(".-",[n])])])]),s=this.e'
HTML += b'val(e,l);break;case"cot":c=Math.sin(n.re)*Math.sin(n.re)+Mat'
HTML += b'h.sinh(n.im)*Math.sinh(n.im),s.re=Math.sin(n.re)*Math.cos(n.'
HTML += b're)/c,s.im=-(Math.sinh(n.im)*Math.cosh(n.im))/c;break;case"e'
HTML += b'xp":s.re=Math.exp(n.re)*Math.cos(n.im),s.im=Math.exp(n.re)*M'
HTML += b'ath.sin(n.im);break;case"floor":s.re=Math.floor(n.re),s.im=M'
HTML += b'ath.floor(n.im);break;case"ln":case"log":s.re=Math.log(Math.'
HTML += b'sqrt(n.re*n.re+n.im*n.im)),c=Math.abs(n.im)<1e-9?0:n.im,s.im'
HTML += b'=Math.atan2(c,n.re);break;case"log10":l=new r("/",[new r("ln'
HTML += b'",[n]),new r("ln",[r.const(10)])]),s=this.eval(e,l);break;ca'
HTML += b'se"log2":l=new r("/",[new r("ln",[n]),new r("ln",[r.const(2)'
HTML += b'])]),s=this.eval(e,l);break;case"round":s.re=Math.round(n.re'
HTML += b'),s.im=Math.round(n.im);break;case"sin":s.re=Math.sin(n.re)*'
HTML += b'Math.cosh(n.im),s.im=Math.cos(n.re)*Math.sinh(n.im);break;ca'
HTML += b'se"sinc":l=new r("/",[new r("sin",[n]),n]),s=this.eval(e,l);'
HTML += b'break;case"sinh":l=new r("*",[r.const(.5,0),new r("-",[new r'
HTML += b'("exp",[n]),new r("exp",[new r(".-",[n])])])]),s=this.eval(e'
HTML += b',l);break;case"sqrt":l=new r("^",[n,r.const(.5)]),s=this.eva'
HTML += b'l(e,l);break;case"tan":c=Math.cos(n.re)*Math.cos(n.re)+Math.'
HTML += b'sinh(n.im)*Math.sinh(n.im),s.re=Math.sin(n.re)*Math.cos(n.re'
HTML += b')/c,s.im=Math.sinh(n.im)*Math.cosh(n.im)/c;break;case"tanh":'
HTML += b'l=new r("/",[new r("-",[new r("exp",[n]),new r("exp",[new r('
HTML += b'".-",[n])])]),new r("+",[new r("exp",[n]),new r("exp",[new r'
HTML += b'(".-",[n])])])]),s=this.eval(e,l);break}break}default:if(t.o'
HTML += b'p.startsWith("var:")){let n=t.op.substring(4);if(n==="pi")re'
HTML += b'turn r.const(Math.PI);if(n==="e")return r.const(Math.E);if(n'
HTML += b'==="i")return r.const(0,1);if(n==="true")return r.const(1);i'
HTML += b'f(n==="false")return r.const(0);if(n in e)return e[n];throw '
HTML += b'new Error("eval-error: unknown variable \'"+n+"\'")}else throw'
HTML += b' new Error("UNIMPLEMENTED eval \'"+t.op+"\'")}return s}static '
HTML += b'parse(e){let t=new a;if(t.src=e,t.token="",t.skippedWhiteSpa'
HTML += b'ce=!1,t.pos=0,t.next(),t.root=t.parseExpr(!1),t.token!=="")t'
HTML += b'hrow new Error("remaining tokens: "+t.token+"...");return t}'
HTML += b'parseExpr(e){return this.parseAdd(e)}parseAdd(e){let t=this.'
HTML += b'parseMul(e);for(;["+","-"].includes(this.token)&&!(e&&this.s'
HTML += b'kippedWhiteSpace);){let i=this.token;this.next(),t=new r(i,['
HTML += b't,this.parseMul(e)])}return t}parseMul(e){let t=this.parsePo'
HTML += b'w(e);for(;!(e&&this.skippedWhiteSpace);){let i="*";if(["*","'
HTML += b'/"].includes(this.token))i=this.token,this.next();else if(!e'
HTML += b'&&this.token==="(")i="*";else if(this.token.length>0&&(this.'
HTML += b'isAlpha(this.token[0])||this.isNum(this.token[0])))i="*";els'
HTML += b'e break;t=new r(i,[t,this.parsePow(e)])}return t}parsePow(e)'
HTML += b'{let t=this.parseUnary(e);for(;["^"].includes(this.token)&&!'
HTML += b'(e&&this.skippedWhiteSpace);){let i=this.token;this.next(),t'
HTML += b'=new r(i,[t,this.parseUnary(e)])}return t}parseUnary(e){retu'
HTML += b'rn this.token==="-"?(this.next(),new r(".-",[this.parseMul(e'
HTML += b')])):this.parseInfix(e)}parseInfix(e){if(this.token.length=='
HTML += b'0)throw new Error("expected unary");if(this.isNum(this.token'
HTML += b'[0])){let t=this.token;return this.next(),this.token==="."&&'
HTML += b'(t+=".",this.next(),this.token.length>0&&(t+=this.token,this'
HTML += b'.next())),new r("const",[],parseFloat(t))}else if(this.fun1('
HTML += b').length>0){let t=this.fun1();this.next(t.length);let i=null'
HTML += b';if(this.token==="(")if(this.next(),i=this.parseExpr(e),this'
HTML += b'.token+="",this.token===")")this.next();else throw Error("ex'
HTML += b'pected \')\'");else i=this.parseMul(!0);return new r(t,[i])}el'
HTML += b'se if(this.token==="("){this.next();let t=this.parseExpr(e);'
HTML += b'if(this.token+="",this.token===")")this.next();else throw Er'
HTML += b'ror("expected \')\'");return t.explicitParentheses=!0,t}else i'
HTML += b'f(this.token==="|"){this.next();let t=this.parseExpr(e);if(t'
HTML += b'his.token+="",this.token==="|")this.next();else throw Error('
HTML += b'"expected \'|\'");return new r("abs",[t])}else if(this.isAlpha'
HTML += b'(this.token[0])){let t="";return this.token.startsWith("pi")'
HTML += b'?t="pi":this.token.startsWith("true")?t="true":this.token.st'
HTML += b'artsWith("false")?t="false":this.token.startsWith("C1")?t="C'
HTML += b'1":this.token.startsWith("C2")?t="C2":t=this.token[0],t==="I'
HTML += b'"&&(t="i"),this.next(t.length),new r("var:"+t,[])}else throw'
HTML += b' new Error("expected unary")}static compare(e,t,i={}){let o='
HTML += b'new Set;e.getVars(o),t.getVars(o);for(let l=0;l<10;l++){let '
HTML += b'n={};for(let f of o)f in i?n[f]=i[f]:n[f]=r.const(Math.rando'
HTML += b'm(),Math.random());let h=e.eval(n),p=t.eval(n),m=h.re-p.re,u'
HTML += b'=h.im-p.im;if(Math.sqrt(m*m+u*u)>1e-9)return!1}return!0}fun1'
HTML += b'(){let e=["abs","acos","acosh","asin","asinh","atan","atanh"'
HTML += b',"ceil","cos","cosh","cot","exp","floor","ln","log","log10",'
HTML += b'"log2","round","sin","sinc","sinh","sqrt","tan","tanh"];for('
HTML += b'let t of e)if(this.token.toLowerCase().startsWith(t))return '
HTML += b't;return""}next(e=-1){if(e>0&&this.token.length>e){this.toke'
HTML += b'n=this.token.substring(e),this.skippedWhiteSpace=!1;return}t'
HTML += b'his.token="";let t=!1,i=this.src.length;for(this.skippedWhit'
HTML += b'eSpace=!1;this.pos<i&&`\t\n `.includes(this.src[this.pos]);)th'
HTML += b'is.skippedWhiteSpace=!0,this.pos++;for(;!t&&this.pos<i;){let'
HTML += b' s=this.src[this.pos];if(this.token.length>0&&(this.isNum(th'
HTML += b'is.token[0])&&this.isAlpha(s)||this.isAlpha(this.token[0])&&'
HTML += b'this.isNum(s))&&this.token!="C")return;if(`^%#*$()[]{},.:;+-'
HTML += b'*/_!<>=?|\t\n `.includes(s)){if(this.token.length>0)return;t=!'
HTML += b'0}`\t\n `.includes(s)==!1&&(this.token+=s),this.pos++}}isNum(e'
HTML += b'){return e.charCodeAt(0)>=48&&e.charCodeAt(0)<=57}isAlpha(e)'
HTML += b'{return e.charCodeAt(0)>=65&&e.charCodeAt(0)<=90||e.charCode'
HTML += b'At(0)>=97&&e.charCodeAt(0)<=122||e==="_"}toString(){return t'
HTML += b'his.root==null?"":this.root.toString()}toTexString(){return '
HTML += b'this.root==null?"":this.root.toTexString()}},r=class a{const'
HTML += b'ructor(e,t,i=0,s=0){this.op=e,this.c=t,this.re=i,this.im=s,t'
HTML += b'his.explicitParentheses=!1}clone(){let e=new a(this.op,this.'
HTML += b'c.map(t=>t.clone()),this.re,this.im);return e.explicitParent'
HTML += b'heses=this.explicitParentheses,e}static const(e=0,t=0){retur'
HTML += b'n new a("const",[],e,t)}compare(e,t=0,i=1e-9){let s=this.re-'
HTML += b'e,c=this.im-t;return Math.sqrt(s*s+c*c)<i}toString(){let e="'
HTML += b'";if(this.op==="const"){let t=Math.abs(this.re)>1e-14,i=Math'
HTML += b'.abs(this.im)>1e-14;t&&i&&this.im>=0?e="("+this.re+"+"+this.'
HTML += b'im+"i)":t&&i&&this.im<0?e="("+this.re+"-"+-this.im+"i)":t&&t'
HTML += b'his.re>0?e=""+this.re:t&&this.re<0?e="("+this.re+")":i?e="("'
HTML += b'+this.im+"i)":e="0"}else this.op.startsWith("var")?e=this.op'
HTML += b'.split(":")[1]:this.c.length==1?e=(this.op===".-"?"-":this.o'
HTML += b'p)+"("+this.c.toString()+")":e="("+this.c.map(t=>t.toString('
HTML += b')).join(this.op)+")";return e}toTexString(e=!1){let i="";swi'
HTML += b'tch(this.op){case"const":{let s=Math.abs(this.re)>1e-9,c=Mat'
HTML += b'h.abs(this.im)>1e-9,o=s?""+this.re:"",l=c?""+this.im+"i":"";'
HTML += b'l==="1i"?l="i":l==="-1i"&&(l="-i"),!s&&!c?i="0":(c&&this.im>'
HTML += b'=0&&s&&(l="+"+l),i=o+l);break}case".-":i="-"+this.c[0].toTex'
HTML += b'String();break;case"+":case"-":case"*":case"^":{let s=this.c'
HTML += b'[0].toTexString(),c=this.c[1].toTexString(),o=this.op==="*"?'
HTML += b'"\\\\cdot ":this.op;i="{"+s+"}"+o+"{"+c+"}";break}case"/":{let'
HTML += b' s=this.c[0].toTexString(!0),c=this.c[1].toTexString(!0);i="'
HTML += b'\\\\frac{"+s+"}{"+c+"}";break}case"floor":{let s=this.c[0].toT'
HTML += b'exString(!0);i+="\\\\"+this.op+"\\\\left\\\\lfloor"+s+"\\\\right\\\\rf'
HTML += b'loor";break}case"ceil":{let s=this.c[0].toTexString(!0);i+="'
HTML += b'\\\\"+this.op+"\\\\left\\\\lceil"+s+"\\\\right\\\\rceil";break}case"ro'
HTML += b'und":{let s=this.c[0].toTexString(!0);i+="\\\\"+this.op+"\\\\lef'
HTML += b't["+s+"\\\\right]";break}case"acos":case"acosh":case"asin":cas'
HTML += b'e"asinh":case"atan":case"atanh":case"cos":case"cosh":case"co'
HTML += b't":case"exp":case"ln":case"log":case"log10":case"log2":case"'
HTML += b'sin":case"sinc":case"sinh":case"tan":case"tanh":{let s=this.'
HTML += b'c[0].toTexString(!0);i+="\\\\"+this.op+"\\\\left("+s+"\\\\right)";'
HTML += b'break}case"sqrt":{let s=this.c[0].toTexString(!0);i+="\\\\"+th'
HTML += b'is.op+"{"+s+"}";break}case"abs":{let s=this.c[0].toTexString'
HTML += b'(!0);i+="\\\\left|"+s+"\\\\right|";break}default:if(this.op.star'
HTML += b'tsWith("var:")){let s=this.op.substring(4);switch(s){case"pi'
HTML += b'":s="\\\\pi";break}i=" "+s+" "}else{let s="warning: Node.toStr'
HTML += b'ing(..):";s+=" unimplemented operator \'"+this.op+"\'",console'
HTML += b'.log(s),i=this.op,this.c.length>0&&(i+="\\\\left({"+this.c.map'
HTML += b'(c=>c.toTexString(!0)).join(",")+"}\\\\right)")}}return!e&&thi'
HTML += b's.explicitParentheses&&(i="\\\\left({"+i+"}\\\\right)"),i}};func'
HTML += b'tion re(a,e){let t=1e-9;if(v.compare(a,e))return!0;a=a.clone'
HTML += b'(),e=e.clone(),_(a.root),_(e.root);let i=new Set;a.getVars(i'
HTML += b'),e.getVars(i);let s=[],c=[];for(let n of i.keys())n.startsW'
HTML += b'ith("C")?s.push(n):c.push(n);let o=s.length;for(let n=0;n<o;'
HTML += b'n++){let h=s[n];a.renameVar(h,"_C"+n),e.renameVar(h,"_C"+n)}'
HTML += b'for(let n=0;n<o;n++)a.renameVar("_C"+n,"C"+n),e.renameVar("_'
HTML += b'C"+n,"C"+n);s=[];for(let n=0;n<o;n++)s.push("C"+n);let l=[];'
HTML += b'N(P(o),l);for(let n of l){let h=a.clone(),p=e.clone();for(le'
HTML += b't u=0;u<o;u++)p.renameVar("C"+u,"__C"+n[u]);for(let u=0;u<o;'
HTML += b'u++)p.renameVar("__C"+u,"C"+u);let m=!0;for(let u=0;u<o;u++)'
HTML += b'{let d="C"+u,f={};f[d]=new r("*",[new r("var:C"+u,[]),new r('
HTML += b'"var:K",[])]),p.setVars(f);let g={};g[d]=r.const(Math.random'
HTML += b'(),Math.random());for(let x=0;x<o;x++)u!=x&&(g["C"+x]=r.cons'
HTML += b't(0,0));let C=new r("abs",[new r("-",[h.root,p.root])]),M=ne'
HTML += b'w v;M.root=C;for(let x of c)g[x]=r.const(Math.random(),Math.'
HTML += b'random());let y=me(M,"K",g)[0];p.setVars({K:r.const(y,0)}),g'
HTML += b'={};for(let x=0;x<o;x++)u!=x&&(g["C"+x]=r.const(0,0));if(v.c'
HTML += b'ompare(h,p,g)==!1){m=!1;break}}if(m&&v.compare(h,p))return!0'
HTML += b'}return!1}function me(a,e,t){let i=1e-11,s=1e3,c=0,o=0,l=1,n'
HTML += b'=888;for(;c<s;){t[e]=r.const(o);let p=a.eval(t).re;t[e]=r.co'
HTML += b'nst(o+l);let m=a.eval(t).re;t[e]=r.const(o-l);let u=a.eval(t'
HTML += b').re,d=0;if(m<p&&(p=m,d=1),u<p&&(p=u,d=-1),d==1&&(o+=l),d==-'
HTML += b'1&&(o-=l),p<i)break;(d==0||d!=n)&&(l/=2),n=d,c++}t[e]=r.cons'
HTML += b't(o);let h=a.eval(t).re;return[o,h]}function _(a){for(let e '
HTML += b'of a.c)_(e);switch(a.op){case"+":case"-":case"*":case"/":cas'
HTML += b'e"^":{let e=[a.c[0].op,a.c[1].op],t=[e[0]==="const",e[1]==="'
HTML += b'const"],i=[e[0].startsWith("var:C"),e[1].startsWith("var:C")'
HTML += b'];i[0]&&t[1]?(a.op=a.c[0].op,a.c=[]):i[1]&&t[0]?(a.op=a.c[1]'
HTML += b'.op,a.c=[]):i[0]&&i[1]&&e[0]==e[1]&&(a.op=a.c[0].op,a.c=[]);'
HTML += b'break}case".-":case"abs":case"sin":case"sinc":case"cos":case'
HTML += b'"tan":case"cot":case"exp":case"ln":case"log":case"sqrt":a.c['
HTML += b'0].op.startsWith("var:C")&&(a.op=a.c[0].op,a.c=[]);break}}va'
HTML += b'r A=class{constructor(e,t,i,s){this.question=t,this.inputId='
HTML += b'i,i.length==0&&(this.inputId=i="gap-"+t.gapIdx,t.types[this.'
HTML += b'inputId]="string",t.expected[this.inputId]=s,t.gapIdx++),i i'
HTML += b'n t.student||(t.student[i]="");let c=s.split("|"),o=0;for(le'
HTML += b't p=0;p<c.length;p++){let m=c[p];m.length>o&&(o=m.length)}le'
HTML += b't l=k("");e.appendChild(l);let n=Math.max(o*15,24),h=W(n);if'
HTML += b'(t.gapInputs[this.inputId]=h,h.addEventListener("keyup",()=>'
HTML += b'{this.question.editedQuestion(),h.value=h.value.toUpperCase('
HTML += b'),this.question.student[this.inputId]=h.value.trim()}),l.app'
HTML += b'endChild(h),this.question.showSolution&&(this.question.stude'
HTML += b'nt[this.inputId]=h.value=c[0],c.length>1)){let p=k("["+c.joi'
HTML += b'n("|")+"]");p.style.fontSize="small",p.style.textDecoration='
HTML += b'"underline",l.appendChild(p)}}},L=class{constructor(e,t,i,s,'
HTML += b'c,o,l=!1){i in t.student||(t.student[i]=""),this.question=t,'
HTML += b'this.inputId=i,this.outerSpan=k(""),this.outerSpan.style.pos'
HTML += b'ition="relative",e.appendChild(this.outerSpan),this.inputEle'
HTML += b'ment=W(Math.max(s*12,48)),this.outerSpan.appendChild(this.in'
HTML += b'putElement),this.equationPreviewDiv=w(),this.equationPreview'
HTML += b'Div.classList.add("equationPreview"),this.equationPreviewDiv'
HTML += b'.style.display="none",this.outerSpan.appendChild(this.equati'
HTML += b'onPreviewDiv),this.inputElement.addEventListener("click",()='
HTML += b'>{this.question.editedQuestion(),this.edited()}),this.inputE'
HTML += b'lement.addEventListener("keyup",()=>{this.question.editedQue'
HTML += b'stion(),this.edited()}),this.inputElement.addEventListener("'
HTML += b'focusout",()=>{this.equationPreviewDiv.innerHTML="",this.equ'
HTML += b'ationPreviewDiv.style.display="none"}),this.inputElement.add'
HTML += b'EventListener("keydown",n=>{let h="abcdefghijklmnopqrstuvwxy'
HTML += b'z";h+="ABCDEFGHIJKLMNOPQRSTUVWXYZ",h+="0123456789",h+="+-*/^'
HTML += b'(). <>=|",o&&(h="-0123456789"),n.key.length<3&&h.includes(n.'
HTML += b'key)==!1&&n.preventDefault();let p=this.inputElement.value.l'
HTML += b'ength*12;this.inputElement.offsetWidth<p&&(this.inputElement'
HTML += b'.style.width=""+p+"px")}),(l||this.question.showSolution)&&('
HTML += b't.student[i]=this.inputElement.value=c)}edited(){let e=this.'
HTML += b'inputElement.value.trim(),t="",i=!1;try{let s=v.parse(e);i=s'
HTML += b'.root.op==="const",t=s.toTexString(),this.inputElement.style'
HTML += b'.color="black",this.equationPreviewDiv.style.backgroundColor'
HTML += b'="green"}catch{t=e.replaceAll("^","\\\\hat{~}").replaceAll("_"'
HTML += b',"\\\\_"),this.inputElement.style.color="maroon",this.equation'
HTML += b'PreviewDiv.style.backgroundColor="maroon"}z(this.equationPre'
HTML += b'viewDiv,t,!0),this.equationPreviewDiv.style.display=e.length'
HTML += b'>0&&!i?"block":"none",this.question.student[this.inputId]=e}'
HTML += b'},B=class{constructor(e,t,i,s){this.parent=e,this.question=t'
HTML += b',this.inputId=i,this.matExpected=new E(0,0),this.matExpected'
HTML += b'.fromString(s),this.matStudent=new E(this.matExpected.m==1?1'
HTML += b':3,this.matExpected.n==1?1:3),t.showSolution&&this.matStuden'
HTML += b't.fromMatrix(this.matExpected),this.genMatrixDom(!0)}genMatr'
HTML += b'ixDom(e){let t=w();this.parent.innerHTML="",this.parent.appe'
HTML += b'ndChild(t),t.style.position="relative",t.style.display="inli'
HTML += b'ne-block";let i=document.createElement("table");t.appendChil'
HTML += b'd(i);let s=this.matExpected.getMaxCellStrlen();for(let d=0;d'
HTML += b'<this.matStudent.m;d++){let f=document.createElement("tr");i'
HTML += b'.appendChild(f),d==0&&f.appendChild(this.generateMatrixParen'
HTML += b'thesis(!0,this.matStudent.m));for(let g=0;g<this.matStudent.'
HTML += b'n;g++){let C=d*this.matStudent.n+g,M=document.createElement('
HTML += b'"td");f.appendChild(M);let y=this.inputId+"-"+C;new L(M,this'
HTML += b'.question,y,s,this.matStudent.v[C],!1,!e)}d==0&&f.appendChil'
HTML += b'd(this.generateMatrixParenthesis(!1,this.matStudent.m))}let '
HTML += b'c=["+","-","+","-"],o=[0,0,1,-1],l=[1,-1,0,0],n=[0,22,888,88'
HTML += b'8],h=[888,888,-22,-22],p=[-22,-22,0,22],m=[this.matExpected.'
HTML += b'n!=1,this.matExpected.n!=1,this.matExpected.m!=1,this.matExp'
HTML += b'ected.m!=1],u=[this.matStudent.n>=10,this.matStudent.n<=1,th'
HTML += b'is.matStudent.m>=10,this.matStudent.m<=1];for(let d=0;d<4;d+'
HTML += b'+){if(m[d]==!1)continue;let f=k(c[d]);n[d]!=888&&(f.style.to'
HTML += b'p=""+n[d]+"px"),h[d]!=888&&(f.style.bottom=""+h[d]+"px"),p[d'
HTML += b']!=888&&(f.style.right=""+p[d]+"px"),f.classList.add("matrix'
HTML += b'ResizeButton"),t.appendChild(f),u[d]?f.style.opacity="0.5":f'
HTML += b'.addEventListener("click",()=>{for(let g=0;g<this.matStudent'
HTML += b'.m;g++)for(let C=0;C<this.matStudent.n;C++){let M=g*this.mat'
HTML += b'Student.n+C,y=this.inputId+"-"+M,S=this.question.student[y];'
HTML += b'this.matStudent.v[M]=S,delete this.question.student[y]}this.'
HTML += b'matStudent.resize(this.matStudent.m+o[d],this.matStudent.n+l'
HTML += b'[d],""),this.genMatrixDom(!1)})}}generateMatrixParenthesis(e'
HTML += b',t){let i=document.createElement("td");i.style.width="3px";f'
HTML += b'or(let s of["Top",e?"Left":"Right","Bottom"])i.style["border'
HTML += b'"+s+"Width"]="2px",i.style["border"+s+"Style"]="solid";retur'
HTML += b'n this.question.language=="de"&&(e?i.style.borderTopLeftRadi'
HTML += b'us="5px":i.style.borderTopRightRadius="5px",e?i.style.border'
HTML += b'BottomLeftRadius="5px":i.style.borderBottomRightRadius="5px"'
HTML += b'),i.rowSpan=t,i}};var b={init:0,errors:1,passed:2,incomplete'
HTML += b':3},H=class{constructor(e,t,i,s){this.state=b.init,this.lang'
HTML += b'uage=i,this.src=t,this.debug=s,this.instanceOrder=P(t.instan'
HTML += b'ces.length,!0),this.instanceIdx=0,this.choiceIdx=0,this.incl'
HTML += b'udesSingleChoice=!1,this.gapIdx=0,this.expected={},this.type'
HTML += b's={},this.student={},this.gapInputs={},this.parentDiv=e,this'
HTML += b'.questionDiv=null,this.feedbackPopupDiv=null,this.titleDiv=n'
HTML += b'ull,this.checkAndRepeatBtn=null,this.showSolution=!1,this.fe'
HTML += b'edbackSpan=null,this.numCorrect=0,this.numChecked=0,this.has'
HTML += b'CheckButton=!0}reset(){this.gapIdx=0,this.choiceIdx=0,this.i'
HTML += b'nstanceIdx=(this.instanceIdx+1)%this.src.instances.length}ge'
HTML += b'tCurrentInstance(){let e=this.instanceOrder[this.instanceIdx'
HTML += b'];return this.src.instances[e]}editedQuestion(){this.state=b'
HTML += b'.init,this.updateVisualQuestionState(),this.questionDiv.styl'
HTML += b'e.color="black",this.checkAndRepeatBtn.innerHTML=I,this.chec'
HTML += b'kAndRepeatBtn.style.display="block",this.checkAndRepeatBtn.s'
HTML += b'tyle.color="black"}updateVisualQuestionState(){let e="black"'
HTML += b',t="transparent";switch(this.state){case b.init:e="white";br'
HTML += b'eak;case b.passed:e="var(--green)",t="rgba(0,150,0, 0.035)";'
HTML += b'break;case b.incomplete:case b.errors:e="var(--red)",t="rgba'
HTML += b'(150,0,0, 0.035)",this.includesSingleChoice==!1&&this.numChe'
HTML += b'cked>=5&&(this.feedbackSpan.innerHTML="&nbsp;&nbsp;"+this.nu'
HTML += b'mCorrect+" / "+this.numChecked);break}this.questionDiv.style'
HTML += b'.backgroundColor=t,this.questionDiv.style.borderColor=e,this'
HTML += b'.questionDiv.style.borderWidth="6px"}populateDom(e=!1){if(th'
HTML += b'is.parentDiv.innerHTML="",this.questionDiv=w(),this.parentDi'
HTML += b'v.appendChild(this.questionDiv),this.questionDiv.classList.a'
HTML += b'dd("question"),this.feedbackPopupDiv=w(),this.feedbackPopupD'
HTML += b'iv.classList.add("questionFeedback"),this.questionDiv.append'
HTML += b'Child(this.feedbackPopupDiv),this.feedbackPopupDiv.innerHTML'
HTML += b'="awesome",this.debug&&"src_line"in this.src){let s=w();s.cl'
HTML += b'assList.add("debugInfo"),s.innerHTML="Source code: lines "+t'
HTML += b'his.src.src_line+"..",this.questionDiv.appendChild(s)}if(thi'
HTML += b's.titleDiv=w(),this.questionDiv.appendChild(this.titleDiv),t'
HTML += b'his.titleDiv.classList.add("questionTitle"),this.titleDiv.in'
HTML += b'nerHTML=this.src.title,this.src.error.length>0){let s=k(this'
HTML += b'.src.error);this.questionDiv.appendChild(s),s.style.color="r'
HTML += b'ed";return}let t=this.getCurrentInstance();if(t!=null&&"__sv'
HTML += b'g_image"in t){let s=t.__svg_image.v,c=w();this.questionDiv.a'
HTML += b'ppendChild(c);let o=document.createElement("img");c.appendCh'
HTML += b'ild(o),o.classList.add("img"),o.src="data:image/svg+xml;base'
HTML += b'64,"+s}for(let s of this.src.text.c)this.questionDiv.appendC'
HTML += b'hild(this.generateText(s));let i=w();if(i.innerHTML="",i.cla'
HTML += b'ssList.add("button-group"),this.questionDiv.appendChild(i),t'
HTML += b'his.hasCheckButton=Object.keys(this.expected).length>0,this.'
HTML += b'hasCheckButton&&(this.checkAndRepeatBtn=F(),i.appendChild(th'
HTML += b'is.checkAndRepeatBtn),this.checkAndRepeatBtn.innerHTML=I,thi'
HTML += b's.checkAndRepeatBtn.style.backgroundColor="black",e&&(this.c'
HTML += b'heckAndRepeatBtn.style.height="0",this.checkAndRepeatBtn.sty'
HTML += b'le.visibility="hidden")),this.feedbackSpan=k(""),this.feedba'
HTML += b'ckSpan.style.userSelect="none",i.appendChild(this.feedbackSp'
HTML += b'an),this.debug){if(this.src.variables.length>0){let o=w();o.'
HTML += b'classList.add("debugInfo"),o.innerHTML="Variables generated '
HTML += b'by Python Code",this.questionDiv.appendChild(o);let l=w();l.'
HTML += b'classList.add("debugCode"),this.questionDiv.appendChild(l);l'
HTML += b'et n=this.getCurrentInstance(),h="",p=[...this.src.variables'
HTML += b'];p.sort();for(let m of p){let u=n[m].t,d=n[m].v;switch(u){c'
HTML += b'ase"vector":d="["+d+"]";break;case"set":d="{"+d+"}";break}h+'
HTML += b'=u+" "+m+" = "+d+"<br/>"}l.innerHTML=h}let s=["python_src_ht'
HTML += b'ml","text_src_html"],c=["Python Source Code","Text Source Co'
HTML += b'de"];for(let o=0;o<s.length;o++){let l=s[o];if(l in this.src'
HTML += b'&&this.src[l].length>0){let n=w();n.classList.add("debugInfo'
HTML += b'"),n.innerHTML=c[o],this.questionDiv.appendChild(n);let h=w('
HTML += b');h.classList.add("debugCode"),this.questionDiv.append(h),h.'
HTML += b'innerHTML=this.src[l]}}}this.hasCheckButton&&this.checkAndRe'
HTML += b'peatBtn.addEventListener("click",()=>{this.state==b.passed?('
HTML += b'this.state=b.init,this.reset(),this.populateDom()):V(this)})'
HTML += b'}generateMathString(e){let t="";switch(e.t){case"math":case"'
HTML += b'display-math":for(let i of e.c){let s=this.generateMathStrin'
HTML += b'g(i);i.t==="var"&&t.includes("!PM")&&(s.startsWith("{-")?(s='
HTML += b'"{"+s.substring(2),t=t.replaceAll("!PM","-")):t=t.replaceAll'
HTML += b'("!PM","+")),t+=s}break;case"text":return e.d;case"plus_minu'
HTML += b's":{t+=" !PM ";break}case"var":{let i=this.getCurrentInstanc'
HTML += b'e(),s=i[e.d].t,c=i[e.d].v;switch(s){case"vector":return"\\\\le'
HTML += b'ft["+c+"\\\\right]";case"set":return"\\\\left\\\\{"+c+"\\\\right\\\\}"'
HTML += b';case"complex":{let o=c.split(","),l=parseFloat(o[0]),n=pars'
HTML += b'eFloat(o[1]);return r.const(l,n).toTexString()}case"matrix":'
HTML += b'{let o=new E(0,0);return o.fromString(c),t=o.toTeXString(e.d'
HTML += b'.includes("augmented"),this.language!="de"),t}case"term":{tr'
HTML += b'y{t=v.parse(c).toTexString()}catch{}break}default:t=c}}}retu'
HTML += b'rn e.t==="plus_minus"?t:"{"+t+"}"}generateText(e,t=!1){switc'
HTML += b'h(e.t){case"paragraph":case"span":{let i=document.createElem'
HTML += b'ent(e.t=="span"||t?"span":"p");for(let s of e.c)i.appendChil'
HTML += b'd(this.generateText(s));return i.style.userSelect="none",i}c'
HTML += b'ase"text":return k(e.d);case"code":{let i=k(e.d);return i.cl'
HTML += b'assList.add("code"),i}case"italic":case"bold":{let i=k("");r'
HTML += b'eturn i.append(...e.c.map(s=>this.generateText(s))),e.t==="b'
HTML += b'old"?i.style.fontWeight="bold":i.style.fontStyle="italic",i}'
HTML += b'case"math":case"display-math":{let i=this.generateMathString'
HTML += b'(e);return T(i,e.t==="display-math")}case"string_var":{let i'
HTML += b'=k(""),s=this.getCurrentInstance(),c=s[e.d].t,o=s[e.d].v;ret'
HTML += b'urn c==="string"?i.innerHTML=o:(i.innerHTML="EXPECTED VARIAB'
HTML += b'LE OF TYPE STRING",i.style.color="red"),i}case"gap":{let i=k'
HTML += b'("");return new A(i,this,"",e.d),i}case"input":case"input2":'
HTML += b'{let i=e.t==="input2",s=k("");s.style.verticalAlign="text-bo'
HTML += b'ttom";let c=e.d,o=this.getCurrentInstance()[c];if(this.expec'
HTML += b'ted[c]=o.v,this.types[c]=o.t,!i)switch(o.t){case"set":s.appe'
HTML += b'nd(T("\\\\{"),k(" "));break;case"vector":s.append(T("["),k(" "'
HTML += b'));break}if(o.t==="string")new A(s,this,c,this.expected[c]);'
HTML += b'else if(o.t==="vector"||o.t==="set"){let l=o.v.split(","),n='
HTML += b'l.length;for(let h=0;h<n;h++){h>0&&s.appendChild(k(" , "));l'
HTML += b'et p=c+"-"+h;new L(s,this,p,l[h].length,l[h],!1)}}else if(o.'
HTML += b't==="matrix"){let l=w();s.appendChild(l),new B(l,this,c,o.v)'
HTML += b'}else if(o.t==="complex"){let l=o.v.split(",");new L(s,this,'
HTML += b'c+"-0",l[0].length,l[0],!1),s.append(k(" "),T("+"),k(" ")),n'
HTML += b'ew L(s,this,c+"-1",l[1].length,l[1],!1),s.append(k(" "),T("i'
HTML += b'"))}else{let l=o.t==="int";new L(s,this,c,o.v.length,o.v,l)}'
HTML += b'if(!i)switch(o.t){case"set":s.append(k(" "),T("\\\\}"));break;'
HTML += b'case"vector":s.append(k(" "),T("]"));break}return s}case"ite'
HTML += b'mize":return U(e.c.map(i=>j(this.generateText(i))));case"sin'
HTML += b'gle-choice":case"multi-choice":{let i=e.t=="multi-choice";i|'
HTML += b'|(this.includesSingleChoice=!0);let s=document.createElement'
HTML += b'("table"),c=e.c.length,o=this.debug==!1,l=P(c,o),n=i?K:Z,h=i'
HTML += b'?q:X,p=[],m=[];for(let u=0;u<c;u++){let d=l[u],f=e.c[d],g="m'
HTML += b'c-"+this.choiceIdx+"-"+d;m.push(g);let C=f.c[0].t=="bool"?f.'
HTML += b'c[0].d:this.getCurrentInstance()[f.c[0].d].v;this.expected[g'
HTML += b']=C,this.types[g]="bool",this.student[g]=this.showSolution?C'
HTML += b':"false";let M=this.generateText(f.c[1],!0),y=document.creat'
HTML += b'eElement("tr");s.appendChild(y),y.style.cursor="pointer";let'
HTML += b' S=document.createElement("td");p.push(S),y.appendChild(S),S'
HTML += b'.innerHTML=this.student[g]=="true"?n:h;let x=document.create'
HTML += b'Element("td");y.appendChild(x),x.appendChild(M),i?y.addEvent'
HTML += b'Listener("click",()=>{this.editedQuestion(),this.student[g]='
HTML += b'this.student[g]==="true"?"false":"true",this.student[g]==="t'
HTML += b'rue"?S.innerHTML=n:S.innerHTML=h}):y.addEventListener("click'
HTML += b'",()=>{this.editedQuestion();for(let D of m)this.student[D]='
HTML += b'"false";this.student[g]="true";for(let D=0;D<m.length;D++){l'
HTML += b'et Q=l[D];p[Q].innerHTML=this.student[m[Q]]=="true"?n:h}})}r'
HTML += b'eturn this.choiceIdx++,s}case"image":{let i=w(),c=e.d.split('
HTML += b'"."),o=c[c.length-1],l=e.c[0].d,n=e.c[1].d,h=document.create'
HTML += b'Element("img");i.appendChild(h),h.classList.add("img"),h.sty'
HTML += b'le.width=l+"%";let p={svg:"svg+xml",png:"png",jpg:"jpeg"};re'
HTML += b'turn h.src="data:image/"+p[o]+";base64,"+n,i}default:{let i='
HTML += b'k("UNIMPLEMENTED("+e.t+")");return i.style.color="red",i}}}}'
HTML += b';function V(a){a.feedbackSpan.innerHTML="",a.numChecked=0,a.'
HTML += b'numCorrect=0;let e=!0;for(let s in a.expected){let c=a.types'
HTML += b'[s],o=a.student[s],l=a.expected[s];switch(o!=null&&o.length='
HTML += b'=0&&(e=!1),c){case"bool":a.numChecked++,o.toLowerCase()===l.'
HTML += b'toLowerCase()&&a.numCorrect++;break;case"string":{a.numCheck'
HTML += b'ed++;let n=a.gapInputs[s],h=o.trim().toUpperCase(),p=l.trim('
HTML += b').toUpperCase().split("|"),m=!1;for(let u of p)if(O(h,u)<=1)'
HTML += b'{m=!0,a.numCorrect++,a.gapInputs[s].value=u,a.student[s]=u;b'
HTML += b'reak}n.style.color=m?"black":"white",n.style.backgroundColor'
HTML += b'=m?"transparent":"maroon";break}case"int":a.numChecked++,Mat'
HTML += b'h.abs(parseFloat(o)-parseFloat(l))<1e-9&&a.numCorrect++;brea'
HTML += b'k;case"float":case"term":{a.numChecked++;try{let n=v.parse(l'
HTML += b'),h=v.parse(o),p=!1;a.src.is_ode?p=re(n,h):p=v.compare(n,h),'
HTML += b'p&&a.numCorrect++}catch(n){a.debug&&(console.log("term inval'
HTML += b'id"),console.log(n))}break}case"vector":case"complex":case"s'
HTML += b'et":{let n=l.split(",");a.numChecked+=n.length;let h=[];for('
HTML += b'let p=0;p<n.length;p++){let m=a.student[s+"-"+p];m.length==0'
HTML += b'&&(e=!1),h.push(m)}if(c==="set")for(let p=0;p<n.length;p++)t'
HTML += b'ry{let m=v.parse(n[p]);for(let u=0;u<h.length;u++){let d=v.p'
HTML += b'arse(h[u]);if(v.compare(m,d)){a.numCorrect++;break}}}catch(m'
HTML += b'){a.debug&&console.log(m)}else for(let p=0;p<n.length;p++)tr'
HTML += b'y{let m=v.parse(h[p]),u=v.parse(n[p]);v.compare(m,u)&&a.numC'
HTML += b'orrect++}catch(m){a.debug&&console.log(m)}break}case"matrix"'
HTML += b':{let n=new E(0,0);n.fromString(l),a.numChecked+=n.m*n.n;for'
HTML += b'(let h=0;h<n.m;h++)for(let p=0;p<n.n;p++){let m=h*n.n+p;o=a.'
HTML += b'student[s+"-"+m],o!=null&&o.length==0&&(e=!1);let u=n.v[m];t'
HTML += b'ry{let d=v.parse(u),f=v.parse(o);v.compare(d,f)&&a.numCorrec'
HTML += b't++}catch(d){a.debug&&console.log(d)}}break}default:a.feedba'
HTML += b'ckSpan.innerHTML="UNIMPLEMENTED EVAL OF TYPE "+c}}e==!1?a.st'
HTML += b'ate=b.incomplete:a.state=a.numCorrect==a.numChecked?b.passed'
HTML += b':b.errors,a.updateVisualQuestionState();let t=[];switch(a.st'
HTML += b'ate){case b.passed:t=ee[a.language];break;case b.incomplete:'
HTML += b't=te[a.language];break;case b.errors:t=se[a.language];break}'
HTML += b'let i=t[Math.floor(Math.random()*t.length)];a.feedbackPopupD'
HTML += b'iv.innerHTML=i,a.feedbackPopupDiv.style.color=a.state===b.pa'
HTML += b'ssed?"var(--green)":"var(--red)",a.feedbackPopupDiv.style.di'
HTML += b'splay="flex",setTimeout(()=>{a.feedbackPopupDiv.style.displa'
HTML += b'y="none"},1e3),a.state===b.passed?a.src.instances.length>0?a'
HTML += b'.checkAndRepeatBtn.innerHTML=Y:a.checkAndRepeatBtn.style.vis'
HTML += b'ibility="hidden":a.checkAndRepeatBtn!=null&&(a.checkAndRepea'
HTML += b'tBtn.innerHTML=I)}function fe(a,e){["en","de","es","it","fr"'
HTML += b'].includes(a.lang)==!1&&(a.lang="en"),e&&(document.getElemen'
HTML += b'tById("debug").style.display="block"),document.getElementByI'
HTML += b'd("date").innerHTML=a.date,document.getElementById("title").'
HTML += b'innerHTML=a.title,document.getElementById("author").innerHTM'
HTML += b'L=a.author,document.getElementById("courseInfo1").innerHTML='
HTML += b'G[a.lang];let t=\'<span onclick="location.reload()" style="te'
HTML += b'xt-decoration: none; font-weight: bold; cursor: pointer">\'+$'
HTML += b'[a.lang]+"</span>";document.getElementById("courseInfo2").in'
HTML += b'nerHTML=J[a.lang].replace("*",t),document.getElementById("da'
HTML += b'ta-policy").innerHTML=ae[a.lang];let i=a.timer,s=[],c=docume'
HTML += b'nt.getElementById("questions"),o=1;for(let l of a.questions)'
HTML += b'{l.title=""+o+". "+l.title;let n=w();c.appendChild(n);let h='
HTML += b'new H(n,l,a.lang,e);h.showSolution=e,s.push(h),h.populateDom'
HTML += b'(i>0),e&&l.error.length==0&&h.hasCheckButton&&h.checkAndRepe'
HTML += b'atBtn.click(),o++}if(i>0){document.getElementById("stop-now"'
HTML += b').style.display="block",document.getElementById("stop-now-bt'
HTML += b'n").innerHTML=ne[a.lang],document.getElementById("stop-now-b'
HTML += b'tn").addEventListener("click",()=>{i=1});let l=document.getE'
HTML += b'lementById("timer");l.style.display="block",l.innerHTML=le(i'
HTML += b');let n=setInterval(()=>{if(i--,l.innerHTML=le(i),i<=0){docu'
HTML += b'ment.getElementById("stop-now").style.display="none",clearIn'
HTML += b'terval(n);let h=0,p=0;for(let u of s){let d=u.src.points;p+='
HTML += b'd,V(u),u.state===b.passed&&(h+=d)}document.getElementById("q'
HTML += b'uestions-eval").style.display="block",document.getElementByI'
HTML += b'd("questions-eval-text").innerHTML=ie[a.lang]+":";let m=docu'
HTML += b'ment.getElementById("questions-eval-percentage");m.innerHTML'
HTML += b'=p==0?"":""+Math.round(h/p*100)+" %",console.log(h),console.'
HTML += b'log(p)}},1e3)}}function le(a){let e=Math.floor(a/60),t=a%60;'
HTML += b'return e+":"+(""+t).padStart(2,"0")}return ue(ge);})();sell.'
HTML += b'init(quizSrc,debug);</script></body> </html> '
HTML = HTML.decode('utf-8')
# @end(html)


def main():
    """the main function"""

    print("---------------------------------------------------------------------")
    print("pySELL by Andreas Schwenk - Licensed under GPLv3 - https://pysell.org")
    print("---------------------------------------------------------------------")

    # get input and output path
    if len(sys.argv) < 2:
        print("USAGE: pysell [-J] INPUT_PATH.txt")
        print("   option -J enables to output a JSON file for debugging purposes")
        sys.exit(-1)
    write_explicit_json_file = "-J" in sys.argv
    input_path = sys.argv[-1]
    input_dirname = os.path.dirname(input_path)
    output_path = input_path.replace(".txt", ".html")
    output_debug_path = input_path.replace(".txt", "_DEBUG.html")
    output_json_path = input_path.replace(".txt", ".json")
    if os.path.isfile(input_path) is False:
        print("error: input file path does not exist")
        sys.exit(-1)

    # read input
    input_src: str = ""
    with open(input_path, mode="r", encoding="utf-8") as f:
        input_src = f.read()

    # compile
    out = compile_input_file(input_dirname, input_src)
    output_debug_json = json.dumps(out)
    output_debug_json_formatted = json.dumps(out, indent=2)
    for question in out["questions"]:
        del question["src_line"]
        del question["text_src_html"]
        del question["python_src_html"]
        del question["python_src_tokens"]
    output_json = json.dumps(out)

    # write test output
    if write_explicit_json_file:
        with open(output_json_path, "w", encoding="utf-8") as f:
            f.write(output_debug_json_formatted)

    # write html
    # (a) debug version (*_DEBUG.html)
    with open(output_debug_path, "w", encoding="utf-8") as f:
        f.write(
            HTML.replace(
                "let quizSrc = {};", "let quizSrc = " + output_debug_json + ";"
            ).replace("let debug = false;", "let debug = true;")
        )
    # (b) release version (*.html)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(HTML.replace("let quizSrc = {};", "let quizSrc = " + output_json + ";"))

    # exit normally
    sys.exit(0)


if __name__ == "__main__":
    main()
