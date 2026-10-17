"""Mini Lexical Analyzer (Python + SLY)
วิชา 05506237 Programming Languages Concepts and Paradigms

ติดตั้ง:  pip install sly
วิธีใช้:  python lexer.py tests/test1.txt
"""
import sys
from sly import Lexer


class LexicalError(Exception):
    """เกิดเมื่อพบข้อความที่ไม่ตรงกับ token ใด ๆ"""


class MiniLexer(Lexer):
    # ---------- รายชื่อ token ----------
    tokens = {
        # operators
        PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
        GT, GE, LT, LE, EQ, INCREMENT, DECREMENT,
        # parentheses and semicolon
        LPAREN, RPAREN, SEMICOLON,
        # keywords
        IF, THEN, ELSE, ENDIF, WHILE, DO, ENDWHILE, PRINT, NEWLINE, READ,
        # others
        INTEGER, ID, STRING,
    }

    # อักขระที่ถูกข้าม (space, tab, carriage return)
    ignore = ' \t\r'

    # ---------- comments: ต้องวางก่อน DIVIDE เพราะขึ้นต้นด้วย / ----------
    ignore_line_comment = r'//[^\n]*'

    @_(r'/\*[\s\S]*?\*/')
    def ignore_block_comment(self, t):
        self.lineno += t.value.count('\n')

    @_(r'/\*')   # มี /* แต่ไม่มี */ ปิด -> ถือเป็น lexical error
    def ignore_unterminated_comment(self, t):
        raise LexicalError(
            f"Lexical error: unexpected character / "
            f"(unterminated block comment starting at line {self.lineno})")

    @_(r'\n+')   # อักขระขึ้นบรรทัดใหม่ (ไม่ใช่ keyword newline)
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # ---------- operators: ตัวยาวต้องมาก่อนตัวสั้น ----------
    INCREMENT = r'\+\+'
    DECREMENT = r'--'
    EQ        = r'=='
    GE        = r'>='
    LE        = r'<='
    PLUS      = r'\+'
    MINUS     = r'-'
    TIMES     = r'\*'
    DIVIDE    = r'/'
    ASSIGN    = r'='
    GT        = r'>'
    LT        = r'<'

    # ---------- วงเล็บและ semicolon ----------
    LPAREN    = r'\('
    RPAREN    = r'\)'
    SEMICOLON = r';'

    # ---------- string: อยู่บรรทัดเดียว ไม่รองรับ escape ----------
    STRING = r'"[^"\n]*"'

    # ---------- ตัวเลขที่มีตัวอักษรตามหลัง (เช่น 1score) -> identifier ผิดรูปแบบ ----------
    @_(r'[0-9]+[a-zA-Z_][a-zA-Z0-9_]*')
    def ignore_bad_identifier(self, t):
        raise LexicalError(
            f"Lexical error: unexpected character {t.value[0]} "
            f"(invalid identifier \"{t.value}\" cannot start with a digit, line {self.lineno})")

    # ---------- integer: เลขจำนวนเต็มไม่ติดลบ ----------
    INTEGER = r'[0-9]+'

    # ---------- identifier และ keywords (keyword เป็นตัวพิมพ์เล็กเท่านั้น) ----------
    ID = r'[a-zA-Z][a-zA-Z0-9]*'
    ID['if'] = IF
    ID['then'] = THEN
    ID['else'] = ELSE
    ID['endif'] = ENDIF
    ID['while'] = WHILE
    ID['do'] = DO
    ID['endwhile'] = ENDWHILE
    ID['print'] = PRINT
    ID['newline'] = NEWLINE
    ID['read'] = READ

    # ---------- lexical error: อักขระที่ไม่ตรงกับ token ใด ๆ ----------
    def error(self, t):
        raise LexicalError(f"Lexical error: unexpected character {t.value[0]}")


# ชนิดของ token -> ข้อความหน้าผลลัพธ์ (ไม่ต้องเขียน if-else ไล่ทีละชนิด)
OPERATORS = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'GT', 'GE', 'LT',
             'LE', 'EQ', 'INCREMENT', 'DECREMENT']
KEYWORDS = ['IF', 'THEN', 'ELSE', 'ENDIF', 'WHILE', 'DO', 'ENDWHILE',
            'PRINT', 'NEWLINE', 'READ']
LABEL = {
    **{name: 'operator' for name in OPERATORS},
    **{name: 'keyword' for name in KEYWORDS},
    'INTEGER': 'integer',
    'STRING': 'string',
    'LPAREN': 'left parenthesis',
    'RPAREN': 'right parenthesis',
    'SEMICOLON': 'semicolon',
}


def analyze(source):
    lexer = MiniLexer()
    symbol_table = set()                  # symbol table เก็บเฉพาะ identifier
    try:
        for tok in lexer.tokenize(source):
            if tok.type == 'ID':
                if tok.value in symbol_table:
                    print(f'identifier "{tok.value}" already in symbol table')
                else:
                    symbol_table.add(tok.value)
                    print(f'new identifier: {tok.value}')
            else:
                print(f'{LABEL[tok.type]}: {tok.value}')
    except LexicalError as err:
        print(err)
        sys.exit(1)                       # หยุดการทำงานทันทีเมื่อพบ lexical error
    return symbol_table


def main():
    if len(sys.argv) != 2:
        print('usage: python lexer.py <input.txt>')
        sys.exit(2)
    sys.stdout.reconfigure(encoding='utf-8')   # ให้แสดง string ภาษาไทยบน Windows console ได้
    try:
        with open(sys.argv[1], encoding='utf-8') as f:
            source = f.read()
    except OSError as err:
        print(f'cannot open file: {err.filename}')
        sys.exit(2)
    analyze(source)


if __name__ == '__main__':
    main()