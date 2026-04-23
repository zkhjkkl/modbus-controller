import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => AppState(),
      child: const MyApp(),
    ),
  );
}

class AppState with ChangeNotifier {
  WebSocketChannel? _channel;
  String _status = '未连接';
  String _serverAddress = '192.168.1.1:8765';
  bool _connected = false;

  WebSocketChannel? get channel => _channel;
  String get status => _status;
  String get serverAddress => _serverAddress;
  bool get connected => _connected;

  AppState() {
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    _serverAddress = prefs.getString('server_address') ?? '192.168.1.1:8765';
    notifyListeners();
  }

  Future<void> saveSettings(String address) async {
    _serverAddress = address;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('server_address', address);
    notifyListeners();
  }

  Future<void> connect() async {
    if (_connected) {
      return;
    }

    _status = '连接中...';
    _connected = false;
    notifyListeners();

    try {
      print('尝试连接: ws://$_serverAddress');
      final uri = Uri.parse('ws://$_serverAddress');

      // 使用 Completer 实现连接超时
      final completer = Completer<WebSocketChannel>();
      Timer? timeoutTimer;

      // 设置5秒超时
      timeoutTimer = Timer(const Duration(seconds: 5), () {
        if (!completer.isCompleted) {
          completer.completeError(TimeoutException('连接超时，请检查服务器地址和网络'));
        }
      });

      // 异步建立连接
      WebSocketChannel.connect(uri).then((channel) {
        if (!completer.isCompleted) {
          timeoutTimer?.cancel();
          completer.complete(channel);
        }
      }).catchError((error) {
        if (!completer.isCompleted) {
          timeoutTimer?.cancel();
          completer.completeError(error);
        }
      });

      // 等待连接完成（带超时）
      _channel = await completer.future;
      print('WebSocket连接建立成功');

      // 监听消息
      _channel!.stream.listen(
        (message) {
          print('收到消息: $message');
          _handleMessage(message);
        },
        onError: (error) {
          print('连接错误: $error');
          _status = '连接错误: ${error.toString()}';
          _connected = false;
          notifyListeners();
        },
        onDone: () {
          print('连接断开');
          _status = '连接已断开';
          _connected = false;
          notifyListeners();
        },
      );

      _connected = true;
      _status = '已连接';
      notifyListeners();

      // 发送测试消息确认连接
      await Future.delayed(const Duration(milliseconds: 500));
      sendCommand('ping');

    } on TimeoutException catch (e) {
      print('连接超时: $e');
      _status = '连接超时，请检查：\n1. PC端网关是否运行\n2. IP地址是否正确\n3. 防火墙是否允许端口8765';
      _connected = false;
      notifyListeners();
    } on SocketException catch (e) {
      print('网络错误: $e');
      _status = '网络错误: ${e.message}\n请确保设备在同一网络';
      _connected = false;
      notifyListeners();
    } catch (e) {
      print('连接异常: $e');
      _status = '连接失败: $e';
      _connected = false;
      notifyListeners();
    }
  }

  void disconnect() {
    _channel?.sink.close();
    _channel = null;
    _connected = false;
    _status = '已断开';
    notifyListeners();
  }

  void sendCommand(String command, {int? register, int? value, String? type}) {
    if (!_connected || _channel == null) {
      _status = '未连接，无法发送命令';
      notifyListeners();
      return;
    }

    final message = {
      'command': command,
      if (register != null) 'register': register,
      if (value != null) 'value': value,
      if (type != null) 'type': type,
    };

    try {
      _channel!.sink.add(message.toString().replaceAll("'", '"'));
      _status = '命令已发送: $command';
      notifyListeners();
    } catch (e) {
      _status = '发送失败: $e';
      notifyListeners();
    }
  }

  void _handleMessage(String message) {
    // 处理服务器响应
    print('收到消息: $message');
    // 可以解析JSON并更新状态
  }
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Modbus无线控制器',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Modbus无线控制器'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SettingsPage()),
              );
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // 状态显示
          Consumer<AppState>(
            builder: (context, state, child) {
              return Container(
                padding: const EdgeInsets.all(16),
                color: state.connected ? Colors.green[100] : Colors.red[100],
                child: Row(
                  children: [
                    Icon(
                      state.connected ? Icons.check_circle : Icons.error,
                      color: state.connected ? Colors.green : Colors.red,
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        state.status,
                        style: TextStyle(
                          color: state.connected ? Colors.green : Colors.red,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              );
            },
          ),

          // 控制按钮区域
          Expanded(
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // 启动按钮
                  SizedBox(
                    width: 200,
                    height: 200,
                    child: Consumer<AppState>(
                      builder: (context, state, child) {
                        return ElevatedButton(
                          onPressed: state.connected
                              ? () {
                                  state.sendCommand('start');
                                }
                              : null,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                            shape: const CircleBorder(),
                            padding: const EdgeInsets.all(20),
                          ),
                          child: const Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.play_arrow, size: 60, color: Colors.white),
                              SizedBox(height: 10),
                              Text(
                                '启动',
                                style: TextStyle(
                                  fontSize: 24,
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
                  ),

                  const SizedBox(height: 40),

                  // 停止按钮
                  SizedBox(
                    width: 200,
                    height: 200,
                    child: Consumer<AppState>(
                      builder: (context, state, child) {
                        return ElevatedButton(
                          onPressed: state.connected
                              ? () {
                                  state.sendCommand('stop');
                                }
                              : null,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.red,
                            shape: const CircleBorder(),
                            padding: const EdgeInsets.all(20),
                          ),
                          child: const Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.stop, size: 60, color: Colors.white),
                              SizedBox(height: 10),
                              Text(
                                '停止',
                                style: TextStyle(
                                  fontSize: 24,
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          ),

          // 连接控制
          Padding(
            padding: const EdgeInsets.all(16),
            child: Consumer<AppState>(
              builder: (context, state, child) {
                return Row(
                  children: [
                    Expanded(
                      child: ElevatedButton(
                        onPressed: state.connected ? null : () => state.connect(),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                        ),
                        child: const Text(
                          '连接',
                          style: TextStyle(fontSize: 18),
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: ElevatedButton(
                        onPressed: state.connected ? () => state.disconnect() : null,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.red,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                        ),
                        child: const Text(
                          '断开',
                          style: TextStyle(fontSize: 18),
                        ),
                      ),
                    ),
                  ],
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  final TextEditingController _addressController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadCurrentSettings();
  }

  Future<void> _loadCurrentSettings() async {
    final state = Provider.of<AppState>(context, listen: false);
    _addressController.text = state.serverAddress;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('设置'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '服务器地址',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _addressController,
              decoration: const InputDecoration(
                hintText: '例如: 192.168.1.1:8765',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.computer),
              ),
            ),
            const SizedBox(height: 20),
            const Text(
              '说明:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 5),
            const Text('请输入PC端网关的IP地址和端口号，格式为 IP:端口'),
            const SizedBox(height: 30),
            Center(
              child: ElevatedButton(
                onPressed: () {
                  final state = Provider.of<AppState>(context, listen: false);
                  state.saveSettings(_addressController.text);
                  Navigator.pop(context);
                },
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16),
                ),
                child: const Text('保存设置'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}