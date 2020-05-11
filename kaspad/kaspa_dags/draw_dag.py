import os
import subprocess
from kaspy_tools.kaspad import kaspad_constants
from kaspy_tools.logs import config_logger
import pygraphviz as pgv
from kaspy_tools import kaspy_tools_constants

KT_logger = config_logger.get_kaspy_tools_logger()


def draw_graph_image(v_blocks, fname):
    graph = make_dag_graph(v_blocks)
    pwd = os.getcwd()  # Where am I?
    os.chdir(kaspy_tools_constants.GRAPH_IMAGES_PATH)
    graph_to_files(graph, fname)
    export_graph_to_image(graph, fname)
    os.chdir(pwd)  # Go back


def make_dag_graph(v_blocks):
    graph = pgv.AGraph()
    add_nodes_and_edges(graph, v_blocks)
    return graph


def add_nodes_and_edges(graph, v_blocks):
    for block in v_blocks:
        confirmations = str(block['confirmations'])
        hash_str = block['hash'][kaspad_constants.PARTIAL_HASH_SIZE:]
        conf_str = 'confirmations:' + str(block['confirmations'])
        bluescore_str = 'blue score:' + str(block['blueScore'])
        details_label = \
            f'<<TABLE BORDER="0">' \
            f'<TR><TD>{hash_str}</TD></TR>' \
            f'<TR><TD>{conf_str}</TD></TR>' \
            f'<TR><TD>{bluescore_str}</TD></TR>' \
            f'</TABLE>>'
        if block['isChainBlock'] == True:
            graph.add_node(block['hash'][kaspad_constants.PARTIAL_HASH_SIZE:], shape='square', style='filled',
                           fillcolor='cyan', label=details_label)
        else:
            graph.add_node(block['hash'][kaspad_constants.PARTIAL_HASH_SIZE:], label=details_label)

        for parent in block['parentHashes']:
            if parent == block['selectedParentHash']:
                graph.add_edge(block['hash'][kaspad_constants.PARTIAL_HASH_SIZE:],
                               parent[kaspad_constants.PARTIAL_HASH_SIZE:], color='blue')
            else:
                graph.add_edge(block['hash'][kaspad_constants.PARTIAL_HASH_SIZE:],
                               parent[kaspad_constants.PARTIAL_HASH_SIZE:], color='black')


def export_graph_to_image(graph, fname):
    cmd_args = []
    cmd_args.extend(['dot', '-Tpng', fname + '.dot', '-o', fname + '.png'])
    completed_process = subprocess.run(args=cmd_args, capture_output=True)


def graph_to_files(graph, fname):
    graph.layout(prog='dot')
    graph.write(fname + '.dot')
