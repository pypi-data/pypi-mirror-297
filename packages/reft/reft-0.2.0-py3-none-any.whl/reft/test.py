import re
from reft import FT

def parse_condition_string(s, IFSO='IFSO', EFSO='EFSO', ELSO='ELSO', IFEO='IFEO'):
    gs = [
        f"\s*{IFSO}\s*.*((.|\n)+?)(?=(({EFSO})|({ELSO})|({IFEO})))",
        f"(\s*{EFSO}\s*.*((.|\n)+?)(?=(({EFSO})|({ELSO})|({IFEO}))))*",
        f"(\s*{ELSO}\s*((.|\n)+?)(?={IFEO}))?",
        f"\s*{IFEO}\s*"
    ]
    vids = [0, 1, 2]
    ft = FT()
    ft.login(_hook, *gs, areas=vids)
    return ft.handle(s)

def _hook(if_expr, ef_expr, el_expr):
    print(f"if_expr: {if_expr}")
    print(f"ef_expr: {ef_expr}")
    print(f"el_expr: {el_expr}")


s = """
IFSO 1 > 2
str1
EFSO 2-2
str2
EFSO 1
str3
ELSO
str4
IFEO
"""

parse_condition_string(s)