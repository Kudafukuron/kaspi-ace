import 'package:flutter/material.dart';
import '../api/api_service.dart';

class ChatScreen extends StatefulWidget {
  final ApiService api;
  final int salesmanId;

  const ChatScreen({
    super.key,
    required this.api,
    required this.salesmanId,
  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  List messages = [];
  final controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    loadHistory();
  }

  Future<void> loadHistory() async {
    final data = await widget.api.getChatHistory(widget.salesmanId);
    setState(() => messages = data);
  }

  Future<void> send() async {
    final text = controller.text.trim();
    if (text.isEmpty) return;

    await widget.api.sendMessage(widget.salesmanId, text);
    controller.clear();

    await loadHistory();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Chat")),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: messages.length,
              itemBuilder: (_, i) {
                final m = messages[i];
                final isMe = m["sender"] == widget.api.loggedInUserId;

                return Align(
                  alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    padding: const EdgeInsets.all(10),
                    margin: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: isMe ? Colors.blue[300] : Colors.grey[300],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(m["content"]),
                  ),
                );
              },
            ),
          ),
          Row(
            children: [
              Expanded(child: TextField(controller: controller)),
              IconButton(
                icon: const Icon(Icons.send),
                onPressed: send,
              )
            ],
          ),
        ],
      ),
    );
  }
}
