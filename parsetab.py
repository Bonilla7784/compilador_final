
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AYUDA BOOL COLON COMMA CTEI DIVIDE ELSE EQUALS EQUAL_EQUAL FALSE FLOAT FLOAT_NUMBER GREATER_EQUAL GREATER_THAN ID IF INT LBRACE LBRACKET LESS_EQUAL LESS_THAN LPAREN MAIN MINUS MULTIPLY NOT_EQUAL PLUS PRINT PROGRAM RBRACE RBRACKET RETURN RPAREN SEMICOLON STRING STRING_LITERAL TEACH_DIVISION TEACH_FUNCTION_CALL TEACH_FUNCTION_DECLARATION TEACH_IF TEACH_MULTIPLICATION TEACH_SUBSTRACTION TEACH_SUM TEACH_WHILE TRUE VARIABLES VOID WHILEprogram : PROGRAM ID SEMICOLON placeholder_goto_main create_scopes global_scope main_function end_scopes fill_goto_mainplaceholder_goto_main : global_scope : VARIABLES LBRACE decl_list RBRACE function_decl_list\n                    | VARIABLES LBRACE decl_list RBRACEfunction_decl_list : function_decl function_decl_list\n                          | emptymain_function : MAIN LPAREN RPAREN LBRACE start_main stmt_list RBRACEstart_main : fill_goto_main : create_scopes : end_scopes : decl_list : decl SEMICOLON decl_list\n                 | decl SEMICOLON\n                 | emptydecl : type ID\n            | array_decltype : INT\n            | FLOAT\n            | STRING\n            | BOOLstmt_list : stmt SEMICOLON stmt_list\n                 | stmt SEMICOLONstmt : assign\n            | print\n            | conditional\n            | loop\n            | function_call\n            | decl\n            | built_in_function\n            | return_stmtbuilt_in_function : TEACH_SUM LPAREN RPAREN\n                         | TEACH_SUBSTRACTION LPAREN RPAREN\n                         | TEACH_MULTIPLICATION LPAREN RPAREN\n                         | TEACH_DIVISION LPAREN RPAREN\n                         | TEACH_IF LPAREN RPAREN\n                         | TEACH_WHILE LPAREN RPAREN\n                         | TEACH_FUNCTION_DECLARATION LPAREN RPAREN\n                         | TEACH_FUNCTION_CALL LPAREN RPAREN\n                         | AYUDA LPAREN RPARENassign : ID EQUALS exprexpr : expr PLUS term\n            | expr MINUS term\n            | expr comp_op term\n            | termterm : term MULTIPLY factor\n            | term DIVIDE factor\n            | factor\n            | function_callfactor : LPAREN expr RPAREN\n              | CTEI\n              | FLOAT_NUMBER\n              | STRING_LITERAL\n              | TRUE\n              | FALSE\n              | ID\n              | function_callprint : PRINT COLON exprconditional : IF LPAREN comp_expr RPAREN LBRACE stmt_list RBRACE else_stmt\n                   | IF LPAREN comp_expr RPAREN LBRACE stmt_list RBRACEcomp_expr : expr comp_op exprcomp_op : LESS_THAN\n               | GREATER_THAN\n               | LESS_EQUAL\n               | GREATER_EQUAL\n               | EQUAL_EQUAL\n               | NOT_EQUALelse_stmt : ELSE LBRACE else_part stmt_list RBRACE\n                 | emptyelse_part : loop : WHILE LPAREN comp_expr RPAREN LBRACE stmt_list RBRACEcreate_function_scope : function_decl : type ID LPAREN create_function_scope param_list RPAREN LBRACE stmt_list end_scopes RBRACE\n                     | VOID ID LPAREN create_function_scope param_list RPAREN LBRACE stmt_list end_scopes RBRACEreturn_stmt : RETURN expr\n                   | emptyfunction_call : ID LPAREN arg_list RPARENarg_list : arg_list COMMA expr\n                | exprparam_list : param COMMA param_list\n                  | param\n                  | emptyparam : type IDarray_decl : type ID LBRACKET CTEI RBRACKETempty :'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,9,12,23,69,],[0,-11,-9,-1,-7,]),'ID':([2,17,19,20,21,22,28,32,33,36,64,70,71,72,73,74,75,89,115,116,117,118,119,120,121,122,123,124,125,127,133,135,149,152,153,155,169,170,],[3,27,-17,-18,-19,-20,-8,38,39,51,95,51,95,95,95,95,95,95,95,95,95,-61,-62,-63,-64,-65,-66,95,95,144,95,95,51,51,51,51,-69,51,]),'SEMICOLON':([3,15,18,27,28,36,42,43,44,45,46,47,48,49,50,65,68,70,85,86,87,88,90,91,92,93,94,95,99,102,106,107,108,109,110,111,112,113,114,132,137,138,139,140,141,142,143,149,152,153,155,160,161,164,166,169,170,172,],[4,26,-16,-15,-8,-84,70,-23,-24,-25,-26,-27,-28,-29,-30,-75,-83,-84,-74,-44,-47,-48,-50,-51,-52,-53,-54,-55,-40,-57,-31,-32,-33,-34,-35,-36,-37,-38,-39,-76,-41,-42,-43,-45,-56,-46,-49,-84,-84,-84,-84,-59,-70,-58,-68,-69,-84,-67,]),'VARIABLES':([4,5,6,],[-2,-10,8,]),'MAIN':([7,25,29,30,31,37,167,168,],[10,-4,-3,-84,-6,-5,-72,-73,]),'LBRACE':([8,24,134,136,145,147,165,],[11,28,149,152,153,155,169,]),'LPAREN':([10,38,39,51,53,54,55,56,57,58,59,60,61,62,63,64,71,72,73,74,75,89,95,115,116,117,118,119,120,121,122,123,124,125,133,135,],[13,66,67,72,74,75,76,77,78,79,80,81,82,83,84,89,89,89,89,89,89,89,72,89,89,89,-61,-62,-63,-64,-65,-66,89,89,89,89,]),'RBRACE':([11,14,16,26,34,41,70,98,156,157,158,159,162,163,171,],[-84,25,-14,-13,-12,69,-22,-21,160,161,-11,-11,167,168,172,]),'INT':([11,25,26,28,30,36,66,67,70,96,97,146,149,152,153,155,167,168,169,170,],[19,19,19,-8,19,19,-71,-71,19,19,19,19,19,19,19,19,-72,-73,-69,19,]),'FLOAT':([11,25,26,28,30,36,66,67,70,96,97,146,149,152,153,155,167,168,169,170,],[20,20,20,-8,20,20,-71,-71,20,20,20,20,20,20,20,20,-72,-73,-69,20,]),'STRING':([11,25,26,28,30,36,66,67,70,96,97,146,149,152,153,155,167,168,169,170,],[21,21,21,-8,21,21,-71,-71,21,21,21,21,21,21,21,21,-72,-73,-69,21,]),'BOOL':([11,25,26,28,30,36,66,67,70,96,97,146,149,152,153,155,167,168,169,170,],[22,22,22,-8,22,22,-71,-71,22,22,22,22,22,22,22,22,-72,-73,-69,22,]),'RPAREN':([13,66,67,76,77,78,79,80,81,82,83,84,86,87,88,90,91,92,93,94,95,96,97,100,101,103,105,126,128,129,130,131,132,137,138,139,140,141,142,143,144,146,148,150,151,154,],[24,-71,-71,106,107,108,109,110,111,112,113,114,-44,-47,-48,-50,-51,-52,-53,-54,-55,-84,-84,132,-78,134,136,143,145,-80,-81,147,-76,-41,-42,-43,-45,-56,-46,-49,-82,-84,-77,-60,-44,-79,]),'VOID':([25,30,167,168,],[33,33,-72,-73,]),'LBRACKET':([27,],[35,]),'PRINT':([28,36,70,149,152,153,155,169,170,],[-8,52,52,52,52,52,52,-69,52,]),'IF':([28,36,70,149,152,153,155,169,170,],[-8,53,53,53,53,53,53,-69,53,]),'WHILE':([28,36,70,149,152,153,155,169,170,],[-8,54,54,54,54,54,54,-69,54,]),'TEACH_SUM':([28,36,70,149,152,153,155,169,170,],[-8,55,55,55,55,55,55,-69,55,]),'TEACH_SUBSTRACTION':([28,36,70,149,152,153,155,169,170,],[-8,56,56,56,56,56,56,-69,56,]),'TEACH_MULTIPLICATION':([28,36,70,149,152,153,155,169,170,],[-8,57,57,57,57,57,57,-69,57,]),'TEACH_DIVISION':([28,36,70,149,152,153,155,169,170,],[-8,58,58,58,58,58,58,-69,58,]),'TEACH_IF':([28,36,70,149,152,153,155,169,170,],[-8,59,59,59,59,59,59,-69,59,]),'TEACH_WHILE':([28,36,70,149,152,153,155,169,170,],[-8,60,60,60,60,60,60,-69,60,]),'TEACH_FUNCTION_DECLARATION':([28,36,70,149,152,153,155,169,170,],[-8,61,61,61,61,61,61,-69,61,]),'TEACH_FUNCTION_CALL':([28,36,70,149,152,153,155,169,170,],[-8,62,62,62,62,62,62,-69,62,]),'AYUDA':([28,36,70,149,152,153,155,169,170,],[-8,63,63,63,63,63,63,-69,63,]),'RETURN':([28,36,70,149,152,153,155,169,170,],[-8,64,64,64,64,64,64,-69,64,]),'CTEI':([35,64,71,72,73,74,75,89,115,116,117,118,119,120,121,122,123,124,125,133,135,],[40,90,90,90,90,90,90,90,90,90,90,-61,-62,-63,-64,-65,-66,90,90,90,90,]),'RBRACKET':([40,],[68,]),'EQUALS':([51,],[71,]),'COLON':([52,],[73,]),'FLOAT_NUMBER':([64,71,72,73,74,75,89,115,116,117,118,119,120,121,122,123,124,125,133,135,],[91,91,91,91,91,91,91,91,91,91,-61,-62,-63,-64,-65,-66,91,91,91,91,]),'STRING_LITERAL':([64,71,72,73,74,75,89,115,116,117,118,119,120,121,122,123,124,125,133,135,],[92,92,92,92,92,92,92,92,92,92,-61,-62,-63,-64,-65,-66,92,92,92,92,]),'TRUE':([64,71,72,73,74,75,89,115,116,117,118,119,120,121,122,123,124,125,133,135,],[93,93,93,93,93,93,93,93,93,93,-61,-62,-63,-64,-65,-66,93,93,93,93,]),'FALSE':([64,71,72,73,74,75,89,115,116,117,118,119,120,121,122,123,124,125,133,135,],[94,94,94,94,94,94,94,94,94,94,-61,-62,-63,-64,-65,-66,94,94,94,94,]),'PLUS':([85,86,87,88,90,91,92,93,94,95,99,101,102,104,126,132,137,138,139,140,141,142,143,148,150,151,],[115,-44,-47,-48,-50,-51,-52,-53,-54,-55,115,115,115,115,115,-76,-41,-42,-43,-45,-56,-46,-49,115,115,-43,]),'MINUS':([85,86,87,88,90,91,92,93,94,95,99,101,102,104,126,132,137,138,139,140,141,142,143,148,150,151,],[116,-44,-47,-48,-50,-51,-52,-53,-54,-55,116,116,116,116,116,-76,-41,-42,-43,-45,-56,-46,-49,116,116,-43,]),'LESS_THAN':([85,86,87,88,90,91,92,93,94,95,99,101,102,104,126,132,137,138,139,140,141,142,143,148,150,151,],[118,-44,-47,-48,-50,-51,-52,-53,-54,-55,118,118,118,118,118,-76,-41,-42,-43,-45,-56,-46,-49,118,118,-43,]),'GREATER_THAN':([85,86,87,88,90,91,92,93,94,95,99,101,102,104,126,132,137,138,139,140,141,142,143,148,150,151,],[119,-44,-47,-48,-50,-51,-52,-53,-54,-55,119,119,119,119,119,-76,-41,-42,-43,-45,-56,-46,-49,119,119,-43,]),'LESS_EQUAL':([85,86,87,88,90,91,92,93,94,95,99,101,102,104,126,132,137,138,139,140,141,142,143,148,150,151,],[120,-44,-47,-48,-50,-51,-52,-53,-54,-55,120,120,120,120,120,-76,-41,-42,-43,-45,-56,-46,-49,120,120,-43,]),'GREATER_EQUAL':([85,86,87,88,90,91,92,93,94,95,99,101,102,104,126,132,137,138,139,140,141,142,143,148,150,151,],[121,-44,-47,-48,-50,-51,-52,-53,-54,-55,121,121,121,121,121,-76,-41,-42,-43,-45,-56,-46,-49,121,121,-43,]),'EQUAL_EQUAL':([85,86,87,88,90,91,92,93,94,95,99,101,102,104,126,132,137,138,139,140,141,142,143,148,150,151,],[122,-44,-47,-48,-50,-51,-52,-53,-54,-55,122,122,122,122,122,-76,-41,-42,-43,-45,-56,-46,-49,122,122,-43,]),'NOT_EQUAL':([85,86,87,88,90,91,92,93,94,95,99,101,102,104,126,132,137,138,139,140,141,142,143,148,150,151,],[123,-44,-47,-48,-50,-51,-52,-53,-54,-55,123,123,123,123,123,-76,-41,-42,-43,-45,-56,-46,-49,123,123,-43,]),'COMMA':([86,87,88,90,91,92,93,94,95,100,101,129,132,137,138,139,140,141,142,143,144,148,],[-44,-47,-48,-50,-51,-52,-53,-54,-55,133,-78,146,-76,-41,-42,-43,-45,-56,-46,-49,-82,-77,]),'MULTIPLY':([86,87,88,90,91,92,93,94,95,132,137,138,139,140,141,142,143,151,],[124,-47,-48,-50,-51,-52,-53,-54,-55,-76,124,124,124,-45,-56,-46,-49,124,]),'DIVIDE':([86,87,88,90,91,92,93,94,95,132,137,138,139,140,141,142,143,151,],[125,-47,-48,-50,-51,-52,-53,-54,-55,-76,125,125,125,-45,-56,-46,-49,125,]),'ELSE':([160,],[165,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'placeholder_goto_main':([4,],[5,]),'create_scopes':([5,],[6,]),'global_scope':([6,],[7,]),'main_function':([7,],[9,]),'end_scopes':([9,158,159,],[12,162,163,]),'decl_list':([11,26,],[14,34,]),'decl':([11,26,36,70,149,152,153,155,170,],[15,15,48,48,48,48,48,48,48,]),'empty':([11,25,26,30,36,70,96,97,146,149,152,153,155,160,170,],[16,31,16,31,65,65,130,130,130,65,65,65,65,166,65,]),'type':([11,25,26,30,36,70,96,97,146,149,152,153,155,170,],[17,32,17,32,17,17,127,127,127,17,17,17,17,17,]),'array_decl':([11,26,36,70,149,152,153,155,170,],[18,18,18,18,18,18,18,18,18,]),'fill_goto_main':([12,],[23,]),'function_decl_list':([25,30,],[29,37,]),'function_decl':([25,30,],[30,30,]),'start_main':([28,],[36,]),'stmt_list':([36,70,149,152,153,155,170,],[41,98,156,157,158,159,171,]),'stmt':([36,70,149,152,153,155,170,],[42,42,42,42,42,42,42,]),'assign':([36,70,149,152,153,155,170,],[43,43,43,43,43,43,43,]),'print':([36,70,149,152,153,155,170,],[44,44,44,44,44,44,44,]),'conditional':([36,70,149,152,153,155,170,],[45,45,45,45,45,45,45,]),'loop':([36,70,149,152,153,155,170,],[46,46,46,46,46,46,46,]),'function_call':([36,64,70,71,72,73,74,75,89,115,116,117,124,125,133,135,149,152,153,155,170,],[47,88,47,88,88,88,88,88,88,88,88,88,141,141,88,88,47,47,47,47,47,]),'built_in_function':([36,70,149,152,153,155,170,],[49,49,49,49,49,49,49,]),'return_stmt':([36,70,149,152,153,155,170,],[50,50,50,50,50,50,50,]),'expr':([64,71,72,73,74,75,89,133,135,],[85,99,101,102,104,104,126,148,150,]),'term':([64,71,72,73,74,75,89,115,116,117,133,135,],[86,86,86,86,86,86,86,137,138,139,86,151,]),'factor':([64,71,72,73,74,75,89,115,116,117,124,125,133,135,],[87,87,87,87,87,87,87,87,87,87,140,142,87,87,]),'create_function_scope':([66,67,],[96,97,]),'arg_list':([72,],[100,]),'comp_expr':([74,75,],[103,105,]),'comp_op':([85,99,101,102,104,126,148,150,],[117,117,117,117,135,117,117,117,]),'param_list':([96,97,146,],[128,131,154,]),'param':([96,97,146,],[129,129,129,]),'else_stmt':([160,],[164,]),'else_part':([169,],[170,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM ID SEMICOLON placeholder_goto_main create_scopes global_scope main_function end_scopes fill_goto_main','program',9,'p_program','parser_2.py',31),
  ('placeholder_goto_main -> <empty>','placeholder_goto_main',0,'p_placeholder_goto_main','parser_2.py',36),
  ('global_scope -> VARIABLES LBRACE decl_list RBRACE function_decl_list','global_scope',5,'p_global_scope','parser_2.py',42),
  ('global_scope -> VARIABLES LBRACE decl_list RBRACE','global_scope',4,'p_global_scope','parser_2.py',43),
  ('function_decl_list -> function_decl function_decl_list','function_decl_list',2,'p_function_decl_list','parser_2.py',51),
  ('function_decl_list -> empty','function_decl_list',1,'p_function_decl_list','parser_2.py',52),
  ('main_function -> MAIN LPAREN RPAREN LBRACE start_main stmt_list RBRACE','main_function',7,'p_main_function','parser_2.py',60),
  ('start_main -> <empty>','start_main',0,'p_start_main','parser_2.py',65),
  ('fill_goto_main -> <empty>','fill_goto_main',0,'p_fill_goto_main','parser_2.py',72),
  ('create_scopes -> <empty>','create_scopes',0,'p_create_scopes','parser_2.py',78),
  ('end_scopes -> <empty>','end_scopes',0,'p_end_scopes','parser_2.py',82),
  ('decl_list -> decl SEMICOLON decl_list','decl_list',3,'p_decl_list','parser_2.py',87),
  ('decl_list -> decl SEMICOLON','decl_list',2,'p_decl_list','parser_2.py',88),
  ('decl_list -> empty','decl_list',1,'p_decl_list','parser_2.py',89),
  ('decl -> type ID','decl',2,'p_decl','parser_2.py',97),
  ('decl -> array_decl','decl',1,'p_decl','parser_2.py',98),
  ('type -> INT','type',1,'p_type','parser_2.py',103),
  ('type -> FLOAT','type',1,'p_type','parser_2.py',104),
  ('type -> STRING','type',1,'p_type','parser_2.py',105),
  ('type -> BOOL','type',1,'p_type','parser_2.py',106),
  ('stmt_list -> stmt SEMICOLON stmt_list','stmt_list',3,'p_stmt_list','parser_2.py',111),
  ('stmt_list -> stmt SEMICOLON','stmt_list',2,'p_stmt_list','parser_2.py',112),
  ('stmt -> assign','stmt',1,'p_stmt','parser_2.py',121),
  ('stmt -> print','stmt',1,'p_stmt','parser_2.py',122),
  ('stmt -> conditional','stmt',1,'p_stmt','parser_2.py',123),
  ('stmt -> loop','stmt',1,'p_stmt','parser_2.py',124),
  ('stmt -> function_call','stmt',1,'p_stmt','parser_2.py',125),
  ('stmt -> decl','stmt',1,'p_stmt','parser_2.py',126),
  ('stmt -> built_in_function','stmt',1,'p_stmt','parser_2.py',127),
  ('stmt -> return_stmt','stmt',1,'p_stmt','parser_2.py',128),
  ('built_in_function -> TEACH_SUM LPAREN RPAREN','built_in_function',3,'p_built_in_function','parser_2.py',133),
  ('built_in_function -> TEACH_SUBSTRACTION LPAREN RPAREN','built_in_function',3,'p_built_in_function','parser_2.py',134),
  ('built_in_function -> TEACH_MULTIPLICATION LPAREN RPAREN','built_in_function',3,'p_built_in_function','parser_2.py',135),
  ('built_in_function -> TEACH_DIVISION LPAREN RPAREN','built_in_function',3,'p_built_in_function','parser_2.py',136),
  ('built_in_function -> TEACH_IF LPAREN RPAREN','built_in_function',3,'p_built_in_function','parser_2.py',137),
  ('built_in_function -> TEACH_WHILE LPAREN RPAREN','built_in_function',3,'p_built_in_function','parser_2.py',138),
  ('built_in_function -> TEACH_FUNCTION_DECLARATION LPAREN RPAREN','built_in_function',3,'p_built_in_function','parser_2.py',139),
  ('built_in_function -> TEACH_FUNCTION_CALL LPAREN RPAREN','built_in_function',3,'p_built_in_function','parser_2.py',140),
  ('built_in_function -> AYUDA LPAREN RPAREN','built_in_function',3,'p_built_in_function','parser_2.py',141),
  ('assign -> ID EQUALS expr','assign',3,'p_assign','parser_2.py',152),
  ('expr -> expr PLUS term','expr',3,'p_expr','parser_2.py',165),
  ('expr -> expr MINUS term','expr',3,'p_expr','parser_2.py',166),
  ('expr -> expr comp_op term','expr',3,'p_expr','parser_2.py',167),
  ('expr -> term','expr',1,'p_expr','parser_2.py',168),
  ('term -> term MULTIPLY factor','term',3,'p_term','parser_2.py',193),
  ('term -> term DIVIDE factor','term',3,'p_term','parser_2.py',194),
  ('term -> factor','term',1,'p_term','parser_2.py',195),
  ('term -> function_call','term',1,'p_term','parser_2.py',196),
  ('factor -> LPAREN expr RPAREN','factor',3,'p_factor','parser_2.py',219),
  ('factor -> CTEI','factor',1,'p_factor','parser_2.py',220),
  ('factor -> FLOAT_NUMBER','factor',1,'p_factor','parser_2.py',221),
  ('factor -> STRING_LITERAL','factor',1,'p_factor','parser_2.py',222),
  ('factor -> TRUE','factor',1,'p_factor','parser_2.py',223),
  ('factor -> FALSE','factor',1,'p_factor','parser_2.py',224),
  ('factor -> ID','factor',1,'p_factor','parser_2.py',225),
  ('factor -> function_call','factor',1,'p_factor','parser_2.py',226),
  ('print -> PRINT COLON expr','print',3,'p_print','parser_2.py',265),
  ('conditional -> IF LPAREN comp_expr RPAREN LBRACE stmt_list RBRACE else_stmt','conditional',8,'p_conditional','parser_2.py',271),
  ('conditional -> IF LPAREN comp_expr RPAREN LBRACE stmt_list RBRACE','conditional',7,'p_conditional','parser_2.py',272),
  ('comp_expr -> expr comp_op expr','comp_expr',3,'p_comp_expr','parser_2.py',282),
  ('comp_op -> LESS_THAN','comp_op',1,'p_comp_op','parser_2.py',304),
  ('comp_op -> GREATER_THAN','comp_op',1,'p_comp_op','parser_2.py',305),
  ('comp_op -> LESS_EQUAL','comp_op',1,'p_comp_op','parser_2.py',306),
  ('comp_op -> GREATER_EQUAL','comp_op',1,'p_comp_op','parser_2.py',307),
  ('comp_op -> EQUAL_EQUAL','comp_op',1,'p_comp_op','parser_2.py',308),
  ('comp_op -> NOT_EQUAL','comp_op',1,'p_comp_op','parser_2.py',309),
  ('else_stmt -> ELSE LBRACE else_part stmt_list RBRACE','else_stmt',5,'p_else_stmt','parser_2.py',315),
  ('else_stmt -> empty','else_stmt',1,'p_else_stmt','parser_2.py',316),
  ('else_part -> <empty>','else_part',0,'p_else_part','parser_2.py',325),
  ('loop -> WHILE LPAREN comp_expr RPAREN LBRACE stmt_list RBRACE','loop',7,'p_loop','parser_2.py',331),
  ('create_function_scope -> <empty>','create_function_scope',0,'p_create_function_scope','parser_2.py',338),
  ('function_decl -> type ID LPAREN create_function_scope param_list RPAREN LBRACE stmt_list end_scopes RBRACE','function_decl',10,'p_function_decl','parser_2.py',346),
  ('function_decl -> VOID ID LPAREN create_function_scope param_list RPAREN LBRACE stmt_list end_scopes RBRACE','function_decl',10,'p_function_decl','parser_2.py',347),
  ('return_stmt -> RETURN expr','return_stmt',2,'p_return_stmt','parser_2.py',365),
  ('return_stmt -> empty','return_stmt',1,'p_return_stmt','parser_2.py',366),
  ('function_call -> ID LPAREN arg_list RPAREN','function_call',4,'p_function_call','parser_2.py',382),
  ('arg_list -> arg_list COMMA expr','arg_list',3,'p_arg_list','parser_2.py',389),
  ('arg_list -> expr','arg_list',1,'p_arg_list','parser_2.py',390),
  ('param_list -> param COMMA param_list','param_list',3,'p_param_list','parser_2.py',398),
  ('param_list -> param','param_list',1,'p_param_list','parser_2.py',399),
  ('param_list -> empty','param_list',1,'p_param_list','parser_2.py',400),
  ('param -> type ID','param',2,'p_param','parser_2.py',408),
  ('array_decl -> type ID LBRACKET CTEI RBRACKET','array_decl',5,'p_array_decl','parser_2.py',424),
  ('empty -> <empty>','empty',0,'p_empty','parser_2.py',455),
]
