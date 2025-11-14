import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'api/api_service.dart';
import 'screens/products_screen.dart';
import 'screens/suppliers_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final api = ApiService();
  await api.loadTokens();  // load saved session

  runApp(SupplierConsumerApp(api: api));
}

class SupplierConsumerApp extends StatelessWidget {
  final ApiService api;
  const SupplierConsumerApp({super.key, required this.api});

  @override
  Widget build(BuildContext context) {
    final bool isLoggedIn = api.accessToken != null;
    return MaterialApp(
      title: 'Supplier Consumer Platform',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        scaffoldBackgroundColor: Colors.white,
      ),
      home: isLoggedIn
          ? SuppliersScreen(api: api)
          : LoginScreen(api: api),
    );
  }
}
