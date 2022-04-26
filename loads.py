import sqlite3 as sq
import pandas as pd
import yahoo_fin.stock_info as si
import datetime
import numpy as np


class stock:
    def __init__(self,ticker:str) -> None:
        self.ticker = ticker


    def income(self, tipo: str= "anual"):
        #Obtengo último estado cargado
        p = funciones("income").ultCargado(self.ticker , self.tipo) 
        #p es el último estado de resultados cargados
        
        if tipo == "anual":
            btipo = True
        else:
            btipo = False
        
        data=pd.DataFrame(si.get_income_statement(self.ticker,yearly = btipo))
        fecha = max(data.iloc[0,:].index)
        #fecha es último estado de resultados disponible
        p = datetime.datetime.strptime(p, '%Y-%m-%d')
        #transformo a datetime para comparar
        
        if fecha > p:#confirmo si hay algo para cargar
            data.replace(to_replace=[None], value=0, inplace=True)
            indice = data.index#lista con los índices
            
            #chequeo de columnas en tabla
            rdo = funciones("income").checkCol()
            
            #lista de campos a insertar
            sql1 = "(ticker, fecha,tipo"
            for i in indice:
                sql1 = sql1 + "," + i
                if i not in rdo:
                    con = sq.connect("/home/rodrigo/Documentos/eFinanc.db")
                    cursor = con.cursor()
                    sql = "alter TABLE income add " + i +" numeric;;"
                    cursor.execute(sql)
                    con.commit()
                    cursor.close()
                    con.close()
            
            sql1 = sql1 + ")"
            #print(sql1)

            f=0#iterador de fechas
            while f < len(data.iloc[0,:].index):
                fIterada = data.iloc[0,:].index[f]
                if fIterada > p:
                    #valores a insertar ingresos anual
                    sql2 = "('" + self.ticker + "','"+str(fIterada)+"','"+ tipo +"'"
                    for v in data.iloc[:,f]:
                        sql2 = sql2+","+str(v)
                    sql2 = sql2 + ")"
                    f+=1
                    #print(sql2)
                
                    try:
                        con = sq.connect("/home/rodrigo/Documentos/eFinanc.db")
                        #print(i)
                        cursor = con.cursor()
                        sql = "insert into income " + sql1 + " values " + sql2 +";"
                        #print(sql)
                        cursor.execute(sql)
                        con.commit()
                        cursor.close()
                        con.close()
                        
                    except sq.Error as error:
                        print(error)
    
    #--------------------Cashflow--------------------------
    def cash(self, tipo: str= "anual"):
        #Obtengo último estado cargado
        p = funciones("fFondos").ultCargado(self.ticker,self.tipo)
        #p es el último estado cargado
        
        if tipo == "anual":
            btipo = True
        else:
            btipo = False
        data=pd.DataFrame(si.get_cash_flow(self.ticker,yearly = btipo))
        fecha = max(data.iloc[0,:].index)
        #fecha es último estado de resultados disponible
        p = datetime.datetime.strptime(p, '%Y-%m-%d')
        #transformo a datetime para comparar
        
        if fecha > p:#confirmo si hay algo para cargar
            data.replace(to_replace=[None], value=0, inplace=True)
            data.replace(to_replace=np.nan, value=0, inplace=True)
            indice = data.index#lista con los índices

            #chequeo de columnas en tabla
            rdo = funciones("fFondos").checkCol()
            
            #lista de campos a insertar
            sql1 = "(ticker, fecha,tipo"
            for i in indice:
                sql1 = sql1 + "," + i
                
                if i not in rdo:
                    con = sq.connect("/home/rodrigo/Documentos/eFinanc.db")
                    cursor = con.cursor()
                    sql = "alter TABLE fFondos add " + i +" numeric;;"
                    cursor.executescript(sql)
                    con.commit()
                    cursor.close()
                    con.close()
            
            sql1 = sql1 + ")"
            #print(sql1)

            f=0#iterador de fechas
            while f < len(data.iloc[0,:].index):
                fIterada = data.iloc[0,:].index[f]
                if fIterada > p:
                    #valores a insertar ingresos anual
                    sql2 = "('" + self.ticker + "','"+str(fIterada)+"','"+ tipo +"'"
                    for v in data.iloc[:,f]:
                        sql2 = sql2+","+str(v)
                    sql2 = sql2 + ")"
                    f+=1
                    #print(sql2)
                
                    try:
                        con = sq.connect("/home/rodrigo/Documentos/eFinanc.db")
                        #print(i)
                        cursor = con.cursor()
                        sql = "insert into fFondos " + sql1 + " values " + sql2 +";"
                        #print(sql)
                        cursor.execute(sql)
                        con.commit()
                        cursor.close()
                        con.close()
                        
                    except sq.Error as error:
                        print(error)
    
class funciones:
    def __init__(self,tabla:str) -> None:
        self.tabla = tabla
    
    def checkCol(self):
        #chequeo de columnas en tabla
            import sqlalchemy as db
            engine = db.create_engine("sqlite:////home/rodrigo/Documentos/eFinanc.db")
            connection = engine.connect()
            metadata = db.MetaData()
            check = db.Table(self.tabla, metadata, autoload=True, autoload_with=engine)
            rdo = []
            for i in (check.columns.keys()):
                rdo.append(i)
            connection.close()
            return rdo
    
    def ultCargado(self,ticker: str,tipo: str):
         #Obtengo último estado cargado
        con = sq.connect("/home/rodrigo/Documentos/eFinanc.db")
        cursor = con.cursor()
        sql = """SELECT iif((t1.dd ISNULL),"2010-01-01", strftime('%Y-%m-%d',t1.dd)) as """ + tipo + """
        from Tickers left join
        (SELECT Ticker, max(fecha) as dd
        from """ + self.tabla +""" GROUP by ticker,tipo
        HAVING tipo = '""" + tipo +"""' and ticker = '""" + ticker + """') as t1 on Tickers.Ticker = t1.ticker
        WHERE Tickers.ticker = '""" + ticker + "';"
        pk = cursor.execute(sql).fetchone()
        con.commit()
        cursor.close()
        con.close()
        p = str(pk).replace("(", "").replace(",)", "").replace("'", "")
        return p  
