import 'package:flutter/material.dart';
import '../api/api_service.dart';
import 'products_screen.dart';

class LoginScreen extends StatefulWidget {
  final ApiService api;
  const LoginScreen({super.key, required this.api});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _username = TextEditingController();
  final _password = TextEditingController();
  bool loading = false;

  ApiService get api => widget.api;

  Future<void> login() async {
    setState(() => loading = true);
    final success = await api.login(_username.text, _password.text);
    setState(() => loading = false);

    if (success) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => ProductsScreen(api: api)),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Invalid credentials")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Login")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(children: [
          TextField(controller: _username, decoration: const InputDecoration(labelText: "Username")),
          TextField(controller: _password, decoration: const InputDecoration(labelText: "Password"), obscureText: true),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: loading ? null : login,
            child: loading ? const CircularProgressIndicator() : const Text("Login"),
          ),
        ]),
      ),
    );
  }
}
