#ImportData

import pandas
from qpython import qconnection

q = qconnection.QConnection(host='localhost',port = 5000, pandas=True)
q.open()

qscript=os.path.abspath(os.path.join(os.getcwd(), os.pardir))+"\\KDB\\histo.q"

#q.sync('show "{}"'.format(str(qscript)))
# to do - instruct q process to load KDB histo data for all syms 