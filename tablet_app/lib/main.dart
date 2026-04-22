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

    try {
      final uri = Uri.parse('ws://$_serverAddress');
      _channel = WebSocketChannel.connect(uri);

      _channel!.stream.listen(
        (message) {
          _handleMessage(message);
        },
        onError: (error) {
          _status = '连接错误: $error';
          _connected = false;
          notifyListeners();
        },
        onDone: () {
          _status = '连接已断开';
          _connected = false;
          notifyListeners();
        },
      );

      _status = '连接中...';
      _connected = true;
      notifyListeners();

      // 等待连接建立
      await Future.delayed(const Duration(seconds: 2));
      _status = '已连接';
      notifyListeners();

    } catch (e) {
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