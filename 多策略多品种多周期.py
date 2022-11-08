"""
关注公众号:Ctp接口量化
"""
import time
from API import *	
class MACDStrategy(Strategy):
    def __init__(self):
        super().__init__()
        # self.symbol_lsit = ["UR301","rb2301","au2212","IF2211","IC2211","i2301","eb2211","MA301"]  #订阅合约
        self.symbol_lsit = ["i2301"]  #订阅合约
        self.BarType = BarType.Time5  #K线周期
        self.StrategyType = StrategyType.Bar  #策略类型  StrategyType.Renko   StrategyType.Bar   StrategyType.Tick
    def on_tick(self, tick=None):
        print(tick.InstrumentID,tick.LastPrice)  
    def on_bar(self, tick=None, Bar=None):
        symbol = tick.InstrumentID   #合约代码
        Bid = tick.BidPrice1    #买价
        Ask = tick.AskPrice1    #卖价
        LastPrice = tick.LastPrice  #最新价
        #print(symbol) #合约
        #print(tick.LastPrice) #合约tick.UpdateTime
        # print(tick.UpdateTime) #合约tick.UpdateTime
        # print(Bar[0]["symbol"]) #合约
        kline = Bar[0]["data"]    # K 线数据
        if len(kline) <= 35:   # 小于35 条 退出 
            return   
        # K,D,J  = self.KDJ(kline) # 取KDJ指标数组
        # UP,MB,DN  = self.BOLL(kline) # 取BOLL指标数组
        # EMA  = self.EMA(kline,60) # 取EMA指标数组
        # RSI  = self.RSI(kline) # 取RSI指标数组
        # MA1  = self.MA(kline,30) # 取MA指标数组Channels
        # MA2  = self.MA(kline,60) # 取MA指标数组Channels
        dif,dea,macd  = self.MACD(kline) # 取MACD指标数组
        close,High,low = self.tick(kline)      # 取收盘价数组 # 获取最新价格（卖价）
        # print(self.Get_Position(symbol))
        Pos = self.GetPosition(symbol)
        # print(Pos)
        # 开多单
        if Pos["Direction"]=="None" and dif[-1]>dea[-1] and dif[-2] < dea[-2] and dea[-1] > 0:
            print(symbol) #合约
            print("MACD策略开多")
            最低价 = min(low[-10:])
            止盈 = Ask + (Ask-最低价)*3
            # self.send(symbol, DirectionType.Buy, OffsetType.Open, Ask, 3, OrderType.Limit)  # # OrderType.FOK   OrderType.FAK   OrderType.Market
            self.send(symbol, DirectionType.Buy, OffsetType.Open, Ask, 3, OrderType.Limit,止损=最低价,止盈=止盈,移动止损=最低价)  # # OrderType.FOK   OrderType.FAK   OrderType.Market
        # # 开空单
        if Pos["Direction"]=="None" and dif[-1]<dea[-1] and dif[-2] > dea[-2] and dea[-1] < 0:
            print(symbol) #合约
            print("MACD策略开空")
            最高价 = max(High[-10:])
            止盈 = Bid - (最高价-Bid)*3
            # self.send(symbol, DirectionType.Sell, OffsetType.Open, Bid, 3, OrderType.Limit)   # # OffsetType.Open   OffsetType.Close   OffsetType.CloseToday  OffsetType.CloseYesterday
            self.send(symbol, DirectionType.Sell, OffsetType.Open, Bid, 3, OrderType.Limit,止损=最高价,止盈=止盈,移动止损=最高价)   # # OffsetType.Open   OffsetType.Close   OffsetType.CloseToday  OffsetType.CloseYesterday
        # # 平多单
        if Pos["Direction"]==DirectionType.Buy and dif[-1]<dea[-1] and dif[-2] > dea[-2]:
            print(symbol) #合约
            print("MACD策略平多单")
            self.send(symbol, DirectionType.Sell, OffsetType.Close, Bid, Pos['Volume'], OrderType.Limit)         
        # # 平空单        
        if Pos["Direction"]==DirectionType.Sell and dif[-1]>dea[-1] and dif[-2] < dea[-2]:
            print(symbol) #合约
            print("MACD策略平空单")
            self.send(symbol, DirectionType.Buy, OffsetType.Close, Ask, Pos['Volume'], OrderType.Limit)
        if 'kwargs' in Pos.keys():
            # print(Pos["kwargs"])
            if Pos["Direction"]==DirectionType.Buy and LastPrice<Pos["kwargs"]["止损"]:
                print(symbol) #合约
                print("MACD策略止损多单")
                self.send(symbol, DirectionType.Sell, OffsetType.Close, Bid, Pos['Volume'], OrderType.Limit)         
            # # 平空单        
            if Pos["Direction"]==DirectionType.Sell and LastPrice>Pos["kwargs"]["止损"]:
                print(symbol) #合约
                print("MACD策略止损空单")
                self.send(symbol, DirectionType.Buy, OffsetType.Close, Ask, Pos['Volume'], OrderType.Limit)
            # # 多单 修改移动止损价
            if Pos["Direction"]==DirectionType.Buy and (LastPrice - Pos["kwargs"]["移动止损"]) > (Pos["Price"] - Pos["kwargs"]["止损"]):
                self.OrderModify(symbol, LastPrice - (Pos["Price"] - Pos["kwargs"]["止损"]))
                print("空单 修改移动止损价",LastPrice - (Pos["Price"] - Pos["kwargs"]["止损"]))
            # # 空单 修改移动止损价
            if Pos["Direction"]==DirectionType.Sell and (Pos["kwargs"]["移动止损"] - LastPrice) > (Pos["kwargs"]["止损"] - Pos["Price"]):
                self.OrderModify(symbol, LastPrice + (Pos["kwargs"]["止损"] - Pos["Price"]))
                print("空单 修改移动止损价",LastPrice + (Pos["kwargs"]["止损"] - Pos["Price"]))

class MAStrategy(Strategy):
    def __init__(self):
        super().__init__()
        # self.symbol_lsit = ["UR301","rb2301","au2212","IF2211","IC2211","i2301","eb2211","MA301"]  #订阅合约
        self.symbol_lsit = ["MA301"]  #订阅合约
        self.BarType = BarType.Time5  #K线周期
        self.StrategyType = StrategyType.Bar  #策略类型  StrategyType.Renko   StrategyType.Bar   StrategyType.Tick
    def on_tick(self, tick=None):
        print(tick.InstrumentID,tick.LastPrice)  
    def on_bar(self, tick=None, Bar=None):
        symbol = tick.InstrumentID   #合约代码
        Bid = tick.BidPrice1    #买价
        Ask = tick.AskPrice1    #卖价
        LastPrice = tick.LastPrice  #最新价
        #print(symbol) #合约
        #print(tick.LastPrice) #合约tick.UpdateTime
        # print(tick.UpdateTime) #合约tick.UpdateTime
        # print(Bar[0]["symbol"]) #合约
        kline = Bar[0]["data"]    # K 线数据
        if len(kline) <= 35:   # 小于35 条 退出 
            return   
        # K,D,J  = self.KDJ(kline) # 取KDJ指标数组
        # UP,MB,DN  = self.BOLL(kline) # 取BOLL指标数组
        # EMA  = self.EMA(kline,60) # 取EMA指标数组
        # RSI  = self.RSI(kline) # 取RSI指标数组
        MA1  = self.MA(kline,5) # 取MA指标数组Channels
        MA2  = self.MA(kline,10) # 取MA指标数组Channels
        MA3  = self.MA(kline,30) # 取MA指标数组Channels
        # dif,dea,macd  = self.MACD(kline) # 取MACD指标数组
        close,High,low = self.tick(kline)      # 取收盘价数组 # 获取最新价格（卖价）
        # print(self.Get_Position(symbol))
        Pos = self.GetPosition(symbol)
        # print(Pos)
        # 开多单
        if Pos["Direction"]=="None" and MA1[-1]>MA2[-1] and MA1[-2] < MA2[-2] and close[-1] > MA3[-1]:
            print(symbol) #合约
            print("MA策略开多")
            最低价 = min(low[-10:])
            止盈 = Ask + (Ask-最低价)*3
            # self.send(symbol, DirectionType.Buy, OffsetType.Open, Ask, 3, OrderType.Limit)  # # OrderType.FOK   OrderType.FAK   OrderType.Market
            self.send(symbol, DirectionType.Buy, OffsetType.Open, Ask, 3, OrderType.Limit,止损=最低价,止盈=止盈,移动止损=最低价)  # # OrderType.FOK   OrderType.FAK   OrderType.Market
        # # 开空单
        if Pos["Direction"]=="None" and MA1[-1]<MA2[-1] and MA1[-2] > MA2[-2] and close[-1] < MA3[-1]:
            print(symbol) #合约
            print("MA策略开空")
            最高价 = max(High[-10:])
            止盈 = Bid - (最高价-Bid)*3
            # self.send(symbol, DirectionType.Sell, OffsetType.Open, Bid, 3, OrderType.Limit)   # # OffsetType.Open   OffsetType.Close   OffsetType.CloseToday  OffsetType.CloseYesterday
            self.send(symbol, DirectionType.Sell, OffsetType.Open, Bid, 3, OrderType.Limit,止损=最高价,止盈=止盈,移动止损=最高价)   # # OffsetType.Open   OffsetType.Close   OffsetType.CloseToday  OffsetType.CloseYesterday
        # # 平多单
        if Pos["Direction"]==DirectionType.Buy and MA1[-1]<MA2[-1] and MA1[-2] > MA2[-2]:
            print(symbol) #合约
            print("MA策略平多单")
            self.send(symbol, DirectionType.Sell, OffsetType.Close, Bid, Pos['Volume'], OrderType.Limit)         
        # # 平空单        
        if Pos["Direction"]==DirectionType.Sell and MA1[-1]>MA2[-1] and MA1[-2] < MA2[-2]:
            print(symbol) #合约
            print("MA策略平空单")
            self.send(symbol, DirectionType.Buy, OffsetType.Close, Ask, Pos['Volume'], OrderType.Limit)
        if 'kwargs' in Pos.keys():
            # print(Pos["kwargs"])
            if Pos["Direction"]==DirectionType.Buy and LastPrice<Pos["kwargs"]["止损"]:
                print(symbol) #合约
                print("RSI策略止损多单")
                self.send(symbol, DirectionType.Sell, OffsetType.Close, Bid, Pos['Volume'], OrderType.Limit)         
            # # 平空单        
            if Pos["Direction"]==DirectionType.Sell and LastPrice>Pos["kwargs"]["止损"]:
                print(symbol) #合约
                print("RSI策略止损空单")
                self.send(symbol, DirectionType.Buy, OffsetType.Close, Ask, Pos['Volume'], OrderType.Limit)
            # # 多单 修改移动止损价
            if Pos["Direction"]==DirectionType.Buy and (LastPrice - Pos["kwargs"]["移动止损"]) > (Pos["Price"] - Pos["kwargs"]["止损"]):
                self.OrderModify(symbol, LastPrice - (Pos["Price"] - Pos["kwargs"]["止损"]))
                print("空单 修改移动止损价",LastPrice - (Pos["Price"] - Pos["kwargs"]["止损"]))
            # # 空单 修改移动止损价
            if Pos["Direction"]==DirectionType.Sell and (Pos["kwargs"]["移动止损"] - LastPrice) > (Pos["kwargs"]["止损"] - Pos["Price"]):
                self.OrderModify(symbol, LastPrice + (Pos["kwargs"]["止损"] - Pos["Price"]))
                print("空单 修改移动止损价",LastPrice + (Pos["kwargs"]["止损"] - Pos["Price"]))
class KDJStrategy(Strategy):
    def __init__(self):
        super().__init__()
        # self.symbol_lsit = ["UR301","rb2301","au2212","IF2211","IC2211","i2301","eb2211","MA301"]  #订阅合约
        self.symbol_lsit = ["ag2212"]  #订阅合约
        self.BarType = BarType.Time5  #K线周期
        self.StrategyType = StrategyType.Bar  #策略类型  StrategyType.Renko   StrategyType.Bar   StrategyType.Tick
    def on_tick(self, tick=None):
        print(tick.InstrumentID,tick.LastPrice)  
    def on_bar(self, tick=None, Bar=None):
        symbol = tick.InstrumentID   #合约代码
        Bid = tick.BidPrice1    #买价
        Ask = tick.AskPrice1    #卖价
        LastPrice = tick.LastPrice  #最新价
        #print(symbol) #合约
        #print(tick.LastPrice) #合约tick.UpdateTime
        # print(tick.UpdateTime) #合约tick.UpdateTime
        # print(Bar[0]["symbol"]) #合约
        kline = Bar[0]["data"]    # K 线数据
        if len(kline) <= 35:   # 小于35 条 退出 
            return   
        K,D,J  = self.KDJ(kline) # 取KDJ指标数组
        # UP,MB,DN  = self.BOLL(kline) # 取BOLL指标数组
        # EMA  = self.EMA(kline,60) # 取EMA指标数组
        # RSI  = self.RSI(kline) # 取RSI指标数组
        # MA1  = self.MA(kline,30) # 取MA指标数组Channels
        # MA2  = self.MA(kline,60) # 取MA指标数组Channels
        dif,dea,macd  = self.MACD(kline) # 取MACD指标数组
        close,High,low = self.tick(kline)      # 取收盘价数组 # 获取最新价格（卖价）
        # print(self.Get_Position(symbol))
        Pos = self.GetPosition(symbol)
        # print(Pos)
        # 开多单
        if Pos["Direction"]=="None" and K[-1]>D[-1] and K[-2] < D[-2] and dea[-1] > 0:
            print(symbol) #合约
            print("KDJ策略开多")
            最低价 = min(low[-10:])
            止盈 = Ask + (Ask-最低价)*3
            # self.send(symbol, DirectionType.Buy, OffsetType.Open, Ask, 3, OrderType.Limit)  # # OrderType.FOK   OrderType.FAK   OrderType.Market
            self.send(symbol, DirectionType.Buy, OffsetType.Open, Ask, 3, OrderType.Limit,止损=最低价,止盈=止盈,移动止损=最低价)  # # OrderType.FOK   OrderType.FAK   OrderType.Market
        # # 开空单
        if Pos["Direction"]=="None" and K[-1]<D[-1] and K[-2] > D[-2] and dea[-1] < 0:
            print(symbol) #合约
            print("KDJ策略开空")
            最高价 = max(High[-10:])
            止盈 = Bid - (最高价-Bid)*3
            # self.send(symbol, DirectionType.Sell, OffsetType.Open, Bid, 3, OrderType.Limit)   # # OffsetType.Open   OffsetType.Close   OffsetType.CloseToday  OffsetType.CloseYesterday
            self.send(symbol, DirectionType.Sell, OffsetType.Open, Bid, 3, OrderType.Limit,止损=最高价,止盈=止盈,移动止损=最高价)   # # OffsetType.Open   OffsetType.Close   OffsetType.CloseToday  OffsetType.CloseYesterday
        # # 平多单
        if Pos["Direction"]==DirectionType.Buy and K[-1]<D[-1] and K[-2] > D[-2]:
            print(symbol) #合约
            print("KDJ策略平多单")
            self.send(symbol, DirectionType.Sell, OffsetType.Close, Bid, Pos['Volume'], OrderType.Limit)         
        # # 平空单        
        if Pos["Direction"]==DirectionType.Sell and K[-1]>D[-1] and K[-2] < D[-2]:
            print(symbol) #合约
            print("KDJ策略平空单")
            self.send(symbol, DirectionType.Buy, OffsetType.Close, Ask, Pos['Volume'], OrderType.Limit)
        if 'kwargs' in Pos.keys():
            # print(Pos["kwargs"])
            if Pos["Direction"]==DirectionType.Buy and LastPrice<Pos["kwargs"]["止损"]:
                print(symbol) #合约
                print("RSI策略止损多单")
                self.send(symbol, DirectionType.Sell, OffsetType.Close, Bid, Pos['Volume'], OrderType.Limit)         
            # # 平空单        
            if Pos["Direction"]==DirectionType.Sell and LastPrice>Pos["kwargs"]["止损"]:
                print(symbol) #合约
                print("RSI策略止损空单")
                self.send(symbol, DirectionType.Buy, OffsetType.Close, Ask, Pos['Volume'], OrderType.Limit)
            # # 多单 修改移动止损价
            if Pos["Direction"]==DirectionType.Buy and (LastPrice - Pos["kwargs"]["移动止损"]) > (Pos["Price"] - Pos["kwargs"]["止损"]):
                self.OrderModify(symbol, LastPrice - (Pos["Price"] - Pos["kwargs"]["止损"]))
                print("空单 修改移动止损价",LastPrice - (Pos["Price"] - Pos["kwargs"]["止损"]))
            # # 空单 修改移动止损价
            if Pos["Direction"]==DirectionType.Sell and (Pos["kwargs"]["移动止损"] - LastPrice) > (Pos["kwargs"]["止损"] - Pos["Price"]):
                self.OrderModify(symbol, LastPrice + (Pos["kwargs"]["止损"] - Pos["Price"]))
                print("空单 修改移动止损价",LastPrice + (Pos["kwargs"]["止损"] - Pos["Price"]))
class RSIStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.symbol_lsit = ["UR301","rb2301","au2212","IF2211","IC2211","i2301","eb2211","MA301"]  #订阅合约
        self.symbol_lsit = ["sc2212"]  #订阅合约
        self.BarType = BarType.Time5  #K线周期
        self.StrategyType = StrategyType.Bar  #策略类型  StrategyType.Renko   StrategyType.Bar   StrategyType.Tick
    def on_tick(self, tick=None):
        print(tick.InstrumentID,tick.LastPrice)  
    def on_bar(self, tick=None, Bar=None):
        symbol = tick.InstrumentID   #合约代码
        Bid = tick.BidPrice1    #买价
        Ask = tick.AskPrice1    #卖价
        LastPrice = tick.LastPrice  #最新价
        #print(symbol) #合约
        #print(tick.LastPrice) #合约tick.UpdateTime
        # print(tick.UpdateTime) #合约tick.UpdateTime
        # print(Bar[0]["symbol"]) #合约
        kline = Bar[0]["data"]    # K 线数据
        if len(kline) <= 35:   # 小于35 条 退出 
            return   
        # K,D,J  = self.KDJ(kline) # 取KDJ指标数组
        # UP,MB,DN  = self.BOLL(kline) # 取BOLL指标数组
        # EMA  = self.EMA(kline,60) # 取EMA指标数组
        RSI  = self.RSI(kline) # 取RSI指标数组
        # MA1  = self.MA(kline,30) # 取MA指标数组Channels
        # MA2  = self.MA(kline,60) # 取MA指标数组Channels
        dif,dea,macd  = self.MACD(kline) # 取MACD指标数组
        close,High,low = self.tick(kline)      # 取收盘价数组 # 获取最新价格（卖价）
        # print(self.Get_Position(symbol))
        Pos = self.GetPosition(symbol)
        # print(Pos)
        # 开多单
        if Pos["Direction"]=="None" and RSI[-1]>50 and RSI[-2] < 50 and dea[-1] > 0:
            print(symbol) #合约
            print("RSI策略开多")
            最低价 = min(low[-10:])
            止盈 = Ask + (Ask-最低价)*3
            # self.send(symbol, DirectionType.Buy, OffsetType.Open, Ask, 3, OrderType.Limit)  # # OrderType.FOK   OrderType.FAK   OrderType.Market
            self.send(symbol, DirectionType.Buy, OffsetType.Open, Ask, 3, OrderType.Limit,止损=最低价,止盈=止盈,移动止损=最低价)  # # OrderType.FOK   OrderType.FAK   OrderType.Market
        # # 开空单
        if Pos["Direction"]=="None" and RSI[-1]<50 and RSI[-2] > 50 and dea[-1] < 0:
            print(symbol) #合约
            print("RSI策略开空")
            最高价 = max(High[-10:])
            止盈 = Bid - (最高价-Bid)*3
            # self.send(symbol, DirectionType.Sell, OffsetType.Open, Bid, 3, OrderType.Limit)   # # OffsetType.Open   OffsetType.Close   OffsetType.CloseToday  OffsetType.CloseYesterday
            self.send(symbol, DirectionType.Sell, OffsetType.Open, Bid, 3, OrderType.Limit,止损=最高价,止盈=止盈,移动止损=最高价)   # # OffsetType.Open   OffsetType.Close   OffsetType.CloseToday  OffsetType.CloseYesterday
        # # 平多单
        if Pos["Direction"]==DirectionType.Buy and RSI[-1]<50 and RSI[-2] > 50:
            print(symbol) #合约
            print("RSI策略平多单")
            self.send(symbol, DirectionType.Sell, OffsetType.Close, Bid, Pos['Volume'], OrderType.Limit)         
        # # 平空单        
        if Pos["Direction"]==DirectionType.Sell and RSI[-1]>50 and RSI[-2] < 50:
            print(symbol) #合约
            print("RSI策略平空单")
            self.send(symbol, DirectionType.Buy, OffsetType.Close, Ask, Pos['Volume'], OrderType.Limit)
        if 'kwargs' in Pos.keys():
            # print(Pos["kwargs"])
            if Pos["Direction"]==DirectionType.Buy and LastPrice<Pos["kwargs"]["止损"]:
                print(symbol) #合约
                print("RSI策略止损多单")
                self.send(symbol, DirectionType.Sell, OffsetType.Close, Bid, Pos['Volume'], OrderType.Limit)         
            # # 平空单        
            if Pos["Direction"]==DirectionType.Sell and LastPrice>Pos["kwargs"]["止损"]:
                print(symbol) #合约
                print("RSI策略止损空单")
                self.send(symbol, DirectionType.Buy, OffsetType.Close, Ask, Pos['Volume'], OrderType.Limit)
            # # 多单 修改移动止损价
            if Pos["Direction"]==DirectionType.Buy and (LastPrice - Pos["kwargs"]["移动止损"]) > (Pos["Price"] - Pos["kwargs"]["止损"]):
                self.OrderModify(symbol, LastPrice - (Pos["Price"] - Pos["kwargs"]["止损"]))
                print("空单 修改移动止损价",LastPrice - (Pos["Price"] - Pos["kwargs"]["止损"]))
            # # 空单 修改移动止损价
            if Pos["Direction"]==DirectionType.Sell and (Pos["kwargs"]["移动止损"] - LastPrice) > (Pos["kwargs"]["止损"] - Pos["Price"]):
                self.OrderModify(symbol, LastPrice + (Pos["kwargs"]["止损"] - Pos["Price"]))
                print("空单 修改移动止损价",LastPrice + (Pos["kwargs"]["止损"] - Pos["Price"]))


Config = {'brokerid':'9999', 'userid':'127922', 'password':'668868', 'appid':'simnow_client_test', 'auth_code':'0000000000000000', 'product_info':'python dll', 'td_address':'tcp://180.168.146.187:10201', 'md_address':'tcp://180.168.146.187:10211'}
# Config = {'brokerid':'9999', 'userid':'127922', 'password':'668868', 'appid':'simnow_client_test', 'auth_code':'0000000000000000', 'product_info':'python dll', 'td_address':'tcp://180.168.146.187:10130', 'md_address':'tcp://180.168.146.187:10131'}

if __name__ == '__main__':
    t = CtpGateway()
    t.add_Strategy(MACDStrategy())
    t.add_Strategy(MAStrategy())
    t.add_Strategy(KDJStrategy())
    t.add_Strategy(RSIStrategy())
    t.add_Config(Config)
    t.Start()
