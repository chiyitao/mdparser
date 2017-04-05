import sys      # for test the generated intermediate file
import reportlab     # for pdf generation

# This is a parser for github style markdown parser.

LINE_BEGIN = 'LINE_BEGIN'
LINE_END = 'LINE_END'

ERROR_INFO_POUND_NO_SPACE = 'non-space character after pound key'

NODE_TYPE_EMTPY_LINE = 'empty line'
NODE_TYPE_ERROR = 'error'
NODE_TYPE_TITLE = 'title'
NODE_TYPE_ITEM = 'item'

class physical_node():
    def __init__():
        # attributes
        self.node_type = ''
        self.node_position = (-1, -1)
        self.node_text = ''
        self.error_info = ''

def parser(md_str):

    lines = md_str.split('\n')
    
    for line in lines:
        physical_nodes = parse_line(line)

def real_type_node(node_type, node_begin, node_end, node_text, error_info):
    real_node = physical_node()
    real_node.node_type = node_type()
    real_node.node_position = (node_begin, node_end) # end position is not contained.
    real_node.node_text = node_text
    real_node.error_info = error_info
    return real_node

def parse_line(line):

    physical_nodes = []
    
    # 1. Title

    # Begins with one or more pound keys(#). With one or more
    # whitespaces following the pound key sequence.

    if line == '':
        
        # empty_node = physical_node()
        # empty_node.node_type = NODE_TYPE_EMPTY_LINE
        # empty_node.node_position = (LINE_BEGIN, LINE_END)
        # empty_node.node_text = ''
        # empty_node.error_info = ''
        empty_node = real_type_node(NODE_TYPE_EMPTY_LINE, 0, 1, '', '')
        physical_nodes.append(empty_node)
        return physical_nodes

    sign_s = 0     # sign start 
    sign_e = 0     # sign end 
    char_pt_i = 0     # character pointer i
    char_pt_j = 0     # character pointer j

    line_len = len(line)

    for char_pt_i in range(0, line_len):
        if char_pt_i == 0:
            if line[char_pt_i] == '#':
                title_level = 1 # at least level 1
                title_sign_s = char_pt_i # 0
                while line[title_sign_s + title_level] == '#':
                    title_level += 1

                char_pt_j = title_sign_s + title_level
                if line[char_pt_j + 1] != ' ':                    
                    # error_node = physical_node()
                    # error_node.node_type = NODE_TYPE_ERROR
                    # error_node.node_position = (char_pt_j + 1, char_pt_j + 2)
                    # error_node.node_text = ''
                    # error_node.error_info = ''
                    error_node = real_type_node(NODE_TYPE_ERROR, char_pt_j + 1, char_pt_j + 2, '', '')
                    physical_nodes.append(error_node)
                    break
                else:
                    # title_node = physical_node()
                    # title_node.node_type = str(title_level) + ' ' + NODE_TYPE_TITLE
                    # title_node.node_position = (char_pt_j + 2, line_len)      
                    # title_node.node_text = line[char_pt_j + 2:line_len]
                    # title_node.error_info = ''
                    cur_title_node_type = str(title_level) + ' ' + NONE_TYPE_TITLE
                    title_node = real_type_node(cur_title_node_type,
                                                char_pt_j + 2,
                                                line_len,
                                                line[(char_pt_j + 2):line_len],
                                                '')
                    physical_nodes.append(title_node)
                    break

            if line[char_pt_i] == '*':
                # may be an item or a bold or an italic word
                # it depends on the next character
                if line[char_pt_i + 1] == ' ':
                    # it is an item
                    # item_node = physical_node()
                    # item_node.node_type = NODE_TYPE_ITEM
                    # item_node.node_position = (char_pt_i + 2, line_len)
                    # item_node.node_text = line[char_pt_i + 2 : line_len]
                    # item_node.error_info = ''
                    item_node = real_type_node(NODE_TYPE_ITEM,
                                               char_pt_i + 2,
                                               line_len,
                                               line[(char_pt_i + 2) : line_len],
                                               '')
                    physical_nodes.append(item_node)
                else:
                    # text in line may contain bold or italic or link
                    # or nested code
                    physical_nodes = inner_line_parse(line)
                        

        char_pt_i += 1
        
    return physical_nodes # finally
    
def inner_line_parse(line_str):
    italic_sign_star = '*'
    italic_sign_underline = '_'
    bold_sign_star = '**'
    bold_sign_underline = '__'
    # using two stack to retrieve the current state of the text line.
    char_stack = []
    status_stack = []
    


