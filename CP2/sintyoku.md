2-5

Next 2-6


## 2章
pythonでサーバ/クライアント通信を行う  
->socketライブラリが重要


##<u> TCP client </u>##

target_host(文字列):  
①www.google.comのようなドメイン形式  
②192.168.0.1のようなIPv4アドレスの文字列

target_port(整数):  
port番号

ソケットを作成
socket.socket(family,type,protocol)

family ->AF_INET(def),AF_INET6,AF_UNIX  
type   ->SOCK_STREAM(def),SOCK_DGRAM etc  
protocol ->省略,0  


IF_INET ->IPv4に対応
SOCK_STREAM:TCP  
サーバへ接続
socket.connect(address)
address=(host,port)
アドレスで示されるソケットに接続


ソケットにデータ送信  
client.send(string,flag)

ソケットは接続済みデないといけない  

client.recv(bufsize)  
データを受信し、文字列で返す  
受信最大バイト数はbufsizeで指定(2の累乗の4096がよく使用される)  



##<u> UDP client </u>##

client.sendto(string,address)  

ソケットにデータを送信  
ソケットに接続済みでないといけない  

client.recvfrom(bufsize)  

データを受信して、タプルとして返す  
string :受信データの文字列  
addres:送信元アドレス  



##<u> TCP Server</u>##

threading  

.bind(ip,port)  

サーバソケット  

server.listen(int)  

接続要求を(int)個まで待たせる  


handler_client関数  

サーバ側(自分)に受信したデータを表示  
クライアント側(相手)にパケットの返送(今回は"ACK")  

socket.accept()  
接続を受ける  
  
アドレスはbind済み&listen状態であることが必要

戻り値:conn,addr
connは新しいソケットオブジェクト
addr　ソケットにbindしているあaddress


threading.Thread(group,target,name,args(),)

start():スレッドの起動
