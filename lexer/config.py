WORD="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789"

RESERVED_WORDS="""and double not_eq throw and_eq dynamic_cast
operator true asm else or try auto enum or_eq typedef bitand
explicit private typeid bitor extern protected typename 
bool false public union break float register unsigned
case for reinterpret-cast using catch friend return	
virtual char goto short void class if signed this
volatile compl inline sizeof wchar_t const not
int static while const-cast long mutable
static_cast	xor continue namespace
struct xor_eq default switch new
delete template""".split()

HEX_DECIMALS="0123456789ABCDEFabcdef"

COMMENTS=["//", "/*", "*/"]

HEX_LETTERS="ABCDEFabcdef"

OPERATORS="+-*/=%|&^><~!?"

DELIMITERS="}{)(][,:.;"

DECIMALS="0123456789"

STRING=["'", '"']

EMPTY=" \n\t"