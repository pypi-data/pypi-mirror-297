import websocket
import threading
import time
import json
import logging
from dataclasses import dataclass
from typing import Callable, Any
from typing import Optional

def str_to_bool(s):
    """
    文字列をブール値に変換する

    Args:
        s (str): "true" または "false"（大文字小文字は無視）

    Returns:
        bool: 変換されたブール値"true"ならTrue、"false"ならFalse
    """
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        raise ValueError(f"Cannot covert {s} to a boolean.")  # 有効な文字列でない場合はエラー

class UninitializedClientError(Exception):
    """WebSocketClientが初期化されていないことを示すカスタム例外"""
    pass


class _WebSocketClient:
    def __init__(self):
        self.lock = threading.Lock()
        self.connected = False
        self.response_event = threading.Event()  # イベントオブジェクトを追加
        self.callbacks = {}  # コールバック関数を保持

    def connect(self, host:str, port:int):
        self.host = host
        self.port = port
        self.url = "ws://%s:%d/ws" %(host, port)
        logging.debug("connecting '%s'" % (self.url))
        self.connected = False
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.run_forever()

    def disconnect(self):
        self.connected = False
        self.host = None
        self.port = None
        self.close()

    def setCallback(self, eventName, callbackFunc):
            # イベント名に対応するコールバックリストがまだ存在しない場合は、新しいリストを作成する
            if eventName not in self.callbacks:
                self.callbacks[eventName] = []
            
            # 指定されたイベント名のリストにコールバック関数を追加する
            self.callbacks[eventName].append(callbackFunc)

    def on_message(self, ws, message):
        logging.debug("on_message '%s'" % message)
        try:
            jsonMessage = json.loads(message)
            type = jsonMessage['type']
            data = jsonMessage['data']
            if(type == 'result'):
                self.result = data
            elif(type == 'error'):
                self.error = data
            elif(type == 'logged'):
                self.connected = True
                self.result = data
            elif(type == 'attach'):
                self.result = data
            elif(type == 'event'):
                jsonEvent = json.loads(data)
                eventName = jsonEvent['name']
                logging.debug("on event %s '%s'" %(eventName, jsonEvent['data']))
                # 指定されたイベント名に対応するすべてのコールバック関数を実行する
                if eventName in self.callbacks:
                    for callback in self.callbacks[eventName]:
                        # 新しいスレッドでコールバック関数を実行
                        callback_thread = threading.Thread(target=callback, args=(jsonEvent['data'],))
                        callback_thread.start()
                        # callback(jsonEvent['data'])
                        return
                if(jsonEvent['data']):    
                    self.result = jsonEvent['data']
                    self.response_event.set()  # イベントをセットして、メッセージの受信を通知
                return
            else:
                self.result = data
            self.response_event.set()  # イベントをセットして、メッセージの受信を通知
        except json.JSONDecodeError:
            logging.error("JSONDecodeError '%s'" % message)    

    def on_error(self, ws, error):
        logging.debug("on_error '%s'" % error)

    def on_close(self, ws, close_status_code, close_msg):
        logging.debug("### closed ###")
        self.connected = False

    def on_open(self, ws):
        logging.debug("Opened connection")
        self.connected = True

    def run_forever(self):
        self.thread.start()

    def wait_for_connection(self):
        while not self.connected:
            time.sleep(0.1)  # Wait for connection to be established

    def send(self, message):
        logging.debug("send sending'%s'" % message)
        self.wait_for_connection()
        with self.lock:
            self.result = None
            self.response_event.clear()  # イベントをクリアして新しいレスポンスの準備をする
            self.ws.send(message)
            self.response_event.wait()  # サーバーからのレスポンスを待つ
        return self.result  # 最後に受信したメッセージを返す

    def close(self):
        self.ws.close()
        self.thread.join()

    def waitFor(self, entity: str, name: str, args=None):
        data = {"entity": entity, "name": name}
        if args is not None:
            data['args'] = args            
        message = {
            "type": "hook",
            "data": data
        }
        self.send(json.dumps(message))

    def sendCall(self, entity: str, name: str, args=None):
        data = {"entity": entity, "name": name}
        if args is not None:
            data['args'] = args            
        message = {
            "type": "call",
            "data": data
        }
        self.send(json.dumps(message))

class Coordinates:
    """
    座標の基準を表すデータクラス
    """
    world = ""
    relative = "~"
    local = "^"

class Side:
    """
    ブロックの配置方向を表すデータクラス
    """
    right = "Right"
    left = "Left"
    front = "Front"
    back = "Back"
    top = "Top"
    bottom = "Bottom"

@dataclass(frozen=True)
class Location:
    """
    座標を表すデータクラス

    Attributes:
        x (str): X座標
        y (str): Y座標
        z (str): Z座標
        world (str): ワールド名
    """
    x: int
    y: int
    z: int
    world: str = "world"

@dataclass(frozen=True)
class InteractEvent:
    """
    クリックイベントを表すデータクラス

    Attributes:
        action (str): アクションの名前
        player (str): クリックしたプレイヤー名
        player_uuid (str): クリックしたプレイヤーの一意の識別子（UUID）
        event (str): アイテムに設定されている名前
        name (str): ブロックあるいはエンティティーの名前
        type (str): ブロックあるいはエンティティーの種類
        data (int): ブロックのデータ値
        world (str): ブロックあるいはエンティティーのいたワールド名
        x (int): クリックした場所のワールドにおけるX座標
        y (int): クリックした場所のワールドにおけるY座標
        z (int): クリックした場所のワールドにおけるZ座標
    """
    action: str
    player: str
    player_uuid: str
    event: str
    name: str
    type: str
    data: int = 0
    world: str = "world"
    x: int = 0 
    y: int = 0 
    z: int = 0

@dataclass(frozen=True)
class EventMessage:
    """
    イベントメッセージを表すデータクラス

    Attributes:
        sender (str): 送信者の名前
        uuid (str): 送信者の一意の識別子（UUID）
        message (str): イベントメッセージ
    """
    entityUuid: str
    sender: str
    uuid: str
    message: str


@dataclass(frozen=True)
class ChatMessage:
    """
    チャットメッセージを表すデータクラス

    Attributes:
        player (str): プレイヤー名
        uuid (str): プレイヤーの一意の識別子（UUID）
        message (str): プレイヤーがチャットで送信したメッセージの内容
    """
    player: str
    uuid: str
    entityUuid: str
    message: str

@dataclass(frozen=True)
class RedstonePower:
    """
    レッドストーン信号を表すデータクラス

    Attributes:
        oldCurrent (int): 前のレッドストーン信号の強さ
        newCurrent (int): 最新のレッドストーン信号の強さ
    """
    entityUuid: str
    oldCurrent: int
    newCurrent: int

@dataclass(frozen=True)
class Block:
    """
    ブロックを表すデータクラス

    Attributes:
        name (str): ブロックの種類
        data (int): ブロックのデータ値
        isLiquid (bool): 液体ブロックかどうか
        isAir (bool): 空気ブロックかどうか
        isBurnable (bool): 燃えるブロックかどうか
        isFuel (bool): 燃料ブロックかどうか
        isOccluding (bool): 透過しないブロックかどうか
        isSolid (bool): 壁のあるブロックかどうか
        isPassable (bool): 通過可能なブロックかどうか
        world (str): ブロックが存在するワールドの名前（デフォルトは"world"）
        x (int): ブロックのX座標
        y (int): ブロックのY座標
        z (int): ブロックのZ座標
    """
    name: str
    type: str = "block"
    data: int = 0
    isLiquid: bool = False
    isAir: bool = False
    isBurnable: bool = False
    isFuel: bool = False
    isOccluding: bool = False
    isSolid: bool = False
    isPassable: bool = False
    x: int = 0
    y: int = 0
    z: int = 0
    world: str = "world"

@dataclass(frozen=True)
class ItemStack:
    slot: int = 0
    name: str = "air"
    amount: int = 0

class Player:
    def __init__(self, player: str):
        self.name = player

    def login(self, host:str, port:int) -> 'Player':
        self.client = _WebSocketClient()
        self.client.connect(host, port)
        self.client.send(json.dumps({
            "type": "login",
            "data": {
                "player": self.name,
            }
        }))
        logging.debug("login '%s'" % self.client.result)
        # ret = json.loads(self.client.result)
        self.uuid = self.client.result['playerUUID']
        self.world = self.client.result['world']
        return self

    def logout(self):
        self.client.disconnect()    


    def getEntity(self, name: str) -> 'Entity': 
        """
        指定された名前のエンティティを取得する

        Args:
            name (str): エンティティの名前

        Returns:
            Entity: 取得したエンティティ

        Raises:
            UninitializedClientError: クライアントが初期化されていない場合        
        """
        if self.client is None or not self.client.connected:  # 接続状態をチェック
            raise UninitializedClientError("Client is not initialized")

        message = {
            "type": "attach",
            "data": {"entity": name}
        }
        self.client.send(json.dumps(message))
        result = self.client.result
        if(result is None):
            raise ValueError("Entity '%s' not found" % name)
        

        entity =  Entity(self.client, self.world, result)
        #ロールバックできるように設定
        self.client.send(json.dumps({
            "type": "start",
            "data": {"entity": entity.uuid}
        }))
        return entity

class Inventory:
    """
    インベントリを表すクラス
    """
    def __init__(self, client: _WebSocketClient, entityUUID: str, world: str, x: int, y: int, z:int, size:int, items: list):
        self.client = client
        self.entityUUID = entityUUID
        self.location = Location(x, y, z, world)
        self.size = size
        self.items = items

    def getItem(self, slot: int) -> ItemStack :
        """
        指定されたスロットのアイテムを取得する

        Args:
            slot (int): 取得するアイテムのスロット番号
        """
        self.client.sendCall(self.entityUUID, "getInventoryItem", [self.location.x, self.location.y, self.location.z, slot])
        itemStack = ItemStack(** json.loads(self.client.result))
        return itemStack

    def swapItem(self, slot1: int, slot2: int) :
        """
        インベントリの内容を置き換える

        Args:
            slot1 (int): 置き換え元のアイテムのスロット番号
            slot2 (int): 置き換え先のアイテムのスロット番号
        """
        self.client.sendCall(self.entityUUID, "swapInventoryItem", [self.location.x, self.location.y, self.location.z, slot1, slot2])

    def moveItem(self, slot1: int, slot2: int) :
        """
        インベントリの内容を移動させる

        Args:
            slot1 (int): 移動元のアイテムのスロット番号
            slot2 (int): 移動先のアイテムのスロット番号        
        """
        self.client.sendCall(self.entityUUID, "moveInventoryItem", [self.location.x, self.location.y, self.location.z, slot1, slot2])

    def storeItem(self, item: ItemStack, slot: int):
        """
        チェストを開いたエンティティーのインベントリからこのインベントリにアイテムを入れる

        Args:
            item (ItemStack): 引き出し元になるペットのアイテム
            slot (int): 格納先になるチェストのアイテムスロット番号        
        """
        self.client.sendCall(self.entityUUID, "storeInventoryItem", [self.location.x, self.location.y, self.location.z, item.slot, slot])

    def retrieveItem(self, slot: int, item: ItemStack):
        """
        チェストを開いたエンティティーのインベントリからこのインベントリからアイテムを取り出す

        Args:
            slot (int): 格納先になるペットのアイテムスロット番号
            item (ItemStack): 引き出し元になるチェストのアイテム        
        """
        self.client.sendCall(self.entityUUID, "retrieveInventoryItem", [self.location.x, self.location.y, self.location.z, slot, item.slot])


class Entity:
    """
    エンティティを表すクラス
    """
    def __init__(self, client: _WebSocketClient, world: str, uuid: str):
        self.client = client
        self.world = world
        self.uuid = uuid
        self.positions = []

    def reset(self):
        self.client.sendCall(self.uuid, "restoreArea")

    def waitForPlayerChat(self):
        """
        チャットを受信するまでまつ
        """
        self.client.waitFor(self.uuid, 'onPlayerChat')
        print('result = ', self.client.result)
        return ChatMessage(** self.client.result)

    def waitForRedstoneChange(self):
        """
        レッドストーン信号が変わるまでまつ
        """
        self.client.waitFor(self.uuid, 'onEntityRedstone')
        return RedstonePower(** self.client.result)

    def setOnMessage(self, callbackFunc: Callable[['Entity', str], Any]):
        """
        カスタムイベントメッセージを受信したときに呼び出されるコールバック関数を設定する
        """
        def callbackWrapper(data):
            logging.debug("setOnMessage callbackWrapper '%s'" % data)
            if(data['entityUuid'] == self.uuid):
                logging.debug("callbackWrapper '%s'" % data)
                event = EventMessage(**data)
                callbackFunc(self, event)
        self.client.setCallback('onCustomEvent', callbackWrapper)

    def sendMessage(self, target: str, message: str):
        """
        カスタムイベントメッセージを送信する

        Args:
            target (str): 送信先のEntityの名前
            message (str): 送信するメッセージの内容
        """
        self.client.sendCall(self.uuid, "sendEvent", [target, message])

    def executeCommand(self, command: str):
        """
        コマンドを実行する

        Args:
            command (str): 実行するコマンドの内容
        """
        self.client.sendCall(self.uuid, "executeCommand", [command])
    
    def openInventory(self, x, y, z) -> Inventory :
        self.client.sendCall(self.uuid, "openInventory", [x, y, z])
        inventory = Inventory(self.client, self.uuid, ** json.loads(self.client.result))
        return inventory

    def push(self) -> bool :
        """
        自分の位置を保存する
        """
        pos = self.getLocation()
        self.positions.append(pos)
        return True
    
    def pop(self) -> bool :
        """
        自分の位置を保存した位置に戻す
        """
        if(len(self.positions) > 0):
            pos = self.positions.pop()
            self.teleport(pos)
            return True
        else:
            return False

    def forward(self) -> bool :
        """
        自分を前方に移動させる
        """
        self.client.sendCall(self.uuid, "forward")
        return str_to_bool(self.client.result)

    def back(self) -> bool :
        """
        自分を後方に移動させる
        """
        self.client.sendCall(self.uuid, "back")
        return str_to_bool(self.client.result)

    def up(self) -> bool :
        """
        自分を上方に移動させる
        """
        self.client.sendCall(self.uuid, "up")
        return str_to_bool(self.client.result)

    def down(self) -> bool :
        """
        自分を下方に移動させる
        """
        self.client.sendCall(self.uuid, "down")
        return str_to_bool(self.client.result)

    def stepLeft(self) -> bool :
        """
        自分を左に移動させる
        """
        self.client.sendCall(self.uuid, "stepLeft")
        return str_to_bool(self.client.result)

    def stepRight(self) -> bool :
        """
        自分を右に移動させる
        """
        self.client.sendCall(self.uuid, "stepRight")
        return str_to_bool(self.client.result)

    def turnLeft(self) :
        """
        自分を左に回転させるaw
        """
        self.client.sendCall(self.uuid, "turnLeft")

    def turnRight(self) :
        """
        自分を右に回転させる
        """
        self.client.sendCall(self.uuid, "turnRight")

    def makeSound(self) -> bool :
        """
        自分を鳴かせる
        """
        self.client.sendCall(self.uuid, "sound")
        return str_to_bool(self.client.result)

    def addForce(self, x: float, y: float, z: float) -> bool :
        """
        前方へ移動する

        Args:
            x (float): x軸方向の加速
            y (float): y軸方向の加速
            z (float): z軸方向の加速
        """
        self.client.sendCall(self.uuid, "addForce", [x, y, z])
        return str_to_bool(self.client.result)

    def jump(self):
        """
        ジャンプさせる
        """
        self.client.sendCall(self.uuid, "jump")  

    def turn(self, degrees: int):
        """
        自分を回転させる

        Args:
            degrees (int): 回転する速度
        """
        self.client.sendCall(self.uuid, "turn", [degrees])  

    def placeX(self, x: int, y: int, z: int, cord: Coordinates=Coordinates.local, side=None,) -> bool :
        """
        指定した座標にブロックを設置する

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            cord (Coordinates): 座標の種類（'', '^', '~'）
            side (str): 設置する面
        """
        self.client.sendCall(self.uuid, "placeX", [x, y, z, cord, side])
        return str_to_bool(self.client.result)

    def placeHere(self, x: int, y: int, z: int, side=None) -> bool :
        """
        自分を中心に指定した座標にブロックを設置する

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            side (str): 設置する面
        """
        self.client.sendCall(self.uuid, "placeX", [x, y, z, "^", side])
        return str_to_bool(self.client.result)

    def place(self, side=None) -> bool :
        """
        自分の前方にブロックを設置する
        """
        self.client.sendCall(self.uuid, "placeFront", [side])
        return str_to_bool(self.client.result)

    def placeUp(self, side=None) -> bool :
        """
        自分の真上にブロックを設置する
        """
        self.client.sendCall(self.uuid, "placeUp", [side])
        return str_to_bool(self.client.result)

    def placeDown(self, side=None) -> bool :
        """
        自分の真下にブロックを設置する
        """
        self.client.sendCall(self.uuid, "placeDown", [side])
        return str_to_bool(self.client.result)

    def useItemX(self, x: int, y: int, z: int, cord: Coordinates = Coordinates.local) -> bool :
        """
        指定した座標にアイテムを使う

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            cord (Coordinates): 座標の種類（'', '^', '~'）        
        """
        self.client.sendCall(self.uuid, "useItemX", [x, y, z, cord])
        return str_to_bool(self.client.result)

    def useItemHere(self, x: int, y: int, z: int) -> bool :
        """
        自分を中心に指定した座標にアイテムを使う

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
        """
        self.client.sendCall(self.uuid, "useItemX", [x, y, z, "^"])
        return str_to_bool(self.client.result)

    def useItem(self) -> bool :
        """
        自分の前方にアイテムを使う
        """
        self.client.sendCall(self.uuid, "useItemFront")
        return str_to_bool(self.client.result)

    def useItemUp(self) -> bool :
        """
        自分の真上にアイテムを使う
        """
        self.client.sendCall(self.uuid, "useItemUp")
        return str_to_bool(self.client.result)

    def useItemDown(self) -> bool :
        """
        自分の真下にアイテムを使う
        """
        self.client.sendCall(self.uuid, "useItemDown")
        return str_to_bool(self.client.result)

    def harvest(self) -> bool :
        """
        自分の位置のブロックを収穫する
        """
        self.client.sendCall(self.uuid, "digX", [0, 0, 0])
        return str_to_bool(self.client.result)

    def attack(self) -> bool :
        """
        自分の前方を攻撃する
        """
        self.client.sendCall(self.uuid, "attack")
        return str_to_bool(self.client.result)

    def plant(self) -> bool :
        """
        自分の足元に植物を植える
        """
        self.client.sendCall(self.uuid, "plantX", [0, -1, 0, "^"])
        return str_to_bool(self.client.result)
    
    def plantX(self, x : int, y: int, z: int, cord: Coordinates = Coordinates.local) -> bool :
        """
        指定した座標のブロックに植物を植える

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            cord (Coordinates): 座標の種類（'', '^', '~'）        
        """
        self.client.sendCall(self.uuid, "plantX", [x, y, z, cord])
        return str_to_bool(self.client.result)

    def till(self) -> bool :
        """
        自分の足元のブロックを耕す
        """
        self.client.sendCall(self.uuid, "tillX", [0, -1, 0, "^"])
        return str_to_bool(self.client.result)
    
    def tillX(self, x : int, y: int, z: int, cord: Coordinates = Coordinates.local) -> bool :
        """
        指定した座標のブロックを耕す

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            cord (Coordinates): 座標の種類（'', '^', '~'）        
        """
        self.client.sendCall(self.uuid, "tillX", [x, y, z, cord])
        return str_to_bool(self.client.result)

    def flatten(self) -> bool :
        """
        自分の足元のブロックに平らにする
        """
        self.client.sendCall(self.uuid, "flattenX", [0, -1, 0, "^"])
        return str_to_bool(self.client.result)
    
    def flattenX(self, x : int, y: int, z: int, cord: Coordinates = Coordinates.local) -> bool :
        """
        指定した座標のブロックを平らにする

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            cord (Coordinates): 座標の種類（'', '^', '~'）        
        """
        self.client.sendCall(self.uuid, "flattenX", [x, y, z, cord])
        return str_to_bool(self.client.result)

    def dig(self) -> bool :
        """
        自分の前方のブロックを壊す
        """
        self.client.sendCall(self.uuid, "digFront")
        return str_to_bool(self.client.result)

    def digUp(self) -> bool :
        """
        自分の真上のブロックを壊す
        """
        self.client.sendCall(self.uuid, "digUp")
        return str_to_bool(self.client.result)

    def digDown(self) -> bool :
        """
        自分の真下のブロックを壊す
        """
        self.client.sendCall(self.uuid, "digDown")
        return str_to_bool(self.client.result)

    def digX(self, x : int, y: int, z: int, cord: Coordinates = Coordinates.local) -> bool :
        """
        指定した座標のブロックを壊す

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            cord (Coordinates): 座標の種類（'', '^', '~'）        
        """
        self.client.sendCall(self.uuid, "digX", [x, y, z, cord])
        return str_to_bool(self.client.result)

    def pickupItemsX(self, x : int, y: int, z: int, cord: Coordinates = Coordinates.local) -> int :
        """
        指定した座標の周辺のアイテムを拾う

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            cord (Coordinates): 座標の種類（'', '^', '~'）        
        """
        self.client.sendCall(self.uuid, "pickupItemsX", [x, y, z, cord])
        return int(self.client.result)

    def pickupItems(self) -> int :
        """
        自分の周辺のアイテムを拾う

        """
        self.client.sendCall(self.uuid, "pickupItemsX", [0, 0, 0, "^"])
        return int(self.client.result)

    def action(self) -> bool :
        """
        自分の前方の装置を使う
        """
        self.client.sendCall(self.uuid, "actionFront")
        return str_to_bool(self.client.result)

    def actionUp(self) -> bool :
        """
        自分の真上の装置を使う
        """
        self.client.sendCall(self.uuid, "actionUp")
        return str_to_bool(self.client.result)

    def actionDown(self) -> bool :
        """
        自分の真下の装置を使う
        """
        self.client.sendCall(self.uuid, "actionDown")
        return str_to_bool(self.client.result)

    def setItem(self, slot: int, block: str) -> bool :
        """
        自分のインベントリにアイテムを設定する

        Args:
            slot (int): 設定するアイテムのスロット番号
            block (str): 設定するブロックの種類
        """
        self.client.sendCall(self.uuid, "setItem", [slot, block])
        return str_to_bool(self.client.result)

    def getItem(self, slot: int) -> ItemStack :
        """
        自分のインベントリからアイテムを取得する

        Args:
            slot (int): 取得するアイテムのスロット番号
        """
        self.client.sendCall(self.uuid, "getItem", [slot])
        itemStack = ItemStack(** json.loads(self.client.result))
        return itemStack

    def swapItem(self, slot1: int, slot2: int) -> bool :
        """
       自分のインベントリのアイテムを置き換える
        """
        self.client.sendCall(self.uuid, "swapItem", [slot1, slot2])
        return str_to_bool(self.client.result)

    def moveItem(self, slot1: int, slot2: int) -> bool :
        """
        自分のインベントリのアイテムを移動させる
        """
        self.client.sendCall(self.uuid, "moveItem", [slot1, slot2])
        return str_to_bool(self.client.result)

    def dropItem(self, slot1: int) -> bool :
        """
        自分のインベントリのアイテムを落とす
        """
        self.client.sendCall(self.uuid, "dropItem", [slot1])
        return str_to_bool(self.client.result)

    def selectItem(self, slot: int) -> bool :
        """
        自分のインベントリのアイテムを手に持たせる

        Args:
            slot (int): アイテムを持たせたいスロットの番号
        """
        self.client.sendCall(self.uuid, "grabItem", [slot])
        return str_to_bool(self.client.result)

    def say(self, message: str):
        """
        メッセージをチャットに送る

        Args:
            message (str): エンティティがチャットで送信するメッセージの内容
        """
        self.client.sendCall(self.uuid, "sendChat", [message])

    def findNearbyBlockX(self, x: int, y: int, z: int, cord: Coordinates, block: str, maxDepth: int) -> Optional[Block]:
        """
        指定された座標を中心に近くのブロックを取得する

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            cord (Coordinates): 座標の種類（'', '^', '~'）
            block (str): ブロックの名前( "water:0" など)
            maxDepth (int): 探索する最大の深さ
        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.sendCall(self.uuid, "findNearbyBlockX", [x, y, z, cord, block, maxDepth])
    
        print('result = ', self.client.result)
        # resultがNoneまたは空のケースに対応
        if not self.client.result:
            return None
        
        try:
            result = json.loads(self.client.result)
            if not result:
                return None
        except json.JSONDecodeError:
            # 例外が発生した場合、無効なJSONとして処理し、Noneを返す
            return None

        block = Block(**result)
        return block

    def inspectX(self, x: int, y: int, z: int, cord: Coordinates = Coordinates.local) -> Block :
        """
        指定された座標のブロックを調べる

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            cord (Coordinates): 座標の種類（'', '^', '~'）
        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.sendCall(self.uuid, "inspect", [x, y, z, cord])
        block = Block(** json.loads(self.client.result))
        return block

    def inspectHere(self, x: int, y: int, z: int) -> Block :
        """
        自分を中心に指定された座標のブロックを調べる

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.sendCall(self.uuid, "inspect", [x, y, z, "^"])
        block = Block(** json.loads(self.client.result))
        return block

    def inspect(self) -> Block :
        """
        自分の前方のブロックを調べる

        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.sendCall(self.uuid, "inspect", [0, 0, 1])
        block = Block(** json.loads(self.client.result))
        return block

    def inspectUp(self) -> Block :
        """
        自分を真上のブロックを調べる

        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.sendCall(self.uuid, "inspect", [0, 1, 0])
        block = Block(** json.loads(self.client.result))
        return block

    def inspectDown(self) -> Block :
        """
        自分の足元のブロックを調べる

        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.sendCall(self.uuid, "inspect", [0, -1, 0])
        block = Block(** json.loads(self.client.result))
        return block

    def getLocation(self) -> Location :
        """
        自分の現在位置を調べる
        Returns:
            Location: 調べた位置情報    
        """
        self.client.sendCall(self.uuid, "getPosition")
        location = Location(** json.loads(self.client.result))
        return location
    
    def teleport(self, location: Location) :
        """
        自分を指定されたワールド座標に移動する
        Args:
            location (Location): 座標
        """
        self.client.sendCall(self.uuid, "teleport", [location.x, location.y, location.z, Coordinates.world])

    def isBlocked(self) -> bool :
        """
        自分の前方にブロックがあるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.sendCall(self.uuid, "isBlockedFront")
        return str_to_bool(self.client.result)

    def isBlockedUp(self) -> bool :
        """
        自分の真上にブロックがあるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.sendCall(self.uuid, "isBlockedUp")
        return str_to_bool(self.client.result)

    def isBlockedDown(self) -> bool :
        """
        自分の真下にブロックがあるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.sendCall(self.uuid, "isBlockedDown")
        return str_to_bool(self.client.result)


    def canDig(self) -> bool :
        """
        自分の前方のブロックが壊せるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.sendCall(self.uuid, "isCanDigFront")
        return str_to_bool(self.client.result)

    def canDigUp(self) -> bool :
        """
        自分の上のブロックが壊せるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.sendCall(self.uuid, "isCanDigUp")
        return str_to_bool(self.client.result)

    def canDigDown(self) -> bool :
        """
        自分の下のブロックが壊せるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.sendCall(self.uuid, "isCanDigDown")
        return str_to_bool(self.client.result)

    def getDistance(self) -> float :
        """
        自分と前方のなにかとの距離を調べる
        """
        self.client.sendCall(self.uuid, "getTargetDistanceFront")
        return self.client.result

    def getDistanceUp(self) -> float :
        """
        自分と真上のなにかとの距離を調べる
        """
        self.client.sendCall(self.uuid, "getTargetDistanceUp")
        return float(self.client.result)

    def getDistanceDown(self) -> float :
        """
        自分と真下のなにかとの距離を調べる
        """
        self.client.sendCall(self.uuid, "getTargetDistanceDown")
        return self.client.result

    def getDistanceTarget(self, uuid) -> float :
        """
        自分とターゲットとの距離を調べる
        """
        self.client.sendCall(self.uuid, "getTargetDistance", [uuid])
        return self.client.result

    def getBlockByColor(self, color: str) -> Block :
        """
        指定された色に近いブロックを取得する

        Args:
            color (str): ブロックの色(HexRGB形式)
        """
        self.client.sendCall(self.uuid, "blockColor", [color])
        block = Block(** json.loads(self.client.result))
        return block
