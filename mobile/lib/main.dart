import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const SupplierConsumerApp());
}

class SupplierConsumerApp extends StatelessWidget {
  const SupplierConsumerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Supplier Consumer Platform',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        scaffoldBackgroundColor: Colors.white,
      ),
      home: const LoginScreen(),
    );
  }
}
