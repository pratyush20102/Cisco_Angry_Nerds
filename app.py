import streamlit as st
import pandas as pd
import base64
from io import StringIO
import graphviz
import seaborn as sb


#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(page_title='DataViz: A visualizer and parser for ACL data', layout='wide')
#---------------------------------#


# Download CSV data
def filedownload(df, filename):
    txt = df.to_txt(index=False)
    b64 = base64.b64encode(txt.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/txt;base64,{b64}" download={filename}>Download {filename} File</a>'
    return href

# def imagedownload(plt, filename):
#     s = io.BytesIO()
#     plt.savefig(s, format='pdf', bbox_inches='tight')
#     plt.close()
#     b64 = base64.b64encode(s.getvalue()).decode()  # strings <-> bytes conversions
#     href = f'<a href="data:image/png;base64,{b64}" download={filename}>Download {filename} File</a>'
#     return href

#---------------------------------#
st.write("""
# DataViz: A visualizer and parser for ACL data     
""")

#---------------------------------#

# Sidebar - Collects user input features into dataframe
with st.sidebar.header('1. Upload your TXT file'):
    uploaded_file2 = st.sidebar.file_uploader("Upload your input TXT file")
    uploaded_file = (uploaded_file2)

    # st.write((uploaded_file))
    st.sidebar.markdown("""[Example TXT input file](https://raw.githubusercontent.com/k-rishabh6172/cisco/main/Generator/Input.txt)""")
# #---------------------------------#
# # Main logic
# for I/O for local system
import sys

# For fast I/O
input = sys.stdin.readline
# input = sys.stdin.readline
# print = sys.stdout.write
 
# importing libraries
import fileinput
from collections import defaultdict, deque

# Code
Count = 0
rules = defaultdict(list)
rule = -1
adj = defaultdict(list)
Port = defaultdict(set)
seen = set()
user_port = {}
user_user = {}
edge_list = []

if uploaded_file != None:
    for line in uploaded_file:
        line = line.decode()
        if(line[0] == "C"):
            line_list = line.split()
            From = int(line_list[4])
            To = int(line_list[6])
            rule = int(line_list[-1][5: ])
            if(tuple[From, To] in seen):
                continue
            seen.add(tuple([From, To]))
            for permissions in rules[rule]:
                adj[From].append([To, permissions]) # directed graph of form adj[u].append([v, wt])
                edge_list.append([From, To])
                Port[permissions].add(tuple([From, To])) # This Port contain the added From-To pair
                if From in user_port:
                    if permissions in user_port[From]:
                        user_port[From][permissions].append(To)
                    else:
                        user_port[From][permissions]=[To]
                else:
                    user_port[From] = {}
                    user_port[From][permissions] = [To]
                if From in user_user:
                    if To in user_user[From]:
                        user_user[From][To].append(permissions)
                    else:
                        user_user[From][To]=[permissions]
                else:
                    user_user[From] = {}
                    user_user[From][To] = [permissions]
        else:
            if(line[0] == "I"):
                line_list = line.split()
                rule = int(line_list[-1][5: ])
            else:
                line_list = line.split()
                # permit = 1, deny = 0
                status = 0 # initial deny
                if(line_list[1] == "permit"):
                    status = 1 # status changes to permit
                else:
                    continue
                port = int(line_list[-1])
                rules[rule].append(port) # All the status and ports in sorted order of the operations for the rules " rule "

ans = []
for i in range(65536):
    ans.append(len(adj[i]))
ans2 = [[0 for i in range(256)] for i in range(256)]
cur = 0
for i in range(256):
    for j in range(256):
        ans2[i][j] = ans[cur]
        cur += 1

# Queries
def query1(query): # Type 1: query
    query = query.split()
    node = int(query[0])
    protocols={}
    if node in user_port:
        for i in user_port[node].keys():
            protocols[i]=len(user_port[node][i])
    chart_data=[]
    for i in range(256):
        if i in protocols:
            chart_data.append([i,protocols[i]])
        else:
            chart_data.append([i,0])

    # import numpy as np
    # import plotly.figure_factory as ff

    # hist_data = []
    # group_labels = []
    # temp1 = []
    # temp2 = []
    # for i, j in chart_data:
    #     hist_data.append(j)
    #     group_labels.append(i)

    # # Create distplot with custom bin_size
    # fig = ff.create_distplot(
    #         hist_data, group_labels)

    # # Plot!
    # st.plotly_chart(fig, use_container_width=True)

    return adj[node],chart_data

def query2(query): # Type 2: query
    query = query.split()
    node, port = query
    node = int(node)
    port = int(port)
    if(len(user_port[node][port]) == 0):
        return "No Connections"
    return user_port[node][port]

def query3(query): # Type3: query
    query = query.split()
    node1, node2, status = query
    node1 = int(node1)
    node2 = int(node2)
    status = int(status)
    allowed2=[]
    denied2=[]
    for i in range(256):
        denied2.append(i)
    if(node1 in user_user):
        if node2 in user_user[node1]:
            allowed=user_user[node1][node2]
            if status:
                return allowed
            else:
                denied=[]
                allowed_set=set(allowed)
                for i in range(256):
                    if i not in allowed_set:
                        denied.append(i)
                return denied
        else:
            if status:
                return allowed2
            else:
                return denied2
    else:
        if status:
            return allowed2
        else:
            return denied2

def query4(query): # Type4: query
    query = query.split()
    node1, node2, port = query
    node1 = int(node1)
    node2 = int(node2)
    port = int(port)
    if(tuple([node1, node2]) in Port[port]):
        cgraph = graphviz.Digraph()
        cgraph.edge(str(node1), str(node2))
        st.graphviz_chart(cgraph)
        return "Yes"
    else:
        return "No"
    
def query5(): # Type5: query
    return 65536 * 65536 - len(seen)

def query6(query): # Type6: query
    query = query.split()
    port = int(query[0])
    if(len(Port[port]) == 0):
        return "No Connections"
    return list(Port[port])

import plotly.express as px

if (uploaded_file != None):
    fig = px.imshow(ans2, text_auto=True)
    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)

# Displays the dataset
st.subheader('1. Data File')

if uploaded_file != None:
    #code for displaying the graph:
    st.subheader('1. Graph of the input file')

    # Create a graphlib graph object
    graph = graphviz.Digraph()
    for u, v in edge_list:
        graph.edge(str(u), str(v))

    st.graphviz_chart(graph)

    #query region starts:
    st.subheader('2. Querying and Visualisation')

    #dropdown for the query:
    option = st.selectbox(
        'Select the required query:',
        ('Connections of a group', 'Via which protocol', 'Boolean Communications between two groups', 'Commmunication using particular protocol', 'Number of groups not connected', 'Check directly connected'))

    st.write('You selected:', option)
    
    #query1: 
    if (option == "Connections of a group"):
        st.markdown("**Description of Query 1: 1 GroupNumber, where the detailed status of GroupNumber is returned. The query result is a 2D list wherein the first element is the GroupNumber to which it's connected. The second integer is the protocol port number. Example: 1 6 returns [[18,6]], means the group 1 is connected to group 18 via port 6.**")
        
        query = st.text_area("Enter the query in correct format: ")
        if(len(query)):
            st.write(query1(query))
    elif (option == "Via which protocol"):
        st.markdown("**Description of Query 2: GroupNumber ProtocolNumber, where the function returns the different GroupNumbers to which the given GroupNumber is connected via the given Protocol Number. For example: if 82 6 returns [56,89], it means that GroupNumber 6 communicates with GroupNumbers 56 and 89 via TCP.**")
        query = st.text_area("Enter the query in correct format: ")
        if(len(query)):
            st.write(query2(query))
    elif (option == "Boolean Communications between two groups"):
        st.markdown("**Description of Query 3: GroupNumber1 GroupNumber2 Flag, where the function returns the ProtocolNumbers using which GroupNumber1 can directly communicate with GroupNumber2 if Flag has been set to 1. If the value of Flag has been set to 0, we get the ProtocolNumbers using which GroupNumber1 cannot communicate with GroupNumber2. For example, if 34 56 1 returns [6,45], it means that GroupNumber 34 communicates with 56 via TCP and IRDP.**")
        query = st.text_area("Enter the query in correct format: ")
        if(len(query)):
            ans = query3(query)
            numberToPort={0: 'HOPOPT', 1: 'ICMP', 2: 'IGMP', 3: 'GGP', 4: 'IP-in-IP', 5: 'ST', 6: 'TCP', 7: 'CBT', 8: 'EGP', 9: 'IGP', 10: 'BBN-RCC-MON', 11: 'NVP-II', 12: 'PUP', 13: 'ARGUS', 14: 'EMCON', 15: 'XNET', 16: 'CHAOS', 17: 'UDP', 18: 'MUX', 19: 'DCN-MEAS', 20: 'HMP', 21: 'PRM', 22: 'XNS-IDP', 23: 'TRUNK-1', 24: 'TRUNK-2', 25: 'LEAF-1', 26: 'LEAF-2', 27: 'RDP', 28: 'IRTP', 29: 'ISO-TP4', 30: 'NETBLT', 31: 'MFE-NSP', 32: 'MERIT-INP', 33: 'DCCP', 34: '3PC', 35: 'IDPR', 36: 'XTP', 37: 'DDP', 38: 'IDPR-CMTP', 39: 'TP++', 40: 'IL', 41: 'IPv6', 42: 'SDRP', 43: 'IPv6-Route', 44: 'IPv6-Frag', 45: 'IDRP', 46: 'RSVP', 47: 'GRE', 48: 'MHRP', 49: 'BNA', 50: 'ESP', 51: 'AH', 52: 'I-NLSP', 53: 'SWIPE', 54: 'NARP', 55: 'MOBILE', 56: 'TLSP', 57: 'SKIP', 58: 'IPv6-ICMP', 59: 'IPv6-NoNxt', 60: 'IPv6-Opts', 61: 61, 62: 'CFTP', 63: 63, 64: 'SAT-EXPAK', 65: 'KRYPTOLAN', 66: 'RVD', 67: 'IPPC', 68: 68, 69: 'SAT-MON', 70: 'VISA', 71: 'IPCU', 72: 'CPNX', 73: 'CPHB', 74: 'WSN', 75: 'PVP', 76: 'BR-SAT-MON', 77: 'SUN-ND', 78: 'WB-MON', 79: 'WB-EXPAK', 80: 'ISO-IP', 81: 'VMTP', 82: 'SECURE-VMTP', 83: 'VINES', 84: 'IPTM', 85: 'NSFNET-IGP', 86: 'DGP', 87: 'TCF', 88: 'EIGRP', 89: 'OSPF', 90: 'Sprite-RPC', 91: 'LARP', 92: 'MTP', 93: 'AX.25', 94: 'IPIP', 95: 'MICP', 96: 'SCC-SP', 97: 'ETHERIP', 98: 'ENCAP', 99: 99, 100: 'GMTP', 101: 'IFMP', 102: 'PNNI', 103: 'PIM', 104: 'ARIS', 105: 'SCPS', 106: 'QNX', 107: 'A/N', 108: 'IPComp', 109: 'SNP', 110: 'Compaq-Peer', 111: 'IPX-in-IP', 112: 'VRRP', 113: 'PGM', 114: 114, 115: 'L2TP', 116: 'DDX', 117: 'IATP', 118: 'STP', 119: 'SRP', 120: 'UTI', 121: 'SMP', 122: 'SM', 123: 'PTP', 124: 'IS-IS over IPv4', 125: 'FIRE', 126: 'CRTP', 127: 'CRUDP', 128: 'SSCOPMCE', 129: 'IPLT', 130: 'SPS', 131: 'PIPE', 132: 'SCTP', 133: 'FC', 134: 'RSVP-E2E-IGNORE', 135: 'Mobility Header', 136: 'UDPLite', 137: 'MPLS-in-IP', 138: 'manet', 139: 'HIP', 140: 'Shim6', 141: 'WESP', 142: 'ROHC'}
            ans2=[]
            for i in ans:
                if i>142:
                    ans2.append(i)
                    continue
                ans2.append(numberToPort[i])
            st.write(ans2)
            st.write(ans)
    elif (option == "Commmunication using particular protocol"):
        st.markdown("**Description of Query 4: GroupNumber1 GroupNumber2 ProtocolNumber, where the function returns YES if GroupNumber1 is able to directly communicate with GroupNumber2 via the given ProtocolNumber and NO otherwise. For example, if 6 76 45 returns YES, it means that GroupNumbers 6 and 76 can communicate via IRDP.**")
        query = st.text_area("Enter the query in correct format: ")
        if(len(query)):
            st.write(query4(query))
    elif (option == "Number of groups not connected"):
        st.markdown("**Description of Query 5: The function returns the number of groups (connected components formed using the connections between separate GroupNumbers) that are not connected to any other groups.**")
        # query = st.text_area("Enter the query in correct format: ")
        st.write(query5())
    elif (option == "Check directly connected"):
        st.markdown("**Description of Query 6: ProtocolNumber, where the function returns a 2D list wherein the first and second elements are the GroupNumbers which are directly connected via the given ProtocolNumber. For example, if 6 returns [[45,78]], it means that GroupNumbers 45 and 78 are connected via TCP.**")
        query = st.text_area("Enter the query in correct format: ")
        if(len(query)):
            st.write(query6(query))

else:
    st.write("Upload an input file")
