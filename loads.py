import sqlite3 as sq
import pandas as pd
import yahoo_fin.stock_info as si
import datetime

class stock:
    def __init__(self,ticker:str) -> None:
        self.ticker = ticker


    def income(self, tipo: str= "anual"):
        #Obtengo último estado cargado
        con = sq.connect("/home/rodrigo/Documentos/eFinanc.db")
        cursor = con.cursor()
        sql = """SELECT iif((t1.dd ISNULL),"2010-01-01", t1.dd) as """ + tipo + """
        from Tickers left join
        (SELECT Ticker, max(fecha) as dd
        from income GROUP by ticker,tipo
        HAVING tipo = '""" + tipo +"""' and ticker = '""" + self.ticker + """') as t1 on Tickers.Ticker = t1.ticker
        WHERE Tickers.ticker = '""" + self.ticker + "';"
        pk = cursor.execute(sql).fetchone()
        con.commit()
        cursor.close()
        con.close()
        p = str(pk).replace("(", "").replace(",)", "").replace("'", "")
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
            #lista de campos a insertar
            sql1 = "(ticker, fecha,tipo"
            for i in indice:
                sql1 = sql1 + "," + i
            
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
        con = sq.connect("/home/rodrigo/Documentos/eFinanc.db")
        cursor = con.cursor()
        sql = """SELECT iif((t1.dd ISNULL),"2010-01-01", t1.dd) as """ + tipo + """
        from Tickers left join
        (SELECT Ticker, max(fecha) as dd
        from fFondos GROUP by ticker,tipo
        HAVING tipo = '""" + tipo +"""' and ticker = '""" + self.ticker + """') as t1 on Tickers.Ticker = t1.ticker
        WHERE Tickers.ticker = '""" + self.ticker + "';"
        pk = cursor.execute(sql).fetchone()
        con.commit()
        cursor.close()
        con.close()
        p = str(pk).replace("(", "").replace(",)", "").replace("'", "")
        #p es el último estado de resultados cargados
        
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
            indice = data.index#lista con los índices
            #lista de campos a insertar
            sql1 = "(ticker, fecha,tipo"
            for i in indice:
                sql1 = sql1 + "," + i
            
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
    
